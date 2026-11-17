import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import bridge
import pair_synthetic
import production_adapter

SOURCE=Path('/home/lizening/research-notes/agent-logs/20261116__CODEX__two-object-paired-eval__candidate/gate-live/eprime_ports.py')
def fixture(root):
    source=root/'inputs';source.mkdir()
    values={'game':b'fake-game-no-real-task',
            'routing':json.dumps({'task_type':'pick_two_obj_and_place'}).encode(),
            'config':json.dumps({'dataset':{'data_path':'REPLACE_ONLY_WITH_THIS_PARENT_PRIVATE_ROOT','num_train_games':1},
                    'env':{'domain_randomization':False,'expert_type':'handcoded','goal_desc_human_anns_prob':0.0,'task_types':[6]},
                    'general':{'training_method':'dqn'},'rl':{'training':{'max_nb_steps_per_episode':50}}}).encode()}
    data={}
    for k,v in values.items():
        path=source/(k+'.json');path.write_bytes(v);data[k]={'path':str(path),'sha256':hashlib.sha256(v).hexdigest()}
    cases={'fictional-case':{'family':'two','inputs':data}}
    setup,verify,_=production_adapter.load_synthetic_bound(SOURCE,root,cases)
    return data,setup,verify

class CombinedTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name).resolve()
        self.inputs,self.setup,self.verify=fixture(self.root)
        self.output=self.root/'run'
    def rows(self):
        return [json.loads(line) for line in (self.output/'owner'/'parent-ledger.jsonl').read_text().splitlines()]
    def test_one_setup_two_fake_arms_same_paths_and_state(self):
        owner=pair_synthetic.run_pair(self.output,self.inputs,self.setup,self.verify)
        self.assertEqual(owner.counts,{'materialize':1, **{op:2 for op in bridge.OPS}})
        self.assertEqual(owner.finished,['A','B']);self.assertEqual(owner.closed,{'A','B'})
        paths=[]
        for arm in ('A','B'):
            events=[json.loads(x) for x in (self.output/('arm-'+arm)/'worker.jsonl').read_text().splitlines()]
            paths.append(events[0]['payload']['paths'])
            self.assertEqual(events[0]['kind'],'synthetic_input_paths')
            self.assertIn('reset_returned',[e['kind'] for e in events])
        self.assertEqual(paths[0],paths[1]);self.assertNotEqual(self.output/'arm-A',self.output/'arm-B')
        rows=self.rows();events=[r['event'] for r in rows]
        self.assertEqual(events.count('public_claim_matched'),2)
        self.assertEqual(events.count('arm_pre_verified'),2);self.assertEqual(events.count('arm_post_verified'),2)
        self.assertEqual(events[-1],'synthetic_pair_complete')
    def test_mismatched_second_reset_never_admits_second_model(self):
        with self.assertRaises(bridge.Stop):pair_synthetic.run_pair(self.output,self.inputs,self.setup,self.verify,mode='mismatch')
        rows=self.rows()
        reserved=[r['payload'] for r in rows if r['event']=='reserved']
        self.assertEqual(sum(r.get('operation')=='model_load' for r in reserved),1)
        self.assertEqual(sum(r.get('operation')=='reset' for r in reserved),2)
        self.assertEqual(rows[-1]['event'],'aborted')
        self.assertFalse(any(r['event']=='synthetic_pair_complete' for r in rows))
        with self.assertRaises(FileExistsError):pair_synthetic.run_pair(self.output,self.inputs,self.setup,self.verify)
    def test_interrupted_reserved_model_stays_charged(self):
        with self.assertRaises(bridge.Stop):pair_synthetic.run_pair(self.output,self.inputs,self.setup,self.verify,mode='interrupt')
        rows=self.rows();reserved=[r for r in rows if r['event']=='reserved' and r['payload'].get('operation')=='model_load']
        returned=[r for r in rows if r['event']=='returned' and r['payload'].get('operation')=='model_load']
        self.assertEqual(len(reserved),1);self.assertEqual(len(returned),0)
        self.assertEqual(rows[-1]['payload']['active']['operation'],'model_load')
        self.assertFalse((self.output/'arm-B').exists())
    def test_post_arm_tamper_prevents_second_arm(self):
        def tamper(arm,paths):
            if arm=='A':Path(paths[0]).write_bytes(b'fake tampering')
        with self.assertRaises(ValueError):pair_synthetic.run_pair(self.output,self.inputs,self.setup,self.verify,hook=tamper)
        self.assertFalse((self.output/'arm-B').exists());self.assertEqual(self.rows()[-1]['event'],'aborted')

if __name__=='__main__':unittest.main(verbosity=2)
