"""Only the jobs declared here are authorized software checks; never call a real probe."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,subprocess,sys,time
root=Path(__file__).resolve().parent
worktree=Path('/home/lizening/wt-si-e2-cuda-uuid-compat')
python='/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python'
job=sys.argv[1]
if job=='focused':
 files=['tests/test_si_e2_cuda_uuid_compat.py',*[str(p.relative_to(worktree)) for p in sorted((worktree/'tests').glob('test_si_p3_runtime_*.py'))]]
 argv=[python,'-m','pytest','-q','-p','no:cacheprovider','--basetemp=/tmp/si-e2-uuid-focused-dfc00e49','--junitxml='+str(root/'focused.xml'),*files]
elif job=='full':
 argv=[python,'-m','pytest','-q','-p','no:cacheprovider','--basetemp=/tmp/si-e2-uuid-full-dfc00e49','--junitxml='+str(root/'full.xml')]
elif job=='compile':
 argv=[python,'-I','-c',"from pathlib import Path; paths=[Path('src/self_improvement/si_p3/runtime_backend.py'),Path('tests/test_si_e2_cuda_uuid_compat.py')]; [compile(p.read_text(),str(p),'exec') for p in paths]; print('Compiled 2 changed/new Python files without pycache')"]
elif job=='diff_check':argv=['git','diff','--check','dfc00e49d1ef4d48453d2331507429f8a0c7bbc5','HEAD']
else:raise SystemExit('unknown software job')
env={'HOME':'/home/lizening','PATH':str(Path(python).parent)+':/usr/bin:/bin','LANG':'C.UTF-8','LC_ALL':'C.UTF-8','CUDA_VISIBLE_DEVICES':'','HF_HUB_OFFLINE':'1','HF_DATASETS_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1','TOKENIZERS_PARALLELISM':'false','PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':str(worktree/'src')+':'+str(worktree/'tests')}
pre=subprocess.run(['git','status','--porcelain=v1'],cwd=worktree,capture_output=True,text=True,check=True).stdout
sha=subprocess.run(['git','rev-parse','HEAD'],cwd=worktree,capture_output=True,text=True,check=True).stdout.strip()
if pre:raise SystemExit('refusing tests on dirty candidate: '+pre)
start=datetime.now(timezone.utc).isoformat();at=time.monotonic()
with (root/'receipts'/f'{job}.stdout').open('xb') as out,(root/'receipts'/f'{job}.stderr').open('xb') as err:
 result=subprocess.run(argv,cwd=worktree,env=env,stdout=out,stderr=err)
post=subprocess.run(['git','status','--porcelain=v1'],cwd=worktree,capture_output=True,text=True,check=True).stdout
receipt={'argv':argv,'cwd':str(worktree),'environment':env,'source_sha':sha,'started_utc':start,'ended_utc':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-at,'authentic_returncode':result.returncode,'pre_status':pre,'post_status':post,'scope':'production software tests only; external CUDA/8B/world edges fake; no execution release'}
for suffix in ('stdout','stderr'):
 p=root/'receipts'/f'{job}.{suffix}';receipt[suffix]={'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
with (root/'receipts'/f'{job}.receipt.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps(receipt,indent=2),flush=True)
print((root/'receipts'/f'{job}.stdout').read_text()[-4500:],flush=True)
sys.exit(result.returncode)
