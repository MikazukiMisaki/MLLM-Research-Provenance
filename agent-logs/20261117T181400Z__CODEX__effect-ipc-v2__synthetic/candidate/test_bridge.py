import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest
import bridge

HERE=Path(__file__).parent
class BridgeTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
    def budget(self,**caps):return bridge.Budget(self.root/'budget',caps)
    def run_child(self,budget,arm,mode='normal',rogue=False):
        parent,child=socket.socketpair()
        log=budget.root.parent/('worker-'+arm+'.jsonl')
        script='rogue_client.py' if rogue else 'fake_client.py'
        args=[sys.executable,'-I','-B',str(HERE/script),str(child.fileno())]
        if not rogue:args.append(str(log))
        args.append(mode)
        proc=subprocess.Popen(args,pass_fds=(child.fileno(),),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        child.close()
        try:budget.serve(parent,arm,log)
        finally:
            parent.close()
            try:proc.wait(timeout=8)
            except subprocess.TimeoutExpired:
                proc.terminate();proc.wait(timeout=3)
        return proc.returncode,log
    def test_two_real_protocol_clients_share_total_counts(self):
        b=self.budget(model_load=2,generation=2)
        for arm in ('A','B'):
            rc,log=self.run_child(b,arm)
            self.assertEqual(rc,0);self.assertTrue(log.exists())
        self.assertEqual(b.counts,{'model_load':2,'generation':2})
        self.assertEqual(b.finished,['A','B']);self.assertFalse(b.failed)
        rows=[json.loads(x) for x in b.path.read_text().splitlines()]
        self.assertEqual([r['event'] for r in rows].count('reserved'),4)
        self.assertEqual([r['event'] for r in rows].count('returned'),4)
        with self.assertRaises(bridge.Stop): bridge.Budget(self.root/'budget',{'generation':1})
    def test_disconnect_after_ack_retains_reservation(self):
        b=self.budget(model_load=2,generation=2)
        with self.assertRaises(bridge.Stop):self.run_child(b,'A','interrupt')
        self.assertTrue(b.failed);self.assertEqual(b.counts['model_load'],1)
        self.assertEqual(b.active['operation'],'model_load')
        with self.assertRaises(bridge.Stop):self.run_child(b,'B')
    def test_real_client_unknown_aborts(self):
        b=self.budget(model_load=2,generation=2)
        with self.assertRaises(bridge.Stop):self.run_child(b,'A','unknown')
        self.assertTrue(b.failed);self.assertEqual(b.counts['model_load'],1)
        rows=[json.loads(x) for x in b.path.read_text().splitlines()]
        self.assertIn('unknown',[r['event'] for r in rows])
        with self.assertRaises(bridge.Stop):self.run_child(b,'B')
    def test_shared_cap_stops_second_child(self):
        b=self.budget(model_load=2,generation=1)
        self.run_child(b,'A')
        with self.assertRaises(bridge.Stop):self.run_child(b,'B')
        self.assertTrue(b.failed);self.assertEqual(b.counts['generation'],1)
    def test_wrong_arm_order_stops_batch(self):
        b=self.budget(model_load=2,generation=2)
        with self.assertRaises(bridge.Stop):self.run_child(b,'B')
        self.assertTrue(b.failed)
        with self.assertRaises(bridge.Stop):self.run_child(b,'A')

    def test_malformed_order_duplicate_and_fake_receipt_fail(self):
        for mode in ('sequence','duplicate','unknown_kind','bad_receipt','early_finish','pipeline'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                b=bridge.Budget(Path(tmp)/'budget',{'generation':2})
                with self.assertRaises(bridge.Stop):self.run_child(b,'A',mode,True)
                self.assertTrue(b.failed)
                if mode in ('duplicate','bad_receipt','pipeline'):
                    self.assertEqual(b.counts['generation'],1);self.assertIsNotNone(b.active)

    def test_short_write_ack_with_original_client(self):
        lengths=[]
        def sender(sock,data):
            def short(view):
                n=sock.send(view[:1]);lengths.append(n);return n
            bridge.send_all(sock,data,short)
        b=bridge.Budget(self.root/'budget',{'model_load':2,'generation':2},ack_sender=sender)
        for arm in ('A','B'):
            rc,_=self.run_child(b,arm,'interleaved')
            self.assertEqual(rc,0)
        self.assertGreater(len(lengths),10)
        self.assertTrue(all(n==1 for n in lengths))
        self.assertEqual(b.finished,['A','B'])

    def test_existing_ledger_without_claim_refuses_reuse(self):
        target=self.root/'budget';target.mkdir()
        data=b'existing incomplete journal\n';(target/'parent-ledger.jsonl').write_bytes(data)
        with self.assertRaises(bridge.Stop): bridge.Budget(target,{'generation':1})
        self.assertEqual((target/'parent-ledger.jsonl').read_bytes(),data)
        self.assertFalse((target/'claim').exists())

    def test_baseexception_permanently_latches_owner(self):
        b=self.budget(model_load=2,generation=2)
        original=bridge.valid_receipt
        def interrupted(*args): raise SystemExit('synthetic interruption')
        bridge.valid_receipt=interrupted
        try:
            with self.assertRaises(bridge.Stop): self.run_child(b,'A')
        finally: bridge.valid_receipt=original
        self.assertTrue(b.failed)
        self.assertEqual(b.counts['model_load'],1)
        self.assertEqual(b.active['operation'],'model_load')
        with self.assertRaises(bridge.Stop): self.run_child(b,'B')

    def test_parent_per_arm_cap_not_child_cap(self):
        b=self.budget(model_load=2,generation=2)
        with self.assertRaises(bridge.Stop): self.run_child(b,'A','over_arm')
        self.assertTrue(b.failed)
        self.assertEqual(b.arm_counts['A']['generation'],1)
        self.assertEqual(b.counts['generation'],1)

    def test_duplicate_prior_lifecycle_rejected(self):
        b=self.budget(model_load=2,generation=2)
        with self.assertRaises(bridge.Stop):self.run_child(b,'A','old_duplicate')
        self.assertTrue(b.failed);self.assertEqual(b.counts['generation'],1)
        self.assertEqual(b.active['operation'],'generation')

    def test_claimed_return_needs_matching_start_same_operation(self):
        for mode in ('orphan','wrong_started'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                b=bridge.Budget(Path(tmp)/'budget',{'model_load':2,'generation':2})
                with self.assertRaises(bridge.Stop):self.run_child(b,'A',mode)
                self.assertTrue(b.failed);self.assertIsNotNone(b.active)
                self.assertEqual(b.counts['generation'],1)

if __name__=='__main__':unittest.main(verbosity=2)
