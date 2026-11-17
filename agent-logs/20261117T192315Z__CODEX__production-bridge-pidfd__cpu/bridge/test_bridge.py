import hashlib
import json
from pathlib import Path
import tempfile
import subprocess
import unittest
from unittest.mock import patch
import global_owner
import production_adapter
import bridge

PORT=Path('/home/lizening/research-notes/agent-logs/20261116__CODEX__two-object-paired-eval__candidate/gate-live/eprime_ports.py')
def fixture(root):
    source=root/'inputs';source.mkdir();manifests={}
    for case,_ in global_owner.SCHEDULE:
        directory=source/case;directory.mkdir()
        values={'game':('fake game '+case).encode(),
          'routing':json.dumps({'task_type':'pick_two_obj_and_place'}).encode(),
          'config':json.dumps({'dataset':{'data_path':'REPLACE_ONLY_WITH_THIS_PARENT_PRIVATE_ROOT','num_train_games':1},
          'env':{'domain_randomization':False,'expert_type':'handcoded','goal_desc_human_anns_prob':0.0,'task_types':[6]},
          'general':{'training_method':'dqn'},'rl':{'training':{'max_nb_steps_per_episode':50}}}).encode()}
        data={}
        for k,v in values.items():
            p=directory/(k+'.json');p.write_bytes(v);data[k]={'path':str(p),'sha256':hashlib.sha256(v).hexdigest()}
        manifests[case]=data
    cases={case:{'family':'two','inputs':data} for case,data in manifests.items()}
    setup,verify,_=production_adapter.load_synthetic_bound(PORT,root,cases)
    return manifests,setup,verify

class BridgeTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name).resolve();self.inputs,self.setup,self.verify=fixture(self.root);self.out=self.root/'run'
    def rows(self):return [json.loads(line) for line in (self.out/'owner'/'global.jsonl').read_text().splitlines()]
    def test_four_pairs_real_episode_and_fictional_edges(self):
        owner=bridge.run_synthetic_bridge(self.out,self.root,self.inputs,self.setup,self.verify)
        self.assertEqual(owner.counts,{'materialize':4,'env_construct':8,'env_init':8,'reset':8,'model_load':8,'generation':8,'step':8})
        self.assertEqual(owner.tokens,{'input':8*4096,'output':8*16})
        self.assertTrue(owner.completed)
        with self.assertRaises(RuntimeError):bridge.launch_production()
        cli=[r['payload'] for r in self.rows() if r['event']=='synthetic_worker_cli']
        self.assertEqual(len(cli),8)
        closed=[r['payload'] for r in self.rows() if r['event']=='arm_closed']
        self.assertEqual(len(closed),8)
        for i,(case,order) in enumerate(global_owner.SCHEDULE):
            a,b=closed[2*i:2*i+2]
            self.assertEqual((a['case'],a['arm']),(case,order[0]))
            self.assertEqual(a['child_result_claim']['initial_public'],b['child_result_claim']['initial_public'])
            for arm in order:
                cfg=json.loads((self.out/(case+'-'+arm)/'config.json').read_text())
                self.assertEqual(cfg['case'],case);self.assertEqual(cfg['arm'],arm);self.assertEqual(cfg['synthetic_test_context']['classification'],'FAKE_CPU_ONLY')
                self.assertIn('manifest_sha256',cfg);self.assertIn('pair_binding',cfg);self.assertIn('runtime',cfg)
                events=[json.loads(line) for line in (self.out/(case+'-'+arm)/'output'/'worker_events.jsonl').read_text().splitlines()]
                kinds=[e['kind'] for e in events]
                for name in ('synthetic_cli_config_verified','synthetic_boundaries_scope','reset_returned','prepared','generation_returned','dev_parser_returned','step_returned','dev_decision_committed','fixed_product_episode_outcome_known','fixed_product_arm_result'):
                    self.assertIn(name,kinds)
                self.assertTrue(kinds.index('prepared')<kinds.index('dev_parser_returned')<kinds.index('step_returned'))
        self.assertNotEqual(closed[0]['child_result_claim']['initial_public'],closed[2]['child_result_claim']['initial_public'])
    def test_second_arm_reset_mismatch_stops_before_model_load(self):
        case=global_owner.SCHEDULE[0][0]
        with self.assertRaises(Exception):
            bridge.run_synthetic_bridge(self.out,self.root,self.inputs,self.setup,self.verify,mode_by_case={case:'mismatch'})
        rows=self.rows();reserve=[r['payload'] for r in rows if r['event']=='reserve']
        self.assertEqual(sum(r['operation']=='materialize' for r in reserve),1)
        self.assertEqual(sum(r['operation']=='model_load' for r in reserve),1)
        self.assertEqual(sum(r['operation']=='generation' for r in reserve),1)
        self.assertEqual(sum(r['operation']=='step' for r in reserve),1)
        self.assertTrue(any(r['event']=='aborted' for r in rows))
        self.assertFalse(any(r['event']=='synthetic_batch_complete' for r in rows))
if __name__=='__main__':unittest.main(verbosity=2)
