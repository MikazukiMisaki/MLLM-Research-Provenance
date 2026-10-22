"""Capture an authentic software-check process, its exit status, and raw output."""
import json,os,subprocess,sys,time
from pathlib import Path
label=sys.argv[1]
command=sys.argv[2:]
base=Path(__file__).resolve().parent
started=time.time()
env=dict(os.environ)
env['PYTHONPATH']='src'
log=base/(label+'.log')
if log.exists():raise FileExistsError(log)
with log.open('wb') as stream:
 result=subprocess.run(command,cwd='/home/lizening/wt-r19-source-contract-review-fixes',env=env,stdout=stream,stderr=subprocess.STDOUT)
receipt={'label':label,'argv':command,'cwd':'/home/lizening/wt-r19-source-contract-review-fixes','environment_overrides':{'PYTHONPATH':'src'},'exit_code':result.returncode,'exit_code_source':'subprocess.returncode','started_unix':started,'completed_unix':time.time(),'class':'software_checks_only_no_scientific_execution'}
(base/(label+'.receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
sys.exit(result.returncode)
