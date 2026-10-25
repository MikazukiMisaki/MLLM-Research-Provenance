#!/usr/bin/env python3
"""Read installed package metadata only; imports no model/environment libraries."""
import hashlib,json,os,subprocess,sys,time
from datetime import datetime,timezone
from pathlib import Path
OWN=Path(__file__).resolve().parent; RAW=OWN/'raw'; RAW.mkdir(exist_ok=True)
code="""import importlib.metadata as m,json,sys
names=['torch','transformers','tokenizers','trl','peft','accelerate','datasets','safetensors','huggingface_hub','numpy','PyYAML','alfworld','textworld','gym','gymnasium','spacy']
out={}
for n in names:
 try:
  d=m.distribution(n); out[n]={'version':d.version,'origin':str(d.locate_file(''))}
 except m.PackageNotFoundError: out[n]={'version':None,'origin':None}
print(json.dumps({'python':sys.version,'packages':out},sort_keys=True))"""
argv=['/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python','-I','-c',code]
env={k:os.environ[k] for k in ('PATH','LANG','LC_ALL','HOME','USER') if k in os.environ}; env['PYTHONNOUSERSITE']='1'
start=datetime.now(timezone.utc).isoformat(); t=time.monotonic_ns()
try:
 p=subprocess.run(argv,cwd='/home/lizening/Alfworld-Self-Improvement-Project',env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False); rc,out,err=p.returncode,p.stdout,p.stderr
except Exception as e: rc,out,err=None,b'',(type(e).__name__+': '+str(e)).encode()
end=datetime.now(timezone.utc).isoformat(); elapsed=(time.monotonic_ns()-t)/1e9
op=RAW/'environment_packages.stdout.bin'; ep=RAW/'environment_packages.stderr.bin'; op.write_bytes(out); ep.write_bytes(err)
rec={'schema':'SI_E2_PACKAGE_METADATA_RECEIPT_V1','argv':argv,'cwd':'/home/lizening/Alfworld-Self-Improvement-Project','started_utc':start,'ended_utc':end,'monotonic_elapsed_seconds':elapsed,'returncode':rc,'stdout':{'path':str(op),'bytes':len(out),'sha256':hashlib.sha256(out).hexdigest()},'stderr':{'path':str(ep),'bytes':len(err),'sha256':hashlib.sha256(err).hexdigest()}}
(OWN/'environment_packages_receipt.json').write_text(json.dumps(rec,sort_keys=True,indent=2)+'\n')
if rc: sys.exit(rc)
(OWN/'ENVIRONMENT_PACKAGES.json').write_text(json.dumps(json.loads(out),sort_keys=True,indent=2)+'\n')
print(json.dumps({'returncode':rc,'package_count':len(json.loads(out)['packages']),'receipt':str(OWN/'environment_packages_receipt.json')},sort_keys=True))
