import datetime,hashlib,json,os,shutil,subprocess
from pathlib import Path

repo=Path('/home/lizening/research-notes');root=Path('/home/lizening/wt-r19-recovery-duration-v1')
proposal=repo/'agent-logs/2026-10-23T002200Z__LUNA__r19-live-proposal__2da980f'
out=Path(Path('/tmp/r19-live-proposal-review-path.txt').read_text().strip())
release_dir=repo/'agent-logs/2026-10-23T000029Z__SOL__r19-phase1-preflight-release__2da980f_669620'
release=json.loads((release_dir/'phase1_release.json').read_text())
prior_review=repo/'agent-logs/2026-10-23T001840Z__SOL__r19-phase1-independent-verification__2da980f_d9db8d'
source='2da980f631badc25086d12db60d128ff507d3ae6'
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def canonical(value):return json.dumps(value,ensure_ascii=True,sort_keys=True,separators=(',',':'))
def objsha(value):return hashlib.sha256(canonical(value).encode()).hexdigest()
def load(path):return json.loads(Path(path).read_text())
def put(name,value):(out/name).write_text(json.dumps(value,ensure_ascii=True,indent=2,sort_keys=True)+'\n')
commands=[]
def git(path,*args):
    z=subprocess.run(['git','-C',str(path),*args],capture_output=True,text=True)
    commands.append({'argv':['git','-C',str(path),*args],'exit_code':z.returncode,'stdout':z.stdout,'stderr':z.stderr})
    assert z.returncode==0,commands[-1]
    return z.stdout.strip()
assert git(root,'rev-parse','HEAD')==source and git(root,'status','--porcelain')==''
assert git(root,'branch','--show-current')==''
assert git(root,'ls-remote','origin','refs/heads/codex/r19-source-contract-review-fixes').split()[0]==source
assert git(root,'ls-remote','origin','refs/heads/codex/r19-recovery-duration-v1').split()[0]=='bf31f3da430ffc35bd17fc380e1752adce6d1467'
head=git(repo,'rev-parse','HEAD');assert head=='6089c85df4d39f61cf8cf5bca25842f5e6f7db36'
assert git(repo,'ls-remote','origin','refs/heads/main').split()[0]==head
assert git(repo,'diff','--name-only')=='' and git(repo,'diff','--cached','--name-only')==''
raw_expected={'R19_LIVE_SUCCESSOR_PROPOSAL.md':'c7b1a59fcb1ec2d968ac691efe4d3a3a6ddf523beb9df24d89cc902bca204967',
 'child_argv.json':'af84459ed7a90bb59f90b4965e959d4e80a24d6c3c563f443b4cb8f4433781fe',
 'supervisor_argv.json':'c9f57d2735d95250b8a12d34c68f6ea7e8bd644e9a5c194bad55d42a81b4024b',
 'environment_plan.json':'24af21a3db2ae89abc56f81e5fb8e457ed3a801ca9fc21ef40a472b4c02703c9',
 'bindings.json':'9f10793c0e73ac70c861c0ef8a8d2babbbe878f5aba167a5b4c61f26d2e05aa2'}
for name,digest in raw_expected.items():assert sha(proposal/name)==digest
b=load(proposal/'bindings.json');child=load(proposal/'child_argv.json');supervisor=load(proposal/'supervisor_argv.json');env=load(proposal/'environment_plan.json')
canonical_expected={'child_argv.json':'93aa3a833fbb65241fcab6b7e68d3863fa83985084d9c1b27875c730285f55ef',
 'supervisor_argv.json':'c2270f4e43d88d53022b38bc4bc0e1890bc49b738387f99485045fd9020e450a',
 'environment_plan.json':'d0bd5721913a6316affcbd4918befe65f2f9400a9d6e14536b88df5627e62189',
 'bindings.json':'ccef7bbf8a303f8ebb221a1e0e40c26d56e5f6877ad44ce6ad41314d4ac14816'}
for name,digest in canonical_expected.items():
    value=load(proposal/name);assert objsha(value)==digest
    assert canonical(value)==json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')),'ASCII domain mismatch'
