from pathlib import Path
from decimal import Decimal
import copy,hashlib,json,tarfile
O=Path(__file__).parent
OLD=Path('/home/lizening/research-notes/agent-logs/2026-10-30T004400Z__CODEX__si-project-resource-ledger-static/PARTIAL_ACTUAL_LEDGER.json')
ARCHIVE=Path('/home/lizening/research-notes/agent-logs/2026-10-29T131100Z__LUNA__si-u1-eval-engineering__f2e4895/RAW_EVIDENCE_PRIVATE.tar.gz')
def sha(data):return hashlib.sha256(data).hexdigest()
def fsha(path):
 with path.open('rb') as f:
  h=hashlib.sha256()
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
  return h.hexdigest()
def read(k):return json.loads(Path(old['input_sources'][k]['path']).read_text())
assert fsha(OLD)=='1f55ee5cc4404e3566e53d8897620c1f0bf50f5764bf2e14d2f5bba712f9ab59'
assert fsha(ARCHIVE)=='f17526737a8c050a9cfc7f6b4373a626ea99b9fbfd08dd323c2565a2460e3cdf'
old=json.loads(OLD.read_text());bindings={}
for k,v in old['input_sources'].items():
 actual=fsha(Path(v['path']));bindings[k]={'expected':v['sha256'],'actual':actual,'matches':actual==v['sha256']}
assert len(bindings)==16 and all(v['matches'] for v in bindings.values())
with tarfile.open(ARCHIVE,'r:gz') as tar:
 f=tar.extractfile('run/engineering/engineering_events.jsonl');raw=f.read()
assert sha(raw)=='3e3289ef0ed7b1e1edd0d2f4f7647d6c6941005e1367e586d08d519deb5b4f5b'
ev=[json.loads(line) for line in raw.splitlines()];reset=[v for v in ev if v['payload'].get('op')=='reset'];start=[v for v in reset if v['kind']=='unit_started'];ret=[v for v in reset if v['kind']=='external_returned'];fail=[v for v in reset if v['kind']=='unit_failed'];done=[v for v in reset if v['kind']=='unit_completed']
assert len(start)==1 and len(ret)==2 and len(fail)==1 and not done
call=[v for v in ret if v['payload'].get('boundary')=='raw_reset_call_returned'];snap=[v for v in ret if v['payload'].get('boundary')=='raw_reset_returned'];assert len(call)==len(snap)==1
assert call[0]['payload']['data']['returned'] is True and snap[0]['payload']['data']['lossless'] is False
assert fail[0]['payload']['started_event']==start[0]['event_id'] and fail[0]['payload']['return_events']==[call[0]['event_id'],snap[0]['event_id']]
rows=copy.deepcopy(old['rows']);ids={r['ledger_id']:r for r in rows};assert len(ids)==len(rows)
for row in rows:
 p=row['physical_known'];row['is_additive']=row['ledger_id']!='si.pre-s01.unnamed-engineering';row['attribution_pending']=not row['is_additive'];row['verification_level']='manual_source_summary_not_full_independent_raw_recount'
 if 'env_reset_completed' in p:p['env_reset_physical_completed']=p['env_reset_completed']
 if 'env_operations_including_reset_completed' in p:p['budgeted_env_operations_physical_completed']=p['env_operations_including_reset_completed']
 if 'env_nonreset_operations_completed' in p:p['budgeted_env_nonreset_physical_completed']=p['env_nonreset_operations_completed']
 elif 'env_step_completed' in p:p['budgeted_env_nonreset_physical_completed']=p['env_step_completed']
 if 'budgeted_env_operations_physical_completed' in p:
  row['budgeted_env_measure_definition']='physical reset plus recorded step/nonreset transition operations, excluding construct/close; aliases/wrappers excluded'
failrow=ids['si.u1.eng.eval.failed-reset'];fp=failrow['physical_known'];assert fp['env_reset_physical_returned']==1 and fp['env_operations_reserved_or_spent']==1 and failrow['logical_known']['reset_unit_logical_completed']==0 and failrow['logical_known']['reset_unit_logical_failed']==1
fp['env_reset_physical_completed']=1;fp['budgeted_env_operations_physical_completed']=1;fp['budgeted_env_nonreset_physical_completed']=0
failrow['budgeted_env_measure_definition']='physical reset plus recorded step/nonreset transition operations, excluding construct/close; aliases/wrappers excluded';failrow['verification_level']='raw_archived_reset_event_linkage_recounted'
# Reset return and reservation describe the same physical operation; do not add both.
fix=ids['si.u1.eng.eval.completed']['physical_known'];assert fix['env_reset_physical_completed']==1 and fix['budgeted_env_operations_physical_completed']==2
assert fp['budgeted_env_operations_physical_completed']+fix['budgeted_env_operations_physical_completed']==3
# Explicitly match structured source fields wherever the source actually provides them.
r=read('r19_reconciliation');cases=[('r19.g2.failed-replay',r['runs'][0]),('r19.g2.successful-smoke',r['runs'][1]),('r19.g3.import-fail-a0de',r['runs'][2]),('r19.g3.failed-3d1c',r['runs'][3])]
for rid,s in cases:
 p=ids[rid]['physical_known'];assert p['budgeted_env_operations_physical_completed']==s['environment_operations_including_resets'];ids[rid]['verification_level']='structured_source_summary_matched_not_raw_recounted'
