import ast,copy,hashlib,json,os,re,runpy,subprocess,sys
from pathlib import Path
import pytest
root=Path('/tmp/r19-independent-review-2da980f');p=Path('/tmp/r19-2da-review-path.txt').read_text().strip();p=Path(p)
sys.path[:0]=[str(root),str(root/'src')]
from scripts import run_r19_experiment as r
from scripts import analyze_r19_recovery_duration as a
ns=runpy.run_path(str(root/'tests/test_r19_source_pipeline.py'))
auth,_=r._load_g3_authorization()
amend=json.loads(r.R19_B1_G3_SOURCE_CONTRACT_REPAIR_AMENDMENT.read_text())
overlay=dict(auth['scientific_execution_fingerprints'])
overlay.update({k:v['new'] for k,v in amend['changed_method_fingerprints'].items()})
assert len(overlay)==40
assert r._current_scientific_function_fingerprints(overlay)==overlay
old=r._current_scientific_function_fingerprints(auth['scientific_execution_fingerprints'])
changed={k for k in old if old[k]!=auth['scientific_execution_fingerprints'][k]}
assert changed==set(amend['changed_method_fingerprints']) and len(changed)==9
# Independently verify every frozen old fingerprint against actual baseline Git bytes.
for key,expected in auth['scientific_execution_fingerprints'].items():
 rel,name=key.split('::');s=subprocess.check_output(['git','-C',str(root),'show','bf31f3da:'+rel],text=True);tree=ast.parse(s);parts=name.split('.')
 nodes=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==parts[0]]
 node=nodes[0]
 if len(parts)==2:node=next(x for x in node.body if isinstance(x,ast.FunctionDef) and x.name==parts[1])
 assert hashlib.sha256(ast.get_source_segment(s,node).encode()).hexdigest()==expected,key
frozen={}
for rel in ['R19_PROTOCOL.md','configs/experiments/r19_recovery_duration_v1.json','configs/experiments/r19_preflight_v3/source_schedule.json','configs/experiments/r19_preflight_v3/exclusion_manifest.json','configs/experiments/r19_b1_g3_authorization_v1.json','configs/experiments/r19_b1_g3_entrypoint_repair_authorization_v1.json','configs/experiments/r19_b1_baseline_manifest.json']:
 original=subprocess.check_output(['git','-C',str(root),'show','bf31f3da:'+rel]);assert original==(root/rel).read_bytes();frozen[rel]=hashlib.sha256(original).hexdigest()
