"""SI-P2: stdlib read audit only, all 171 historical rows, no training export."""
from audit_io import *
from collections import Counter,defaultdict
import re


def ref(p,n=None,h=None,pointer=None):
 return {'path':str(p),'line':n,'raw_line_sha256':h,'pointer':pointer}
def indexed(p):return {r['prefix_id']:(n,h,r) for n,h,r in rows(p)}
def policy(s):return s.get('metadata',{}).get('policy') or s.get('policy_metadata') or {}
def won_entries(v):
 out=[]
 if isinstance(v,dict):
  for k,x in v.items():
   if k in ('facts','extra.expert_plan'):continue
   if k=='won':out.append(x[0] if isinstance(x,list) and len(x)==1 else x)
   elif isinstance(x,(dict,list)):out.extend(won_entries(x))
 elif isinstance(v,list):
  for x in v:
   if isinstance(x,(dict,list)):out.extend(won_entries(x))
 return out
def terminal_info(s,r):
 w=won_entries(s)
 return {'source':r,'record_sha256':vs(s),'done':s.get('done'),'reward':s.get('reward'),'truncated':s.get('truncated'),'raw_won':w,'raw_won_status':'RAW_WON_RECORDED' if w else 'RAW_WON_NOT_RECORDED'}
def p0_text(goal,obs,recent,mapping):
 history='\n\n'.join('Action: '+x['action']+'\nResult: '+x['resulting_observation'] for x in recent) if recent else '(none)'
 actions='\n'.join('['+k+'] '+v for k,v in mapping.items())
 return ('You are an ALFWorld household agent. Select exactly one next action.\n'
 'Return exactly one bare action ID in the form Axyz. Do not output a label, command, explanation, reasoning, or <think> tags.\n\n'
 'Task goal:\n'+goal+'\n\nCurrent observation:\n'+obs+'\n\nRecent action/result transitions (last 4):\n'+history+'\n\nIndexed admissible actions:\n'+actions+'\n\nYour response:')
def success_step(s):return bool(s.get('done') and float(s.get('reward',0))>0)
def executed_step(s):
 if 'action_executed' in s:return bool(s['action_executed'])
 return s.get('action') is not None

def stop_proof(steps,label,reason,cap,initial=None):
 seq=([initial] if initial else [])+steps
 expected=int(any(success_step(s) for s in seq))
 used=sum(executed_step(s) for s in steps)+(1 if initial else 0)
 last=seq[-1] if seq else {}
 ended=bool(last.get('done') or last.get('truncated'))
 selection_failure=bool(steps and not executed_step(steps[-1]) and (steps[-1].get('selection_status') not in (None,'selected') or steps[-1].get('failure_reason') or steps[-1].get('failure_category')))
 known_stop=(ended and reason in ('environment_terminal','environment_truncated','recovery_terminal')) or (reason=='remaining_horizon' and used==cap) or (reason=='selection_failure' and selection_failure)
 return {'label_matches_original_terminal_predicate':label in (0,1,False,True) and int(label)==expected,
 'recorded_stop_supported':bool(known_stop),'executed_actions_within_horizon':0<=used<=cap,
 'recorded_label':int(label) if label in (0,1,False,True) else None,'terminal_predicate_from_recorded_steps':expected,
 'reason':reason,'executed_environment_actions':used,'allowed_horizon':cap,'last_done':last.get('done'),'last_reward':last.get('reward'),'last_truncated':last.get('truncated'),'last_step_sha256':vs(last)}

def anchor(c):
 # Literal LF bytes. This function consumes no outcome or target information.
 return ts('SI-P2-anchor-v1'+chr(10)+c['canonical_task']+chr(10)+c['stage']+chr(10)+c['prefix_id']+chr(10))

m=authority()
keys=[{k:c[k] for k in ('case_id','canonical_task','stage','prefix_id')}|{'anchor_key':anchor(c)} for c in m['rows']]
output('anchor_keys_pre_outcome.json',{'rule':'SI-P2-anchor-v1 with real LF separators','phase':'Computed from fixed identity-only manifest before opening parent evidence','keys':keys})
pr=parent_rows(m)
source={};wanted=defaultdict(set)
for c,r in pr:wanted[c['stage']].add(c['canonical_task'])
for st,path in SOURCES.items():
 for n,h,s in rows(path):
  t=canon(s['task']['task_id'])
  if t in wanted[st]:
   assert (st,t) not in source,('ambiguous source',st,t)
   source[(st,t)]=(n,h,s)
