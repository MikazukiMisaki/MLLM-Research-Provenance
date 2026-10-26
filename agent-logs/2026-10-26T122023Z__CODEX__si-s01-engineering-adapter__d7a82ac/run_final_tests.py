from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,time,sys
OWN=Path(__file__).resolve().parent;REPO=Path('/home/lizening/wt-si-s01-engineering-adapter');BASE=Path('/home/lizening/research-notes/agent-logs/2026-10-26T111621Z__SOL__si-s01-independent-base844-suite__critic_1f34d86d');PY='/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python'
OUT=OWN/'final_tests';OUT.mkdir(exist_ok=False);contract=json.loads((BASE/'execution_environment.json').read_bytes())
assert hashlib.sha256((OWN/'baseline_runner.py').read_bytes()).hexdigest()==contract['runner_sha256']
assert hashlib.sha256(Path(PY).read_bytes()).hexdigest()==contract['pinned_interpreter_sha256']
env=dict(os.environ)
for key in contract['removed_keys']:env.pop(key,None)
env.update(contract['set_values']);(OUT/'environment_contract.json').write_text(json.dumps(contract,indent=2)+'\n')
for mode in ('focused','collect','full'):
 before=subprocess.check_output(['git','status','--porcelain=v1'],cwd=REPO,text=True);assert not before,before
 sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
 argv=[PY,'-I',str(OWN/('focused_runner.py' if mode=='focused' else 'baseline_runner.py')),str(REPO),str(OUT)]
 if mode!='focused':argv.append(mode)
 at=time.monotonic();utc=datetime.now(timezone.utc).isoformat()
 with (OUT/(mode+'.stdout')).open('xb') as out,(OUT/(mode+'.stderr')).open('xb') as err:r=subprocess.run(argv,cwd=REPO,env=env,stdout=out,stderr=err)
 after=subprocess.check_output(['git','status','--porcelain=v1'],cwd=REPO,text=True)
 receipt={'argv':argv,'cwd':str(REPO),'source_sha':sha,'started_utc':utc,'elapsed_seconds':time.monotonic()-at,'authentic_returncode':r.returncode,'pre_status':before,'post_status':after,'same_explicit_environment_contract':contract,'baseline_runner_sha256':contract['runner_sha256'],'scope':'Only software fixtures, including predeclared tiny CPU models/tokenizers and fake raw model/CUDA/NVML/TextWorld. No actual Qwen/tokenizer/CUDA/world/hostSSH/preflight/science.'}
 for suffix in ('stdout','stderr'):
  p=OUT/(mode+'.'+suffix);b=p.read_bytes();receipt[suffix]={'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 (OUT/(mode+'.receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'mode':mode,'source_sha':sha,'returncode':r.returncode,'elapsed_seconds':receipt['elapsed_seconds']}),flush=True)
 assert not after,after
 if mode in ('focused','collect') and r.returncode:raise SystemExit(r.returncode)
raise SystemExit(r.returncode)
