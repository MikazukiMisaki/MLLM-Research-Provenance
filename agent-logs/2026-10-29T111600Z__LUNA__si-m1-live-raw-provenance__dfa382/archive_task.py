"""Copy and hash exact run bytes; no runner/model/environment invocation."""
import hashlib,json,os,re,shutil,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
O=Path(__file__).resolve().parent
base=Path('/tmp/si_m1_uid-2000_run-394f9f90869dd8505844caa7ea1a7e9f_35jwli1v');root=Path('/home/lizening/wt-si-five-case-probe');readiness=Path('/home/lizening/research-notes/agent-logs/2026-10-29T110600Z__LUNA__si-m1-resume-readiness__dfa382')
clearance=Path('/home/lizening/research-notes/agent-logs/2026-10-29T110346Z__ASTRA__si-m1-independent-exact-review__5e2283b0/ONE_LIVE_CLEARANCE_394f9f90869dd8505844caa7ea1a7e9f.json')
auth=Path('/home/lizening/wt-si-five-case-probe/configs/local/si_m1_authorization_e37046d42289de2898d82bddd04b5f14.json');a=json.loads(auth.read_bytes())
source_list=[]
for directory in ('output','control'):
 for path in sorted((base/directory).iterdir()):
  if not path.is_file() or path.is_symlink():raise ValueError('nonregular input '+str(path))
  source_list.append((path,Path('raw')/directory/path.name))
fixed=[(auth,'bindings/authorization.json'),(clearance,'bindings/clearance.json'),(Path(a['review']['path']),'bindings/independent_review.json'),(root/'configs/local/si_m1_single_step_proposal_draft.json','bindings/proposal.json'),(root/'configs/local/si_m1_environment_draft.json','bindings/environment_draft.json'),(root/'configs/experiments/si_m1_single_step_v1.json','bindings/scientific_contract.json'),(root/'configs/experiments/si_s01_shared_resource_v1.json','bindings/shared_resource_contract.json'),(Path('/home/lizening/research-notes/agent-logs/2026-10-27T024153Z__ASTRA__minimal-recoverability-design-review__e6fb570f/MINIMAL_RECOVERABILITY_DESIGN.md'),'bindings/frozen_design.md'),(root/'scripts/run_si_m1_probe.py','scripts/production_entry.py'),(readiness/'run_once.py','scripts/run_once.py'),(readiness/'prepare_once_v2.py','scripts/prepare_once_v2.py'),(readiness/'FINAL_LIVE_DRIFT_CHECK.json','bindings/final_drift_check.json')]
source_list.extend((p,Path(x)) for p,x in fixed)
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(2**20),b''):h.update(b)
 return h.hexdigest()
patterns=[re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----'),re.compile(rb'gh[pousr]_[A-Za-z0-9]{30,}'),re.compile(rb'sk-[A-Za-z0-9]{30,}')]
rows=[];matches=[]
for src,rel in source_list:
 if src.is_symlink() or not src.is_file():raise ValueError('source not regular '+str(src))
 before=sha(src);size=src.stat().st_size;dest=O/rel;dest.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
 with src.open('rb') as i,dest.open('xb') as o:
  shutil.copyfileobj(i,o,2**20);o.flush();os.fsync(o.fileno())
 copied=sha(dest);after=sha(src);data=dest.read_bytes()
 if not(before==after==copied) or size!=len(data):raise ValueError('source/copy mismatch '+str(src))
 for n,regex in enumerate(patterns):
  if regex.search(data):matches.append({'path':str(rel),'pattern_index':n})
 rows.append({'path':str(rel),'source_path':str(src),'bytes':size,'sha256':before,'source_after_sha256':after,'copy_sha256':copied})
report=json.loads((base/'output/probe_report.json').read_bytes());sup=json.loads((base/'output/supervisor_exit.json').read_bytes());wrap=json.loads((base/'control/live_invocation_exit.json').read_bytes())
inv={'schema':'SI_M1_RAW_PROVENANCE_COPY_V1','recorded_utc':datetime.now(timezone.utc).isoformat(),'status':'LOCAL_ONLY_PENDING_COORDINATOR_PUBLICATION','run_id':a['run_id'],'source_sha':a['source_sha'],'files':rows,'file_count':len(rows),'total_bytes':sum(r['bytes'] for r in rows),'all_original_before_after_copy_match':True,'targeted_credential_patterns_matches':matches,'excluded':'Model weights, adapters, cache, input dataset files, and unrelated work. Raw output ledger is intentionally included.','run_observations':{'outer_rc':wrap['returncode'],'supervisor_rc':sup['authentic_returncode'],'supervisor_execution_status':sup['execution_status'],'allocated_device_hours':sup['allocated_device_hours'],'physical':report['physical'],'case_outcomes':[{'case_id':r['case_id'],'Z_immediate':r['Z_immediate'],'disposition':r['disposition']} for r in report['rows']],'cumulative_prior':{'generations':7101,'environment_operations':10004},'cumulative_after':{'generations':7101+report['physical']['completed']['generations'],'environment_operations':10004+report['physical']['completed']['environment_operations']}}}
with (O/'COPY_MANIFEST.json').open('x') as f:json.dump(inv,f,indent=2);f.write('\n')
print(json.dumps({'file_count':len(rows),'total_bytes':inv['total_bytes'],'all_original_before_after_copy_match':True,'targeted_credential_pattern_matches':len(matches),'manifest_sha256':sha(O/'COPY_MANIFEST.json'),'run_observations':inv['run_observations']},sort_keys=True))
if matches:sys.exit(2)
