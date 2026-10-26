from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys,time
OWN=Path(__file__).resolve().parent;REPO=Path('/home/lizening/wt-si-p3-source-only-v2');BASE=Path('/home/lizening/research-notes/agent-logs/2026-10-26T111621Z__SOL__si-s01-independent-base844-suite__critic_1f34d86d')
OUT=OWN/'comparable';OUT.mkdir(exist_ok=False)
python='/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python'
contract=json.loads((BASE/'execution_environment.json').read_text());assert hashlib.sha256(Path(python).read_bytes()).hexdigest()==contract['pinned_interpreter_sha256']
assert hashlib.sha256((OWN/'baseline_runner.py').read_bytes()).hexdigest()==contract['runner_sha256']
env=dict(os.environ)
for key in contract['removed_keys']:env.pop(key,None)
env.update(contract['set_values'])
(OUT/'environment_contract.json').write_text(json.dumps(contract,indent=2)+'\n')
for mode in ('collect','full'):
 status=subprocess.check_output(['git','status','--porcelain=v1'],cwd=REPO,text=True);assert not status,status
 sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip();argv=[python,'-I',str(OWN/'baseline_runner.py'),str(REPO),str(OUT),mode]
 at=time.monotonic();utc=datetime.now(timezone.utc).isoformat()
 with (OUT/(mode+'.stdout')).open('xb') as out,(OUT/(mode+'.stderr')).open('xb') as err:result=subprocess.run(argv,cwd=REPO,env=env,stdout=out,stderr=err)
 post=subprocess.check_output(['git','status','--porcelain=v1'],cwd=REPO,text=True)
 receipt={'argv':argv,'cwd':str(REPO),'source_sha':sha,'started_utc':utc,'authentic_returncode':result.returncode,'elapsed_seconds':time.monotonic()-at,'pre_status':status,'post_status':post,'same_runner_sha256':contract['runner_sha256'],'same_explicit_environment_contract':contract,'scope':'CPU software tests. Existing tiny CPU PEFT/tokenizer fixtures permitted; no real Qwen tokenizer, Qwen weights, CUDA initialization, ALFWorld, SSH or production preflight/live invocation.'}
 for suffix in ('stdout','stderr'):
  p=OUT/(mode+'.'+suffix);receipt[suffix]={'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 (OUT/(mode+'.receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'mode':mode,'returncode':result.returncode,'elapsed_seconds':receipt['elapsed_seconds']}),flush=True)
 assert not post,post
 if mode=='collect' and result.returncode:raise SystemExit(result.returncode)
raise SystemExit(result.returncode)
