import datetime,hashlib,json,os,subprocess
from pathlib import Path
root=Path('/home/lizening/wt-r19-recovery-duration-v1');p=Path('/tmp/r19-2da-review-path.txt').read_text().strip();p=Path(p)
git=lambda *a:subprocess.check_output(['git','-C',str(root),*a],text=True).strip()
old_head=git('rev-parse','HEAD');old_branch=git('branch','--show-current');old_status=git('status','--porcelain')
assert old_head=='da7d348ffd3677d619dd31357e1e1e3cca28c9ec' and old_branch=='codex/r19-source-contract-repair'
assert not git('diff','--name-only') and not git('diff','--cached','--name-only')
original=[root/'R19_IMPLEMENTATION_ONBOARDING.md']
oldout=root/'artifacts/runtime/r19_b1_g3_pilot_after_a0de515d7e104101bf8157175ea3d995_20261022T190221Z'
original += list(oldout.glob('*'))
original += list((root/'configs/local').glob('*'))
original=[f for f in original if f.is_file()]
hashes={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in original}
probe=p/'evidence/authentic_loader_probe.py'
probe.write_text("""import json,os,sys
from pathlib import Path
assert all(k not in os.environ for k in ('PYTHONPATH','PYTHONHOME','VIRTUAL_ENV'))
root=Path('/home/lizening/wt-r19-recovery-duration-v1');sys.path[:0]=[str(root),str(root/'src')]
from scripts import run_r19_experiment as r
assert r._git('rev-parse','HEAD')=='2da980f631badc25086d12db60d128ff507d3ae6'
assert r.PROJECT_ROOT.resolve()==root.resolve()
a,_=r._load_g3_authorization()
gate=json.loads((root/'configs/local/r19_b1_g3_gate_bf31f3.json').read_text())
paths=[r.R19_B1_G3_SOURCE_CONTRACT_REPAIR_AMENDMENT,r.R19_B1_G3_SOURCE_CONTRACT_RESTART_AUTHORIZATION,r.R19_B1_G3_SOURCE_UNIT_RESOLUTION]
gate['source_contract_restart']={'amendment_sha256':r.sha256_file(paths[0]),'authorization_sha256':r.sha256_file(paths[1]),'unit_resolution_event_sha256':r.sha256_file(paths[2]),'supervisor_record_directory':'/home/lizening/research-notes/agent-logs/2026-10-22T190221Z__CODEX__r19-g3-cli-preflight__bf31f3da/live_supervisor','failure_audit_json_path':'/home/lizening/research-notes/agent-logs/2026-10-22T191409Z__ASTRA__r19-g3-failure-audit__3d1ccea7/failure_audit.json'}
result=r._load_source_contract_restart_authorization(gate=gate,original_authorization=a)
proposed=root/'artifacts/runtime/r19_b1_g3_REVIEW_ONLY_ABSENT_NEVER_CREATED_2da980f'
assert not proposed.exists()
r._assert_single_g3_campaign_unused(proposed,approved_predecessor_output=root/result[0]['predecessor']['output_relative_path'])
print(json.dumps({'status':'PASS_NO_MOCKS_GENUINE_PREDECESSOR_IN_INTENDED_CONTEXT','implementation_sha':r._git('rev-parse','HEAD'),'runner_origin':r.__file__,'PROJECT_ROOT':str(r.PROJECT_ROOT),'source_gate_augmented_in_memory_only':True,'record_hashes':{x.name:r.sha256_file(x) for x in paths},'snapshot_sha256':r.sha256_json(result[4]),'caps':result[0]['restart']['remaining_phase_caps'],'cumulative_start':result[0]['restart']['cumulative_start'],'new_output_created':proposed.exists(),'preflight_or_live_entrypoint_called':False,'real_model_or_alfworld_calls':0},indent=2))
""")
receipt={'authorization':'Explicit user reply: allow temporary checkout switch and restoration for read-only authentic loader only.','old_head':old_head,'old_branch':old_branch,'old_status':old_status,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operation_log':[]}
try:
 r=subprocess.run(['git','-C',str(root),'switch','--detach','2da980f631badc25086d12db60d128ff507d3ae6'],capture_output=True,text=True);receipt['operation_log'].append({'stage':'temporary_detached_checkout','exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr});assert r.returncode==0
 clean=dict(os.environ)
 for key in ('PYTHONPATH','PYTHONHOME','VIRTUAL_ENV'):clean.pop(key,None)
 args=['/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python',str(probe)]
 r=subprocess.run(args,cwd='/tmp',env=clean,capture_output=True,text=True)
 (p/'evidence/authentic_loader.stdout.json').write_text(r.stdout);(p/'evidence/authentic_loader.stderr.log').write_text(r.stderr)
 receipt.update({'argv':args,'cwd':'/tmp','removed_environment_keys':['PYTHONPATH','PYTHONHOME','VIRTUAL_ENV'],'loader_exit_code':r.returncode,'exit_source':'subprocess.returncode'})
finally:
 r=subprocess.run(['git','-C',str(root),'switch',old_branch],capture_output=True,text=True);receipt['operation_log'].append({'stage':'restore_original_branch','exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 receipt.update({'restored_head':git('rev-parse','HEAD'),'restored_branch':git('branch','--show-current'),'restored_status':git('status','--porcelain'),'original_local_files_sha256_unchanged':all(Path(f).is_file() and hashlib.sha256(Path(f).read_bytes()).hexdigest()==s for f,s in hashes.items()),'protected_file_hashes_before':hashes,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
 (p/'evidence/authentic_context.receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
assert receipt['restored_head']==old_head and receipt['restored_branch']==old_branch and receipt['restored_status']==old_status and receipt['original_local_files_sha256_unchanged']
print(json.dumps({k:receipt[k] for k in ['loader_exit_code','restored_head','restored_branch','restored_status','original_local_files_sha256_unchanged']},indent=2))
assert receipt['loader_exit_code']==0,(p/'evidence/authentic_loader.stderr.log').read_text()
