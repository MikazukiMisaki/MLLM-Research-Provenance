import collections,hashlib,json,os,pathlib
P=pathlib.Path(__file__).resolve().parent;cases=json.loads((P/'PRIVATE_CASE_TABLE.json').read_bytes())['cases'];F=pathlib.Path('/home/lizening/research-notes/agent-logs/2026-10-29T145200Z__LUNA__si-u1-production-preflight-proposal__853/run_parent/evaluation_c2356bbda2b44159a333e7c9d24fc2d4/evaluation/events.jsonl');A=pathlib.Path('/home/lizening/research-notes/agent-logs/2026-10-29T113523Z__ASTRA__three-arm-prospective-design__a55d1af9/FINAL_PILOT82_PAIRED_ANALYSIS_C2356.json')
def sha_file(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def dig(x):return hashlib.sha256(json.dumps(x,ensure_ascii=True,sort_keys=True,separators=(',',':')).encode()).hexdigest()
expected=json.loads(A.read_bytes())['evidence_hashes'][str(F)];assert sha_file(F)==expected
need={}
for c in cases:
 for other in 'AB':
  comp=c['comparisons']['C_vs_'+other];i=comp['first_command_difference_index']
  if comp['outcome_delta']!=0:
   assert i is not None
   for arm in ('C',other):need[(c['task_id'],arm,i)]=None
with F.open() as f:
 for line in f:
  event=json.loads(line)
  if event['kind']!='unit_started':continue
  p=event['payload'];i=p['identity'];key=(i.get('task_id'),i.get('arm'),i.get('index'))
  if i.get('op')=='generation' and key in need:
   assert need[key] is None;prep=p['prepared'];need[key]={'public_prompt_sha256':dig(prep['prompt']),'rendered_prompt_sha256':dig(prep['rendered_prompt']),'input_ids_sha256':dig(prep['input_ids']),'attention_mask_sha256':dig(prep['attention_mask']),'source_sequence':event['sequence'],'source_event_id':event['event_id']}
assert all(v is not None for v in need.values())
items=[];summary=collections.Counter()
for c in cases:
 for other in 'AB':
  comp=c['comparisons']['C_vs_'+other];i=comp['first_command_difference_index']
  if comp['outcome_delta']:
   x=need[(c['task_id'],'C',i)];y=need[(c['task_id'],other,i)];flags={k+'_equal':x[k+'_sha256']==y[k+'_sha256'] for k in ('public_prompt','rendered_prompt','input_ids','attention_mask')};summary['compared']+=1
   for k,v in flags.items():summary[k]+=int(v)
   items.append({'case_id':c['case_id'],'task_id':c['task_id'],'comparison':'C_vs_'+other,'outcome_delta':comp['outcome_delta'],'zero_based_step':i,'same_observation_and_action_map':comp['same_observation_and_map_at_first_command_difference'],'same_full_input_flags':flags,'C_source':x,'other_source':y})
assert summary['compared']==11 and sha_file(F)==expected
agg={'schema':'SI_U1_DESCRIPTIVE_FIRST_DIVERGENCE_V1','counts':dict(summary),'comparisons':'11 outcome-discordant pairs across nine tasks; the same task can occur in both contrasts.','interpretation':'Equality establishes identical recorded inputs at the first different executed command, not that the divergence caused final outcome; analysis is selected post outcome.','events_sha256':expected,'single_analyst_review_pending':True}
for name,obj in [('FIRST_DIVERGENCE_AGGREGATE.json',agg),('PRIVATE_FIRST_DIVERGENCE.json',{'items':items})]:
 with (P/name).open('x') as f:json.dump(obj,f,indent=2,sort_keys=True);f.write('\n');f.flush();os.fsync(f.fileno())
 os.chmod(P/name,0o600)
print(json.dumps(agg,sort_keys=True))
