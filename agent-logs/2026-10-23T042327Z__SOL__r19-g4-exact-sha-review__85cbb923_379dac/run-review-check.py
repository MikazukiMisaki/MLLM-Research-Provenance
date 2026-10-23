from pathlib import Path
import subprocess,os,sys,json,datetime
p=Path(Path('/tmp/r19-g4-independent-review-path.txt').read_text().strip());name=sys.argv[1];root=Path(sys.argv[2]);args=[]
for value in sys.argv[3:]:
 if '*' in value:
  expanded=sorted(str(x.relative_to(root)) for x in root.glob(value));assert expanded,value;args.extend(expanded)
 else:args.append(value)
env=dict(os.environ)
for key in ('PYTHONPATH','PYTHONHOME','VIRTUAL_ENV'):env.pop(key,None)
env.update({'HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1'})
argv=['/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python',*args]
def git(*a):return subprocess.check_output(['git','-C',str(root),*a],text=True).strip()
start=datetime.datetime.now(datetime.timezone.utc).isoformat();head=git('rev-parse','HEAD');before=git('status','--porcelain');assert not before,before
with (p/'evidence'/f'{name}.log').open('wb') as log:r=subprocess.run(argv,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
d={'argv':argv,'cwd':str(root),'started_at_utc':start,'finished_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_subprocess_returncode':r.returncode,'head_before':head,'head_after':git('rev-parse','HEAD'),'git_status_before':before,'git_status_after':git('status','--porcelain'),'python_override_presence':{k:k in env for k in ('PYTHONPATH','PYTHONHOME','VIRTUAL_ENV')},'pinned_python':argv[0],'scope':'ENGINEERING_TESTS_ONLY_NO_OFFICIAL_PREFLIGHT_OR_SCIENCE'}
(p/'evidence'/f'{name}.receipt.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2));print((p/'evidence'/f'{name}.log').read_text()[-1600:])