controls={st:indexed(p) for st,p in CONTROLS.items()}
replays={st:indexed(p) for st,p in REPLAYS.items()}
legacy_man={st:readjson(next(Path(c['source_path']).parent/'run_manifest.json' for c,r in pr if c['stage']==st)) for st in ('R4','R10_OSR','R16_OSR')}
rman=readjson(R19/'execution_manifest.json');runtime=readjson(R19/'runtime_manifest.json')
isolation=runtime['model_adapter_isolation'];model_files=runtime['model_files'];pin=rman['pinned_model_revision']
pin_checks={'weights_revision_equals_snapshot':pin==model_files['snapshot_revision'],
 'loaded_actor_commit_bound':isolation['task_actor']['loaded_commit_hash']==pin,
 'loaded_recovery_commit_bound':isolation['recovery_controller']['loaded_commit_hash']==pin,
 'tokenizer_files_hashed':bool(model_files['snapshot_file_sha256'].get('tokenizer.json')),
 'actor_tokenizer_template_bound':bool(isolation['task_actor'].get('chat_template_sha256')),
 'recovery_tokenizer_template_bound':bool(isolation['recovery_controller'].get('chat_template_sha256')),
 'adapter_directory_bound':rman['adapter_sha256']==model_files['adapter_directory_sha256'],
 'recovery_adapter_off':isolation['recovery_adapter_active'] is False and isolation['recovery_controller']['active_adapters']==[],
 'actor_adapter_on':isolation['sft_adapter_active'] is True and bool(isolation['task_actor']['active_adapters']),
 'separate_model_objects':isolation['distinct_model_objects'] is True and isolation['kv_cache_shared'] is False}
model_info={}
for st in SOURCES:
 man=rman if st=='R19_K1' else legacy_man[st]
 model_info[st]={'axis':'MODEL_IDENTITY_PINNED' if st=='R19_K1' and all(pin_checks.values()) else 'MODEL_IDENTITY_PARTIAL',
 'base_model':'Qwen/Qwen3-8B','weights_revision':pin if st=='R19_K1' else 'UNKNOWN',
 'tokenizer_revision':model_files['snapshot_revision'] if st=='R19_K1' else 'UNKNOWN',
 'loaded_adapter_roles_pinned':all(pin_checks.values()) if st=='R19_K1' else False,
 'implementation_sha':man.get('implementation_sha',man.get('git_revision_before_inference')),
 'teacher':'adapter-off base first recovery target','suffix':'adapter-on SFT-P0, evidence only',
 'source_manifest':str(R19/'execution_manifest.json' if st=='R19_K1' else next(Path(c['source_path']).parent/'run_manifest.json' for c,r in pr if c['stage']==st)),
 'identity_checks':pin_checks if st=='R19_K1' else {'historical_exact_weights_tokenizer_and_loaded_roles_receipt':'NOT_RECORDED'},
 'limitation':'Original runtime receipts only; no model/cache/tokenizer loading or retrospective current-cache fill.'}
output('model_identity_bindings.json',model_info)
for rel in ['src/sft/protocol.py','src/models/action_parser.py','src/env/alfworld.py','src/trajectory/trajectory.py','src/sft/r3.py','src/sft/r9.py','src/recovery/r19_duration.py','src/recovery/two_stage.py','src/recovery/persistent_prefix_selection.py','scripts/run_sft_recovery_feasibility.py','scripts/run_persistent_recovery_osr_control.py','scripts/run_r19_experiment.py']:
 register(FROZEN/rel)
prior=readjson(P1/'eleven_target_audit.json');assert sha(P1/'eleven_target_audit.json')=='f8fe8141d2c431274082856105a2b8aa81c76b774fe624fe50c5d33bf77ba901'
register(P1/'historical_contracts.json');register(P1/'SUCCESS_PREDICATE_AND_AXES_ADDENDUM.md')
# Event reads follow only initial-prefix and K1 evidence references; other K arms are not audited.
need=set()
for c,r in pr:
 if c['stage']!='R19_K1':continue
 a=r['k_results']['1'];need.add(r['evidence_refs']['prefix_attempt_event_id']);need.add(a['arm_event_id'])
 for ids in a['evidence_refs'].values():need.update(ids)
eventpath=R19/'execution_events.jsonl'
events={e['event_id']:(n,h,e) for n,h,e in rows(eventpath) if e['event_id'] in need}
need_more=set()
for c,r in pr:
 if c['stage']!='R19_K1':continue
 pe=events[r['evidence_refs']['prefix_attempt_event_id']][2]['payload']
 initial=pe['replay_evidence'];need_more.update(initial['replay_transition_event_ids']);need_more.add(initial['reset_event_id']);need_more.add(pe['source_episode_event_id'])
for n,h,e in rows(eventpath):
 if e['event_id'] in need_more:events[e['event_id']]=(n,h,e)

def evref(eid,pointer=None):
 n,h,e=events[eid];return ref(eventpath,n,h,pointer)|{'event_id':eid,'kind':e['kind']}

