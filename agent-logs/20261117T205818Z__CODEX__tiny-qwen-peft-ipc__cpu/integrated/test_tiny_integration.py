import hashlib,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from safetensors import safe_open
import parent_bridge as parent
class Integration(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name).resolve()
 def verify_fake(self,root):
  d=root/'fake_final';path=d/'fictional.safetensors';receipt=json.loads((d/'receipt.json').read_text())
  digest=hashlib.sha256(path.read_bytes()).hexdigest();self.assertEqual(receipt['sha256'],digest)
  self.assertEqual(receipt['status'],'RELOAD_CHECKED_CALLBACK_RETURN_REQUIRED')
  with safe_open(str(path),framework='pt',device='cpu') as data:
   self.assertEqual(data.metadata()['scope'],'FICTIONAL_CPU_ONLY_NOT_LORA_NOT_SCIENCE');self.assertEqual(data.metadata()['step'],'16')
   keys=list(data.keys());self.assertEqual(len(keys),14);self.assertTrue(all(x.startswith('fictional.') and 'lora_' in x for x in keys))
  return digest
 def test_tiny_peft_success_exact_ipc_and_reload(self):
  root=self.root/'success'
  with patch.dict(os.environ,{'FAKE_CHECKPOINT_SCENARIO':'normal','HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1'}):r=parent.run_fake(root,'normal')
  self.assertEqual(r['outcome'],'FICTIONAL_COMPLETE',str(r));self.assertEqual(r['returncode'],0);self.assertEqual(r['counts'],parent.CAPS)
  digest=self.verify_fake(root);events=[json.loads(x) for x in (root/'worker_events.jsonl').read_text().splitlines()]
  result=next(x['payload'] for x in events if x['kind']=='fake_run_result');receipt=result['callback_receipt']
  self.assertEqual(receipt['sha256'],digest);self.assertEqual(receipt['callback_status'],'CONFIRMED_FICTIONAL_ONLY')
  self.assertEqual(receipt['fixture_adapter_mapping'],'PREFIXED_STATE_DICT_NOT_PEFT_EXPORT')
  self.assertTrue(receipt['base_unchanged']);self.assertTrue(receipt['lora_changed']);self.assertTrue(receipt['adapter_reload_exact'])
  self.assertLessEqual(receipt['logits_max_abs'],1e-6)
 def test_interrupted_after_save_is_unknown(self):
  root=self.root/'interrupt'
  with patch.dict(os.environ,{'FAKE_CHECKPOINT_SCENARIO':'interrupt_after_checkpoint','HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1'}):r=parent.run_fake(root,'normal')
  self.assertEqual((r['outcome'],r['returncode'],r['active']),('UNKNOWN',24,(162,'checkpoint_final')),str(r))
  self.assertEqual(r['counts']['optimizer_step'],16);digest=self.verify_fake(root)
  events=[json.loads(x) for x in (root/'worker_events.jsonl').read_text().splitlines()]
  self.assertFalse(any(x['kind'] in ('checkpoint_final_returned','fake_run_result') for x in events))
  with self.assertRaises(FileExistsError):parent.run_fake(root,'normal')
  self.assertEqual(digest,self.verify_fake(root))
  with self.assertRaises(RuntimeError):parent.dispatch_real()
if __name__=='__main__':unittest.main(verbosity=2)
