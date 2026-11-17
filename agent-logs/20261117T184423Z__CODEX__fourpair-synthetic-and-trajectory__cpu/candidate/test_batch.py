"""Synthetic-only four pair tests; original source functions, fake edges."""
import hashlib
import json
from pathlib import Path
import socket
import tempfile
import unittest
import batch_synthetic
import bridge
import production_adapter

SOURCE=Path('/home/lizening/research-notes/agent-logs/20261116__CODEX__two-object-paired-eval__candidate/gate-live/eprime_ports.py')
def fixture(root):
    source=root/'inputs';source.mkdir()
    manifests={}
    for pair,_ in bridge.SCHEDULE:
        p=source/pair;p.mkdir()
        values={'game':('fabricated game '+pair).encode(),
          'routing':json.dumps({'task_type':'pick_two_obj_and_place'}).encode(),
          'config':json.dumps({'dataset':{'data_path':'REPLACE_ONLY_WITH_THIS_PARENT_PRIVATE_ROOT','num_train_games':1},
             'env':{'domain_randomization':False,'expert_type':'handcoded','goal_desc_human_anns_prob':0.0,'task_types':[6]},
             'general':{'training_method':'dqn'},'rl':{'training':{'max_nb_steps_per_episode':50}}}).encode()}
        data={}
        for k,v in values.items():
            path=p/(k+'.json');path.write_bytes(v);data[k]={'path':str(path),'sha256':hashlib.sha256(v).hexdigest()}
        manifests[pair]=data
    cases={p:{'family':'two','inputs':data} for p,data in manifests.items()}
    setup,verify,_=production_adapter.load_synthetic_bound(SOURCE,root,cases)
    return manifests,setup,verify

class BatchTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name).resolve()
        self.inputs,self.setup,self.verify=fixture(self.root);self.out=self.root/'run'
    def rows(self):return [json.loads(x) for x in (self.out/'owner'/'parent-ledger.jsonl').read_text().splitlines()]
    def test_four_pairs_eight_arms_one_shared_ledger(self):
        owner=batch_synthetic.run_batch(self.out,self.inputs,self.setup,self.verify)
        expected=[(p,a) for p,order in bridge.SCHEDULE for a in order]
        self.assertEqual(owner.finished,expected);self.assertEqual(owner.closed,set(expected))
        self.assertEqual(owner.counts,{'materialize':4,'env_construct':8,'env_init':8,'reset':8,'model_load':8,'generation':16,'step':16})
        rows=self.rows();self.assertEqual(rows[-1]['event'],'synthetic_batch_complete')
        self.assertEqual(len([r for r in rows if r['event']=='public_claim_matched']),8)
        exits=[r for r in rows if r['event']=='synthetic_child_exit'];self.assertEqual(len(exits),8)
        self.assertTrue(all(r['payload']['returncode']==0 for r in exits))
        for pair,order in bridge.SCHEDULE:
            paths=[]
            for arm in order:
                events=[json.loads(x) for x in (self.out/('arm-'+pair+'-'+arm)/'worker.jsonl').read_text().splitlines()]
                paths.append(events[0]['payload']['paths'])
                prepared=[e['payload']['public'] for e in events if e['kind']=='prepared']
                self.assertEqual(len(prepared),2)
                self.assertEqual(prepared[1]['recent_history'],[['same fake observation','fictional action']])
            self.assertEqual(paths[0],paths[1])
    def test_mid_batch_interrupt_latches_and_keeps_cost(self):
        saved=[];original=bridge.Budget
        def capturing(*a,**kw):
            obj=original(*a,**kw);saved.append(obj);return obj
        bridge.Budget=capturing
        try:
            with self.assertRaises(bridge.Stop):
                batch_synthetic.run_batch(self.out,self.inputs,self.setup,self.verify,mode_by_pair={'two':'interrupt_any'})
        finally:bridge.Budget=original
        owner=saved[0];self.assertTrue(owner.failed)
        self.assertEqual(owner.counts['materialize'],2);self.assertEqual(owner.counts['model_load'],3)
        self.assertEqual(owner.counts['generation'],4);self.assertEqual(owner.active['operation'],'model_load')
        rows=self.rows();self.assertEqual(rows[-1]['event'],'aborted')
        self.assertFalse(any(r['event']=='synthetic_batch_complete' for r in rows))
        a,b=socket.socketpair()
        try:
            with self.assertRaises(bridge.Stop):owner.serve(a,'two','A',self.out/'unused')
        finally:a.close();b.close()
        with self.assertRaises(FileExistsError):batch_synthetic.run_batch(self.out,self.inputs,self.setup,self.verify)
    def test_wrong_order_stops_before_any_setup(self):
        bad=(('one',('B','A')),)+bridge.SCHEDULE[1:]
        with self.assertRaises(bridge.Stop):batch_synthetic.run_batch(self.out,self.inputs,self.setup,self.verify,schedule=bad)
        rows=self.rows();self.assertEqual(rows[-1]['event'],'aborted')
        self.assertFalse(any(r['event']=='reserved' for r in rows))
        with self.assertRaises(FileExistsError):batch_synthetic.run_batch(self.out,self.inputs,self.setup,self.verify)
    def test_reversed_pair_second_arm_reset_mismatch_prevents_model(self):
        with self.assertRaises(bridge.Stop):
            batch_synthetic.run_batch(self.out,self.inputs,self.setup,self.verify,mode_by_pair={'two':'mismatch_A'})
        rows=self.rows();reservations=[r['payload'] for r in rows if r['event']=='reserved']
        self.assertTrue(any(r.get('pair')=='two' and r.get('arm')=='A' and r.get('operation')=='reset' for r in reservations))
        self.assertFalse(any(r.get('pair')=='two' and r.get('arm')=='A' and r.get('operation')=='model_load' for r in reservations))
        self.assertEqual(rows[-1]['event'],'aborted')
        self.assertFalse((self.out/'pair-three').exists())

if __name__=='__main__':unittest.main(verbosity=2)
