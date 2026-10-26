from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,time
OWN=Path(__file__).resolve().parent;REPO=Path('/home/lizening/wt-si-s01-engineering-adapter');PY='/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python'
label='actual_reader_v1';sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip();before=subprocess.check_output(['git','status','--porcelain=v1'],cwd=REPO,text=True);assert not before
argv=[PY,'-I',str(OWN/'actual_reader_check.py'),str(REPO),str(OWN/(label+'.result.json'))]
env={'PATH':str(Path(PY).parent)+':/usr/bin:/bin','HOME':'/home/lizening','CUDA_VISIBLE_DEVICES':'','HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1','PYTHONDONTWRITEBYTECODE':'1','TOKENIZERS_PARALLELISM':'false','LANG':'C.UTF-8'};at=time.monotonic();utc=datetime.now(timezone.utc).isoformat()
with (OWN/'receipts'/(label+'.stdout')).open('xb') as out,(OWN/'receipts'/(label+'.stderr')).open('xb') as err:r=subprocess.run(argv,cwd=REPO,env=env,stdout=out,stderr=err,timeout=120)
receipt={'argv':argv,'source_sha':sha,'cwd':str(REPO),'started_utc':utc,'authentic_returncode':r.returncode,'elapsed_seconds':time.monotonic()-at,'pre_status':before,'post_status':subprocess.check_output(['git','status','--porcelain=v1'],cwd=REPO,text=True),'scope':'Authorized model-free original first-source nine-slice production reader only, actual MODE/constants, no preflight/runtime/validator/analyzer/model/env/science'}
for suffix in ('stdout','stderr'):
 p=OWN/'receipts'/(label+'.'+suffix);b=p.read_bytes();receipt[suffix]={'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
(OWN/'receipts'/(label+'.json')).write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt));print((OWN/'receipts'/(label+'.stdout')).read_text());print((OWN/'receipts'/(label+'.stderr')).read_text());raise SystemExit(r.returncode)
