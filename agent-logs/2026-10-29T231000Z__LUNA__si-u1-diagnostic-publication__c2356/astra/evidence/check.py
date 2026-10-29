import json,hashlib,sys,re
from pathlib import Path
from collections import Counter,defaultdict
b=Path(__file__).parent.parent;src=Path('/home/lizening/research-notes/agent-logs/2026-10-29T222600Z__SOL__si-u1-disagreement-diagnostic__c2356');a=json.loads((b/'FINAL_PILOT82_PAIRED_ANALYSIS_C2356.json').read_text());pairs=a['paired_records'];dis={p['task_id'] for p in pairs if p['C']!=p['A'] or p['C']!=p['B']};two={p['task_id'] for p in pairs if p['family']=='pick_two_obj_and_place'};assert len(dis)==9 and len(two)==8 and not dis&two;chosen=dis|two
cases=json.loads((src/'PRIVATE_CASE_TABLE.json').read_text())['cases'];assert {c['task_id'] for c in cases}==chosen;priv={c['task_id']:c for c in cases};div=json.loads((src/'PRIVATE_FIRST_DIVERGENCE.json').read_text())['items'];divlookup={(r['task_id'],r['comparison']):r for r in div}
def dig(v):return hashlib.sha256(json.dumps(v,ensure_ascii=True,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for s in iter(lambda:f.read(1048576),b''):h.update(s)
 return h.hexdigest()
events=Path('/home/lizening/research-notes/agent-logs/2026-10-29T145200Z__LUNA__si-u1-production-preflight-proposal__853/run_parent/evaluation_c2356bbda2b44159a333e7c9d24fc2d4/evaluation/events.jsonl');assert sha(events)==a['evidence_hashes'][str(events)]
sys.path.insert(0,'/home/lizening/wt-si-self-imitation-evaluator/src')
from models.protocol_stability import parse_p2_selection
from models.action_parser import action_id_mapping
states={};gens=defaultdict(list);prepared={};requests={};episodes={}
for line in events.open('rb'):
 row=json.loads(line);k=row['kind'];p=row['payload'];i=p.get('identity',{});task=i.get('task_id',p.get('task_id'));arm=i.get('arm',p.get('arm'));key=(task,arm)
 if task not in chosen:continue
 if k=='unit_started':
  if i['op']=='generation':prepared[key]=p['prepared']
  elif i['op']=='step':requests[key]=p['request']
 elif k=='unit_completed':
  op=i['op'];data=p['data']
  if op=='reset':states[key]=data
  elif op=='generation':
   st=states[key];parsed=parse_p2_selection(data['raw_output'],st['valid_actions'],reflection_required=False);assert parsed.selection_status=='selected';idx=i['index'];assert idx==len(gens[key]);pv=priv[task]['arms'][arm]['timeline'][idx]
   assert pv['generation_event_sequence']==row['sequence'] and pv['generation_event_id']==row['event_id'] and pv['raw_output']==data['raw_output'] and pv['command']==parsed.action and pv['action_id']==parsed.action_id
   assert pv['before_observation_sha256']==dig(st['observation']) and pv['before_action_map_sha256']==dig(st['valid_actions']);assert not data['token_cap_reached'] and data['output_complete'] is True
   gens[key].append({'command':parsed.action,'action_id':parsed.action_id,'obs':dig(st['observation']),'map':dig(st['valid_actions']),'input':{x:dig(prepared[key][x]) for x in ('prompt','rendered_prompt','input_ids','attention_mask')}})
  elif op=='step':
   g=gens[key][-1];assert requests[key]=={'action_id':g['action_id'],'command':g['command'],'action_map':action_id_mapping(states[key]['valid_actions'])};pv=priv[task]['arms'][arm]['timeline'][i['index']];assert pv['step_event_sequence']==row['sequence'] and pv['step_event_id']==row['event_id'] and pv['after_done']==data['done'] and pv['after_reward']==data['reward'];states[key]=data
 elif k=='episode_closed':episodes[key]=p
assert len(episodes)==51 and sum(map(len,gens.values()))==2206
summary={};patterns={};adjacent=0
for arm in 'ABC':
 success=sum(episodes[(task,arm)]['outcome'] for task in chosen);failure=17-success;bad=[episodes[(task,arm)] for task in chosen if not episodes[(task,arm)]['outcome']];assert all(p['steps']==50 and p['end_state']['done'] is True and p['end_state']['reward']==0 for p in bad);summary[arm]={'success':success,'failure':failure};pc=Counter()
 for task in chosen:
  g=gens[(task,arm)];commands=[x['command'] for x in g];repeated=any(commands[j:j+w]==commands[j+w:j+2*w] for w in (2,3,4) for j in range(len(commands)-2*w+1));cat='success' if episodes[(task,arm)]['outcome'] else 'failure';pc[cat]+=int(repeated)
  if task in two:pc['pick_two']+=int(repeated)
  adjacent+=sum((x['obs'],x['map'])==(y['obs'],y['map']) for x,y in zip(g,g[1:]))
 patterns[arm]=dict(pc)
compared=0
for pair in pairs:
 task=pair['task_id']
 if task not in dis:continue
 for other in 'AB':
  if pair['C']==pair[other]:continue
  left,right=gens[(task,'C')],gens[(task,other)];idx=next(i for i,(x,y) in enumerate(zip(left,right)) if x['command']!=y['command']);assert left[idx]['input']==right[idx]['input'] and left[idx]['obs']==right[idx]['obs'] and left[idx]['map']==right[idx]['map'];entry=divlookup[(task,'C_vs_'+other)];assert idx==entry['zero_based_step'] and all(entry['same_full_input_flags'].values());compared+=1
assert compared==11 and adjacent==0
train=Path('/home/lizening/research-notes/agent-logs/2026-10-29T115700Z__SOL__si-pilot82-dataset-materialization');coverage={};sets={}
for arm in 'BC':
 rows=[json.loads(x) for x in (train/(arm+'_candidate_PRIVATE.jsonl')).read_text().splitlines()];groups={r['task_group'] for r in rows};two_rows=[r for r in rows if r['family']=='pick_two_obj_and_place'];labels=defaultdict(set)
 for r in rows:assert hashlib.sha256(r['prompt'].encode()).hexdigest()==r['rendered_prompt_sha256'];assert re.fullmatch('A[0-9]{3}',r['completion']);labels[r['rendered_prompt_sha256']].add(r['completion'])
 assert len(rows)==312 and len(groups)==78 and len(labels)==312 and all(len(v)==1 for v in labels.values());assert len(two_rows)==8 and len({r['task_group'] for r in two_rows})==2
 m=json.loads((train/(arm+'_manifest_candidate_PRIVATE.json')).read_text());assert all(Counter(m['ordered_sample_ids'][312*i:312*(i+1)])==Counter(r['sample_id'] for r in rows) for i in range(4));sets[arm]=(groups,set(labels));coverage[arm]={'parents':78,'rows':312,'pick_two_parents':2,'pick_two_rows':8,'exact_prompt_conflicts':0,'unique_prompts':312}
assert not sets['B'][0]&sets['C'][0] and not sets['B'][1]&sets['C'][1]
r={'status':'PASS_DESCRIPTIVE_COUNTS_AND_METHOD_WITH_LIMITS','selected_tasks':17,'disagreement_tasks':9,'pick_two_tasks':8,'trajectories':51,'generations':2206,'outcomes':summary,'all37_failures_50_steps_done_true_reward_zero':True,'first_divergence_equal_recorded_inputs_comparisons':compared,'repeated_block_2_to_4_counts':patterns,'adjacent_identical_observation_and_map':adjacent,'training_coverage':coverage,'input_difference_tokens':695872-661620,'input_difference_relative_to_B':(695872-661620)/661620,'no_private_identifiers_emitted':True,'model_environment_calls':0}
Path(__file__).with_name('RESULT.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r))
