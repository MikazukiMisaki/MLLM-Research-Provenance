import ast,datetime,hashlib,json,os,shutil,subprocess,sys
from pathlib import Path

p=Path(Path('/tmp/r19-phase1-verification-path.txt').read_text().strip())
repo=Path('/home/lizening/research-notes')
release_dir=repo/'agent-logs/2026-10-23T000029Z__SOL__r19-phase1-preflight-release__2da980f_669620'
luna=repo/'agent-logs/2026-10-22T235413Z__CODEX__r19-phase1-preparation__2da980f'
root=Path('/home/lizening/wt-r19-recovery-duration-v1')
source='2da980f631badc25086d12db60d128ff507d3ae6'
expected_run='a9ca70cb082b4f2387d242664031b0bc'
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def objsha(value):return hashlib.sha256(json.dumps(value,ensure_ascii=True,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def put(name,value):(p/name).write_text(json.dumps(value,ensure_ascii=True,indent=2,sort_keys=True)+'\n')
commands=[]
def git(path,*args):
    proc=subprocess.run(['git','-C',str(path),*args],capture_output=True,text=True)
    commands.append({'argv':['git','-C',str(path),*args],'exit_code':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr})
    assert proc.returncode==0,commands[-1]
    return proc.stdout.strip()
assert git(root,'rev-parse','HEAD')==source
assert git(root,'branch','--show-current')==''
assert git(root,'status','--porcelain')==''
assert git(root,'ls-remote','origin','refs/heads/codex/r19-source-contract-review-fixes').split()[0]==source
head=git(repo,'rev-parse','HEAD')
assert head=='4f870c885d87ab4e8e049a4569a4a10c2d5970f3'
assert git(repo,'ls-remote','origin','refs/heads/main').split()[0]==head
assert git(repo,'rev-parse','origin/main')==head
assert git(repo,'diff','--name-only')=='' and git(repo,'diff','--cached','--name-only')==''
release_path=release_dir/'phase1_release.json'
assert sha(release_path)=='d634514f0d177ff7b6b2712dd160fa0d1c86ba193e3e377260c5bc872e27ae46'
release=json.loads(release_path.read_text())
assert sha(release['review']['path'])==release['review']['sha256']
assert sha(release['adjudication']['path'])==release['adjudication']['sha256']
assert sha(release['gate']['destination'])==release['gate']['sha256']
assert sha(release['gate']['reviewed_bytes_path'])==release['gate']['sha256']
assert Path(release['gate']['destination']).read_bytes()==Path(release['gate']['reviewed_bytes_path']).read_bytes()
gate=json.loads(Path(release['gate']['destination']).read_text())
assert gate['review']['artifact_path']==release['review']['path']
assert gate['review']['artifact_sha256']==release['review']['sha256']
supervisor=luna/'preflight_supervisor'
expected={'runner.log':'9652604e8e033ea62fac1436f5bd9f4d1a6528ab2a8e8326b431b3a8db81f392',
    'runner_exit.json':'7323984be1fbac09a88586feeda2e98a4ab13be1c72110ec5fb2e22bce46af6c',
    'supervisor_status.json':'9ae5417d129178a64cc21c5ba50f38f1a3df037ba1231e866964c8ba391308de',
    'launch_context.json':'aa6bf1f1dc18ec7d0c52c1b9afa069973ca9304fdf917eab2241f0b75f21546a',
    'pilot_preflight_receipt.json':'aed33e7f813a7ce2992b7860fbef59cabe814e31543c3e8eb1dcac5b95390574'}
assert {name:sha(supervisor/name) for name in expected}==expected
c=json.loads((supervisor/'launch_context.json').read_text())
e=json.loads((supervisor/'runner_exit.json').read_text())
s=json.loads((supervisor/'supervisor_status.json').read_text())
r=json.loads((supervisor/'pilot_preflight_receipt.json').read_text())
child=json.loads((release_dir/'child_argv.json').read_text())
super_argv=json.loads((release_dir/'supervisor_argv.json').read_text())
for record in (c,e,s):
    assert record['command_argv']==child
    assert record['command_sha256']==objsha(child)==release['argv']['child_canonical_sha256']
    assert record['cwd']==str(root)
    assert record['evidence_class']=='preflight_only'
    assert record['supersedes_run_id']==release['predecessor_run_id']
    assert record['implementation_sha']==source
    assert record['run_id']==expected_run
assert c['supervisor_argv']==super_argv
assert objsha(c['supervisor_argv'])==release['argv']['supervisor_canonical_sha256']
assert c['supervisor_entrypoint']==str(root/'scripts/launch_r19_supervised.py')
assert c['supervisor_interpreter']==c['interpreter']==child[0]
assert e['exit_code_source']=='subprocess.returncode' and e['exit_code']==0
assert e['status']==s['status']=='completed' and s['exit_code']==0
assert e['interrupted_by_supervisor'] is False
assert (e['supervisor_pid'],e['child_pid'])==(776941,776946)
assert e['launch_context_sha256']==s['launch_context_sha256']==r['supervisor_context_sha256']==expected['launch_context.json']
assert e['runner_log_sha256']==s['runner_log_sha256']==expected['runner.log']
assert s['runner_exit_sha256']==expected['runner_exit.json']
assert e['events_sha256'] is None and e['branches_sha256'] is None and e['artifacts_complete'] is False
assert s['events_sha256'] is None and s['branches_sha256'] is None
assert json.loads((supervisor/'runner.log').read_text())==r
assert r['run_id']==expected_run and r['status']=='PREFLIGHT_ONLY_PASS'
assert r['implementation_sha']==source and r['gate_manifest_sha256']==release['gate']['sha256']
assert r['scheduled_train_tasks']==127 and r['g2_evidence_carried_forward'] is True and r['new_g2_run_performed'] is False
assert r['g2_executed_implementation_sha']=='92aae1d9b230cc212c6ec4effc99aa468941e69d'
effects={'model_objects_loaded','model_generations','environment_instances_constructed','environment_resets','environment_steps','scientific_units_created','fresh_train_attempts'}
assert set(r['scientific_side_effects'])==effects and all(type(v) is int and v==0 for v in r['scientific_side_effects'].values())
assert r['output_path_absent'] is True and not os.path.lexists(release['scientific_output_sentinel'])
assert not os.path.lexists(release['staging']['onboarding_source'])
for path in (release['staging']['verified_copy'],release['staging']['move_original_exclusively_to']):
    assert sha(path)==release['staging']['onboarding_sha256']
    assert Path(path).stat().st_mode&0o777==0o644
assert git(root,'check-ignore',release['gate']['destination'])==release['gate']['destination']
env=json.loads((release_dir/'environment_set_unset.json').read_text())
assert sha(release_dir/'environment_set_unset.json')==release['environment']['file_sha256']
assert c['effective_environment']==env['set']
assert objsha(c['effective_environment'])=='84a59e93bd64b751ec5e1baad246314776562158bdb46019a864d5dba52697c0'
assert objsha(c['effective_environment'])==release['environment']['recorded_effective_environment_canonical_sha256']
assert c['omitted_environment_key_presence']=={'PYTHONPATH':False,'PYTHONHOME':False,'VIRTUAL_ENV':False}
assert all(k not in c['effective_environment'] for k in ('HF_HOME','CUDA_VISIBLE_DEVICES','CUDA_HOME','PYTHONPATH','PYTHONHOME','VIRTUAL_ENV'))
assert r['production_module_origins']=={name:str(root/Path(name.replace('.','/')).with_suffix('.py')) for name in ('scripts.run_r19_experiment','scripts.analyze_r19_recovery_duration')}
for name,origin in r['production_module_origins'].items():
    rel=str(Path(origin).relative_to(root))
    original=subprocess.run(['git','-C',str(root),'show',f'{source}:{rel}'],capture_output=True)
    assert original.returncode==0 and original.stdout==Path(origin).read_bytes()

inventory_checks={}
for inv,base in ((repo/'FILE_HASHES.sha256',repo),(luna/'FILE_HASHES.sha256',luna)):
    count=0
    for line in inv.read_text().splitlines():
        digest,relative=line.split('  ',1)
        path=Path(relative) if Path(relative).is_absolute() else base/relative
        assert sha(path)==digest,str(path)
        count+=1
    inventory_checks[str(inv)]={'checked':count,'status':'PASS'}
remote_checks={}
paths=[*(supervisor/name for name in expected),luna/'RECORD.md',release_path,
       Path(release['review']['path']),Path(release['adjudication']['path']),Path(release['gate']['reviewed_bytes_path']),repo/'FILE_HASHES.sha256',repo/'INDEX.md']
for path in paths:
    rel=str(path.relative_to(repo))
    z=subprocess.run(['git','-C',str(repo),'show',f'origin/main:{rel}'],capture_output=True)
    assert z.returncode==0 and z.stdout==path.read_bytes(),rel
    remote_checks[rel]=sha(path)

# Only read-only production validators below; no run_live_experiment, CLI,
# supervisor, model constructor, ALFWorld or monkeypatch is invoked.
sys.path[:0]=[str(root),str(root/'src')]
from scripts import run_r19_experiment as production
from scripts import analyze_r19_recovery_duration as analyzer
assert production.PROJECT_ROOT==root and Path(production.__file__).resolve()==root/'scripts/run_r19_experiment.py'
assert Path(analyzer.__file__).resolve()==root/'scripts/analyze_r19_recovery_duration.py'
runtime=production._runtime_manifest(data_root=Path('/home/lizening/alfworld_data'),config_path=Path(env['set']['ALFWORLD_CONFIG_PATH']))
identity=json.loads(production.R19_B1_BASELINE.read_text())
assert runtime==identity['runtime_expectations']['preload']
assert objsha(runtime)==gate['runtime_manifest_preload_sha256']
gate_result=production.validate_execution_gates(mode='pilot',protocol_path=production.R19_PROTOCOL,
    model_identity_path=production.R19_B1_BASELINE,gate_manifest_path=Path(release['gate']['destination']),
    output_path=Path(release['scientific_output_sentinel']),schedule_path=Path(gate['source_schedule_path']),
    exclusion_path=Path(gate['exclusion_manifest_path']),observed_runtime_manifest=runtime)
inputs=production._read_exact_local_inputs(mode='pilot',data_root=Path('/home/lizening/alfworld_data'),
    config_path=Path(env['set']['ALFWORLD_CONFIG_PATH']),adapter_path=Path(child[child.index('--adapter')+1]),
    schedule_path=Path(gate['source_schedule_path']),exclusion_path=Path(gate['exclusion_manifest_path']),
    protocol=json.loads(production.R19_PROTOCOL.read_text()),identity=identity)
assert objsha(inputs['model_bytes'])==r['model_files_sha256']
assert objsha(inputs['source_files'])==r['source_file_manifest_sha256']
assert inputs['adapter_sha256']==r['adapter_sha256']
assert inputs['model_bytes']['snapshot_revision']==r['model_revision']
for key in ('implementation_sha','protocol_sha256','source_schedule_sha256','exclusion_manifest_sha256',
            'g3_authorization_sha256','entrypoint_repair_authorization_sha256','source_contract_restart_authorization_sha256',
            'source_contract_repair_amendment_sha256','source_restart_predecessor_run_id',
            'source_restart_unit_resolution_event_sha256','source_restart_expected_snapshot_sha256',
            'source_restart_remaining_phase_caps'):
    assert gate_result[key]==r[key],key
assert gate_result['gate_manifest_sha256']==r['gate_manifest_sha256']
review=json.loads(Path(release['review']['path']).read_text())
assert r['source_restart_remaining_phase_caps']==review['remaining_phase_caps']==release['remaining_phase_caps']

prior_state=json.loads((release_dir/'release_time_state_and_hash_checks.json').read_text())
post_protected={}
for path,digest in prior_state['protected_files'].items():
    # Candidate-worktree files and original execution input paths remain untouched.
    assert sha(path)==digest,path
    post_protected[path]=digest
costs={}
directories={'g2_failed_predecessor':Path(gate['g2_carry_forward']['failed_predecessor_directory']),
    'g2_successful_smoke':Path(gate['g2_carry_forward']['evidence_directory'])}
restart=json.loads(production.R19_B1_G3_SOURCE_CONTRACT_RESTART_AUTHORIZATION.read_text())
directories['g3_failed_source']=root/restart['predecessor']['output_relative_path']
for label,directory in directories.items():
    ledger=directory/'execution_events.jsonl'
    events=[json.loads(line) for line in ledger.read_text().splitlines() if line.strip()]
    physical=analyzer.validate_event_ledger(events,expected_evidence_class='live')
    costs[label]={'ledger_path':str(ledger),'ledger_sha256':sha(ledger),'raw_production_validator':physical,
        'model_generations':physical['completed_physical_model_generations'],
        'non_reset_environment_operations':physical['physical_environment_operations'],
        'resets':physical['physical_environment_resets'],'incomplete_operations':physical['incomplete_operations']}
total={key:sum(v[key] for v in costs.values()) for key in ('model_generations','non_reset_environment_operations','resets','incomplete_operations')}
total['environment_operations_including_resets']=total['non_reset_environment_operations']+total['resets']
assert total=={'model_generations':177,'non_reset_environment_operations':330,'resets':12,'incomplete_operations':0,'environment_operations_including_resets':342}
manifest=json.loads((directories['g3_failed_source']/'execution_manifest.json').read_text())
registry=json.loads((directories['g3_failed_source']/'unit_registry.json').read_text())
assert manifest['status']=='RUNNING' and len(registry['units'])==1
assert next(iter(registry['units'].values()))['status']=='in_progress'
assert [x for x in (root/'artifacts/runtime').glob('r19_b1_g3_*')]==[directories['g3_failed_source']]
assert all(not Path(f'/proc/{pid}').exists() for pid in (e['supervisor_pid'],e['child_pid']))
active=[]
for proc in Path('/proc').iterdir():
    if not proc.name.isdigit():continue
    try:
        args=[v.decode(errors='replace') for v in (proc/'cmdline').read_bytes().split(b'\0') if v]
        if args and 'python' in Path(args[0]).name and any(Path(arg).name in ('launch_r19_supervised.py','run_r19_recovery_duration.py','run_r19_experiment.py') for arg in args[1:]):
            active.append({'pid':int(proc.name),'argv':args})
    except (OSError,PermissionError):pass
assert active==[],active
assert git(root,'rev-parse','HEAD')==source and git(root,'status','--porcelain')==''
put('raw_preflight_hashes.json',expected)
put('read_only_production_gate_result.json',gate_result)
put('current_runtime_preload.json',runtime)
put('physical_cost_reconciliation.json',{'per_ledger':costs,'total':total,'new_scientific_cost_this_task':0,'new_preflight_invocations_this_task':0})
put('protected_evidence_postcheck.json',post_protected)
put('raw_git_receipts.json',commands)
(p/'raw-preflight').mkdir()
for name in expected:shutil.copyfile(supervisor/name,p/'raw-preflight'/name)
source_text=(root/'scripts/run_r19_experiment.py').read_text();tree=ast.parse(source_text)
func=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='run_live_experiment')
preflight=next(x for x in func.body if isinstance(x,ast.If) and isinstance(x.test,ast.Name) and x.test.id=='preflight_only')
assert isinstance(preflight.body[-1],ast.Return)
later=[x for x in func.body if x.lineno>preflight.end_lineno]
mkdir_line=next(x.lineno for x in later if isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Attribute) and x.value.func.attr=='mkdir')
runtime_line=next(n.lineno for x in later for n in ast.walk(x) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='LiveR19Runtime')
summary={'status':'PASS_INDEPENDENT_EXACT_SHA_PRODUCTION_PREFLIGHT_VERIFICATION',
    'start_utc':started,'finish_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'implementation_sha':source,'run_id':expected_run,'authentic_child_exit':0,'authentic_exit_source':'subprocess.returncode',
    'supervisor_status':'completed','preflight_receipt_status':'PREFLIGHT_ONLY_PASS',
    'release_sha256':sha(release_path),'release_state':'CONSUMED_BY_THIS_ONE_PREFLIGHT; DO_NOT_REUSE',
    'gate_sha256':r['gate_manifest_sha256'],'review_sha256':release['review']['sha256'],
    'known_failed_adjudication_sha256':release['adjudication']['sha256'],
    'evidence_sha256':expected,'child_argv_canonical_sha256':objsha(child),'supervisor_argv_canonical_sha256':objsha(super_argv),
    'effective_environment_canonical_sha256':objsha(c['effective_environment']),
    'environment_exactly_matches_release':True,'python_override_variables_absent':True,
    'runtime_preload_sha256':objsha(runtime),'snapshot_file_count':len(inputs['model_bytes']['snapshot_file_sha256']),
    'adapter_file_count':len(inputs['model_bytes']['adapter_file_sha256']),'source_identity_count':len(inputs['source_files']),
    'model_files_sha256':objsha(inputs['model_bytes']),'source_file_manifest_sha256':objsha(inputs['source_files']),
    'read_only_production_gate_validation':'PASS_NO_MOCKS_OR_PROJECT_ROOT_OVERRIDE_IN_REAL_EXECUTION_CONTEXT',
    'preflight_early_return_code_evidence':{'source_file':str(root/'scripts/run_r19_experiment.py'),
        'source_file_sha256':sha(root/'scripts/run_r19_experiment.py'),'preflight_if_line':preflight.lineno,
        'preflight_return_line':preflight.body[-1].lineno,'later_output_mkdir_line':mkdir_line,'later_runtime_constructor_line':runtime_line,
        'interpretation':'Zero counters supported by reviewed preflight branch returning before scientific output/runtime construction. No OS-level syscall tracing claim.'},
    'scientific_side_effects':r['scientific_side_effects'],'output_sentinel_absent':True,
    'execution_clean_detached_head':source,'all_post_protected_hashes_match':True,
    'failed_source_registry_preserved':'in_progress','failed_source_manifest_preserved':'RUNNING',
    'known_failed_disposition':'Accepted independent append-only adjudication; source episode remains incomplete, not task success/failure.',
    'G2_CARRY_FORWARD':'PASS_AUTHENTIC_92aae1d_NO_RERUN','IMPLEMENTATION_REVIEW':'PASS_UNCHANGED_EXACT_2da980f',
    'source_treatment_semantics_changed':False,'scientific_execution_behavior_changed':True,
    'remaining_phase_caps':r['source_restart_remaining_phase_caps'],'cumulative_actual':total,
    'raw_inventory_checks':inventory_checks,'observed_provenance_main':head,'remote_bytes_verified':remote_checks,
    'active_r19_processes':active,'reviewer_new_preflight_or_live_invocations':0,
    'LIVE_LAUNCH_CLEARANCE':'NOT_GRANTED','scientific_execution_release':False,'fresh_explicit_user_science_authorization':'STILL_REQUIRED',
    'next_authorized_step':'Read-only preparation of a fresh unique live argv/output/record proposal only; no launch. Independent clearance and fresh explicit user science authorization required.'}
put('preflight_verification.json',summary)
shutil.copyfile(__file__,p/'verify_preflight_read_only.py')
print(json.dumps({key:summary[key] for key in ('status','run_id','authentic_child_exit','environment_exactly_matches_release','snapshot_file_count','adapter_file_count','source_identity_count','cumulative_actual','LIVE_LAUNCH_CLEARANCE')},indent=2),flush=True)