assert objsha({'set':env['set'],'unset':env['unset']})=='4c1e7ef497ccdcc288e8e79c844705842ad15697c574108b9f146f3d64c148dc'
output=Path(b['future_path_absence_checked']['scientific_output'])
record=Path(b['future_path_absence_checked']['supervisor_record_directory'])
assert not os.path.lexists(output) and not os.path.lexists(record) and not os.path.lexists(record.parent)
assert output.parent==root/'artifacts/runtime' and output.name.startswith('r19_b1_g3_')
assert output!=Path(release['scientific_output_sentinel'])
assert '--preflight-only' not in child and '--preflight-receipt' not in child
base_child=load(release_dir/'child_argv.json')
expected_child=[];index=0
while index<len(base_child):
    token=base_child[index]
    if token=='--preflight-only':index+=1;continue
    if token=='--preflight-receipt':index+=2;continue
    if token=='--output':expected_child.extend([token,str(output)]);index+=2;continue
    expected_child.append(token);index+=1
assert child==expected_child
expected_supervisor=[child[0],str(root/'scripts/launch_r19_supervised.py'),'--record-dir',str(record),
    '--evidence-class','live','--supersedes-run-id',release['predecessor_run_id'],'--',*child]
assert supervisor==expected_supervisor
preflight_env=load(release_dir/'environment_set_unset.json')
assert env['set']==preflight_env['set'] and env['unset']==preflight_env['unset']
injected=env['supervisor_injected_after_future_authorization']
assert injected['R19_EVIDENCE_CLASS']=='live' and injected['R19_EXIT_RECEIPT_PATH']==str(record/'runner_exit.json')
assert injected['R19_SUPERVISOR_CONTEXT_PATH']==str(record/'launch_context.json')
assert 'SUPERVISOR_GENERATES' in injected['R19_RUN_ID']
assert sha(release['gate']['destination'])==b['source']['phase1_gate_sha256']==release['gate']['sha256']
assert b['source']['implementation_sha']==source and b['source']['execution_root']==str(root)
assert sha(release['review']['path'])==b['preflight_and_reviews']['implementation_review_json_sha256']
assert sha(release['adjudication']['path'])==b['preflight_and_reviews']['known_failed_adjudication_sha256']
assert sha(prior_review/'preflight_verification.json')==b['preflight_and_reviews']['actual_preflight_verification_sha256']
assert sha(prior_review/'INDEPENDENT_PREFLIGHT_REVIEW.md')==b['preflight_and_reviews']['human_preflight_review_sha256']
prior=load(prior_review/'preflight_verification.json');gate=load(release['gate']['destination'])
for name,digest in b['preflight_and_reviews']['raw_preflight_supervisor_hashes'].items():
    assert sha(repo/'agent-logs/2026-10-22T235413Z__CODEX__r19-phase1-preparation__2da980f/preflight_supervisor'/name)==digest==prior['evidence_sha256'][name]
assert b['preflight_and_reviews']['actual_preflight_run_id']==prior['run_id']
assert b['preflight_and_reviews']['preflight_child_returncode']==0
auth=load(root/'configs/experiments/r19_b1_g3_source_contract_restart_authorization_v1.json')
old=root/auth['predecessor']['output_relative_path'];assert output!=old
frozen=load(root/'configs/experiments/r19_recovery_duration_v1.json')
fields=b['scientific_and_input_bindings']
checks={'baseline_manifest_sha256':root/'configs/experiments/r19_b1_baseline_manifest.json',
 'baseline_amendment_sha256':root/'R19_B1_G2_AMENDMENT.md',
 'source_schedule_sha256':Path(gate['source_schedule_path']),
 'exclusion_manifest_sha256':Path(gate['exclusion_manifest_path']),
 'environment_manifest_sha256':old/'environment_manifest.json',
 'alfworld_config_sha256':Path(env['set']['ALFWORLD_CONFIG_PATH']),
 'entrypoint_repair_authorization_sha256':root/'configs/experiments/r19_b1_g3_entrypoint_repair_authorization_v1.json',
 'g3_authorization_record_sha256':root/'configs/experiments/r19_b1_g3_authorization_v1.json',
 'source_contract_repair_amendment_sha256':root/'configs/experiments/r19_b1_g3_source_contract_repair_amendment_v1.json',
 'source_contract_restart_authorization_sha256':root/'configs/experiments/r19_b1_g3_source_contract_restart_authorization_v1.json',
 'source_unit_resolution_events_sha256':root/'configs/experiments/r19_b1_g3_source_unit_resolution_events_v1.jsonl'}
