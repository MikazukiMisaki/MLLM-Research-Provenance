#!/usr/bin/env python3
"""Capture actual helper SHA output, return code, timing and raw streams."""
import hashlib,json,os,subprocess,sys,time
from datetime import datetime,timezone
from pathlib import Path
OWN=Path(__file__).resolve().parent; RAW=OWN/'raw'; RAW.mkdir(exist_ok=True)
PY='/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python'
argv=[PY,'-I',str(OWN/'hash_runtime_inputs.py')]
env={k:os.environ[k] for k in ('PATH','LANG','LC_ALL','HOME','USER') if k in os.environ}; env['PYTHONNOUSERSITE']='1'
start=datetime.now(timezone.utc).isoformat(); t=time.monotonic_ns()
try:
 p=subprocess.run(argv,cwd='/home/lizening/Alfworld-Self-Improvement-Project',env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False); rc,out,err=p.returncode,p.stdout,p.stderr
except Exception as e: rc,out,err=None,b'',(type(e).__name__+': '+str(e)).encode()
end=datetime.now(timezone.utc).isoformat(); elapsed=(time.monotonic_ns()-t)/1e9
op=RAW/'runtime_hashes.stdout.bin'; ep=RAW/'runtime_hashes.stderr.bin'; op.write_bytes(out); ep.write_bytes(err)
rec={'schema':'SI_E2_RUNTIME_HASH_CAPTURE_RECEIPT_V1','argv':argv,'cwd':'/home/lizening/Alfworld-Self-Improvement-Project','started_utc':start,'ended_utc':end,'monotonic_elapsed_seconds':elapsed,'returncode':rc,'stdout':{'path':str(op),'bytes':len(out),'sha256':hashlib.sha256(out).hexdigest()},'stderr':{'path':str(ep),'bytes':len(err),'sha256':hashlib.sha256(err).hexdigest()}}
(OWN/'runtime_hashes_receipt.json').write_text(json.dumps(rec,sort_keys=True,indent=2)+'\n')
if rc: sys.exit(rc)
print(json.dumps({'returncode':rc,'hash_inventory_sha256':hashlib.sha256(out).hexdigest(),'receipt':str(OWN/'runtime_hashes_receipt.json')},sort_keys=True))
