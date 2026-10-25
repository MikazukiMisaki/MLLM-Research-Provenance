#!/usr/bin/env python3
"""Metadata-only binding of the first completed saved TRAIN source episode."""
import hashlib,json
from pathlib import Path

RUN_ID='260422ac02bd42a8b2929d7ef240526b'
ROOT=Path('/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z')
SUP=Path('/home/lizening/research-notes/agent-logs/2026-10-23T002200Z__LUNA__r19-g3-live-successor__2da980f/supervisor_live')
MON=Path('/home/lizening/research-notes/agent-logs/2026-10-23T005510Z__SOL__r19-authorized-g3-monitor__2da980f_eea6b8')
def sha(p):
 h=hashlib.sha256(); n=0
 with Path(p).open('rb') as f:
  while True:
   b=f.read(8*1024*1024)
   if not b: break
   h.update(b); n+=len(b)
 return {'path':str(p),'bytes':n,'sha256':h.hexdigest()}

def map_facts(obj):
 wanted={'valid_actions','valid_action_map','action_map','admissible_commands','available_actions'}
 found=[]
 def walk(x,path='$'):
  if isinstance(x,dict):
   for k,v in x.items():
    q=path+'.'+str(k)
    if k in wanted:
     encoded=json.dumps(v,ensure_ascii=False,sort_keys=False,separators=(',',':')).encode('utf-8')
     found.append({'path':q,'value_type':type(v).__name__,'count':len(v) if isinstance(v,(list,dict,tuple)) else None,'sha256':hashlib.sha256(encoded).hexdigest(),'is_missing_or_null':v is None})
    walk(v,q)
  elif isinstance(x,list):
   for i,v in enumerate(x): walk(v,f'{path}[{i}]')
 walk(obj)
 return found

traj=ROOT/'source_trajectories.jsonl'
with traj.open('rb') as f: record_bytes=f.readline()
record=json.loads(record_bytes)
meta=record['metadata']; task=record['task']; steps=record.get('steps',[])
task_id=task['task_id']; schedule_index=meta['schedule_index']
registry=json.loads((ROOT/'unit_registry.json').read_text())['units']
matches=[]
for unit_hash,unit in registry.items():
 ident=unit.get('identity',{})
 if ident.get('unit')=='source_episode' and ident.get('canonical_trial_id')==task_id:
  matches.append({'unit_hash':unit_hash,'status':unit.get('status'),'schedule_index':ident.get('schedule_index')})
assert len(matches)==1, f'expected exactly one source registry match, got {len(matches)}'
assert matches[0]['status']=='completed'
assert matches[0]['schedule_index']==schedule_index==0
assert meta.get('split')=='train'
actions=[s['action'] for s in steps]
assert all(isinstance(a,str) and a for a in actions)
actions_canonical=json.dumps(actions,ensure_ascii=False,separators=(',',':')).encode('utf-8')
action_sha=hashlib.sha256(actions_canonical).hexdigest()
game=Path(task['metadata']['game_file']); game_hash=sha(game)
assert game_hash['sha256']==meta['source_game_sha256']

comparison=json.loads((ROOT/'source_restart_comparison.json').read_text())
assert comparison['canonical_trial_id']==task_id and comparison['schedule_index']==schedule_index
assert comparison['status']=='PASS' and comparison['comparison_before_first_environment_action'] is True

context=json.loads((SUP/'launch_context.json').read_text())
exit_receipt=json.loads((SUP/'runner_exit.json').read_text())
status=json.loads((SUP/'supervisor_status.json').read_text())
assert context['run_id']==exit_receipt['run_id']==status['run_id']==RUN_ID
assert exit_receipt['exit_code']==0 and exit_receipt['status']=='completed'
config_path=Path(context['effective_environment']['ALFWORLD_CONFIG_PATH'])
env_manifest=json.loads((ROOT/'environment_manifest.json').read_text())
config_hash=sha(config_path)
assert config_hash['sha256']==env_manifest['alfworld_config_sha256']
base_config=Path('/home/lizening/wt-r19-recovery-duration-v1/configs/local/alfworld_base_a40.yaml')
domain=Path('/home/lizening/alfworld_data/logic/alfred.pddl')
grammar=Path('/home/lizening/alfworld_data/logic/alfred.twl2')

refs=meta['r19_source_event_refs']
expected=set(refs['generation_event_ids']+[refs['reset_event_id'],refs['source_episode_event_id']]+refs['transition_event_ids'])
found={}
with (ROOT/'execution_events.jsonl').open('rb') as f:
 for raw in f:
  ev=json.loads(raw)
  eid=ev.get('event_id')
  if eid in expected:
   found[eid]={'kind':ev.get('kind'),'sequence':ev.get('sequence'),'run_id':ev.get('run_id'),'evidence_class':ev.get('evidence_class'),'payload_keys':sorted(ev.get('payload',{})) if isinstance(ev.get('payload'),dict) else [],'action_map_facts':map_facts(ev.get('payload'))}
if set(found)!=expected: raise RuntimeError('referenced source event IDs missing from original event ledger')
assert all(v['run_id']==RUN_ID and v['evidence_class']=='live' for v in found.values())

