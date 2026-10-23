import copy,datetime,hashlib,json,os,shutil,subprocess
from pathlib import Path
repo=Path('/home/lizening/research-notes');root=Path('/home/lizening/wt-r19-recovery-duration-v1')
out=Path(Path('/tmp/r19-live-proposal-v2-review-path.txt').read_text().strip())
revision=repo/'agent-logs/2026-10-23T003452Z__LUNA__r19-live-proposal-revision-2__2da980f'
old_dir=repo/'agent-logs/2026-10-23T002200Z__LUNA__r19-live-proposal__2da980f'
prior=repo/'agent-logs/2026-10-23T002952Z__SOL__r19-exact-live-proposal-review__2da980f_5a72b1'
release_dir=repo/'agent-logs/2026-10-23T000029Z__SOL__r19-phase1-preflight-release__2da980f_669620'
source='2da980f631badc25086d12db60d128ff507d3ae6'
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(path):return json.loads(Path(path).read_text())
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def canon(value):return json.dumps(value,ensure_ascii=True,sort_keys=True,separators=(',',':'))
def objsha(value):return hashlib.sha256(canon(value).encode()).hexdigest()
def put(name,value):(out/name).write_text(json.dumps(value,ensure_ascii=True,sort_keys=True,indent=2)+'\n')
commands=[]
def git(path,*args):
    z=subprocess.run(['git','-C',str(path),*args],text=True,capture_output=True)
    commands.append({'argv':['git','-C',str(path),*args],'exit_code':z.returncode,'stdout':z.stdout,'stderr':z.stderr})
    assert z.returncode==0,commands[-1]
    return z.stdout.strip()
assert git(root,'rev-parse','HEAD')==source and git(root,'status','--porcelain')=='' and git(root,'branch','--show-current')==''
assert git(root,'ls-remote','origin','refs/heads/codex/r19-source-contract-review-fixes').split()[0]==source
assert git(root,'ls-remote','origin','refs/heads/codex/r19-recovery-duration-v1').split()[0]=='bf31f3da430ffc35bd17fc380e1752adce6d1467'
head=git(repo,'rev-parse','HEAD');assert head=='405346e0fad9c419b103f9a31898a4bf95ec1583'
assert git(repo,'ls-remote','origin','refs/heads/main').split()[0]==head
assert git(repo,'diff','--name-only')=='' and git(repo,'diff','--cached','--name-only')==''
raw_expected={'R19_LIVE_SUCCESSOR_PROPOSAL_REVISION_2.md':'d6b4ebb9f77c434411e39f9ef13aea1bc42f86580bdaadf43c529e267202f754',
 'bindings.json':'a6fd21f10c0acd28740c153521b3d0027e1445c51ce2600089eb73fd56cc82d9',
 'correction_evidence.json':'77e01ef93a9b5a0ed97858b1eff0ff06b83ee0b458764a6596f383ac596c7410',
 'child_argv.json':'af84459ed7a90bb59f90b4965e959d4e80a24d6c3c563f443b4cb8f4433781fe',
 'supervisor_argv.json':'c9f57d2735d95250b8a12d34c68f6ea7e8bd644e9a5c194bad55d42a81b4024b',
 'environment_plan.json':'24af21a3db2ae89abc56f81e5fb8e457ed3a801ca9fc21ef40a472b4c02703c9'}
for name,value in raw_expected.items():assert sha(revision/name)==value,name
b=load(revision/'bindings.json');old=load(old_dir/'bindings.json');evidence=load(revision/'correction_evidence.json')
assert b['proposal_revision']==2
for key,hash_key in [('proposal_path','proposal_sha256'),('bindings_path','bindings_sha256'),('superseding_review_path','superseding_review_sha256')]:
    assert sha(b['supersedes'][key])==b['supersedes'][hash_key]
