"""Read-only operational gate; never imports scientific modules."""
import os,sys,json,hashlib,subprocess,fcntl
from pathlib import Path
repo=Path('/home/lizening/Alfworld-Self-Improvement-Project')
runtime=repo/'artifacts/runtime/validation/progress-aware-r18-c2-formal-aa9fa3c34520941e'
sha='aa9fa3c34520941e7e3be00294b111e8254fd65b'
audit=Path(__file__).resolve().parent
baseline=json.loads((audit/'runtime-state.json').read_text())
def require(condition,message):
 if not condition:raise SystemExit('STOP: '+message)
def git(*args):return subprocess.check_output(['git',*args],cwd=repo,text=True).strip()
require(git('branch','--show-current')=='codex/progress-aware-recovery','branch differs')
require(git('rev-parse','HEAD')==sha,'HEAD differs')
require(git('rev-parse','origin/codex/progress-aware-recovery')==sha,'remote differs; fetch before this check')
require(not git('status','--porcelain=v1'),'worktree dirty')
require(Path(sys.executable).resolve()==Path('/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python').resolve(),'wrong Python environment')
expected={'ALFWORLD_DATA':'/home/lizening/alfworld_data','ALFWORLD_CONFIG_PATH':str(repo/'configs/local/alfworld_base_university.yaml'),'TOKENIZERS_PARALLELISM':'false','PYTHONPATH':'.'}
for k,v in expected.items():require(os.environ.get(k)==v,'environment mismatch '+k)
require(Path(expected['ALFWORLD_DATA']).is_dir(),'data directory missing')
require(Path(expected['ALFWORLD_CONFIG_PATH']).is_file(),'local config missing')
require((repo/'artifacts/runtime/model-artifacts/sft-policy-bootstrap/full/final_adapter').is_dir(),'adapter missing')
files={str(f.relative_to(runtime)):hashlib.sha256(f.read_bytes()).hexdigest() for f in runtime.rglob('*') if f.is_file()}
require(files=={k:v['sha256'] for k,v in baseline['files'].items()},'runtime changed since audit; requires a new read-only review')
m=json.loads((runtime/'run_manifest.json').read_text())
require(m['status']=='initialized' and m['provenance']['implementation_commit']==sha,'manifest state/provenance differs')
for k in ['accepted_branches','completed_branch_reruns','incomplete_branch_retries','operational_interruptions']:require(m[k]==0,'manifest counter changed: '+k)
for name in baseline['formal_reports']:require(not (repo/'reports'/name).exists(),'formal report exists')
control=repo/'artifacts/runtime/progress-aware-r18-c2-control'
for name,e in baseline['control'].items():
 if not isinstance(e,dict):continue
 f=control/name
 require(f.is_file() and hashlib.sha256(f.read_bytes()).hexdigest()==e['sha256'],'control state changed '+name)
owner=json.loads((control/'experiment.json').read_text())
require(owner=={'project_root':str(repo),'runtime':str(runtime)},'runtime owner changed')
active=[]
for f in Path('/proc').glob('[0-9]*/cmdline'):
 try:argv=f.read_bytes().decode(errors='replace').split('\0')
 except (FileNotFoundError,PermissionError,ProcessLookupError):continue
 if any(Path(a).name in ['run_progress_aware_card_v2_r18_c2.py','durable-wrapper.sh'] for a in argv if a):active.append(f.parent.name)
require(not active,'existing runner/wrapper processes '+str(active))
# PID files are evidence, not authority: check PID plus start ticks and current boot.
for f in Path('/home/lizening/research-notes/agent-logs').glob('*/runner.pid'):
 for name in ['launcher','runner']:
  ident=f.parent/(name+'.identity')
  if not ident.exists():continue
  pid,ticks=ident.read_text().split()
  stat=Path('/proc')/pid/'stat'
  if stat.exists():
   raw=stat.read_text().rsplit(') ',1)[1].split()
   require(raw[19]!=ticks,'recorded '+name+' identity still exists: '+str(ident))
fd=os.open(control/'writer.lock',os.O_RDONLY)
try:
 try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
 except BlockingIOError:raise SystemExit('STOP: formal runner flock is held')
 fcntl.flock(fd,fcntl.LOCK_UN)
finally:os.close(fd)
print(json.dumps({'preflight':'PASS','sha':sha,'manifest_status':m['status'],'accepted_branches':0,'ledger_rows':0,'formal_lock':'available at probe time','environment':expected},indent=2))
