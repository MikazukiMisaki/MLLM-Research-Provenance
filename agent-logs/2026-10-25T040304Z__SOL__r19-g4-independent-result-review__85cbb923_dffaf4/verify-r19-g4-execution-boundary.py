from pathlib import Path
import json,hashlib,subprocess,ast,datetime
p=Path(Path('/tmp/r19-g4-result-review-path.txt').read_text().strip());cdir=Path(Path('/tmp/r19-g4-execution-clearance-path.txt').read_text().strip());op=Path('/home/lizening/research-notes/agent-logs/2026-10-25T040521Z__LUNA__r19-formal-g4__85cbb923')
load=lambda f:json.loads(Path(f).read_text());sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest();c=load(cdir/'offline_G4_execution_clearance.json');d=load(cdir/'proposal_and_drift_review.json');ctx=load(op/'execution_context.json');start=load(op/'child_start.json');end=load(op/'child_exit.json');mark=load(op/'consumption_marker.json');latch=load(op/'analyzer_attempt_latch.json');pre=load(op/'pre_execution_input_hashes.json');operator=load(op/'execution_result.json')
assert sha(op/'execution_context.json')=='a1e62f343c1389cc39edc017f9b5129675c759dc286474152295c2600312aff7';assert sha(op/'consumption_marker.json')=='77ae5577e9cbfcb193b9ddaa83fd27b52c5bf03f2a38028260c7815c0f93abaa'
for obj in [ctx,start,end,mark,latch,pre,operator]:assert obj['clearance_id']==c['clearance_id']
for obj in [ctx,start,end,mark,latch,operator]:assert obj['analysis_identity']=='r19-g4-offline-2026-10-25T040521Z-ebad1a0c'
assert start['argv']==load(cdir/'proposed_analyzer_argv.json') and start['environment']==c['effective_environment'] and start['cwd']==c['execution_cwd'] and start['shell'] is False
assert start['argv_canonical_sha256']==c['argv_canonical_sha256'] and start['environment_canonical_sha256']==c['environment_canonical_sha256'];assert end['pid']==start['pid']==805875 and end['returncode']==0 and end['returncode_source']=='subprocess.Popen.wait' and end['interrupted'] is False and end['retry_permitted'] is False
assert end['started_at_utc']==start['started_at_utc'];assert mark['maximum_analyzer_invocations']==1 and mark['automatic_retry'] is False
stamp=lambda value:datetime.datetime.fromisoformat(value.replace('Z','+00:00'));assert stamp(mark['marker_written_at_utc'])<stamp(latch['attempt_latched_at_utc'])<=stamp(start['started_at_utc'])<stamp(end['finished_at_utc'])
assert pre['count']==56 and pre['sha256']==d['input_sha256'];current={name:sha(name) for name in pre['sha256']};assert current==pre['sha256'];(p/'original_56_post_audit_hashes.json').write_text(json.dumps(current,indent=2)+'\n')
stdout=load(op/'analyzer.stdout.raw');assert stdout['status']=='PASS' and stdout['report']==str(Path(c['planned_output_path'])/'R19_OPPORTUNITY_REPORT.md');assert (op/'analyzer.stderr.raw').stat().st_size==0
q=Path(c['planned_output_path']);assert {x.name for x in q.iterdir()}==set(c['allowed_new_output_files']);hm=load(q/'report_hashes.json');assert sha(q/'summary.json')==stdout['summary_json_sha256']==hm['summary_json_sha256'] and sha(q/'R19_OPPORTUNITY_REPORT.md')==stdout['opportunity_report_sha256']==hm['opportunity_report_sha256']
script=(op/'launch_once.py').read_text();tree=ast.parse(script);launches=[node for node in ast.walk(tree) if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and isinstance(node.func.value,ast.Name) and node.func.value.id=='subprocess' and node.func.attr=='Popen'];assert len(launches)==1
assert all(not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='Popen' for n in ast.walk(node)) for node in ast.walk(tree) if isinstance(node,(ast.For,ast.While)))
assert {n.names[0].name.split('.')[0] for n in tree.body if isinstance(n,ast.Import)}<={'datetime','hashlib','json','os','subprocess','sys','time'}
found=[]
for path in Path('/home/lizening/research-notes/agent-logs').glob('*/consumption_marker.json'):
 obj=load(path)
 if obj.get('clearance_id')==c['clearance_id']:found.append(str(path))
assert found==[str(op/'consumption_marker.json')]
for root,expected in [('/home/lizening/wt-r19-g4-consumer-contract-repair','85cbb92395e5e2420c2adeb1fa0634653e742910'),('/home/lizening/wt-r19-recovery-duration-v1','2da980f631badc25086d12db60d128ff507d3ae6')]:
 assert subprocess.check_output(['git','-C',root,'rev-parse','HEAD'],text=True).strip()==expected;assert not subprocess.check_output(['git','-C',root,'status','--porcelain'],text=True).strip()
active=[]
for line in subprocess.check_output(['ps','-eo','pid,ppid,args'],text=True).splitlines()[1:]:
 fields=line.split(None,2)
 if len(fields)>2 and any(Path(x).name in {'analyze_r19_recovery_duration.py','run_r19_recovery_duration.py','launch_r19_supervised.py'} for x in fields[2].split()[1:3]):active.append(line.strip())
assert active==[]
result={'status':'PASS_SINGLE_AUTHENTIC_COMPLETED_OFFLINE_G4_AND_UNCHANGED_INPUTS','verified_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'clearance_id':c['clearance_id'],'clearance_sha256':sha(cdir/'offline_G4_execution_clearance.json'),'analysis_identity':ctx['analysis_identity'],'authentic_child_pid':start['pid'],'authentic_returncode':end['returncode'],'returncode_source':end['returncode_source'],'one_clearance_marker_one_exclusive_latch_one_Popen_no_retry':True,'exact_approved_argv_cwd_environment':True,'original_56_pre_and_current_hashes_match':True,'old_readiness_and_scientific_evidence_not_modified':True,'exact_three_outputs_and_stdout_hash_binding':True,'single_analysis_completed_no_active_R19_process':True,'formal_analysis_invocations_by_reviewer':0,'new_model_environment_G2_G3_preflight_supervisor_calls':0,'cumulative_cost':{'generations':5142,'environment_operations_including_resets':7949,'incomplete_external_operations':0},'original_operator_evidence_sha256':{name:sha(op/name) for name in ['launch_once.py','execution_context.json','consumption_marker.json','analyzer_attempt_latch.json','child_start.json','child_exit.json','pre_execution_input_hashes.json','analyzer.stdout.raw','analyzer.stderr.raw','execution_result.json']},'remote_upload':'PENDING_OPERATOR_PUBLICATION'}
(p/'execution_boundary_review.json').write_text(json.dumps(result,indent=2)+'\n')
for name in ['child_start.json','child_exit.json','execution_context.json','consumption_marker.json','analyzer_attempt_latch.json','analyzer.stdout.raw','analyzer.stderr.raw']:(p/('observed_'+name)).write_bytes((op/name).read_bytes())
(p/'verify-r19-g4-report-arithmetic.py').write_bytes(Path('/tmp/verify-r19-g4-report-arithmetic.py').read_bytes());(p/'verify-r19-g4-execution-boundary.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps({k:v for k,v in result.items() if k not in ['original_operator_evidence_sha256']},indent=2))
