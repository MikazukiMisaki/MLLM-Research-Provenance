#!/usr/bin/env python3
"""Capture safe metadata-only output for the predetermined source replay candidate."""
import hashlib,json,os,subprocess,sys,time
from datetime import datetime,timezone
from pathlib import Path
OWN=Path(__file__).resolve().parent; RAW=OWN/'raw'; RAW.mkdir(exist_ok=True)
PY='/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python'
argv=[PY,'-I',str(OWN/'inspect_first_source.py')]
env={k:os.environ[k] for k in ('PATH','LANG','LC_ALL','HOME','USER') if k in os.environ}; env['PYTHONNOUSERSITE']='1'
start=datetime.now(timezone.utc).isoformat(); t=time.monotonic_ns()
try:
 p=subprocess.run(argv,cwd='/home/lizening/Alfworld-Self-Improvement-Project',env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False); rc,out,err=p.returncode,p.stdout,p.stderr
except Exception as e: rc,out,err=None,b'',(type(e).__name__+': '+str(e)).encode()
end=datetime.now(timezone.utc).isoformat(); elapsed=(time.monotonic_ns()-t)/1e9
op=RAW/'source_candidate_v3.stdout.bin'; ep=RAW/'source_candidate_v3.stderr.bin'; op.write_bytes(out); ep.write_bytes(err)
rec={'schema':'SI_E2_SOURCE_CANDIDATE_CAPTURE_RECEIPT_V1','argv':argv,'cwd':'/home/lizening/Alfworld-Self-Improvement-Project','started_utc':start,'ended_utc':end,'monotonic_elapsed_seconds':elapsed,'returncode':rc,'stdout':{'path':str(op),'bytes':len(out),'sha256':hashlib.sha256(out).hexdigest()},'stderr':{'path':str(ep),'bytes':len(err),'sha256':hashlib.sha256(err).hexdigest()}}
(OWN/'source_candidate_v3_receipt.json').write_text(json.dumps(rec,sort_keys=True,indent=2)+'\n')
if rc: sys.exit(rc)
try:
 candidate=json.loads(out)
 (OWN/'FIRST_SOURCE_REPLAY_CANDIDATE_V3.json').write_text(json.dumps(candidate,sort_keys=True,indent=2)+'\n')
except Exception as e:
 print(type(e).__name__+': '+str(e),file=sys.stderr); sys.exit(2)
print(json.dumps({'returncode':rc,'source_record_sha256':candidate['source_record']['line_sha256'],'trajectory_file_sha256':candidate['source_record']['trajectory_file']['sha256'],'output':str(OWN/'FIRST_SOURCE_REPLAY_CANDIDATE_V3.json')},sort_keys=True))
