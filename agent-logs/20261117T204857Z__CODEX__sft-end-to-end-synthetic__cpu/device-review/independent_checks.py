import json,sys,types
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,'/home/lizening/research-notes/agent-logs/20261118__CODEX__si-device-independent-sft__private')
import torch
import torch.nn.functional as F
import device_core as c
from test_device_core import TinyCPU,FakeOwner
rows=json.loads(Path('/home/lizening/research-notes/agent-logs/20261118__CODEX__si-device-independent-sft__private/fixture.json').read_text())['rows']
def optimizer(model):return torch.optim.AdamW(model.parameters(),lr=3e-5,betas=(.9,.999),eps=1e-8,weight_decay=0.,amsgrad=False,foreach=False,capturable=False,maximize=False,fused=False)
model=TinyCPU();opt=optimizer(model);owner=FakeOwner();step_original=opt.step;refs=[];callbacks=[]
def ref_loss(row):
    x=torch.tensor([row['input_ids']],dtype=torch.long)
    y=torch.tensor([[t if m else -100 for t,m in zip(row['input_ids'],row['loss_mask'])]],dtype=torch.long)
    z=model(input_ids=x,attention_mask=torch.ones_like(x),use_cache=False).logits
    return F.cross_entropy(z[:,:-1,:].float().reshape(-1,5),y[:,1:].reshape(-1),ignore_index=-100,reduction='sum')
def check_step(*args,**kwargs):
    index=len(refs);batch=rows[(index%4)*4:(index%4)*4+4];n=sum(sum(r['loss_mask'][1:]) for r in batch)
    expected=torch.autograd.grad(sum(ref_loss(r) for r in batch)/n,model.weight)[0]
    torch.testing.assert_close(model.weight.grad,expected,rtol=1e-5,atol=1e-7)
    refs.append(index);return step_original(*args,**kwargs)
with patch.object(opt,'step',side_effect=check_step):
    r=c.run_injected_core(model=model,optimizer=opt,rows=rows,owner=owner,checkpoint_writer=lambda m,o,x:callbacks.append(x) or {'fake':True},vocab_size=5,eos_token_id=3,pad_token_id=4)
assert len(refs)==16 and len(callbacks)==1 and len(owner.events)==326
assert all(owner.events[i][0]=='reserve' and owner.events[i+1]==('returned',owner.events[i][1]) for i in range(0,len(owner.events),2))
print('PASS: actual injected core, 16 independent gradient references, 163 correctly ordered fake reservation-return pairs, final callback once')
class BadFn(torch.autograd.Function):
 @staticmethod
 def forward(ctx,x):return x.clone()
 @staticmethod
 def backward(ctx,g):return torch.full_like(g,float('nan'))
class BadGrad(TinyCPU):
 def forward(self,**kw):return types.SimpleNamespace(logits=BadFn.apply(super().forward(**kw).logits))
bad=BadGrad();badopt=optimizer(bad);badowner=FakeOwner();badcallbacks=[]
try:c.run_injected_core(model=bad,optimizer=badopt,rows=rows,owner=badowner,checkpoint_writer=lambda *x:badcallbacks.append(1),vocab_size=5,eos_token_id=3,pad_token_id=4)
except c.Stop as e:assert 'nonfinite or absent gradient' in str(e)
else:raise AssertionError('bad gradient accepted')
assert not badopt.state and not badcallbacks and ('unknown','backward') in badowner.events and ('reserve','optimizer_step') not in badowner.events
assert not torch.cuda.is_initialized()
print('PASS: finite forward/nonfinite gradient: fake backward UNKNOWN, zero step reservations and callbacks; CUDA_INITIALIZED False')