integrity=json.loads((MON/'final_g3_integrity_audit.json').read_text())
output_hashes={x['path'].rsplit('/',1)[-1]:x['sha256'] for x in json.loads(Path('/home/lizening/research-notes/agent-logs/2026-10-25T124118Z__LUNA__si-e2-resource-readiness__sie2_4c82/raw/runtime_hashes.stdout.bin').read_text())['g3_output_files']}
super_hashes={x['path'].rsplit('/',1)[-1]:x['sha256'] for x in json.loads(Path('/home/lizening/research-notes/agent-logs/2026-10-25T124118Z__LUNA__si-e2-resource-readiness__sie2_4c82/raw/runtime_hashes.stdout.bin').read_text())['g3_supervisor_files']}
assert output_hashes==integrity['raw_output_file_sha256']
assert super_hashes==integrity['supervisor_file_sha256']

result={
 'schema':'SI_E2_FIRST_SOURCE_REPLAY_CANDIDATE_V1',
 'status':'PREPARATION_ONLY_NO_ENVIRONMENT_CALLS',
 'selection_rule':'First JSONL record in the original source_trajectories file; no outcome-based search or substitution.',
 'original_run_id':RUN_ID,
 'source_record':{
  'trajectory_id':record['trajectory_id'],'canonical_task_id':task_id,'family':meta['task_family'],'split':meta['split'],
  'schedule_index':schedule_index,'seed':record['seed'],'nominal_seed':meta['nominal_seed'],
  'max_steps':meta['max_steps'],'saved_action_command_count':len(actions),'saved_action_sequence_sha256':action_sha,
  'line_bytes':len(record_bytes),'line_sha256':hashlib.sha256(record_bytes).hexdigest(),
  'source_trajectory_sha256_claim_in_record':meta['source_trajectory_sha256'],
  'trajectory_file':sha(traj),'trajectory_data_sha256_claim_in_record':meta['source_traj_data_sha256'],
  'truncated':record.get('truncated'),'recorded_termination_reason':meta.get('termination_reason'),
  'terminal_map_behavior_on_replay':'NOT_OBSERVED_PENDING_ENGINEERING_RELEASE',
  'registry_match':matches[0],
  'source_event_refs':{'generation_count':len(refs['generation_event_ids']),'reset_count':1,'source_episode_count':1,'transition_count':len(refs['transition_event_ids']),'event_ids':refs,'all_refs_found_in_original_live_ledger':True,'matched_events':sorted(found.values(),key=lambda x:x['sequence'])}
 },
 'original_action_map_evidence':{
  'first_saved_step_map_facts':map_facts(steps[0]) if steps else [],
  'last_saved_step_map_facts':map_facts(steps[-1]) if steps else [],
  'reset_event_map_facts':found[refs['reset_event_id']]['action_map_facts'],
  'last_transition_event_map_facts':found[refs['transition_event_ids'][-1]]['action_map_facts'],
  'missing_terminal_action_map_policy':'Preserve missing as missing; do not coerce to empty list/map.'
 },
 'replay_inputs':{
  'saved_game_file':game_hash,
  'active_historical_alfworld_config':config_hash,
  'base_a40_config':sha(base_config),
  'domain_file':sha(domain),'grammar_file':sha(grammar),
  'g3_environment_manifest_alfworld_config_sha256':env_manifest['alfworld_config_sha256'],
  'first_source_snapshot_comparison':{k:comparison.get(k) for k in ['status','expected_snapshot_sha256','observed_snapshot_sha256','comparison_before_first_environment_action','environment_actions_executed_before_comparison']}
 },
 'original_g3_integrity':{
  'current_output_file_hashes_equal_independent_final_audit':True,
  'output_files_verified':len(output_hashes),
  'current_supervisor_file_hashes_equal_independent_final_audit':True,
  'supervisor_files_verified':len(super_hashes),
  'independent_final_decision':str(MON/'INDEPENDENT_G3_FINAL_DECISION.json'),
  'historical_science_cumulative_generations':5142,
  'historical_science_cumulative_environment_operations_including_resets':7949,
  'this_audit_scientific_increments':{'generations':0,'environment_operations':0,'resets':0}
 },
 'fixed_replay_design':{
  'number_of_instances':2,'lifecycle':'Two fresh one-game environment instances, one reset per instance; same reviewed pool_seed in both; never reuse/reset one instance as if it were freshly constructed.',
  'pool_seed':'PENDING_FROZEN_SOL_CLI_AND_INDEPENDENT_REVIEW',
  'reset_seed_for_each_instance':record['seed'],
  'actions_per_replay':len(actions),'total_saved_action_steps':2*len(actions),'total_resets':2,
  'full_public_maps_and_transitions':'Compare every ordered public field/map/transition. Missing terminal action map remains missing and is reported; never coerce to an empty action list.',
  'model_generated_action_execution':'FORBIDDEN',
  'bounded_environment_ceiling':{'max_resets':2,'max_physical_action_steps':100},
  'release_status':'NOT_RELEASED; no instance constructed and no reset/step performed'
 }
}
print(json.dumps(result,sort_keys=True,separators=(',',':')))
