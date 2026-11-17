"""Finite fictional inputs and partial-read fault injection only."""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock
import select_pairs as selector
import test_selector as fixture
from read_journal import ReadJournal,recover

class ReadAccountingTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'inputs';self.manifest=fixture.build_fixture(self.root)
        self.raw=fixture.encode(self.manifest);(self.root/'manifest.json').write_bytes(self.raw)
        self.out=Path(self.tmp.name)/'out'
        selector.COUNTS.update(files_reserved=0,bytes_reserved=0,returned_bytes_lower_bound=0,ledger_records=0,read_unknown=False)
        selector.READ_LOG=None
    def args(self,bytes_cap=20000000):
        return ['select_pairs.py','--input-root',str(self.root),'--manifest',str(self.root/'manifest.json'),
            '--manifest-sha256',fixture.sha(self.raw),'--output',str(self.out),'--max-files','10000',
            '--max-bytes',str(bytes_cap),'--max-ledger-records','128']
    def test_partial_then_oserror_retains_full_reservation(self):
        real=os.read;calls=[]
        def injected(fd,n):
            path=os.readlink('/proc/self/fd/'+str(fd))
            if path.endswith('/p00-episode.json'):
                calls.append(n)
                if len(calls)==1:return real(fd,min(5,n))
                raise OSError('fictional partial read failure')
            return real(fd,n)
        with mock.patch.object(sys,'argv',self.args()),mock.patch.object(selector.os,'read',side_effect=injected):
            rc=selector.main()
        status=json.loads((self.out/'status.json').read_text());rows=[json.loads(x) for x in (self.out/'ledger.jsonl').read_text().splitlines()]
        episode_size=(self.root/'p00-episode.json').stat().st_size
        self.assertEqual(rc,1);self.assertEqual(status['status'],'UNKNOWN');self.assertEqual(rows[0]['disposition'],'UNKNOWN')
        self.assertEqual(status['counters']['bytes_reserved'],len(self.raw)+episode_size)
        self.assertEqual(status['counters']['returned_bytes_lower_bound'],len(self.raw)+5)
        recovered=recover(self.out/'read_journal.jsonl')
        self.assertEqual(recovered['read_accounting'],'UNKNOWN');self.assertEqual(recovered['reserved_bytes'],len(self.raw)+episode_size)
        self.assertEqual(recovered['returned_bytes_lower_bound'],len(self.raw)+5);self.assertEqual(recovered['unknown_reads'],[1])
    def test_byte_ceiling_prevents_next_read(self):
        with mock.patch.object(sys,'argv',self.args(bytes_cap=len(self.raw))):rc=selector.main()
        status=json.loads((self.out/'status.json').read_text());recovered=recover(self.out/'read_journal.jsonl')
        self.assertEqual(rc,1);self.assertEqual(status['status'],'UNKNOWN');self.assertIn('byte read ceiling',status['reason'])
        self.assertEqual(recovered['reserved_files'],1);self.assertEqual(recovered['reserved_bytes'],len(self.raw))
        self.assertEqual(recovered['read_accounting'],'UNKNOWN')
    def test_incomplete_and_torn_reservation_recovery_unknown(self):
        path=Path(self.tmp.name)/'crash.jsonl';journal=ReadJournal(path,{'files':1,'bytes':20,'ledger_records':1})
        journal.event('RESERVE',{'id':0,'bytes':10,'path':'fictional'})
        state=recover(path);self.assertEqual(state['read_accounting'],'UNKNOWN');self.assertEqual(state['unclosed'],[0])
        with path.open('ab') as f:f.write(b'{"partial":')
        state=recover(path);self.assertEqual(state['read_accounting'],'UNKNOWN');self.assertEqual(state['journal_integrity'],'UNKNOWN')
    def test_hash_chained_short_return_is_unknown(self):
        path=Path(self.tmp.name)/'short.jsonl';journal=ReadJournal(path,{'files':1,'bytes':10,'ledger_records':1})
        journal.event('RESERVE',{'id':0,'bytes':10,'path':'fictional'})
        journal.event('RETURNED',{'id':0,'known_bytes':5})
        journal.event('READ_PHASE_COMPLETE',{'selection_status':'INSUFFICIENT'})
        self.assertEqual(recover(path)['read_accounting'],'UNKNOWN')
    def test_hash_chained_record_after_complete_is_unknown(self):
        path=Path(self.tmp.name)/'after.jsonl';journal=ReadJournal(path,{'files':1,'bytes':10,'ledger_records':1})
        journal.event('READ_PHASE_COMPLETE',{'selection_status':'INSUFFICIENT'})
        journal.event('RESERVE',{'id':0,'bytes':10,'path':'fictional'})
        journal.event('RETURNED',{'id':0,'known_bytes':10})
        self.assertEqual(recover(path)['read_accounting'],'UNKNOWN')
    def test_hash_chained_reservations_over_header_are_unknown(self):
        path=Path(self.tmp.name)/'over.jsonl';journal=ReadJournal(path,{'files':1,'bytes':5,'ledger_records':1})
        journal.event('RESERVE',{'id':0,'bytes':10,'path':'fictional'})
        journal.event('RETURNED',{'id':0,'known_bytes':10})
        journal.event('READ_PHASE_COMPLETE',{'selection_status':'INSUFFICIENT'})
        self.assertEqual(recover(path)['read_accounting'],'UNKNOWN')

if __name__=='__main__':unittest.main(verbosity=2)
