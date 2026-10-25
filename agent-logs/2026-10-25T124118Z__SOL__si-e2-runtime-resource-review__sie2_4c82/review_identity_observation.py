"""Read-only root review of captured identity results; standard library only."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,uuid
r=Path(__file__).resolve().parent
own=Path('/home/lizening/research-notes/agent-logs/2026-10-25T141400Z__LUNA__si-e2-cuda-identity__dfc00e49_2e79')
load=lambda p:json.loads(p.read_bytes())
x=load(own/'identity_run/identity_observation.json');pre=load(own/'identity_run/pre_allocation_identity.json');exit=load(own/'identity_run/launcher_receipt.json');prior=load(r/'independent_runtime_recount.json')
assert exit['authentic_returncode']==1 and exit['within_seconds_cap'] and exit['remaining'] is None
assert x['model_loads']==x['generations']==x['environment_calls']==0
assert pre['uuid']==x['uuid'] and pre['one_byte_allocation_completed'] is False and x['one_byte_allocation_completed'] is True
expected=x['expected_uuid'];actual=x['uuid']['str']
assert expected.startswith('GPU-') and len(actual)==36
assert uuid.UUID(expected[4:])==uuid.UUID(actual)
rows=[[s.strip() for s in line.split(',')] for line in x['compute_after']['stdout'].splitlines() if line.strip()]
assert len(rows)==1 and rows[0][0]==expected and int(rows[0][1])!=x['pid']
assert x['status']=='IDENTITY_RAW_OBSERVED_OWNERSHIP_UNPROVEN' and not x['own_compute_row_observed']
review={'schema':'SI_E2_ROOT_INDEPENDENT_CUDA_IDENTITY_REVIEW_V1','UTC':datetime.now(timezone.utc).isoformat(),'raw_UUID_identity':'PASS_SAME_COMPLETE_UUID_BYTES_DIFFERENT_WIRE_PREFIX','torch_UUID_type':x['uuid']['type_module']+'.'+x['uuid']['type_name'],'torch_UUID_value':actual,'NVML_UUID_value':expected,'source_compatibility_finding':'runtime_backend.py115/137 directly compares str(_CUuuid) without GPU- to NVML GPU-prefixed UUID. Observed installed wire deterministically rejected before weights.','local_pid':x['pid'],'NVML_compute_pid':int(rows[0][1]),'GPU_PROCESS_OWNERSHIP':'UNPROVEN','unknown_compute_PID_must_not_be_whitelisted':True,'namespace_evidence':'/proc/self/status lists NSpid837631 only; docker cgroup/pid namespace link preserved. No trusted host/local PID mapping saved.','root_cause_scope':['Confirmed UUID representation mismatch','Independent unresolved host/local process identity binding'],'diagnostic_returncode':1,'diagnostic_elapsed_seconds':exit['elapsed_seconds'],'diagnostic_within60seconds':True,'diagnostic_explicit_tensor_bytes':1,'actual_cuda_allocator_bytes':x['cuda_memory'],'model_weights_loaded':0,'generations':0,'environment_calls':0,'remaining_process':None,'science_cumulative_unchanged':{'generations':5142,'reset_inclusive_operations':7949},'conservative_diagnostic_interval_device_hours':exit['elapsed_seconds']/3600,'original_probe_plus_diagnostic_allocated_interval_upper_bound_device_hours':prior['allocated_device_hours']+exit['elapsed_seconds']/3600,'runtime_or_science_ready':False,'new_probe_authorization':'NOT_GRANTED','minimal_followup':'Strict UUID wire compatibility and preassertion raw evidence persistence, no PID guard weakening. Trusted execution-context mapping must be independently proven before8B.','evidence':{str(p.relative_to(own)):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted((own/'identity_run').iterdir()) if p.is_file()}}
with (r/'independent_cuda_identity_review.json').open('x') as f:json.dump(review,f,indent=2);f.write('\n')
print(json.dumps({k:review[k] for k in ('raw_UUID_identity','GPU_PROCESS_OWNERSHIP','diagnostic_returncode','diagnostic_elapsed_seconds','runtime_or_science_ready')}))
