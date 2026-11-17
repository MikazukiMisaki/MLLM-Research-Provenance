import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import candidate as c

SCRIPT=Path(__file__).parent/'fake_arm.py'

def setup(root,inputs,journal,family):
    assert family=='two'
    root=Path(root); eroot=root/'eprime_only'; dataset=eroot/'dataset'; task=dataset/'authored-eprime-only'
    task.mkdir(parents=True)
    game=task/'game.tw-pddl'; game.write_text('imaginary-game:'+inputs['case'])
    (task/'traj_data.json').write_text('{"type":"imaginary"}')
    config=eroot/'actual_config.json'; config.write_text(json.dumps({'data_path':str(dataset)}))
    journal('synthetic_setup', {'fake':True})
    return game,config,dataset

def verify(game,config,dataset,inputs,journal,phase):
    assert Path(game).read_text()=='imaginary-game:'+inputs['case']
    assert json.loads(Path(config).read_text())['data_path']==str(dataset)
    journal('synthetic_verify', {'phase':phase})

def spawn_for(mode='ok',seen=None):
    def spawn(pair,arm,paths,fd):
        if seen is not None: seen.append((pair,arm,tuple(map(str,paths))))
        return subprocess.Popen([sys.executable,'-I','-B',str(SCRIPT),str(fd),arm,mode],pass_fds=(fd,),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    return spawn

class CandidateTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'private'
        self.owner=c.Owner(self.root)
    def run_pair(self,case,order=('A','B'),mode='ok',seen=None,v=verify):
        return c.pair(self.owner,case,order,{'case':case},setup,v,spawn_for(mode,seen))

    def test_four_setups_eight_arm_processes_and_common_pair_paths(self):
        seen=[]
        for i,case in enumerate(c.PAIRS): self.run_pair(case,('A','B') if i%2==0 else ('B','A'),seen=seen)
        self.owner.complete()
        self.assertEqual(self.owner.count,{'materialize':4,'env_construct':8,'env_init':8,'reset':8,'model_load':8,'generation':8,'step':8})
        self.assertEqual(len(seen),8)
        for case in c.PAIRS:
            paths=[v[2] for v in seen if v[0]==case]
            self.assertEqual(len(paths),2); self.assertEqual(paths[0],paths[1])
        self.assertEqual(c.inspect_log(self.owner.log)['seq'],self.owner.seq)
        with self.assertRaises(c.Stop): c.Owner(self.root)

    def test_mismatched_second_reset_stops_before_second_model(self):
        with self.assertRaises(c.Stop): self.run_pair('one',mode='mismatch')
        self.assertEqual(self.owner.count['model_load'],1)
        self.assertEqual(self.owner.count['materialize'],1)
        self.assertIsNone(self.owner.open)

    def test_unreturned_generation_remains_charged(self):
        with self.assertRaises(c.Stop): self.run_pair('one',mode='open')
        self.assertEqual(self.owner.count['generation'],1)
        self.assertEqual(self.owner.open['kind'],'generation')
        with self.assertRaises(c.Stop): self.owner.reserve('two',None,'materialize')
        with self.assertRaises(c.Stop): c.Owner(self.root)

    def test_input_drift_stops_before_second_arm(self):
        phases=[]
        def alter(game,config,dataset,inputs,journal,phase):
            verify(game,config,dataset,inputs,journal,phase)
            phases.append(phase)
            if phase=='post': Path(game).write_text('mutated')
        with self.assertRaises(c.Stop): self.run_pair('one',v=alter)
        self.assertEqual(self.owner.count['model_load'],1)
        self.assertEqual(phases,['pre','post'])

    def test_own_arm_and_global_cap_and_no_refund(self):
        token=self.owner.reserve('one',None,'materialize'); self.owner.returned(token,{})
        self.owner.start_arm('one','A')
        t=self.owner.reserve('one','A','reset'); self.owner.returned(t,{})
        with self.assertRaises(c.Stop): self.owner.reserve('one','A','reset')
        with self.assertRaises(c.Stop): self.owner.reserve('one',None,'materialize')
        self.assertEqual(self.owner.count['reset'],1)

    def test_truncated_journal_stops_live_owner(self):
        self.owner.reserve('one',None,'materialize')
        data=self.owner.log.read_bytes(); self.owner.log.write_bytes(data[:-1])
        with self.assertRaises(c.Stop): self.owner.write('unexpected',{})

if __name__=='__main__': unittest.main(verbosity=2)