assert b['supersedes']['proposal_sha256']=='c7b1a59fcb1ec2d968ac691efe4d3a3a6ddf523beb9df24d89cc902bca204967'
assert b['supersedes']['bindings_sha256']=='9f10793c0e73ac70c861c0ef8a8d2babbbe878f5aba167a5b4c61f26d2e05aa2'
assert b['supersedes']['superseding_review_sha256']=='afe215c3785b128f4d9c1a3be4840cf524b7712a6cd7eb3cfca2b060ab142916'
assert sha(prior/'LUNA_CORRECTION_TASK.md')==b['supersedes']['correction_task_sha256']
assert sha(prior/'corrected_binding_requirements.json')=='4082394774d072e8c7f7d5f75097856ca6fe64298d7e58efd0f5aa2308ea6bf9'
correct=load(prior/'corrected_binding_requirements.json')

# Compare all unaffected binding data exactly, not only selected fields.
old_unchanged=copy.deepcopy(old);new_unchanged=copy.deepcopy(b)
for key in ('proposal_revision','supersedes'):new_unchanged.pop(key)
for key in ('model_snapshot_aggregate_sha256','runtime_preload_sha256','runtime_manifest_sha256'):old_unchanged['scientific_and_input_bindings'].pop(key)
for key in ('preflight_receipt_model_files_sha256','frozen_preload_runtime_expectations_canonical_sha256','historical_runtime_artifacts','future_live_post_load_runtime_identity'):new_unchanged['scientific_and_input_bindings'].pop(key)
for key in ('old_live_runner_log_sha256','old_live_runner_exit_sha256','old_live_supervisor_status_sha256'):old_unchanged['failed_predecessor_and_cost'].pop(key)
new_unchanged['failed_predecessor_and_cost'].pop('authentic_predecessor_supervisor')
old_unchanged['future_protocol_limits_not_authorization'].pop('fixed_quotas')
new_unchanged['future_protocol_limits_not_authorization'].pop('fixed_quotas')
assert old_unchanged==new_unchanged,'Unreviewed binding delta'
for name in ('child_argv.json','supervisor_argv.json','environment_plan.json'):
    assert (revision/name).read_bytes()==(old_dir/name).read_bytes()
assert objsha(load(revision/'child_argv.json'))=='93aa3a833fbb65241fcab6b7e68d3863fa83985084d9c1b27875c730285f55ef'
assert objsha(load(revision/'supervisor_argv.json'))=='c2270f4e43d88d53022b38bc4bc0e1890bc49b738387f99485045fd9020e450a'
assert objsha(load(revision/'environment_plan.json'))=='d0bd5721913a6316affcbd4918befe65f2f9400a9d6e14536b88df5627e62189'
assert objsha(b)=='33d10f0ccc5831a1fa782a61360b3aacab6fc04a48afe560e655c83eb0bb2eaa'
assert objsha(evidence)=='cb000c9be53e8195455e7417e435dba52d036a3319956561ab28482293948cc7'
release=load(release_dir/'phase1_release.json');gate=load(release['gate']['destination'])
assert sha(release['gate']['destination'])==b['source']['phase1_gate_sha256']==release['gate']['sha256']
auth_path=root/'configs/experiments/r19_b1_g3_source_contract_restart_authorization_v1.json'
auth=load(auth_path);assert sha(auth_path)==b['scientific_and_input_bindings']['source_contract_restart_authorization_sha256']
pred=b['failed_predecessor_and_cost'];actual=pred['authentic_predecessor_supervisor'];observed={}
assert actual['run_id']==pred['predecessor_run_id']==auth['predecessor']['run_id']==correct['authentic_predecessor_run_id']
assert actual['implementation_sha']==auth['predecessor']['implementation_sha']
assert set(actual['artifacts'])==set(auth['predecessor']['supervisor_record_sha256'])
for name,artifact in actual['artifacts'].items():
    assert Path(artifact['path']).parent==Path(actual['record_directory'])
    assert sha(artifact['path'])==artifact['raw_sha256']==auth['predecessor']['supervisor_record_sha256'][name]
    assert artifact['path']==correct['authentic_predecessor_supervisor'][name]['path']
    observed[name]={'path':artifact['path'],'raw_sha256':sha(artifact['path'])}
    if name.endswith('.json'):
        parsed=load(artifact['path']);assert parsed['run_id']==actual['run_id'] and parsed['implementation_sha']==actual['implementation_sha']
        observed[name]['parsed']={k:parsed.get(k) for k in ('run_id','implementation_sha','evidence_class','status','exit_code','exit_code_source','supersedes_run_id','events_sha256','launch_context_sha256','runner_log_sha256')}
