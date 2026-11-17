import copy,json,unittest,types
from pathlib import Path
import torch
import torch.nn.functional as F
import stateful_core as core
class TinyCPU(torch.nn.Module):
 def __init__(self,nonfinite=False):
  super().__init__();self.weight=torch.nn.Parameter(torch.zeros((5,5),dtype=torch.float32,device='cpu'));self.nonfinite=nonfinite
 def forward(self,*,input_ids,attention_mask,use_cache):
  logits=F.one_hot(input_ids,num_classes=5).to(torch.float32) @ self.weight
  if self.nonfinite:logits=logits*torch.tensor(float('nan'))
  return types.SimpleNamespace(logits=logits)
class Tests(unittest.TestCase):
 def setUp(self):
  self.rows=json.loads(Path(__file__).with_name('fixture.json').read_text())['rows']
  self.calls=[]
 def callback(self,model,optimizer,metadata):
  self.calls.append({'model_id':id(model),'optimizer_step':int(optimizer.state[model.weight]['step'].item()),'metadata':metadata})
  return {'scope':'FICTIONAL_RECEIPT'}
 def test_actual_candidate_one_optimizer_and_final_callback(self):
  model=TinyCPU();out=core.run_cpu_research_core(model=model,rows=self.rows,checkpoint_writer=self.callback,vocab_size=5,eos_token_id=3,pad_token_id=4)
  self.assertEqual(out['metadata'],{'selection':'FINAL_ONLY_NO_BEST','seed':42,'epochs':4,'microbatches':64,'optimizer_steps':16})
  self.assertEqual(len(self.calls),1);self.assertEqual(self.calls[0]['model_id'],id(model));self.assertEqual(self.calls[0]['optimizer_step'],16)
  self.assertEqual([x['optimizer_step'] for x in out['history']],list(range(1,17)))
  for e in range(4):
   self.assertEqual([r for step in out['history'] if step['epoch']==e for r in step['row_ids']],[r['row_id'] for r in self.rows])
 def test_bad_mask_and_nonfinite_fail_before_checkpoint(self):
  bad=copy.deepcopy(self.rows);bad[0]['loss_mask'][0]=1
  with self.assertRaises(core.Stop):core.run_cpu_research_core(model=TinyCPU(),rows=bad,checkpoint_writer=self.callback,vocab_size=5,eos_token_id=3,pad_token_id=4)
  with self.assertRaisesRegex(core.Stop,'nonfinite loss'):core.run_cpu_research_core(model=TinyCPU(nonfinite=True),rows=self.rows,checkpoint_writer=self.callback,vocab_size=5,eos_token_id=3,pad_token_id=4)
  self.assertFalse(self.calls)
  with self.assertRaises(RuntimeError):core.run_real_training(authenticated=True)
if __name__=='__main__':unittest.main(verbosity=2)
