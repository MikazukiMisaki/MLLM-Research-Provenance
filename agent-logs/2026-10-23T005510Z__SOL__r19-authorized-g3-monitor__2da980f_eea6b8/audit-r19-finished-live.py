import datetime,hashlib,json,subprocess,sys,traceback
from pathlib import Path
p=Path(Path('/tmp/r19-live-monitor-path.txt').read_text().strip());cd=Path(Path('/tmp/r19-live-clearance-path.txt').read_text().strip())
c=json.loads((cd/'launch_clearance.json').read_text());root=Path(c['execution_cwd']);out=Path(c['scientific_output_path']);supervisor=Path(c['supervisor_record_directory'])
def load(x):return json.loads(Path(x).read_text())
def sha(x):return hashlib.sha256(Path(x).read_bytes()).hexdigest()
def objsha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=True,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def put(name,value):(p/name).write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
receipt=load(supervisor/'runner_exit.json');status=load(supervisor/'supervisor_status.json');context=load(supervisor/'launch_context.json')
assert receipt['exit_code_source']=='subprocess.returncode'
assert receipt['run_id']==context['run_id']==status['run_id']=='260422ac02bd42a8b2929d7ef240526b'
assert receipt['implementation_sha']==context['implementation_sha']==c['implementation_sha']
assert receipt['command_sha256']==context['command_sha256']==c['argv']['child_canonical_sha256']
assert context['command_argv']==load(c['argv']['child_path']) and context['supervisor_argv']==load(c['argv']['supervisor_path'])
assert context['effective_environment']==load(c['environment_plan']['path'])['set']
assert receipt['interrupted_by_supervisor'] is False
assert receipt['launch_context_sha256']==sha(supervisor/'launch_context.json')
assert receipt['runner_log_sha256']==sha(supervisor/'runner.log')
raw_hashes={str(f.relative_to(out)):sha(f) for f in sorted(out.rglob('*')) if f.is_file()}
supervisor_hashes={f.name:sha(f) for f in sorted(supervisor.iterdir()) if f.is_file()}
events=[json.loads(line) for line in (out/'execution_events.jsonl').read_text().splitlines() if line.strip()]
branches=[json.loads(line) for line in (out/'branches.jsonl').read_text().splitlines() if line.strip()]
manifest=load(out/'execution_manifest.json');runtime=load(out/'runtime_manifest.json');environment=load(out/'environment_manifest.json');registry=load(out/'unit_registry.json')
sys.path[:0]=[str(root),str(root/'src')]
from scripts import analyze_r19_recovery_duration as a
physical=a.validate_event_ledger(events,expected_evidence_class='live');put('final_raw_physical_validation.json',physical)
new_cost={'model_generations':physical['completed_physical_model_generations'],'non_reset_environment_operations':physical['physical_environment_operations'],'resets':physical['physical_environment_resets'],'incomplete_external_operations':physical['incomplete_operations']}
new_cost['environment_operations_including_resets']=new_cost['non_reset_environment_operations']+new_cost['resets']
total={key:c['cumulative_start'][key]+value for key,value in new_cost.items()}
assert total['model_generations']<=c['global_ceilings']['model_calls'] and total['environment_operations_including_resets']<=c['global_ceilings']['environment_operations']
assert physical['training_run_events']==physical['external_paid_model_call_events']==0
audit={'schema_version':'r19_independent_final_g3_raw_integrity_audit_v1','observed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'run_id':receipt['run_id'],'implementation_sha':receipt['implementation_sha'],'authentic_child_exit_code':receipt['exit_code'],'exit_code_source':'subprocess.returncode',
 'supervisor_status':status['status'],'execution_manifest_status':manifest['status'],'clearance_sha256':sha(cd/'launch_clearance.json'),
 'new_cost':new_cost,'cumulative_cost':total,'raw_output_file_sha256':raw_hashes,'supervisor_file_sha256':supervisor_hashes,
 'G4_executed':False,'G4_acceptance':'BLOCKED_BY_CONFIRMED_V2_PRODUCER_V1_CONSUMER_SCHEMA_CONTRACT',
 'G4_blocker_record_sha256':sha(p/'g4_runtime_schema_contract_finding.json'),'new_scientific_or_preflight_or_report_calls':0}
checks={};errors=[]
def check(name,fn):
 try:checks[name]={'status':'PASS','result':fn()}
 except Exception as error:
  errors.append(name);checks[name]={'status':'FAIL','error_type':type(error).__name__,'error':str(error),'traceback':traceback.format_exc()}
def success_exit():
 assert receipt['exit_code']==0 and receipt['status']==status['status']=='completed'
 return a.validate_live_exit_receipt(receipt,events=events,protocol_sha256=c['protocol_sha256'],events_path=out/'execution_events.jsonl',branches_path=out/'branches.jsonl',receipt_path=supervisor/'runner_exit.json',supervisor_status_path=supervisor/'supervisor_status.json',runner_log_path=supervisor/'runner.log')
