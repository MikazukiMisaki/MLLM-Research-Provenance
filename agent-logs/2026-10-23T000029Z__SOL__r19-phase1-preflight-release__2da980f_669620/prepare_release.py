import datetime, hashlib, json, os, re, shutil, subprocess
from pathlib import Path

task = Path('/tmp/r19-phase1-release-path.txt').read_text().strip()
out = Path(task)
repo = Path('/home/lizening/research-notes')
execution = Path('/home/lizening/wt-r19-recovery-duration-v1')
candidate = Path('/home/lizening/wt-r19-source-contract-review-fixes')
exact = '2da980f631badc25086d12db60d128ff507d3ae6'
old = 'da7d348ffd3677d619dd31357e1e1e3cca28c9ec'
review_dir = repo/'agent-logs/2026-10-22T234140Z__SOL__r19-exact-sha-independent-review__2da980f_198732'
proposal_dir = repo/'agent-logs/2026-10-22T235413Z__CODEX__r19-phase1-preparation__2da980f'
proposal_path = proposal_dir/'R19_PHASE1_PREPARATION_PROPOSAL.md'
review_path = review_dir/'independent_review.json'
adjudication_path = review_dir/'known_failed_adjudication.json'
review_sha = '85a694f24da347dcb0e6f09f4fe0d33afefb46abf1d5b0063361870c3fe7820b'
adjudication_sha = '3abea8efc2bd9d88677d71031aef0a21e905e6dd7b3ed75d06f1486d4c6718e0'
proposal_sha = '7bcdcff209bbf462d8aced19efef0b2c74352f9129e779f35272a04cf72fbc2c'
onboarding_sha = '27be0ca4c3e5abffa4fa492aaf47bf087328f41718fcc5f774c43fdf5b1c4e7e'
supervisor_old = repo/'agent-logs/2026-10-22T190221Z__CODEX__r19-g3-cli-preflight__bf31f3da/live_supervisor'
audit = repo/'agent-logs/2026-10-22T191409Z__ASTRA__r19-g3-failure-audit__3d1ccea7/failure_audit.json'

def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def canon(value): return json.dumps(value,ensure_ascii=True,sort_keys=True,separators=(',',':'))
def objsha(value): return hashlib.sha256(canon(value).encode()).hexdigest()
def write(name,value):
    path=out/name
    assert not path.exists(),str(path)
    path.write_text(json.dumps(value,ensure_ascii=True,sort_keys=True,indent=2)+'\n')
    return digest(path)
commands=[]
def git(root,*args):
    command=['git','-C',str(root),*args]
    proc=subprocess.run(command,text=True,capture_output=True)
    commands.append({'argv':command,'returncode':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr})
    assert proc.returncode==0,commands[-1]
    return proc.stdout.strip()

for path,sha in ((review_path,review_sha),(adjudication_path,adjudication_sha),(proposal_path,proposal_sha),
                 (execution/'R19_IMPLEMENTATION_ONBOARDING.md',onboarding_sha),
                 (proposal_dir/'preserved/R19_IMPLEMENTATION_ONBOARDING.md',onboarding_sha)):
    assert digest(path)==sha,str(path)
review=json.loads(review_path.read_text())
assert review['status']=='PASS' and review['IMPLEMENTATION_REVIEW']=='PASS' and review['G2_CARRY_FORWARD']=='PASS'
assert review['implementation_sha']==exact
assert git(candidate,'rev-parse','HEAD')==exact
assert git(candidate,'branch','--show-current')=='codex/r19-source-contract-review-fixes'
assert git(candidate,'status','--porcelain')==''
assert git(candidate,'ls-remote','origin','refs/heads/codex/r19-source-contract-review-fixes').split()[0]==exact
assert git(execution,'rev-parse','HEAD')==old
assert git(execution,'branch','--show-current')=='codex/r19-source-contract-repair'
assert git(execution,'status','--porcelain')=='?? R19_IMPLEMENTATION_ONBOARDING.md'
assert git(execution,'ls-remote','origin','refs/heads/codex/r19-source-contract-repair').split()[0]==old
assert git(repo,'diff','--name-only')==''
assert git(repo,'diff','--cached','--name-only')==''
provenance_head=git(repo,'rev-parse','HEAD')
assert git(repo,'ls-remote','origin','refs/heads/main').split()[0]==provenance_head

