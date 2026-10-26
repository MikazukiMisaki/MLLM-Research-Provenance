from pathlib import Path
import os,sys,json,subprocess,time,hashlib,shutil,datetime
OWN=Path(__file__).resolve().parent
B=json.loads((OWN/'BINDING.json').read_text());TREE=Path(B['checkout']);OUT=Path(B['external'])
CONTRACT=json.loads((OWN/'execution_environment.json').read_text())
ENV=dict(os.environ)
for k in CONTRACT['removed_keys']:ENV.pop(k,None)
ENV.update(CONTRACT['set_values'])
CACHE=OUT/'cache';CACHE.mkdir(exist_ok=True)
ENV.update({'TMPDIR':str(OUT),'PYTHONPYCACHEPREFIX':str(CACHE/'pycache'),'XDG_CACHE_HOME':str(CACHE/'xdg'),'HF_HOME':str(CACHE/'hf'),'TORCH_HOME':str(CACHE/'torch'),'PYTEST_DEBUG_TEMPROOT':str(OUT/'pytest-temproot')})
(OUT/'pytest-temproot').mkdir(exist_ok=True)
(OWN/'execution_controls.json').write_text(json.dumps({'additional_interpreter_flags':['-B'],'reason':'disable main-process bytecode writes while preserving runner exact bytes; project tests may use explicit isolated subprocess flags','cache_redirects':{k:ENV[k] for k in ['TMPDIR','PYTHONPYCACHEPREFIX','XDG_CACHE_HOME','HF_HOME','TORCH_HOME','PYTEST_DEBUG_TEMPROOT']},'contract_key_presence':{k:k in ENV for k in CONTRACT['removed_keys']},'contract_overrides':{k:ENV[k] for k in CONTRACT['set_values']},'run_each_mode_once':['collect','full']},indent=2)+'\n')
receipts=[]
for MODE in ('collect','full'):
    args=[CONTRACT['pinned_interpreter'],'-I','-B',str(OWN/'baseline_runner.py'),str(TREE),str(OUT),MODE]
    before=datetime.datetime.now(datetime.timezone.utc).isoformat();start=time.monotonic();timed=False
    with (OWN/(MODE+'.stdout')).open('wb') as stdout,(OWN/(MODE+'.stderr')).open('wb') as stderr:
        p=subprocess.Popen(args,cwd=TREE,env=ENV,stdout=stdout,stderr=stderr)
        try:rc=p.wait(timeout=1800)
        except subprocess.TimeoutExpired:p.kill();rc=p.wait();timed=True
    receipt={'argv':args,'cwd':str(TREE),'authentic_returncode':rc,'timeout':timed,'start_utc':before,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-start,'stdout_bytes':(OWN/(MODE+'.stdout')).stat().st_size,'stderr_bytes':(OWN/(MODE+'.stderr')).stat().st_size,'stdout_sha256':hashlib.sha256((OWN/(MODE+'.stdout')).read_bytes()).hexdigest(),'stderr_sha256':hashlib.sha256((OWN/(MODE+'.stderr')).read_bytes()).hexdigest()}
    (OWN/(MODE+'.receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n');receipts.append(receipt)
    for p in OUT.glob(MODE+'.*.json'):shutil.copyfile(p,OWN/p.name)
    if MODE=='full' and (OUT/'baseline.junit.xml').exists():shutil.copyfile(OUT/'baseline.junit.xml',OWN/'baseline.junit.xml')
    print(json.dumps({'mode':MODE,'returncode':rc,'elapsed_seconds':receipt['elapsed_seconds'],'timed_out':timed}),flush=True)
    if timed:break
(OWN/'SUITE_SUBPROCESS_RECEIPTS.json').write_text(json.dumps(receipts,indent=2)+'\n')
