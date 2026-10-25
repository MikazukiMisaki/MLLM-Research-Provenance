"""Read fixed existing evidence, emit compact hashes/lineage; no training rows."""
import collections,json,re
from pathlib import Path

def audit(ns):
 OWN,FROZEN,RUNTIME,R19=(ns[k] for k in ('OWN','FROZEN','RUNTIME','R19'));readjson=ns['readjson'];rows=ns['streamrows'];vsha=ns['value_sha'];tsha=ns['text_sha'];register=ns['register']
 def ref(p,n=None,h=None,pointer=None):return {'path':str(p),'line':n,'raw_line_sha256':h,'pointer':pointer}
 def find(p,pid):
  for n,h,r in rows(p):
   if r.get('prefix_id')==pid:return n,h,r
  return None,None,None
 def won_entries(obj,pointer=''):
  out=[]
  if isinstance(obj,dict):
   for k,v in obj.items():
    if k in ('facts','extra.expert_plan'):continue
    q=pointer+'/'+k
    if k=='won':out.append({'pointer':q,'value':v[0] if isinstance(v,list) and len(v)==1 else v})
    elif isinstance(v,(dict,list)):out.extend(won_entries(v,q))
  elif isinstance(obj,list):
   for j,v in enumerate(obj):
    if isinstance(v,(dict,list)):out.extend(won_entries(v,pointer+'/'+str(j)))
  return out
 def terminal(step,reference):
  return {'source':reference,'done':step.get('done'),'reward':step.get('reward'),'truncated':step.get('truncated'),'won_entries':won_entries(step),'step_record_sha256':vsha(step)}
 def policy_meta(step):return step.get('metadata',{}).get('policy') or step.get('policy_metadata') or {}
 def prompt(goal,obs,recent,mapping):
  tr='\n\n'.join('Action: '+x['action']+'\nResult: '+x['resulting_observation'] for x in recent) if recent else '(none)'
  action='\n'.join('['+k+'] '+v for k,v in mapping.items())
  return ('You are an ALFWorld household agent. Select exactly one next action.\n'
    'Return exactly one bare action ID in the form Axyz. Do not output a label, command, explanation, reasoning, or <think> tags.\n\n'
    'Task goal:\n'+goal+'\n\nCurrent observation:\n'+obs+'\n\nRecent action/result transitions (last 4):\n'+tr+'\n\nIndexed admissible actions:\n'+action+'\n\nYour response:')
 for path in [ns['COORD']/'SOL_RESEARCH_TASK.md',Path('/home/lizening/research-notes/agent-logs/2026-10-25T054106Z__SOL__self-improvement-phase0__b1c48c/PHASE0_DECISION_AND_NEXT_STEPS.md'),Path('/home/lizening/research-notes/agent-logs/2026-10-25T054106Z__SOL__self-improvement-phase0__b1c48c/phase0_independent_review.json')]:register(path)
 for name in ['src/sft/policy.py','src/sft/protocol.py','src/models/action_parser.py','src/env/alfworld.py','src/sft/r3.py','src/sft/r9.py','src/recovery/persistent_prefix_selection.py','src/recovery/r13_1_prefix_selection.py','scripts/run_sft_recovery_feasibility.py','scripts/run_persistent_recovery_osr_control.py','scripts/run_r19_experiment.py']:
  register(FROZEN/name)
 raw=ns['rawcases']();src=ns['sourcecases']()
 replay_paths={'R4':RUNTIME/'validation/sft-recovery-replay-continue-r3-20260908T055308Z/replay_validation.jsonl','R16_OSR':RUNTIME/'validation/progress-aware-recovery-r16-osr-20260910T000000Z/replay_ledger.jsonl'}
 control_paths={'R4':RUNTIME/'validation/sft-recovery-replay-continue-r3-20260908T055308Z/continue_branches.jsonl','R10_OSR':RUNTIME/'validation/persistent-recovery-replay-continue-r9-20260909T033000Z/continue_branches.jsonl','R16_OSR':RUNTIME/'validation/progress-aware-recovery-r15-b-20260910T000000Z/continue_ledger.jsonl'}
 manifests={stage:readjson(Path(c['source_path']).parent/'run_manifest.json') for c,r in raw.values() if (stage:=c['stage'])!='R19_K1'}
 r19man=readjson(R19/'execution_manifest.json');r19runtime=readjson(R19/'runtime_manifest.json')
 c19,r19=next((c,r) for c,r in raw.values() if c['stage']=='R19_K1');arm19=r19['k_results']['1'];refs19=arm19['evidence_refs']
 need={r19['evidence_refs']['prefix_attempt_event_id']}
 for ids in refs19.values():need.update(ids)
 need.update(arm19['replay_evidence']['replay_transition_event_ids']);need.add(arm19['replay_evidence']['reset_event_id'])
 # Initial-prefix replay is distinct from K1 replay AFTER the first recovery action.
 events={}
 eventpath=R19/'execution_events.jsonl'
 for n,h,e in rows(eventpath):
  if e['event_id'] in need:events[e['event_id']]=(n,h,e)
 initial=events[r19['evidence_refs']['prefix_attempt_event_id']][2]['payload']['replay_evidence']
 need2=set(initial['replay_transition_event_ids'])|{initial['reset_event_id']}
 for n,h,e in rows(eventpath):
  if e['event_id'] in need2:events[e['event_id']]=(n,h,e)
 output={'schema':'SI_P1_ELEVEN_TARGET_LINEAGE_V1','fixed_case_count':11,'fixed_canonical_tasks':10,'audit_not_training_dataset':True,'scientific_permission':'NOT_GRANTED','data_feasibility':'NOT_READY','qualified_training_N':None,'projection_contract':'SI_P1_P0_PUBLIC_FIELDS_V1','projection_encoding':'ASCII JSON, sort_keys=True, separators comma/colon; ordered map serialized as id-command pair list; no task id/index/treatment/target in input hash','cases':[]}
 for cid,(c,r) in raw.items():
  stage=c['stage'];d=c['decision_index'];sp=ns['SOURCES'][stage];sn,sh,s=src[(stage,c['canonical_task'])];steps=s['steps'];step=steps[d];goal=s['task']['text'];obs=step['observation'];acts=step['valid_actions'];mapping={f'A{j:03d}':cmd for j,cmd in enumerate(acts)}
  recent=[{'action':steps[j]['action'],'resulting_observation':steps[j+1]['observation']} for j in range(max(0,d-4),d)]
  projection={'goal':goal,'observation':obs,'recent_action_result_transitions':recent,'ordered_action_map':list(mapping.items())}
  sourceprompt=policy_meta(step).get('prompt');staticprompt=prompt(goal,obs,recent,mapping)
  prefix_history=[[x['observation'],x['action']] for x in steps[:d]]
  source_map=step['metadata'].get('action_selection',policy_meta(step).get('action_selection',{})).get('id_to_command')
  fieldrefs={'goal':{'source':ref(sp,sn,sh,'/task/text'),'sha256_utf8':tsha(goal),'available_before_decision':d},'observation':{'source':ref(sp,sn,sh,f'/steps/{d}/observation'),'sha256_utf8':tsha(obs),'available_before_decision':d},'history':{'source_steps':[{'action_pointer':f'/steps/{j}/action','result_pointer':f'/steps/{j+1}/observation','result_available_by_state_index':j+1,'entry_sha256':vsha(recent[j-max(0,d-4)])} for j in range(max(0,d-4),d)],'source':ref(sp,sn,sh),'sha256':vsha(recent),'transition_count':len(recent),'uses_current_action_or_its_result':False},'ordered_action_map':{'source':ref(sp,sn,sh,f'/steps/{d}/valid_actions'),'action_count':len(acts),'ordered_actions_sha256':vsha(acts),'indexed_map_sha256':vsha(mapping),'all_source_policy_ids_match':source_map==mapping}}
  checks={'fixed_row_hash_matches':True,'source_task_matches':ns['canonical'](s['task']['task_id'])==c['canonical_task'],'source_nonterminal_before_action':not any(x.get('done') for x in steps[:d]),'remaining_horizon_50_minus_d':50-d==c['remaining_horizon'],'stored_actor_public_prompt_matches_static_P0':sourceprompt==staticprompt,'source_P0_map_equals_ordered_admissibles':source_map==mapping}
  gaps=[];event_refs=[]
  if stage=='R4':
   gen=r['raw_generations']['recovery']['stage_two']['generation'];parsed=r['raw_generations']['recovery']['stage_two']['parsed'];teacher_map=parsed['id_to_command'];aid=parsed['action_id'];command=parsed['action'];executed=r['recover']['recovery_action'];transition=r['recover']['recovery_transition'];suffix=r['recover']['continuation']['steps'];s1=r['recover']['stage_one'];s1gen=r['raw_generations']['recovery']['stage_one']['generation'];genptr='/raw_generations/recovery/stage_two/generation';parsedptr='/raw_generations/recovery/stage_two/parsed';transptr='/recover/recovery_transition';suffixptr='/recover/continuation/steps';execflag=r['recover']['recovery_action_executed']
   rn,rh,replay=find(replay_paths[stage],c['prefix_id']);repref=ref(replay_paths[stage],rn,rh);trs=replay['transitions']
   checks.update({'recorded_exact_replay':replay['replay_match'] and r['prefix_replay']['replay_match'],'replay_task_identity':replay['task_id']==c['canonical_task'],'replay_current_observation':replay['branch_observation']==obs,'replay_current_action_order':replay['branch_valid_actions']==acts,'replay_recent_H4':replay['replay_recent_context']==recent,'source_prefix_actions_replayed_exactly':len(trs)==d and all(t['action']==steps[j]['action'] and t['replayed_observation']==steps[j]['observation'] and t['resulting_observation']==steps[j+1]['observation'] and t['exact'] for j,t in enumerate(trs)),'R4_replay_hashes_bind_source_and_R3':r['prefix_replay']['action_map_hash_replay']==vsha(mapping) and r['prefix_replay']['observation_hash_replay']==tsha(obs) and r['prefix_replay']['recent_context_hash_replay']==vsha(recent)})
   replayinfo={'source':repref,'replay_record_sha256':vsha(replay),'transitions_count':len(trs),'first_and_last_transition_sha256':[vsha(trs[0]),vsha(trs[-1])],'R4_source_summary':ref(c['source_path'],c['source_line'],c['source_row_sha256'],'/prefix_replay'),'limitation':'Full R3 public replay plus R4 own exact-replay hash receipt; no new replay.'}
  elif stage in ('R10_OSR','R16_OSR'):
   gen=r['recovery_full']['stage_two']['generation'];parsed=r['recovery_full']['stage_two']['parsed'];teacher_map=parsed['id_to_command'];aid=parsed['action_id'];command=parsed['action'];executed=r['recovery_mapped_command'];transition=r['recovery_transition'];suffix=r['continuation_full']['steps'];s1=r['recovery_full']['stage_one']['parsed'];s1gen=r['recovery_full']['stage_one']['generation'];genptr='/recovery_full/stage_two/generation';parsedptr='/recovery_full/stage_two/parsed';transptr='/recovery_transition';suffixptr='/continuation_full/steps';execflag=r['recovery_action_executed']
   if stage=='R10_OSR':
    replay=r['replay_full'];repref=ref(c['source_path'],c['source_line'],c['source_row_sha256'],'/replay_full');trs=replay['transitions'];sig=replay['signature']
    checks.update({'recorded_exact_replay':replay['replay_match'],'replay_current_observation':replay['branch_observation']==obs,'replay_current_action_order':replay['branch_valid_actions']==acts,'replay_recent_H4':replay['replay_recent_context']==recent,'source_prefix_actions_replayed_exactly':len(trs)==d and all(t['action']==steps[j]['action'] and t['observation_before']==steps[j]['observation'] and t['resulting_observation']==steps[j+1]['observation'] and t['exact'] for j,t in enumerate(trs)),'replay_all_pre_action_maps_match':sig['valid_actions_through_prefix']==[x['valid_actions'] for x in steps[:d+1]]})
   else:
    rn,rh,replay=find(replay_paths[stage],c['prefix_id']);repref=ref(replay_paths[stage],rn,rh);trs=replay['transition_checks']
    checks.update({'recorded_exact_replay':replay['replay_match'],'replay_task_identity':replay['task_id']==c['canonical_task'],'replay_observation_digest':replay['current_observation_sha256']==tsha(obs),'replay_map_digest':replay['current_indexed_action_map_sha256']==vsha(mapping),'replay_recent_H4_digest':replay['recent_k4_context_sha256']==vsha(recent),'all_recorded_transition_checks_true':len(trs)==d and all(all(t[k] for k in ['action_admissible','action_map_equal','done_equal','observation_equal','result_observation_equal','reward_equal','truncated_equal']) for t in trs),'branch_replay_summary_binds_ledger':r['replay']['complete_public_prefix_sha256']==replay['complete_public_prefix_sha256']})
   replayinfo={'source':repref,'replay_record_sha256':vsha(replay),'transitions_count':len(trs),'first_and_last_transition_sha256':[vsha(trs[0]),vsha(trs[-1])],'note':'Existing full public replay trace' if stage=='R10_OSR' else 'Existing per-transition equality receipts + complete prefix hash; original public source remains bound.'}
  else:
   ids=refs19['recovery_generation_event_ids'];ge=[events[x] for x in ids if events[x][2]['identity']['component']=='stage2']
   if len(ge)!=1:raise RuntimeError('K1 has unexpected stage2 refs')
   gn,gh,gev=ge[0];ev=gev['payload']['evidence'];gen=ev['generation'];parsed=ev;teacher_map=ev['id_to_command'];aid=ev['action_id'];command=ev['command'];tn,th,te=events[refs19['recovery_transition_event_ids'][0]];action=te['payload']['action'];transition=action['transition'];executed=action['command'];execflag=True
   g1n,g1h,g1=next(events[x] for x in ids if events[x][2]['identity']['component']=='stage1');s1=g1['payload']['evidence'];s1gen=s1['generation'];genptr='/payload/evidence/generation';parsedptr='/payload/evidence';transptr='/payload/action/transition';suffixptr='K1 suffix_transition_event_ids';suffix=[events[x][2]['payload']['transition'] for x in refs19['suffix_transition_event_ids']]
   trs=[events[x][2]['payload'] for x in initial['replay_transition_event_ids']]
   checks.update({'recorded_exact_replay':initial['replay_match'],'initial_replay_count_before_recovery':len(trs)==d,'initial_replay_source_action_observation_map_match':all(t['command']==steps[j]['action'] and t['before_state']['observation']==steps[j]['observation'] and t['before_state']['valid_actions']==steps[j]['valid_actions'] and t['transition']['observation']==steps[j+1]['observation'] for j,t in enumerate(trs)),'recovery_event_before_history_exact':action['history_before']==prefix_history,'recovery_event_before_observation_exact':action['observation_before']==obs,'recovery_event_before_order_exact':action['valid_actions_before']==acts,'recovery_event_index_is_one':action['recovery_action_index']==1,'K1_stage_two_attempt_one':gev['identity']['stage_two_attempt']==1,'recovery_event_map_exact':action['action_map']==mapping,'event_implementation_is_executed2da':all(events[x][2]['implementation_sha']=='2da980f631badc25086d12db60d128ff507d3ae6' for x in ids+refs19['recovery_transition_event_ids'])})
   replayinfo={'source':ref(eventpath,*events[r19['evidence_refs']['prefix_attempt_event_id']][:2],'/payload/replay_evidence'),'replay_record_sha256':vsha(initial),'transitions_count':len(trs),'first_and_last_transition_sha256':[vsha(trs[0]),vsha(trs[-1])],'recovery_source_event_id':te['event_id'],'K1_post_recovery_replay_not_used_as_original_prefix':True,'no_K2_target_read':True}
   for en,eh,e in [ge[0],events[refs19['recovery_transition_event_ids'][0]],events[refs19['suffix_transition_event_ids'][-1]]]:event_refs.append({**ref(eventpath,en,eh),'event_id':e['event_id'],'kind':e['kind']})
   # For these event-schema fields, parser status is named status, command is explicit.
  suffixn=len(suffix)
  if stage=='R19_K1':
   seq=[]
   for eid in refs19['suffix_transition_event_ids']:
    pl=events[eid][2]['payload'];before=pl['before_state'];tr=pl['transition'];seq.append({'observation':before['observation'],'valid_actions':before['valid_actions'],'action':pl['command'],'result':tr['observation'],'reward':tr['reward'],'done':tr['done']})
  else:
   seq=[{'observation':st['observation'],'valid_actions':st['valid_actions'],'action':st['action'],'result':st.get('resulting_observation'), 'reward':st['reward'],'done':st['done']} for st in suffix]
  suffix_sequence_hash=vsha({'goal':goal,'steps':seq}) if seq else None
  if suffix:
   terminalstep=suffix[-1];terminalref=ref(c['source_path'],c['source_line'],c['source_row_sha256'],suffixptr+f'/{suffixn-1}') if stage!='R19_K1' else ref(eventpath,*events[refs19['suffix_transition_event_ids'][-1]][:2],'/payload/transition')
  else:terminalstep=transition;terminalref=ref(c['source_path'],c['source_line'],c['source_row_sha256'],transptr)
  term=terminal(terminalstep,terminalref)
  if stage!='R19_K1':
   cn,ch,cr=find(control_paths[stage],c['prefix_id']);control=cr.get('continue') or cr.get('continue_full') or cr;controlsteps=control.get('steps',[])
   ctlstep=controlsteps[-1] if controlsteps else {};ctlterm=terminal(ctlstep,ref(control_paths[stage],cn,ch,('/continue/steps/' if stage=='R4' else '/continue_full/steps/' if stage=='R10_OSR' else '/steps/')+str(len(controlsteps)-1)));control_success=control.get('success',cr.get('continue_success',cr.get('r_continue')))
  else:
   ctlstep=steps[-1];ctlterm=terminal(ctlstep,ref(sp,sn,sh,f'/steps/{len(steps)-1}'));control_success=r['continue_success']
  checks.update({'CONTINUE_recorded_zero':int(control_success)==0,'recover_recorded_one':int(r.get('recover',{}).get('success',r.get('r_osr',r.get('k_results',{}).get('1',{}).get('success',0))))==1,'stage_one_valid':s1.get('status')=='valid','raw_output_is_recorded_ID':gen.get('raw_output','').strip()==aid and re.fullmatch(r'A\d{3}',aid) is not None,'teacher_selected_status':parsed.get('status')=='selected','teacher_map_equals_P0_by_every_ID':teacher_map==mapping,'teacher_valid_actions_order_if_present':parsed.get('valid_actions',acts)==acts,'recorded_ID_resolves_same_command':teacher_map.get(aid)==command and mapping.get(aid)==command,'executed_flag_command_transition':bool(execflag and executed==command and transition),'no_truncated_generation':gen.get('output_complete') is True and gen.get('token_cap_reached') is False,'recovery_terminal_done_positive_reward_recorded':term['done'] is True and term['reward']>0,'continuation_horizon_with_first_recovery':1+suffixn<=c['remaining_horizon']})
  explicitwon=[x['value'] for x in term['won_entries']]
  terminal_axis='EXPLICIT_DONE_WON_TRUE_REWARD_POSITIVE' if explicitwon and all(v is True for v in explicitwon) and term['done'] is True and term['reward']>0 else 'DONE_POSITIVE_REWARD_WON_NOT_RECORDED'
  if stage=='R19_K1' and not ctlterm['won_entries']:gaps.append('CONTINUE_TERMINAL_WON_MISSING: done=true and reward=0 plus original CONTINUE=0 are recorded; do not fabricate won=false.')
  if terminal_axis!='EXPLICIT_DONE_WON_TRUE_REWARD_POSITIVE':gaps.append('TERMINAL_WON_MISSING: raw terminal done/reward recorded; wrapper forwards underlying reward, does not substitute won. No success re-label or historical-result rejection.')
  bad=[k for k,v in checks.items() if not v]
  if teacher_map!=mapping:disposition='REINDEX_REQUIRED';gaps.append('P0/teacher maps differ; no reindex or replacement target performed')
  elif any(not checks[k] for k in ['stage_one_valid','raw_output_is_recorded_ID','teacher_selected_status','recorded_ID_resolves_same_command','executed_flag_command_transition','no_truncated_generation']):disposition='EXCLUDE_INVALID'
  elif bad or gaps:disposition='HOLD_EVIDENCE'
  else:disposition='INPUT_TARGET_LINEAGE_SUPPORTED'
  model=manifests.get(stage,r19man);weights=r19man.get('pinned_model_revision','UNKNOWN') if stage=='R19_K1' else 'UNKNOWN';model_axis='MODEL_IDENTITY_PINNED' if stage=='R19_K1' else 'MODEL_IDENTITY_PARTIAL'
  modelinfo={'axis':model_axis,'teacher_role':'adapter-off recovery base, distinct from adapter-on SFT suffix','base_model':'Qwen/Qwen3-8B','resolved_weights_revision':weights,'resolved_tokenizer_revision':r19runtime['model_files']['snapshot_revision'] if stage=='R19_K1' else 'UNKNOWN','tokenizer_identity_basis':{'snapshot_revision':r19runtime['model_files']['snapshot_revision'],'recorded_snapshot_tokenizer_json_sha256':r19runtime['model_files']['snapshot_file_sha256']['tokenizer.json'],'recorded_actor_chat_template_sha256':r19runtime['model_adapter_isolation']['task_actor']['chat_template_sha256'],'recorded_recovery_chat_template_sha256':r19runtime['model_adapter_isolation']['recovery_controller']['chat_template_sha256']} if stage=='R19_K1' else 'No historical resolved revision in the read run manifests','actor_adapter_directory_sha256':'6e403d85b150a74dfcc176f1f180ce4baf6fdacd922d2f96b3ceef0a21100f11','implementation_sha':model.get('git_revision_before_inference',model.get('implementation_sha')),'recovery_adapter_active':False if stage!='R4' else 'NOT_EXPLICIT_IN_MANIFEST; static distinct recovery construction','suffix_adapter_active':True,'source_manifest':str(Path(c['source_path']).parent/('execution_manifest.json' if stage=='R19_K1' else 'run_manifest.json')),'source_actor_recorded_model_version':s.get('model_version'),'static_contract_binding':'historical_contracts.json: executed stage method AST matches frozen85, no historical model revision inference','runtime_loaded_commit_and_adapter_record':r19runtime['model_adapter_isolation'] if stage=='R19_K1' else 'Historical run manifest isolation fields only; no loaded commit/tokenizer revision receipt','isolation_receipt':model.get('model_isolation',model.get('model_load',model.get('model_adapter_isolation'))),'limitation':'Historical main-resolution weights/tokenizer not retrospectively filled from R19' if stage!='R19_K1' else 'Pinned in original runtime and execution manifests; no model files loaded or new runtime validation'}
  publicsummary={'contract':'STATIC_PUBLIC_FIELDS_AND_P0_PUBLIC_TEXT_ONLY','projection_sha256':vsha(projection),'source_actor_public_prompt_sha256':tsha(sourceprompt) if sourceprompt else None,'static_public_text_sha256':tsha(staticprompt),'existing_chat_render_sha256':policy_meta(step).get('rendered_prompt_sha256',policy_meta(step).get('generation',{}).get('rendered_prompt_sha256')),'chat_template_or_tokenizer_revalidation':'NOT_PERFORMED','full_prompt_or_JSONL_exported':False,'fields':fieldrefs,'excluded_fields':['teacher diagnosis/subgoal/card','current source action/model output/result/environment_metadata','terminal/reward/won','stratum/K/oracle/future actions','expert_plan/facts'],'source_step_current_metadata_environment_is_post_action_not_input':True}
  suffixinfo={'producer':'adapter-on frozen SFT-P0','actions':suffixn,'target_adopted_here':False,'target_identity_not_adapter_off':True,'suffix_action_ids_sha256':vsha([x.get('action_id') for x in suffix]) if stage!='R19_K1' else vsha(refs19['suffix_generation_event_ids']),'generation_or_step_refs':refs19['suffix_generation_event_ids'] if stage=='R19_K1' else ref(c['source_path'],c['source_line'],c['source_row_sha256'],suffixptr),'semantic_public_action_sequence_sha256':suffix_sequence_hash,'physical_alias_evidence':'No derived alias among fixed cases; legacy lacks event IDs, so semantic equality alone does not assert physical reuse','source_endpoints':{'first_sha256':vsha(suffix[0]) if suffix else None,'last_sha256':vsha(suffix[-1]) if suffix else None},'original_prefix_0to1_not_per_suffix_step_causal_label':True}
  output['cases'].append({'case_id':cid,'prefix_id':c['prefix_id'],'stage':stage,'canonical_task':c['canonical_task'],'family':c['family'],'decision_index':d,'remaining_horizon':c['remaining_horizon'],'source_episode':{'reference':ref(sp,sn,sh),'trajectory_id':s['trajectory_id'],'public_prefix_action_count':d,'full_public_prefix_field_sha256':vsha({'goal':goal,'observations':[x['observation'] for x in steps[:d+1]],'actions':[x['action'] for x in steps[:d]],'valid_actions':[x['valid_actions'] for x in steps[:d+1]]})},'branch_record':ref(c['source_path'],c['source_line'],c['source_row_sha256']),'public_projection':publicsummary,'existing_replay':replayinfo,'first_recovery_target':{'producer':'adapter-off recovery base','generation_source':ref(c['source_path'] if stage!='R19_K1' else eventpath,c['source_line'] if stage!='R19_K1' else gn,c['source_row_sha256'] if stage!='R19_K1' else gh,genptr),'parsed_source_pointer':parsedptr,'failure_reason':parsed.get('failure_reason'),'teacher_valid_actions_list_recorded':isinstance(parsed.get('valid_actions'),list),'teacher_ordered_ID_command_pairs_sha256':vsha(sorted(teacher_map.items(),key=lambda kv:int(kv[0][1:]))),'transition_source':ref(c['source_path'] if stage!='R19_K1' else eventpath,c['source_line'] if stage!='R19_K1' else tn,c['source_row_sha256'] if stage!='R19_K1' else th,transptr),'raw_output':gen.get('raw_output'),'raw_output_sha256':tsha(gen.get('raw_output','')),'recorded_parser_status':parsed.get('status'),'action_id':aid,'mapped_command':command,'teacher_map_sha256':vsha(teacher_map),'P0_map_sha256':vsha(mapping),'all_entries_ID_command_equal':teacher_map==mapping,'executed_command':executed,'transition_source_pointer':transptr,'transition_sha256':vsha(transition),'done_after_first':transition.get('done'),'reward_after_first':transition.get('reward'),'source_end_state_observation_sha256':tsha(transition['observation'])},'checks':checks,'failed_or_unresolved_checks':bad,'terminal_corroboration':{'axis':terminal_axis,'recovery_branch_terminal':term,'CONTINUE_terminal':ctlterm,'historical_success_label_retained':True,'not_inferred_from_subgoal_or_shaping_reward':True},'model_identity':modelinfo,'suffix_separate':suffixinfo,'recorded_tokens':{'first_recovery_stage1':{k:s1gen.get(k) for k in ['input_tokens','generated_tokens','max_new_tokens']},'first_recovery_stage2':{k:gen.get(k) for k in ['input_tokens','generated_tokens','max_new_tokens']},'source_actor_same_public_P0':step.get('token_statistics'),'prospective_projected_training_tokens':None,'note':'Recorded inference counts only; no tokenizer. Teacher prompt length is not P0 projected training length.'},'event_refs':event_refs,'disposition':disposition,'evidence_gaps':gaps,'learning_gain':'NOT_PROVEN','training_row_approved':False})
 groups=collections.defaultdict(list)
 for x in output['cases']:groups[x['public_projection']['projection_sha256']].append(x)
 output['same_public_input_groups']=[{'public_projection_sha256':h,'case_ids':[x['case_id'] for x in group],'target_commands':sorted({x['first_recovery_target']['mapped_command'] for x in group}),'different_target_commands':len({x['first_recovery_target']['mapped_command'] for x in group})>1,'status':'AMBIGUITY_OR_MULTISOLUTION_CLUE_NOT_AUTO_ERROR'} for h,group in groups.items() if len(group)>1]
 tasks=collections.defaultdict(list)
 for x in output['cases']:tasks[x['canonical_task']].append(x['case_id'])
 output['same_task_multiple_prefix_groups']={t:ids for t,ids in tasks.items() if len(ids)>1}
 suffixgroups=collections.defaultdict(list)
 for x in output['cases']:
  h=x['suffix_separate']['semantic_public_action_sequence_sha256']
  if h:suffixgroups[h].append(x['case_id'])
 output['same_semantic_suffix_groups']=[{'suffix_sequence_sha256':h,'case_ids':ids,'meaning':'Repeated public behavior, not proof of physically reused generation or independent training examples'} for h,ids in suffixgroups.items() if len(ids)>1]
 output['summary']={'rows':len(output['cases']),'canonical_tasks':len(tasks),'families_by_row':dict(collections.Counter(x['family'] for x in output['cases'])),'dispositions':dict(collections.Counter(x['disposition'] for x in output['cases'])),'mechanical_input_target_checks_all_true':sum(all(x['checks'].values()) for x in output['cases']),'model_identity_axes':dict(collections.Counter(x['model_identity']['axis'] for x in output['cases'])),'terminal_axes':dict(collections.Counter(x['terminal_corroboration']['axis'] for x in output['cases'])),'same_public_input_multitarget_groups':sum(g['different_target_commands'] for g in output['same_public_input_groups']),'qualified_training_N':'NOT_ESTABLISHED; no training row approval','B_pool_ready':False}
 ns['savebindings']();output['input_bindings']=list(ns['BINDINGS'].values())
 (OWN/'eleven_target_audit.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(output['summary'],ensure_ascii=False,indent=2))
 for x in output['cases']:print(x['case_id'],x['disposition'],x['first_recovery_target']['action_id'],x['first_recovery_target']['mapped_command'],'bad',x['failed_or_unresolved_checks'],'gaps',x['evidence_gaps'])
