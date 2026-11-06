"""Synthetic stub objects/modules only: never load or call the real parser."""
import hashlib
import importlib
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest import mock
import real_loader as r

class FakeLisp:
    def __init__(self,fail_at=None):self.calls=[];self.fail_at=fail_at
    def parse_nested_list(self,stream):
        text=stream.read();self.calls.append(text)
        if len(self.calls)==self.fail_at:raise ValueError('synthetic parse failure')
        return [text]
class FakeParser:
    def __init__(self,fail_at=None):self.calls=[];self.fail_at=fail_at
    def parse_task(self,domain,problem):
        self.calls.append((domain[:],problem[:]))
        assert domain==['fake-domain']
        domain.append('mutated')
        if len(self.calls)==self.fail_at:raise SystemExit('synthetic failure')

class Tests(unittest.TestCase):
    def setUp(self):self.inputs={'domain':b'fake-domain',**{k:('fake-'+k).encode() for k in r.ORDER}}
    def test_both_real_entries_fail_before_io(self):
        self.assertFalse(r.REAL_PARSER_ENABLED);self.assertEqual(len(r.DEPS),13);self.assertEqual(len(r.INPUTS),5)
        self.assertEqual(set(r._maps().values()),set(r.DEPS))
        with mock.patch.object(r.os,'open') as opened:
            with self.assertRaisesRegex(RuntimeError,'REAL_PARSER_HARD_DISABLED'):r.real_execution()
            with self.assertRaisesRegex(RuntimeError,'REAL_PARSER_HARD_DISABLED'):r._real_impl(lambda x:True)
            opened.assert_not_called()
    def test_fake_four_cases_fresh_ast_and_order(self):
        lisp=FakeLisp();parser=FakeParser();events=[]
        r._parse_cases(lisp,parser,self.inputs,lambda e:events.append(e) or True)
        self.assertEqual(len(lisp.calls),8);self.assertEqual(len(parser.calls),4)
        self.assertEqual([e['case'] for e in events if e['event']=='case_started'],list(r.ORDER))
        self.assertEqual([e['case'] for e in events if e['event']=='case_returned'],list(r.ORDER))
        self.assertEqual(lisp.calls[::2],['fake-domain']*4)
    def test_fake_case_keys_and_latin1(self):
        lisp=FakeLisp();parser=FakeParser();inputs=dict(self.inputs);inputs['clean-1']=b'fake-\xff'
        r._parse_cases(lisp,parser,inputs,lambda e:True)
        self.assertEqual(lisp.calls[1],'fake-\u00ff')
        for bad in ({k:v for k,v in inputs.items() if k!='heat-2'},{**inputs,'extra':b'x'}):
            with self.assertRaises(ValueError):r._parse_cases(FakeLisp(),FakeParser(),bad,lambda e:True)
    def test_fake_failure_and_systemexit_stop_following_cases(self):
        for lisp,parser,exc in ((FakeLisp(fail_at=3),FakeParser(),ValueError),(FakeLisp(),FakeParser(fail_at=2),SystemExit)):
            events=[]
            with self.assertRaises(exc):r._parse_cases(lisp,parser,self.inputs,lambda e:events.append(e) or True)
            self.assertEqual([e['case'] for e in events if e['event']=='case_started'],list(r.ORDER[:2]))
            self.assertEqual(events[-1],{'event':'case_unknown','case':'heat-1'})
    def test_missing_ack_stops_before_fake_parser(self):
        lisp=FakeLisp();parser=FakeParser()
        with self.assertRaises(RuntimeError):r._parse_cases(lisp,parser,self.inputs,lambda e:False)
        self.assertEqual(lisp.calls,[]);self.assertEqual(parser.calls,[])
    def test_lost_return_ack_stops_and_marks_case_unknown(self):
        lisp=FakeLisp();parser=FakeParser();events=[]
        def ack(event):
            events.append(event)
            return event['event']!='task_returned'
        with self.assertRaises(RuntimeError):r._parse_cases(lisp,parser,self.inputs,ack)
        self.assertEqual(len(parser.calls),1)
        self.assertEqual(events[-1],{'event':'case_unknown','case':'clean-1'})
        self.assertFalse(any(e.get('case')=='heat-1' for e in events))
    def test_verified_snapshot_and_symlink_or_drift_rejection(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'fake';p.write_bytes(b'one');digest=hashlib.sha256(b'one').hexdigest()
            snapshot=r._read_verified(p,digest);p.write_bytes(b'two')
            self.assertEqual(snapshot,b'one')
            with self.assertRaises(ValueError):r._read_verified(p,digest)
            with self.assertRaises(ValueError):r._read_verified(p,hashlib.sha256(b'two').hexdigest(),cap=2)
            symlink=Path(td)/'link';symlink.symlink_to(p)
            with self.assertRaises(OSError):r._read_verified(symlink,hashlib.sha256(b'two').hexdigest())
    def test_fake_private_namespace_serves_snapshots_and_denies_unlisted(self):
        prefix='_si_synthetic_test'
        module=prefix+'.translate.toy'
        source={'toy.py':b'VALUE = 7\n'};mapping={module:'toy.py'}
        finder,loaded=r._open_namespace(prefix,source,mapping)
        try:
            found=importlib.import_module(module)
            self.assertEqual(found.VALUE,7);self.assertEqual(loaded[module]['sha256'],hashlib.sha256(source['toy.py']).hexdigest())
            with self.assertRaises(ImportError):importlib.import_module(prefix+'.translate.unlisted')
        finally:r._close_namespace(prefix,finder)
        self.assertNotIn(module,sys.modules)
    def test_forbidden_preloaded_runtime_is_rejected(self):
        sentinel=types.ModuleType('fast_downward')
        with mock.patch.dict(sys.modules,{'fast_downward':sentinel}):
            with self.assertRaises(RuntimeError):r._open_namespace('_si_other',{'x.py':b''},{'_si_other.translate.x':'x.py'})
        self.assertNotIn('_si_other',sys.modules)

if __name__=='__main__':unittest.main(verbosity=2)
