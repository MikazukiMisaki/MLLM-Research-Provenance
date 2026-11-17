"""One fixed-product DEV arm in its own externally supervised process.

This is an implementation candidate, not an executable experiment on import.
The parent must bind the task, product, previous public reset, budget and GPU.
"""
from pathlib import Path
import hashlib
import os
import stat


ARM_CAPS = {"env_construct": 1, "env_init": 1,
            "reset": 1, "model_load": 1, "generation": 50, "step": 50}


def bound_paths(binding):
    """Check shared pair paths, exact bytes and lexical containment. Not OS isolation."""
    if type(binding) is not dict or set(binding)!={'root','game','config','data_root','sha256'}:
        raise ValueError('pair binding shape')
    root=Path(binding['root'])
    if not root.is_absolute() or '..' in root.parts or root.is_symlink():raise ValueError('pair root')
    game,config,data_root=(Path(binding[k]) for k in ('game','config','data_root'))
    if game!=data_root/'authored-eprime-only'/'game.tw-pddl':raise ValueError('pair layout')
    for path in (game,config,data_root):
        if not path.is_absolute() or '..' in path.parts or not path.is_relative_to(root):raise ValueError('pair containment')
        cursor=root
        for part in path.relative_to(root).parts:
            cursor=cursor/part
            if cursor.is_symlink():raise ValueError('symlink in pair path')
    files={'game':game,'routing':game.parent/'traj_data.json','config':config}
    if type(binding['sha256']) is not dict or set(binding['sha256'])!=set(files):raise ValueError('pair digest map')
    for name,path in files.items():
        fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
        try:
            before=os.fstat(fd)
            if not stat.S_ISREG(before.st_mode) or before.st_nlink!=1 or before.st_size>1_000_000:raise ValueError('pair file shape')
            with os.fdopen(fd,'rb',closefd=False) as f:data=f.read(1_000_001)
            after=os.fstat(fd)
            if ((before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)!=
                (after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns) or
                hashlib.sha256(data).hexdigest()!=binding['sha256'][name]):raise ValueError('pair file drift')
        finally:os.close(fd)
    return game,config,data_root


def run_arm(*, output, budget_fd, case, arm, previous_initial, inputs, seed,
            journal_class, owner_class, controller_class, pair_binding,
            verify_materialized, environment_class, step_wrapper, episode,
            projection, source_worker, load_producer, parser, parse_value,
            state_factory, expected_eos, expected_pad):
    if arm not in ("P0", "CANDIDATE") or arm not in case["order"]:
        raise ValueError("unexpected arm")
    if (set(inputs) != {"game", "routing", "config"} or
            {k: v["sha256"] for k, v in inputs.items()} != case["input_sha256"]):
        raise ValueError("case input hash mismatch")
    if type(seed) is not int or seed != case["seed"]:
        raise ValueError("case seed mismatch")
    if previous_initial is not None and not isinstance(previous_initial, dict):
        raise ValueError("previous initial state must be an object")
    output = Path(output)
    if not output.is_absolute() or not output.is_dir() or any(output.iterdir()):
        raise ValueError("fresh arm output required")
    journal = journal_class(output / "worker_events.jsonl", 64 * 1024 * 1024)
    owner = owner_class(budget_fd, journal, ARM_CAPS)
    controller = controller_class(owner)
    materialized = None
    post_verified = False
    finished = False
    try:
        journal.emit("fixed_product_arm_started", {
            "case": case["case"], "arm": arm, "seed": seed,
            "scope": "EXPOSED_AUTHORED_DEV", "horizon": 50})
        game, config, data_root = bound_paths(pair_binding)
        materialized = (game, config, data_root)
        verify_materialized(game, config, data_root, inputs, journal.emit, "pre")
        bound_paths(pair_binding)

        class BoundEnvironment:
            def __init__(self):
                self.inner = step_wrapper(environment_class(
                    game, config, data_root, seed, family="two", case_id=case["case"]))

            def initialize(self):
                return self.inner.initialize()

            def reset(self):
                result = self.inner.reset()
                if (type(result) is not tuple or len(result) != 3 or
                        getattr(result[0], "goal", None) != case["public_goal"] or
                        getattr(result[0], "family", None) != "pick_two_obj_and_place"):
                    raise ValueError("public goal or family mismatch")
                return result

            def step(self, action):
                return self.inner.step(action)

            def close(self):
                return self.inner.close()

        result = episode(
            arm=arm, previous_initial=previous_initial, controller=controller,
            env_factory=BoundEnvironment, load_producer=load_producer,
            projection=projection, source_worker=source_worker, parser=parser,
            parse_value=parse_value, state_factory=state_factory,
            expected_game=str(game), expected_eos=expected_eos, expected_pad=expected_pad)
        if (not isinstance(result, dict) or result.get("arm") != arm or
                not isinstance(result.get("initial_public"), dict)):
            raise ValueError("invalid arm outcome")
        verify_materialized(game, config, data_root, inputs, journal.emit, "post")
        bound_paths(pair_binding)
        post_verified = True
        journal.emit("fixed_product_arm_result", result)
        owner.finish("COMPLETED")
        finished = True
        return result
    except BaseException as error:
        if materialized is not None and not post_verified:
            try:
                verify_materialized(*materialized, inputs, journal.emit, "post")
            except BaseException as verification_error:
                try:
                    journal.emit("input_post_verification_failed", {"type": type(verification_error).__name__})
                except BaseException:
                    pass
        try:
            journal.emit("fixed_product_arm_stopped", {
                "type": type(error).__name__, "effects": "UNKNOWN_AS_NEEDED"})
        except BaseException:
            pass
        if not finished:
            try:
                owner.finish("STOPPED")
            except BaseException:
                pass
        raise
    finally:
        try:
            owner.close()
        finally:
            journal.close()