def one(c,r):
 cid=c['case_id'];st=c['stage'];d=c['decision_index'];horizon=c['remaining_horizon'];br=ref(c['source_path'],c['source_line'],c['source_row_sha256'])
 result={k:c[k] for k in ('case_id','prefix_id','stage','canonical_task','family','decision_index','remaining_horizon')}
 result.update({'anchor_key':anchor(c),'branch_record':br,'model_identity_axis':model_info[st]['axis'],'learning_gain':'NOT_PROVEN','training_row_approved':False,'checks':{},'Q_hist':'HOLD','Q_hist_reasons':[]})
 checks=result['checks'];invalid=[]
 try:
  sn,sh,s=source[(st,c['canonical_task'])];steps=s['steps'];step=steps[d];sp=SOURCES[st]
  goal=s['task']['text'];obs=step['observation'];acts=step['valid_actions'];mapping={f'A{j:03d}':a for j,a in enumerate(acts)}
  recent=[{'action':steps[j]['action'],'resulting_observation':steps[j+1]['observation']} for j in range(max(0,d-4),d)]
  history=[[x['observation'],x['action']] for x in steps[:d]]
  projection={'goal':goal,'observation':obs,'recent_action_result_transitions':recent,'ordered_action_map':list(mapping.items())}
  smap=step.get('metadata',{}).get('action_selection',policy(step).get('action_selection',{})).get('id_to_command')
  public_text=p0_text(goal,obs,recent,mapping)
  checks.update({'original_row_hash_bound':True,'source_task_identity':canon(s['task']['task_id'])==c['canonical_task'],
   'branch_task_identity':canon(r.get('task_id',r.get('canonical_trial_id')))==c['canonical_task'],
   'decision_index_matches':int(r.get('selected_decision_index',r.get('decision_index',d)))==d,
   'source_prefix_nonterminal':not any(x.get('done') or x.get('truncated') for x in steps[:d]),
   'horizon_50_minus_d':50-d==horizon,'ordered_complete_source_map':smap==mapping,
   'stored_actor_public_text_matches_static_P0':policy(step).get('prompt')==public_text})
  result['source_public']={'reference':ref(sp,sn,sh),'trajectory_id':s.get('trajectory_id'),
   'field_pointers':{'goal':'/task/text','observation':f'/steps/{d}/observation','history_actions':[f'/steps/{j}/action' for j in range(max(0,d-4),d)],'history_results':[f'/steps/{j+1}/observation' for j in range(max(0,d-4),d)],'ordered_map':f'/steps/{d}/valid_actions'},
   'projection_sha256':vs(projection),'public_text_sha256':ts(public_text),'goal_sha256':ts(goal),'observation_sha256':ts(obs),'recent_H4_sha256':vs(recent),'ordered_map_sha256':vs(mapping),'map_size':len(mapping),
   'full_public_prefix_sha256':vs({'goal':goal,'observations':[x['observation'] for x in steps[:d+1]],'actions':[x['action'] for x in steps[:d]],'valid_actions':[x['valid_actions'] for x in steps[:d+1]]}),
   'projection_contract':'P1 ASCII JSON ensure_ascii=True sort_keys=True separators comma-colon; ordered ID-command pairs',
   'projection_and_stored_public_text_only_not_tokenizer_validation':True,'full_training_prompt_or_JSONL_exported':False}
  if st=='R4':
   g2=r['raw_generations']['recovery']['stage_two'];gen=g2['generation'];parsed=g2['parsed'];s1=r['recover']['stage_one'];g1=r['raw_generations']['recovery']['stage_one']['generation'];rec=r['recover'];suffix=rec['continuation']['steps'];transition=rec['recovery_transition'];exe=rec['recovery_action_executed'];command=parsed.get('action');executed=rec.get('recovery_action');recover_label=rec['success'];rec_reason=rec['termination_reason'];genref=br|{'pointer':'/raw_generations/recovery/stage_two/generation'};trref=br|{'pointer':'/recover/recovery_transition'}
   rn,rh,replay=replays[st][c['prefix_id']];trs=replay['transitions']
   checks.update({'existing_replay_exact':replay['replay_match'] is True and r['prefix_replay']['replay_match'] is True,
    'replay_task':canon(replay['task_id'])==c['canonical_task'], 'replay_observation':replay['branch_observation']==obs,
    'replay_ordered_actions':replay['branch_valid_actions']==acts,'replay_H4':replay['replay_recent_context']==recent,
    'full_prefix_replay_source_match':len(trs)==d and all(t['action']==steps[j]['action'] and t['replayed_observation']==steps[j]['observation'] and t['resulting_observation']==steps[j+1]['observation'] and t['exact'] is True for j,t in enumerate(trs)),
    'own_R4_replay_hash_receipt':r['prefix_replay']['action_map_hash_replay']==vs(mapping) and r['prefix_replay']['observation_hash_replay']==ts(obs) and r['prefix_replay']['recent_context_hash_replay']==vs(recent)})
   repref=ref(REPLAYS[st],rn,rh)
   suffix_refs=br|{'pointer':'/recover/continuation/steps'};physical_id=None
  elif st in ('R10_OSR','R16_OSR'):
   g2=r['recovery_full']['stage_two'];gen=g2['generation'];parsed=g2['parsed'];s1=r['recovery_full']['stage_one']['parsed'];g1=r['recovery_full']['stage_one']['generation'];suffix=r['continuation_full']['steps'];transition=r['recovery_transition'];exe=r['recovery_action_executed'];command=parsed.get('action');executed=r.get('recovery_mapped_command');recover_label=r['r_osr'];rec_reason=r['termination_reason'];genref=br|{'pointer':'/recovery_full/stage_two/generation'};trref=br|{'pointer':'/recovery_transition'};physical_id=None
   if st=='R10_OSR':
    replay=r['replay_full'];trs=replay['transitions'];repref=br|{'pointer':'/replay_full'}
    checks.update({'existing_replay_exact':replay['replay_match'] is True,'replay_observation':replay['branch_observation']==obs,'replay_ordered_actions':replay['branch_valid_actions']==acts,'replay_H4':replay['replay_recent_context']==recent,
     'full_prefix_replay_source_match':len(trs)==d and all(t['action']==steps[j]['action'] and t['observation_before']==steps[j]['observation'] and t['resulting_observation']==steps[j+1]['observation'] and t['exact'] is True for j,t in enumerate(trs)),
     'replay_all_source_maps':replay['signature']['valid_actions_through_prefix']==[x['valid_actions'] for x in steps[:d+1]]})
   else:
    rn,rh,replay=replays[st][c['prefix_id']];repref=ref(REPLAYS[st],rn,rh);trs=replay['transition_checks']
    checks.update({'existing_replay_exact':replay['replay_match'] is True,'replay_task':canon(replay['task_id'])==c['canonical_task'],
     'replay_observation':replay['current_observation_sha256']==ts(obs),'replay_ordered_actions':replay['current_indexed_action_map_sha256']==vs(mapping),'replay_H4':replay['recent_k4_context_sha256']==vs(recent),
     'full_prefix_original_equality_receipts':len(trs)==d and all(all(t[k] is True for k in ['action_admissible','action_map_equal','done_equal','observation_equal','result_observation_equal','reward_equal','truncated_equal']) for t in trs),
     'branch_replay_hash_bound':r['replay']['complete_public_prefix_sha256']==replay['complete_public_prefix_sha256']})
   suffix_refs=br|{'pointer':'/continuation_full/steps'}
  else:
   a=r['k_results']['1'];refs=a['evidence_refs'];peid=r['evidence_refs']['prefix_attempt_event_id'];pe=events[peid][2];initial=pe['payload']['replay_evidence'];replay=initial;repref=evref(peid,'/payload/replay_evidence');trs=[events[eid][2]['payload'] for eid in initial['replay_transition_event_ids']]
   gens=[(eid,events[eid][2]) for eid in refs['recovery_generation_event_ids']]
   stage1=[(eid,e) for eid,e in gens if e['identity'].get('component')=='stage1'];stage2=[(eid,e) for eid,e in gens if e['identity'].get('component')=='stage2' and e['identity'].get('stage_two_attempt')==1]
   checks['exactly_one_initial_stage1_stage2']=len(stage1)==len(stage2)==1
   g1id,g1e=stage1[0];g2id,g2e=stage2[0];s1=g1e['payload']['evidence'];g1=s1['generation'];parsed=g2e['payload']['evidence'];gen=parsed['generation'];command=parsed.get('command');genref=evref(g2id,'/payload/evidence/generation');physical_id=g2id
   trids=refs['recovery_transition_event_ids'];action=events[trids[0]][2]['payload']['action'] if trids else {};transition=action.get('transition');exe=bool(trids);executed=action.get('command');trref=evref(trids[0],'/payload/action/transition') if trids else None
   suffix=[]
   for eid in refs['suffix_transition_event_ids']:
    e=events[eid][2];p=e['payload'];tr=p['transition'];suffix.append({**tr,'action':p['command'],'observation_before':p['before_state']['observation'],'valid_actions_before':p['before_state']['valid_actions'],'action_executed':True})
   recover_label=a['success'];rec_reason=a['sft_termination_reason'];suffix_refs={'path':str(eventpath),'event_ids_sha256':vs(refs['suffix_transition_event_ids']),'first':evref(refs['suffix_transition_event_ids'][0]) if refs['suffix_transition_event_ids'] else None,'last':evref(refs['suffix_transition_event_ids'][-1]) if refs['suffix_transition_event_ids'] else None}
   source_done=events[pe['payload']['source_episode_event_id']][2]
   checks.update({'existing_replay_exact':initial['replay_match'] is True,'full_prefix_replay_source_match':len(trs)==d and all(t['command']==steps[j]['action'] and t['before_state']['observation']==steps[j]['observation'] and t['before_state']['valid_actions']==steps[j]['valid_actions'] and t['transition']['observation']==steps[j+1]['observation'] for j,t in enumerate(trs)),
    'initial_replay_current_observation':initial['observation_sha256']==ts(obs),'initial_replay_current_map':initial['action_map_sha256']==vs(mapping),'initial_replay_full_history':initial['history_sha256']==vs(history),
    'first_action_public_before_match':not exe or (action['history_before']==history and action['observation_before']==obs and action['valid_actions_before']==acts and action['action_map']==mapping and action['recovery_action_index']==1),
    'generation_identity_bound':all(e['identity'].get('prefix_id')==c['prefix_id'] and e['identity'].get('canonical_trial_id')==c['canonical_task'] and e['implementation_sha']=='2da980f631badc25086d12db60d128ff507d3ae6' for eid,e in gens),
    'source_episode_receipt_task_bound':source_done['identity'].get('canonical_trial_id')==c['canonical_task'],
    'K1_counts_match_recorded_events':a['recovery_environment_actions']==len(trids) and a['sft_environment_actions']==len(suffix)})
   result['r19_evidence']={'initial_stage1':evref(g1id),'initial_stage2':evref(g2id),'first_environment_step':trref,'source_episode':evref(pe['payload']['source_episode_event_id']), 'K1_arm':evref(a['arm_event_id']), 'K1_derived_source_event_id':a.get('derived_source_event_id'),'first_target_only':True}
  aid=parsed.get('action_id');tmap=parsed.get('id_to_command') or {};raw=gen.get('raw_output')
  checks.update({'stage1_valid':s1.get('status')=='valid','stage1_generation_complete':g1.get('output_complete') is True,
   'stage2_complete_not_truncated':gen.get('output_complete') is True,
   'stage2_raw_bare_ID':isinstance(raw,str) and isinstance(aid,str) and raw.strip()==aid and re.fullmatch(r'A\d{3}',aid) is not None,
   'stage2_recorded_selected':parsed.get('status')=='selected','teacher_map_equals_P0_every_ID':tmap==mapping,
   'teacher_ordered_actions_if_recorded':parsed.get('valid_actions',acts)==acts,
   'same_ID_same_command':tmap.get(aid)==command and mapping.get(aid)==command,
   'first_action_executed_command_transition':exe is True and bool(transition) and command==executed})
  if s1.get('status') not in (None,'valid'):invalid.append('STAGE1_INVALID:'+str(s1.get('status')))
  if g1.get('output_complete') is False:invalid.append('STAGE1_TRUNCATED')
  if gen.get('output_complete') is False:invalid.append('STAGE2_TRUNCATED')
  if parsed.get('status') not in (None,'selected'):invalid.append('STAGE2_INVALID:'+str(parsed.get('status')))
  if raw is not None and not checks['stage2_raw_bare_ID']:invalid.append('STAGE2_NOT_BARE_EXECUTABLE_ID')
  if exe is False:invalid.append('FIRST_ACTION_NOT_EXECUTED')
  if exe and command!=executed:invalid.append('EXECUTED_COMMAND_MISMATCH')
  if not checks['teacher_map_equals_P0_every_ID']:result['Q_hist_reasons'].append('REINDEX_REQUIRED_NO_TARGET_CHANGE')
  result['replay']={'source':repref,'record_sha256':vs(replay),'original_prefix_transition_count':len(trs),'original_existing_receipt_only_no_new_replay':True}
  result['first_target']={'producer':'adapter-off base','action_id':aid,'command':command,'raw_output_sha256':ts(raw) if isinstance(raw,str) else None,
   'source':genref,'generation_record_sha256':vs(gen),'parser_status':parsed.get('status'),'stage1_status':s1.get('status'),
   'teacher_map_sha256':vs(tmap),'executed':exe,'executed_command':executed,'transition_source':trref,'transition_sha256':vs(transition) if transition else None,
   'physical_generation_event_id':physical_id,'physical_reuse_evidence':'AUTHENTICATED_GENERATION_EVENT_ID' if physical_id else 'NOT_PROVEN_LEGACY_NO_EVENT_ID'}
  # Both labels are checked from original complete branches under the same stop rules.
  if st!='R19_K1':
   cn,ch,cr=controls[st][c['prefix_id']];ctl=cr.get('continue') or cr.get('continue_full') or cr;cs=ctl.get('steps',[]);clabel=ctl.get('success',cr.get('continue_success',cr.get('r_continue')));creason=ctl.get('termination_reason',cr.get('termination_reason'))
   ctlref=ref(CONTROLS[st],cn,ch)
   recorded_control=r['continue']['success'] if st=='R4' else r.get('r_continue',r.get('continue_success'))
   checks['CONTINUE_label_cross_record_binding']=int(recorded_control)==int(clabel)
   checks['CONTINUE_task_identity']=canon(cr.get('task_id',c['canonical_task']))==c['canonical_task']
  else:
   cs=steps[d:];clabel=r['continue_success'];ctlref=ref(sp,sn,sh,f'/steps/{d}:end');creason=s.get('termination_reason')
   # Original source trajectories end at done/truncated or at their action cap.
   if not creason:creason='environment_terminal' if cs and (cs[-1].get('done') or cs[-1].get('truncated')) else 'remaining_horizon' if len(cs)==horizon else 'selection_failure'
   checks['CONTINUE_label_cross_record_binding']=int(clabel)==int(success_step(steps[-1]))
  cp=stop_proof(cs,clabel,creason,horizon)
  rp=stop_proof(suffix,recover_label,rec_reason,horizon,transition if exe else None)
  for name,proof in [('CONTINUE',cp),('recover',rp)]:
   for check in ['label_matches_original_terminal_predicate','recorded_stop_supported','executed_actions_within_horizon']:checks[name+'_'+check]=proof[check]
  result['labels']={'CONTINUE':int(clabel),'recover':int(recover_label),'original_frozen_rule':'terminal done && reward>0, original horizon/selection fail-closed stops','historical_labels_retained':True}
  ctlterm=cs[-1] if cs else {};rterm=suffix[-1] if suffix else transition or {}
  if st=='R19_K1':
   recovery_terminal_ref=evref(refs['suffix_transition_event_ids'][-1],'/payload/transition') if suffix else trref
   control_terminal_ref=ref(sp,sn,sh,f'/steps/{len(steps)-1}')
  else:
   recovery_terminal_ref=br|{'pointer':('/recover/continuation/steps/' if st=='R4' else '/continuation_full/steps/')+str(len(suffix)-1)} if suffix else trref
   control_terminal_ref=ctlref|{'pointer':('/continue/steps/' if st=='R4' else '/continue_full/steps/' if st=='R10_OSR' else '/steps/')+str(len(cs)-1)}
  result['terminal_corroboration']={'CONTINUE':terminal_info(ctlterm,control_terminal_ref),'recover':terminal_info(rterm,recovery_terminal_ref),'missing_won_is_not_mechanical_failure':True}
  result['stop_proof']={'CONTINUE':cp,'recover':rp}
  result['suffix_evidence_only']={'actions_recorded':len(suffix),'source':suffix_refs,'sequence_sha256':vs(suffix),'teacher_target_adopted':False,'adapter':'SFT-P0 on'}
  result['recorded_inference_tokens']={'stage1':{k:g1.get(k) for k in ['input_tokens','generated_tokens','max_new_tokens','output_complete','token_cap_reached']},'stage2':{k:gen.get(k) for k in ['input_tokens','generated_tokens','max_new_tokens','output_complete','token_cap_reached']},'source_actor':step.get('token_statistics'),'projected_training_tokens':None}
  failed=[k for k,v in checks.items() if v is not True]
  result['failed_checks']=failed
  result['Q_hist_reasons'].extend(invalid or failed)
  result['Q_hist']='EXCLUDE' if invalid else 'HOLD' if failed else 'PASS'
 except (KeyError,IndexError,TypeError,ValueError,AttributeError) as e:
  result['Q_hist']='EXCLUDE' if invalid else 'HOLD';result['Q_hist_reasons'].extend(invalid);result['Q_hist_reasons'].append('MISSING_OR_UNCLOSED_EVIDENCE:'+type(e).__name__+':'+str(e));result['failed_checks']=[k for k,v in checks.items() if v is not True]
 result['Q_pin']='PASS' if result['Q_hist']=='PASS' and model_info[st]['axis']=='MODEL_IDENTITY_PINNED' else 'EXCLUDE' if result['Q_hist']=='EXCLUDE' else 'HOLD'
 result['Q_pin_reasons']=[] if result['Q_pin']=='PASS' else (['Q_HIST_NOT_PASS'] if result['Q_hist']!='PASS' else [])+(['HISTORICAL_MODEL_IDENTITY_PARTIAL'] if model_info[st]['axis']!='MODEL_IDENTITY_PINNED' else [])
 return result

