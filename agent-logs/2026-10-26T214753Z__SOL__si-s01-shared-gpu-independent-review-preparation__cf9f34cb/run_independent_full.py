from pathlib import Path
import json,subprocess,os,time,datetime,hashlib,sys
ctx=json.loads(Path('/tmp/si-s01-shared-root-review-preparation.json').read_text());d=Path(ctx['directory']);repo=Path(ctx['checkout']);external=Path(ctx['external']);out=d/'independent_full';out.mkdir(exist_ok=False)
env=dict(os.environ)
for k in ('PYTHONPATH','PYTHONHOME','VIRTUAL_ENV','PYTEST_ADDOPTS','PYTEST_PLUGINS'):env.pop(k,None)
env.update(CUDA_VISIBLE_DEVICES='',PYTHONDONTWRITEBYTECODE='1',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',TOKENIZERS_PARALLELISM='false')
for k,name in [('TMPDIR','tmp'),('XDG_CACHE_HOME','cache'),('HF_HOME','hf'),('TORCH_HOME','torch'),('PYTEST_DEBUG_TEMPROOT','pytest')]:
 p=external/name;p.mkdir(exist_ok=True);env[k]=str(p)
argv=['/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python','-I','-B',str(d/'independent_suite_runner.py'),str(repo),str(out),'full']
start=time.monotonic();at=datetime.datetime.now(datetime.timezone.utc).isoformat()
(out/'EXECUTION_PLAN.json').write_text(json.dumps({'source_sha':ctx['candidate_sha'],'argv':argv,'cwd':str(repo),'software_only':True,'gpu_visible':'','removed_keys':['PYTHONPATH','PYTHONHOME','VIRTUAL_ENV','PYTEST_ADDOPTS','PYTEST_PLUGINS'],'baseline':'exact e5 independent archived full.reports.json'},indent=2)+'\n')
with (out/'stdout.log').open('wb') as stdout,(out/'stderr.log').open('wb') as stderr:
 p=subprocess.Popen(argv,cwd=repo,env=env,stdout=stdout,stderr=stderr)
 try:rc=p.wait(timeout=1800);timed=False
 except subprocess.TimeoutExpired:p.kill();rc=p.wait();timed=True
receipt={'argv':argv,'cwd':str(repo),'source_sha':ctx['candidate_sha'],'authentic_returncode':rc,'timeout':timed,'started_utc':at,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-start,'stdout_sha256':hashlib.sha256((out/'stdout.log').read_bytes()).hexdigest(),'stderr_sha256':hashlib.sha256((out/'stderr.log').read_bytes()).hexdigest()}
(out/'AUTHENTIC_EXECUTION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt),flush=True)
