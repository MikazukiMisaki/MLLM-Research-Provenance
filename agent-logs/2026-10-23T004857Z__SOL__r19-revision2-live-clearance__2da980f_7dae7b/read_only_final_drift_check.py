import datetime,hashlib,json,os,subprocess,sys
from pathlib import Path
p=Path(Path('/tmp/r19-live-clearance-path.txt').read_text().strip())
root=Path('/home/lizening/wt-r19-recovery-duration-v1');repo=Path('/home/lizening/research-notes')
review_dir=repo/'agent-logs/2026-10-23T004021Z__SOL__r19-exact-live-proposal-revision2-review__2da980f_9d3489'
proposal_dir=repo/'agent-logs/2026-10-23T003452Z__LUNA__r19-live-proposal-revision-2__2da980f'
release_dir=repo/'agent-logs/2026-10-23T000029Z__SOL__r19-phase1-preflight-release__2da980f_669620'
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(x):return json.loads(Path(x).read_text())
def sha(x):return hashlib.sha256(Path(x).read_bytes()).hexdigest()
def objsha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=True,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def put(name,value):(p/name).write_text(json.dumps(value,ensure_ascii=True,sort_keys=True,indent=2)+'\n')
commands=[]
def git(path,*args):
 z=subprocess.run(['git','-C',str(path),*args],text=True,capture_output=True);commands.append({'argv':['git','-C',str(path),*args],'exit_code':z.returncode,'stdout':z.stdout,'stderr':z.stderr});assert z.returncode==0,commands[-1];return z.stdout.strip()
request=load(review_dir/'user_authorization_request.json');review=load(request['review_artifact_path'])
assert sha(review_dir/'user_authorization_request.json')=='75412c4733663ffa14d9b9802c9775d681f0f5cd40d359328acc96db31503402'
assert sha(request['review_artifact_path'])==request['review_artifact_sha256']=='ac47276b1f97cf4c6d623460b23f13e48035726b73ae7a909877ba71bd573514'
assert sha(request['proposal_path'])==request['proposal_sha256']=='d6b4ebb9f77c434411e39f9ef13aea1bc42f86580bdaadf43c529e267202f754'
assert sha(proposal_dir/'bindings.json')==request['bindings_sha256']
assert sha(proposal_dir/'environment_plan.json')==request['environment_plan_raw_sha256']
assert git(root,'rev-parse','HEAD')==request['implementation_sha'] and git(root,'status','--porcelain')=='' and git(root,'branch','--show-current')==''
assert git(root,'ls-remote','origin','refs/heads/codex/r19-source-contract-review-fixes').split()[0]==request['implementation_sha']
assert git(root,'ls-remote','origin','refs/heads/codex/r19-recovery-duration-v1').split()[0]=='bf31f3da430ffc35bd17fc380e1752adce6d1467'
head=git(repo,'rev-parse','HEAD');assert head=='17c9a8a9e053082c8aebdb83e6813d0dff33f42a'
assert git(repo,'ls-remote','origin','refs/heads/main').split()[0]==head
assert git(repo,'diff','--name-only')=='' and git(repo,'diff','--cached','--name-only')==''
child=load(request['child_argv_path']);supervisor=load(request['supervisor_argv_path']);env=load(request['environment_plan_path'])
assert objsha(child)==request['child_argv_canonical_sha256'] and objsha(supervisor)==request['supervisor_argv_canonical_sha256']
assert all(k not in os.environ for k in env['unset']) and all(os.environ.get(k)==v for k,v in env['set'].items())
assert '--preflight-only' not in child and '--preflight-receipt' not in child and supervisor[supervisor.index('--evidence-class')+1]=='live'
output=Path(request['proposed_scientific_output']);record=Path(request['proposed_supervisor_record_directory'])
assert not any(os.path.lexists(x) for x in (output,record,record.parent))
gate_path=Path(child[child.index('--manifest')+1]);assert sha(gate_path)==request['gate_sha256'];gate=load(gate_path)
active=[]
for item in Path('/proc').iterdir():
 if not item.name.isdigit():continue
 try:
  args=[v.decode(errors='replace') for v in (item/'cmdline').read_bytes().split(b'\0') if v]
  if args and 'python' in Path(args[0]).name and any(Path(v).name in ('launch_r19_supervised.py','run_r19_recovery_duration.py','run_r19_experiment.py') for v in args[1:]):active.append({'pid':int(item.name),'argv':args})
 except OSError:pass
