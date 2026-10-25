"""Read immutable captured wire; run only pure/software production consumers, not CUDA."""
from pathlib import Path
from dataclasses import replace
from types import SimpleNamespace
import csv,hashlib,io,json,sys
root=Path(__file__).resolve().parent
repo=Path('/home/lizening/wt-si-e2-cuda-uuid-compat')
sys.path[:0]=[str(repo/'src'),str(repo/'tests')]
from si_e2_support import permit
from self_improvement.si_p3.contract import ContractError,digest
from self_improvement.si_p3.runtime_backend import cuda_uuid_matches,verify_cuda_uuid
from self_improvement.si_p3.runtime_ledger import EngineeringLedger,reconstruct
from self_improvement.si_p3 import runtime_gate
identity=Path('/home/lizening/research-notes/agent-logs/2026-10-25T141400Z__LUNA__si-e2-cuda-identity__dfc00e49_2e79/identity_run')
expected_hashes={'pre_allocation_identity.json':'41712d0516832fc48ddaadccee66a9e93ad48d4c0fa744ec5b5eb5c171824335','identity_observation.json':'b30bec7d674a273d08b55bf90da12d8be4ec6ddf493686cccb4322369778e982'}
rows={}
for name,expected_hash in expected_hashes.items():
 b=(identity/name).read_bytes()
 assert hashlib.sha256(b).hexdigest()==expected_hash
 rows[name]=json.loads(b)
pre=rows['pre_allocation_identity.json'];after=rows['identity_observation.json']
expected=pre['expected_uuid'];wire=pre['uuid']['str']
assert pre['uuid']['type_module']=='torch._C' and pre['uuid']['type_name']=='_CUuuid'
assert pre['uuid']==after['uuid'] and expected==after['expected_uuid']
assert wire!=expected and cuda_uuid_matches(wire,expected)
assert not cuda_uuid_matches(wire,'GPU-00000000-0000-0000-0000-000000000000')
fixture=root/'captured_wire_software_fixture';fixture.mkdir()
p=permit(fixture)
a=dict(p.authorization,gpu_uuid=expected)
p=replace(p,authorization=a,authorization_sha256=digest(a))
p.output.mkdir()
ledger=EngineeringLedger(p.output/'wire_events.jsonl',p,evidence_class='synthetic_software_fixture')
class _CUuuid:
 __module__='torch._C'
 def __str__(self):return wire
 def __repr__(self):return pre['uuid']['repr']
verify_cuda_uuid(SimpleNamespace(cuda=SimpleNamespace(get_device_properties=lambda ordinal:SimpleNamespace(uuid=_CUuuid()))),ledger,expected,point='captured_wire_software_fixture')
raw=ledger.events[-1]['payload']['observed']['uuid']
assert raw=={key:pre['uuid'][key] for key in ('present','type_module','type_name','str','repr')}
compute_raw=after['compute_after']['stdout']
compute_rows=list(csv.reader(io.StringIO(compute_raw),skipinitialspace=True))
assert after['pid']==837631 and int(compute_rows[0][1])==3082604
# Device name/UUID are recorded; memory columns below are explicit software fixture columns.
gpu_raw=expected+', NVIDIA A40, 46068, 14\n'
original_query=runtime_gate.subprocess.check_output
queries=[]
def fake_query(argv,**kwargs):
 queries.append(argv)
 if '--query-gpu=uuid,name,memory.total,memory.used' in argv:return gpu_raw
 assert '--query-compute-apps=gpu_uuid,pid,process_name,used_gpu_memory' in argv
 return compute_raw
runtime_gate.subprocess.check_output=fake_query
try:
 try:
  runtime_gate.inspect_gpu(expected,allowed_pids={after['pid']},require_owned_context=True)
 except ContractError as error:
  assert str(error)=='foreign GPU process'
  resource=error.resource_evidence
  assert resource['process_raw']==compute_raw
 else:raise AssertionError('captured unmapped host PID was incorrectly accepted')
finally:runtime_gate.subprocess.check_output=original_query
cost=ledger.snapshot();ledger.close()
assert 'torch' not in sys.modules
summary={'source_sha':'844cc4b78df1f83e29391ffd5ab861a2d0c0a3fd','fixture_kind':'SOFTWARE_CONSUMER_OF_FROZEN_RECORDED_WIRE_NOT_NEW_RUNTIME','input_sha256':expected_hashes,'observed_wire_type':pre['uuid']['type_module']+'.'+pre['uuid']['type_name'],'original_direct_comparison':wire==expected,'strict_full_uuid_match':True,'raw_value_type_repr_persisted':True,'captured_local_pid':after['pid'],'captured_nvml_pid':int(compute_rows[0][1]),'unmapped_pid_rejected':True,'error_resource_preserves_original_compute_raw':True,'memory_columns_are_software_fixture_not_contemporaneous_measurement':True,'mocked_query_count':len(queries),'torch_imported':False,'actual_cuda_nvml_model_env_calls':0,'science_calls':0,'journal_cost':cost,'runtime_readiness':'BLOCKED_OWNERSHIP_NOT_PROVEN'}
(root/'CAPTURED_WIRE_SOFTWARE_CHECK.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
