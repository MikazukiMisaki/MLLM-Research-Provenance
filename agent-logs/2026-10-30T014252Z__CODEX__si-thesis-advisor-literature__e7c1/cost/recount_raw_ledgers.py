#!/usr/bin/env python3
"""Read-only, aggregate-only audit of historical physical event ledgers."""
from pathlib import Path
from collections import Counter
import hashlib,json
N=Path('/home/lizening/research-notes/agent-logs');W=Path('/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime')
sources=list(Path('/tmp').glob('si_s01_source_uid-2000_run-f96b86f3391940eaa9d75040c444a8e4_*/raw/source_events.jsonl'));assert len(sources)==1
G=list(W.glob('r19_b1_g3_successor*/execution_events.jsonl'));assert len(G)==1
F={
 'g2_failed':N/'2026-10-22T072356Z__ASTRA__r19-b1-g2__a7d913c4/g2-output/execution_events.jsonl',
 'g2_success':N/'2026-10-22T091640Z__CODEX__r19-b1-replay-repair__92aae1d/g2_evidence/execution_events.jsonl',
 'g3_failed':W/'r19_b1_g3_pilot_after_a0de515d7e104101bf8157175ea3d995_20261022T190221Z/execution_events.jsonl',
 'g3_success':G[0],
 'source96':sources[0],
 'm1':N/'2026-10-29T111600Z__LUNA__si-m1-live-raw-provenance__dfa382/raw/output/probe_events.jsonl',
 'siu1_eval':N/'2026-10-29T145200Z__LUNA__si-u1-production-preflight-proposal__853/run_parent/evaluation_c2356bbda2b44159a333e7c9d24fc2d4/evaluation/events.jsonl'}