assert active==[],active
gpu=subprocess.run(['nvidia-smi','--query-compute-apps=pid,process_name,used_gpu_memory','--format=csv,noheader'],capture_output=True,text=True)
assert gpu.returncode==0 and not gpu.stdout.strip(),(gpu.returncode,gpu.stdout,gpu.stderr)
sys.path[:0]=[str(root),str(root/'src')]
from scripts import run_r19_experiment as r
from scripts import analyze_r19_recovery_duration as analyzer
assert r.PROJECT_ROOT==root and Path(r.__file__).resolve()==root/'scripts/run_r19_experiment.py'
data=Path(child[child.index('--data-root')+1]);config=Path(child[child.index('--config')+1]);adapter=Path(child[child.index('--adapter')+1])
runtime=r._runtime_manifest(data_root=data,config_path=config);identity=load(r.R19_B1_BASELINE)
assert runtime==identity['runtime_expectations']['preload']
gates=r.validate_execution_gates(mode='pilot',protocol_path=r.R19_PROTOCOL,model_identity_path=r.R19_B1_BASELINE,
 gate_manifest_path=gate_path,output_path=output,schedule_path=Path(gate['source_schedule_path']),exclusion_path=Path(gate['exclusion_manifest_path']),observed_runtime_manifest=runtime)
inputs=r._read_exact_local_inputs(mode='pilot',data_root=data,config_path=config,adapter_path=adapter,
 schedule_path=Path(gate['source_schedule_path']),exclusion_path=Path(gate['exclusion_manifest_path']),protocol=load(r.R19_PROTOCOL),identity=identity)
preflight_review=load(repo/'agent-logs/2026-10-23T001840Z__SOL__r19-phase1-independent-verification__2da980f_d9db8d/preflight_verification.json')
assert objsha(inputs['model_bytes'])==preflight_review['model_files_sha256'] and objsha(inputs['source_files'])==preflight_review['source_file_manifest_sha256']
assert objsha(runtime)==preflight_review['runtime_preload_sha256']
for name,digest in preflight_review['evidence_sha256'].items():assert sha(repo/'agent-logs/2026-10-22T235413Z__CODEX__r19-phase1-preparation__2da980f/preflight_supervisor'/name)==digest
assert sha(repo/'agent-logs/2026-10-23T001840Z__SOL__r19-phase1-independent-verification__2da980f_d9db8d/preflight_verification.json')==review['preflight_verification_sha256']
assert sha(gate['review']['artifact_path'])==gate['review']['artifact_sha256']==review['implementation_review_sha256']
protected=load(release_dir/'release_time_state_and_hash_checks.json')['protected_files']
for path,digest in protected.items():assert sha(path)==digest,path
restart=load(r.R19_B1_G3_SOURCE_CONTRACT_RESTART_AUTHORIZATION);old_output=root/restart['predecessor']['output_relative_path']
assert sorted(str(x) for x in (root/'artifacts/runtime').glob('r19_b1_g3_*'))==[str(old_output)]
assert load(old_output/'execution_manifest.json')['status']=='RUNNING'
assert next(iter(load(old_output/'unit_registry.json')['units'].values()))['status']=='in_progress'
costs={}
for label,directory in {'g2_failed_predecessor':Path(gate['g2_carry_forward']['failed_predecessor_directory']),
 'g2_successful_smoke':Path(gate['g2_carry_forward']['evidence_directory']),'g3_failed_predecessor':old_output}.items():
 ledger=directory/'execution_events.jsonl';events=[json.loads(line) for line in ledger.read_text().splitlines() if line.strip()]
 physical=analyzer.validate_event_ledger(events,expected_evidence_class='live')
 costs[label]={'ledger_path':str(ledger),'ledger_sha256':sha(ledger),'raw_production_validator':physical}
