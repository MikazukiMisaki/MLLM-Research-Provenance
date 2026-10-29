import collections,datetime,hashlib,json,os,pathlib
P=pathlib.Path(__file__).resolve().parent;src=P/'PRIVATE_CASE_TABLE.json';raw=src.read_bytes();table=json.loads(raw)
def patterns(commands):
 found=[]
 for width in (2,3,4):
  for i in range(len(commands)-2*width+1):
   if commands[i:i+width]==commands[i+width:i+2*width]:found.append({'first_index':i,'block_width':width,'repeat_count_at_least':2});break
 return found
private=[];groups=collections.defaultdict(collections.Counter);diffs=collections.Counter();repeats=collections.Counter()
for c in table['cases']:
 is_two=c['family']=='pick_two_obj_and_place'
 for a,v in c['arms'].items():
  t=v['timeline'];commands=[z['command'] for z in t if z['command'] is not None];pats=patterns(commands);cat='success' if v['outcome']==1 else 'failure';g=groups[a+'_'+cat];g['episodes']+=1;g['steps_50']+=int(v['steps']==50);g['done_true_reward_zero']+=int(v['last_done'] and v['last_reward']==0);g['selected_parser_actions']+=v['parser_counts'].get('selected',0);g['unselected_parser_actions']+=sum(n for k,n in v['parser_counts'].items() if k!='selected');g['identical_2_to_4_step_block_repeated']+=int(bool(pats));g['one_or_more_token_cap']+=int(any(z['token_cap_reached'] for z in t));g['one_or_more_incomplete_output']+=int(any(not z['output_complete'] for z in t));g['same_observation_and_action_map_adjacent']+=int(v['consecutive_same_observation_and_action_map_count']>0)
  if is_two:
   h=groups['pick_two_'+a];h['episodes']+=1;h['steps_50']+=int(v['steps']==50);h['done_true_reward_zero']+=int(v['last_done'] and v['last_reward']==0);h['identical_2_to_4_step_block_repeated']+=int(bool(pats));h['selected_parser_actions']+=v['parser_counts'].get('selected',0)
  private.append({'case_id':c['case_id'],'arm':a,'pattern_anchor_indices':pats})
 for other in 'AB':
  if c['selection_reason']['C_vs_'+other+'_disagrees']:
   j=c['comparisons']['C_vs_'+other];diffs['C_vs_'+other+'_disagreement']+=1
   if j['first_command_difference_index'] is None:diffs['C_vs_'+other+'_no_command_difference_in_overlap']+=1
   if j['same_observation_and_map_at_first_command_difference'] is True:diffs['C_vs_'+other+'_same_observation_map_at_first_command_difference']+=1
base={'schema':'SI_U1_SELECTED_CASE_PATTERN_SUMMARY_V1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'private_case_table_sha256':hashlib.sha256(raw).hexdigest(),'groups':{k:dict(v) for k,v in groups.items()},'disagreement_observation_map_comparisons':dict(diffs),'definitions':{'identical_2_to_4_step_block_repeated':'At least one adjacent repetition of an exactly matching command-string block of length 2,3 or 4; may be purposeful and is not proof of a loop or cause.','same_observation_and_action_map_adjacent':'Adjacent identical observation text and available-action list, not full prompt or hidden state.','token_cap':'Model output flagged token_cap_reached, not itself invalid parse.','diagnostic_unit':'Selected outcome-conditioned cases only; no estimate of population frequency.'},'case_count':len(table['cases']),'unreviewed_single_analyst':True}
for name,obj in [('PATTERN_SUMMARY.json',base),('PRIVATE_PATTERN_ANCHORS.json',{'schema':'SI_U1_PRIVATE_PATTERN_ANCHORS_V1','items':private})]:
 with (P/name).open('x') as f:json.dump(obj,f,indent=2,sort_keys=True);f.write('\n');f.flush();os.fsync(f.fileno())
 os.chmod(P/name,0o600)
print(json.dumps(base,sort_keys=True))
