"""Real direct subprocesses run a fixed invented program; no model or GPU."""

import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import signal
import tempfile
import unittest
from unittest import mock

import supervisor


class SupervisorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.claims = self.base / "claims"
        self.ledgers = self.base / "ledgers"
        self.claims.mkdir()
        self.ledgers.mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def run_one(self, name="run", mode="success", timeout=1):
        return supervisor.run_synthetic(name, str(self.claims), str(self.ledgers), mode, timeout)

    def events(self, name="run"):
        return [json.loads(line) for line in (self.ledgers / (name + ".jsonl")).read_text().splitlines()]

    def assert_reaped(self, pid):
        with self.assertRaises(ChildProcessError):
            os.waitpid(pid, os.WNOHANG)

    def test_success_and_durable_event_order(self):
        self.assertFalse(supervisor.REAL_MODEL_ENABLED)
        self.assertFalse(supervisor.GPU_EXECUTION_ENABLED)
        result = self.run_one()
        self.assertEqual(result["status"], "SYNTHETIC_COMPLETE")
        self.assertEqual(result["cleanup"], "reaped")
        self.assert_reaped(result["pid"])
        events = self.events()
        self.assertEqual([(e["operation"], e["state"]) for e in events],
                         [("attempt", "started"), ("spawn", "started"), ("spawn", "returned"),
                          ("worker", "started"), ("worker", "returned"), ("cleanup", "returned"),
                          ("attempt", "returned")])
        previous = "0" * 64
        for event in events:
            self.assertEqual(event["previous"], previous)
            body = {k: v for k, v in event.items() if k != "hash"}
            self.assertEqual(event["hash"], hashlib.sha256(supervisor._encode(body)).hexdigest())
            previous = event["hash"]
        self.assertEqual(events[4]["detail"]["exit_code"], 0)

    def test_real_child_crash_is_unknown_without_retry(self):
        result = self.run_one(mode="crash")
        self.assertEqual(result["status"], "INCOMPLETE_UNKNOWN")
        self.assertEqual(result["cleanup"], "reaped")
        self.assert_reaped(result["pid"])
        events = self.events()
        self.assertEqual([e["detail"].get("exit_code") for e in events if e["operation"] == "worker" and e["state"] == "returned"], [17])
        self.assertEqual((events[-1]["operation"], events[-1]["state"]), ("attempt", "unknown"))
        with self.assertRaises(FileExistsError):
            self.run_one(mode="success")
        self.assertEqual(self.events(), events)

    def test_real_child_timeout_is_stopped_via_pidfd_and_reaped(self):
        result = self.run_one(mode="hang", timeout=0.08)
        self.assertEqual(result["status"], "INCOMPLETE_UNKNOWN")
        self.assertEqual(result["reason"], "synthetic worker timeout")
        self.assertEqual(result["cleanup"], "reaped")
        self.assertIn(result["exit_code"], (-signal.SIGTERM, -signal.SIGKILL))
        self.assert_reaped(result["pid"])
        events = self.events()
        self.assertNotIn(("worker", "returned"), [(e["operation"], e["state"]) for e in events])
        self.assertEqual((events[-1]["operation"], events[-1]["state"]), ("attempt", "unknown"))
        with self.assertRaises(FileExistsError):
            self.run_one()

    def test_two_simultaneous_attempts_only_one_claims(self):
        def attempt():
            try:
                return self.run_one()
            except FileExistsError:
                return "duplicate"
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: attempt(), range(2)))
        self.assertEqual(sum(result == "duplicate" for result in results), 1)
        complete = next(result for result in results if result != "duplicate")
        self.assertEqual(complete["status"], "SYNTHETIC_COMPLETE")
        self.assert_reaped(complete["pid"])
        self.assertEqual(sum(e["operation"] == "spawn" and e["state"] == "returned" for e in self.events()), 1)

    def test_partial_ledger_write_stops_child_and_marks_ledger_unavailable(self):
        real_write = os.write
        failing_fd = None
        def faulty_write(fd, data):
            nonlocal failing_fd
            if b'"operation":"spawn"' in data and b'"state":"returned"' in data:
                failing_fd = fd
                return real_write(fd, data[:12])
            if failing_fd == fd:
                raise OSError("injected partial ledger write")
            return real_write(fd, data)
        with mock.patch.object(supervisor.os, "write", side_effect=faulty_write):
            result = self.run_one(mode="hang")
        self.assertEqual(result["status"], "INCOMPLETE_UNKNOWN")
        self.assertTrue(result["ledger_unavailable"])
        self.assertEqual(result["cleanup"], "reaped")
        self.assert_reaped(result["pid"])
        data = (self.ledgers / "run.jsonl").read_bytes()
        self.assertFalse(data.endswith(b"\n"))
        lines = data.splitlines()
        self.assertEqual([(json.loads(line)["operation"], json.loads(line)["state"]) for line in lines[:-1]],
                         [("attempt", "started"), ("spawn", "started")])
        with self.assertRaises(FileExistsError):
            self.run_one()

    def test_claim_fsync_failure_stops_before_spawn_and_claim_remains(self):
        with mock.patch.object(supervisor.os, "fsync", side_effect=OSError("injected claim sync failure")):
            with self.assertRaises(OSError):
                self.run_one()
        self.assertTrue((self.claims / "run.claim").exists())
        self.assertFalse((self.ledgers / "run.jsonl").exists())
        with self.assertRaises(FileExistsError):
            self.run_one()

    def test_ledger_fsync_failure_after_spawn_leaves_unknown_and_stops(self):
        original_append = supervisor.Ledger.append
        def fail_return_fsync(ledger, operation, state, **detail):
            if (operation, state) == ("spawn", "returned"):
                with mock.patch.object(supervisor.os, "fsync", side_effect=OSError("injected ledger sync failure")):
                    return original_append(ledger, operation, state, **detail)
            return original_append(ledger, operation, state, **detail)
        with mock.patch.object(supervisor.Ledger, "append", new=fail_return_fsync):
            result = self.run_one(mode="hang")
        self.assertEqual(result["status"], "INCOMPLETE_UNKNOWN")
        self.assertTrue(result["ledger_unavailable"])
        self.assertEqual(result["cleanup"], "reaped")
        self.assert_reaped(result["pid"])
        # Even if bytes are readable in page cache, the failed fsync gives no durability proof.
        self.assertNotIn(("attempt", "returned"), [(e["operation"], e["state"]) for e in self.events()])
        with self.assertRaises(FileExistsError):
            self.run_one()

    def test_invalid_inputs_and_separate_directories(self):
        for run_id in ("../escape", "", "a/b"):
            with self.assertRaises(supervisor.Stop):
                self.run_one(name=run_id)
        with self.assertRaises(supervisor.Stop):
            supervisor.run_synthetic("x", str(self.claims), str(self.claims), "success", 1)
        with self.assertRaises(supervisor.Stop):
            self.run_one(mode="model")
        self.assertEqual(list(self.claims.iterdir()), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