for k in ('B','C'):
 s=read('training_'+k);row=ids['si.u1.train.'+k];p=row['physical_known'];assert p['allocated_device_seconds']==s['physical_supervised_device_seconds'] and p['supervised_tokens']==s['supervised_tokens'] and row['logical_known']['optimizer_updates']==s['optimizer_updates'];row['verification_level']='structured_source_summary_matched_not_raw_recounted'
e=read('siu1_eval_ops');p=ids['si.u1.eval.c2356']['physical_known'];assert p['generation_completed']==e['actual_counters']['generations'] and p['budgeted_env_operations_physical_completed']==e['actual_counters']['environment_operations'] and p['env_construct_completed']==e['physical_operations_completed']['environment_construct'] and p['env_close_completed']==e['physical_operations_completed']['environment_close'];ids['si.u1.eval.c2356']['verification_level']='structured_source_summary_matched_not_raw_recounted'
s=read('e2_exit');assert ids['si.e2.initial-uuid-stop']['physical_known']['allocated_device_seconds']==s['elapsed_seconds'];ids['si.e2.initial-uuid-stop']['verification_level']='structured_exit_matched_failure_detail_manual_summary'
science=[r for r in rows if r['class'] in ('science','science_or_technical_run') and r['is_additive']]
gens=sum(r['physical_known']['generation_completed'] for r in science if 'generation_completed' in r['physical_known'])
ops=sum(r['physical_known']['budgeted_env_operations_physical_completed'] for r in science if 'budgeted_env_operations_physical_completed' in r['physical_known'])
assert gens==12112 and ops==15315
s01=ids['si.s01.source-f96']['physical_known'];evp=ids['si.u1.eval.c2356']['physical_known'];assert s01['env_construct_completed']==s01['env_close_completed']==96 and evp['env_construct_completed']==evp['env_close_completed']==246
construct_close=[s01['env_construct_completed'],s01['env_close_completed'],evp['env_construct_completed'],evp['env_close_completed']];assert sum(construct_close)==684
eng_seconds=sum(Decimal(str(ids[k]['physical_known']['allocated_device_seconds'])) for k in ('si.u1.eng.train.failed','si.u1.eng.train.remediation','si.u1.eng.eval.failed-reset','si.u1.eng.eval.completed'))
result={'schema':'SI_PROJECT_PARTIAL_RESOURCE_LEDGER_V2','status':'APPEND_ONLY_CORRECTION_PARTIAL_NOT_GLOBAL_TOTAL','supersedes_for_accounting_only':{'old_snapshot_path':str(OLD),'sha256':fsha(OLD),'old_snapshot_unmodified':True},'source_bindings':bindings,'raw_failure_event_archive':{'path':str(ARCHIVE),'sha256':fsha(ARCHIVE),'member':'run/engineering/engineering_events.jsonl','member_sha256':sha(raw),'start_count':len(start),'physical_returned_count':len(call),'lossless_false_count':len(snap),'unit_failed_count':len(fail),'logical_completed_count':len(done),'start_and_return_links_verified':True},'metric_definition':'budgeted physical env operations = resets plus recorded steps/nonreset transitions, excludes construct/close; logical failures/reservations describe the same call and are not added','corrected_engineering_pair':{'physical_resets':fp['env_reset_physical_completed']+fix['env_reset_physical_completed'],'physical_nonreset_steps':1,'budgeted_env_operations_physical_completed':fp['budgeted_env_operations_physical_completed']+fix['budgeted_env_operations_physical_completed'],'logical_failed_resets':1,'logical_completed_resets':1,'generation_completed':1,'method':'separate leaves; failed reset returned physically despite logical failure'},'known_science_subset':{'generation_completed':gens,'budgeted_env_operations_physical_completed':ops,'additional_constructs_source96_plus_eval':342,'additional_closes_source96_plus_eval':342,'additional_construct_and_close_calls':684,'scope':'Selected known leaves, construct/close separate; unknown earlier research and engineering excluded; not a full project total.'},'known_siu1_four_engineering_allocations_decimal_seconds':str(eng_seconds),'rows':rows,'omitted_metrics':'unknown_or_not_applicable_never_zero','recount_limits':['Only failed reset raw archived event linkage is independently reconstructed here; structured sources matched for enumerated fields.','Many historical figures are manual source-summary transcriptions, not raw-ledger recomputations; unknowns remain.','Attribution-pending engineering aggregate is explicitly non-additive until verified.','No CUDA/model/environment or old evidence mutation.']}
assert fsha(OLD)=='1f55ee5cc4404e3566e53d8897620c1f0bf50f5764bf2e14d2f5bba712f9ab59' and fsha(ARCHIVE)=='f17526737a8c050a9cfc7f6b4373a626ea99b9fbfd08dd323c2565a2460e3cdf'
(O/'PARTIAL_ACTUAL_LEDGER_V2.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ('raw_failure_event_archive','corrected_engineering_pair','known_science_subset','known_siu1_four_engineering_allocations_decimal_seconds')},indent=2))