schedule=json.loads((root/'configs/experiments/r19_preflight_v3/source_schedule.json').read_text());assert len(schedule['episodes'])==127 and [x['schedule_index'] for x in schedule['episodes']]==list(range(127))
restart=json.loads(r.R19_B1_G3_SOURCE_CONTRACT_RESTART_AUTHORIZATION.read_text());caps=restart['restart']['remaining_phase_caps']
assert caps['model_calls']['source']==caps['environment_operations']['source']==8999
assert restart['restart']['cumulative_start']=={'model_generations':177,'environment_operations_including_resets':342}
summary={'implementation_sha':'2da980f631badc25086d12db60d128ff507d3ae6','frozen_files':frozen,'method_fingerprints':{'count':40,'changed_count':9,'changed_methods':amend['changed_method_fingerprints'],'all_old_base_and_new_target_match':True,'effective_sha256':r.sha256_json(overlay)},'record_hashes':{f.name:r.sha256_file(f) for f in [r.R19_B1_G3_SOURCE_CONTRACT_REPAIR_AMENDMENT,r.R19_B1_G3_SOURCE_CONTRACT_RESTART_AUTHORIZATION,r.R19_B1_G3_SOURCE_UNIT_RESOLUTION]},'caps':caps,'projected_maximum':{'model_calls':177+sum(caps['model_calls'].values()),'env_operations':342+sum(caps['environment_operations'].values())},'global_ceilings':auth['resource_limits']['cumulative_campaign_ceilings_including_g2'],'two_task_production_cases':[]}
for case in ['valid_full_paths','invalid_later_aliases']:
 casepath=p/('local-independent-'+case);casepath.mkdir()
 with pytest.MonkeyPatch.context() as mp:
  runtime,registry,schedule,output,envs,pending=ns['runtime_fixture'](casepath,mp,restart=True,count=2)
  if case=='invalid_later_aliases':
   calls=[0]
   def gen(backend,prompt,cap):
    if cap==40:raw='Diagnosis: Immediate issue\nSubgoal: take pencil 1 from desk 1'
    elif backend is runtime.recovery_backend:
     calls[0]+=1;raw='A000' if calls[0]<=2 else 'invalid'
    else:raw='A000'
    return ns['generation'](prompt,raw,cap)
   mp.setattr(r,'_generate_exact',gen)
  execution=r._run_frozen_pilot(runtime=runtime,schedule=schedule,output_path=output,registry=registry,sink=runtime.sink,pending_attempts=pending)
  runtime.close_remaining_environments()
  events=ns['read_events'](output);branches=[json.loads(l) for l in (output/'branches.jsonl').read_text().splitlines()]
  physical=a.validate_event_ledger(events,expected_evidence_class='synthetic')
  evidence=a.validate_branch_evidence(branches,events,return_operation_ids=True)
  source=a.validate_live_source_schedule(schedule,{'schema_version':'r19_exclusion_manifest_v1','status':'frozen_before_inference','excluded_task_trial_ids':[]},events,evidence['_operation_event_ids'],physical)
  comparison=ns['comparison_arguments'](runtime,output);comparison['comparison_path']=Path(comparison['comparison_path']);a.validate_source_restart_comparison(**comparison)
  assert source['completed_source_episodes']==2 and execution['formal_branch_count']==2 and evidence['validated_k_arms']==10
  for row in [json.loads(l) for l in (output/'source_trajectories.jsonl').read_text().splitlines()]:assert r._trajectory_sha256(row)==row['metadata']['source_trajectory_sha256']
  clean=dict(os.environ)
  for k in ['PYTHONPATH','PYTHONHOME','VIRTUAL_ENV']:clean.pop(k,None)
  command=[sys.executable,str(root/'scripts/analyze_r19_recovery_duration.py'),'--protocol',str(r.R19_PROTOCOL),'--events',str(output/'execution_events.jsonl'),'--branches',str(output/'branches.jsonl'),'--output',str(casepath/'report'),'--evidence-class','synthetic','--allow-synthetic']
  cli=[]
  for repetition in range(2):
   result=subprocess.run(command,cwd='/tmp',env=clean,capture_output=True,text=True);cli.append({'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr});assert result.returncode==0,result.stderr
  (casepath/'cli_receipts.json').write_text(json.dumps({'argv':command,'clean_environment':True,'runs':cli},indent=2)+'\n')
  summary['two_task_production_cases'].append({'case':case,'source_episodes':source['completed_source_episodes'],'branches':len(branches),'K_arms':evidence['validated_k_arms'],'physical':physical,'phase_env_counts':dict(runtime.environment_operation_counts),'recovery_call_counts':[{k:v['logical_cost']['recovery_only']['model_calls'] for k,v in row['k_results'].items()} for row in branches],'fresh_cli_exit_codes':[x['exit_code'] for x in cli],'report_idempotent':True})
checks={}
for name,cmd in [('diff_check',['git','diff','--check','bf31f3da..2da980f']),('py_compile',[sys.executable,'-m','py_compile','scripts/run_r19_experiment.py','scripts/analyze_r19_recovery_duration.py','scripts/run_r19_recovery_duration.py','tests/test_r19_source_contract.py','tests/test_r19_source_pipeline.py','tests/test_r19_g3_authorization.py'])]:
 child=subprocess.run(cmd,cwd=root,capture_output=True,text=True);checks[name]={'exit_code':child.returncode,'stdout':child.stdout,'stderr':child.stderr};assert child.returncode==0
summary['checks']=checks
focused=(p/'evidence/focused.log').read_text();full=(p/'evidence/full.log').read_text();baseline=Path('/tmp/r19-independent-full.log').read_text()
ids=lambda t:set(re.findall(r'^(?:FAILED|ERROR) (tests/\S+)',t,re.M))
assert ids(full)==ids(baseline)
summary['tests']={'focused':focused.strip().splitlines()[-1],'full':full.strip().splitlines()[-1],'new_failure_error_ids':sorted(ids(full)-ids(baseline)),'unchanged_failure_error_ids':sorted(ids(full))}
(p/'evidence/independent_checks.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({'tests':summary['tests'],'two_task_cases':[{k:c[k] for k in ['case','source_episodes','branches','K_arms','phase_env_counts','recovery_call_counts','fresh_cli_exit_codes']} for c in summary['two_task_production_cases']],'record_hashes':summary['record_hashes'],'changed_fingerprints':len(changed)},indent=2))
