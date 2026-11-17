import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import global_owner
import production_adapter
import scheduler_synthetic

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

class SchedulerTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name).resolve();self.inputs,self.setup,self.verify=fixture(self.root);self.out=self.root/'run'
    def rows(self):return [json.loads(line) for line in (self.out/'owner'/'global.jsonl').read_text().splitlines()]
    def test_four_pairs_two_arms_and_per_pair_initials(self):
        owner=scheduler_synthetic.run_fixture(self.out,self.root,self.inputs,self.setup,self.verify)
        expected={(case,arm) for case,order in global_owner.SCHEDULE for arm in order}
        self.assertEqual(owner.closed,expected);self.assertTrue(owner.completed)
        self.assertEqual(owner.counts,{'materialize':4,'env_construct':8,'env_init':8,'reset':8,'model_load':8,'generation':8,'step':0})
        self.assertEqual(owner.tokens,{'input':8*4096,'output':8*16})
        rows=self.rows();self.assertEqual(rows[-1]['event'],'synthetic_batch_complete')
        closed=[r['payload'] for r in rows if r['event']=='arm_closed']
        self.assertEqual([(r['case'],r['arm']) for r in closed],[(c,a) for c,order in global_owner.SCHEDULE for a in order])
        self.assertEqual(len(closed),8);self.assertEqual(len({r['cleanup']['pid'] for r in closed}),8)
        for case,order in global_owner.SCHEDULE:
            per=[r for r in closed if r['case']==case]
            self.assertEqual(per[0]['child_result_claim']['initial_public'],per[1]['child_result_claim']['initial_public'])
            self.assertEqual(per[0]['child_result_claim']['initial_public']['task_id'],case)
            self.assertTrue(all(r['cleanup']['visible_group_members']==[] for r in per))
        self.assertNotEqual(closed[0]['child_result_claim']['initial_public'],closed[2]['child_result_claim']['initial_public'])
        with self.assertRaises(FileExistsError):scheduler_synthetic.run_fixture(self.out,self.root,self.inputs,self.setup,self.verify)
    def test_owned_cleanup_timeout_stops_and_keeps_reservation(self):
        with self.assertRaises(Exception):
            scheduler_synthetic.run_fixture(self.out,self.root,self.inputs,self.setup,self.verify,linger_case=global_owner.SCHEDULE[1][0])
        rows=self.rows();self.assertIn('aborted',[r['event'] for r in rows])
        cleanup=[r['payload'] for r in rows if r['event']=='synthetic_cleanup_after_abort']
        self.assertEqual(len(cleanup),1);self.assertIsNotNone(cleanup[0]['observed_returncode'])
        reserves=[r['payload'] for r in rows if r['event']=='reserve']
        self.assertEqual(sum(r['operation']=='materialize' for r in reserves),2)
        self.assertEqual(sum(r['operation']=='generation' for r in reserves),3)
        self.assertEqual(sum(r.get('input_tokens_reserved',0) for r in reserves),3*4096)
        self.assertEqual(sum(r.get('output_tokens_reserved',0) for r in reserves),3*16)
        self.assertEqual(len([r for r in rows if r['event']=='arm_closed']),2)
        self.assertFalse(any(r['event']=='synthetic_batch_complete' for r in rows))
        with self.assertRaises(FileExistsError):scheduler_synthetic.run_fixture(self.out,self.root,self.inputs,self.setup,self.verify)

    def test_claimed_prepared_rejects_multiple_outputs_and_missing_public(self):
        prompt='fictional prompt';base={'public':{'goal':'fictional','observation':'fictional',
          'recent_history':[],'valid_actions':['fictional action'],'public_prompt':prompt,
          'public_prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),
          'action_map':{'A000':'fictional action'}},'rendered_prompt':'fictional render',
          'input_ids':[4,5],'attention_mask':[1,1],
          'kwargs':{'max_new_tokens':16,'do_sample':False,'num_beams':1,'num_return_sequences':1,
                    'return_dict_in_generate':True,'output_scores':True},
          'generation_config':{'eos_token_id':[151645,151643],'pad_token_id':151643,'forced_eos_token_id':None},
          'eos_ids':[151645,151643]}
        path=self.root/'claimed.jsonl'
        def write_claim(payload):
            row={'seq':0,'previous':'0'*64,'kind':'prepared','payload':payload}
            row['digest']=global_owner.sha(global_owner.canonical(row))
            path.write_bytes(global_owner.canonical(row)+b'\n')
        write_claim(base);self.assertEqual(global_owner.claimed_prepared(path)['input_ids'],[4,5])
        bad=json.loads(json.dumps(base));bad['kwargs']['num_return_sequences']=2;write_claim(bad)
        with self.assertRaises(global_owner.Stop):global_owner.claimed_prepared(path)
        bad=json.loads(json.dumps(base));del bad['public'];write_claim(bad)
        with self.assertRaises(global_owner.Stop):global_owner.claimed_prepared(path)
        bad=json.loads(json.dumps(base));bad['public']['public_prompt_sha256']='0'*64;write_claim(bad)
        with self.assertRaises(global_owner.Stop):global_owner.claimed_prepared(path)

if __name__=='__main__':unittest.main(verbosity=2)
