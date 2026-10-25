#!/usr/bin/env python3
"""Run the read-only worker once, preserving actual child argv/env/output/exit."""
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

OWN = Path(__file__).resolve().parent
EXPECTED = Path("/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__LUNA__si-e1-token-runtime-audit__sie1_b8f6").resolve()
assert OWN == EXPECTED
PYTHON = Path("/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python")
PROJECT = Path("/home/lizening/Alfworld-Self-Improvement-Project")
RAW = OWN / "raw"
RAW.mkdir(exist_ok=True)

attempts = sorted(RAW.glob("audit_worker_*.stdout.bin"))
attempt = len(attempts) + 1
tag = f"audit_worker_{attempt:03d}"
argv = [str(PYTHON), "-I", str(OWN / "audit_worker.py")]
env = os.environ.copy()
removed = []
for name in ("PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP", "VIRTUAL_ENV"):
    if name in env:
        env.pop(name)
        removed.append(name)
env.update({
    "PYTHONNOUSERSITE": "1",
    "HF_HUB_OFFLINE": "1",
    "TRANSFORMERS_OFFLINE": "1",
    "HF_DATASETS_OFFLINE": "1",
    "HF_HOME": "/home/lizening/.cache/huggingface",
    "HF_HUB_CACHE": "/home/lizening/.cache/huggingface/hub",
    "TOKENIZERS_PARALLELISM": "false",
    "CUDA_VISIBLE_DEVICES": "",
})
started_utc = datetime.now(timezone.utc).isoformat()
started_monotonic = time.monotonic_ns()
proc = subprocess.Popen(argv, cwd=str(PROJECT), env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = proc.communicate()
ended_monotonic = time.monotonic_ns()
ended_utc = datetime.now(timezone.utc).isoformat()
(RAW / f"{tag}.stdout.bin").write_bytes(stdout)
(RAW / f"{tag}.stderr.bin").write_bytes(stderr)
receipt = {
    "attempt": attempt,
    "argv": argv,
    "cwd": str(PROJECT),
    "pid": proc.pid,
    "started_utc": started_utc,
    "ended_utc": ended_utc,
    "monotonic_elapsed_seconds": (ended_monotonic - started_monotonic) / 1e9,
    "returncode": proc.returncode,
    "environment_policy": {
        "python_path_vars_removed": removed,
        "PYTHONPATH": "unset",
        "PYTHONHOME": "unset",
        "PYTHONNOUSERSITE": env["PYTHONNOUSERSITE"],
        "HF_HUB_OFFLINE": env["HF_HUB_OFFLINE"],
        "TRANSFORMERS_OFFLINE": env["TRANSFORMERS_OFFLINE"],
        "HF_DATASETS_OFFLINE": env["HF_DATASETS_OFFLINE"],
        "HF_HOME": env["HF_HOME"],
        "HF_HUB_CACHE": env["HF_HUB_CACHE"],
        "TOKENIZERS_PARALLELISM": env["TOKENIZERS_PARALLELISM"],
        "CUDA_VISIBLE_DEVICES": "empty; GPU hidden",
        "full_environment_dump": False,
    },
    "stdout": {"path": str(RAW / f"{tag}.stdout.bin"), "bytes": len(stdout), "sha256": hashlib.sha256(stdout).hexdigest()},
    "stderr": {"path": str(RAW / f"{tag}.stderr.bin"), "bytes": len(stderr), "sha256": hashlib.sha256(stderr).hexdigest()},
}
receipt_path = OWN / f"{tag}.receipt.json"
receipt_path.write_text(json.dumps(receipt, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
sys.stdout.write(stdout.decode("utf-8", errors="replace"))
sys.stderr.write(stderr.decode("utf-8", errors="replace"))
print(json.dumps({"attempt": attempt, "returncode": proc.returncode, "stdout_sha256": receipt["stdout"]["sha256"], "stderr_sha256": receipt["stderr"]["sha256"], "receipt": str(receipt_path)}, sort_keys=True))
sys.exit(proc.returncode)
