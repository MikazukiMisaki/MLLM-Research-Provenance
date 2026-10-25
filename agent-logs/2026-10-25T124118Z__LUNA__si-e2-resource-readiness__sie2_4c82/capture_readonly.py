#!/usr/bin/env python3
"""Capture bounded, non-science host and repository inspection commands."""
import hashlib
import json
import os
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

OWN = Path(__file__).resolve().parent
RAW = OWN / "raw"
RAW.mkdir(exist_ok=True)
PYTHON = "/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python"
PROJECT = "/home/lizening/Alfworld-Self-Improvement-Project"
G3 = "/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z"
ADAPTER = "/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/model-artifacts/sft-policy-bootstrap/full/final_adapter"
SNAPSHOT = "/home/lizening/.cache/huggingface/hub/models--Qwen--Qwen3-8B/snapshots/b968826d9c46dd6066d109eabc6255188de91218"

COMMANDS = [
    ("gpu_inventory", ["nvidia-smi", "--query-gpu=index,uuid,name,driver_version,memory.total,memory.used,memory.free,compute_mode,pci.bus_id", "--format=csv,noheader"], "/"),
    ("gpu_compute_processes", ["nvidia-smi", "--query-compute-apps=gpu_uuid,pid,process_name,used_memory", "--format=csv,noheader"], "/"),
    ("gpu_mig_compute", ["nvidia-smi", "-q", "-d", "MIG,COMPUTE"], "/"),
    ("ram_inventory", ["free", "-b"], "/"),
    ("cpu_inventory", ["lscpu"], "/"),
    ("disk_relevant_paths", ["df", "-B1", "-P", "/", "/home/lizening/.cache/huggingface", ADAPTER, G3], "/"),
    ("project_head", ["git", "-C", PROJECT, "rev-parse", "HEAD"], PROJECT),
    ("project_status", ["git", "-C", PROJECT, "status", "--short", "--branch"], PROJECT),
    ("project_worktrees", ["git", "-C", PROJECT, "worktree", "list", "--porcelain"], PROJECT),
    ("a995_object", ["git", "-C", PROJECT, "cat-file", "-t", "a995d4c3c5f7d31a2cf1fd0afc4bfa4bd72ee3a3"], PROJECT),
    ("g3_tree_inventory", ["find", G3, "-maxdepth", "3", "-type", "f", "-printf", "%P\\t%s\\n"], "/"),
    ("pinned_package_probe", [PYTHON, "-I", "-c", "import importlib.metadata as m,json,sys; names=['torch','transformers','tokenizers','trl','peft','accelerate','datasets','safetensors','huggingface_hub','numpy','PyYAML']; out={};\nfor n in names:\n d=m.distribution(n); out[n]={'version':d.version,'origin':str(d.locate_file(''))}\nprint(json.dumps({'python':sys.version,'packages':out},sort_keys=True))"], PROJECT),
]

env = {k: os.environ[k] for k in ("PATH", "LANG", "LC_ALL", "HOME", "USER") if k in os.environ}
env.update({"PYTHONNOUSERSITE": "1", "CUDA_DEVICE_ORDER": "PCI_BUS_ID"})
records = []
for name, argv, cwd in COMMANDS:
    start = datetime.now(timezone.utc).isoformat()
    t0 = time.monotonic_ns()
    try:
        cp = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        rc = cp.returncode
        stdout, stderr = cp.stdout, cp.stderr
    except Exception as exc:
        rc = None
        stdout, stderr = b"", (type(exc).__name__ + ": " + str(exc)).encode()
    elapsed = (time.monotonic_ns() - t0) / 1e9
    end = datetime.now(timezone.utc).isoformat()
    outp, errp = RAW / f"{name}.stdout.bin", RAW / f"{name}.stderr.bin"
    outp.write_bytes(stdout)
    errp.write_bytes(stderr)
    records.append({
        "name": name, "argv": argv, "cwd": cwd, "started_utc": start, "ended_utc": end,
        "monotonic_elapsed_seconds": elapsed, "returncode": rc,
        "stdout": {"path": str(outp), "bytes": len(stdout), "sha256": hashlib.sha256(stdout).hexdigest()},
        "stderr": {"path": str(errp), "bytes": len(stderr), "sha256": hashlib.sha256(stderr).hexdigest()},
    })
receipt = {"schema": "SI_E2_READ_ONLY_HOST_CAPTURE_V1", "commands": records}
(OWN / "host_inspection_receipts.json").write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"commands": len(records), "returncodes": {r['name']: r['returncode'] for r in records}, "receipt": str(OWN / 'host_inspection_receipts.json')}, sort_keys=True))