ex=load(actual['artifacts']['runner_exit.json']['path']);status=load(actual['artifacts']['supervisor_status.json']['path']);context=load(actual['artifacts']['launch_context.json']['path'])
assert ex['status']==status['status']==actual['status']=='failed' and ex['exit_code']==status['exit_code']==actual['exit_code']==1
assert ex['exit_code_source']=='subprocess.returncode' and ex['events_sha256']==pred['predecessor_events_sha256']
assert context['evidence_class']==actual['evidence_class']=='live'
assert context['supersedes_run_id']==actual['supersedes_run_id']=='a0de515d7e104101bf8157175ea3d995'
assert ex['launch_context_sha256']==observed['launch_context.json']['raw_sha256']
assert ex['runner_log_sha256']==status['runner_log_sha256']==observed['runner.log']['raw_sha256']
assert status['runner_exit_sha256']==observed['runner_exit.json']['raw_sha256']
ev1=evidence['LIVE_P01_run_identity_and_supervisor_artifacts']
assert sha(ev1['restart_authorization_path'])==ev1['restart_authorization_raw_sha256']==sha(auth_path)
for name,item in ev1['actual_files'].items():
    assert sha(item['path'])==item['actual_raw_sha256']==item['restart_authorization_expected_raw_sha256']==observed[name]['raw_sha256']
wrong=ev1['old_proposal_misbound_hash_trio_is_a0de_not_3d1'];wrong_dir=Path(wrong['historical_record_directory'])
for field,file in [('runner_exit_json_raw_sha256','runner_exit.json'),('supervisor_status_json_raw_sha256','supervisor_status.json'),('runner_log_raw_sha256','runner.log')]:assert sha(wrong_dir/file)==wrong[field]
wrong_exit=load(wrong_dir/'runner_exit.json')
assert wrong_exit['run_id']==wrong['parsed_run_id']=='a0de515d7e104101bf8157175ea3d995'
assert wrong_exit['implementation_sha']==wrong['parsed_implementation_sha']=='ef2328f06256054a6b71c6dc4bdc74dab3a1d3d9' and wrong_exit['events_sha256'] is None
protocol_path=root/'configs/experiments/r19_recovery_duration_v1.json';protocol=load(protocol_path)
quotas=protocol['population']['eligible_targets_by_stratum']
assert quotas==auth['frozen_science']['eligible_quotas']==b['future_protocol_limits_not_authorization']['fixed_quotas']==correct['frozen_eligible_quotas']
ev2=evidence['LIVE_P02_quota_semantics']
assert sha(ev2['protocol_path'])==ev2['protocol_raw_sha256']==sha(protocol_path)
assert ev2['protocol_parsed_value']==ev2['authorization_parsed_value']==quotas
assert ev2['other_distinct_protocol_field']['value']==protocol['population']['candidate_queue_targets']
domains={}
fields=b['scientific_and_input_bindings'];ev3=evidence['LIVE_P03_runtime_digest_domains']
for name,item in fields['historical_runtime_artifacts'].items():
    domains[name]={'path':item['path'],'raw_file_sha256':sha(item['path']),'canonical_object_sha256':objsha(load(item['path']))}
    assert domains[name]==item==correct['historical_runtime_artifact_domains'][name]
    evidence_key='historical_runtime_manifest' if name=='runtime_manifest.json' else 'historical_runtime_manifest_preload'
    assert item['raw_file_sha256']==ev3[evidence_key]['actual_raw_sha256'] and item['canonical_object_sha256']==ev3[evidence_key]['actual_canonical_object_sha256']
