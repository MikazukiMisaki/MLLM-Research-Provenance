import copy,json,math,unittest
from pathlib import Path
import fake_stateful_sft as s
class TestFakeSFT(unittest.TestCase):
 def setUp(self):self.raw=Path(__file__).with_name('fixture.json').read_bytes()
 def test_stateful_counts_mask_causal_and_final(self):
  result=s.run_fake_fixture(self.raw);fixture=json.loads(self.raw)
  self.assertEqual((result['initialization_count'],result['optimizer_initialization_count'],result['epochs'],result['microbatches'],result['optimizer_steps']),(1,1,4,64,16))
  self.assertEqual([b['prior_optimizer']['step'] for b in result['trace']],list(range(16)))
  for i,b in enumerate(result['trace']):
   if i:self.assertEqual(result['trace'][i-1]['after_optimizer'],b['prior_optimizer'])
   self.assertEqual(b['after_optimizer']['step'],i+1)
   self.assertEqual(b['active_targets'],sum(r['target_count'] for r in b['rows']))
   for record in b['rows']:
    src=fixture['rows'][int(record['row_id'][-2:])]
    self.assertEqual(record['input_ids'],src['input_ids']);self.assertEqual(record['loss_mask'],src['loss_mask'])
    self.assertEqual(record['labels'],[-100 if m==0 else t for t,m in zip(src['input_ids'],src['loss_mask'])])
  for epoch in range(4):
   seen=[r['row_id'] for b in result['trace'] if b['epoch']==epoch for r in b['rows']]
   self.assertEqual(seen,[r['row_id'] for r in fixture['rows']])
  first=result['trace'][0];weights=result['initial_weights'];den=sum(math.exp(v) for v in weights);probs=[math.exp(v)/den for v in weights]
  targets=[t for r in first['rows'] for t in r['labels'][1:] if t!=-100]
  self.assertAlmostEqual(first['loss_sum'],sum(-math.log(probs[t]) for t in targets),places=12)
  for k in range(s.VOCAB):
   gradient=sum(probs[k]-(1 if t==k else 0) for t in targets)/len(targets)
   self.assertAlmostEqual(first['after_optimizer']['m'][k],0.1*gradient,places=12)
  self.assertNotEqual(result['trace'][0]['after_optimizer']['m'],[0.0]*s.VOCAB)
  self.assertEqual(result['final_checkpoint']['selection'],'FINAL_ONLY_NO_BEST')
  self.assertEqual(result['final_checkpoint']['optimizer'],result['trace'][-1]['after_optimizer'])
 def test_reject_altered_mask_and_real_entry(self):
  doc=json.loads(self.raw);bad=copy.deepcopy(doc);bad['rows'][0]['loss_mask'][0]=1
  with self.assertRaises(s.Invalid):s._validated_fake_rows(bad)
  bad=copy.deepcopy(doc);bad['rows'][0]['input_ids']=[0]*4097
  with self.assertRaises(s.Invalid):s._validated_fake_rows(bad)
  with self.assertRaises(s.Invalid):s.run_fake_fixture(self.raw+b' ')
  with self.assertRaises(RuntimeError):s.run_training(self.raw)
 def test_deterministic(self):self.assertEqual(s.run_fake_fixture(self.raw),s.run_fake_fixture(self.raw))
if __name__=='__main__':unittest.main(verbosity=2)