for key,path in checks.items():assert sha(path)==fields[key],key
assert fields['runtime_preload_sha256']==prior['runtime_preload_sha256']
assert fields['model_snapshot_aggregate_sha256']==prior['model_files_sha256']
assert fields['source_manifest_sha256']==prior['source_file_manifest_sha256']
assert fields['adapter_aggregate_sha256']=='6e403d85b150a74dfcc176f1f180ce4baf6fdacd922d2f96b3ceef0a21100f11'
assert fields['model_snapshot_file_count']==12 and fields['adapter_file_count']==11 and fields['source_identity_count']==127
g2=b['g2_carry_forward'];actual_g2=gate['g2_carry_forward']
assert g2['run_id']==actual_g2['g2_run_id'] and g2['executed_implementation_sha']==actual_g2['g2_executed_implementation_sha']
for field,file in [('execution_manifest_sha256','execution_manifest.json'),('execution_events_sha256','execution_events.jsonl'),
                   ('branches_sha256','branches.jsonl'),('offline_verification_sha256','offline_verification.json'),('smoke_checks_sha256','smoke_checks.json')]:
    assert g2[field]==sha(Path(actual_g2['evidence_directory'])/file)==actual_g2['g2_evidence_sha256'][file]
pred=b['failed_predecessor_and_cost'];assert pred['predecessor_run_id']==auth['predecessor']['run_id']
for key,file in [('predecessor_events_sha256','execution_events.jsonl'),('predecessor_manifest_sha256','execution_manifest.json'),
                 ('predecessor_registry_sha256','unit_registry.json'),('predecessor_gate_receipt_sha256','g3_gate_receipt.json'),('predecessor_branches_sha256','branches.jsonl')]:
    assert pred[key]==sha(old/file)
assert sha(gate['source_contract_restart']['failure_audit_json_path'])==pred['failure_audit_sha256']
cost_path=repo/'agent-logs/2026-10-22T192507Z__CODEX__r19-g3-physical-cost-audit__3d1ccea7/cost_reconciliation.json'
assert pred['physical_cost_reconciliation_sha256']==sha(cost_path)
assert pred['cumulative_before_any_future_successor']==release['cumulative_start']
limits=b['future_protocol_limits_not_authorization']
assert limits['train_identities']==127 and limits['schedule_start_index']==0 and limits['attempt_cap']==120 and limits['eligible_state_cap']==60
assert limits['K_values']==[1,2,3,4,5] and limits['total_horizon']==50
assert limits['source_remaining_model_calls']==limits['source_remaining_environment_operations']==8999
assert limits['other_phase_model_caps']=={k:v for k,v in release['remaining_phase_caps']['model_calls'].items() if k!='source'}
assert limits['other_phase_environment_caps']=={k:v for k,v in release['remaining_phase_caps']['environment_operations'].items() if k!='source'}
assert limits['global_model_call_ceiling']==26988 and limits['global_environment_operation_ceiling']==41260
assert limits['quota_transfer'] is False and limits['automatic_retry'] is False and limits['max_successor_campaigns']==1
assert b['authorization_state']['launch_allowed_by_this_proposal'] is False
inventory={}
for inv,base in [(repo/'FILE_HASHES.sha256',repo),(proposal/'FILE_HASHES.sha256',proposal)]:
    count=0
    for line in inv.read_text().splitlines():
        digest,path=line.split('  ',1);assert sha(base/path)==digest;count+=1
    inventory[str(inv)]={'count':count,'status':'PASS'}
remote={}
for file in proposal.iterdir():
    if not file.is_file():continue
    result=subprocess.run(['git','-C',str(repo),'show',f'origin/main:{file.relative_to(repo)}'],capture_output=True)
    assert result.returncode==0 and result.stdout==file.read_bytes()
    remote[str(file.relative_to(repo))]=sha(file)

# Confirmed inconsistencies collected without changing the submitted proposal.
actual_supervisor=Path(gate['source_contract_restart']['supervisor_record_directory'])
wrong_supervisor=repo/'agent-logs/2026-10-22T105439Z__CODEX__r19-b1-g3-launch__ef2328f/supervisor_raw'
supervisor_evidence={}
for key,file in [('old_live_runner_log_sha256','runner.log'),('old_live_runner_exit_sha256','runner_exit.json'),('old_live_supervisor_status_sha256','supervisor_status.json')]:
    assert pred[key]==sha(wrong_supervisor/file)
    assert pred[key]!=sha(actual_supervisor/file)
    supervisor_evidence[key]={'submitted':pred[key],'submitted_matches_path':str(wrong_supervisor/file),
        'required_path':str(actual_supervisor/file),'required_sha256':sha(actual_supervisor/file)}
