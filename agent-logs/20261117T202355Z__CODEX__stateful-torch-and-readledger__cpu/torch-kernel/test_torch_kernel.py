import copy,json,unittest
from pathlib import Path
import torch
import torch.nn.functional as F
import torch_fixture_kernel as k
class KernelTest(unittest.TestCase):
 def setUp(self):self.raw=Path(__file__).with_name('fixture.json').read_bytes()
 def test_kernel_vs_independent_combined_reference(self):
  result=k.run_fictional_torch_cpu(self.raw);fixture=json.loads(self.raw)
  self.assertEqual((result['model_initializations'],result['optimizer_initializations'],result['microbatches'],result['optimizer_steps']),(1,1,64,16))
  previous_m=torch.zeros((4,4),dtype=torch.float64);previous_v=torch.zeros((4,4),dtype=torch.float64)
  for i,step in enumerate(result['trace']):
   self.assertEqual(step['optimizer_step'],i+1)
   self.assertEqual(step['epoch'],i//4)
   self.assertEqual([r['row_id'] for r in step['rows']],[r['row_id'] for r in fixture['rows'][4*(i%4):4*(i%4)+4]])
   if i:self.assertEqual(result['trace'][i-1]['weights_after'],step['weights_before'])
   w=torch.tensor(step['weights_before'],dtype=torch.float64,device='cpu',requires_grad=True)
   logits_list=[];labels_list=[]
   for row in step['rows']:
    src=fixture['rows'][int(row['row_id'][-2:])]
    self.assertEqual(row['input_ids'],src['input_ids']);self.assertEqual(row['loss_mask'],src['loss_mask'])
    ids=torch.tensor(row['input_ids'],dtype=torch.long,device='cpu')
    labels=torch.tensor(row['labels'],dtype=torch.long,device='cpu')
    logits_list.append((F.one_hot(ids,num_classes=4).to(dtype=torch.float64) @ w.T)[:-1]);labels_list.append(labels[1:])
   active=sum(int((x!=-100).sum().item()) for x in labels_list)
   self.assertEqual(active,step['active_targets'])
   total=F.cross_entropy(torch.cat(logits_list),torch.cat(labels_list),ignore_index=-100,reduction='sum')/active
   reference=torch.autograd.grad(total,w)[0]
   gradient=torch.tensor(step['gradient'],dtype=torch.float64)
   torch.testing.assert_close(reference,gradient,atol=1e-12,rtol=1e-12)
   previous_m=0.9*previous_m+0.1*gradient;previous_v=0.999*previous_v+0.001*gradient.square()
   torch.testing.assert_close(previous_m,torch.tensor(step['moment_1'],dtype=torch.float64),atol=1e-12,rtol=1e-12)
   torch.testing.assert_close(previous_v,torch.tensor(step['moment_2'],dtype=torch.float64),atol=1e-12,rtol=1e-12)
  self.assertEqual(result['checkpoint']['selection'],'FINAL_ONLY_NO_BEST')
  self.assertEqual(result['checkpoint']['weights'],result['trace'][-1]['weights_after'])
  self.assertEqual(result['checkpoint']['optimizer_moment_1'],result['trace'][-1]['moment_1'])
 def test_corrupt_mask_and_real_entry_rejected(self):
  doc=json.loads(self.raw);doc=copy.deepcopy(doc);doc['rows'][0]['loss_mask'][0]=1
  with self.assertRaises(k.Rejected):k._validate_fake_rows(doc)
  with self.assertRaises(k.Rejected):k.run_fictional_torch_cpu(self.raw+b' ')
  with self.assertRaises(RuntimeError):k.run_real_training(self.raw)
if __name__=='__main__':unittest.main(verbosity=2)
