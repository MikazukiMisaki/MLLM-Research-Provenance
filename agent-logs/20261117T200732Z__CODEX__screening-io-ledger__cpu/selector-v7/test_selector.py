"""Only invented files, episodes, outcome claims and token IDs; no real runtime."""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest

HERE=Path(__file__).resolve().parent
def encode(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def build_fixture(root,count=16):
    root.mkdir();files={};train=[];evaluation=[]
    def store(name,value):
        raw=encode(value);(root/name).write_bytes(raw);files[name]=sha(raw);return name
    for parent in range(count):
        pid='SYNTHETIC_TRAIN_%02d'%parent;lineage=['synthetic-train-lineage-%02d'%parent]
        decisions=[]
        for i,command in enumerate(['go to example','look','examine example','look','examine example','go to example']):
            prefix='p%02d-d%d-'%(parent,i)
            action={'mapping':{'A000':'look','A001':command} if command!='look' else {'A000':'look'},
                    'selected_id':'A000' if command=='look' else 'A001','command':command}
            decisions.append({'index':i,'source_decision_id':'FAKE-%02d-DECISION-%d'%(parent,i),
                'prompt_ref':store(prefix+'prompt.json',{'text':'fictional prompt '+str(i),'input_ids':[7,8]}),
                'action_ref':store(prefix+'action.json',action),
                'label_ref':store(prefix+'label.json',{'token_ids':[11,12]}),
                'mask_ref':store(prefix+'mask.json',{'sequence_ids':[7,8,11,12],'loss_mask':[0,0,1,1]})})
        terminal=store('p%02d-terminal.json'%parent,{'complete':True,'won':True})
        episode=store('p%02d-episode.json'%parent,{'parent':pid,'lineage':lineage,'episode_id':'FAKE-%02d'%parent,
                'product_sha256':'a'*64,'terminal_ref':terminal,'decisions':decisions})
        train.append({'parent':pid,'lineage':lineage,'episode_ref':episode})
        if parent<16:evaluation.append({'parent':'SYNTHETIC_EVAL_%02d'%parent,'lineage':['synthetic-eval-lineage-%02d'%parent]})
    return {'schema':'SI_STATE_SELECTION_DEMO_V7','files':files,'train':train,'evaluation':evaluation,'claimed_product_sha256':'a'*64}

class SelectorTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)/'input'
        self.manifest=build_fixture(self.root);self.out=Path(self.tmp.name)/'out'
    def run_program(self,*,expected=None,max_files=10000,max_bytes=20000000,max_ledger=128):
        raw=encode(self.manifest);path=self.root/'manifest.json';path.write_bytes(raw)
        run=subprocess.run([sys.executable,'-I','-B',str(HERE/'select_pairs.py'),'--input-root',str(self.root),
            '--manifest',str(path),'--manifest-sha256',expected or sha(raw),'--output',str(self.out),
            '--max-files',str(max_files),'--max-bytes',str(max_bytes),'--max-ledger-records',str(max_ledger)],capture_output=True,text=True)
        return run,json.loads((self.out/'status.json').read_text())
    def test_fictional_16_success(self):
        run,status=self.run_program();self.assertEqual(run.returncode,0,run.stderr)
        self.assertEqual(status['selected_parents'],16);self.assertEqual(status['source_identity'],'UNKNOWN')
        target=[json.loads(x) for x in (self.out/'target.jsonl').read_text().splitlines()]
        control=[json.loads(x) for x in (self.out/'control.jsonl').read_text().splitlines()]
        self.assertEqual(len(target),16);self.assertEqual(len(control),16)
        self.assertEqual([r['selection']['index'] for r in target],[5]*16)
        self.assertEqual([r['selection']['index'] for r in control],[0]*16)
    def test_mismatched_label_not_repaired_or_replaced(self):
        name='p00-d5-label.json';raw=encode({'token_ids':[99,12]});(self.root/name).write_bytes(raw);self.manifest['files'][name]=sha(raw)
        mask='p00-d5-mask.json';raw=encode({'sequence_ids':[7,8,99,12],'loss_mask':[0,0,1,1]});(self.root/mask).write_bytes(raw);self.manifest['files'][mask]=sha(raw)
        run,status=self.run_program();self.assertEqual(run.returncode,1);self.assertEqual(status['status'],'INSUFFICIENT')
        self.assertEqual(json.loads((self.out/'ledger.jsonl').read_text().splitlines()[0])['reason'],'no matching pair')
        self.assertFalse((self.out/'target.jsonl').exists())
    def test_declared_lineage_overlap_rejected(self):
        self.manifest['evaluation'][0]['lineage']=self.manifest['train'][0]['lineage'][:]
        run,status=self.run_program();self.assertEqual(run.returncode,1);self.assertIn('lineage overlap',status['reason'])
    def test_referenced_raw_bytes_drift_rejected(self):
        (self.root/'p00-d0-prompt.json').write_text('{}')
        run,status=self.run_program();self.assertEqual(run.returncode,1);self.assertIn('hash mismatch',status['reason'])
    def test_no_failed_episode_backfill(self):
        name='p00-terminal.json';raw=encode({'complete':True,'won':False});(self.root/name).write_bytes(raw);self.manifest['files'][name]=sha(raw)
        run,status=self.run_program();self.assertEqual(run.returncode,1);self.assertEqual(status['status'],'INSUFFICIENT')
        self.assertEqual(json.loads((self.out/'ledger.jsonl').read_text().splitlines()[0])['disposition'],'REJECT')
    def test_wrong_manifest_hash_rejected(self):
        run,status=self.run_program(expected='0'*64);self.assertEqual(run.returncode,1);self.assertIn('hash mismatch',status['reason'])
    def edit_episode(self,index,fn):
        ref=self.manifest['train'][index]['episode_ref'];episode=json.loads((self.root/ref).read_bytes())
        fn(episode);raw=encode(episode);(self.root/ref).write_bytes(raw);self.manifest['files'][ref]=sha(raw)
    def test_alias_episode_id_across_parents_rejected(self):
        self.edit_episode(1,lambda e:e.update(episode_id='FAKE-00'))
        run,status=self.run_program();self.assertEqual(run.returncode,1);self.assertIn('episode source identity',status['reason'])
    def test_alias_terminal_ref_across_parents_rejected(self):
        self.edit_episode(1,lambda e:e.update(terminal_ref='p00-terminal.json'))
        run,status=self.run_program();self.assertEqual(run.returncode,1);self.assertIn('terminal receipt reused',status['reason'])
    def test_hardlink_terminal_alias_across_parents_rejected(self):
        name='linked-terminal.json';os.link(self.root/'p00-terminal.json',self.root/name)
        self.manifest['files'][name]=self.manifest['files']['p00-terminal.json']
        self.edit_episode(1,lambda e:e.update(terminal_ref=name))
        run,status=self.run_program();self.assertEqual(run.returncode,1);self.assertIn('terminal receipt reused',status['reason'])
    def test_alias_full_decision_refs_across_parents_rejected(self):
        def change(e):
            d=e['decisions'][0]
            for key in ('prompt','action','label','mask'):d[key+'_ref']='p00-d0-'+key+'.json'
        self.edit_episode(1,change)
        run,status=self.run_program();self.assertEqual(run.returncode,1);self.assertIn('decision refs reused',status['reason'])
    def test_alias_decision_identity_across_parents_rejected(self):
        self.edit_episode(1,lambda e:e['decisions'][0].update(source_decision_id='FAKE-00-DECISION-0'))
        run,status=self.run_program();self.assertEqual(run.returncode,1);self.assertIn('decision source identity',status['reason'])
    def test_shared_label_artifact_alone_is_permitted(self):
        self.edit_episode(1,lambda e:e['decisions'][0].update(label_ref='p00-d0-label.json'))
        run,status=self.run_program();self.assertEqual(run.returncode,0,run.stderr);self.assertEqual(status['selected_parents'],16)
    def fixture_20(self):
        self.tmp.cleanup();self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'input';self.manifest=build_fixture(self.root,count=20);self.out=Path(self.tmp.name)/'out'
    def test_first_16_then_unscanned(self):
        self.fixture_20();run,status=self.run_program();self.assertEqual(run.returncode,0,run.stderr)
        rows=[json.loads(x) for x in (self.out/'ledger.jsonl').read_text().splitlines()]
        self.assertEqual([r['disposition'] for r in rows],['ACCEPT']*16+['NOT_SCANNED_AFTER_SELECTION']*4)
        self.assertEqual(status['counters']['ledger_records'],20+16*6)
    def test_known_reject_then_select_next_frozen_parent(self):
        self.fixture_20();name='p00-terminal.json';raw=encode({'complete':True,'won':False})
        (self.root/name).write_bytes(raw);self.manifest['files'][name]=sha(raw)
        run,status=self.run_program();self.assertEqual(run.returncode,0,run.stderr)
        rows=[json.loads(x) for x in (self.out/'ledger.jsonl').read_text().splitlines()]
        self.assertEqual([r['disposition'] for r in rows],['REJECT']+['ACCEPT']*16+['NOT_SCANNED_AFTER_SELECTION']*3)
    def test_unknown_stops_and_records_unscanned(self):
        self.fixture_20();(self.root/'p01-d0-prompt.json').write_text('{}')
        run,status=self.run_program();self.assertEqual(run.returncode,1);self.assertEqual(status['status'],'UNKNOWN')
        rows=[json.loads(x) for x in (self.out/'ledger.jsonl').read_text().splitlines()]
        self.assertEqual([r['disposition'] for r in rows],['ACCEPT','UNKNOWN']+['NOT_SCANNED_AFTER_STOP']*18)
        self.assertEqual(rows[1]['decisions'][0]['disposition'],'UNKNOWN')
        self.assertFalse((self.out/'target.jsonl').exists())
    def test_resource_file_ceiling_stops(self):
        self.fixture_20();run,status=self.run_program(max_files=3)
        self.assertEqual(run.returncode,1);self.assertEqual(status['status'],'UNKNOWN')
        self.assertEqual(status['counters']['files_read'],3);self.assertIn('file read ceiling',status['reason'])

if __name__=='__main__':unittest.main(verbosity=2)
