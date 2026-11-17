"""One fictional CPU tensor example; not a training job or real LoRA product."""
import json
from pathlib import Path
import torch
from final_checkpoint import FictionalFinalCheckpoint

root=Path(__file__).resolve().parent/'demo-output'
root.mkdir(mode=0o700,exist_ok=False)
values={'fictional.weight':torch.tensor([[0.0,1.25],[-2.0,3.0]],dtype=torch.float32,device='cpu'),
        'fictional.count':torch.tensor([1,2],dtype=torch.int64,device='cpu')}
callback=FictionalFinalCheckpoint(root/'final')
result=callback(16,values)
with (root/'callback_return.json').open('x') as f:json.dump(result,f,sort_keys=True,indent=2);f.write('\n')
print(json.dumps(result,sort_keys=True))
