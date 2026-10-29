"""Read-only post-outcome descriptive inspection; no model/world execution."""
import collections,datetime,hashlib,json,os,pathlib,re
P=pathlib.Path(__file__).resolve().parent
A=pathlib.Path('/home/lizening/research-notes/agent-logs/2026-10-29T113523Z__ASTRA__three-arm-prospective-design__a55d1af9/FINAL_PILOT82_PAIRED_ANALYSIS_C2356.json')
M=pathlib.Path('/home/lizening/research-notes/agent-logs/2026-10-29T144100Z__SOL__si-u1-stage2-plan__2060cc8/stage2/manifest.json')
D=pathlib.Path('/home/lizening/research-notes/agent-logs/2026-10-29T145200Z__LUNA__si-u1-production-preflight-proposal__853/run_parent/evaluation_c2356bbda2b44159a333e7c9d24fc2d4')
F=D/'evaluation/events.jsonl';R=D/'evaluation/report.json';RUN='c2356bbda2b44159a333e7c9d24fc2d4'
def sha(p):
 h=hashlib.sha256()
 with pathlib.Path(p).open('rb') as f:
  for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
 return h.hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()
def save(name,obj):
 with (P/name).open('x',encoding='utf-8') as f:json.dump(obj,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
 os.chmod(P/name,0o600)
assert sha(A)=='4a3ea016d4c06022980482ac9dbc58155a68bbe20fbc723a68ce49c7c345ea9b' and sha(M)=='7d1b61a9054f99a40fe895c7bb292a81e7a578bbd5fc6bf0777157676213e338'
a=json.loads(A.read_bytes());m=json.loads(M.read_bytes());report=json.loads(R.read_bytes());assert a['run_id']==RUN and a['production_audit']['status']=='AUDIT_PASS_LIVE' and a['production_audit']['report_status']=='COMPLETE' and a['production_audit']['episode_count']==246 and not a['production_audit']['pending_na_count']
before={str(p):sha(p) for p in (A,M,F,R)};assert before[str(F)]==a['evidence_hashes'][str(F)] and before[str(R)]==a['evidence_hashes'][str(R)]
pairs=a['paired_records'];tasks=m['tasks'];eps=report['episodes'];assert len(pairs)==len(tasks)==82 and len(eps)==246 and report['status']=='COMPLETE' and report['pending_na']==[]
selected=[]
for i,(t,pair) in enumerate(zip(tasks,pairs)):
 assert (pair['task_id'],pair['family'])==(t['task_id'],t['family']) and set(pair)=={'task_id','family','A','B','C'}
 for arm_idx,arm in enumerate('ABC'):
  e=eps[arm_idx*82+i];assert (e['task_id'],e['family'],e['seed'],e['arm'],bool(e['outcome']))==(t['task_id'],t['family'],t['seed'],arm,pair[arm])
 if pair['C']!=pair['A'] or pair['C']!=pair['B'] or pair['family']=='pick_two_obj_and_place':selected.append({'order_index':i,'task_id':t['task_id'],'family':t['family'],'pair':pair,'arms':{a:{'unit_starts':{},'unit_completions':{},'episode_closed':None} for a in 'ABC'}})
lookup={c['task_id']:c for c in selected}; assert len(lookup)==len(selected) and sum(c['family']=='pick_two_obj_and_place' for c in selected)==8
with F.open(encoding='utf-8') as f:
 for line in f:
  row=json.loads(line);kind=row['kind'];p=row['payload'];ident=p.get('identity',{}) if type(p) is dict else {};task=ident.get('task_id') if ident else p.get('task_id');arm=ident.get('arm') if ident else p.get('arm')
  if task not in lookup or arm not in 'ABC' or len(arm)!=1:continue
  dest=lookup[task]['arms'][arm]
  if kind in ('unit_started','unit_completed'):
   op=ident.get('op');idx=ident.get('index');key=f'{op}:{idx}' if idx is not None else op
   store=dest['unit_starts' if kind=='unit_started' else 'unit_completions'];assert key not in store
   store[key]={'sequence':row['sequence'],'event_id':row['event_id'],'payload':p}
  elif kind=='episode_closed':assert dest['episode_closed'] is None;dest['episode_closed']={'sequence':row['sequence'],'event_id':row['event_id'],'payload':p}

def max_consecutive(seq):
 best=run=0;prev=object()
 for x in seq:
  run=run+1 if x==prev else 1;prev=x;best=max(best,run)
 return best
summary_counts={a:collections.Counter() for a in 'ABC'};private=[];pair_directions=collections.Counter()
for ci,c in enumerate(selected,1):
 pair=c['pair'];case={'case_id':f'case_{ci:02d}','task_id':c['task_id'],'schedule_index':c['order_index'],'family':c['family'],'selection_reason':{'C_vs_A_disagrees':pair['C']!=pair['A'],'C_vs_B_disagrees':pair['C']!=pair['B'],'pick_two_all':c['family']=='pick_two_obj_and_place'},'paired_results':{a:pair[a] for a in 'ABC'},'arms':{},'comparisons':{}}
 for other in 'AB':
  if pair['C']!=pair[other]:pair_directions[f'C_vs_{other}_'+('win' if pair['C'] else 'loss')]+=1
 for arm in 'ABC':
  x=c['arms'][arm];starts=x['unit_starts'];ends=x['unit_completions'];ep=x['episode_closed'];assert ep is not None;erow=ep['payload'];assert erow['outcome']==int(pair[arm]);
  assert 'reset' in ends and 'environment_close' in ends
  gs=sorted((int(k.split(':')[1]),v) for k,v in ends.items() if k.startswith('generation:'));st=sorted((int(k.split(':')[1]),v) for k,v in ends.items() if k.startswith('step:'))
  assert [i for i,_ in gs]==list(range(len(gs))) and [i for i,_ in st]==list(range(len(st))) and len(st)==erow['steps'] and len(gs) in (len(st),len(st)+1)
  state=ends['reset']['payload']['data'];timeline=[];parser=collections.Counter();total_in=total_out=0
  for i,gen in gs:
   g=gen['payload']['data'];raw=g['raw_output'];lines=[v.strip() for v in raw.splitlines() if v.strip()];last=lines[-1] if lines else '';actions=state.get('valid_actions');assert type(actions) is list and bool(actions)
   if re.fullmatch(r'A\d{3}',last) is None:status='action_format_violation';aid=None;command=None
   else:
    aid=last;idx=int(last[1:]);status='selected' if idx<len(actions) else 'action_out_of_range';command=actions[idx] if status=='selected' else None
   parser[status]+=1;total_in+=g['input_tokens'];total_out+=g['generated_tokens']
   item={'index':i,'generation_event_sequence':gen['sequence'],'generation_event_id':gen['event_id'],'raw_output':raw,'output_complete':g['output_complete'],'token_cap_reached':g['token_cap_reached'],'input_tokens':g['input_tokens'],'output_tokens':g['generated_tokens'],'parser_status_reconstructed':status,'action_id':aid,'command':command,'before_observation_sha256':digest(state['observation']),'before_action_map_sha256':digest(actions)}
   if i<len(st):
    step=st[i][1];request=starts[f'step:{i}']['payload']['request'];assert status=='selected' and request['action_id']==aid and request['command']==command and request['action_map']=={f'A{j:03d}':v for j,v in enumerate(actions)}
    next_state=step['payload']['data'];item.update({'step_event_sequence':step['sequence'],'step_event_id':step['event_id'],'after_observation_excerpt':next_state['observation'][:240],'after_observation_sha256':digest(next_state['observation']),'after_done':next_state['done'],'after_reward':next_state['reward'],'after_truncated':next_state['truncated']});state=next_state
   else:assert status!='selected' and erow['termination']=='selection_failure'
   timeline.append(item)
  assert erow['termination'] in ('terminal','horizon','selection_failure') and bool(erow['end_state']['done'])==bool(state['done']) and erow['end_state']['reward']==state['reward']
  cmds=[z['command'] for z in timeline if z['command'] is not None];statekeys=[(z['before_observation_sha256'],z['before_action_map_sha256']) for z in timeline if z['command'] is not None];same_state_adjacent=sum(statekeys[i]==statekeys[i-1] for i in range(1,len(statekeys)))
  category=('success_terminal' if erow['outcome']==1 else 'failure_'+erow['termination'])
  arm_summary={'outcome':erow['outcome'],'termination':erow['termination'],'category_observed':category,'steps':len(st),'generation_count':len(gs),'input_tokens':total_in,'output_tokens':total_out,'last_done':state['done'],'last_reward':state['reward'],'last_truncated':state['truncated'],'parser_counts':dict(parser),'max_consecutive_identical_commands':max_consecutive(cmds),'consecutive_same_observation_and_action_map_count':same_state_adjacent,'episode_closed_sequence':ep['sequence'],'episode_closed_event_id':ep['event_id'],'diagnostic_cause':'UNKNOWN','timeline':timeline}
  case['arms'][arm]=arm_summary;summary_counts[arm][category]+=1
  if max_consecutive(cmds)>=3:summary_counts[arm]['consecutive_identical_command_ge3']+=1
  if same_state_adjacent:summary_counts[arm]['consecutive_same_observation_and_map']+=1
 for other in 'AB':
  csteps=case['arms']['C']['timeline'];osteps=case['arms'][other]['timeline'];first_command=next((i for i,(a,b) in enumerate(zip(csteps,osteps)) if a['command']!=b['command']),None);first_state=next((i for i,(a,b) in enumerate(zip(csteps,osteps)) if (a['before_observation_sha256'],a['before_action_map_sha256'])!=(b['before_observation_sha256'],b['before_action_map_sha256'])),None)
  case['comparisons']['C_vs_'+other]={'outcome_delta':int(pair['C'])-int(pair[other]),'first_command_difference_index':first_command,'first_observation_or_action_map_difference_index':first_state,'comparison_only_available_to_shorter_trajectory':True,'same_observation_and_map_at_first_command_difference':None if first_command is None else (csteps[first_command]['before_observation_sha256'],csteps[first_command]['before_action_map_sha256'])==(osteps[first_command]['before_observation_sha256'],osteps[first_command]['before_action_map_sha256']),'same_full_prompt_not_established':True}
 private.append(case)
assert pair_directions=={'C_vs_A_win':3,'C_vs_A_loss':1,'C_vs_B_win':3,'C_vs_B_loss':4}
after={str(p):sha(p) for p in (A,M,F,R)};assert before==after
base={'schema':'SI_U1_POSTRESULT_DESCRIPTIVE_DIAGNOSTIC_V1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'run_id':RUN,'input_sha256':{pathlib.Path(k).name:v for k,v in before.items()},'selection_counts':{'selected_union':len(selected),'pick_two_tasks':8,'C_vs_A_disagreement_tasks':4,'C_vs_B_disagreement_tasks':7,'both_comparisons_disagreement':sum(c['selection_reason']['C_vs_A_disagrees'] and c['selection_reason']['C_vs_B_disagrees'] for c in private)},'pair_directions':dict(pair_directions),'selected_episode_count':len(selected)*3,'arm_counts':{k:dict(v) for k,v in summary_counts.items()},'definitions':{'consecutive_identical_command_ge3':'At least three consecutive identical executed command strings; does not establish a harmful loop.','consecutive_same_observation_and_map':'At least one adjacent pair of steps with identical observable text and available-action list; excludes prior history and is not full prompt equality.','diagnostic_cause':'UNKNOWN unless separately supported; outcome and repeated patterns are descriptive only.'},'limitations':['Selection is outcome-informed, post-hoc and not a randomized or confirmatory analysis.','Single analyst; full independent case review pending.','No inference that observed repetition caused failure or that training source caused a difference.','Remainder of 82-task cohort is not the denominator for selected-case summaries.'],'no_models_environment_training_or_scientific_reexecution':True}
save('PRIVATE_CASE_TABLE.json',{'schema':'SI_U1_PRIVATE_DESCRIPTIVE_CASES_V1','summary':base,'cases':private});save('DESCRIPTIVE_AGGREGATE.json',base)
print(json.dumps({'selected_union':len(selected),'pair_directions':dict(pair_directions),'arm_counts':{k:dict(v) for k,v in summary_counts.items()},'same_all_evidence_hashes':before==after},sort_keys=True))