out=[one(c,r) for c,r in pr]
assert len(out)==171 and len({x['case_id'] for x in out})==171
# Selection receives only quality, identity, physical receipt and public target keys, never outcomes.
selection=[{k:x.get(k) for k in ('case_id','canonical_task','stage','prefix_id','anchor_key','Q_hist','Q_pin')}|{'physical_id':x.get('first_target',{}).get('physical_generation_event_id'),'projection_sha256':x.get('source_public',{}).get('projection_sha256'),'command':x.get('first_target',{}).get('command')} for x in out]
output('selection_inputs_without_outcomes.json',selection)

def select(quality):
 chosen=[x for x in selection if x[quality]=='PASS'];flows={'RAW':[x['case_id'] for x in selection],'QUALITY':[x['case_id'] for x in chosen]};removed={};ordered=lambda v:sorted(v,key=lambda x:(x['anchor_key'],x['case_id']))
 seen=set();phys=[]
 for x in ordered(chosen):
  key=x['physical_id']
  if key is not None and key in seen:removed[x['case_id']]={'reason':'PHYSICAL_GENERATION_REUSE','key':key};continue
  if key is not None:seen.add(key)
  phys.append(x)
 flows['PHYSICAL_DEDUP']=[x['case_id'] for x in phys];seen=set();anch=[]
 for x in ordered(phys):
  key=x['canonical_task']
  if key in seen:removed[x['case_id']]={'reason':'NONMINIMUM_TASK_ANCHOR','key':key};continue
  seen.add(key);anch.append(x)
 flows['TASK_ANCHOR']=[x['case_id'] for x in anch];seen={};final=[]
 for x in ordered(anch):
  key=(x['projection_sha256'],x['command'])
  if key in seen:removed[x['case_id']]={'reason':'EXACT_PUBLIC_INPUT_TARGET_DUPLICATE','kept_case_id':seen[key]};continue
  seen[key]=x['case_id'];final.append(x)
 flows['EXACT_INPUT_TARGET_DEDUP']=[x['case_id'] for x in final]
 return {'flow_case_ids':flows,'removed_after_quality':removed,'registered_used_task_ids_after_anchor':sorted({x['canonical_task'] for x in anch}),'no_slot_refill':True}
