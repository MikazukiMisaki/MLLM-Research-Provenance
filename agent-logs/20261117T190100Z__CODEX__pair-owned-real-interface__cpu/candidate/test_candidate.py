"""No-op integration with original file/IPC interfaces and isolated candidate stage."""
import hashlib
import json
from pathlib import Path
import select
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import global_owner
import production_adapter
from fixed_product_dev.arm_budget import StageBudgetChannel
from fixed_product_dev.arm_stage import bound_paths

HERE=Path(__file__).parent
PORT=Path('/home/lizening/research-notes/agent-logs/20261116__CODEX__two-object-paired-eval__candidate/gate-live/eprime_ports.py')
CASE='eval-two-pair-a'
class ParentJournal:
    def __init__(self):self.rows=[]
    def emit(self,k,v):self.rows.append((k,v))

def fixture(root):
    source=root/'fake-inputs';source.mkdir()
    content={'game':b'fictional game',
      'routing':json.dumps({'task_type':'pick_two_obj_and_place'}).encode(),
      'config':json.dumps({'dataset':{'data_path':'REPLACE_ONLY_WITH_THIS_PARENT_PRIVATE_ROOT','num_train_games':1},
       'env':{'domain_randomization':False,'expert_type':'handcoded','goal_desc_human_anns_prob':0.0,'task_types':[6]},
       'general':{'training_method':'dqn'},'rl':{'training':{'max_nb_steps_per_episode':50}}}).encode()}
    inputs={}
    for k,v in content.items():
        p=source/(k+'.json');p.write_bytes(v);inputs[k]={'path':str(p),'sha256':hashlib.sha256(v).hexdigest()}
    setup,verify,_=production_adapter.load_synthetic_bound(PORT,root,{'synthetic':{'family':'two','inputs':inputs}})
    return inputs,setup,verify

class CandidateTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name).resolve();self.inputs,self.setup,self.verify=fixture(self.root)
        self.owner=global_owner.GlobalOwner(self.root/'global')
        self.binding=self.owner.materialize_pair(CASE,self.inputs,self.setup,self.verify)
    def run_arm(self,mode='normal',first_state=None):
        armroot=self.root/('worker-'+mode);armroot.mkdir()
        work=armroot/'output';work.mkdir()
        case={'case':CASE,'order':['P0','CANDIDATE'],'seed':42,'public_goal':'fictional',
              'input_sha256':{k:v['sha256'] for k,v in self.inputs.items()}}
        cfg={'output':str(work),'case':case,'arm':'P0','inputs':self.inputs,'binding':self.binding,
             'port_source':str(PORT),'fixture_root':str(self.root)}
        config=armroot/'config.json';config.write_text(json.dumps(cfg))
        self.owner.initial=first_state
        self.owner.begin_arm(CASE,'P0',work/'worker_events.jsonl',self.inputs,self.verify)
        parent,child=socket.socketpair();parent.setblocking(False)
        proc=subprocess.Popen([sys.executable,'-I','-B',str(HERE/'fake_worker.py'),str(config),str(child.fileno()),mode],
                 pass_fds=(child.fileno(),),stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
        child.close();stage=StageBudgetChannel('EVAL',parent,ParentJournal(),global_owner=self.owner,case=CASE,arm='P0')
        error=None;deadline=time.monotonic()+10
        try:
            while time.monotonic()<deadline:
                readable,writable,_=select.select([parent],[parent] if stage.pending_ack else [],[],0.1)
                if writable:stage.write_ack()
                if readable:
                    data=parent.recv(8192)
                    if not data:
                        stage.eof();break
                    stage.receive(data)
            else:raise RuntimeError('synthetic test deadline')
        except BaseException as exc:
            error=exc
        finally:
            parent.close()
            try:_,stderr=proc.communicate(timeout=8)
            except subprocess.TimeoutExpired:
                proc.terminate();_,stderr=proc.communicate(timeout=3)
        return proc.returncode,stage,error,stderr,work
    def test_shared_paths_real_stage_protocol_and_token_full_debit(self):
        self.assertEqual(self.owner.counts['materialize'],1)
        paths=bound_paths(self.binding)
        self.assertEqual(str(paths[0]),self.binding['game'])
        rc,stage,error,stderr,work=self.run_arm()
        self.assertIsNone(error,stderr.decode());self.assertEqual(rc,0,stderr.decode())
        self.assertEqual(stage.finished,'COMPLETED')
        self.assertEqual(self.owner.tokens,{'input':4096,'output':16})
        self.assertEqual(self.owner.counts['generation'],1)
        self.assertTrue((work/'worker_events.jsonl').exists())
        with self.assertRaises(global_owner.Stop):self.owner.close_arm_after_cleanup()
        self.assertTrue(self.owner.failed)
        with self.assertRaises(global_owner.Stop):self.owner.complete()
    def test_missing_and_duplicate_prepared_fail_before_reservation(self):
        for mode in ('missing_prepared','duplicate_prepared'):
            with self.subTest(mode=mode),tempfile.TemporaryDirectory() as t:
                root=Path(t).resolve();inputs,setup,verify=fixture(root);owner=global_owner.GlobalOwner(root/'global')
                binding=owner.materialize_pair(CASE,inputs,setup,verify)
                self.root,self.inputs,self.setup,self.verify,self.owner,self.binding=root,inputs,setup,verify,owner,binding
                rc,stage,error,stderr,work=self.run_arm(mode)
                self.assertIsNotNone(error);self.assertTrue(owner.failed)
                self.assertEqual(owner.counts['generation'],0);self.assertEqual(owner.tokens,{'input':0,'output':0})
    def test_generation_ack_then_interrupt_not_refunded(self):
        rc,stage,error,stderr,work=self.run_arm('interrupt')
        self.assertIsNotNone(error);self.assertTrue(self.owner.failed)
        self.assertEqual(self.owner.counts['generation'],1)
        self.assertEqual(self.owner.tokens,{'input':4096,'output':16})
        self.assertEqual(self.owner.active['operation'],'generation')
    def test_reset_claim_mismatch_denies_model_admission(self):
        rc,stage,error,stderr,work=self.run_arm(first_state={'observation':'different'})
        self.assertIsNotNone(error);self.assertTrue(self.owner.failed)
        self.assertEqual(self.owner.counts['reset'],1);self.assertEqual(self.owner.counts['model_load'],0)
    def test_pair_input_hash_drift_rejected(self):
        Path(self.binding['game']).write_bytes(b'tampered fake')
        with self.assertRaises(ValueError):bound_paths(self.binding)
    def test_actual_worker_main_stays_hard_blocked(self):
        p=subprocess.run([sys.executable,'-I','-B',str(HERE/'fixed_product_dev'/'worker.py')],capture_output=True,text=True)
        self.assertNotEqual(p.returncode,0);self.assertIn('RESEARCH_HOLD',p.stderr)

if __name__=='__main__':unittest.main(verbosity=2)
