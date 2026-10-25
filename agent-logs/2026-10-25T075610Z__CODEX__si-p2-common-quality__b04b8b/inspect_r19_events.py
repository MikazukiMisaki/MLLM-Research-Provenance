from audit_io import *
from collections import Counter
m=authority();pr=[(c,r) for c,r in parent_rows(m) if c['stage']=='R19_K1'];need=set()
for c,r in pr:
 a=r['k_results']['1'];need.add(r['evidence_refs']['prefix_attempt_event_id']);need.add(a['arm_event_id'])
 for key,ids in a['evidence_refs'].items():need.update(ids)
events={e['event_id']:(n,h,e) for n,h,e in rows(R19/'execution_events.jsonl') if e['event_id'] in need}
counts=Counter();sample=set();summary=[]
for c,r in pr:
 a=r['k_results']['1'];gs=[events[x][2] for x in a['evidence_refs']['recovery_generation_event_ids']]
 g1=next((g for g in gs if g['identity'].get('component')=='stage1'),None)
 g2=[g for g in gs if g['identity'].get('component')=='stage2']
 status1=(g1 or {}).get('payload',{}).get('evidence',{}).get('status');status2=[g['payload']['evidence'].get('status') for g in g2]
 row={'case_id':c['case_id'],'s1':status1,'s2':status2,'gen_count':len(gs),'recovery_steps':len(a['evidence_refs']['recovery_transition_event_ids']),'suffix_steps':len(a['evidence_refs']['suffix_transition_event_ids']),'reason':a['stopping_reason'],'sft_reason':a['sft_termination_reason'],'sft_terminal':a['sft_terminal'],'success':a['success'],'derived_source_event_id':a.get('derived_source_event_id'),'eligibility':r['eligibility_reason']}
 summary.append(row);counts[str((status1,tuple(status2),row['recovery_steps'],a['stopping_reason'],a['sft_termination_reason']))]+=1
 if (status1,tuple(status2)) not in sample:
  sample.add((status1,tuple(status2)));print('STATUS_EXAMPLE',json.dumps(row))
  for g in [g1,*g2]:
   if g:print('GENSHAPE',g['kind'],g['identity'],list(g['payload']),list(g['payload']['evidence']),{k:v for k,v in g['payload']['evidence'].items() if k in ['status','failure_reason','action_id','command']})
  pe=events[r['evidence_refs']['prefix_attempt_event_id']][2];print('PREFIXKEYS',list(pe['payload']));print('PREFIXSCALARS',{k:v for k,v in pe['payload'].items() if not isinstance(v,(dict,list))});print('INITIAL',pe['payload']['replay_evidence'])
  if a['evidence_refs']['recovery_transition_event_ids']:
   tr=events[a['evidence_refs']['recovery_transition_event_ids'][0]][2];ac=tr['payload']['action'];print('ACTIONSHAPE',tr['kind'],tr['identity'],list(ac),{k:v for k,v in ac.items() if k in ['command','action_id','operation_event_id','recovery_action_index']})
  print('ARMKEYS',list(events[a['arm_event_id']][2]['payload']))
print('COUNTS',dict(counts));output('r19_event_shape_inspection.json',summary);finish_bindings('r19_inspection_input_bindings.json')
