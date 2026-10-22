import datetime,json,os,subprocess,sys
from pathlib import Path
p=Path('/tmp/r19-2da-review-path.txt').read_text().strip();p=Path(p)
name=sys.argv[1];python='/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python';root='/tmp/r19-independent-review-2da980f'
commands={'focused':[python,'-m','pytest','-o','addopts=','-q','--basetemp',str(p/'local-focused-fixtures'),'tests/test_r19_entrypoint_repair.py','tests/test_r19_g3_authorization.py','tests/test_r19_recovery_duration.py','tests/test_r19_source_contract.py','tests/test_r19_source_pipeline.py'],'full':[python,'-m','pytest','-o','addopts=','-q','--tb=short','--basetemp',str(p/'local-full-fixtures'),'tests/']}
env=dict(os.environ);env['PYTHONPATH']='src'
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (p/'evidence'/f'{name}.log').open('w') as out:r=subprocess.run(commands[name],cwd=root,env=env,stdout=out,stderr=subprocess.STDOUT)
receipt={'argv':commands[name],'cwd':root,'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':r.returncode,'exit_source':'subprocess.returncode','classification':'software_tests_only','PYTHONPATH':'src'}
(p/'evidence'/f'{name}.receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
