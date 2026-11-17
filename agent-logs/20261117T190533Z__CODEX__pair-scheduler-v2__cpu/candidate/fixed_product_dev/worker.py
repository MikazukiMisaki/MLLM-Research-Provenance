"""One-arm worker for the fixed-product DEV comparison.

Requires a separately configured external budget owner and private, hashed
manifest. This module does not provide resource admission or launch authority.
"""

import argparse
import dataclasses
import hashlib
import json
import os
from pathlib import Path
import sys


def read_bound(path, digest, *, limit=16 * 1024 * 1024):
    fd = os.open(Path(path), os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        before = os.fstat(fd)
        if not 0 < before.st_size <= limit:
            raise ValueError("bound file size")
        parts = []
        remaining = before.st_size
        while remaining:
            block = os.read(fd, min(remaining, 65536))
            if not block:
                raise ValueError("short bound file")
            parts.append(block)
            remaining -= len(block)
        after = os.fstat(fd)
        if ((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns,
             before.st_ctime_ns) != (after.st_dev, after.st_ino, after.st_size,
                                      after.st_mtime_ns, after.st_ctime_ns)):
            raise ValueError("bound file changed while read")
        data = b"".join(parts)
        if hashlib.sha256(data).hexdigest() != digest:
            raise ValueError("bound file digest mismatch")
        return data
    finally:
        os.close(fd)


def main():
    # The parent bound is conservative; trusted real-worker binding and cleanup remain unreviewed.
    raise RuntimeError("RESEARCH_HOLD: production token provenance and cleanup gates are not implemented")
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--config-sha256", required=True)
    ap.add_argument("--budget-fd", required=True, type=int)
    args = ap.parse_args()
    config = json.loads(read_bound(args.config, args.config_sha256))
    manifest = json.loads(read_bound(config["manifest_path"], config["manifest_sha256"]))
    if manifest["schema"] != "FIXED_PRODUCT_FOUR_PAIR_DEV_V1":
        raise ValueError("protocol manifest schema")
    cases = manifest["cases"]
    if len(cases) != 4 or len({row["case"] for row in cases}) != 4:
        raise ValueError("four unique cases required")
    matches = [row for row in cases if row["case"] == config["case"]]
    if len(matches) != 1 or config["seed"] != manifest["env_seed"]:
        raise ValueError("case or seed binding")
    row = matches[0]
    index = cases.index(row)
    expected_order = ["P0", "CANDIDATE"] if index % 2 == 0 else ["CANDIDATE", "P0"]
    if row["order"] != expected_order or manifest["horizon"] != 50:
        raise ValueError("order or horizon mismatch")
    arm = config["arm"]
    previous_initial = config["previous_initial"]
    if arm == expected_order[0]:
        if previous_initial is not None:
            raise ValueError("first arm must not have a previous reset")
    elif arm == expected_order[1]:
        if not isinstance(previous_initial, dict):
            raise ValueError("second arm requires the first public reset")
    else:
        raise ValueError("arm is not in the fixed order")
    required_limits = {"episodes": 8, "generation": 400, "model_load": 8,
                       "reset": 8, "step": 400,
                       "materialize": 4, "env_construct": 8, "env_init": 8,
                       "input_tokens_per_generation": 4096,
                       "output_tokens_per_generation": 16}
    if manifest["limits"] != required_limits or config["limits"] != required_limits:
        raise ValueError("batch limits binding")
    output = Path(config["output"])
    if not output.is_absolute() or not output.is_dir() or any(output.iterdir()):
        raise ValueError("fresh private arm output required")
    legacy = Path(config["legacy_dir"])
    source = Path(config["source_root"])
    if not legacy.is_absolute() or not source.is_absolute():
        raise ValueError("absolute code roots required")
    for item in config["code_files"]:
        read_bound(item["path"], item["sha256"], limit=2 * 1024 * 1024)
    # Load our independent package separately from the pinned runtime's
    # self_improvement package so imports use the declared source root.
    sys.path[:0] = [str(Path(__file__).resolve().parents[1]), str(legacy), str(source / "src")]

    from fixed_product_dev.arm_stage import run_arm
    from fixed_product_dev.episode import run_episode
    from effect_ipc import Journal, EffectOwner, Controller
    from eprime_ports import verify_materialized, EPrimeEnvironment
    from environment_step import StepEnabledAuthoredEnv
    import source_worker
    from producer_port import ProducerPort
    from production_loader import load_frozen_adapter
    from self_improvement.si_p3.contract import PublicState, projection
    from self_improvement.si_transfer_eval.resource import SharedGPU
    from models.protocol_stability import parse_p2_selection

    runtime = config["runtime"]
    loads = 0

    def load_product(arm):
        nonlocal loads
        if arm not in ("P0", "CANDIDATE"):
            raise ValueError("unknown product")
        loads += 1
        if loads > 1:
            raise ValueError("arm model load limit")
        receipts = output / ("load-%d" % loads)
        receipts.mkdir(mode=0o700)
        resource = SharedGPU(expected_uuid=runtime["gpu_uuid"],
                             journal_path=receipts / "resource.jsonl", engineering_only=True)
        producer = None
        try:
            product = runtime["products"][arm]
            producer = load_frozen_adapter(
                arm="A" if arm == "P0" else "B",
                adapter_path=product["adapter_path"], adapter_sha256=product["adapter_tree_sha256"],
                base_path=runtime["base_path"], base_sha256=runtime["base_tree_sha256"],
                resource=resource, packages=runtime["packages"],
                runtime_identity=runtime["runtime_identity"], import_receipt_dir=receipts)
            return ProducerPort(producer, resource)
        except BaseException:
            if producer is not None:
                try:
                    producer.close()
                except BaseException:
                    pass
            try:
                resource.close()
            except BaseException:
                pass
            raise

    def parser(raw, actions):
        return parse_p2_selection(raw, actions, reflection_required=False)

    def state_factory(old, after):
        return PublicState(old.task_id, old.family, old.goal, after["observation"],
                           tuple(after["valid_actions"]), after["done"],
                           after["reward"], after["truncated"])

    case = dict(row, seed=manifest["env_seed"])
    run_arm(output=output, budget_fd=args.budget_fd, case=case, arm=arm,
            previous_initial=previous_initial, inputs=config["inputs"],
            seed=config["seed"], journal_class=Journal, owner_class=EffectOwner,
            controller_class=Controller, pair_binding=config["pair_binding"],
            verify_materialized=verify_materialized, environment_class=EPrimeEnvironment,
            step_wrapper=StepEnabledAuthoredEnv, episode=run_episode,
            projection=projection, source_worker=source_worker, load_producer=load_product,
            parser=parser, parse_value=dataclasses.asdict, state_factory=state_factory,
            expected_eos=config["expected_eos"], expected_pad=config["expected_pad"])


if __name__ == "__main__":
    main()
