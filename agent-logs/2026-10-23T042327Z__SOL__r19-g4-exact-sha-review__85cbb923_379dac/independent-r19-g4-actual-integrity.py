import pathlib,json,hashlib,sys,subprocess,datetime,traceback
p=pathlib.Path(pathlib.Path('/tmp/r19-g4-independent-review-path.txt').read_text().strip());root=pathlib.Path('/tmp/r19-g4-independent-review-85cbb923');repo=pathlib.Path('/home/lizening/research-notes');executed=pathlib.Path('/home/lizening/wt-r19-recovery-duration-v1');out=executed/'artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z';sup=repo/'agent-logs/2026-10-23T002200Z__LUNA__r19-g3-live-successor__2da980f/supervisor_live';assignment=repo/'agent-logs/2026-10-23T035119Z__SOL__r19-g4-minimal-contract-repair-assignment__9c5a99'
def sha(f):return hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest()
def load(f):return json.loads(pathlib.Path(f).read_text())
def git(where,*args):return subprocess.check_output(['git','-C',str(where),*args],text=True).strip()
assert git(root,'rev-parse','HEAD')=='85cbb92395e5e2420c2adeb1fa0634653e742910';assert not git(root,'status','--porcelain');assert git(executed,'rev-parse','HEAD')=='2da980f631badc25086d12db60d128ff507d3ae6'
expected=load(assignment/'observed_state_and_evidence_bindings.json')['exact_byte_sha256'];paths=set(map(pathlib.Path,expected))|set(x for x in out.rglob('*') if x.is_file())|set(x for x in sup.rglob('*') if x.is_file())
paths|=set((root/'configs/experiments').glob('r19*.json'))|set((root/'configs/experiments/r19_preflight_v3').glob('*.json'))|{root/'R19_PROTOCOL.md'}
launch=load(sup/'launch_context.json');argv=launch['command_argv']
paths|={pathlib.Path(argv[argv.index(k)+1]) for k in ('--protocol','--manifest','--config')}
old=load(root/'configs/experiments/r19_b1_g3_source_contract_restart_authorization_v1.json')['predecessor'];oldout=executed/old['output_relative_path'];paths|=set(x for x in oldout.rglob('*') if x.is_file())
pre={str(f):sha(f) for f in sorted(paths)};assert all(pre[k]==v for k,v in expected.items())
(p/'evidence'/'actual_independent.pre_hashes.json').write_text(json.dumps(pre,indent=2)+'\n')
sys.path[:0]=[str(root),str(root/'src')]
from scripts import analyze_r19_recovery_duration as a
from recovery import r19_duration as d
assert pathlib.Path(a.__file__).resolve()==root/'scripts/analyze_r19_recovery_duration.py';assert pathlib.Path(d.__file__).resolve()==root/'src/recovery/r19_duration.py';assert a.PROJECT_ROOT==root
visited=set();forbidden=[]
def profile(frame,event,arg):
 if event=='call' and pathlib.Path(frame.f_code.co_filename) in (pathlib.Path(a.__file__),pathlib.Path(d.__file__)):
  name=frame.f_code.co_name;visited.add(name)
  if name in ('main','render_report','analyze_duration_branches','paired_metrics'):
   forbidden.append(name);raise AssertionError('unauthorized scientific report/statistics call: '+name)
sys.setprofile(profile)
checks={}
def check(n,fn):
 value=fn();checks[n]={'status':'PASS_PRODUCTION_INTEGRITY_ONLY','result':value};print(n,'RETURNED',flush=True);return value
events=a._read_jsonl(out/'execution_events.jsonl');branches=a._read_jsonl(out/'branches.jsonl')
physical=check('validate_event_ledger',lambda:a.validate_event_ledger(events,expected_evidence_class='live'))
b=check('validate_branch_evidence',lambda:a.validate_branch_evidence(branches,events,return_operation_ids=True));operation_ids=b.pop('_operation_event_ids')
schedule=root/'configs/experiments/r19_preflight_v3/source_schedule.json';exclusions=root/'configs/experiments/r19_preflight_v3/exclusion_manifest.json';protocol=root/'configs/experiments/r19_recovery_duration_v1.json'
check('validate_live_source_schedule',lambda:a.validate_live_source_schedule(load(schedule),load(exclusions),events,operation_ids,physical))
check('validate_live_execution_provenance',lambda:a.validate_live_execution_provenance(execution_manifest=load(out/'execution_manifest.json'),runtime_manifest=load(out/'runtime_manifest.json'),environment_manifest=load(out/'environment_manifest.json'),schedule_path=schedule,exclusion_path=exclusions,protocol_path=protocol,events_path=out/'execution_events.jsonl',branches_path=out/'branches.jsonl',g3_gate_receipt_path=out/'g3_gate_receipt.json',events=events,physical=physical))
check('validate_live_exit_receipt',lambda:a.validate_live_exit_receipt(load(sup/'runner_exit.json'),events=events,protocol_sha256=sha(protocol),events_path=out/'execution_events.jsonl',branches_path=out/'branches.jsonl',receipt_path=sup/'runner_exit.json',supervisor_status_path=sup/'supervisor_status.json',runner_log_path=sup/'runner.log'))
sys.setprofile(None)
post={str(f):sha(f) for f in sorted(paths)};assert pre==post;assert not forbidden
assert checks['validate_live_execution_provenance']['result']['implementation_sha']=='2da980f631badc25086d12db60d128ff507d3ae6'
assert checks['validate_live_exit_receipt']['result']['start_proof']=='supervisor_launch_context'
assert physical['completed_physical_model_generations']==4965 and physical['physical_environment_operations']==7273 and physical['physical_environment_resets']==334 and physical['incomplete_operations']==0
(p/'evidence'/'actual_independent.post_hashes.json').write_text(json.dumps(post,indent=2)+'\n')
record={'status':'PASS_ALL_FIVE_INDEPENDENT_PRODUCTION_INTEGRITY_VALIDATORS_ON_UNCHANGED_GENUINE_G3','observed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'analyzer_source_sha':git(root,'rev-parse','HEAD'),'executed_G3_sha':git(executed,'rev-parse','HEAD'),'executed_G3_run_id':'260422ac02bd42a8b2929d7ef240526b','module_origins':{'analyzer':a.__file__,'duration':d.__file__},'analyzer_raw_sha256':sha(a.__file__),'original_hash_count':len(pre),'original_pre_post_equal':True,'checks':checks,'profile_observed_analyzer_duration_functions':sorted(visited),'forbidden_actual_data_main_statistics_renderer_calls':forbidden,'model_environment_calls':0,'formal_G4_executed':False,'evidence_or_production_code_modified':False}
(p/'evidence'/'actual_independent.json').write_text(json.dumps(record,indent=2)+'\n');print('ALL_FIVE_PASS_ORIGINALS_UNCHANGED_NO_REPORT',len(pre),flush=True)
