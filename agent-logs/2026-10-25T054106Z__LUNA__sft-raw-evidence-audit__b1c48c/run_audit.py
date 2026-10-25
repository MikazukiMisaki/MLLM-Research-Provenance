#!/usr/bin/env python3
"""Capture an authentic subprocess receipt for the stdlib-only audit."""
import datetime
import hashlib
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path("/home/lizening/research-notes/agent-logs/2026-10-25T054106Z__LUNA__sft-raw-evidence-audit__b1c48c")
SCRIPT = ROOT / "audit_sft_raw.py"
cmd = [sys.executable, str(SCRIPT)]
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
p = subprocess.run(cmd, cwd="/home/lizening/wt-codex-r18c2", text=True, capture_output=True, check=False)
end = datetime.datetime.now(datetime.timezone.utc).isoformat()
receipt = {
    "command": cmd,
    "cwd": "/home/lizening/wt-codex-r18c2",
    "pid": os.getpid(),
    "child_returncode": p.returncode,
    "started_at_utc": start,
    "finished_at_utc": end,
    "python_executable": sys.executable,
    "python_version": sys.version,
    "stdout": p.stdout,
    "stderr": p.stderr,
    "stdout_sha256": hashlib.sha256(p.stdout.encode()).hexdigest(),
    "stderr_sha256": hashlib.sha256(p.stderr.encode()).hexdigest(),
}
(ROOT / "audit_subprocess_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: receipt[k] for k in ("command", "cwd", "pid", "child_returncode", "started_at_utc", "finished_at_utc", "python_executable", "stdout_sha256", "stderr_sha256")}, indent=2))
if p.stdout:
    print(p.stdout)
if p.stderr:
    print("STDERR:\n" + p.stderr, file=sys.stderr)
raise SystemExit(p.returncode)
