from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys,time
root=Path(__file__).resolve().parent;repo=Path('/home/lizening/wt-si-p3-source-only-v2')
label=sys.argv[1];which=sys.argv[2]
python='/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python'
pre=subprocess.check_output(['git','status','--porcelain=v1'],cwd=repo,text=True)
if pre:raise SystemExit('dirty candidate refused: '+pre)
sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()
if which=='focused':
 argv=[python,'-m','pytest','-q','-p','no:cacheprovider','--basetemp=/tmp/si-s01-'+label,'--junitxml='+str(root/(label+'.xml')),*[str(p.relative_to(repo)) for p in sorted((repo/'tests').glob('test_si_s01*.py'))]]
elif which=='full':argv=[python,'-m','pytest','-q','-p','no:cacheprovider','--basetemp=/tmp/si-s01-'+label,'--junitxml='+str(root/(label+'.xml'))]
else:raise SystemExit('unknown job')
env={'HOME':'/home/lizening','PATH':str(Path(python).parent)+':/usr/bin:/bin','LANG':'C.UTF-8','LC_ALL':'C.UTF-8','CUDA_VISIBLE_DEVICES':'','HF_HUB_OFFLINE':'1','HF_DATASETS_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1','TOKENIZERS_PARALLELISM':'false','PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':str(repo/'src')+':'+str(repo/'tests')}
start=datetime.now(timezone.utc).isoformat();at=time.monotonic()
with (root/'receipts'/(label+'.stdout')).open('xb') as out,(root/'receipts'/(label+'.stderr')).open('xb') as err:r=subprocess.run(argv,cwd=repo,env=env,stdout=out,stderr=err)
post=subprocess.check_output(['git','status','--porcelain=v1'],cwd=repo,text=True)
receipt={'argv':argv,'cwd':str(repo),'environment':env,'source_sha':sha,'started_utc':start,'elapsed_seconds':time.monotonic()-at,'authentic_returncode':r.returncode,'pre_status':pre,'post_status':post,'scope':'software fixtures only; no real tokenizer/CUDA/8B/ALFWorld/SSH/preflight/science'}
for suffix in ('stdout','stderr'):
 p=root/'receipts'/(label+'.'+suffix);receipt[suffix]={'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
with (root/'receipts'/(label+'.json')).open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps(receipt,indent=2));print((root/'receipts'/(label+'.stdout')).read_text()[-9000:]);sys.exit(r.returncode)
