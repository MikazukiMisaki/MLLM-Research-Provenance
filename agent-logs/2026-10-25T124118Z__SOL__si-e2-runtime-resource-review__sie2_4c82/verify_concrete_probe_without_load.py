"""Positive production binding checks only; does not call main/worker/supervisor/load."""
from pathlib import Path
import os
import sys
import json
import hashlib
import subprocess

OWN=Path(__file__).resolve().parent
assert OWN.name=='2026-10-25T124118Z__SOL__si-e2-runtime-resource-review__sie2_4c82'
source=Path(sys.argv[1]).resolve();auth=Path(sys.argv[2]).resolve();auth_sha=sys.argv[3];proposal=Path(sys.argv[4]).resolve()
os.environ['CUDA_VISIBLE_DEVICES']=json.loads(auth.read_bytes())['gpu_uuid']
os.environ['HF_HUB_OFFLINE']='1';os.environ['TRANSFORMERS_OFFLINE']='1'
for name in ('PYTHONPATH','PYTHONHOME','VIRTUAL_ENV','LD_PRELOAD'):os.environ.pop(name,None)
sys.path.insert(0,str(source/'src'))
from self_improvement.si_p3.runtime_gate import authenticate,verify_artifacts,inspect_gpu,engineering_prompts,digest
from self_improvement.si_p3.runtime_diagnostic import verify_packages
from self_improvement.si_p3.runtime_environment import historical_replay,bind_original_game_path

p=authenticate(source,auth,auth_sha,proposal)
assert not p.output.exists()
artifacts=verify_artifacts(p)
packages=verify_packages(p)
env=p.proposal['environment']
replay=historical_replay(Path(env['trajectory']).read_bytes(),Path(env['events']).read_bytes())
bind_original_game_path(env,json.loads(Path(env['trajectory']).read_bytes().splitlines()[0]),replay)
assert replay.seed==30000 and len(replay.commands)==6 and replay.states[-1]['done'] is True
assert len(replay.commands)*2<=p.ceilings['steps'] and p.ceilings['resets']==2
assert env['game_sha256']=='e393d4f3f521c7ceba7a6201a09884aec0f8941b4c87bcd4d427ea33a717bb99'
assert env['traj_data_sha256']=='eb817b82a0b7d4f3d08bebe43a581194f8dc796fb894b17f826c0c1c16ede385'
import torch
from transformers import AutoTokenizer
tok=AutoTokenizer.from_pretrained(p.proposal['model']['base_snapshot'],local_files_only=True,trust_remote_code=False)
lengths={}
for phase,prompt in engineering_prompts().items():
    rendered=tok.apply_chat_template([{'role':'user','content':prompt}],tokenize=False,
                                    add_generation_prompt=True,enable_thinking=False)
    encoded=tok(text=rendered,add_special_tokens=True)
    assert encoded['attention_mask']==[1]*len(encoded['input_ids'])
    assert len(encoded['input_ids'])<=p.ceilings['per_call_input']
    lengths[phase]={'input_tokens':len(encoded['input_ids']),
                    'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),
                    'rendered_prompt_sha256':hashlib.sha256(rendered.encode()).hexdigest(),
                    'input_ids_sha256':digest(encoded['input_ids'])}
assert sum(x['input_tokens'] for x in lengths.values())<=p.ceilings['input_tokens']
resources=inspect_gpu(p.gpu_uuid,allowed_pids=set())
project_origins={}
for name,module in list(sys.modules.items()):
    if name.split('.')[0] not in ('self_improvement','models','env','recovery','sft'):continue
    if not getattr(module,'__file__',None):continue
    path=Path(module.__file__).resolve()
    assert path.is_relative_to(source/'src'),(name,path)
    project_origins[name]={'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
assert not torch.cuda.is_initialized()
assert not p.output.exists()
result={'schema':'SI_E2_ROOT_MODEL_FREE_CONCRETE_BINDINGS_V1','status':'MODEL_FREE_BINDINGS_VERIFIED',
        'not_a_supervisor_or_model_environment_run':True,'source_sha':p.authorization['source_sha'],
        'authorization_sha256':auth_sha,'proposal_sha256':p.proposal_sha256,
        'artifacts':artifacts,'package_origins':packages,'project_module_origins':project_origins,
        'exact_four_input_sizes':lengths,'GPU_preallocation_snapshot':resources,
        'historical_replay':{'task_id':replay.task_id,'seed':replay.seed,'states':len(replay.states),
                             'commands':len(replay.commands),'terminal_in_original':replay.states[-1]['done']},
        'torch_cuda_initialized':False,'real_model_loads':0,'generations':0,'ALFWorld_construct_reset_step':0,
        'future_output_still_absent':True,'science_authorized':False,
        'not_proven':['own_CUDA_PID_mapping','8B_runtime_fit','live_replay_equality','training_fit']}
with (OWN/'concrete_probe_model_free_verification.json').open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'source_sha':result['source_sha'],
                  'total_prepared_input_tokens':sum(v['input_tokens'] for v in lengths.values()),
                  'torch_cuda_initialized':False,'future_output_absent':True}))
