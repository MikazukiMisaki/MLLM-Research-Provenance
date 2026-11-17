"""Fictional subprocess tests; no model, task asset, GPU, or environment."""
from pathlib import Path
import tempfile
import unittest
import prototype as p

class CoordinationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'run'

    def test_four_pairs_eight_distinct_arm_children(self):
        o = p.run(self.root)
        result = p.audit(o.journal)
        self.assertTrue(result['complete'])
        self.assertEqual(len(result['reserved']), 12)
        import json
        rows = [json.loads(line)['data']['receipt'] for line in o.journal.read_text().splitlines()
                if json.loads(line)['event'] == 'return']
        self.assertEqual(len({r['pid'] for r in rows if r['kind'] == 'arm'}), 8)
        for i, pair in enumerate(p.PAIRS):
            group = [r for r in rows if r['pair'] == pair]
            self.assertEqual([r['kind'] for r in group], ['setup', 'arm', 'arm'])
            self.assertEqual([r['arm'] for r in group[1:]], ['A', 'B'] if i % 2 == 0 else ['B', 'A'])
            self.assertEqual(len({r['task_hash'] for r in group}), 1)
        with self.assertRaises(p.Stop): p.run(self.root)

    def test_failure_reservation_remains_open_and_no_restart(self):
        with self.assertRaises(p.Stop): p.run(self.root, fail_on=('arm', 'two', 'A'))
        result = p.audit(self.root / 'ledger.jsonl')
        self.assertEqual(result['reserved'].keys() - result['returned'], {('arm', 'two', 'A')})
        self.assertFalse(result['complete'])
        with self.assertRaises(p.Stop): p.run(self.root)

    def test_open_reservation_blocks_future_work(self):
        o = p.Owner(self.root)
        o.reserve('setup', 'one')
        with self.assertRaises(p.Stop): o.reserve('arm', 'one', 'A')
        with self.assertRaises(p.Stop): o.reserve('setup', 'two')
        self.assertEqual(len(p.audit(o.journal)['reserved']), 1)

    def test_four_setup_cap_duplicate_and_no_refund(self):
        o = p.Owner(self.root)
        for pair in p.PAIRS: p.effect(o, 'setup', pair, None, 'a' * 64)
        with self.assertRaises(p.Stop): o.reserve('setup', 'one')
        with self.assertRaises(p.Stop): o.reserve('setup', 'five')
        self.assertEqual(len(p.audit(o.journal)['reserved']), 4)

    def test_ambiguous_or_tampered_journal_fails_closed(self):
        o = p.Owner(self.root)
        o.reserve('setup', 'one')
        raw = o.journal.read_bytes()
        o.journal.write_bytes(raw[:-1])
        with self.assertRaises(p.Stop): p.audit(o.journal)
        o.journal.write_bytes(raw.replace(b'one', b'two', 1))
        with self.assertRaises(p.Stop): p.audit(o.journal)

    def test_live_owner_stops_on_journal_tamper(self):
        o = p.Owner(self.root)
        token = o.reserve('setup', 'one')
        o.journal.write_bytes(o.journal.read_bytes().replace(b'one', b'two', 1))
        with self.assertRaises(p.Stop): o.returned_effect('setup', 'one', None, token, {})

    def test_unmatched_return_and_arm_before_setup(self):
        o = p.Owner(self.root)
        with self.assertRaises(p.Stop): o.reserve('arm', 'one', 'A')
        token = o.reserve('setup', 'one')
        with self.assertRaises(p.Stop): o.returned_effect('setup', 'one', None, token + 'x', {})
        self.assertEqual(len(p.audit(o.journal)['returned']), 0)

if __name__ == '__main__': unittest.main(verbosity=2)