assert fields['frozen_preload_runtime_expectations_canonical_sha256']==gate['runtime_manifest_preload_sha256']==correct['frozen_preload_runtime_expectations_canonical_sha256']
assert fields['future_live_post_load_runtime_identity']==ev3['future_live_post_load_runtime']=='NOT_OBSERVED'
model_binding=fields['preflight_receipt_model_files_sha256'];model_receipt=load(model_binding['receipt_path'])
assert sha(model_binding['receipt_path'])==model_binding['receipt_raw_sha256']
assert model_binding['receipt_field']=='model_files_sha256' and model_receipt[model_binding['receipt_field']]==model_binding['value']
assert evidence['model_aggregate_field_check']['actual_value']==model_binding['value']
assert evidence['model_aggregate_field_check']['actual_json_field']==model_binding['receipt_field']
protected=load(release_dir/'release_time_state_and_hash_checks.json')['protected_files']
for path,value in protected.items():assert sha(path)==value
prior_preflight=load(b['preflight_and_reviews']['actual_preflight_verification_path'])
assert sha(b['preflight_and_reviews']['actual_preflight_verification_path'])==b['preflight_and_reviews']['actual_preflight_verification_sha256']
assert sha(release['review']['path'])==b['preflight_and_reviews']['implementation_review_json_sha256']
assert sha(release['adjudication']['path'])==b['preflight_and_reviews']['known_failed_adjudication_sha256']
assert prior_preflight['status']=='PASS_INDEPENDENT_EXACT_SHA_PRODUCTION_PREFLIGHT_VERIFICATION'
assert b['preflight_and_reviews']['raw_preflight_supervisor_hashes']==prior_preflight['evidence_sha256']
assert b['preflight_and_reviews']['actual_preflight_run_id']==prior_preflight['run_id']
for name,value in prior_preflight['evidence_sha256'].items():assert sha(Path(release['supervisor_record_directory'])/name)==value
output=Path(b['future_path_absence_checked']['scientific_output']);record=Path(b['future_path_absence_checked']['supervisor_record_directory'])
assert not any(os.path.lexists(path) for path in (output,record,record.parent,Path(release['scientific_output_sentinel'])))
assert load(revision/'child_argv.json')[load(revision/'child_argv.json').index('--output')+1]==str(output)
active=[]
for process in Path('/proc').iterdir():
    if not process.name.isdigit():continue
    try:
        args=[v.decode(errors='replace') for v in (process/'cmdline').read_bytes().split(b'\0') if v]
        if args and 'python' in Path(args[0]).name and any(Path(a).name in ('launch_r19_supervised.py','run_r19_recovery_duration.py','run_r19_experiment.py') for a in args[1:]):active.append({'pid':int(process.name),'argv':args})
    except OSError:pass
assert not active
old_output=root/auth['predecessor']['output_relative_path']
assert sorted(str(p) for p in (root/'artifacts/runtime').glob('r19_b1_g3_*'))==[str(old_output)]
assert load(old_output/'execution_manifest.json')['status']=='RUNNING'
assert len(load(old_output/'unit_registry.json')['units'])==1 and next(iter(load(old_output/'unit_registry.json')['units'].values()))['status']=='in_progress'
inventories={}
for path,base in [(repo/'FILE_HASHES.sha256',repo),(revision/'FILE_HASHES.sha256',revision)]:
    count=0
    for line in path.read_text().splitlines():
        value,name=line.split('  ',1);assert sha(base/name)==value;count+=1
    inventories[str(path)]={'count':count,'status':'PASS'}
remote={}
for path in revision.iterdir():
    if not path.is_file():continue
    z=subprocess.run(['git','-C',str(repo),'show',f'origin/main:{path.relative_to(repo)}'],capture_output=True)
    assert z.returncode==0 and z.stdout==path.read_bytes();remote[str(path.relative_to(repo))]=sha(path)