sel_hist=select('Q_hist');sel_pin=select('Q_pin')
# Only now join immutable labels for descriptive counts / B,C set definitions.
byid={x['case_id']:x for x in out}
def category(x):
 l=x.get('labels',{});a,b=l.get('CONTINUE'),l.get('recover')
 return 'C_rescue' if (a,b)==(0,1) else 'neutral_success' if (a,b)==(1,1) else 'harm' if (a,b)==(1,0) else 'failure' if (a,b)==(0,0) else 'LABEL_UNRESOLVED'
def describe(ids):
 xs=[byid[k] for k in ids]
 def summarise(ys):
  cnt=Counter(category(x) for x in ys)
  return {'rows':len(ys),'unique_tasks':len({x['canonical_task'] for x in ys}),'B':cnt['C_rescue']+cnt['neutral_success'],'C':cnt['C_rescue'],'B_minus_C':cnt['neutral_success'],'harm':cnt['harm'],'failure':cnt['failure'],'label_unresolved':cnt['LABEL_UNRESOLVED']}
 return summarise(xs)|{'by_source':{st:summarise([x for x in xs if x['stage']==st]) for st in SOURCES},'by_family':{f:summarise([x for x in xs if x['family']==f]) for f in sorted({x['family'] for x in out})}}
def pool_sets(s):
 ids=s['flow_case_ids']['EXACT_INPUT_TARGET_DEDUP'];groups={n:[byid[k] for k in ids if category(byid[k])==cat] for n,cat in [('C','C_rescue'),('B_minus_C','neutral_success'),('harm','harm'),('failure','failure')]};groups['B']=groups['C']+groups['B_minus_C']
 sets={name:{'case_ids':sorted(x['case_id'] for x in xs),'task_ids':sorted({x['canonical_task'] for x in xs})} for name,xs in groups.items()}
 assert set(sets['C']['case_ids'])<=set(sets['B']['case_ids'])
 neutral=Counter((x['stage'],x['family']) for x in groups['B_minus_C']);cs=Counter((x['stage'],x['family']) for x in groups['C'])
 capacity=sum(min(v,neutral[k]) for k,v in cs.items())
 return {'sets':sets,'B_different_from_C':bool(groups['B_minus_C']),
 'distinct_task_count_upper_bounds_not_training_N':{'B_vs_C_per_arm_without_token_balance':min(len(groups['B']),len(groups['C'])),'disjoint_neutral_vs_C_unmatched':min(len(groups['B_minus_C']),len(groups['C'])),'disjoint_neutral_vs_C_same_source_and_family':capacity},
 'C_source_family_neutral_coverage':[{'stage':k[0],'family':k[1],'C':v,'B_minus_C':neutral[k]} for k,v in sorted(cs.items())],
 'training_N':'NOT_ESTABLISHED','actual_training_tokens':'UNKNOWN_NO_TOKENIZER','equal_budget_control':'NOT_ESTABLISHED'}
