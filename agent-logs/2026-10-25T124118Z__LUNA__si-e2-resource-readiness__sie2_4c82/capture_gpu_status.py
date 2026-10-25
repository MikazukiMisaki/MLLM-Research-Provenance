#!/usr/bin/env python3
"""Capture driver-supported GPU display/MIG query without changing device state."""
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
COMMANDS = [
    ("gpu_default_display", ["nvidia-smi"], "/"),
    ("gpu_mig_mode_query", ["nvidia-smi", "--query-gpu=mig.mode.current,mig.mode.pending", "--format=csv,noheader"], "/"),
    ("gpu_full_status", ["nvidia-smi", "-q"], "/"),
    ("scheduler_binary_presence", ["bash", "-lc", "for x in squeue scontrol qstat; do command -v \"$x\" || true; done"], "/"),
]
env = {k: os.environ[k] for k in ("PATH", "LANG", "LC_ALL", "HOME", "USER") if k in os.environ}
records = []
for name, argv, cwd in COMMANDS:
    start = datetime.now(timezone.utc).isoformat()
    t0 = time.monotonic_ns()
    try:
        cp = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        rc, stdout, stderr = cp.returncode, cp.stdout, cp.stderr
    except Exception as exc:
        rc, stdout, stderr = None, b"", (type(exc).__name__ + ": " + str(exc)).encode()
    end = datetime.now(timezone.utc).isoformat()
    elapsed = (time.monotonic_ns() - t0) / 1e9
    outp, errp = RAW / f"{name}.stdout.bin", RAW / f"{name}.stderr.bin"
    outp.write_bytes(stdout); errp.write_bytes(stderr)
    records.append({"name":name,"argv":argv,"cwd":cwd,"started_utc":start,"ended_utc":end,
        "monotonic_elapsed_seconds":elapsed,"returncode":rc,
        "stdout":{"path":str(outp),"bytes":len(stdout),"sha256":hashlib.sha256(stdout).hexdigest()},
        "stderr":{"path":str(errp),"bytes":len(stderr),"sha256":hashlib.sha256(stderr).hexdigest()}})
(OWN / "gpu_status_receipts.json").write_text(json.dumps({"schema":"SI_E2_GPU_STATUS_CAPTURE_V1","commands":records},sort_keys=True,indent=2)+"\n")
print(json.dumps({"returncodes":{r['name']:r['returncode'] for r in records},"receipt":str(OWN/"gpu_status_receipts.json")},sort_keys=True))