assert git(root,'status','--porcelain')==''
observations={'raw_proposal_hashes':raw_expected,'unchanged_binding_subtrees_match_previous_reviewed_proposal':True,
    'argv_environment_byte_identical_to_reviewed_revision1':True,'authentic_supervisor_observations':observed,
    'actual_quotas':quotas,'historical_runtime_domains':domains,'model_aggregate_binding':model_binding,
    'old_proposal_bytes_preserved':True,'protected_file_count':len(protected),'all_protected_file_hashes_unchanged':True,
    'inventories':inventories,'remote_file_bytes_match':remote,'future_output_record_parent_absent':True,
    'active_r19_processes':active,'only_original_failed_g3_output':str(old_output),
    'reviewer_new_supervisor_preflight_model_environment_scientific_calls':0}
put('independent_raw_comparison_results.json',observations)
put('raw_git_receipts.json',commands)
(out/'reviewed-proposal').mkdir()
for name in raw_expected:shutil.copyfile(revision/name,out/'reviewed-proposal'/name)
review={'schema_version':'r19_independent_exact_live_proposal_revision2_review_v1','status':'PASS_EXACT_PROPOSAL_REVIEW_ONLY',
    'start_utc':started,'finish_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'Sol',
    'reviewer_task':'01a0994c-a209-7600-8a3e-5ff3096ed346','implementation_sha':source,
    'proposal_path':str(revision/'R19_LIVE_SUCCESSOR_PROPOSAL_REVISION_2.md'),'proposal_sha256':raw_expected['R19_LIVE_SUCCESSOR_PROPOSAL_REVISION_2.md'],
    'bindings_path':str(revision/'bindings.json'),'bindings_sha256':raw_expected['bindings.json'],
    'correction_evidence_sha256':raw_expected['correction_evidence.json'],
    'EXACT_LIVE_PROPOSAL_REVIEW':'PASS','resolved_findings':['LIVE-P01','LIVE-P02','LIVE-P03'],'findings':[],
    'IMPLEMENTATION_REVIEW':'PASS_EXACT_2da980f_UNCHANGED','G2_CARRY_FORWARD':'PASS_AUTHENTIC_92aae1d_NO_RERUN',
    'ACTUAL_PRODUCTION_PREFLIGHT':'PASS_a9ca70cb_UNCHANGED','preflight_verification_sha256':b['preflight_and_reviews']['actual_preflight_verification_sha256'],
    'implementation_review_sha256':b['preflight_and_reviews']['implementation_review_json_sha256'],
    'known_failed_adjudication_sha256':b['preflight_and_reviews']['known_failed_adjudication_sha256'],
    'source_treatment_semantics_changed':False,'scientific_execution_behavior_changed':True,
    'child_argv_canonical_sha256':objsha(load(revision/'child_argv.json')),
    'supervisor_argv_canonical_sha256':objsha(load(revision/'supervisor_argv.json')),
    'environment_plan_raw_sha256':raw_expected['environment_plan.json'],'environment_plan_canonical_sha256':objsha(load(revision/'environment_plan.json')),
    'gate_sha256':b['source']['phase1_gate_sha256'],'execution_cwd':str(root),'proposed_scientific_output':str(output),'proposed_supervisor_record_directory':str(record),
    'cumulative_actual':release['cumulative_start'],'remaining_phase_caps':release['remaining_phase_caps'],'global_ceilings':release['global_ceilings'],
    'first_source_expected_snapshot_sha256':auth['predecessor']['restart_snapshot_sha256'],
    'genuine_first_source_restart_comparison':'NOT_RUN','genuine_first_source_completion':'NOT_RUN','genuine_G3_cohort_and_G4':'NOT_AVAILABLE',
    'known_failed_source_disposition':'Accepted independent append-only KNOWN_FAILED; original registry in_progress/manifest RUNNING remain unchanged.',
    'observed_provenance_main':head,'new_scientific_calls':0,'new_supervisor_or_preflight_calls':0,
    'LIVE_LAUNCH_CLEARANCE':'NOT_GRANTED','fresh_explicit_user_scientific_authorization':'NOT_GRANTED','launch_allowed':False,
    'conditions':['Only these exact proposal/source/argv/env/gate/input bindings reviewed; drift invalidates acceptance.',
        'Separate independent exact-proposal launch clearance and fresh explicit user scientific authorization both required before any supervisor/model/environment process.',
        'Old live clearance and one-preflight release consumed; no repeat preflight or automatic retry.',
        'Any authorized future first-source snapshot mismatch/failure/uncertainty stops and preserves costs/raw evidence; no retry or tuning.',
        'A possible future launch is one engineering successor only, fresh run UUID/output/record, old unit incomplete and historical177/342 retained.',
        'No G2 rerun, training, held-out work, scientific code/input changes or G4 authorization. Genuine G3 validation required before G4.']}
