import copy,hashlib,json,unittest
from pathlib import Path
import fixture_adapter as a
class TestFixture(unittest.TestCase):
 def setUp(self):
  self.raw=Path(__file__).with_name('fixture.json').read_bytes();self.fixture=json.loads(self.raw)
 def test_exact_fixture_preserves_all_tokens_and_mask(self):
  self.assertEqual(hashlib.sha256(self.raw).hexdigest(),a.FIXTURE_SHA256)
  out=a.convert_fixture(self.raw);self.assertFalse(out['trainer_compatible']);self.assertEqual(out['scientific_use'],'HOLD')
  for original,converted in zip(self.fixture['rows'],out['rows']):
   refs=original['selection']['refs'];p=self.fixture['objects'][refs['prompt_ref']]['input_ids'];m=self.fixture['objects'][refs['mask_ref']]
   self.assertEqual(converted['prompt'],p);self.assertEqual(converted['input_ids'],m['sequence_ids']);self.assertEqual(converted['loss_mask'],m['loss_mask'])
   self.assertEqual(converted['labels'],[-100,-100,101,151645])
 def test_changed_or_unauthenticated_input_never_accepted(self):
  with self.assertRaises(a.Rejected):a.convert_fixture(self.raw+b' ')
  with self.assertRaises(a.Rejected):a.convert_fixture(b'{"AUTHENTICATED": true}')
  with self.assertRaises(RuntimeError):a.convert_for_training(self.raw)
 def test_fixture_alias_mismatch_and_truncation_rejected(self):
  bad=copy.deepcopy(self.fixture);bad['rows'][1]['selection']['refs']['prompt_ref']=bad['rows'][0]['selection']['refs']['prompt_ref']
  with self.assertRaises(a.Rejected):a._project_fake(bad)
  bad=copy.deepcopy(self.fixture);bad['objects']['target-mask']['loss_mask']=[0,1,1,1]
  with self.assertRaises(a.Rejected):a._project_fake(bad)
  bad=copy.deepcopy(self.fixture);bad['objects']['target-prompt']['input_ids']=[1]*4096
  with self.assertRaises(a.Rejected):a._project_fake(bad)
if __name__=='__main__':unittest.main(verbosity=2)
