#!/usr/bin/env python3
"""Read-only SI-S01 input binding capture; standard library only."""
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path


OWN = Path(__file__).resolve().parent
PROTOCOL = Path("/home/lizening/research-notes/agent-logs/2026-10-26T100859Z__SOL__si-p3-persistent-launch-coordination__f1a52e8c/ADOPTED_SOURCE_ONLY_PROTOCOL.md")
RESERVATIONS = Path("/home/lizening/research-notes/agent-logs/2026-10-25T084517Z__SOL__si-p3-controlled-experience-design__si3_7d91/ADOPTED_METADATA_RESERVATIONS.json")
E1_BINDINGS = Path("/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__LUNA__si-e1-token-runtime-audit__sie1_b8f6/input_bindings.json")
PROPOSAL = Path("/home/lizening/research-notes/agent-logs/2026-10-25T133918Z__LUNA__si-e2-engineering-probe__dfc00e49_7a61/SI_E2_PROPOSAL_REVISION_2.json")
ENV_PROPOSAL = Path("/home/lizening/research-notes/agent-logs/2026-10-25T133918Z__LUNA__si-e2-engineering-probe__dfc00e49_7a61/ENGINEERING_ENV_PROPOSAL_REVISION_2.json")
EXPECTED_ORDER_SHA = "40893826093d24bb111803a3532a260c2061c6c9b1c28b8d95c87000b3daa6c2"
FAMILIES = [
    "pick_and_place_simple",
    "pick_clean_then_place_in_recep",
    "pick_cool_then_place_in_recep",
    "pick_heat_then_place_in_recep",
    "pick_two_obj_and_place",
]
PINNED_PYTHON = Path("/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python")
EXPECTED_MODEL = Path("/home/lizening/.cache/huggingface/hub/models--Qwen--Qwen3-8B/snapshots/b968826d9c46dd6066d109eabc6255188de91218")
EXPECTED_ADAPTER = Path("/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/model-artifacts/sft-policy-bootstrap/full/final_adapter")
SOURCE_ROOT = Path("/home/lizening/wt-si-e2-cuda-uuid-compat")
ORIGINAL_ROOT = Path("/home/lizening/wt-r19-recovery-duration-v1")
SOCKET = Path("/home/lizening/.codex/app-server-control/forwarded-ssh-agent.sock")


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha_file(path):
    h = hashlib.sha256()
    with path.open("rb", buffering=0) as stream:
        while True:
            block = stream.read(1024 * 1024)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def file_binding(path):
    st = path.stat()
    return {"path": str(path), "exists": True, "bytes": st.st_size, "sha256": sha_file(path)}


def model_stat_tree(path, certified_group):
    rows = []
    for row in certified_group["files"]:
        p = Path(row["path"])
        try:
            ls = p.lstat()
            target = os.readlink(p) if stat.S_ISLNK(ls.st_mode) else None
            st = p.stat()
            rows.append({
                "path": str(p),
                "exists": True,
                "current_lstat_type": "symlink" if stat.S_ISLNK(ls.st_mode) else "regular" if stat.S_ISREG(ls.st_mode) else "other",
                "current_symlink_target": target,
                "current_target_bytes": st.st_size,
                "certified_bytes": row["bytes"],
                "size_matches_certified": st.st_size == row["bytes"],
                "mtime_ns": st.st_mtime_ns,
                "certified_sha256": row["sha256"],
                "current_content_rehashed": False,
            })
        except OSError as exc:
            rows.append({"path": str(p), "exists": False, "error_type": type(exc).__name__, "certified_bytes": row["bytes"], "certified_sha256": row["sha256"], "current_content_rehashed": False})
    return {"root": str(path), "certified_file_count": certified_group["file_count"], "current_stat_count": len(rows), "rows": rows}


def snapshot_regular_inputs(paths):
    return {str(p): file_binding(p) for p in paths}