put('exact_proposal_revision2_review.json',review)
authorization_request={'schema_version':'r19_specific_scientific_authorization_request_v1','status':'PENDING_USER_DECISION_NOT_AUTHORIZATION',
    'requested_action':'Authorize one supervised live G3 engineering successor under reviewed exact proposal revision2; not executed by this request.',
    'proposal_path':review['proposal_path'],'proposal_sha256':review['proposal_sha256'],'bindings_sha256':review['bindings_sha256'],
    'implementation_sha':source,'review_artifact_path':str(out/'exact_proposal_revision2_review.json'),
    'review_artifact_sha256':sha(out/'exact_proposal_revision2_review.json'),
    'child_argv_path':str(revision/'child_argv.json'),'child_argv_canonical_sha256':review['child_argv_canonical_sha256'],
    'supervisor_argv_path':str(revision/'supervisor_argv.json'),'supervisor_argv_canonical_sha256':review['supervisor_argv_canonical_sha256'],
    'environment_plan_path':str(revision/'environment_plan.json'),'environment_plan_raw_sha256':review['environment_plan_raw_sha256'],
    'gate_sha256':review['gate_sha256'],'execution_cwd':str(root),'proposed_scientific_output':str(output),'proposed_supervisor_record_directory':str(record),
    'predecessor_run_id':auth['predecessor']['run_id'],'requested_maximum_live_launches':1,'automatic_retry':False,
    'scheduled_TRAIN_identities':127,'schedule_first_index':0,'attempt_cap':120,'eligible_cap':60,'eligible_quotas':quotas,'K':[1,2,3,4,5],'horizon':50,
    'cumulative_start':release['cumulative_start'],'source_remaining_model_generations':8999,'source_remaining_environment_operations':8999,
    'remaining_phase_caps':release['remaining_phase_caps'],'global_ceilings':release['global_ceilings'],
    'projected_cumulative_maximum':load(release['review']['path'])['projected_cumulative_maximum'],
    'first_source_snapshot_sha256':review['first_source_expected_snapshot_sha256'],'compare_before_first_action':True,
    'stop_on_failure_mismatch_or_uncertainty_without_retry':True,'original_evidence_immutable_and_prior_costs_retained':True,
    'G2_rerun_authorized':False,'new_preflight_authorized':False,'G4_authorized':False,'training_or_heldout_authorized':False,
    'approval_received':False,'LIVE_LAUNCH_CLEARANCE':'NOT_GRANTED','launch_allowed':False,
    'after_explicit_user_approval':'Independently recheck drift/absence/process/input bindings, then issue separate exact launch clearance before dispatching any live invocation.',
    'why_explicit_approval_required':'The prior one-successor live clearance was consumed and current proposal explicitly withholds fresh scientific authorization; technical review PASS does not authorize science.'}
put('user_authorization_request.json',authorization_request)
shutil.copyfile(__file__,out/'review_revision2_read_only.py')
print(json.dumps({'status':review['status'],'resolved':review['resolved_findings'],'inventories':inventories,'proposal_sha256':review['proposal_sha256'],
    'review_sha256':sha(out/'exact_proposal_revision2_review.json'),'user_authorization_request_sha256':sha(out/'user_authorization_request.json'),
    'LIVE_LAUNCH_CLEARANCE':'NOT_GRANTED','launch_allowed':False},indent=2))