wrong_exit=load(wrong_supervisor/'runner_exit.json');right_exit=load(actual_supervisor/'runner_exit.json')
assert wrong_exit['run_id']=='a0de515d7e104101bf8157175ea3d995' and right_exit['run_id']==pred['predecessor_run_id']
supervisor_evidence['wrong_run']={key:wrong_exit.get(key) for key in ('run_id','implementation_sha','exit_code','events_sha256')}
supervisor_evidence['correct_run']={key:right_exit.get(key) for key in ('run_id','implementation_sha','exit_code','events_sha256')}
quotas=frozen['population']['eligible_targets_by_stratum']
assert quotas==auth['frozen_science']['eligible_quotas']=={'failure':30,'success_control':15,'random_control':15}
assert limits['fixed_quotas']!=quotas
runtime_domains={file:{'path':str(old/file),'raw_file_sha256':sha(old/file),'canonical_object_sha256':objsha(load(old/file))}
    for file in ('runtime_manifest.json','runtime_manifest_preload.json')}
assert fields['runtime_manifest_sha256']==runtime_domains['runtime_manifest_preload.json']['raw_file_sha256']
assert fields['runtime_manifest_sha256'] not in (runtime_domains['runtime_manifest.json']['raw_file_sha256'],runtime_domains['runtime_manifest.json']['canonical_object_sha256'])
correct_four={file:{'path':str(actual_supervisor/file),'raw_file_sha256':sha(actual_supervisor/file)}
    for file in ('runner.log','runner_exit.json','supervisor_status.json','launch_context.json')}
assert {file:record['raw_file_sha256'] for file,record in correct_four.items()}==auth['predecessor']['supervisor_record_sha256']
findings=[
 {'id':'LIVE-P01','severity':'MAJOR','blocks_exact_proposal_acceptance':True,'file':str(proposal/'bindings.json'),'line':76,
  'title':'Wrong failed-run supervisor identity','trigger':'Use failed_predecessor_and_cost old_live_* fields to authenticate named predecessor3d1ccea7.',
  'evidence':supervisor_evidence,'required_fix':'Bind all four authentic3d1ccea7 supervisor artifact paths/raw hashes and run identity; retain a0de historical import failure only as a distinct optional historical record.'},
 {'id':'LIVE-P02','severity':'MAJOR','blocks_exact_proposal_acceptance':True,'file':str(proposal/'bindings.json'),'line':94,
  'title':'Eligible quota categories do not match frozen protocol','trigger':'Interpret future_protocol_limits_not_authorization.fixed_quotas as scientific cohort quotas.',
  'submitted':limits['fixed_quotas'],'required':quotas,'protocol_path':str(root/'configs/experiments/r19_recovery_duration_v1.json'),
  'authorization_path':str(root/'configs/experiments/r19_b1_g3_source_contract_restart_authorization_v1.json'),
  'required_fix':'Use failure30/success_control15/random_control15; phase labels initial_attempt/recovery/suffix are not enrollment strata. Do not change actual frozen protocol or code.'},
 {'id':'LIVE-P03','severity':'MAJOR','blocks_exact_proposal_acceptance':True,'file':str(proposal/'bindings.json'),'line':48,
  'title':'Runtime preload file digest mislabeled as runtime manifest identity','trigger':'Resolve scientific_and_input_bindings.runtime_manifest_sha256 to historical runtime_manifest.json or canonical runtime identity.',
  'submitted':fields['runtime_manifest_sha256'],'actual_domains':runtime_domains,
  'frozen_runtime_preload_expectations_sha256':prior['runtime_preload_sha256'],
  'required_fix':'Bind explicit historical artifact path/raw-file hash/canonical-object hash and domain.6395... is historical runtime_manifest_preload.json raw hash;306a... is runtime_manifest.json raw hash;f4c6... canonical runtime identity.64eb... remains frozen preload expectations. Future live post-load runtime is not yet observed; do not label an old preload as it.'}
]
put('confirmed_findings.json',findings)
put('corrected_binding_requirements.json',{'status':'CORRECTION_REQUIREMENTS_ONLY_NOT_A_PASS_OR_CLEARANCE',
    'authentic_predecessor_run_id':right_exit['run_id'],'authentic_predecessor_supervisor':correct_four,
    'frozen_eligible_quotas':quotas,'historical_runtime_artifact_domains':runtime_domains,
    'frozen_preload_runtime_expectations_canonical_sha256':prior['runtime_preload_sha256'],
    'scientific_calls_authorized':0,'new_preflight_authorized':False,'live_clearance':False})
