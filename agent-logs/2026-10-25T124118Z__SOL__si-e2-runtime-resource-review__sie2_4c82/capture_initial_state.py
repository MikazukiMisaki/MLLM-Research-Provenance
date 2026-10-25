"""Read-only SI-E2 initial metadata/resource capture; no model/env imports."""
from pathlib import Path
import hashlib
import json
import struct
import subprocess
from datetime import datetime, timezone

OWN = Path(__file__).resolve().parent
assert OWN.name == '2026-10-25T124118Z__SOL__si-e2-runtime-resource-review__sie2_4c82'
ROOT = Path('/home/lizening/wt-codex-r18c2')

def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda: f.read(1048576), b''):
            h.update(b)
    return h.hexdigest()

def command(name, argv, cwd=ROOT):
    start = datetime.now(timezone.utc).isoformat()
    p = subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (OWN / (name + '.stdout')).write_bytes(p.stdout)
    (OWN / (name + '.stderr')).write_bytes(p.stderr)
    receipt = dict(argv=argv, cwd=str(cwd), start_utc=start,
                   finish_utc=datetime.now(timezone.utc).isoformat(),
                   subprocess_returncode=p.returncode,
                   stdout_sha256=hashlib.sha256(p.stdout).hexdigest(),
                   stderr_sha256=hashlib.sha256(p.stderr).hexdigest())
    (OWN / (name + '.receipt.json')).write_text(json.dumps(receipt, indent=2)+'\n')
    return receipt

def header_summary(paths):
    result = {'files': [], 'parameters_by_dtype': {}, 'total_parameters': 0, 'tensor_storage_bytes': 0}
    for p in paths:
        with p.open('rb') as f:
            n = struct.unpack('<Q', f.read(8))[0]
            assert n < 10000000
            header = json.loads(f.read(n))
        tensors = {k:v for k,v in header.items() if k != '__metadata__'}
        result['files'].append({'path':str(p), 'bytes':p.stat().st_size,
                                'header_sha256':hashlib.sha256(json.dumps(header,sort_keys=True).encode()).hexdigest(),
                                'tensors':len(tensors)})
        for t in tensors.values():
            count=1
            for dim in t['shape']:
                count *= dim
            result['total_parameters'] += count
            result['parameters_by_dtype'][t['dtype']] = result['parameters_by_dtype'].get(t['dtype'],0)+count
            result['tensor_storage_bytes'] += t['data_offsets'][1]-t['data_offsets'][0]
    return result

receipts=[]
for name,args,cwd in [
    ('guard_root',['pwd'],ROOT),
    ('guard_top',['git','rev-parse','--show-toplevel'],ROOT),
    ('guard_branch',['git','branch','--show-current'],ROOT),
    ('guard_status',['git','status','--short','--branch'],ROOT),
    ('guard_HEAD',['git','rev-parse','HEAD'],ROOT),
    ('scientific_remote_base',['git','ls-remote','origin','refs/heads/codex/si-p3-engineering-contracts'],ROOT),
    ('provenance_remote_start',['git','ls-remote','origin','refs/heads/main'],Path('/home/lizening/research-notes')),
    ('gpu_start',['nvidia-smi','--query-gpu=index,uuid,name,memory.total,memory.free,driver_version,compute_mode','--format=csv'],ROOT),
    ('gpu_processes_start',['nvidia-smi','--query-compute-apps=pid,process_name,gpu_uuid,used_memory','--format=csv'],ROOT),
]:
    receipts.append(command(name,args,cwd))

snapshot=Path('/home/lizening/.cache/huggingface/hub/models--Qwen--Qwen3-8B/snapshots/b968826d9c46dd6066d109eabc6255188de91218')
adapter=Path('/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/model-artifacts/sft-policy-bootstrap/full/final_adapter')
base = header_summary(sorted(snapshot.glob('*.safetensors')))
p0 = header_summary(sorted(adapter.glob('*.safetensors')))
estimate = {
    'schema':'SI_E2_STATIC_STORAGE_BOUND_V1', 'evidence_class':'read_only_safetensors_headers_not_a_model_load',
    'base':base, 'P0':p0,
    'metadata_sha256':{str(p):sha(p) for p in (snapshot/'config.json',adapter/'adapter_config.json')},
    'future_training_FP32_LoRA_weight_grad_Adam_moments_lower_bound_bytes':p0['total_parameters']*16,
    'interpretation':'Static tensor storage/parameter counts only; no activations, KV/workspace, temporary load copies, runtime overhead or measured optimizer state. Not a training-fit claim.',
    'no_model_env_training_imports':True
}
(OWN/'independent_static_storage_bounds.json').write_text(json.dumps(estimate,indent=2)+'\n')
(OWN/'initial_state_receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
print(json.dumps({'base_parameters':base['total_parameters'],'base_tensor_bytes':base['tensor_storage_bytes'],
                  'P0_parameters':p0['total_parameters'],'P0_tensor_bytes':p0['tensor_storage_bytes'],
                  'base_dtype_counts':base['parameters_by_dtype'],'P0_dtype_counts':p0['parameters_by_dtype'],
                  'command_returncodes':[r['subprocess_returncode'] for r in receipts]}))
