"""Read-only independent streaming rehash after terminated engineering attempt."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,time
r=Path(__file__).resolve().parent
before=json.loads((r/'independent_frozen_input_bytes.json').read_bytes())
start=time.monotonic();rows=[]
for kind in ('frozen_model_files','P0_files','historical_critical_inputs'):
 for row in before[kind]:
  p=Path(row['path']);h=hashlib.sha256()
  with p.open('rb') as f:
   for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
  rows.append({'category':kind,'path':str(p),'bytes':p.stat().st_size,'sha256':h.hexdigest(),'expected_sha256':row['sha256'],'matches':h.hexdigest()==row['sha256'] and p.stat().st_size==row['bytes']})
source=Path('/home/lizening/wt-si-p3-runtime-adaptation')
def git(*args):return subprocess.check_output(['git',*args],cwd=source,text=True).strip()
remote=subprocess.run(['git','ls-remote','origin','refs/heads/codex/si-p3-runtime-adaptation'],cwd=source,capture_output=True,text=True)
assert remote.returncode==0
result={'UTC':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-start,'observed_files':rows,'all_28_original_model_adapter_and_G3_hashes_match':all(x['matches'] for x in rows),'source_SHA':git('rev-parse','HEAD'),'source_branch':git('branch','--show-current'),'source_status':git('status','--porcelain','--untracked-files=all'),'live_remote_returncode':remote.returncode,'live_remote_stdout':remote.stdout,'live_remote_stderr':remote.stderr,'no_model_or_environment_API_calls':True}
with (r/'independent_inputs_after_engineering.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
assert result['all_28_original_model_adapter_and_G3_hashes_match'] and result['source_SHA']=='dfc00e49d1ef4d48453d2331507429f8a0c7bbc5' and not result['source_status']
print(json.dumps({'files':len(rows),'all_match':True,'source_SHA':result['source_SHA'],'clean':True,'remote':remote.stdout.strip(),'elapsed_seconds':result['elapsed_seconds']}))
