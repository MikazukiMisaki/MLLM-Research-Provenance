"""Actual pinned port functions, temporary fake cases, no environment/model/GPU."""
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
import candidate
import production_adapter as adapter
from test_candidate import spawn_for

SOURCE=Path('/home/lizening/research-notes/agent-logs/20261116__CODEX__two-object-paired-eval__candidate/gate-live/eprime_ports.py')

def make_fixture(root,case):
    base=root/case; base.mkdir()
    objects={'game':b'synthetic game; not ALFWorld data',
             'routing':json.dumps({'task_type':'pick_two_obj_and_place'}).encode(),
             'config':json.dumps({'dataset':{'data_path':'REPLACE_ONLY_WITH_THIS_PARENT_PRIVATE_ROOT','num_train_games':1},
                 'env':{'domain_randomization':False,'expert_type':'handcoded','goal_desc_human_anns_prob':0.0,'task_types':[6]},
                 'general':{'training_method':'dqn'},'rl':{'training':{'max_nb_steps_per_episode':50}}}).encode()}
    result={}
    for key,value in objects.items():
        path=base/(key+'.json');path.write_bytes(value)
        result[key]={'path':str(path),'sha256':hashlib.sha256(value).hexdigest()}
    return result

class AdapterTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name).resolve()
        self.fixture=self.root/'inputs';self.fixture.mkdir()
        self.manifests={key:make_fixture(self.fixture,key) for key in candidate.PAIRS}
        self.cases={key:{'family':'two','inputs':manifest} for key,manifest in self.manifests.items()}
        self.setup_port,self.verify_port,self.module=adapter.load_synthetic_bound(SOURCE,self.root,self.cases)
        self.owner=candidate.Owner(self.root/'out')

    def test_four_pairs_actual_production_ports_fake_cases(self):
        seen=[]
        for pair,order in candidate.SCHEDULE:
            candidate.pair(self.owner,pair,order,self.manifests[pair],self.setup_port,self.verify_port,spawn_for(seen=seen))
        self.owner.complete()
        entries=[json.loads(line) for line in self.owner.log.read_text().splitlines()]
        details=[e['data']['event'] for e in entries if e['type']=='setup_detail']
        self.assertEqual(details.count('eprime_materialization_started'),4)
        self.assertEqual(details.count('eprime_materialization_returned'),4)
        self.assertEqual(details.count('eprime_byte_verification_returned'),16)
        self.assertEqual(self.owner.count['materialize'],4)
        self.assertEqual(len(seen),8)
        self.assertTrue(all([seen[i][2]==seen[i+1][2] for i in range(0,8,2)]))
        self.assertIs(self.module.CASES,self.cases)
        self.assertEqual(self.module.materialize.__code__.co_filename,str(SOURCE))

    def test_wrong_source_digest_is_rejected(self):
        with self.assertRaises(adapter.BindingError): adapter.load_synthetic_bound(SOURCE,self.root,self.cases,'0'*64)

    def test_fixture_escape_is_rejected_before_port_call(self):
        bad={'bad':{'family':'two','inputs':dict(self.manifests['one'])}}
        bad['bad']['inputs']['game']={'path':'/etc/hosts','sha256':'0'*64}
        with self.assertRaises(adapter.BindingError): adapter.load_synthetic_bound(SOURCE,self.root,bad)

    def test_real_port_detects_modified_fake_materialization(self):
        out=self.root/'single';out.mkdir()
        journal=lambda *_:None
        paths=self.setup_port(out,self.manifests['one'],journal,family='two')
        Path(paths[0]).write_text('tampered')
        with self.assertRaises(ValueError): self.verify_port(*paths,self.manifests['one'],journal,'post')

if __name__=='__main__':unittest.main(verbosity=2)
