"""Post-exit provenance/cost check only; never emit or extract success outcomes."""
import collections,hashlib,json,math,os,sys
from pathlib import Path
root=Path('/home/lizening/wt-si-self-imitation-evaluator');sys.path.insert(0,str(root/'src'))
from self_improvement.si_transfer_eval.live_audit import authenticate_run,audit_resources
output=Path('/home/lizening/research-notes/agent-logs/2026-10-29T145200Z__LUNA__si-u1-production-preflight-proposal__853/run_parent/evaluation_c2356bbda2b44159a333e7c9d24fc2d4');here=Path(__file__).resolve().parent
manifest=json.loads(Path('/home/lizening/research-notes/agent-logs/2026-10-29T144100Z__SOL__si-u1-stage2-plan__2060cc8/stage2/manifest.json').read_text())
binding=authenticate_run(output);resources=audit_resources(output,manifest)
assert binding['binding']['run_id']=='c2356bbda2b44159a333e7c9d24fc2d4'
previous=None;sequence=0;last=-float('inf');kind_counts=collections.Counter();active=None;completed=collections.Counter();starts=collections.Counter();failed=collections.Counter();actual=collections.Counter();arms_started=[];arms_finished=[];first=None;last_kind=None;eventfile=output/'evaluation/events.jsonl';rawhash=hashlib.sha256()
with eventfile.open('rb') as f:
 for line in f:
  rawhash.update(line);assert line.endswith(b'\n');row=json.loads(line);assert set(row)=={'sequence','previous','kind','payload','monotonic','event_id'} and row['sequence']==sequence and row['previous']==previous and type(row['monotonic']) in (int,float) and math.isfinite(row['monotonic']) and row['monotonic']>=last
  digest=hashlib.sha256(json.dumps({k:v for k,v in row.items() if k!='event_id'},ensure_ascii=True,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest();assert digest==row['event_id'];kind=row['kind'];p=row['payload'];kind_counts[kind]+=1
  if kind=='unit_started':assert active is None;active=(p['unit'],p['identity']['op']);starts[active[1]]+=1
  elif kind in ('unit_completed','unit_failed'):
   assert active is not None and p['unit']==active[0] and p['identity']['op']==active[1]
   if kind=='unit_completed':
    completed[active[1]]+=1
    for k,v in p['actual'].items():assert type(v) is int and v>=0;actual[k]+=v
   else:failed[active[1]]+=1
   active=None
  elif kind=='arm_started':arms_started.append(p['arm'])
  elif kind=='arm_finished':arms_finished.append(p['arm'])
  if first is None:first=kind
  last_kind=kind;sequence+=1;previous=digest;last=row['monotonic']
assert first=='run_opened' and last_kind=='run_closed' and active is None and arms_started==arms_finished==['A','B','C'] and not failed
assert all(starts[k]==completed[k] for k in starts)
assert completed['reset']==246 and completed['environment_construct']==246 and completed['environment_close']==246 and completed['model_load']==completed['model_close']==3
assert actual['environment_operations']==completed['reset']+completed['step'] and actual['generations']==completed['generation']
assert all(actual[k]<=manifest['limits'][k] for k in ('generations','environment_operations','input_tokens','output_tokens'))
assert not any(k=='torch' or k.startswith('torch.') or k=='alfworld' or k.startswith('alfworld.') for k in sys.modules)
result={'schema':'SI_U1_LUNA_EVALUATION_OPERATIONAL_AUDIT_V1','status':'OPERATIONAL_CHECKS_PASS_AWAIT_INDEPENDENT_FULL_AUDIT','native_binding':binding,'journal_sha256':rawhash.hexdigest(),'journal_rows':sequence,'journal_hash_chain_and_monotonicity_verified':True,'run_closed':True,'arms_opened_and_closed':arms_finished,'physical_operations_started':dict(starts),'physical_operations_completed':dict(completed),'physical_operations_failed':dict(failed),'actual_counters':dict(actual),'resource_validation':resources,'incomplete_active_units':0,'no_model_cuda_or_environment_invoked':True,'no_success_outcomes_extracted':True,'note':'Operational checks do not replace approved complete provenance/outcome extractor and independent scientific analysis.'}
path=here/'OPERATIONAL_AUDIT_NO_OUTCOMES.json'
with path.open('x') as f:json.dump(result,f,sort_keys=True,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps({'status':result['status'],'audit_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'journal_sha256':result['journal_sha256'],'journal_rows':sequence,'completed_counts':dict(completed),'actual_counters':dict(actual),'resource_rows':resources['resource_rows']}))
