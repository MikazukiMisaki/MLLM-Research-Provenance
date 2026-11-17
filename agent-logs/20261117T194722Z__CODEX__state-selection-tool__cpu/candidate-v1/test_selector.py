"""Only invented files, episodes, outcome claims and token IDs; no real runtime."""
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest

HERE=Path(__file__).resolve().parent
def encode(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def build_fixture(root):
    root.mkdir();files={};train=[];evaluation=[]
    def store(name,value):
        raw=encode(value);(root/name).write_bytes(raw);files[name]=sha(raw);return name
    for parent in range(16):
        pid='SYNTHETIC_TRAIN_%02d'%parent;lineage=['synthetic-train-lineage-%02d'%parent]
        decisions=[]
        for i,command in enumerate(['go to example','look','examine example','look','examine example','go to example']):
            prefix='p%02d-d%d-'%(parent,i)
            action={'mapping':{'A000':'look','A001':command} if command!='look' else {'A000':'look'},
                    'selected_id':'A000' if command=='look' else 'A001','command':command}
            decisions.append({'index':i,
                'prompt_ref':store(prefix+'prompt.json',{'text':'fictional prompt '+str(i),'input_ids':[7,8]}),
                'action_ref':store(prefix+'action.json',action),
                'label_ref':store(prefix+'label.json',{'token_ids':[11,12]}),
                'mask_ref':store(prefix+'mask.json',{'sequence_ids':[7,8,11,12],'loss_mask':[0,0,1,1]})})
        terminal=store('p%02d-terminal.json'%parent,{'complete':True,'won':True})
        episode=store('p%02d-episode.json'%parent,{'parent':pid,'lineage':lineage,'episode_id':'FAKE-%02d'%parent,
                'product_sha256':'a'*64,'terminal_ref':terminal,'decisions':decisions})
        train.append({'parent':pid,'lineage':lineage,'episode_ref':episode})
        evaluation.append({'parent':'SYNTHETIC_EVAL_%02d'%parent,'lineage':['synthetic-eval-lineage-%02d'%parent]})
    return {'schema':'SI_STATE_SELECTION_DEMO_V1','files':files,'train':train,'evaluation':evaluation,'claimed_product_sha256':'a'*64}

class SelectorTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)/'input'
        self.manifest=build_fixture(self.root);self.out=Path(self.tmp.name)/'out'
    def run_program(self,*,expected=None):
        raw=encode(self.manifest);path=self.root/'manifest.json';path.write_bytes(raw)
        run=subprocess.run([sys.executable,'-I','-B',str(HERE/'select_pairs.py'),'--input-root',str(self.root),
            '--manifest',str(path),'--manifest-sha256',expected or sha(raw),'--output',str(self.out)],capture_output=True,text=True)
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
        run,status=self.run_program();self.assertEqual(run.returncode,1);self.assertIn('no matching pair',status['reason'])
        self.assertFalse((self.out/'target.jsonl').exists())
    def test_declared_lineage_overlap_rejected(self):
        self.manifest['evaluation'][0]['lineage']=self.manifest['train'][0]['lineage'][:]
        run,status=self.run_program();self.assertEqual(run.returncode,1);self.assertIn('lineage overlap',status['reason'])
    def test_referenced_raw_bytes_drift_rejected(self):
        (self.root/'p00-d0-prompt.json').write_text('{}')
        run,status=self.run_program();self.assertEqual(run.returncode,1);self.assertIn('hash mismatch',status['reason'])
    def test_no_failed_episode_backfill(self):
        name='p00-terminal.json';raw=encode({'complete':True,'won':False});(self.root/name).write_bytes(raw);self.manifest['files'][name]=sha(raw)
        run,status=self.run_program();self.assertEqual(run.returncode,1);self.assertIn('completed success',status['reason'])
    def test_wrong_manifest_hash_rejected(self):
        run,status=self.run_program(expected='0'*64);self.assertEqual(run.returncode,1);self.assertIn('hash mismatch',status['reason'])

if __name__=='__main__':unittest.main(verbosity=2)
