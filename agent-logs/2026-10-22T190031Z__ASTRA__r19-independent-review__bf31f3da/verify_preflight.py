import datetime,json,subprocess,sys
from pathlib import Path
root=Path('/home/lizening/wt-r19-recovery-duration-v1');sys.path[:0]=[str(root),str(root/'src')]
from scripts import run_r19_experiment as r
from scripts.run_r19_recovery_duration import _pilot_gate_check
source='bf31f3da430ffc35bd17fc380e1752adce6d1467'
record=Path('/tmp/r19-independent-review/record_path.txt').read_text().strip();record=Path(record)
sup=Path('/home/lizening/research-notes/agent-logs/2026-10-22T190221Z__CODEX__r19-g3-cli-preflight__bf31f3da/preflight_supervisor')
read=lambda p:json.loads(p.read_text())
receipt=read(sup/'pilot_preflight_receipt.json');exitrec=read(sup/'runner_exit.json');status=read(sup/'supervisor_status.json');ctx=read(sup/'launch_context.json')
assert receipt['status']=='PREFLIGHT_ONLY_PASS'
assert exitrec['exit_code']==status['exit_code']==0 and exitrec['exit_code_source']=='subprocess.returncode'
assert exitrec['status']==status['status']=='completed'
assert receipt['implementation_sha']==exitrec['implementation_sha']==status['implementation_sha']==ctx['implementation_sha']==source
assert receipt['run_id']==exitrec['run_id']==status['run_id']==ctx['run_id']
assert receipt['supervisor_context_sha256']==exitrec['launch_context_sha256']==status['launch_context_sha256']==r.sha256_file(sup/'launch_context.json')
assert exitrec['runner_log_sha256']==status['runner_log_sha256']==r.sha256_file(sup/'runner.log')
assert status['runner_exit_sha256']==r.sha256_file(sup/'runner_exit.json')
assert exitrec['command_argv']==status['command_argv']==ctx['command_argv']
assert exitrec['command_sha256']==status['command_sha256']==ctx['command_sha256']==r.sha256_json(ctx['command_argv'])
assert exitrec['evidence_class']==status['evidence_class']==ctx['evidence_class']=='preflight_only'
assert exitrec['supersedes_run_id']==status['supersedes_run_id']==ctx['supersedes_run_id']=='a0de515d7e104101bf8157175ea3d995'
assert all(ctx['omitted_environment_key_presence'][k] is False for k in ['PYTHONPATH','PYTHONHOME','VIRTUAL_ENV'])
assert ctx['cwd']==str(root)
assert ctx['supervisor_entrypoint']==str(root/'scripts/launch_r19_supervised.py')
assert ctx['interpreter']==ctx['supervisor_interpreter']=='/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python'
assert all(type(v) is int and v==0 for v in receipt['scientific_side_effects'].values())
assert receipt['scheduled_train_tasks']==127 and receipt['output_path_absent'] is True
argv=ctx['command_argv'];option=lambda k:Path(argv[argv.index(k)+1])
gatepath=option('--manifest');gate=read(gatepath)
assert gatepath==root/'configs/local/r19_b1_g3_gate_bf31f3.json'
assert r.sha256_file(gatepath)==receipt['gate_manifest_sha256']
assert gate['review']['artifact_sha256']==r.sha256_file(record/'independent_review.json')=='73d3325343896bec3cd6f6b08ea77bae96211b75192b16094e6e6c963ad0ba27'
assert Path(gate['review']['artifact_path'])==record/'independent_review.json'
assert not option('--output').exists()
assert option('--preflight-receipt')==sup/'pilot_preflight_receipt.json'
a,asha=r._load_g3_authorization();_,repairsha=r._load_entrypoint_repair_authorization()
assert receipt['g3_authorization_sha256']==asha and receipt['entrypoint_repair_authorization_sha256']==repairsha
assert receipt['protocol_sha256']==r.sha256_file(option('--protocol'))==r.R19_PROTOCOL_SHA256
assert receipt['source_schedule_sha256']==r.R19_FROZEN_SOURCE_SCHEDULE_SHA256
assert receipt['exclusion_manifest_sha256']==r.R19_FROZEN_EXCLUSION_MANIFEST_SHA256
assert receipt['model_revision']==r.R19_B1_MODEL_REVISION
assert receipt['adapter_sha256']==a['baseline']['adapter_directory_sha256']
assert receipt['g2_executed_implementation_sha']==r.R19_G2_EXECUTED_SHA
assert receipt['g2_evidence_carried_forward'] is True and receipt['new_g2_run_performed'] is False
assert receipt['production_module_origins']=={'scripts.run_r19_experiment':str(root/'scripts/run_r19_experiment.py'),'scripts.analyze_r19_recovery_duration':str(root/'scripts/analyze_r19_recovery_duration.py')}
assert subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()==source
assert not subprocess.check_output(['git','-C',str(root),'status','--porcelain'],text=True).strip()
assert r._current_scientific_function_fingerprints(a['scientific_execution_fingerprints'])==a['scientific_execution_fingerprints']
_pilot_gate_check(option('--protocol'),gatepath,option('--output'))
r._validate_g3_carry_forward(gate=gate,authorization=a,authorization_sha256=asha,head=source,protocol_sha256=r.R19_PROTOCOL_SHA256)
r._assert_single_g3_campaign_unused(option('--output'))
live=[];skip=False
for i,arg in enumerate(argv):
 if arg=='--preflight-only':continue
 if arg=='--preflight-receipt':skip=True;continue
 if skip:skip=False;continue
 live.append(arg)
