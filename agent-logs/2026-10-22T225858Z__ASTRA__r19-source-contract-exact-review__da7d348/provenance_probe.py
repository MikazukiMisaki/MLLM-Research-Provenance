import hashlib,json,subprocess,sys
from pathlib import Path
root=Path('/home/lizening/wt-r19-recovery-duration-v1');sys.path[:0]=[str(root),str(root/'src')]
from scripts import run_r19_experiment as r
assert subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()=='da7d348ffd3677d619dd31357e1e1e3cca28c9ec'
a,_=r._load_g3_authorization()
gate=json.loads(Path('/home/lizening/wt-r19-recovery-duration-v1/configs/local/r19_b1_g3_gate_bf31f3.json').read_text())
paths=[r.R19_B1_G3_SOURCE_CONTRACT_REPAIR_AMENDMENT,r.R19_B1_G3_SOURCE_CONTRACT_RESTART_AUTHORIZATION,r.R19_B1_G3_SOURCE_UNIT_RESOLUTION]
hashes={p.name:r.sha256_file(p) for p in paths}
gate['source_contract_restart']={'amendment_sha256':r.sha256_file(paths[0]),'authorization_sha256':r.sha256_file(paths[1]),'unit_resolution_event_sha256':r.sha256_file(paths[2]),'supervisor_record_directory':'/home/lizening/research-notes/agent-logs/2026-10-22T190221Z__CODEX__r19-g3-cli-preflight__bf31f3da/live_supervisor','failure_audit_json_path':'/home/lizening/research-notes/agent-logs/2026-10-22T191409Z__ASTRA__r19-g3-failure-audit__3d1ccea7/failure_audit.json'}
result=r._load_source_contract_restart_authorization(gate=gate,original_authorization=a)
amendment=json.loads(paths[0].read_text());overlay=dict(a['scientific_execution_fingerprints'])
overlay.update({k:v['new'] for k,v in amendment['changed_method_fingerprints'].items()})
assert r._current_scientific_function_fingerprints(overlay)==overlay
for key,v in amendment['changed_method_fingerprints'].items():assert a['scientific_execution_fingerprints'][key]==v['old']
frozen={}
for name,p in [('protocol',r.R19_PROTOCOL),('schedule',root/'configs/experiments/r19_preflight_v3/source_schedule.json'),('exclusions',root/'configs/experiments/r19_preflight_v3/exclusion_manifest.json')]:
 data=subprocess.check_output(['git','-C',str(root),'show','bf31f3da:'+str(p.relative_to(root))]);assert data==p.read_bytes()
 frozen[name]=r.sha256_file(p)
for filename,sha in a['g2_carry_forward']['evidence_file_sha256'].items():
 p=Path(gate['g2_carry_forward']['evidence_directory'])/filename;assert r.sha256_file(p)==sha
caps=result[0]['restart']['remaining_phase_caps']
summary={'implementation_sha':'da7d348ffd3677d619dd31357e1e1e3cca28c9ec','authentic_record_loader':'PASS_NO_MOCKS','record_hashes':hashes,'expected_snapshot_sha256':r.sha256_json(result[4]),'fingerprints':{'total':len(overlay),'changed_methods':amendment['changed_method_fingerprints'],'effective_manifest_sha256':r.sha256_json(overlay),'all_match':True},'frozen_inputs':frozen,'g2_five_files':'PASS','caps':caps,'projected_cumulative_maximum':{'model_calls':177+sum(caps['model_calls'].values()),'environment_operations':342+sum(caps['environment_operations'].values())},'global_ceilings':a['resource_limits']['cumulative_campaign_ceilings_including_g2'],'scientific_calls':{'models':0,'alfworld':0,'preflight':0,'live':0}}
Path('/tmp/r19-source-review-evidence-da7d348/provenance_checks.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
