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
            kinds=[e['kind'] for e in events]
            for name in ('synthetic_source_bindings','prepared','generation_returned','dev_parser_returned','step_returned','fixed_product_episode_outcome_known','synthetic_observed_episode_returned'):
                self.assertIn(name,kinds)
            selection=next(e['payload']['result'] for e in events if e['kind']=='dev_parser_returned')
            self.assertEqual(selection['action_id'],'A000')
            self.assertEqual(selection['selection_status'],'selected')
            result=next(e['payload']['result'] for e in events if e['kind']=='synthetic_observed_episode_returned')
            self.assertEqual((result['won'],result['steps'],result['termination']),(True,1,'TERMINAL'))
            generated=next(e['payload']['evidence'] for e in events if e['kind']=='generation_returned')
            self.assertEqual(generated['output_ids'],[99,151645])
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

    def test_tuple_origin_claim_matches_serialized_real_shape(self):
        owner=pair_synthetic.run_pair(self.output,self.inputs,self.setup,self.verify,mode='tuple')
        self.assertEqual(owner.finished,['A','B'])
        for arm in ('A','B'):
            rows=[json.loads(line) for line in (self.output/('arm-'+arm)/'worker.jsonl').read_text().splitlines()]
            reset=next(row for row in rows if row['kind']=='reset_returned')
            self.assertEqual(reset['payload']['evidence']['candidate_native_reset'],
                             {'won_batch':[False],'won_batch_type':'tuple'})

    def test_real_shape_list_origin_is_explicit(self):
        pair_synthetic.run_pair(self.output,self.inputs,self.setup,self.verify)
        rows=[json.loads(line) for line in (self.output/'arm-A'/'worker.jsonl').read_text().splitlines()]
        reset=next(row for row in rows if row['kind']=='reset_returned')
        self.assertEqual(reset['payload']['evidence']['candidate_native_reset'],
                         {'won_batch':[False],'won_batch_type':'list'})

    def test_malformed_or_true_claims_stop_before_second_model_and_keep_cost(self):
        for mode in ('bad_true','bad_integer','bad_type','bad_missing','bad_extra','bad_length'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as temp:
                root=Path(temp).resolve();inputs,setup,verify=fixture(root);out=root/'run'
                with self.assertRaises(bridge.Stop):pair_synthetic.run_pair(out,inputs,setup,verify,mode=mode)
                rows=[json.loads(line) for line in (out/'owner'/'parent-ledger.jsonl').read_text().splitlines()]
                reserved=[r['payload'] for r in rows if r['event']=='reserved']
                returned=[r['payload'] for r in rows if r['event']=='returned']
                self.assertEqual(sum(r.get('operation')=='materialize' for r in reserved),1)
                self.assertEqual(sum(r.get('operation')=='reset' for r in reserved),2)
                self.assertEqual(sum(r.get('operation')=='reset' for r in returned),2)
                self.assertEqual(sum(r.get('operation')=='model_load' for r in reserved),1)
                self.assertEqual(rows[-1]['event'],'aborted')
                self.assertFalse(any(r['event']=='synthetic_pair_complete' for r in rows))
                with self.assertRaises(FileExistsError):pair_synthetic.run_pair(out,inputs,setup,verify,mode=mode)

    def test_real_parser_rejects_bad_synthetic_output_without_step(self):
        owner=pair_synthetic.run_pair(self.output,self.inputs,self.setup,self.verify,mode='bad_format')
        self.assertEqual(owner.counts['step'],0)
        for arm in ('A','B'):
            rows=[json.loads(line) for line in (self.output/('arm-'+arm)/'worker.jsonl').read_text().splitlines()]
            selection=next(e['payload']['result'] for e in rows if e['kind']=='dev_parser_returned')
            self.assertEqual(selection['selection_status'],'action_format_violation')
            result=next(e['payload']['result'] for e in rows if e['kind']=='synthetic_observed_episode_returned')
            self.assertEqual((result['won'],result['steps'],result['termination']),(False,0,'POLICY_FAILURE'))

if __name__=='__main__':unittest.main(verbosity=2)
