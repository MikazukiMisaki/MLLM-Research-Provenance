"""Independent byte verification, no model/env import or dataset discovery."""
from pathlib import Path
import hashlib
import json

OWN=Path(__file__).resolve().parent
assert OWN.name=='2026-10-25T124118Z__SOL__si-e2-runtime-resource-review__sie2_4c82'
BASE=Path('/home/lizening/wt-si-p3-engineering-contracts')
snapshot=Path('/home/lizening/.cache/huggingface/hub/models--Qwen--Qwen3-8B/snapshots/b968826d9c46dd6066d109eabc6255188de91218')
adapter=Path('/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/model-artifacts/sft-policy-bootstrap/full/final_adapter')
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def binding(path,expected=None):
    actual=sha(path)
    r={'path':str(path),'bytes':path.stat().st_size,'sha256':actual}
    if expected is not None:
        r.update(expected_sha256=expected,matches=actual==expected)
        assert r['matches'],r
    return r

frozen=json.loads((BASE/'configs/experiments/r19_model_identity_manifest.json').read_bytes())['currently_observed_candidate_not_historical_proof']
model=[binding(snapshot/row['name'],row.get('content_sha256',row.get('sha256'))) for row in frozen['snapshot_files']]
d=hashlib.sha256();p0=[]
for p in sorted(x for x in adapter.rglob('*') if x.is_file()):
    d.update(str(p.relative_to(adapter)).encode())
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):d.update(b)
    p0.append(binding(p))
assert d.hexdigest()=='6e403d85b150a74dfcc176f1f180ce4baf6fdacd922d2f96b3ceef0a21100f11'
run=Path('/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z')
known={
    'execution_events.jsonl':'05e1d443ff304eaa25d08b92a4e19d204a6c93a4f46bbe50aefef3271f211762',
    'source_trajectories.jsonl':'c6f37a7da28e326c70818524c79c17bbd85a286754c111f17db07cbe151a4f1c',
    'branches.jsonl':'eff9b5e74d3d5daa928cb662dcc59fc3f434f66796b673679d40b374f3c8636f',
    'runtime_manifest.json':'306a9e7c2d1b968e2a56e258fcd07aaf7467739460802a2b94c5e20411264916'}
historical=[binding(run/n,h) for n,h in known.items()]
failed=Path('/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_pilot_after_a0de515d7e104101bf8157175ea3d995_20261022T190221Z/execution_events.jsonl')
historical.append(binding(failed,'fde95fcd72f1c4ac6409fab7f2112654e145f6184fefec690cae58ad345f1cd7'))
result={'schema':'SI_E2_ROOT_INDEPENDENT_INPUT_BYTES_V1','frozen_model_files':model,'P0_files':p0,
        'P0_directory_sha256':d.hexdigest(),'historical_critical_inputs':historical,
        'all_expected_bytes_match':True,'new_task_bodies_opened':0,'model_env_calls':0}
with (OWN/'independent_frozen_input_bytes.json').open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
print(json.dumps({'model_files':len(model),'P0_files':len(p0),'historical_files':len(historical),'all_expected_bytes_match':True}))