counts={'schema':'SI_P2_FIXED_FLOW_V1','Q_hist':{name:describe(ids) for name,ids in sel_hist['flow_case_ids'].items()},'Q_pin':{name:describe(ids) for name,ids in sel_pin['flow_case_ids'].items()},'Q_hist_dispositions':dict(Counter(x['Q_hist'] for x in out)),'Q_pin_dispositions':dict(Counter(x['Q_pin'] for x in out))}
pools={'Q_hist':pool_sets(sel_hist),'Q_pin':pool_sets(sel_pin)}
for x in out:
 for q,ss in [('Q_hist',sel_hist),('Q_pin',sel_pin)]:
  x[q+'_final_destination']='FINAL_ANCHOR' if x['case_id'] in ss['flow_case_ids']['EXACT_INPUT_TARGET_DEDUP'] else ss['removed_after_quality'].get(x['case_id'],{}).get('reason',x[q])
previous=[]
for old in prior['cases']:
 x=byid[old['case_id']]
 previous.append({'case_id':x['case_id'],'canonical_task':x['canonical_task'],'Q_hist':x['Q_hist'],'Q_hist_reasons':x['Q_hist_reasons'],'Q_hist_destination':x['Q_hist_final_destination'],'Q_pin':x['Q_pin'],'Q_pin_destination':x['Q_pin_final_destination'],
 'in_C_hist':x['case_id'] in pools['Q_hist']['sets']['C']['case_ids'],'in_C_pin':x['case_id'] in pools['Q_pin']['sets']['C']['case_ids'],
 'same_public_projection_as_P1':x.get('source_public',{}).get('projection_sha256')==old['public_projection']['projection_sha256'],
 'same_first_target_as_P1':x.get('first_target',{}).get('command')==old['first_recovery_target']['mapped_command']})
