from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys,time
OWN=Path(__file__).resolve().parent;REPO=Path('/home/lizening/wt-si-s01-engineering-adapter');PY='/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python'
label=sys.argv[1];targets=sys.argv[2:];assert targets
status=subprocess.check_output(['git','status','--porcelain=v1'],cwd=REPO,text=True);sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
env={'HOME':'/home/lizening','PATH':str(Path(PY).parent)+':/usr/bin:/bin','LANG':'C.UTF-8','LC_ALL':'C.UTF-8','CUDA_VISIBLE_DEVICES':'','HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1','TOKENIZERS_PARALLELISM':'false','PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':str(REPO/'src')+':'+str(REPO/'tests')}
argv=[PY,'-m','pytest','-q','-p','no:cacheprovider','--basetemp=/tmp/si-s01-eng-'+label,'--junitxml='+str(OWN/(label+'.xml')),*targets];at=time.monotonic();utc=datetime.now(timezone.utc).isoformat()
with (OWN/'receipts'/(label+'.stdout')).open('xb') as out,(OWN/'receipts'/(label+'.stderr')).open('xb') as err:result=subprocess.run(argv,cwd=REPO,env=env,stdout=out,stderr=err)
value={'argv':argv,'cwd':str(REPO),'started_utc':utc,'elapsed_seconds':time.monotonic()-at,'authentic_returncode':result.returncode,'source_head':sha,'pre_status':status,'post_status':subprocess.check_output(['git','status','--porcelain=v1'],cwd=REPO,text=True),'scope':'Only explicit synthetic raw model/CUDA/NVML/TextWorld boundaries. No actual Qwen/tokenizer/ALFWorld/CUDA/SSH/preflight/science. Dirty drafting tests are not final candidate acceptance.','environment':env}
for suffix in ('stdout','stderr'):
 p=OWN/'receipts'/(label+'.'+suffix);b=p.read_bytes();value[suffix]={'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
(OWN/'receipts'/(label+'.json')).write_text(json.dumps(value,indent=2)+'\n');print(json.dumps(value));print((OWN/'receipts'/(label+'.stdout')).read_text()[-16000:]);sys.exit(result.returncode)