clearance={'schema_version':'r19_independent_launch_clearance_v1','status':'GRANTED_FOR_ONE_AUTHORIZED_SUCCESSOR','reviewer_task':'01a0994c-a209-7600-8a3e-5ff3096ed346','issued_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'implementation_sha':source,'review_artifact_sha256':r.sha256_file(record/'independent_review.json'),'gate_manifest_sha256':r.sha256_file(gatepath),'positive_preflight_receipt_sha256':r.sha256_file(sup/'pilot_preflight_receipt.json'),'positive_preflight_exit_sha256':r.sha256_file(sup/'runner_exit.json'),'positive_preflight_context_sha256':r.sha256_file(sup/'launch_context.json'),'preflight_run_id':receipt['run_id'],'supervisor_evidence_class_for_live':'live','supersedes_run_id':'a0de515d7e104101bf8157175ea3d995','live_child_argv':live,'live_child_argv_sha256':r.sha256_json(live),'maximum_live_launches':1,'automatic_retry':False,'g2_rerun':False,'cumulative_start':{'model_generations':176,'environment_operations':341},'required_conditions':['same source SHA, gate, runtime and input files as successful preflight','new supervisor run identity and record directory','unchanged pinned protocol, 127 TRAIN identities, 120 attempts, 60 eligible, 30/15/15, K=1..5, horizon=50 and original budgets','preserve authentic nonzero failure and stop without automatic live retry','G4 only on genuine completed G3 evidence','upload sanitized evidence and verified remote commit; report to reviewer'],'checks':'all assertions in verify_preflight.py passed; no reviewer model or environment calls'}
(record/'launch_clearance.json').write_text(json.dumps(clearance,indent=2)+'\n')
(record/'preflight_verification.json').write_text(json.dumps({'status':'PASS','receipt_status':receipt['status'],'exit_code':exitrec['exit_code'],'reviewer_verified_zero_scientific_side_effects':receipt['scientific_side_effects'],'source_and_gate_unchanged':True,'live_argv_sha256':clearance['live_child_argv_sha256']},indent=2)+'\n')
print(json.dumps({'status':clearance['status'],'clearance_path':str(record/'launch_clearance.json'),'clearance_sha256':r.sha256_file(record/'launch_clearance.json'),'live_argv_sha256':clearance['live_child_argv_sha256'],'positive_preflight':'PASS'},indent=2))
