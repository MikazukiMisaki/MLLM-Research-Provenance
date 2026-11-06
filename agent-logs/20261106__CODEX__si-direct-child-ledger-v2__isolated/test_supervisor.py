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


def identity(path):
    value = os.stat(path, follow_symlinks=False)
    return value.st_dev, value.st_ino


class SupervisorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.claims = self.base / "claims"
        self.ledgers = self.base / "ledgers"
        self.claims.mkdir()
        self.ledgers.mkdir()
        self.claim_identity = identity(self.claims)
        self.ledger_identity = identity(self.ledgers)
        self.root_fd = os.open(self.base, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        self.dirs = supervisor.DirectoryBinding(self.root_fd, ("claims",), ("ledgers",),
                                                self.claim_identity, self.ledger_identity)

    def tearDown(self):
        self.dirs.close()
        os.close(self.root_fd)
        self.temp.cleanup()

    def run_one(self, name="run", mode="success", timeout=1):
        return supervisor.run_synthetic(name, self.dirs, mode, timeout)

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
            supervisor.DirectoryBinding(self.root_fd, ("claims",), ("claims",), self.claim_identity, self.claim_identity)
        with self.assertRaises(supervisor.Stop):
            self.run_one(mode="model")
        self.assertEqual(list(self.claims.iterdir()), [])

    def test_parent_chain_symlinks_rejected_without_launch(self):
        outside = self.base / "outside"
        outside.mkdir()
        (self.base / "claims_link").symlink_to(outside, target_is_directory=True)
        (self.base / "outer").mkdir()
        (self.base / "outer" / "link").symlink_to(outside, target_is_directory=True)
        for path in (("claims_link",), ("outer", "link")):
            with self.subTest(path=path), self.assertRaises(OSError):
                supervisor.DirectoryBinding(self.root_fd, path, ("ledgers",), self.claim_identity, self.ledger_identity)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertEqual(list(self.ledgers.iterdir()), [])

    def test_open_chain_rejects_unsafe_components(self):
        for parts in ((), ("..",), (".",), ("",), ("claims/../ledgers",), ("x\x00y",)):
            with self.subTest(parts=parts), self.assertRaises(supervisor.Stop):
                supervisor.DirectoryBinding(self.root_fd, parts, ("ledgers",), self.claim_identity, self.ledger_identity)

    def test_root_must_be_directory_and_expected_identities_required(self):
        root_file = self.base / "not_a_directory"
        root_file.write_text("synthetic")
        fd = os.open(root_file, os.O_RDONLY)
        try:
            with self.assertRaises(supervisor.Stop):
                supervisor.DirectoryBinding(fd, ("claims",), ("ledgers",), self.claim_identity, self.ledger_identity)
        finally:
            os.close(fd)
        for invalid in (None, (True, 2), (1,), (-1, 2)):
            with self.subTest(invalid=invalid), self.assertRaises(supervisor.Stop):
                supervisor.DirectoryBinding(self.root_fd, ("claims",), ("ledgers",), invalid, self.ledger_identity)

    def test_replaced_parent_does_not_redirect_pinned_claim(self):
        replacement = self.base / "replacement"
        replacement.mkdir()
        moved = self.base / "moved_claims"
        self.claims.rename(moved)
        self.claims.symlink_to(replacement, target_is_directory=True)
        result = self.run_one()
        self.assertEqual(result["status"], "SYNTHETIC_COMPLETE")
        self.assert_reaped(result["pid"])
        self.assertTrue((moved / "run.claim").is_file())
        self.assertEqual(list(replacement.iterdir()), [])
        with self.assertRaises(FileExistsError):
            self.run_one()
        with self.assertRaises(OSError):
            supervisor.DirectoryBinding(self.root_fd, ("claims",), ("ledgers",), self.claim_identity, self.ledger_identity)

    def test_regular_directory_replacement_before_binding_is_rejected(self):
        moved = self.base / "moved_claims"
        self.claims.rename(moved)
        self.claims.mkdir()
        with self.assertRaisesRegex(supervisor.Stop, "directory identity mismatch"):
            supervisor.DirectoryBinding(self.root_fd, ("claims",), ("ledgers",), self.claim_identity, self.ledger_identity)
        self.assertEqual(list(self.claims.iterdir()), [])
        self.assertEqual(list(self.ledgers.iterdir()), [])
        self.assertEqual(list(moved.iterdir()), [])

    def test_replaced_ledger_parent_does_not_redirect_pinned_ledger(self):
        replacement = self.base / "replacement"
        replacement.mkdir()
        moved = self.base / "moved_ledgers"
        self.ledgers.rename(moved)
        self.ledgers.symlink_to(replacement, target_is_directory=True)
        result = self.run_one()
        self.assertEqual(result["status"], "SYNTHETIC_COMPLETE")
        self.assert_reaped(result["pid"])
        self.assertTrue((moved / "run.jsonl").is_file())
        self.assertEqual(list(replacement.iterdir()), [])

    def test_replacement_during_chain_resolution_stays_on_open_parent(self):
        parent = self.base / "outer"
        (parent / "nested").mkdir(parents=True)
        nested_identity = identity(parent / "nested")
        replacement = self.base / "impostor"
        (replacement / "nested").mkdir(parents=True)
        moved = self.base / "old_outer"
        real_open = os.open
        changed = False
        def racing_open(path, flags, *args, **kwargs):
            nonlocal changed
            fd = real_open(path, flags, *args, **kwargs)
            if path == "outer" and kwargs.get("dir_fd") is not None and not changed:
                changed = True
                parent.rename(moved)
                parent.symlink_to(replacement, target_is_directory=True)
            return fd
        with mock.patch.object(supervisor.os, "open", side_effect=racing_open):
            binding = supervisor.DirectoryBinding(self.root_fd, ("outer", "nested"), ("ledgers",), nested_identity, self.ledger_identity)
        try:
            result = supervisor.run_synthetic("chain", binding, "success", 1)
            self.assertEqual(result["status"], "SYNTHETIC_COMPLETE")
            self.assert_reaped(result["pid"])
            self.assertTrue((moved / "nested" / "chain.claim").is_file())
            self.assertEqual(list((replacement / "nested").iterdir()), [])
        finally:
            binding.close()

    def test_leaf_collisions_fail_closed(self):
        external = self.base / "external"
        external.write_text("unchanged")
        (self.claims / "run.claim").symlink_to(external)
        with self.assertRaises(FileExistsError):
            self.run_one()
        self.assertEqual(external.read_text(), "unchanged")
        self.assertEqual(list(self.ledgers.iterdir()), [])
        (self.claims / "run.claim").unlink()
        (self.ledgers / "run.jsonl").symlink_to(external)
        with self.assertRaises(FileExistsError):
            self.run_one()
        self.assertTrue((self.claims / "run.claim").exists())
        self.assertEqual(external.read_text(), "unchanged")
        with self.assertRaises(FileExistsError):
            self.run_one()


if __name__ == "__main__":
    unittest.main(verbosity=2)
