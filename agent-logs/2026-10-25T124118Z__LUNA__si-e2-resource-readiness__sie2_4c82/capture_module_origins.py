#!/usr/bin/env python3
"""Capture interpreter-resolved package origins without importing runtimes."""
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

OWN = Path(__file__).resolve().parent
RAW = OWN / "raw"
RAW.mkdir(exist_ok=True)
PYTHON = "/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python"
CODE = r'''import importlib.util,json,sys
modules={"torch":"torch","transformers":"transformers","peft":"peft","alfworld":"alfworld","textworld":"textworld","PyYAML":"yaml"}
out={"python_executable":sys.executable,"python_version":sys.version,"modules":{}}
for key,name in modules.items():
 spec=importlib.util.find_spec(name)
 out["modules"][key]={"module_name":name,"origin":None if spec is None else spec.origin,"search_locations":None if spec is None or spec.submodule_search_locations is None else list(spec.submodule_search_locations)}
print(json.dumps(out,sort_keys=True))'''
ARGV = [PYTHON, "-I", "-c", CODE]
ENV = {k: os.environ[k] for k in ("PATH", "LANG", "LC_ALL", "HOME", "USER") if k in os.environ}
ENV["PYTHONNOUSERSITE"] = "1"
START = datetime.now(timezone.utc).isoformat()
T0 = time.monotonic_ns()
try:
    p = subprocess.run(ARGV, cwd="/home/lizening/Alfworld-Self-Improvement-Project", env=ENV,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    RC, OUT, ERR = p.returncode, p.stdout, p.stderr
except Exception as exc:
    RC, OUT, ERR = None, b"", (type(exc).__name__ + ": " + str(exc)).encode()
END = datetime.now(timezone.utc).isoformat()
ELAPSED = (time.monotonic_ns() - T0) / 1e9
OUT_PATH, ERR_PATH = RAW / "module_origins.stdout.bin", RAW / "module_origins.stderr.bin"
OUT_PATH.write_bytes(OUT)
ERR_PATH.write_bytes(ERR)
receipt = {
    "schema": "SI_E2_MODULE_ORIGINS_CAPTURE_V1", "argv": ARGV,
    "cwd": "/home/lizening/Alfworld-Self-Improvement-Project",
    "environment_allowlist": sorted(ENV), "pythonpath_unset": True,
    "started_utc": START, "ended_utc": END, "monotonic_elapsed_seconds": ELAPSED,
    "returncode": RC,
    "stdout": {"path": str(OUT_PATH), "bytes": len(OUT), "sha256": hashlib.sha256(OUT).hexdigest()},
    "stderr": {"path": str(ERR_PATH), "bytes": len(ERR), "sha256": hashlib.sha256(ERR).hexdigest()},
}
(OWN / "module_origins_receipt.json").write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n")
if RC == 0:
    (OWN / "MODULE_ORIGINS.json").write_text(json.dumps(json.loads(OUT), sort_keys=True, indent=2) + "\n")
print(json.dumps({"returncode": RC, "receipt": str(OWN / "module_origins_receipt.json")}, sort_keys=True))
sys.exit(0 if RC == 0 else 1)
