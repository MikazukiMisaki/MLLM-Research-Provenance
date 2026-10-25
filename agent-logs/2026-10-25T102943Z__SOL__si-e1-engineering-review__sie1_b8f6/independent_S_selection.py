from pathlib import Path
import json,hashlib,re,collections
OWN=Path(__file__).resolve().parent
assert OWN.name=='2026-10-25T102943Z__SOL__si-e1-engineering-review__sie1_b8f6'
BASE=Path('/home/lizening/research-notes')
DATA=Path('/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/sft-policy-bootstrap/sft_expert_dataset_balanced.jsonl')
KNOWN=BASE/'agent-logs/2026-10-25T065200Z__LUNA__si-p1-isolation-budget__caae4c/KNOWN_USE_IDENTITIES.json'
RES=BASE/'agent-logs/2026-10-25T084517Z__SOL__si-p3-controlled-experience-design__si3_7d91/ADOPTED_METADATA_RESERVATIONS.json'
F={'pick_and_place_simple':44,'pick_clean_then_place_in_recep':32,'pick_cool_then_place_in_recep':20,'pick_heat_then_place_in_recep':11,'pick_two_obj_and_place':13}
sha=lambda b:hashlib.sha256(b).hexdigest()
def hf(*v):return sha(('\n'.join(v)+'\n').encode())
def canonical(v):return json.dumps(v,ensure_ascii=True,sort_keys=True,separators=(',',':'))
def hfile(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
assert hfile(DATA)=='c547e8f0c5988b29288f2a097169c7859741b7d4f53f222af31f5e2889d516cf'
known=json.loads(KNOWN.read_text())['registered_identity_members']['expert_train'];selected={};quotas={}
for f,n in F.items():
 ids=[i for i in known if i.startswith(f+'-')];ordered=sorted(ids,key=lambda i:(hf('SI-P3-S-v1',f,i),i));assert len(ids)==179
 for i in ordered[:n]:selected[i]=f
 quotas[f]={'available':len(ids),'selected':n}
assert len(selected)==120
reserved=json.loads(RES.read_text());newids={x['identity'] for x in reserved['rows']};assert not set(selected)&newids
bad=collections.Counter();count=0;valid=collections.Counter();allcandidates=collections.defaultdict(list)
def public(row):
 his=row['recent_history'];trans=[]
 for j,z in enumerate(his):
  result=his[j+1]['observation'] if j+1<len(his) else row['observation']
  trans.append(f"Action: {z['action']}\nResult: {result}")
 ctx='\n\n'.join(trans) if trans else '(none)'
 actions='\n'.join(f'[{i}] {cmd}' for i,cmd in row['indexed_action_map'].items())
 return ('You are an ALFWorld household agent. Select exactly one next action.\n'
 'Return exactly one bare action ID in the form Axyz. Do not output a '
 'label, command, explanation, reasoning, or <think> tags.\n\n'
 f"Task goal:\n{row['goal']}\n\n"
 f"Current observation:\n{row['observation']}\n\n"
 f'Recent action/result transitions (last 4):\n{ctx}\n\n'
 f'Indexed admissible actions:\n{actions}\n\nYour response:')
with DATA.open() as f:
 for lineindex,line in enumerate(f,1):
  row=json.loads(line);count+=1;task=row['task_id']
  if task not in selected:continue
  reason=None
  if row['dataset_split']!='train' or row['source_split']!='train' or row['task_family']!=selected[task]:reason='split_family'
  elif row['terminal_task_success'] is not True:reason='not_original_success'
  elif not re.fullmatch('A[0-9]{3}',row['completion']) or row['completion']!=row['target_action_id']:reason='bad_target'
  elif row['indexed_action_map'].get(row['completion'])!=row['target_command']:reason='map_target'
  elif list(row['indexed_action_map'])!=[f'A{i:03d}' for i in range(len(row['indexed_action_map']))]:reason='map_order'
  elif sha(canonical(row['indexed_action_map']).encode())!=row['indexed_action_map_sha256']:reason='map_digest'
  elif sha(row['prompt'].encode())!=row['prompt_sha256']:reason='prompt_digest'
  elif not 0<=len(row['recent_history'])<=4 or public(row)!=row['public_prompt']:reason='public_projection'
  elif not isinstance(row['tokenizer_length'],int) or row['tokenizer_length']>2048:reason='stored_fit_not_actual_encoding'
  if reason:bad[reason]+=1;continue
  key=hf('SI-P3-S-row-v1',task,str(row['step_index']),row['prompt_sha256'],row['completion'])
  valid[task]+=1;allcandidates[task].append((key,row['step_index'],lineindex,row))
missing=[i for i in selected if not allcandidates[i]];assert not missing,missing
out=[]
for task,f in selected.items():
 key,step,line,row=min(allcandidates[task],key=lambda z:(z[0],z[1]))
 out.append({'task_id':task,'task_family':f,'task_rank_sha256':hf('SI-P3-S-v1',f,task),'selected_row_rank_sha256':key,'step_index':step,'dataset_line_1_based':line,'completion':row['completion'],'prompt_sha256':row['prompt_sha256'],'public_prompt_sha256':sha(row['public_prompt'].encode()),'map_sha256':row['indexed_action_map_sha256'],'stored_tokenizer_length_not_independently_encoded':row['tokenizer_length'],'source_game_sha256':row['source_game_sha256'],'source_traj_data_sha256':row['source_traj_data_sha256'],'trajectory_sha256':row['trajectory_sha256'],'eligible_rows_for_fixed_task':valid[task]})
result={'status':'INDEPENDENT_BACKGROUND_METADATA_SELECTION_ONLY_ACTUAL_TOKENIZER_CHECK_PENDING','task_rows':len(out),'family_quotas':quotas,'dataset_rows_read':count,'mechanical_rejection_counts_for_selected_tasks':dict(bad),'selected_task_replacement':False,'knownexperttrain_tasks':len(known),'intersection_with_all_new_reserved_nonlight1139':0,'fit_rule_limit':2048,'fit_current_evidence':'stored metadata only; Luna real-tokenizer audit must independently confirm; no training-ready claim','input_before_after_sha':{str(p):hfile(p) for p in [DATA,KNOWN,RES]},'rows':out,'scientific_model_environment_training':0,'tokenizer_calls_this_script':0}
(OWN/'independent_S_background_metadata.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['rows','input_before_after_sha']},indent=2))
