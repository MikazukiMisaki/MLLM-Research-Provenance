from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,time
OWN=Path(__file__).resolve().parent;REPO=Path('/home/lizening/wt-si-p3-source-only-v2');BASE='844cc4b78df1f83e29391ffd5ab861a2d0c0a3fd';PY='/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python'
files=subprocess.check_output(['git','diff','--name-only',BASE,'HEAD'],cwd=REPO,text=True).splitlines();files=[x for x in files if x.endswith('.py')]
code="from pathlib import Path;import json,py_compile,sys;fs=json.loads(sys.argv[1]);d=Path('/tmp/si-s01-rt-final-pycompile');d.mkdir(exist_ok=True);[py_compile.compile(f,cfile=str(d/(str(i)+'.pyc')),doraise=True) for i,f in enumerate(fs)];print('compiled',len(fs),'new Python files')"
checks=[('rt_final_compile',[PY,'-I','-c',code,json.dumps([str(REPO/p) for p in files])]),('rt_final_diff_check',['git','diff','--check',BASE,'HEAD']),('rt_final_path_credential_scan',['rg','-n','/home/|/tmp/|/mnt/|api[_-]?key|BEGIN .*PRIVATE KEY|hf_[A-Za-z0-9]{12}',*subprocess.check_output(['git','diff','--name-only',BASE,'HEAD'],cwd=REPO,text=True).splitlines()])]
env=dict(os.environ);env.update(CUDA_VISIBLE_DEVICES='',PYTHONDONTWRITEBYTECODE='1',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1')
for label,argv in checks:
 before=subprocess.check_output(['git','status','--porcelain=v1'],cwd=REPO,text=True);assert not before
 at=time.monotonic();started=datetime.now(timezone.utc).isoformat()
 with (OWN/'receipts'/(label+'.stdout')).open('xb') as out,(OWN/'receipts'/(label+'.stderr')).open('xb') as err:r=subprocess.run(argv,cwd=REPO,env=env,stdout=out,stderr=err)
 after=subprocess.check_output(['git','status','--porcelain=v1'],cwd=REPO,text=True)
 value={'argv':argv,'cwd':str(REPO),'source_sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),'started_utc':started,'authentic_returncode':r.returncode,'elapsed_seconds':time.monotonic()-at,'pre_status':before,'post_status':after,'expected_returncode':1 if label.endswith('scan') else 0}
 for suffix in ('stdout','stderr'):
  p=OWN/'receipts'/(label+'.'+suffix);b=p.read_bytes();value[suffix]={'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 with (OWN/'receipts'/(label+'.json')).open('x') as f:json.dump(value,f,indent=2);f.write('\n')
 print(json.dumps({'label':label,'returncode':r.returncode}));assert r.returncode==value['expected_returncode'] and not after
