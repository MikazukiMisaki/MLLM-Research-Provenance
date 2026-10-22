import copy,json,shutil,subprocess,sys,tempfile
from pathlib import Path
root=Path('/home/lizening/wt-r19-recovery-duration-v1')
sys.path[:0]=[str(root),str(root/'src')]
from scripts import run_r19_experiment as r
assert subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()=='da7d348ffd3677d619dd31357e1e1e3cca28c9ec'
a,_=r._load_g3_authorization()
gate=json.loads((root/'configs/local/r19_b1_g3_gate_bf31f3.json').read_text())
paths=[r.R19_B1_G3_SOURCE_CONTRACT_REPAIR_AMENDMENT,r.R19_B1_G3_SOURCE_CONTRACT_RESTART_AUTHORIZATION,r.R19_B1_G3_SOURCE_UNIT_RESOLUTION]
gate['source_contract_restart']={'amendment_sha256':r.sha256_file(paths[0]),'authorization_sha256':r.sha256_file(paths[1]),'unit_resolution_event_sha256':r.sha256_file(paths[2]),'supervisor_record_directory':'/home/lizening/research-notes/agent-logs/2026-10-22T190221Z__CODEX__r19-g3-cli-preflight__bf31f3da/live_supervisor','failure_audit_json_path':'/home/lizening/research-notes/agent-logs/2026-10-22T191409Z__ASTRA__r19-g3-failure-audit__3d1ccea7/failure_audit.json'}
result=r._load_source_contract_restart_authorization(gate=gate,original_authorization=a)
supervisor=Path(gate['source_contract_restart']['supervisor_record_directory'])
results={'authentic_predecessor':'PASS_NO_MOCKS','tampered_context_rejections':{},'mutated_original_evidence':False}
for field,value in [('cwd','/fake'),('command_argv',['fake','fake','pilot']),('omitted_environment_key_presence',{'PYTHONPATH':True,'PYTHONHOME':False,'VIRTUAL_ENV':False}),('run_id','forged')]:
 with tempfile.TemporaryDirectory(prefix='r19-forged-context-') as tmp:
  dest=Path(tmp)
  for name in result[0]['predecessor']['supervisor_record_sha256']:shutil.copyfile(supervisor/name,dest/name)
  p=dest/'launch_context.json';doc=json.loads(p.read_text());doc[field]=value;p.write_text(json.dumps(doc)+'\n')
  bad=copy.deepcopy(gate);bad['source_contract_restart']['supervisor_record_directory']=str(dest)
  try:r._load_source_contract_restart_authorization(gate=bad,original_authorization=a)
  except r.ExecutionGateError as e:results['tampered_context_rejections'][field]=str(e)
  else:raise AssertionError('forged supervisor accepted')
# Actual persistent gate function; fake output directories in an isolated sandbox only.
with tempfile.TemporaryDirectory(prefix='r19-one-restart-gate-') as tmp:
 original=r.PROJECT_ROOT;r.PROJECT_ROOT=Path(tmp)
 try:
  out=r.PROJECT_ROOT/'artifacts/runtime';out.mkdir(parents=True)
  predecessor=out/'r19_b1_g3_preserved_failed';predecessor.mkdir()
  successor=out/'r19_b1_g3_successor'
  r._assert_single_g3_campaign_unused(successor,approved_predecessor_output=predecessor)
  successor.mkdir()
  try:r._assert_single_g3_campaign_unused(out/'r19_b1_g3_second',approved_predecessor_output=predecessor)
  except FileExistsError:results['one_restart_sandbox_gate']='PASS_REJECT_SECOND_SUCCESSOR'
  else:raise AssertionError('second successor allowed')
 finally:r.PROJECT_ROOT=original
print(json.dumps(results,indent=2))
