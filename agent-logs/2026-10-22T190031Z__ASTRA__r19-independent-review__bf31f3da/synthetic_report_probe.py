"""Synthetic CLI report probe. No model calls and no ALFWorld instances."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
root=Path('/home/lizening/wt-r19-recovery-duration-v1')
sys.path[:0]=[str(root),str(root/'src')]
from recovery.r19_duration import DurableEventJournal,sha256_json,sum_generation_cost
from scripts.analyze_r19_recovery_duration import _source_trajectory_digest,_record_for_parser
from models.protocol_stability import parse_p2_selection
from recovery.two_stage import parse_stage_one_output
from recovery.two_stage_v2 import parse_bare_stage_two_output
out=Path('/tmp/r19-independent-review/synthetic')
out.mkdir(exist_ok=True)
protocol=root/'configs/experiments/r19_recovery_duration_v1.json'
j=DurableEventJournal(out/'events.jsonl',run_id='independent-synthetic-cli-only',protocol_sha256=hashlib.sha256(protocol.read_bytes()).hexdigest(),code_sha='bf31f3da430ffc35bd17fc380e1752adce6d1467',evidence_class='synthetic')
task='synthetic-review-only/trial-001'; pid='synthetic-ineligible'; actions=['look']; obs='Synthetic observation'
def emit(kind,identity,payload): return j.append(kind,identity,payload)
def operation(kind,identity,payload):
 emit(kind+'_started',identity,payload)
 return emit(kind+'_completed',identity,payload)['event_id']
def gen(raw):
 ids=[1,2,3]
 return dict(prompt='synthetic immutable prompt',rendered_prompt_sha256='c'*64,raw_output=raw,token_ids=ids,token_ids_sha256=sha256_json(ids),input_tokens=20,generated_tokens=3,latency_seconds=0.01,max_new_tokens=40,output_complete=True,token_cap_reached=False)
def actor(identity):
 g=gen('bad-output'); p=parse_p2_selection(g['raw_output'],tuple(actions),reflection_required=False)
 evidence={'generation':g,'action_map':{'A000':'look'},'parser_result':dict(valid_actions=actions,id_to_command={'A000':'look'},selection_status=p.selection_status,action_id=p.action_id,action=p.action,failure_category=p.action_failure_category,failure_reason=p.action_failure_reason)}
 return operation('generation',identity,{'evidence':evidence}),g
source_gen,source_g=actor(dict(canonical_trial_id=task,component='task_actor',operation='source_generation',decision_index=0))
trajectory={'task':{'task_id':task},'metadata':{'split':'train','task_family':'pick_and_place_simple'},'steps':[{'observation':obs,'valid_actions':actions,'metadata':{'r19_generation_event_id':source_gen}}]}
trajectory_sha=_source_trajectory_digest(trajectory)
source_id=emit('source_episode_completed',{'canonical_trial_id':task,'split':'train'},{'trajectory':trajectory,'trajectory_sha256':trajectory_sha,'generation_event_ids':[source_gen],'transition_event_ids':[]})['event_id']
def reset(identity):
 return operation('environment_operation',dict(canonical_trial_id=task,split='train',**identity),{'operation':'environment_reset','task_id':task,'seed':30000,'transition':dict(observation=obs,valid_actions=actions,reward=0.,done=False,truncated=False,reset=True)})
reset_id=reset(dict(prefix_id=pid,operation='prefix_reset'))
g1=gen('Diagnosis: incomplete')
p1=parse_stage_one_output(_record_for_parser(g1))
s1=operation('generation',dict(prefix_id=pid,canonical_trial_id=task,component='stage1'),{'evidence':dict(generation=g1,status=p1.status,diagnosis=p1.diagnosis,subgoal=p1.subgoal,failure_reason=p1.failure_reason)})
g2=gen('A000');p2=parse_bare_stage_two_output(_record_for_parser(g2),tuple(actions))
s2=operation('generation',dict(prefix_id=pid,canonical_trial_id=task,component='stage2'),{'evidence':dict(generation=g2,status=p2.status,action_id=p2.action_id,command=p2.action,valid_actions=actions,id_to_command=dict(p2.id_to_command),failure_reason=p2.failure_reason)})
attempt=emit('prefix_attempt_completed',{'prefix_id':pid},{'eligible_primary':False,'task_family':'pick_and_place_simple','stratum':'failure','source_episode_event_id':source_id,'replay_evidence':dict(replay_match=True,reset_event_id=reset_id,replay_transition_event_ids=[]),'recovery_generation_event_ids':[s1,s2],'recovery_transition_event_ids':[]})['event_id']
checkpoint_reset=reset(dict(prefix_id=pid,operation='branch_replay_reset',k=1))
restored=dict(task_id=task,canonical_trial_id=task,nominal_seed=30000,observation=obs,valid_actions=actions,history=[],actions_consumed=0)
suffix,suffix_g=actor(dict(prefix_id=pid,canonical_trial_id=task,component='sft',k=1,decision_index=0,actions_consumed=0))
refs=dict(recovery_generation_event_ids=[s1,s2],recovery_transition_event_ids=[],suffix_generation_event_ids=[suffix],suffix_transition_event_ids=[])
cost=dict(recovery_only=sum_generation_cost([g1,g2],environment_actions=0),full_branch=sum_generation_cost([g1,g2,suffix_g],environment_actions=0))
arm=dict(k=1,checkpoint=0,stage_two_attempts_charged=1,recovery_environment_actions=0,sft_action_cap=50,success=0,terminal=False,derived_identity_from=None,derived_source_event_id=None,replay_evidence=dict(replay_match=True,reset_event_id=checkpoint_reset,replay_transition_event_ids=[],checkpoint=0,restored_state_sha256=sha256_json(restored)),evidence_refs=refs,logical_cost=cost)
arm_id=emit('duration_arm_completed',{'prefix_id':pid,'k':1},{'success':0,'logical_cost':cost,'evidence_refs':refs,'derived_identity_from':None,'derived_source_event_id':None})['event_id']
row=dict(prefix_id=pid,canonical_trial_id=task,attempted=True,eligible_primary=False,task_family='pick_and_place_simple',stratum='failure',decision_index=0,nominal_seed=30000,trajectory_sha256=trajectory_sha,continue_success=0,continue_logical_cost={'full_branch':sum_generation_cost([source_g],environment_actions=0)},k_results={'1':arm},evidence_refs=dict(source_episode_event_id=source_id,prefix_attempt_event_id=attempt,continue_={'generation_event_ids':[source_gen],'transition_event_ids':[]},k_arms={'1':dict(arm_event_id=arm_id,operations=refs)}))
row['evidence_refs']['continue']=row['evidence_refs'].pop('continue_')
(out/'branches.jsonl').write_text(json.dumps(row)+'\n')
env=dict(os.environ)
for key in ['PYTHONPATH','PYTHONHOME','VIRTUAL_ENV']:env.pop(key,None)
cmd=[sys.executable,str(root/'scripts/analyze_r19_recovery_duration.py'),'--protocol',str(protocol),'--events',str(out/'events.jsonl'),'--branches',str(out/'branches.jsonl'),'--output',str(out/'report'),'--evidence-class','synthetic','--allow-synthetic']
r=subprocess.run(cmd,cwd=out,env=env,text=True,capture_output=True)
(out/'cli_result.json').write_text(json.dumps({'argv':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'evidence_class':'synthetic','real_model_calls':0,'real_alfworld_calls':0},indent=2)+'\n')
print(r.stdout,r.stderr,'EXIT',r.returncode)
raise SystemExit(r.returncode)
