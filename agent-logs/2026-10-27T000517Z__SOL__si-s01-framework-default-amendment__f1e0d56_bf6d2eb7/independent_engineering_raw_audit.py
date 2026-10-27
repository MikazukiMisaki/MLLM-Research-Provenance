from pathlib import Path
from datetime import datetime,timezone
import sys,json,hashlib,os
repo=Path('/home/lizening/wt-si-s01-shared-gpu-adapter');sys.path.insert(0,str(repo/'src'))
c=json.load(open('/tmp/si-s01-framework-default-amendment-context.json'));root=Path(c['directory']);a_path=Path(c['authorization']['path']);a_bytes=a_path.read_bytes();a=json.loads(a_bytes);p_bytes=(root/'PRODUCTION_PROPOSAL.json').read_bytes();p=json.loads(p_bytes);output=Path(a['output_path']);before={q.name:hashlib.sha256(q.read_bytes()).hexdigest() for q in output.iterdir() if q.is_file()}
assert hashlib.sha256(a_bytes).hexdigest()==c['authorization']['sha256'];assert hashlib.sha256(p_bytes).hexdigest()==a['proposal_sha256']
from self_improvement.si_s01.engineering_history import read_historical
from self_improvement.si_s01.engineering_contract import EngineeringPermit,MODE
from self_improvement.si_s01.engineering_audit import audit_engineering
from self_improvement.si_s01.engineering_runtime import EngineeringProducer
from self_improvement.si_s01.engineering_gate import verified_engineering_context
from transformers import AutoTokenizer
import torch
assert not torch.cuda.is_initialized()
h=p['history_manifest'];hb=Path(h['path']).read_bytes();assert hashlib.sha256(hb).hexdigest()==h['sha256'];history=read_historical(hb,evidence_class=MODE,expected_manifest_sha256=h['sha256'])
ctx={'launch_path':str(output/'launch_context.json'),'launch_sha256':before['launch_context.json'],'worker_path':str(output/'worker_start.json'),'worker_sha256':before['worker_start.json']}
permit=EngineeringPermit(a,p,c['authorization']['sha256'],a['proposal_sha256'],repo,history,ctx);verified_engineering_context(permit)
tokenizer=AutoTokenizer.from_pretrained(p['model']['base_snapshot'],local_files_only=True,trust_remote_code=False);encoder=EngineeringProducer(tokenizer,None,evidence_class=MODE)
report=audit_engineering(output/'engineering_events.jsonl',permit,encoder);original=json.load(open(output/'engineering_report.json'));assert report==original
supervisor=json.load(open(output/'supervisor_exit.json'));assert supervisor['authentic_returncode']==0 and supervisor['cleanup_established'] is True and supervisor['within_time_cap'] is True;assert supervisor['authorization_sha256']==permit.authorization_sha256 and supervisor['elapsed_seconds']<=510 and supervisor['allocated_devices']==1;assert abs(supervisor['elapsed_seconds']/3600-supervisor['allocated_device_hours'])<1e-12
assert not torch.cuda.is_initialized();after={q.name:hashlib.sha256(q.read_bytes()).hexdigest() for q in output.iterdir() if q.is_file()};assert before==after
value={'schema':'ROOT_INDEPENDENT_ACTUAL_ENGINEERING_RAW_AUDIT_V1','decision':'PASS_OBSERVED_BOUND_PUBLIC_PATH_AND_RESOURCE_ONLY','created_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'source_sha':a['source_sha'],'run_id':a['run_id'],'production_audit_recomputed_equal_original':True,'report_status':report['status'],'coupled_path':{'actual_reset_to_public_prompt':report['coupled_path']['actual_reset_to_public_prompt'],'historical_input_ids_status':report['historical_input_ids_status'],'internal_rng_reconstructed':False},'physical':report['physical'],'shared_resource':report['shared_resource'],'supervisor':supervisor,'original_hashes_before':before,'original_hashes_after':after,'raw_bytes_unchanged':True,'offline_boundary':{'cached_CPU_tokenizer_loaded':1,'model_objects_or_weights_loaded':0,'model_generation_calls':0,'CUDA_initialized':False,'environment_construct_reset_step':0,'original_history_read':'only frozen first rawline35486B plus9 exact referenced event slices <=149225 maxend; no whole-file input hash or scan'},'scope_limitations':['One real first prompt and saved six-action path, not arbitrary8192token inference memory-fit proof','Original internal RNG and historical inputIDs not reconstructed','Shared nonexclusive GPU, no NVML/localPID mapping or wholeprocessVRAM cap claim','Engineering separate from historical5142gens7949ops and futureA96; no selfimprovement success claim']}
(root/'ACTUAL_ENGINEERING_INDEPENDENT_ACCEPTANCE.json').write_text(json.dumps(value,indent=2)+'\n');print(json.dumps({'decision':value['decision'],'run_id':a['run_id'],'status':report['status'],'validated_resource_samples':report['shared_resource']['validated_resource_samples'],'model_generations':report['physical']['completed']['generation'],'env_ops':report['physical']['completed']['environment_operations'],'CUDA_initialized_after':torch.cuda.is_initialized(),'raw_hashes_unchanged':before==after}))
