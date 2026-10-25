#!/usr/bin/env python3
import hashlib, json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
OWN=Path(__file__).resolve().parent
assert OWN == Path("/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__LUNA__si-e1-token-runtime-audit__sie1_b8f6").resolve()
argv=[sys.executable,"-I",str(OWN/"finalize_audit.py")]
env={k:v for k,v in __import__("os").environ.items() if k not in {"PYTHONPATH","PYTHONHOME","PYTHONSTARTUP","VIRTUAL_ENV"}}
start=datetime.now(timezone.utc).isoformat()
p=subprocess.run(argv,cwd=str(OWN),env=env,capture_output=True,text=True,check=False)
end=datetime.now(timezone.utc).isoformat()
receipt={"argv":argv,"cwd":str(OWN),"started_utc":start,"ended_utc":end,"returncode":p.returncode,"stdout":p.stdout,"stderr":p.stderr,"stdout_sha256":hashlib.sha256(p.stdout.encode()).hexdigest(),"stderr_sha256":hashlib.sha256(p.stderr.encode()).hexdigest()}
(OWN/"finalize_audit.receipt.json").write_text(json.dumps(receipt,sort_keys=True,indent=2)+"\n")
sys.stdout.write(p.stdout); sys.stderr.write(p.stderr); sys.exit(p.returncode)