check('authentic_success_exit',success_exit)
if receipt['exit_code']==0:
 def branch_integrity():return a.validate_branch_evidence(branches,events,return_operation_ids=True)
 check('production_branch_integrity',branch_integrity)
 branch_ids=checks.get('production_branch_integrity',{}).get('result',{}).get('_operation_event_ids')
 if branch_ids is not None:
  gate=load(c['gate_path'])
  check('production_full_source_and_branch_scope',lambda:a.validate_live_source_schedule(load(gate['source_schedule_path']),load(gate['exclusion_manifest_path']),events,branch_ids,physical))
 def source_comparison():
  auth=load(root/'configs/experiments/r19_b1_g3_source_contract_restart_authorization_v1.json')
  return a.validate_source_restart_comparison(execution_manifest=manifest,events=events,predecessor_run_id=c['supersedes_run_id'],expected_snapshot=auth['predecessor']['restart_snapshot'],expected_snapshot_sha256=c['first_source_restart']['expected_snapshot_sha256'],comparison_path=out/'source_restart_comparison.json')
 check('production_first_source_comparison',source_comparison)
 def runtime_v2_raw_binding():
  assert runtime['schema_version']=='r19_inference_runtime_manifest_v2'
  inference=runtime['inference'];assert inference['local_files_only'] is True and inference['transport']=='local_transformers' and inference['external_model_calls'] is False
  pure={key:value for key,value in runtime.items() if key not in ('model_files','model_adapter_isolation')}
  identity=load(root/'configs/experiments/r19_b1_baseline_manifest.json');assert pure==identity['runtime_expectations']['preload']
  assert objsha(pure)==c['runtime_preload_sha256'] and objsha(runtime['model_files'])==c['model_files_sha256']
  assert objsha(runtime)==manifest['runtime_manifest_sha256']==manifest['run_context']['runtime_manifest_sha256']
  assert objsha(environment)==manifest['environment_manifest_sha256']==manifest['run_context']['environment_manifest_sha256']
  assert all(event['run_context']==manifest['run_context'] for event in events)
  assert runtime['model_adapter_isolation']['distinct_model_objects'] is True and runtime['model_adapter_isolation']['recovery_adapter_active'] is False and runtime['model_adapter_isolation']['sft_adapter_active'] is True
  return {'scope':'Independent raw v2 frozen-baseline/hash/isolation binding only; NOT a production G4 validator PASS. No manifest flattening or conversion.', 'runtime_raw_sha256':sha(out/'runtime_manifest.json'),'runtime_canonical_sha256':objsha(runtime),'preload_canonical_sha256':objsha(pure),'environment_raw_sha256':sha(out/'environment_manifest.json'),'model_files_sha256':objsha(runtime['model_files'])}
 check('independent_frozen_v2_runtime_raw_binding',runtime_v2_raw_binding)
 def manifest_and_budget():
  assert manifest['status']=='PILOT_READY_FOR_OFFLINE_ANALYSIS' and manifest['physical_expenditure']==physical
  assert manifest['events_sha256']==sha(out/'execution_events.jsonl') and manifest['branches_sha256']==sha(out/'branches.jsonl')
  assert sum(manifest['model_call_counts_by_phase'].values())==new_cost['model_generations']
  assert sum(manifest['environment_operation_counts_by_phase'].values())==new_cost['environment_operations_including_resets']
  for key,value in manifest['model_call_counts_by_phase'].items():assert value<=c['remaining_phase_caps']['model_calls'][key],key
  for key,value in manifest['environment_operation_counts_by_phase'].items():assert value<=c['remaining_phase_caps']['environment_operations'][key],key
  assert len(branches)==manifest['execution']['formal_branch_count']==39
  assert manifest['execution']['source_episode_count']==127 and manifest['execution']['initial_attempt_count']==39
  assert manifest['execution']['eligible_by_stratum']=={'failure':6,'success_control':15,'random_control':15}
  assert manifest['execution']['branch_arm_count']==183
  return {'execution':manifest['execution'],'model_call_counts_by_phase':manifest['model_call_counts_by_phase'],'environment_operation_counts_by_phase':manifest['environment_operation_counts_by_phase'],'all_frozen_phase_caps_respected':True,'global_caps_respected':True,'unused_G2_capacity_not_reallocated':True}
 check('g3_manifest_cost_caps_and_counts',manifest_and_budget)
 def completed_registry():
  units=registry['units'];unfinished=[{'id':key,'status':value.get('status'),'identity':value.get('identity')} for key,value in units.items() if value.get('status')!='completed']
  assert unfinished==[],unfinished
  return {'unit_count':len(units),'unfinished_units':unfinished}
 check('new_run_unit_registry',completed_registry)
def frozen_files():
 expected=load(cd/'final_drift_check.json')['protected_hashes']
 for path,value in expected.items():assert sha(path)==value,path
 assert sha(c['gate_path'])==c['gate_sha256']
 head=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip();dirty=subprocess.check_output(['git','-C',str(root),'status','--porcelain'],text=True).strip()
 assert head==c['implementation_sha'] and not dirty
 return {'protected_file_count':len(expected),'all_old_protected_bytes_unchanged':True,'source_head':head,'source_clean':True}
check('frozen_source_and_predecessor_G2_postcheck',frozen_files)
audit['checks']=checks;audit['failed_integrity_checks']=errors
audit['status']='G3_EXIT0_RAW_INTEGRITY_PASS_G4_CONSUMER_BLOCKED' if receipt['exit_code']==0 and not errors else 'G3_RESULT_REQUIRES_FAILURE_OR_INTEGRITY_REVIEW_NO_RETRY'
audit['production_G4_runtime_provenance_validator']='NOT_RUN; confirmed raw-schema reject predicate already recorded. No fabricated v1 document or fake final fields supplied.'
audit['statistics_or_report_renderer_executed']=False
put('final_g3_integrity_audit.json',audit)
print(json.dumps({key:audit[key] for key in ('status','run_id','authentic_child_exit_code','execution_manifest_status','new_cost','cumulative_cost','failed_integrity_checks','G4_acceptance')},indent=2))