auth_path=candidate/'configs/experiments/r19_b1_g3_authorization_v1.json'
auth=json.loads(auth_path.read_text())
restart_path=candidate/'configs/experiments/r19_b1_g3_source_contract_restart_authorization_v1.json'
restart=json.loads(restart_path.read_text())
assert digest(auth_path)==review['g3_authorization_sha256']
assert digest(restart_path)==review['source_contract_restart_authorization_sha256']
old_local=json.loads((execution/'configs/local/r19_b1_g3_gate_bf31f3.json').read_text())
base_keys=['implementation_sha','protocol_sha256','baseline_manifest_sha256','baseline_amendment_sha256',
    'runtime_expectations_sha256','runtime_manifest_preload_sha256','g3_authorization_sha256',
    'entrypoint_repair_authorization_sha256','source_schedule_sha256','exclusion_manifest_sha256']
gate={'schema_version':'r19_gate_manifest_v1',**{key:review[key] for key in base_keys},
      'source_schedule_path':str(execution/'configs/experiments/r19_preflight_v3/source_schedule.json'),
      'exclusion_manifest_path':str(execution/'configs/experiments/r19_preflight_v3/exclusion_manifest.json')}
review_keys=list(old_local['review'])
review_keys.remove('artifact_path');review_keys.remove('artifact_sha256')
review_keys+=['source_treatment_semantics_changed','source_runtime_bugfix_enabled_intended_execution',
    'source_contract_restart_authorization_sha256','source_contract_repair_amendment_sha256',
    'source_restart_predecessor_run_id','source_restart_unit_resolution_event_sha256',
    'source_restart_expected_snapshot_sha256','source_restart_remaining_phase_caps_sha256',
    'source_restart_failure_disposition','first_source_episode_integration','first_source_restart_comparison']
gate['review']={key:review[key] for key in review_keys}
gate['review'].update(artifact_path=str(review_path),artifact_sha256=review_sha)
g2=auth['g2_carry_forward']
carry={'status':'PASS','g3_authorization_sha256':review['g3_authorization_sha256'],
       'entrypoint_repair_authorization_sha256':review['entrypoint_repair_authorization_sha256'],
       'g2_executed_implementation_sha':g2['g2_executed_implementation_sha'],'g2_run_id':g2['g2_run_id'],
       'g2_evidence_carried_forward':True,'new_g2_run_performed':False,
       'g3_launch_implementation_sha':exact,'review_artifact_sha256':review_sha,
       'old_g2_review_sha256':g2['g2_review_sha256'],
       'old_g2_gate_manifest_sha256':g2['g2_gate_manifest_sha256'],
       'g2_evidence_sha256':g2['evidence_file_sha256']}
for key in ('evidence_directory','failed_predecessor_directory','unit_resolution_event_path',
            'old_g2_review_path','old_g2_gate_manifest_path'):
    carry[key]=old_local['g2_carry_forward'][key]
for key in ('source_contract_restart_authorization_sha256','source_contract_repair_amendment_sha256',
            'source_restart_predecessor_run_id','source_restart_unit_resolution_event_sha256',
            'source_restart_expected_snapshot_sha256'):
    carry[key]=review[key]
gate['g2_carry_forward']=carry
gate['source_contract_restart']={
    'amendment_sha256':review['source_contract_repair_amendment_sha256'],
    'authorization_sha256':review['source_contract_restart_authorization_sha256'],
    'unit_resolution_event_sha256':review['source_restart_unit_resolution_event_sha256'],
    'supervisor_record_directory':str(supervisor_old),'failure_audit_json_path':str(audit)}
protected={}
def protect(path,expected):
    assert digest(path)==expected,str(path)
    protected[str(path)]=expected
for name,expected in g2['evidence_file_sha256'].items():protect(Path(carry['evidence_directory'])/name,expected)
protect(carry['old_g2_review_path'],carry['old_g2_review_sha256'])
protect(carry['old_g2_gate_manifest_path'],carry['old_g2_gate_manifest_sha256'])
predecessor=restart['predecessor']; old_output=execution/predecessor['output_relative_path']
for name,field in [('execution_events.jsonl','event_ledger_sha256'),('execution_manifest.json','execution_manifest_sha256'),
                   ('unit_registry.json','unit_registry_sha256'),('branches.jsonl','branch_ledger_sha256')]:
    protect(old_output/name,predecessor[field])