def read_config_values(config_path):
    # Read only the original small YAML text and extract specific path fields; do not import YAML.
    lines = config_path.read_text(encoding="utf-8").splitlines()
    vals = {}
    section = None
    for line in lines:
        if line and not line[0].isspace() and line.rstrip().endswith(":"):
            section = line.strip()[:-1]
        m = re.match(r"^\s{2}(data_path|eval_id_data_path|eval_ood_data_path|domain|grammar):\s*(.*?)\s*$", line)
        if m:
            vals[f"{section}.{m.group(1)}"] = m.group(2)
    return vals


def main():
    start = {
        "protocol": file_binding(PROTOCOL),
        "reservations": file_binding(RESERVATIONS),
        "e1_bindings": file_binding(E1_BINDINGS),
        "proposal": file_binding(PROPOSAL),
        "environment_proposal": file_binding(ENV_PROPOSAL),
    }
    protocol_text = PROTOCOL.read_text(encoding="utf-8")
    reservations = json.loads(RESERVATIONS.read_text(encoding="utf-8"))
    e1 = json.loads(E1_BINDINGS.read_text(encoding="utf-8"))
    proposal = json.loads(PROPOSAL.read_text(encoding="utf-8"))
    env_proposal = json.loads(ENV_PROPOSAL.read_text(encoding="utf-8"))

    rows = [r for r in reservations["rows"] if r["partition"] == "acquisition_feasibility_96"]
    by_family = {family: [r for r in rows if r["family"] == family] for family in FAMILIES}
    ordered = []
    ranks = {}
    for family in FAMILIES:
        items = []
        for row in by_family[family]:
            task_id = row["identity"]
            rank_wire = f"SI-P3-prefix-v1\n{family}\n{task_id}\n".encode("utf-8")
            rank_hex = sha_bytes(rank_wire)
            ranks[task_id] = rank_hex
            items.append((rank_hex, task_id))
        ordered.extend(task_id for _, task_id in sorted(items))
    newline_no_tail = sha_bytes("\n".join(ordered).encode("utf-8"))
    newline_with_tail = sha_bytes(("\n".join(ordered) + "\n").encode("utf-8"))
    ordered_sha_match = EXPECTED_ORDER_SHA in {newline_no_tail, newline_with_tail}
    order_serialization = "no_trailing_newline" if newline_no_tail == EXPECTED_ORDER_SHA else "trailing_newline" if newline_with_tail == EXPECTED_ORDER_SHA else "unmatched"

    proposal_data_root = Path(proposal["environment"]["data_root"])
    config_path = Path(proposal["environment"]["config"])
    config_paths = read_config_values(config_path)
    train_root = Path(config_paths["dataset.data_path"])
    row_by_identity = {row["identity"]: row for row in rows}
    ordered_file_bindings = []
    for task_id in ordered:
        row = row_by_identity[task_id]
        family = row["family"]
        task_root = train_root / task_id
        for rel in ("game.tw-pddl", "traj_data.json"):
            p = task_root / rel
            try:
                st = p.stat()
                ordered_file_bindings.append({
                    "task_identity_sha256": sha_bytes(task_id.encode("utf-8")),
                    "family": family,
                    "relative_file": rel,
                    "path": str(p),
                    "exists": True,
                    "bytes": st.st_size,
                    "sha256": sha_file(p),
                    "content_parsed_or_printed": False,
                    "content_copied": False,
                })
            except OSError as exc:
                ordered_file_bindings.append({"task_identity_sha256": sha_bytes(task_id.encode("utf-8")), "family": family, "relative_file": rel, "path": str(p), "exists": False, "error_type": type(exc).__name__, "content_parsed_or_printed": False, "content_copied": False})

    base_group = e1["inputs_before"][str(EXPECTED_MODEL)]
    adapter_group = e1["inputs_before"][str(EXPECTED_ADAPTER)]
    model_stat = model_stat_tree(EXPECTED_MODEL, base_group)
    adapter_stat = model_stat_tree(EXPECTED_ADAPTER, adapter_group)

    package_bindings = []
    for name, info in sorted(proposal["packages"].items()):
        p = Path(info["path"])
        package_bindings.append({"module": name, **file_binding(p), "proposal_sha256": info["sha256"], "matches_proposal": sha_file(p) == info["sha256"], "version_from_prior_record": info.get("version")})

    project_modules = [
        SOURCE_ROOT / "src/self_improvement/si_p3/contract.py",
        ORIGINAL_ROOT / "src/env/alfworld.py",
    ]
    project_module_bindings = []
    for p in project_modules:
        if p.is_file():
            project_module_bindings.append(file_binding(p))
        else:
            project_module_bindings.append({"path": str(p), "exists": False})

    logic_paths = {
        "domain": Path(proposal["environment"]["logic_files"]["domain"]["path"]),
        "grammar": Path(proposal["environment"]["logic_files"]["grammar"]["path"]),
    }
    logic_bindings = {k: file_binding(p) for k, p in logic_paths.items()}
    config_binding = file_binding(config_path)
    python_binding = file_binding(PINNED_PYTHON)
    py_version = subprocess.run([str(PINNED_PYTHON), "-I", "--version"], capture_output=True, text=True, check=False)
    python_receipt = {"argv": [str(PINNED_PYTHON), "-I", "--version"], "returncode": py_version.returncode, "stdout": py_version.stdout, "stderr": py_version.stderr}

    socket_report = {"path": str(SOCKET), "env_matches": os.environ.get("SSH_AUTH_SOCK") == str(SOCKET), "checked_by_lstat_only": True}
    try:
        ss = SOCKET.lstat()
        socket_report.update({"exists": True, "type": "socket" if stat.S_ISSOCK(ss.st_mode) else "symlink" if stat.S_ISLNK(ss.st_mode) else "regular_or_other", "owner_uid": ss.st_uid, "mode": oct(stat.S_IMODE(ss.st_mode)), "readable": os.access(SOCKET, os.R_OK), "writable": os.access(SOCKET, os.W_OK)})
    except FileNotFoundError:
        socket_report.update({"exists": False, "type": "missing", "owner_uid": None, "readable": False, "writable": False})

    # Rehash all permitted non-weight files and A96 data bytes to detect concurrent drift.
    after = {
        "protocol": file_binding(PROTOCOL),
        "reservations": file_binding(RESERVATIONS),
        "e1_bindings": file_binding(E1_BINDINGS),
        "proposal": file_binding(PROPOSAL),
        "environment_proposal": file_binding(ENV_PROPOSAL),
        "config": file_binding(config_path),
        "logic": {k: file_binding(p) for k, p in logic_paths.items()},
        "packages": [{"module": x["module"], "path": x["path"], "bytes": x["bytes"], "sha256": sha_file(Path(x["path"]))} for x in package_bindings],
        "project_modules": [{"path": x["path"], "sha256": sha_file(Path(x["path"])) if x.get("exists") else None} for x in project_module_bindings],
        "a96_task_files": [{"path": x["path"], "bytes": Path(x["path"]).stat().st_size, "sha256": sha_file(Path(x["path"]))} if x.get("exists") else {"path": x["path"], "exists": False} for x in ordered_file_bindings],
    }
    a96_initial_by_path = {x["path"]: (x.get("bytes"), x.get("sha256")) for x in ordered_file_bindings}
    a96_after_by_path = {x["path"]: (x.get("bytes"), x.get("sha256")) for x in after["a96_task_files"]}
    a96_unchanged = a96_initial_by_path == a96_after_by_path
    core_unchanged = start == {"protocol": after["protocol"], "reservations": after["reservations"], "e1_bindings": after["e1_bindings"], "proposal": after["proposal"], "environment_proposal": after["environment_proposal"]}
    module_unchanged = all(x.get("exists") and x["sha256"] == y.get("sha256") for x, y in zip(project_module_bindings, after["project_modules"]))
    package_unchanged = all(x["sha256"] == y["sha256"] for x, y in zip(package_bindings, after["packages"]))
    logic_unchanged = all(logic_bindings[k]["sha256"] == after["logic"][k]["sha256"] for k in logic_bindings)
    config_unchanged = config_binding["sha256"] == after["config"]["sha256"]

    result = {
        "schema": "SI_S01_INPUT_HASH_READINESS_NOT_EXECUTABLE_V1",
        "status": "INPUT_HASHES_CAPTURED_SOURCE_SHA_PENDING_NOT_READY_FOR_LAUNCH",
        "source_SHA": "PENDING_FROZEN_EXACT_SHA",
        "software_review": "PENDING",
        "launch_clearance": "NOT_ISSUED",
        "protocol": start["protocol"],
        "reservation": {**start["reservations"], "partition": "acquisition_feasibility_96", "rows": len(rows), "family_counts": {f: len(by_family[f]) for f in FAMILIES}, "expected_ordered_task_newline_sha256": EXPECTED_ORDER_SHA, "computed_no_trailing_newline_sha256": newline_no_tail, "computed_trailing_newline_sha256": newline_with_tail, "matched_serialization": order_serialization, "ordered_task_sha256_matches_expected": ordered_sha_match, "rank_wire": "SHA256('SI-P3-prefix-v1\\n' + family + '\\n' + canonical_task_id + '\\n') then task_id lexical tie-break; family order is fixed FAMILIES list", "ordered_identity_list_written": False, "production_plan_created": False},
        "data": {"root": str(proposal_data_root), "root_is_directory": proposal_data_root.is_dir(), "yaml_config": config_binding, "yaml_selected_paths": config_paths, "task_tree": str(train_root), "task_tree_is_directory": train_root.is_dir(), "task_file_count_expected": len(rows) * 2, "task_files": ordered_file_bindings, "all_task_files_present": len(ordered_file_bindings) == 192 and all(x.get("exists") for x in ordered_file_bindings), "task_payloads_parsed_printed_or_copied": False},
        "runtime": {"pinned_interpreter": python_binding, "version_command_receipt": python_receipt, "packages": package_bindings, "module_origins_read_from_prior_binding_no_imports": True},
        "recorded_environment_plan_metadata_only": {"status": env_proposal.get("status"), "inherit_environment": env_proposal.get("inherit_environment"), "ALFWORLD_DATA": env_proposal.get("set", {}).get("ALFWORLD_DATA"), "unset_names": env_proposal.get("unset", []), "is_executable_or_released": False},
        "logic": logic_bindings,
        "project_source_modules_current_bytes": project_module_bindings,
        "model_and_adapter": {
            "base_revision": "b968826d9c46dd6066d109eabc6255188de91218",
            "adapter_tree_sha256_from_certified_manifest": e1["expected_adapter_tree_sha256"],
            "certified_manifest_path": str(E1_BINDINGS),
            "certified_manifest_sha256": start["e1_bindings"]["sha256"],
            "base": model_stat,
            "adapter": adapter_stat,
            "current_model_content_rehashed_or_loaded": False,
            "current_adapter_content_rehashed_or_loaded": False,
        },
        "socket_lstat_only": socket_report,
        "input_stability": {"core_manifest_inputs_unchanged": core_unchanged, "config_unchanged": config_unchanged, "logic_unchanged": logic_unchanged, "package_source_unchanged": package_unchanged, "listed_project_modules_unchanged": module_unchanged, "all_192_a96_task_files_unchanged_during_two_pass_hash": a96_unchanged},
        "not_performed": ["project imports", "project validators/tests", "tokenizer", "model/weights load", "CUDA/NVML", "environment construction/reset/step/replay", "SSH", "preflight/supervisor/launch", "new production plan/gate/argv/output identity"],
    }
    out = OWN / "INPUT_HASH_READINESS.json"
    out.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(out), "bytes": out.stat().st_size, "sha256": sha_file(out), "a96_rows": len(rows), "a96_task_files": len(ordered_file_bindings), "order_sha_matches": ordered_sha_match, "all_task_files_present": result["data"]["all_task_files_present"], "input_stability": result["input_stability"], "source_SHA": result["source_SHA"], "socket_type": socket_report["type"], "ssh_attempts": 0}, sort_keys=True))
    if not (ordered_sha_match and result["data"]["all_task_files_present"] and all(result["input_stability"].values())):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
