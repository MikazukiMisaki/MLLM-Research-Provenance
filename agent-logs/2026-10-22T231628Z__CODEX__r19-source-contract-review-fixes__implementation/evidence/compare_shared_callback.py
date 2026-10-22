"""Compare old/current shared smoke callback behavior using synthetic edges only."""
import ast,json,runpy,subprocess,sys,types
from pathlib import Path
import pytest
root=Path('/home/lizening/wt-r19-source-contract-review-fixes')
sys.path[:0]=[str(root),str(root/'src')]
ns=runpy.run_path(str(root/'tests/test_r19_source_pipeline.py'))
r=ns['runner']
from recovery.r19_duration import RecoveryCursor,execute_common_recovery_path,extend_common_recovery_path
old_source=subprocess.check_output(['git','-C',str(root),'show','da7d348:scripts/run_r19_experiment.py'],text=True)
klass=next(x for x in ast.parse(old_source).body if isinstance(x,ast.ClassDef) and x.name=='LiveR19Runtime')
old_methods={}
for name in ['recovery_step_callback','common_path_step_factory']:
 node=next(x for x in klass.body if isinstance(x,ast.FunctionDef) and x.name==name)
 namespace=dict(vars(r));exec(compile(ast.get_source_segment(old_source,node),'<recorded-da7d348-method>','exec'),namespace)
 old_methods[name]=namespace[name]
results={}
for version in ['old','new']:
 for p in [8,18]:
  sandbox=Path(__file__).parent/f'callback_{version}_prefix_{p}'
  sandbox.mkdir()
  with pytest.MonkeyPatch.context() as mp:
   runtime,registry,schedule,output,envs,pending=ns['runtime_fixture'](sandbox,mp)
   runtime.mode='smoke'
   if version=='old':
    for name,method in old_methods.items():setattr(runtime,name,types.MethodType(method,runtime))
   episode=schedule['episodes'][0];env=runtime.new_environment(episode['canonical_trial_id'],30000,'train')
   env.actions=['look']*p
   cursor=RecoveryCursor(task=env.task,task_id=env.task.task_id,canonical_trial_id=env.task.task_id,
    nominal_seed=30000,observation=f'state {p}',valid_actions=ns['ACTIONS'],
    history=tuple((f'state {i}','look') for i in range(p)),actions_consumed=p)
   runtime.bind_recovery_prefix(cursor)
   runtime.active_attempt_envs['synthetic-smoke']=env
   path=execute_common_recovery_path(prefix_id='synthetic-smoke',prefix=cursor,
    stage_one_call=runtime.recovery_stage_one,stage_two_call=runtime.recovery_stage_two,
    environment_step=runtime.recovery_step_callback(env,cursor,'synthetic-smoke'),event_sink=runtime.sink,max_actions=1)
   path=extend_common_recovery_path(path=path,stage_two_call=runtime.recovery_stage_two,
    environment_step=runtime.common_path_step_factory(path),event_sink=runtime.sink,max_actions=3)
   events=ns['read_events'](output)
   scientific_generations=[{'identity':e['identity'],'generation':e['payload']['evidence']['generation']} for e in events if e['kind']=='generation_completed']
   scientific_transitions=[{'before':e['payload']['before_state'],'transition':e['payload']['transition'],'command':e['payload']['command'],'action_id':e['payload']['action_id'],'action_map':e['payload']['action_map']} for e in events if e['kind']=='environment_operation_completed']
   indices=[e['identity']['recovery_action_index'] for e in events if e['kind']=='environment_operation_completed']
   results[f'{version}_{p}']={'generations':scientific_generations,'transitions':scientific_transitions,'indices':indices,
    'model_calls':dict(runtime.model_call_counts),'environment_operations':dict(runtime.environment_operation_counts),
    'checkpoints':{str(k):r._cursor_identity(v) for k,v in path.checkpoints.items()},'stop':path.stopping_reason}
for p in [8,18]:
 old=results[f'old_{p}'];new=results[f'new_{p}']
 for field in ['generations','transitions','model_calls','environment_operations','checkpoints','stop']:assert old[field]==new[field],field
 assert old['indices']==[1,1,2] and new['indices']==[1,2,3]
summary={'class':'synthetic_shared_G2_callback_comparison_not_smoke','prefix_actions':[8,18],
 'model_prompts_raw_tokens_commands_public_transitions_checkpoints_stop_and_total_cost':'IDENTICAL',
 'old_physical_indices':[1,1,2],'new_physical_indices':[1,2,3],
 'no_model_or_ALFWorld_calls':True,'actual_G2_executed_SHA':r.R19_G2_EXECUTED_SHA,
 'new_SHA_carry_forward':'PENDING_SOL_EXACT_SHA_REVIEW'}
(Path(__file__).parent/'shared_callback_comparison.json').write_text(json.dumps({'summary':summary,'raw':results},indent=2)+'\n')
print(json.dumps(summary,indent=2))