E={'g2_failed':'b2d9045514bc3251ee3e954e4787569566cf7ba995821adbdb5af6b1dfdf065c','g2_success':'1456c43f7d3f0a849fe4bb8015164815fd70f4e2813d343449c1a34c2eaebe0c','g3_failed':'fde95fcd72f1c4ac6409fab7f2112654e145f6184fefec690cae58ad345f1cd7','g3_success':'05e1d443ff304eaa25d08b92a4e19d204a6c93a4f46bbe50aefef3271f211762','source96':'04ce4c0f32f40a3dbff6f42fec3c54107534ec45dd005795bd52014442513105','m1':'3d635accc0538670a670763cb380afa645135311d0587e3a871656124086f1f0','siu1_eval':'6146bb79faeb572c3674ff9ba907fac4be25eff4c2bd161a3d7cf3156d81c96e'}
def hashfile(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
assert {k:hashfile(p) for k,p in F.items()}==E
out={}
for label in ('g2_failed','g2_success','g3_failed','g3_success'):
 events=Counter();op=Counter();prev=-1
 with F[label].open() as f:
  for line in f:
   e=json.loads(line);assert e['sequence']>prev;prev=e['sequence'];k=e['kind'];events[k]+=1
   if k=='environment_operation_completed':op[e['identity'].get('operation')]+=1
 for x in ('generation','environment_operation'):assert events[x+'_started']==events[x+'_completed']
 reset=sum(v for k,v in op.items() if 'reset' in k);nonreset=sum(op.values())-reset
 out[label]={'generation_started':events['generation_started'],'generation_completed':events['generation_completed'],'reset_completed':reset,'nonreset_completed':nonreset,'env_operations_completed':sum(op.values()),'wrapper_step_completion_events_excluded':events['environment_step_completed'],'operation_counts':dict(op),'counts_only_not_complete_external_identity_or_hash_chain_revalidation':True}
for label in ('source96','m1','siu1_eval'):
 counts=Counter();starts={};completed=set();tokens=Counter();prev=-1;runclosed=0
 with F[label].open() as f:
  for line in f:
   e=json.loads(line);assert e['sequence']>prev;prev=e['sequence'];k=e['kind'];p=e['payload']
   if k=='run_closed':runclosed+=1
   if k=='unit_started':
    assert e['event_id'] not in starts;starts[e['event_id']]=(p['unit'],p['identity'])
   elif k=='unit_completed':
    se=p['started_event'];assert se in starts and se not in completed and starts[se]==(p['unit'],p['identity']);completed.add(se)
    kind=p['identity'].get('kind',p['identity'].get('op'));counts[kind]+=1
    if label=='siu1_eval':
     for t in ('input_tokens','output_tokens'):tokens[t]+=p['actual'][t]
    elif kind in ('generation','stage_one','stage_two'):
     tokens['input_tokens']+=p['data']['raw']['input_tokens'];tokens['output_tokens']+=p['data']['raw']['generated_tokens']
 assert set(starts)==completed and runclosed==1
 gen=counts['generation'] if label!='m1' else counts['stage_one']+counts['stage_two']
 reset=counts['reset'];steps=counts['step'] if label!='m1' else counts['replay']+counts['teacher_step']
 out[label]={'generation_completed':gen,'reset_completed':reset,'nonreset_steps_completed':steps,'env_operations_including_reset':reset+steps,'construct_completed':counts.get('env_construct',counts.get('environment_construct',0)),'close_completed':counts.get('env_close',counts.get('environment_close',0)),'model_load_completed':counts['model_load'],'input_tokens':tokens['input_tokens'],'output_tokens':tokens['output_tokens'],'started_and_completed_units':len(starts),'unmatched_started_units':len(starts)-len(completed),'unit_counts':dict(counts),'scope':'Recorded unit linkage only; does not revalidate full journal chain, actual processes, hidden/unrecorded calls, or task outcomes.'}
assert [(out[x]['generation_completed'],out[x]['env_operations_completed']) for x in ('g2_failed','g2_success','g3_failed','g3_success')]==[(0,19),(176,322),(1,1),(4965,7607)]
assert [(out[x]['generation_completed'],out[x]['env_operations_including_reset']) for x in ('source96','m1','siu1_eval')]==[(1959,2055),(10,64),(5001,5247)]
assert [(out[x]['input_tokens'],out[x]['output_tokens']) for x in ('source96','m1','siu1_eval')]==[(1164593,9795),(5846,184),(2734940,25005)]
assert {k:hashfile(p) for k,p in F.items()}==E
aggregate={'completed_generations':sum(out[x]['generation_completed'] for x in out),'reset_inclusive_env_operations':sum(out[x].get('env_operations_completed',out[x].get('env_operations_including_reset',0)) for x in out),'excluded_known_earlier_import_failure':True,'construct_close_outside_env_operation_count':True}
assert aggregate['completed_generations']==12112 and aggregate['reset_inclusive_env_operations']==15315
aggregate['known_construct_completed_source96_m1_eval']=sum(out[k]['construct_completed'] for k in ('source96','m1','siu1_eval'))
aggregate['known_close_completed_source96_m1_eval']=sum(out[k]['close_completed'] for k in ('source96','m1','siu1_eval'))
assert aggregate['known_construct_completed_source96_m1_eval']==aggregate['known_close_completed_source96_m1_eval']==347
result={'status':'PASS_SELECTED_RAW_LEDGER_COUNTS_NOT_FULL_PROJECT','input_paths_and_sha256':{k:{'path':str(F[k]),'sha256':E[k]} for k in F},'per_run':out,'subtotal_selected_raw_ledgers':aggregate,'limits':['Counting recorded starts/completions does not prove absence of unrecorded work.','R19 counts do not independently verify paired event identity or full chain; use prior authenticated reconciliation and original validators.','SI logs use linked started/completed unit IDs; this is not a replay of full integrity checks or authentication of resource ownership.','Actual training and engineering are not generation/environment leaves in this subtotal; earlier import failure and missing historical runs remain separate, unknown or nonadditive.','Environment construct and close are distinct lifecycle operations outside reset-plus-nonreset counts.']}
Path(__file__).with_name('RAW_LEDGER_RECOUNT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':result['status'],'subtotal':aggregate,'source96':out['source96'],'m1':out['m1'],'siu1_eval':out['siu1_eval']},sort_keys=True))
