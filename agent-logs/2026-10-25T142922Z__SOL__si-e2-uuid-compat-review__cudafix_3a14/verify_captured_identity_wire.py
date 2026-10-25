"""Independent production-helper check against already captured real UUID text; no CUDA import."""
from pathlib import Path
from datetime import datetime,timezone
from types import SimpleNamespace
import hashlib,json,sys,uuid
ROOT=Path(__file__).resolve().parent
checkout=Path(sys.argv[1]).resolve();sys.path.insert(0,str(checkout/'src'))
from self_improvement.si_p3 import runtime_backend as b
from self_improvement.si_p3.runtime_ledger import EngineeringLedger,reconstruct
from self_improvement.si_p3.contract import ContractError
assert Path(b.__file__).resolve()==checkout/'src/self_improvement/si_p3/runtime_backend.py'
actual_path=Path('/home/lizening/research-notes/agent-logs/2026-10-25T141400Z__LUNA__si-e2-cuda-identity__dfc00e49_2e79/identity_run/pre_allocation_identity.json')
actual=json.loads(actual_path.read_bytes());bare=actual['uuid']['str'];expected=actual['expected_uuid']
assert uuid.UUID(bare)==uuid.UUID(expected[4:])
checks=[]
for label,value,expect in [('real_saved_wire',bare,True),('NVML_wire',expected,True),('uppercase_complete_uuid',bare.upper(),True),('other_uuid',bare[:-1]+('0' if bare[-1]!='0' else '1'),False),('prefix_partial',bare[:8],False),('leading_space',' '+bare,False),('newline',bare+'\n',False),('MIG','MIG-'+expected+'/1/0',False),('missing',None,False)]:
 result=b.cuda_uuid_matches(value,expected);assert result is expect;checks.append({'label':label,'expected':expect,'observed':result})
permit=SimpleNamespace(authorization_sha256='software-only',proposal_sha256='software-only')
ledger_path=ROOT/'captured_wire_software_events.jsonl';ledger=EngineeringLedger(ledger_path,permit,evidence_class='synthetic_software_fixture')
b.verify_cuda_uuid(SimpleNamespace(cuda=SimpleNamespace(get_device_properties=lambda i:SimpleNamespace(uuid=bare))),ledger,expected,point='independent_saved_wire_positive')
try:b.verify_cuda_uuid(SimpleNamespace(cuda=SimpleNamespace(get_device_properties=lambda i:SimpleNamespace(uuid=bare+'\n'))),ledger,expected,point='independent_malformed_before_error')
except ContractError:pass
else:raise AssertionError('malformed identity was accepted')
rows=[json.loads(l) for l in ledger_path.read_text().splitlines()]
assert rows[-1]['payload']['observed']['uuid']['str']==bare+'\n'
assert reconstruct(rows)['external_started']==0
ledger.close()
result={'UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS_SOFTWARE_WITH_CAPTURED_REAL_WIRE_TEXT','source_module':str(b.__file__),'source_module_sha256':hashlib.sha256(Path(b.__file__).read_bytes()).hexdigest(),'real_observation_path':str(actual_path),'real_observation_sha256':hashlib.sha256(actual_path.read_bytes()).hexdigest(),'checks':checks,'actual_ledger_hashchain_and_reconstruct':'PASS','negative_raw_value_persisted_before_error':True,'new_CUDA_or_model_or_environment_calls':0,'GPU_process_ownership':'STILL_UNPROVEN_NOT_TESTED_BY_THIS_SCRIPT'}
with (ROOT/'captured_wire_independent_check.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'status':result['status'],'cases':len(checks),'actualCUDA_model_envcalls':0}))
