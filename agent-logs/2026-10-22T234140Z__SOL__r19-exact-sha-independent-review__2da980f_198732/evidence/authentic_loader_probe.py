import json,os,sys
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