for name,expected in predecessor['supervisor_record_sha256'].items():protect(supervisor_old/name,expected)
protect(audit,predecessor['failure_audit_sha256'])
for key,file in [('source_contract_repair_amendment_sha256','r19_b1_g3_source_contract_repair_amendment_v1.json'),
                 ('source_contract_restart_authorization_sha256','r19_b1_g3_source_contract_restart_authorization_v1.json'),
                 ('source_restart_unit_resolution_event_sha256','r19_b1_g3_source_unit_resolution_events_v1.jsonl')]:
    protect(candidate/'configs/experiments'/file,review[key])
protect(gate['source_schedule_path'],gate['source_schedule_sha256'])
protect(gate['exclusion_manifest_path'],gate['exclusion_manifest_sha256'])
gate_sha=write('reviewed_phase1_gate.json',gate)

text=proposal_path.read_text()
blocks=re.findall(r'```text\n(.*?)\n```',text,re.S)
assert len(blocks)==2
supervisor_argv=blocks[0].splitlines()
child_argv=supervisor_argv[supervisor_argv.index('--')+1:]
assert objsha(supervisor_argv)=='7c1519ccb6f34683ee1ac09d4757d8a00bc225576b6a4f8370736790a2b9235b'
assert objsha(child_argv)=='eea6b0032ca714ec011b3d48f9c6a1a1bec3879560910ae77ce3da1c924aaa68'
new_gate=Path(child_argv[child_argv.index('--manifest')+1])
new_record=Path(supervisor_argv[supervisor_argv.index('--record-dir')+1])
new_output=Path(child_argv[child_argv.index('--output')+1])
archive=proposal_dir/'preserved/R19_IMPLEMENTATION_ONBOARDING.execution-original.md'
for path in (new_gate,new_record,new_output,archive):assert not os.path.lexists(path),str(path)
write('supervisor_argv.json',supervisor_argv);write('child_argv.json',child_argv)
previous_context=json.loads((supervisor_old/'launch_context.json').read_text())
values=previous_context['effective_environment']
set_keys=('CONDA_PREFIX','PATH','ALFWORLD_DATA','ALFWORLD_CONFIG_PATH','HF_HUB_CACHE','HF_HUB_OFFLINE','TRANSFORMERS_OFFLINE')
env_set={key:values[key] for key in set_keys}
assert env_set['PATH']==blocks[1]
assert env_set['ALFWORLD_CONFIG_PATH']==str(execution/'configs/local/r19_b1_g2_alfworld.yaml')
for key in ('PATH','CONDA_PREFIX','ALFWORLD_DATA','ALFWORLD_CONFIG_PATH','HF_HUB_CACHE','HF_HUB_OFFLINE','TRANSFORMERS_OFFLINE'):
    assert values[key] in text,(key,values[key])
env_unset=['PYTHONPATH','PYTHONHOME','VIRTUAL_ENV','HF_HOME','CUDA_VISIBLE_DEVICES','CUDA_HOME',
           'R19_RUN_ID','R19_EVIDENCE_CLASS','R19_EXIT_RECEIPT_PATH','R19_SUPERVISOR_CONTEXT_PATH']
environment={'set':env_set,'unset':env_unset,
             'supervisor_injected':{'R19_RUN_ID':'NEW_SUPERVISOR_UUID','R19_EVIDENCE_CLASS':'preflight_only',
                 'R19_EXIT_RECEIPT_PATH':str(new_record/'runner_exit.json'),
                 'R19_SUPERVISOR_CONTEXT_PATH':str(new_record/'launch_context.json')}}
env_sha=write('environment_set_unset.json',environment)
resolvers={key:shutil.which(key,path=env_set['PATH']) for key in ('git','nvidia-smi')}
assert all(resolvers.values()),resolvers