inputgroups=defaultdict(list)
for x in out:
 if x['Q_hist']=='PASS':inputgroups[x['source_public']['projection_sha256']].append(x)
ambiguities=[{'projection_sha256':h,'case_ids':[x['case_id'] for x in xs],'commands':sorted({x['first_target']['command'] for x in xs}),'different_targets':len({x['first_target']['command'] for x in xs})>1,'no_automatic_exclusion':True} for h,xs in inputgroups.items() if len(xs)>1]
result={'schema':'SI_P2_COMMON_QUALITY_AUDIT_V1','fixed_parent_rows':171,'scientific_calls_added':0,'scientific_permission':'NOT_GRANTED','DATA_FEASIBILITY':'NOT_READY','learning_gain':'NOT_PROVEN','qualified_training_N':'NOT_ESTABLISHED','model_identity_reference':'model_identity_bindings.json','cases':out,'selection_hist':sel_hist,'selection_pin':sel_pin,'pool_sets':pools,'original_eleven_dispositions':previous,'same_public_input_groups':ambiguities,'no_training_examples_exported':True}
# Compact output: shared field contracts and interned absolute file paths.
# Every locator keeps its original line/hash/pointer; paths resolve via file_locations.
for item in result['cases']:
 item.get('source_public',{}).pop('field_pointers',None)
 item.get('source_public',{}).pop('projection_contract',None)
 item.get('source_public',{}).pop('projection_and_stored_public_text_only_not_tokenizer_validation',None)
 item.get('source_public',{}).pop('full_training_prompt_or_JSONL_exported',None)
 item.get('labels',{}).pop('original_frozen_rule',None)
 item.get('first_target',{}).pop('producer',None)
 for proof in item.get('stop_proof',{}).values():
  for k in ['label_matches_original_terminal_predicate','recorded_stop_supported','executed_actions_within_horizon']:
   proof.pop(k,None) # Booleans remain in item['checks']; no lost check.
