import hashlib,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from safetensors import safe_open
import parent_bridge as parent
HERE=Path(__file__).resolve().parent
class Integration(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name).resolve()
 def verify_checkpoint(self,root):
  checkpoint=root/'fake_final';artifact=checkpoint/'fictional.safetensors';receipt=json.loads((checkpoint/'receipt.json').read_text())
  digest=hashlib.sha256(artifact.read_bytes()).hexdigest();self.assertEqual(receipt['sha256'],digest)
  self.assertEqual(receipt['status'],'RELOAD_CHECKED_CALLBACK_RETURN_REQUIRED')
  with safe_open(str(artifact),framework='pt',device='cpu') as data:
   self.assertEqual(data.metadata()['scope'],'FICTIONAL_CPU_ONLY_NOT_LORA_NOT_SCIENCE');self.assertEqual(data.metadata()['step'],'16')
   self.assertEqual(list(data.keys()),['fictional.weight']);self.assertEqual(tuple(data.get_tensor('fictional.weight').shape),(5,5))
  return digest
 def test_success_final_callback_receipt(self):
  self.assertEqual(hashlib.sha256((HERE/'parent_bridge.py').read_bytes()).hexdigest(),'d28069bcfaa61f349be0633e8e66ab166066ec831712db0a7e19e2aa06daea2e')
  root=self.root/'success'
  with patch.dict(os.environ,{'FAKE_CHECKPOINT_SCENARIO':'normal'}):r=parent.run_fake(root,'normal')
  self.assertEqual(r['outcome'],'FICTIONAL_COMPLETE');self.assertEqual(r['returncode'],0);self.assertEqual(r['counts'],parent.CAPS)
  digest=self.verify_checkpoint(root)
  events=[json.loads(x) for x in (root/'worker_events.jsonl').read_text().splitlines()]
  self.assertTrue(any(x['kind']=='fake_checkpoint_scenario' and x['payload']['scenario']=='normal' for x in events))
  result=[x['payload'] for x in events if x['kind']=='fake_run_result']
  self.assertEqual(len(result),1);self.assertEqual(result[0]['callback_receipt']['sha256'],digest)
  self.assertEqual(result[0]['callback_receipt']['callback_status'],'CONFIRMED_FICTIONAL_ONLY')
  self.assertEqual(sum(x['kind']=='checkpoint_final_returned' for x in events),1)
 def test_interrupted_after_write_no_retry_or_overwrite(self):
  root=self.root/'interrupted'
  with patch.dict(os.environ,{'FAKE_CHECKPOINT_SCENARIO':'interrupt_after_checkpoint'}):r=parent.run_fake(root,'normal')
  self.assertEqual(r['outcome'],'UNKNOWN');self.assertEqual(r['returncode'],24);self.assertEqual(r['active'],(162,'checkpoint_final'))
  self.assertEqual(r['counts']['optimizer_step'],16);self.assertEqual(r['counts']['checkpoint_final'],1)
  digest=self.verify_checkpoint(root)
  events=[json.loads(x) for x in (root/'worker_events.jsonl').read_text().splitlines()]
  self.assertTrue(any(x['kind']=='fake_checkpoint_scenario' and x['payload']['scenario']=='interrupt_after_checkpoint' for x in events))
  self.assertFalse(any(x['kind'] in ('checkpoint_final_returned','fake_run_result') for x in events))
  ledger=[json.loads(x) for x in (root/'parent.jsonl').read_text().splitlines()]
  self.assertTrue(any(x['kind']=='stopped_unknown' and x['payload']['no_refund'] for x in ledger))
  with self.assertRaises(FileExistsError):parent.run_fake(root,'normal')
  self.assertEqual(digest,self.verify_checkpoint(root))
  with self.assertRaises(RuntimeError):parent.dispatch_real()
if __name__=='__main__':unittest.main(verbosity=2)
