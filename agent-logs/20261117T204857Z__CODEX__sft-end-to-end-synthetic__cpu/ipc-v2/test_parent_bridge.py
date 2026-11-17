import hashlib,json,os,stat,tempfile,unittest
from unittest.mock import patch
from pathlib import Path
import parent_bridge as p
class BridgeTest(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
 def rows(self,root):return [json.loads(x) for x in (root/'parent.jsonl').read_text().splitlines()]
 def test_real_ipc_fictional_positive(self):
  root=self.root/'run';result=p.run_fake(root,'normal');self.assertEqual(result['outcome'],'FICTIONAL_COMPLETE');self.assertEqual(result['returncode'],0);self.assertEqual(result['counts'],p.CAPS)
  rows=self.rows(root);res=[x for x in rows if x['kind']=='reserve'];ret=[x for x in rows if x['kind']=='returned']
  self.assertEqual(len(res),163);self.assertEqual(len(ret),163);self.assertEqual([x['payload']['operation'] for x in res],p.ORDER)
  self.assertEqual(res[-1]['payload']['operation'],'checkpoint_final');self.assertEqual(len([x for x in rows if x['kind']=='finished']),1)
  with self.assertRaises(FileExistsError):p.run_fake(root,'normal')
 def test_interrupted_after_first_step_retains_reservation(self):
  root=self.root/'run';result=p.run_fake(root,'interrupt_after_first_step');rows=self.rows(root)
  self.assertEqual(result['outcome'],'UNKNOWN');self.assertEqual(result['returncode'],23);self.assertEqual(result['active'],(11,'optimizer_step'))
  self.assertEqual(result['counts']['optimizer_step'],1);self.assertEqual(result['counts']['checkpoint_final'],0)
  self.assertTrue(any(x['kind']=='stopped_unknown' and x['payload']['no_refund'] for x in rows));self.assertFalse(any(x['kind']=='finished' for x in rows))
  with self.assertRaises(RuntimeError):p.dispatch_real()
 def test_child_seq_and_owner_seq_reject_bool_and_float(self):
  def make_rows(seq_override=None,owner_override=None):
   previous='0'*64;raw=[]
   for index,kind in enumerate(('validate_model_started','validate_model_returned')):
    owner=0 if owner_override is None else owner_override
    payload={'request':{},'owner_seq':owner,'effect_if_unreturned':'UNKNOWN'} if index==0 else {'owner_seq':owner,'evidence':{'returned':True}}
    row={'schema':'SI_STAGE_WORKER_V1','seq':index if seq_override is None or index!=0 else seq_override,
         'previous':previous,'monotonic_ns':1,'kind':kind,'payload':payload}
    row['digest']=hashlib.sha256(p.canonical(row)).hexdigest();previous=row['digest'];raw.append(p.canonical(row)+b'\n')
   path=self.root/'synthetic-child.jsonl';path.write_bytes(b''.join(raw));return path,hashlib.sha256(raw[-1]).hexdigest()
  path,h=make_rows();p.receipt_check(path,'validate_model',0,h,'returned')
  for bad in (False,0.0):
   with self.subTest(field='seq',value=bad):
    path,h=make_rows(seq_override=bad)
    with self.assertRaises(p.Stop):p.receipt_check(path,'validate_model',0,h,'returned')
   with self.subTest(field='owner_seq',value=bad):
    path,h=make_rows(owner_override=bad)
    with self.assertRaises(p.Stop):p.receipt_check(path,'validate_model',0,h,'returned')
  path,h=make_rows()
  with self.assertRaises(p.Stop):p.receipt_check(path,'validate_model',False,h,'returned')
  with self.assertRaises(p.Stop):p.receipt_check(path,'validate_model',0.0,h,'returned')
 def test_parent_directory_sync_failure_stops_before_child(self):
  root=self.root/'no-sync';real_fsync=os.fsync
  def injected(fd):
   if stat.S_ISDIR(os.fstat(fd).st_mode):raise OSError('FICTIONAL directory fsync failure')
   return real_fsync(fd)
  with patch.object(p.os,'fsync',side_effect=injected):
   with self.assertRaises(p.LedgerCreationUnknown):p.run_fake(root,'normal')
  entries=[json.loads(x) for x in (root/'parent.jsonl').read_text().splitlines()]
  self.assertEqual(entries[0]['kind'],'creation_unknown');self.assertTrue(entries[0]['payload']['no_execution'])
  self.assertFalse((root/'worker_events.jsonl').exists());self.assertFalse((root/'child.stderr').exists())
if __name__=='__main__':unittest.main(verbosity=2)
