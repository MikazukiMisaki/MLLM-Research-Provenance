from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
OWN=Path(__file__).resolve().parent;RAW=Path('/tmp/si-s01-rt_focused');OUT=OWN/'evidence_rt'
selected={'unreaped_process_edge':('test_post_kill_wait_uses_remai0/run',['supervisor_exit.json','worker_start.json','launch_context.json'],'SIMULATED_PROCESS_EDGE_NOT_ACTUAL_KERNEL_HANG'),'atomic_marker_interleaving':('test_worker_marker_partial_wri0',['worker_start.json'],'CONTROLLED_REAL_FILESYSTEM_INTERLEAVING'),'atomic_marker_exclusive':('test_atomic_marker_publication0',['worker_start.json'],'REAL_FILESYSTEM_NO_OVERWRITE_FIXTURE'),'stage_cost_endpoint':('test_source_report_hours_are_e0/run',['source_report.json','SOURCE_REPORT.md'],'SYNTHETIC_SOURCE_ONLY_STAGE_COST')}
def bind(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
rows=[];local=[]
for label,(directory,names,kind) in selected.items():
 src=RAW/directory;assert src.is_dir(),str(src)
 dst=OUT/label;dst.mkdir(exist_ok=True)
 for name in names:
  path=src/name;copy=dst/name
  if copy.exists():assert copy.read_bytes()==path.read_bytes()
  else:
   with copy.open('xb') as f:f.write(path.read_bytes())
  rows.append({'case':label,'kind':kind,'source':bind(path),'copy':bind(copy),'byte_identical':True})
 for path in src.rglob('*'):
  if path.is_file() and not path.is_symlink():local.append({'case':label,**bind(path)})
value={'source_sha':'d7a82acb510157ab7ba5439d790816c5c948439f','evidence_class':'synthetic_software_fixture','real_kernel_unreap_or_GPU_reproduction':False,'copies':rows,'local_raw_files':local,'receipt':bind(OWN/'receipts/rt_focused.json')}
with (OWN/'RT_RELIABILITY_EVIDENCE_INDEX.json').open('x') as f:json.dump(value,f,indent=2);f.write('\n')
with (OWN/'CANDIDATE_STATUS_PENDING_FINAL_TESTS.json').open('x') as f:json.dump({'creation_time_utc':datetime.now(timezone.utc).isoformat(),'historical_snapshot_not_final_status':True,'candidate_sha':value['source_sha'],'branch':'codex/si-p3-source-only-v2','parent_sha':'9bc15b593ec6144915762a2fb1b172e063fe2c48','focused':{'passed':83,'authentic_returncode':0,'receipt':str(OWN/'receipts/rt_focused.json')},'full_regression':'IN_PROGRESS_USING_EXACT_INDEPENDENT_BASELINE_RUNNER','source_clean_and_frozen_during_tests':True,'independent_review_and_launch_authority':False,'actual_runtime':'BLOCKED_UNPROVEN_HOST_LOCAL_PID_MAPPING'},f,indent=2);f.write('\n')
print(json.dumps({'reliability_compact_files':len(rows),'source_sha':value['source_sha']}))
