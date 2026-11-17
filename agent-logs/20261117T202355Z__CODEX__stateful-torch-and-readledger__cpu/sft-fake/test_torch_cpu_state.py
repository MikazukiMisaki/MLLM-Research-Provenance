"""CPU-only fictional tensor test; no pretrained model, data, CUDA or environment."""
import json
from pathlib import Path
import unittest
import torch
import torch.nn.functional as F
import fake_stateful_sft as fake

class TorchCPUState(unittest.TestCase):
 def test_stateful_adamw_and_accumulation_gradient(self):
  raw=Path(__file__).with_name('fixture.json').read_bytes()
  self.assertEqual(__import__('hashlib').sha256(raw).hexdigest(),fake.FIXTURE_SHA256)
  rows=fake._validated_fake_rows(json.loads(raw))
  torch.random.default_generator.manual_seed(42)
  model=torch.nn.Linear(4,4,bias=False,dtype=torch.float64,device='cpu')
  param=model.weight
  optimizer=torch.optim.AdamW([param],lr=3e-5,betas=(0.9,0.999),eps=1e-8,weight_decay=0.0,foreach=False,fused=False)
  model_identity=id(model);param_identity=id(param);optimizer_identity=id(optimizer);micro=0;step_count=0
  def loss(row):
   ids=torch.tensor(row['input_ids'],dtype=torch.long,device='cpu')
   labels=torch.tensor([x if m else -100 for x,m in zip(row['input_ids'],row['loss_mask'])],dtype=torch.long,device='cpu')
   logits=model(F.one_hot(ids,num_classes=4).to(dtype=torch.float64))
   return F.cross_entropy(logits[:-1],labels[1:],ignore_index=-100,reduction='sum')
  for epoch in range(4):
   for start in range(0,16,4):
    batch=rows[start:start+4];den=sum(sum(r['loss_mask'][1:]) for r in batch)
    optimizer.zero_grad(set_to_none=True)
    reference=torch.autograd.grad(sum(loss(r) for r in batch)/den,param)[0]
    for row in batch:(loss(row)/den).backward();micro+=1
    torch.testing.assert_close(param.grad,reference,rtol=1e-12,atol=1e-12)
    optimizer.step();step_count+=1
    self.assertEqual(id(model),model_identity);self.assertEqual(id(model.weight),param_identity);self.assertEqual(id(optimizer),optimizer_identity)
    self.assertEqual(int(optimizer.state[param]['step'].item()),step_count)
    self.assertEqual(param.device.type,'cpu');self.assertEqual(optimizer.state[param]['exp_avg'].device.type,'cpu')
  self.assertEqual((micro,step_count),(64,16))
  self.assertTrue(bool(torch.count_nonzero(optimizer.state[param]['exp_avg']).item()))
  print('CPU_ONLY torch',torch.__version__,'microbatches',micro,'optimizer_steps',step_count,'gradient_comparisons',step_count,flush=True)
if __name__=='__main__':unittest.main(verbosity=2)
