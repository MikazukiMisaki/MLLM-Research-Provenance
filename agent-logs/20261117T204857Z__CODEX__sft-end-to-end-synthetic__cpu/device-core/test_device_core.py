import json,types,unittest
from pathlib import Path
import torch
import torch.nn.functional as F
import device_core as core
class TinyCPU(torch.nn.Module):
 def __init__(self):super().__init__();self.weight=torch.nn.Parameter(torch.zeros((5,5),dtype=torch.float32))
 def forward(self,*,input_ids,attention_mask,use_cache):
  return types.SimpleNamespace(logits=F.one_hot(input_ids,num_classes=5).to(torch.float32) @ self.weight)
class FakeOwner:
 def __init__(self,interrupt=False):self.events=[];self.interrupt=interrupt
 def reserve(self,kind,request):self.events.append(('reserve',kind));return len(self.events)
 def returned(self,ticket,kind,receipt):
  self.events.append(('returned',kind))
  if self.interrupt and kind=='optimizer_step':raise RuntimeError('FICTIONAL interrupted acknowledgement')
 def unknown(self,ticket,kind,error_type):self.events.append(('unknown',kind))
class TestCore(unittest.TestCase):
 def setUp(self):
  self.rows=json.loads(Path(__file__).with_name('fixture.json').read_text())['rows'];self.model=TinyCPU()
  self.opt=torch.optim.AdamW(self.model.parameters(),lr=3e-5,betas=(0.9,0.999),eps=1e-8,weight_decay=0.0,amsgrad=False,foreach=False,capturable=False,maximize=False,fused=False)
  self.saved=[]
 def call(self,owner):
  return core.run_injected_core(model=self.model,optimizer=self.opt,rows=self.rows,owner=owner,
    checkpoint_writer=lambda m,o,meta:self.saved.append(meta) or {'scope':'FAKE'},vocab_size=5,eos_token_id=3,pad_token_id=4)
 def test_cpu_positive(self):
  owner=FakeOwner();out=self.call(owner)
  self.assertEqual((out['metadata']['microbatches'],out['metadata']['optimizer_steps']),(64,16))
  self.assertEqual(int(self.opt.state[self.model.weight]['step'].item()),16)
  for kind,count in [('validate_model',1),('set_train_mode',1),('zero_grad',16),('forward',64),('backward',64),('optimizer_step',16),('checkpoint_final',1)]:
   self.assertEqual(owner.events.count(('reserve',kind)),count);self.assertEqual(owner.events.count(('returned',kind)),count)
  self.assertEqual(len(self.saved),1);self.assertEqual(self.saved[0]['selection'],'FINAL_ONLY_NO_BEST')
 def test_interrupted_step_is_unknown_and_no_retry(self):
  owner=FakeOwner(interrupt=True)
  with self.assertRaisesRegex(RuntimeError,'interrupted'):self.call(owner)
  self.assertEqual(int(self.opt.state[self.model.weight]['step'].item()),1)
  self.assertEqual(owner.events.count(('reserve','optimizer_step')),1)
  self.assertIn(('unknown','optimizer_step'),owner.events);self.assertFalse(self.saved)
  with self.assertRaises(RuntimeError):core.dispatch_real()
if __name__=='__main__':unittest.main(verbosity=2)
