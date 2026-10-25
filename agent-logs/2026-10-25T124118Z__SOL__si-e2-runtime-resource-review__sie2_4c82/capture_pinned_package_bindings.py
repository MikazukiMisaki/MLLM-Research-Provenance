"""Import runtime packages only, with CUDA hidden; never construct model/env."""
import os
os.environ['CUDA_VISIBLE_DEVICES']=''
os.environ['HF_HUB_OFFLINE']='1'
os.environ['TRANSFORMERS_OFFLINE']='1'
import importlib
import hashlib
import json
from pathlib import Path
import sys

OWN=Path(__file__).resolve().parent
assert OWN.name=='2026-10-25T124118Z__SOL__si-e2-runtime-resource-review__sie2_4c82'
names=('torch','transformers','peft','alfworld','textworld','yaml',
       'alfworld.agents.environment.alfred_tw_env','textworld.gym')
observed={}
for name in names:
    module=importlib.import_module(name)
    p=Path(module.__file__).resolve()
    observed[name]={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
                    'version':str(getattr(module,'__version__',''))}
torch=importlib.import_module('torch')
result={'schema':'SI_E2_ROOT_PINNED_PACKAGE_BINDINGS_V1','packages':observed,
        'interpreter':{'path':sys.executable,'sha256':hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest()},
        'CUDA_VISIBLE_DEVICES':'','torch_cuda_initialized':torch.cuda.is_initialized(),
        'model_objects':0,'environment_objects':0,'new_task_bodies':0}
assert result['torch_cuda_initialized'] is False
with (OWN/'independent_pinned_package_bindings.json').open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
