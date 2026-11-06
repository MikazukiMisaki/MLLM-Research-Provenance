"""In-memory and temporary-file tests only; no real subprocess or engine."""
import copy
import hashlib
import json
import os
from pathlib import Path
import signal
import tempfile
import unittest
from unittest import mock

import bindings
import contract
import owner
import worker


def replay(events):
    policy = owner.Protocol()
    for sequence, event in enumerate(events, 1):
        policy.accept({"sequence": sequence, **event})
    return policy


class Tests(unittest.TestCase):
    def test_six_step_contract_matches_frozen_development_binding(self):
        raw = Path(os.environ["PLAN_BINDING"]).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), "c33f4660e5ce1d99c7ad367ca3bda4fc6d7ee7be4b11037a87985dee9da2cb81")
        binding = json.loads(raw)["cases"]["clean-1"]
        self.assertEqual(binding["new_independent_static_review"], "NOT_READY")
        rows = [{"command": command, "name": name, "mapping": mapping} for command, name, mapping in contract.PLAN]
        self.assertEqual(rows, binding["proposed_steps"])

    def test_real_entries_refuse_before_io_or_process(self):
        with mock.patch.object(owner.subprocess, "Popen") as popen, \
             mock.patch.object(owner.bindings, "read_inputs") as inputs, \
             mock.patch.object(owner.os, "open") as file_open:
            with self.assertRaisesRegex(RuntimeError, "REAL_OWNER_DISABLED"):
                owner.supervise(None, "ignored", {})
            popen.assert_not_called()
            inputs.assert_not_called()
            file_open.assert_not_called()
        with mock.patch.object(worker, "setup_parent_death") as setup:
            with self.assertRaisesRegex(RuntimeError, "REAL_WORKER_DISABLED"):
                worker.real_main()
            setup.assert_not_called()
        with self.assertRaisesRegex(RuntimeError, "REAL_WORKER_DISABLED"):
            worker.RealFactory().construct()

    def test_full_fake_worker_and_owner_protocol(self):
        factory, rpc = worker.FakeFactory(), worker.FakeRPC()
        worker.run_contract(factory, {}, rpc)
        policy = replay(rpc.events)
        self.assertTrue(policy.complete)
        self.assertEqual(factory.world.calls, ["load", "reset"] + ["step"] * 6 + ["close"])
        starts = [(e["op"], e["index"]) for e in rpc.events if e["type"] == "START"]
        self.assertEqual(starts, owner.ORDER)
        self.assertEqual(sum(e["type"] == "GROUND" for e in rpc.events), 6)
        self.assertEqual([e["stage"] for e in rpc.events if e["type"] == "OBS"], list(range(7)))

    def test_worker_faults_stop_or_keep_open(self):
        for fault in ("construct", "load", "reset", "duplicate", "wrong-facts", "identity", "step", "close"):
            with self.subTest(fault=fault):
                factory, rpc = worker.FakeFactory(fault), worker.FakeRPC()
                with self.assertRaises(Exception):
                    worker.run_contract(factory, {}, rpc)
                self.assertNotIn("COMPLETE", [e["type"] for e in rpc.events])
                self.assertLessEqual(factory.world.calls.count("step"), 6)
                self.assertFalse(replay(rpc.events).complete)
        factory, rpc = worker.FakeFactory(), worker.FakeRPC(fail_at=("START", "step", 0))
        with self.assertRaises(RuntimeError):
            worker.run_contract(factory, {}, rpc)
        self.assertNotIn("step", factory.world.calls)
        self.assertNotIn("COMPLETE", [e["type"] for e in rpc.events])

    def test_owner_protocol_rejects_forged_or_skipped_evidence(self):
        rpc = worker.FakeRPC()
        worker.run_contract(worker.FakeFactory(), {}, rpc)
        for field in ("sequence", "ground", "facts", "last_action", "bool_stage", "early_complete"):
            events = copy.deepcopy(rpc.events)
            with self.subTest(field=field):
                if field == "ground":
                    next(e for e in events if e["type"] == "GROUND")["mapping"]["a"] = "impostor"
                elif field == "facts":
                    next(e for e in events if e["type"] == "OBS")["state"]["facts"] = []
                elif field == "last_action":
                    next(e for e in events if e["type"] == "OBS" and e["stage"] == 1)["state"]["last_action"] = None
                elif field == "bool_stage":
                    next(e for e in events if e["type"] == "OBS" and e["stage"] == 1)["stage"] = True
                elif field == "early_complete":
                    events = events[:4] + [{"type": "COMPLETE", "steps": 6}]
                policy = owner.Protocol()
                with self.assertRaises(ValueError):
                    for index, event in enumerate(events, 1):
                        policy.accept({"sequence": index + (1 if field == "sequence" and index == 2 else 0), **event})

    def test_limits_use_only_fake_api(self):
        class FakeResource:
            RLIMIT_CPU = 1
            RLIMIT_AS = 2
            RLIMIT_FSIZE = 3
            RLIMIT_CORE = 4
            def __init__(self):
                self.values = {}
            def setrlimit(self, kind, value):
                self.values[kind] = value
            def getrlimit(self, kind):
                return self.values[kind]
        api = FakeResource()
        self.assertEqual(worker.apply_limits(api), {k: list(v) for k, v in worker.LIMITS.items()})
        api.getrlimit = lambda _kind: (0, 0)
        with self.assertRaisesRegex(RuntimeError, "direct_worker_limit_mismatch"):
            worker.apply_limits(api)

    def test_parent_handshake_signal_mask_is_mocked(self):
        class Lib:
            def prctl(self, *args):
                return 0
        with mock.patch.object(worker.ctypes, "CDLL", return_value=Lib()), \
             mock.patch.object(worker.signal, "signal") as set_signal, \
             mock.patch.object(worker.signal, "pthread_sigmask", return_value=set()) as mask, \
             mock.patch.object(worker.os, "getppid", return_value=123):
            worker.setup_parent_death(123)
            set_signal.assert_called_once_with(signal.SIGTERM, signal.SIG_DFL)
            self.assertEqual(mask.call_args_list[0].args, (signal.SIG_UNBLOCK, {signal.SIGTERM}))
        with mock.patch.object(worker.ctypes, "CDLL", return_value=Lib()), \
             mock.patch.object(worker.signal, "signal"), \
             mock.patch.object(worker.signal, "pthread_sigmask", return_value={signal.SIGTERM}), \
             mock.patch.object(worker.os, "getppid", return_value=123):
            with self.assertRaisesRegex(RuntimeError, "parent_or_signal_mask_invalid"):
                worker.setup_parent_death(123)

    def test_owner_rejects_bad_ready_pid_or_limits(self):
        ready = {"type": "READY", "pid": 123, "limits": {key: list(value) for key, value in worker.LIMITS.items()}}
        owner.check_ready(ready, 123)
        for change in ("pid", "limits", "type"):
            altered = copy.deepcopy(ready)
            if change == "pid":
                altered["pid"] = 124
            elif change == "limits":
                altered["limits"]["RLIMIT_CPU"] = [25, 31]
            else:
                altered["type"] = "not-ready"
            with self.subTest(change=change), self.assertRaises(ValueError):
                owner.check_ready(altered, 123)

    def test_one_shot_claim_and_journal_fsync_with_temp_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            dir_fd = os.open(tmp, os.O_RDONLY | os.O_DIRECTORY)
            try:
                owner.create_claim(dir_fd, {"id": "fake"})
                with self.assertRaises(FileExistsError):
                    owner.create_claim(dir_fd, {"id": "fake"})
                journal = owner.Journal(dir_fd)
                journal.append("step_started", {"index": 0})
                journal.append("step_returned", {"index": 0})
                journal.close()
                rows = [json.loads(line) for line in (Path(tmp) / "owner.jsonl").read_text().splitlines()]
                self.assertEqual(rows[1]["previous"], rows[0]["hash"])
                for row in rows:
                    body = {k: v for k, v in row.items() if k != "hash"}
                    self.assertEqual(hashlib.sha256(owner._encode(body)).hexdigest(), row["hash"])
            finally:
                os.close(dir_fd)

    def test_failed_claim_fsync_still_blocks_retry_in_same_filesystem_view(self):
        with tempfile.TemporaryDirectory() as tmp:
            dir_fd = os.open(tmp, os.O_RDONLY | os.O_DIRECTORY)
            try:
                with mock.patch.object(owner.os, "fsync", side_effect=OSError("injected")):
                    with self.assertRaises(OSError):
                        owner.create_claim(dir_fd, {"id": "fake"})
                with self.assertRaises(FileExistsError):
                    owner.create_claim(dir_fd, {"id": "fake"})
            finally:
                os.close(dir_fd)

    def test_fsync_failure_marks_journal_unusable(self):
        with tempfile.TemporaryDirectory() as tmp:
            dir_fd = os.open(tmp, os.O_RDONLY | os.O_DIRECTORY)
            journal = owner.Journal(dir_fd)
            try:
                with mock.patch.object(owner.os, "fsync", side_effect=OSError("injected")):
                    with self.assertRaises(OSError):
                        journal.append("step_started", {"index": 0})
                self.assertFalse(journal.healthy)
                with self.assertRaisesRegex(RuntimeError, "journal_unavailable"):
                    journal.append("attempt_unknown", {})
            finally:
                journal.close()
                os.close(dir_fd)

    def test_no_go_or_ack_before_successful_fsync(self):
        pipe = mock.Mock()
        journal = mock.Mock()
        journal.append.side_effect = OSError("synthetic fsync failure")
        with self.assertRaises(OSError):
            owner.send_go(journal, pipe, 123, {})
        pipe.write.assert_not_called()
        with self.assertRaises(OSError):
            owner.authorize_event(owner.Protocol(), journal, pipe,
                                  {"sequence": 1, "type": "START", "op": "construct", "index": None})
        pipe.write.assert_not_called()
        calls = []
        journal.append.side_effect = lambda *args: calls.append("fsync_returned")
        pipe.write.side_effect = lambda _value: calls.append("write")
        pipe.flush.side_effect = lambda: calls.append("flush")
        owner.send_go(journal, pipe, 123, {})
        self.assertEqual(calls, ["fsync_returned", "write", "flush"])
        calls.clear()
        owner.authorize_event(owner.Protocol(), journal, pipe,
                              {"sequence": 1, "type": "START", "op": "construct", "index": None})
        self.assertEqual(calls, ["fsync_returned", "write", "flush"])

    def test_direct_pidfd_termination_and_wait_are_fakes(self):
        class Clock:
            value = 0.0
            def now(self):
                self.value += 0.2
                return self.value
            def sleep(self, _):
                pass
        class Usage:
            ru_utime, ru_stime, ru_maxrss = 0.2, 0.1, 1024
        clock = Clock()
        sent = []
        calls = []
        def wait_fn(pid, _flags):
            calls.append(pid)
            if len(calls) < 7:
                return 0, 0, None
            return pid, signal.SIGKILL, Usage()
        result = owner.stop_direct(456, 99, wait_fn=wait_fn, now=clock.now, pause=clock.sleep,
                                   send=lambda fd, sig: sent.append((fd, sig)))
        self.assertEqual(sent, [(99, signal.SIGTERM), (99, signal.SIGKILL)])
        self.assertEqual(result["exit_code"], -signal.SIGKILL)
        self.assertEqual(result["maxrss_linux_kib"], 1024)
        self.assertTrue(all(pid == 456 for pid in calls))

    def test_fake_input_hashes_and_manifest_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            problem, grammar, domain = b"fake problem", b"fake grammar", b"fake domain"
            digest = lambda value: hashlib.sha256(value).hexdigest()
            manifest = json.dumps({"case": "clean-1", "status": "DEVELOPMENT_ONLY_STATIC_DRAFT",
                                   "problem_sha256": digest(problem), "grammar_sha256": digest(grammar)}).encode()
            pins = {}
            for name, value in (("problem", problem), ("grammar", grammar), ("domain", domain), ("manifest", manifest)):
                path = root / name
                path.write_bytes(value)
                pins[name] = (path, digest(value))
            result = bindings.read_inputs(pins)
            self.assertEqual(result["problem"], problem)
            (root / "problem").write_bytes(b"changed")
            with self.assertRaisesRegex(ValueError, "input_binding_mismatch"):
                bindings.read_inputs(pins)


if __name__ == "__main__":
    unittest.main(verbosity=2)