active=[]
for proc in Path('/proc').iterdir():
    if not proc.name.isdigit():continue
    try:
        args=(proc/'cmdline').read_bytes().split(b'\0')
        args=[arg.decode(errors='replace') for arg in args if arg]
        if not args:continue
        exe=Path(args[0]).name
        if ('python' in exe or exe in ('uv','torchrun')) and any(
            Path(arg).name in ('launch_r19_supervised.py','run_r19_recovery_duration.py','run_r19_experiment.py')
            for arg in args[1:]):active.append({'pid':int(proc.name),'argv':args})
    except (OSError,PermissionError):pass
assert not active,active
gpu=subprocess.run(['nvidia-smi','--query-compute-apps=pid,process_name,used_gpu_memory','--format=csv,noheader'],text=True,capture_output=True)
assert gpu.returncode==0,(gpu.returncode,gpu.stderr)
assert not gpu.stdout.strip(),gpu.stdout
state={'observed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'execution_head':old,'execution_branch':'codex/r19-source-contract-repair',
       'execution_status':'?? R19_IMPLEMENTATION_ONBOARDING.md','candidate_head':exact,
       'candidate_clean':True,'both_remote_refs_match':True,'provenance_start_head':provenance_head,
       'review_sha256':review_sha,'adjudication_sha256':adjudication_sha,'proposal_sha256':proposal_sha,
       'onboarding_sha256':onboarding_sha,'onboarding_original_mode':oct((execution/'R19_IMPLEMENTATION_ONBOARDING.md').stat().st_mode&0o777),
       'absent_paths':[str(path) for path in (new_gate,new_record,new_output,archive)],
       'active_r19_processes':active,'nvidia_compute_process_query':{'returncode':gpu.returncode,'stdout':gpu.stdout,'stderr':gpu.stderr},
       'reviewed_PATH_resolution':resolvers,
       'historical_cost':{'model_generations':177,'environment_operations_including_resets':342,
           'non_reset_environment_operations':330,'resets':12,'incomplete_external_operations':0},
       'protected_files':protected,'gate_validation_performed':'STATIC_BINDING_AND_FILE_HASH_VERIFICATION_ONLY; real production CLI remains NOT_RUN'}
