import json,sys,types
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,'/home/lizening/research-notes/agent-logs/20261118__CODEX__si-stateful-sft-core__private')
import torch
import torch.nn.functional as F
import stateful_core as core
from test_stateful_core import TinyCPU
rows=json.loads(Path('/home/lizening/research-notes/agent-logs/20261118__CODEX__si-stateful-sft-core__private/fixture.json').read_text())['rows']
original=torch.optim.AdamW
records=[]
model=TinyCPU()
def aggregate(row):
    ids=torch.tensor([row['input_ids']],dtype=torch.long,device='cpu')
    labels=torch.tensor([[t if m else -100 for t,m in zip(row['input_ids'],row['loss_mask'])]],dtype=torch.long,device='cpu')
    logits=model(input_ids=ids,attention_mask=torch.ones_like(ids),use_cache=False).logits
    return F.cross_entropy(logits[:,:-1,:].float().reshape(-1,5),labels[:,1:].reshape(-1),ignore_index=-100,reduction='sum')
class CheckedAdamW(original):
    def step(self,closure=None):
        index=len(records);batch=rows[(index%4)*4:(index%4)*4+4]
        denom=sum(sum(r['loss_mask'][1:]) for r in batch)
        ref=torch.autograd.grad(sum(aggregate(r) for r in batch)/denom,model.weight)[0]
        torch.testing.assert_close(model.weight.grad,ref,rtol=1e-5,atol=1e-7)
        records.append({'before':index,'optimizer_id':id(self),'model_id':id(model)})
        return super().step(closure)
calls=[]
with patch.object(torch.optim,'AdamW',CheckedAdamW):
    out=core.run_cpu_research_core(model=model,rows=rows,checkpoint_writer=lambda m,o,meta:calls.append(meta) or {'synthetic':True},vocab_size=5,eos_token_id=3,pad_token_id=4)
assert len(records)==16 and len({r['optimizer_id'] for r in records})==1 and len(calls)==1 and calls[0]['optimizer_steps']==16
print('PASS actual candidate: 16 independent aggregated-gradient comparisons; one optimizer; final callback exactly after step16')
class NanBackward(torch.autograd.Function):
    @staticmethod
    def forward(ctx,x):return x.clone()
    @staticmethod
    def backward(ctx,grad):return torch.full_like(grad,float('nan'))
class BadGrad(TinyCPU):
    def forward(self,**kwargs):return types.SimpleNamespace(logits=NanBackward.apply(super().forward(**kwargs).logits))
steps=[];callbacks=[]
class CountAdamW(original):
    def step(self,closure=None):steps.append(1);return super().step(closure)
with patch.object(torch.optim,'AdamW',CountAdamW):
    try:core.run_cpu_research_core(model=BadGrad(),rows=rows,checkpoint_writer=lambda *x:callbacks.append(1),vocab_size=5,eos_token_id=3,pad_token_id=4)
    except core.Stop as e:assert 'nonfinite or absent gradient' in str(e)
    else:raise AssertionError('bad gradient accepted')
assert not steps and not callbacks
print('PASS finite forward/nonfinite backward: zero optimizer steps and zero callback')
assert not torch.cuda.is_initialized()
print('CUDA_INITIALIZED',torch.cuda.is_initialized())
