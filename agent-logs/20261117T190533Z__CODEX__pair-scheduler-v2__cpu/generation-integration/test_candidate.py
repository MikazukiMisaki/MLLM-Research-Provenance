"""No-op integration with original file/IPC interfaces and isolated candidate stage."""
import hashlib
import json
import copy
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
        rows=[json.loads(line) for line in (self.owner.root/'global.jsonl').read_text().splitlines()]
        ticket=next(row['payload'] for row in rows if row['event']=='reserve' and row['payload']['operation']=='generation')
        self.assertTrue(all(len(ticket[k])==64 for k in ('prepared_digest','public_sha256','public_prompt_sha256',
                         'rendered_prompt_sha256','input_ids_sha256','attention_mask_sha256',
                         'kwargs_sha256','generation_config_sha256','eos_ids_sha256')))
        self.assertEqual(ticket['input_ids_sha256'],hashlib.sha256(global_owner.canonical([4,5])).hexdigest())
        self.assertEqual(ticket['rendered_prompt_sha256'],hashlib.sha256(b'synthetic rendered prompt').hexdigest())
        with self.assertRaises(global_owner.Stop):self.owner.close_arm_after_cleanup()
        self.assertTrue(self.owner.failed)
        with self.assertRaises(global_owner.Stop):self.owner.complete()
    def test_missing_and_duplicate_prepared_fail_before_reservation(self):
        for mode in ('missing_prepared','duplicate_prepared','bad_public','bad_kwargs'):
            with self.subTest(mode=mode),tempfile.TemporaryDirectory() as t:
                root=Path(t).resolve();inputs,setup,verify=fixture(root);owner=global_owner.GlobalOwner(root/'global')
                binding=owner.materialize_pair(CASE,inputs,setup,verify)
                self.root,self.inputs,self.setup,self.verify,self.owner,self.binding=root,inputs,setup,verify,owner,binding
                rc,stage,error,stderr,work=self.run_arm(mode)
                self.assertIsNotNone(error);self.assertTrue(owner.failed)
                self.assertEqual(owner.counts['generation'],0);self.assertEqual(owner.tokens,{'input':0,'output':0})
    def test_actual_generation_prepared_shape_and_mutations(self):
        rc,stage,error,stderr,work=self.run_arm()
        self.assertIsNone(error,stderr.decode());self.assertEqual(rc,0,stderr.decode())
        source=[json.loads(x) for x in (work/'worker_events.jsonl').read_text().splitlines()]
        real=next(r['payload'] for r in source if r['kind']=='prepared')
        def check(payload):
            row={'seq':0,'previous':'0'*64,'kind':'prepared','payload':payload}
            row['digest']=global_owner.sha(global_owner.canonical(row))
            log=self.root/'test-prepared.jsonl';log.write_bytes(global_owner.canonical(row)+b'\n')
            return global_owner.claimed_prepared(log)
        expected=check(real)
        shuffled=copy.deepcopy(real);shuffled['kwargs']=dict(reversed(list(shuffled['kwargs'].items())))
        self.assertEqual(check(shuffled)['kwargs_sha256'],expected['kwargs_sha256'])
        variants=[]
        for key,val in [('num_return_sequences',2),('num_return_sequences',True),('num_beams',2),
                        ('return_dict_in_generate',1),('output_scores',False),('max_new_tokens',17),('do_sample',0)]:
            obj=copy.deepcopy(real);obj['kwargs'][key]=val;variants.append(obj)
        for key in ('public','rendered_prompt','input_ids','attention_mask','kwargs','generation_config','eos_ids'):
            obj=copy.deepcopy(real);del obj[key];variants.append(obj)
        for key,val in [('public',{}),('rendered_prompt',''),('attention_mask',[1,0]),('eos_ids',[151645,True])]:
            obj=copy.deepcopy(real);obj[key]=val;variants.append(obj)
        obj=copy.deepcopy(real);obj['public']['action_map']['A000']='wrong';variants.append(obj)
        obj=copy.deepcopy(real);obj['public']['public_prompt']='tampered';variants.append(obj)
        obj=copy.deepcopy(real);obj['kwargs']['extra']=1;variants.append(obj)
        obj=copy.deepcopy(real);obj['generation_config']['eos_token_id']=[151645,True];variants.append(obj)
        for i,obj in enumerate(variants):
            with self.subTest(i=i),self.assertRaises(global_owner.Stop):check(obj)
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
