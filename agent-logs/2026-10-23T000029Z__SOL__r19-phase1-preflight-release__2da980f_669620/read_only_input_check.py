import datetime,json,os,sys
from pathlib import Path
root=Path('/tmp/r19-independent-review-2da980f');sys.path[:0]=[str(root),str(root/'src')]
from scripts import run_r19_experiment as r
p=Path('/tmp/r19-phase1-release-path.txt').read_text().strip();p=Path(p)
identity=json.loads(r.R19_B1_BASELINE.read_text());original=Path('/home/lizening/wt-r19-recovery-duration-v1')
config=original/'configs/local/r19_b1_g2_alfworld.yaml';data=Path('/home/lizening/alfworld_data');adapter=Path('/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/model-artifacts/sft-policy-bootstrap/full/final_adapter')
os.environ.update({'ALFWORLD_DATA':str(data),'ALFWORLD_CONFIG_PATH':str(config),'HF_HUB_CACHE':'/home/lizening/.cache/huggingface/hub','HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1'})
for k in ('PYTHONPATH','PYTHONHOME','VIRTUAL_ENV','HF_HOME','CUDA_VISIBLE_DEVICES','CUDA_HOME'):os.environ.pop(k,None)
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
inputs=r._read_exact_local_inputs(mode='pilot',data_root=data,config_path=config,adapter_path=adapter,schedule_path=root/'configs/experiments/r19_preflight_v3/source_schedule.json',exclusion_path=root/'configs/experiments/r19_preflight_v3/exclusion_manifest.json',protocol=json.loads(r.R19_PROTOCOL.read_text()),identity=identity)
runtime=r._runtime_manifest(data_root=data,config_path=config)
assert runtime==identity['runtime_expectations']['preload'],'runtime drift'
summary={'status':'PASS_READ_ONLY_PRODUCTION_INPUT_AND_RUNTIME_HASH_CHECK','start_utc':start,'finish_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewed_source':'2da980f631badc25086d12db60d128ff507d3ae6','no_PROJ_ROOT_override':True,'snapshot_file_count':len(inputs['model_bytes']['snapshot_file_sha256']),'adapter_file_count':len(inputs['model_bytes']['adapter_file_sha256']),'adapter_directory_sha256':inputs['adapter_sha256'],'source_identities':len(inputs['source_files']),'source_files_sha256':r.sha256_json(inputs['source_files']),'model_bytes':inputs['model_bytes'],'config_sha256':r.sha256_file(config),'runtime_preload_sha256':r.sha256_json(runtime),'runtime_exactly_matches_frozen_preload':True,'source_index_zero':inputs['schedule']['episodes'][0],'real_model_objects_loaded':0,'model_generations':0,'alfworld_construct_reset_step':0,'production_preflight_or_supervisor_called':False}
(p/'input_runtime_verification.json').write_text(json.dumps(summary,indent=2)+'\n');(p/'observed_runtime_preload.json').write_text(json.dumps(runtime,indent=2)+'\n')
print(json.dumps({k:summary[k] for k in ['status','snapshot_file_count','adapter_file_count','source_identities','adapter_directory_sha256','runtime_preload_sha256','runtime_exactly_matches_frozen_preload']},indent=2))
