import json,sys
from pathlib import Path
sys.path.insert(0,'/home/lizening/research-notes/agent-logs/20261118__CODEX__si-stateful-sft-core__private')
import torch
import stateful_core as core
from test_stateful_core import TinyCPU
class HasUnusedFrozenNaN(TinyCPU):
 def __init__(self):
  super().__init__();self.frozen=torch.nn.Parameter(torch.tensor(float('nan'),device='cpu'),requires_grad=False)
rows=json.loads(Path('/home/lizening/research-notes/agent-logs/20261118__CODEX__si-stateful-sft-core__private/fixture.json').read_text())['rows']
model=HasUnusedFrozenNaN();calls=[]
r=core.run_cpu_research_core(model=model,rows=rows,checkpoint_writer=lambda *args:calls.append(1),vocab_size=5,eos_token_id=3,pad_token_id=4)
assert r['metadata']['optimizer_steps']==16 and len(calls)==1 and bool(torch.isnan(model.frozen).item())
assert not torch.cuda.is_initialized()
print('ACCEPTED: unused nontrainable CPU parameter NaN; 16 fake updates and final callback; trainable weights/loss remained finite')
print('No pretrained model or GPU; demonstrates nonfinite-check scope, not actual model corruption')
