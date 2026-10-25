from pathlib import Path
import subprocess,json,hashlib,datetime,uuid,os,ast
repo=Path('/home/lizening/research-notes');prep=repo/'agent-logs/2026-10-23T043602Z__LUNA__r19-g4-readiness__85cbb923';review=repo/'agent-logs/2026-10-23T042327Z__SOL__r19-g4-exact-sha-review__85cbb923_379dac';analyzer=Path('/home/lizening/wt-r19-g4-consumer-contract-repair');executed=Path('/home/lizening/wt-r19-recovery-duration-v1');out=executed/'artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z';sup=repo/'agent-logs/2026-10-23T002200Z__LUNA__r19-g3-live-successor__2da980f/supervisor_live'
now=datetime.datetime.now(datetime.timezone.utc);p=repo/'agent-logs'/(now.strftime('%Y-%m-%dT%H%M%SZ')+'__SOL__r19-g4-exact-proposal-clearance__85cbb923_'+uuid.uuid4().hex[:6]);p.mkdir();Path('/tmp/r19-g4-execution-clearance-path.txt').write_text(str(p)+'\n')
def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
def canonical(v):return hashlib.sha256(json.dumps(v,ensure_ascii=True,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def load(path):return json.loads(Path(path).read_text())
def git(path,*args):return subprocess.check_output(['git','-C',str(path),*args],text=True).strip()
assert git(repo,'rev-parse','HEAD')==git(repo,'ls-remote','origin','refs/heads/main').split()[0]=='1c22935bd6b74f113249f155a44fdc9ff0f6c76c'
assert not git(repo,'diff','--name-only') and not git(repo,'diff','--cached','--name-only')
source_states={}
for path,expected in [(Path('/home/lizening/wt-codex-r18c2'),'e537f441010077123a307e9d50ea40cf8dad8547'),(analyzer,'85cbb92395e5e2420c2adeb1fa0634653e742910'),(executed,'2da980f631badc25086d12db60d128ff507d3ae6')]:
 state={'head':git(path,'rev-parse','HEAD'),'branch':git(path,'branch','--show-current'),'status':git(path,'status','--porcelain')};assert state['head']==expected and not state['status'];source_states[str(path)]=state
remote=git(analyzer,'ls-remote','origin','refs/heads/codex/r19-g4-consumer-contract-repair','refs/heads/codex/r19-source-contract-review-fixes');assert '85cbb92395e5e2420c2adeb1fa0634653e742910\trefs/heads/codex/r19-g4-consumer-contract-repair' in remote and '2da980f631badc25086d12db60d128ff507d3ae6\trefs/heads/codex/r19-source-contract-review-fixes' in remote
bindings=load(prep/'input_hashes.json');argv=load(prep/'proposed_analyzer_argv.json');env=load(prep/'proposed_environment.json');input_hashes={}
for line in (prep/'FILE_HASHES.sha256').read_text().splitlines():
 h,name=line.split('  ',1);file=prep/name;assert sha(file)==h
 remote_bytes=subprocess.check_output(['git','-C',str(repo),'show','HEAD:'+str(file.relative_to(repo))]);assert hashlib.sha256(remote_bytes).hexdigest()==h;input_hashes[str(file)]=h
for path,h in bindings['review_artifacts'].items():assert sha(path)==h;input_hashes[path]=h
assert sha(review/'independent_review.json')=='8817b955846624936d591a104a0bcbedde1b66c9c1e1573b6eb60de7db965579';assert load(review/'independent_review.json')['IMPLEMENTATION_REVIEW']=='PASS'
for path,h in load(review/'evidence/actual_independent.pre_hashes.json').items():assert sha(path)==h;input_hashes[path]=h
for group,root in [('g3_output_files',out),('supervisor_files',sup)]:
 for name,h in bindings[group].items():assert sha(root/name)==h;input_hashes[str(root/name)]=h
assert len(bindings['g3_output_files'])==10 and len(bindings['supervisor_files'])==4
assert {x.name for x in out.iterdir() if x.is_file()}==set(bindings['g3_output_files'])
assert sha(analyzer/'scripts/analyze_r19_recovery_duration.py')==bindings['source_identities']['reviewed_analyzer_file_sha256']=='0edadbda5840786400eba0d13decc9c504957e4cda6224fefb98405d41af8b24'
assert argv[:2]==[env['interpreter'],str(analyzer/'scripts/analyze_r19_recovery_duration.py')]
assert len(argv)==28; pairs=argv[2:];opts=dict(zip(pairs[::2],pairs[1::2]));assert len(opts)==13 and len(opts)*2==len(pairs)
expected_opts={'--protocol':str(executed/'configs/experiments/r19_recovery_duration_v1.json'),'--events':str(out/'execution_events.jsonl'),'--branches':str(out/'branches.jsonl'),'--output':str(prep/'future_g4_report'),'--evidence-class':'live','--exit-receipt':str(sup/'runner_exit.json'),'--supervisor-status':str(sup/'supervisor_status.json'),'--runner-log':str(sup/'runner.log'),'--schedule':str(executed/'configs/experiments/r19_preflight_v3/source_schedule.json'),'--exclusions':str(executed/'configs/experiments/r19_preflight_v3/exclusion_manifest.json'),'--execution-manifest':str(out/'execution_manifest.json'),'--runtime-manifest':str(out/'runtime_manifest.json'),'--environment-manifest':str(out/'environment_manifest.json')};assert opts==expected_opts
future=Path(opts['--output']);assert not os.path.lexists(future);assert future.resolve()==future and future.parent==prep
for flag,path in opts.items():
 if flag not in ('--output','--evidence-class'):assert Path(path).is_file();input_hashes[path]=sha(path)
assert sha(prep/'proposed_analyzer_argv.json')==bindings['future_only_command_bindings']['argv_json_raw_sha256']
assert canonical(argv)==bindings['future_only_command_bindings']['argv_canonical_sha256']=='69abc553c35baf28423c0e1eb51a39547e95005f058ba3a87d32e01f32c15c89'
assert canonical(env)==bindings['future_only_command_bindings']['environment_canonical_sha256']=='fb67e1cd8ab5d78ba8f236322de3970f916fcde5ac1bd3654ada01215ffa0aa4'
assert sha(prep/'proposed_environment.json')==bindings['future_only_command_bindings']['environment_json_raw_sha256']
assert env['cwd']==str(executed) and env['inherit_unspecified_environment'] is False and set(env['unset'])=={'PYTHONHOME','PYTHONPATH','VIRTUAL_ENV'}
assert set(env['set']).isdisjoint(env['unset']) and all(isinstance(k,str) and isinstance(v,str) for k,v in env['set'].items())
assert env['set']['HF_HUB_OFFLINE']==env['set']['TRANSFORMERS_OFFLINE']=='1'
assert env['set']['ALFWORLD_CONFIG_PATH']==str(executed/'configs/local/r19_b1_g2_alfworld.yaml') and env['set']['ALFWORLD_DATA']=='/home/lizening/alfworld_data'
probe_code="import sys,json,importlib.metadata as m;print(json.dumps({'executable':sys.executable,'python':sys.version,'packages':{n:m.version(n) for n in ['PyYAML','accelerate','alfworld','huggingface-hub','numpy','peft','safetensors','textworld','tokenizers','torch','transformers']}}))"
probe=subprocess.run([argv[0],'-c',probe_code],cwd=env['cwd'],env=dict(env['set']),capture_output=True,text=True);assert probe.returncode==0,probe.stderr;runtime=load(out/'runtime_manifest.json');observed= json.loads(probe.stdout);assert observed['python']==runtime['python'] and observed['packages']==runtime['packages'];input_hashes[argv[0]]=sha(Path(argv[0]).resolve())
(p/'pinned_python_metadata_probe.json').write_text(json.dumps({'argv':[argv[0],'-c',probe_code],'actual_subprocess_returncode':probe.returncode,'cwd':env['cwd'],'effective_environment':env['set'],'stdout':probe.stdout,'stderr':probe.stderr,'python_and_all_11_package_versions_match_original_runtime':True,'model_environment_imports_or_calls':0},indent=2)+'\n')
commands=subprocess.check_output(['ps','-eo','pid,ppid,args'],text=True).splitlines()[1:];active=[]
for line in commands:
 parts=line.split(None,2)
 if len(parts)>2 and any(Path(x).name in {'run_r19_recovery_duration.py','launch_r19_supervised.py','analyze_r19_recovery_duration.py'} for x in parts[2].split()[1:3]):active.append(line.strip())
assert not active,active
gpu=subprocess.run(['nvidia-smi','--query-compute-apps=pid,process_name,used_memory','--format=csv,noheader'],capture_output=True,text=True);assert gpu.returncode==0 and not gpu.stdout.strip(),(gpu.stdout,gpu.stderr)
receipt=load(sup/'runner_exit.json');status=load(sup/'supervisor_status.json');assert receipt['run_id']==status['run_id']=='260422ac02bd42a8b2929d7ef240526b' and receipt['exit_code']==0 and receipt['exit_code_source']=='subprocess.returncode' and status['status']=='completed' and receipt['interrupted_by_supervisor'] is False
assert sha(sup/'launch_context.json')==receipt['launch_context_sha256']==status['launch_context_sha256']
for path in (analyzer,executed):assert not git(path,'status','--porcelain')
for file in ('proposed_analyzer_argv.json','proposed_environment.json'):(p/file).write_bytes((prep/file).read_bytes())
review_record={'schema_version':'r19_g4_exact_proposal_and_drift_review_v1','reviewer':'Sol','reviewed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_EXACT_PROPOSAL_AND_CURRENT_DRIFT','reviewed_analyzer_sha':'85cbb92395e5e2420c2adeb1fa0634653e742910','executed_G3_sha':'2da980f631badc25086d12db60d128ff507d3ae6','G3_run_id':receipt['run_id'],'worktree_states':source_states,'scientific_live_remote_refs':remote,'provenance_checkpoint':'1c22935bd6b74f113249f155a44fdc9ff0f6c76c','argv_raw_sha256':sha(prep/'proposed_analyzer_argv.json'),'argv_canonical_sha256':canonical(argv),'environment_raw_sha256':sha(prep/'proposed_environment.json'),'environment_canonical_sha256':canonical(env),'effective_environment_exact_allowlist':env['set'],'all_historical_and_proposal_inputs_byte_verified':len(input_hashes),'input_sha256':input_hashes,'existing_G3_output_files':10,'original_supervisor_files':4,'full_original_archive_regular_files':15,'nonblocking_prose_correction':'Readiness prose says15 G3 output files; actual typed binding is10 output +4 supervisor +1 launcher =15 archive regular files. Typed paths/hashes and argv are correct; old prose is left immutable and this record clarifies the count.','future_output_path':str(future),'future_output_absent':True,'no_active_R19_or_GPU_compute':True,'all_11_package_versions_and_python_unchanged':True,'reviewer_actual_analyzer_or_validator_invocations':0,'reviewer_model_environment_generations_resets_steps':0,'formal_G4_not_yet_started':True,'expected_new_output_files':['summary.json','R19_OPPORTUNITY_REPORT.md','report_hashes.json'],'model_environment_generation_reset_action_budget':0,'cumulative_start':{'model_generations':5142,'environment_operations_including_resets':7949,'incomplete_external_operations':0},'conditions':['Exactly one pinned analyzer argv invocation by Luna after new explicit release.','Exact allowlisted environment only; no shell reconstruction or inherited overrides.','No G3/G2/preflight/supervisor/model/environment/retry or evidence/code modification.','Failure or drift stops; preserve actual child exit/logs/partial outputs.','Output writes only planned new leaf; historical readiness files and original scientific evidence remain unchanged.']}
(p/'proposal_and_drift_review.json').write_text(json.dumps(review_record,indent=2)+'\n');print(json.dumps({'directory':str(p),'status':review_record['status'],'review_sha256':sha(p/'proposal_and_drift_review.json'),'verified_input_count':len(input_hashes),'package_count':11,'future_output_absent':True,'no_analyzer_execution':True},indent=2))