total={'model_generations':sum(x['raw_production_validator']['completed_physical_model_generations'] for x in costs.values()),
 'non_reset_environment_operations':sum(x['raw_production_validator']['physical_environment_operations'] for x in costs.values()),
 'resets':sum(x['raw_production_validator']['physical_environment_resets'] for x in costs.values()),
 'incomplete_external_operations':sum(x['raw_production_validator']['incomplete_operations'] for x in costs.values())}
total['environment_operations_including_resets']=total['non_reset_environment_operations']+total['resets']
assert total==request['cumulative_start']
assert gates['source_restart_remaining_phase_caps']==request['remaining_phase_caps']==restart['restart']['remaining_phase_caps']
assert gates['source_restart_expected_snapshot_sha256']==request['first_source_snapshot_sha256']
assert git(root,'status','--porcelain')=='' and not os.path.lexists(output) and not os.path.lexists(record)
result={'status':'PASS_FINAL_READ_ONLY_LIVE_DRIFT_CHECK','start_utc':started,'finish_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'implementation_sha':request['implementation_sha'],'clean_detached_checkout':True,'local_remote_source_match':True,'frozen_bf31_branch_unchanged':True,
 'proposal_sha256':request['proposal_sha256'],'proposal_review_sha256':request['review_artifact_sha256'],
 'fresh_user_authorization_file_sha256':sha(p/'user_authorization.json'),'gate_sha256':sha(gate_path),
 'child_argv_canonical_sha256':objsha(child),'supervisor_argv_canonical_sha256':objsha(supervisor),
 'environment_plan_raw_sha256':sha(request['environment_plan_path']),'effective_environment_canonical_sha256':objsha(env['set']),
 'runtime_preload_sha256':objsha(runtime),'model_files_sha256':objsha(inputs['model_bytes']),'source_file_manifest_sha256':objsha(inputs['source_files']),
 'snapshot_file_count':len(inputs['model_bytes']['snapshot_file_sha256']),'adapter_file_count':len(inputs['model_bytes']['adapter_file_sha256']),
 'source_identity_count':len(inputs['source_files']),'adapter_directory_sha256':inputs['adapter_sha256'],'config_sha256':sha(config),
 'protected_hashes':protected,'active_R19_processes':active,'gpu_compute_query':{'returncode':gpu.returncode,'stdout':gpu.stdout,'stderr':gpu.stderr},
 'target_scientific_output':str(output),'target_supervisor_record_directory':str(record),'target_output_and_record_and_parent_absent':True,
 'cumulative_actual':total,'remaining_phase_caps':request['remaining_phase_caps'],'global_ceilings':request['global_ceilings'],
 'source_snapshot_sha256':request['first_source_snapshot_sha256'],'old_unit_incomplete_preserved':True,
 'production_gate_validation':'PASS_NO_MOCKS_OR_PROJECT_ROOT_OVERRIDE','reviewer_scientific_or_preflight_calls':0,
 'provenance_start_head':head,'clearance_issued_by_this_check':False}
put('final_drift_check.json',result);put('production_gate_validation.json',gates);put('runtime_preload_observed.json',runtime)
put('raw_git_receipts.json',commands);put('physical_cost_recount.json',{'per_ledger':costs,'total':total})
print(json.dumps({k:result[k] for k in ('status','snapshot_file_count','adapter_file_count','source_identity_count','cumulative_actual','target_output_and_record_and_parent_absent')},indent=2),flush=True)