write('release_time_state_and_hash_checks.json',state)
write('read_only_command_receipts.json',commands)
runtime=json.loads((out/'input_runtime_verification.json').read_text())
assert runtime['status']=='PASS_READ_ONLY_PRODUCTION_INPUT_AND_RUNTIME_HASH_CHECK'
assert runtime['runtime_preload_sha256']==review['runtime_manifest_preload_sha256']
assert runtime['source_identities']==127 and runtime['snapshot_file_count']==12 and runtime['adapter_file_count']==11
release={'schema_version':'r19_phase1_zero_science_preflight_release_v1','status':'RELEASED_FOR_ONE_PREFLIGHT_ONLY',
    'issued_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'reviewer':'Sol','reviewer_task':'01a0994c-a209-7600-8a3e-5ff3096ed346',
    'operator':'Luna Excution','operator_task':'01a09fcb-ab5f-7b83-9acf-91026145b764',
    'implementation_sha':exact,'base_scientific_sha':'bf31f3da430ffc35bd17fc380e1752adce6d1467',
    'scientific_execution_authorized':False,'LIVE_LAUNCH_CLEARANCE':'NOT_GRANTED',
    'fresh_user_scientific_authorization':'NOT_GRANTED_BY_THIS_RELEASE',
    'maximum_supervised_preflight_invocations':1,'maximum_live_launches':0,'automatic_retry':False,
    'maximum_model_objects_loaded':0,'maximum_model_generations':0,'maximum_alfworld_constructions':0,
    'maximum_environment_resets':0,'maximum_environment_steps':0,'maximum_scientific_units':0,
    'evidence_class':'preflight_only','predecessor_run_id':predecessor['run_id'],
    'prior_live_clearance':'CONSUMED; NOT_REUSABLE','cumulative_start':state['historical_cost'],
    'remaining_phase_caps':review['remaining_phase_caps'],'global_ceilings':review['global_ceilings'],
    'review':{'path':str(review_path),'sha256':review_sha},
    'adjudication':{'path':str(adjudication_path),'sha256':adjudication_sha},
    'proposal':{'path':str(proposal_path),'sha256':proposal_sha},
    'gate':{'reviewed_bytes_path':str(out/'reviewed_phase1_gate.json'),'destination':str(new_gate),'sha256':gate_sha,
            'copy_rule':'Create exclusively from reviewed bytes; stop if destination already exists. Never edit old gates.'},
    'argv':{'supervisor_path':str(out/'supervisor_argv.json'),'supervisor_canonical_sha256':objsha(supervisor_argv),
            'child_path':str(out/'child_argv.json'),'child_canonical_sha256':objsha(child_argv)},
    'environment':{'path':str(out/'environment_set_unset.json'),'file_sha256':env_sha,
            'canonical_sha256':objsha(environment),'recorded_effective_environment_canonical_sha256':objsha(env_set),
            'prior_proposal_digest':'6f9462a0234a24fb6967946b165bd99db54641c926de88cd0bac33580b702516',
            'prior_proposal_digest_verification':'UNVERIFIED: canonical input object not supplied; this explicit file supersedes only the ambiguous digest representation, preserves proposed runtime values.',
            'apply_rule':'Apply set and remove unset before absolute supervisor invocation; do not preset injected fields; compare recorded effective allowlist to set exactly.'},
    'read_only_inputs':{'path':str(out/'input_runtime_verification.json'),'sha256':digest(out/'input_runtime_verification.json'),
            'runtime_preload_sha256':review['runtime_manifest_preload_sha256']},
    'execution_cwd':str(execution),'supervisor_record_directory':str(new_record),
    'preflight_receipt_path':str(new_record/'pilot_preflight_receipt.json'),
    'scientific_output_sentinel':str(new_output),'scientific_output_must_remain_absent':True,
    'preflight_result':'NOT_RUN',
    'staging':{'authorized':True,'initial_branch':'codex/r19-source-contract-repair','initial_sha':old,
        'target':'detached exact implementation SHA','onboarding_source':str(execution/'R19_IMPLEMENTATION_ONBOARDING.md'),
        'verified_copy':str(proposal_dir/'preserved/R19_IMPLEMENTATION_ONBOARDING.md'),
        'move_original_exclusively_to':str(archive),'onboarding_sha256':onboarding_sha,'onboarding_mode':'0644',
        'restore_on_stop_or_failure':'After authentic child/supervisor exit and evidence preservation, restore original branch/HEAD and onboarding bytes/mode, without reset/clean/ignore changes. Stop/report restoration conflict.',
        'on_pass':'Keep clean exact reviewed detached checkout pending independent receipt review. No live execution.'},
    'stop_rules':['Any source/ref/hash/runtime/input/cwd/environment drift or concurrent R19/GPU process',
        'Any already-existing gate, supervisor record directory, output sentinel or move-destination',
        'Any staging/preflight failure, mismatch, timeout or interruption; preserve evidence and report, no retry',
        'Any model/environment/scientific side effect or nonzero counter',
        'Missing authentic subprocess exit, nonzero child exit, status other than PREFLIGHT_ONLY_PASS, or output sentinel created'],
    'return_evidence':['run_id and authentic launch_context.json, runner_exit.json, supervisor_status.json, runner.log, pilot_preflight_receipt.json with hashes',
        'exact HEAD/clean status, local gate hash, env omissions and effective allowlist, production module origins, frozen input/runtime/review bindings',
        'all zero-side-effect counters, output-sentinel absence, protected predecessor/G2 hashes unchanged, cumulative actual 177/342',
        'own finalized RECORD/hash inventory and coordinated provenance publication'],
    'next_dependency':'Independent review of actual positive preflight -> separate live launch clearance and fresh explicit user scientific authorization -> one bounded live successor -> genuine G3 -> G4'}
write('phase1_release.json',release)
shutil.copyfile('/tmp/r19-phase1-input-check.py',out/'read_only_input_check.py')
shutil.copyfile(__file__,out/'prepare_release.py')
print(json.dumps({'task_dir':str(out),'release_sha256':digest(out/'phase1_release.json'),'gate_sha256':gate_sha,
                  'environment_file_sha256':env_sha,'environment_canonical_sha256':objsha(environment),
                  'status':release['status'],'preflight_result':'NOT_RUN','LIVE_LAUNCH_CLEARANCE':'NOT_GRANTED'},indent=2))