result['shared_field_contract']={
 'goal':'source reference /task/text', 'observation':'source /steps/d/observation',
 'ordered_map':'source /steps/d/valid_actions, complete original order, A000... enumeration',
 'H4':'for j=max(0,d-4)..d-1: action at /steps/j/action; result at /steps/(j+1)/observation',
 'all_fields_available_before_action_d':True,'no_current_output_or_teacher_subgoal_card':True,
 'projection_encoding':'ASCII JSON ensure_ascii=True sort_keys=True separators comma-colon, map as list of ID-command pairs',
 'public_projection_not_tokenizer_or_chat_validation':True,
 'success_rule':'original terminal done && reward>0; recorded horizon/selection fail-closed stops',
 'complete_generation':'original output_complete=True; token_cap_reached alone is not truncation, EOS may occur at cap',
 'teacher':'adapter-off first recovery action only','suffix':'adapter-on SFT-P0, original branch evidence only'}
path_to_id={};file_locations={}
def compact_paths(value):
 if isinstance(value,list):return [compact_paths(v) for v in value]
 if not isinstance(value,dict):return value
 out={}
 for k,v in value.items():
  if k=='path' and isinstance(v,str) and v.startswith('/'):
   if v not in path_to_id:
    ident=f'F{len(path_to_id):03d}';path_to_id[v]=ident;file_locations[ident]=v
   out['file_id']=path_to_id[v]
  else:out[k]=compact_paths(v)
 return out
stored=compact_paths(result);stored['file_locations']=file_locations
p=OWN/'pool_quality_audit.json';p.write_text(json.dumps(stored,ensure_ascii=False,separators=(',',':'))+'\n')
output('pipeline_counts.json',counts);output('pool_sets.json',pools);output('original_eleven_dispositions.json',previous)
finish_bindings()
print('UTC',datetime.datetime.now(datetime.timezone.utc).isoformat())
print('DISPOSITIONS',counts['Q_hist_dispositions'],'pin',counts['Q_pin_dispositions'])
for q in ('Q_hist','Q_pin'):
 print(q,{k:{n:v for n,v in c.items() if n not in ('by_source','by_family')} for k,c in counts[q].items()})
 print(q,'capacities',pools[q]['distinct_task_count_upper_bounds_not_training_N'])
for x in out:
 if x['Q_hist']!='PASS':print('NOT_PASS',x['case_id'],x['Q_hist'],x['Q_hist_reasons'],x['failed_checks'])
print('ORIGINAL_ELEVEN',json.dumps(previous,ensure_ascii=False));print('audit_bytes',p.stat().st_size,'input_files',len(BINDINGS));print('same_input_groups',json.dumps(ambiguities,ensure_ascii=False))
