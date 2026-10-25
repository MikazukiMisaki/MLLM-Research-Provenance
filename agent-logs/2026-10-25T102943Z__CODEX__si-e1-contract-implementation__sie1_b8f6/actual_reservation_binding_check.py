from pathlib import Path
import hashlib,json,sys
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
from self_improvement.si_p3.reservations import bind_reservations,RESERVATIONS_SHA256
from self_improvement.si_p3.contract import ContractError,digest
path=Path(sys.argv[1]);raw=path.read_bytes();before=hashlib.sha256(raw).hexdigest();assert before==RESERVATIONS_SHA256
value=json.loads(raw)
a=[x for x in value['rows'] if x['partition']=='acquisition_feasibility_96']
metadata=[{'task_id':x['identity'],'family':x['family'],'seed':42} for x in a]
plan=bind_reservations(raw,metadata)
assert len(plan)==96 and {(s.task_id,s.family) for s in plan}=={(x['identity'],x['family']) for x in a}
results={'actual_metadata_positive_bound_count':len(plan)}
dev=next(x for x in value['rows'] if x['partition']=='engineering_development_train' and x['family']==a[0]['family'])
mutated=[dict(x) for x in metadata];mutated[0]['task_id']=dev['identity']
try:bind_reservations(raw,mutated)
except ContractError as e:results['same_family_A96_to_D48_rejected']=str(e)
else:raise AssertionError('quota-preserving D48 substitution accepted')
changed=json.loads(raw)
source_index=next(i for i,x in enumerate(changed['rows']) if x['identity']==a[0]['identity'])
dev_index=next(i for i,x in enumerate(changed['rows']) if x['identity']==dev['identity'])
changed['rows'][source_index]['partition'],changed['rows'][dev_index]['partition']=changed['rows'][dev_index]['partition'],changed['rows'][source_index]['partition']
changed['self_reported_sha256']=hashlib.sha256(json.dumps(changed).encode()).hexdigest()
payload=json.dumps(changed).encode()
try:bind_reservations(payload,mutated)
except ContractError as e:results['modified_bytes_and_rehashed_header_rejected']=str(e)
else:raise AssertionError('self-reported hash bypassed frozen digest')
try:bind_reservations(raw,metadata,synthetic_expected_sha256=before)
except ContractError as e:results['historical_digest_override_rejected']=str(e)
else:raise AssertionError('historical digest override accepted')
assert hashlib.sha256(path.read_bytes()).hexdigest()==before
result={'scope':'PURE_OFFLINE_REAL_RESERVATION_METADATA_ONLY','input':{'path':str(path),'sha256_before':before,'sha256_after':before},'caller_seed':42,'seed_status':'explicit software example only; no seed release or executable schedule written','bound_identity_set_sha256':digest(sorted((s.task_id,s.family) for s in plan)),'results':results,'new_task_bodies_read':0,'model_or_environment_or_tokenizer_or_training_calls':0,'execution_authorized':False}
(OWN/'actual_reservation_binding_check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
