"""Fictional CPU-only tensor tests; no real model or training."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import torch
from safetensors import safe_open
import final_checkpoint as candidate

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name).resolve();self.output=self.root/'final'
        self.values={'fictional.weight':torch.tensor([[0.0,1.25],[-2.0,3.0]],device='cpu'),
                     'fictional.count':torch.tensor([1,2],dtype=torch.int64,device='cpu')}
    def test_final_save_reload_and_duplicate(self):
        cb=candidate.FictionalFinalCheckpoint(self.output)
        result=cb(16,self.values)
        self.assertEqual(cb.status,'CONFIRMED_FICTIONAL_ONLY');self.assertEqual(result['callback_status'],cb.status)
        self.assertEqual(result['sha256'],candidate.sha_file(self.output/'fictional.safetensors'))
        stored=json.loads((self.output/'receipt.json').read_text())
        self.assertEqual(stored['status'],'RELOAD_CHECKED_CALLBACK_RETURN_REQUIRED')
        with safe_open(str(self.output/'fictional.safetensors'),framework='pt',device='cpu') as r:
            for key,value in self.values.items():self.assertTrue(torch.equal(r.get_tensor(key),value))
        with self.assertRaises(candidate.CheckpointRejected):cb(16,self.values)
    def test_nonfinal_and_existing_target_rejected(self):
        cb=candidate.FictionalFinalCheckpoint(self.output)
        with self.assertRaises(candidate.CheckpointRejected):cb(15,self.values)
        self.assertFalse(self.output.exists());self.assertEqual(cb.status,'REJECTED')
        self.output.mkdir();(self.output/'keep').write_text('fictional')
        cb2=candidate.FictionalFinalCheckpoint(self.output)
        with self.assertRaises(candidate.CheckpointRejected):cb2(16,self.values)
        self.assertEqual((self.output/'keep').read_text(),'fictional')
    def test_interrupt_keeps_unknown_no_retry(self):
        cb=candidate.FictionalFinalCheckpoint(self.output)
        def interrupt():raise KeyboardInterrupt()
        with self.assertRaises(KeyboardInterrupt):cb(16,self.values,after_temp_sync=interrupt)
        self.assertEqual(cb.status,'UNKNOWN');self.assertFalse(self.output.exists())
        self.assertTrue(cb.temp_path.is_dir());self.assertTrue((cb.temp_path/'fictional.safetensors').exists())
        with self.assertRaises(candidate.CheckpointRejected):cb(16,self.values)
    def test_target_created_during_save_is_not_overwritten(self):
        cb=candidate.FictionalFinalCheckpoint(self.output)
        def occupy():self.output.mkdir();(self.output/'keep').write_text('fictional')
        with self.assertRaises(FileExistsError):cb(16,self.values,after_temp_sync=occupy)
        self.assertEqual(cb.status,'UNKNOWN');self.assertEqual((self.output/'keep').read_text(),'fictional')
        self.assertTrue(cb.temp_path.is_dir())
    def test_failed_final_sync_does_not_claim_confirmation(self):
        cb=candidate.FictionalFinalCheckpoint(self.output);real=candidate.fsync_dir
        def fail_final(path):
            if Path(path)==self.output:raise OSError('fictional final fsync failure')
            real(path)
        with mock.patch.object(candidate,'fsync_dir',side_effect=fail_final):
            with self.assertRaises(OSError):cb(16,self.values)
        self.assertEqual(cb.status,'UNKNOWN');self.assertIsNone(cb.receipt)
        stored=json.loads((self.output/'receipt.json').read_text())
        self.assertEqual(stored['status'],'RELOAD_CHECKED_CALLBACK_RETURN_REQUIRED')
        with self.assertRaises(candidate.CheckpointRejected):cb(16,self.values)

if __name__=='__main__':unittest.main(verbosity=2)
