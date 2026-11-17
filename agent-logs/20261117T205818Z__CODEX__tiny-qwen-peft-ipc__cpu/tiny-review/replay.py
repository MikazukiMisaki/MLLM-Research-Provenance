import hashlib
import json
import os
from pathlib import Path
import runpy
import tempfile

import torch, transformers, peft, safetensors
from safetensors import safe_open

candidate = Path('/home/lizening/research-notes/agent-logs/20261118__CODEX__tiny-qwen3-peft-cpu__private/tiny_demo.py')
print('versions', json.dumps({'torch':torch.__version__, 'transformers':transformers.__version__, 'peft':peft.__version__, 'safetensors':safetensors.__version__}, sort_keys=True), flush=True)
assert os.environ.get('CUDA_VISIBLE_DEVICES') == '' and not torch.cuda.is_initialized()
with tempfile.TemporaryDirectory(prefix='fictional-tiny-review-') as tmp:
    root = Path(tmp)/'output'
    result = runpy.run_path(str(candidate))['run_fictional'](root)
    artifact = root/'FICTIONAL_ADAPTER'/'adapter_model.safetensors'
    sha = hashlib.sha256(artifact.read_bytes()).hexdigest()
    assert sha == result['fake_adapter_files_sha256']['adapter_model.safetensors']
    with safe_open(str(artifact), framework='pt', device='cpu') as obj:
        keys = list(obj.keys())
        assert len(keys) == 14
        assert all('lora_' in k and obj.get_tensor(k).device.type == 'cpu' for k in keys)
    assert result['core_metadata']['microbatches'] == 64 and result['core_metadata']['optimizer_steps'] == 16
    assert result['fake_owner_counts']['forward'] == result['fake_owner_counts']['backward'] == 64
    assert result['fake_owner_counts']['optimizer_step'] == 16
    assert result['fake_lora_changed'] and result['fake_base_unchanged'] and result['adapter_tensor_exact']
    assert not torch.cuda.is_initialized()
    print(json.dumps({'fake_scope':result['scope'], 'counts':result['fake_owner_counts'], 'tensor_count':len(keys), 'adapter_sha256':sha, 'max_abs_diff':result['fake_logits_max_absolute_difference'], 'base_frozen':result['fake_base_unchanged'], 'lora_changed':result['fake_lora_changed'], 'cuda_initialized':torch.cuda.is_initialized()},sort_keys=True),flush=True)