put('raw_git_receipts.json',commands)
put('proposal_checks.json',{'proposal_raw_hashes':raw_expected,'canonical_hashes':canonical_expected,
    'hashes_and_remote_bytes':'PASS','live_child_equals_preflight_with_only_authorized_proposed_edits':True,
    'supervisor_argv_and_predecessor_option':'PASS','environment_static_set_unset_matches_actual_preflight':'PASS',
    'source_clean_detached_exact_sha_and_remote':'PASS','frozen_research_branch_unchanged':'PASS',
    'output_and_record_and_record_parent_absent':True,'remaining_caps_and_other_limits_except_quota_categories':'PASS',
    'old_g2_five_hashes_and_execution_identity':'PASS','preflight_review_gate_adjudication_actual_hashes':'PASS',
    'predecessor_event_manifest_registry_branch_and_gate_bytes':'PASS','historical_cumulative_cost_unchanged':'177 generations/342 operations',
    'inventories':inventory,'verified_remote_bytes':remote,
    'reviewer_scientific_or_preflight_invocations':0,'model_files_rehash_repeated':False,
    'prior_independent_input_runtime_check':'PASS immutable prior preflight verification; no code/input edits in this task; final drift check required before any future authorized launch.'})
(out/'submitted-proposal').mkdir()
for name in raw_expected:shutil.copyfile(proposal/name,out/'submitted-proposal'/name)
review={'schema_version':'r19_independent_exact_live_proposal_review_v1','status':'FAIL_EXACT_PROPOSAL_BINDINGS',
    'reviewed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'Sol',
    'reviewer_task':'01a0994c-a209-7600-8a3e-5ff3096ed346','implementation_sha':source,
    'proposal_path':str(proposal/'R19_LIVE_SUCCESSOR_PROPOSAL.md'),'proposal_sha256':raw_expected['R19_LIVE_SUCCESSOR_PROPOSAL.md'],
    'bindings_path':str(proposal/'bindings.json'),'bindings_sha256':raw_expected['bindings.json'],
    'EXACT_LIVE_PROPOSAL_REVIEW':'FAIL','IMPLEMENTATION_REVIEW':'PASS_UNCHANGED_EXACT_2da980f',
    'G2_CARRY_FORWARD':'PASS_AUTHENTIC_92aae1d_UNCHANGED','ACTUAL_PRODUCTION_PREFLIGHT':'PASS_UNCHANGED_a9ca70cb',
    'findings':findings,'scientific_code_change_required':False,'preflight_rerun_required':False,
    'source_treatment_semantics_changed':False,'scientific_execution_behavior_changed':True,
    'cumulative_actual':release['cumulative_start'],'remaining_phase_caps':release['remaining_phase_caps'],
    'global_ceilings':release['global_ceilings'],'known_failed_unit':'Preserved incomplete; separate independent append-only adjudication accepted.',
    'observed_provenance_main':head,'new_scientific_calls':0,'new_supervisor_or_preflight_calls':0,
    'LIVE_LAUNCH_CLEARANCE':'NOT_GRANTED','fresh_explicit_user_scientific_authorization':'NOT_GRANTED',
    'next_step':'Luna publishes a new immutable proposal revision fixing only three evidenced bindings, superseding old proposal. No source/gate/input/evidence edits, preflight rerun, model, ALFWorld, live or G4. Sol reviews new exact bytes before any clearance/user science authorization.'}
put('exact_proposal_review.json',review)
shutil.copyfile(__file__,out/'review_exact_proposal_read_only.py')
print(json.dumps({'status':review['status'],'findings':[f['id'] for f in findings],'all_other_checked_proposal_axes':'PASS',
    'implementation_and_actual_preflight_remain_PASS':True,'LIVE_LAUNCH_CLEARANCE':'NOT_GRANTED','task':str(out)},indent=2))
