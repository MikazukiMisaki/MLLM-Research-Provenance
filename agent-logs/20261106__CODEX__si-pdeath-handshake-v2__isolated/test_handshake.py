"""Dedicated-process tests own all synthetic descendants; Linux x86_64 only."""
import ctypes
import json
import os
from pathlib import Path
import select
import signal
import subprocess
import sys
import tempfile
import time
import unittest

import owner

PR_SET_CHILD_SUBREAPER = 36
PR_GET_CHILD_SUBREAPER = 37


class HandshakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.libc = ctypes.CDLL(None, use_errno=True)
        old = ctypes.c_int()
        if cls.libc.prctl(PR_GET_CHILD_SUBREAPER, ctypes.byref(old), 0, 0, 0) != 0:
            raise OSError(ctypes.get_errno(), "cannot query subreaper")
        cls.old_subreaper = old.value
        if cls.libc.prctl(PR_SET_CHILD_SUBREAPER, 1, 0, 0, 0) != 0:
            raise OSError(ctypes.get_errno(), "cannot set test subreaper")

    @classmethod
    def tearDownClass(cls):
        cls.libc.prctl(PR_SET_CHILD_SUBREAPER, cls.old_subreaper, 0, 0, 0)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.ledger = Path(self.temp.name) / "events.jsonl"
        self.marker = Path(self.temp.name) / "child_work_started"
        self.proc = None
        self.parent_fd = None
        self.child_fd = None
        self.child_pid = None
        self.child_reaped = False
        self.pending = b""
        self.extra_read = None
        self.extra_write = None

    def tearDown(self):
        if self.proc is not None and self.proc.poll() is None:
            if self.parent_fd is not None:
                try:
                    signal.pidfd_send_signal(self.parent_fd, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            self.proc.wait(timeout=3)
        if self.child_fd is not None and not self.child_reaped:
            try:
                signal.pidfd_send_signal(self.child_fd, signal.SIGKILL)
            except ProcessLookupError:
                pass
            self.reap_known_child(raise_if_missing=False)
        if self.parent_fd is not None:
            os.close(self.parent_fd)
        if self.child_fd is not None:
            os.close(self.child_fd)
        if self.extra_read is not None:
            os.close(self.extra_read)
        if self.extra_write is not None:
            os.close(self.extra_write)
        if self.proc is not None:
            for stream in (self.proc.stdin, self.proc.stdout, self.proc.stderr):
                if stream is not None:
                    stream.close()
        # This suite runs in a dedicated test process. Reap any adopted child
        # whose PID was not emitted if setup itself failed; never signal it.
        deadline = time.monotonic() + 2
        while time.monotonic() < deadline:
            try:
                pid, _ = os.waitpid(-1, os.WNOHANG)
            except ChildProcessError:
                break
            if pid == 0:
                time.sleep(0.01)
        self.temp.cleanup()

    def reap_known_child(self, raise_if_missing=True):
        deadline = time.monotonic() + 3
        while time.monotonic() < deadline:
            try:
                pid, status = os.waitpid(self.child_pid, os.WNOHANG)
            except ChildProcessError:
                if raise_if_missing:
                    raise
                return None
            if pid:
                self.child_reaped = True
                return status
            time.sleep(0.01)
        if raise_if_missing:
            self.fail("known adopted synthetic child was not reaped")
        return None

    def receive(self, expected):
        deadline = time.monotonic() + 3
        while b"\n" not in self.pending:
            readable, _, _ = select.select([self.proc.stdout.fileno()], [], [], max(0, deadline - time.monotonic()))
            self.assertTrue(readable, "owner did not report " + expected)
            chunk = os.read(self.proc.stdout.fileno(), 4096)
            self.assertTrue(chunk, "owner closed output")
            self.pending += chunk
        line, self.pending = self.pending.split(b"\n", 1)
        event = json.loads(line)
        self.assertEqual(event["event"], expected)
        return event

    def start(self, mode="normal"):
        args = [sys.executable, "-I", str(Path(owner.__file__)), str(self.ledger), mode]
        pass_fds = ()
        if mode == "blocked_mask":
            self.extra_read, self.extra_write = os.pipe()
            args.extend((str(self.extra_read), str(self.extra_write)))
            pass_fds = (self.extra_read, self.extra_write)
        self.proc = subprocess.Popen(args,
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     text=True, bufsize=1, close_fds=True, pass_fds=pass_fds)
        self.parent_fd = owner.pidfd_open(self.proc.pid)
        self.child_pid = self.receive("SPAWNED")["child_pid"]
        self.child_fd = owner.pidfd_open(self.child_pid)

    def kill_owner(self):
        signal.pidfd_send_signal(self.parent_fd, signal.SIGKILL)
        self.assertEqual(self.proc.wait(timeout=3), -signal.SIGKILL)
        return self.reap_known_child()

    def events(self):
        return [json.loads(line) for line in self.ledger.read_text().splitlines()]

    def assert_open_unknown(self):
        events = [(x["operation"], x["state"]) for x in self.events()]
        self.assertIn(("attempt", "started"), events)
        self.assertNotIn(("attempt", "returned"), events)
        # This is an observer inference; no claim that killed owner wrote UNKNOWN.
        return events

    def report(self, case, child_exit, events):
        print("OBSERVED " + json.dumps({"case": case, "owner_exit": self.proc.returncode,
                                        "child_exit": child_exit, "events": events}, sort_keys=True), flush=True)

    def test_normal_one_ready_one_go(self):
        self.start()
        self.receive("READY")
        self.proc.stdin.write("GO\n")
        self.proc.stdin.flush()
        self.receive("ARMED")
        self.receive("BEGIN")
        self.receive("DONE")
        self.assertEqual(self.proc.wait(timeout=3), 0)
        events = [(e["operation"], e["state"]) for e in self.events()]
        self.assertEqual(events.count(("ready", "returned")), 1)
        self.assertEqual(events.count(("go", "started")), 1)
        self.assertEqual(events.count(("work", "started")), 1)
        self.assertEqual(events.count(("work", "returned")), 1)
        self.assertLess(events.index(("work", "started")), events.index(("go", "started")))
        self.assertTrue(self.marker.exists())
        self.assertEqual(events[-1], ("attempt", "returned"))
        self.report("normal", 0, events)
        # The live owner, not the test harness, reaped its direct child.
        with self.assertRaises(ChildProcessError):
            os.waitpid(self.child_pid, os.WNOHANG)
        self.child_reaped = True

    def test_owner_death_before_registration_blocks_work(self):
        self.start("prearm")
        status = self.kill_owner()
        self.assertTrue(os.WIFEXITED(status))
        self.assertEqual(os.WEXITSTATUS(status), 41)
        events = self.assert_open_unknown()
        self.assertNotIn(("go", "started"), events)
        self.assertNotIn(("work", "started"), events)
        self.assertFalse(self.marker.exists())
        self.report("owner_death_before_registration", os.waitstatus_to_exitcode(status), events)

    def test_owner_death_after_ready_before_go(self):
        self.start()
        self.receive("READY")
        status = self.kill_owner()
        self.assertTrue(os.WIFSIGNALED(status))
        self.assertEqual(os.WTERMSIG(status), signal.SIGTERM)
        events = self.assert_open_unknown()
        self.assertIn(("ready", "returned"), events)
        self.assertNotIn(("go", "started"), events)
        self.assertNotIn(("work", "started"), events)
        self.assertFalse(self.marker.exists())
        self.report("owner_death_after_ready", os.waitstatus_to_exitcode(status), events)

    def test_owner_death_after_go_keeps_work_open_unknown(self):
        self.start()
        self.receive("READY")
        self.proc.stdin.write("GO\n")
        self.proc.stdin.flush()
        self.receive("ARMED")
        self.receive("BEGIN")
        status = self.kill_owner()
        self.assertTrue(os.WIFSIGNALED(status))
        self.assertEqual(os.WTERMSIG(status), signal.SIGTERM)
        events = self.assert_open_unknown()
        self.assertIn(("go", "started"), events)
        self.assertIn(("work", "started"), events)
        self.assertNotIn(("work", "returned"), events)
        self.assertTrue(self.marker.exists())
        self.report("owner_death_after_go", os.waitstatus_to_exitcode(status), events)

    def test_go_not_supplied_stops_without_work(self):
        self.start()
        self.receive("READY")
        self.proc.stdin.close()
        self.assertNotEqual(self.proc.wait(timeout=3), 0)
        with self.assertRaises(ChildProcessError):
            os.waitpid(self.child_pid, os.WNOHANG)
        self.child_reaped = True  # the live owner performed direct-child wait
        events = [(e["operation"], e["state"]) for e in self.events()]
        self.assertIn(("attempt", "unknown"), events)
        self.assertNotIn(("go", "started"), events)
        self.assertNotIn(("work", "started"), events)
        self.assertFalse(self.marker.exists())
        self.report("missing_go", None, events)

    def test_work_start_fsync_failure_never_sends_go(self):
        self.start("fail_work_sync")
        self.receive("READY")
        self.proc.stdin.write("GO\n")
        self.proc.stdin.flush()
        self.assertNotEqual(self.proc.wait(timeout=3), 0)
        with self.assertRaises(ChildProcessError):
            os.waitpid(self.child_pid, os.WNOHANG)
        self.child_reaped = True
        events = [(e["operation"], e["state"]) for e in self.events()]
        self.assertNotIn(("go", "started"), events)
        self.assertNotIn(("work", "returned"), events)
        self.assertIn(("attempt", "unknown"), events)
        self.assertFalse(self.marker.exists())
        self.report("work_start_fsync_failed", None, events)

    def test_go_pipe_failure_leaves_started_unknown(self):
        self.start("gofail")
        self.receive("READY")
        self.proc.stdin.write("GO\n")
        self.proc.stdin.flush()
        self.receive("ARMED")
        self.assertNotEqual(self.proc.wait(timeout=3), 0)
        with self.assertRaises(ChildProcessError):
            os.waitpid(self.child_pid, os.WNOHANG)
        self.child_reaped = True
        events = [(e["operation"], e["state"]) for e in self.events()]
        self.assertIn(("work", "started"), events)
        self.assertIn(("go", "started"), events)
        self.assertNotIn(("work", "returned"), events)
        self.assertIn(("attempt", "unknown"), events)
        self.assertFalse(self.marker.exists())
        self.report("go_pipe_failed", None, events)

    def test_owner_death_between_started_and_go_leaves_unknown(self):
        self.start("pause_after_started")
        self.receive("READY")
        self.proc.stdin.write("GO\n")
        self.proc.stdin.flush()
        self.receive("ARMED")
        status = self.kill_owner()
        self.assertTrue(os.WIFSIGNALED(status))
        self.assertEqual(os.WTERMSIG(status), signal.SIGTERM)
        events = self.assert_open_unknown()
        self.assertIn(("work", "started"), events)
        self.assertNotIn(("work", "returned"), events)
        self.assertNotIn(("go", "started"), events)
        self.assertFalse(self.marker.exists())
        self.report("owner_death_after_started_before_go", os.waitstatus_to_exitcode(status), events)

    def test_inherited_blocked_sigterm_is_unblocked_with_extra_pipe_writer(self):
        old_mask = signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGTERM})
        try:
            self.start("blocked_mask")
        finally:
            signal.pthread_sigmask(signal.SIG_SETMASK, old_mask)
        self.receive("READY")
        status = self.kill_owner()
        self.assertTrue(os.WIFSIGNALED(status))
        self.assertEqual(os.WTERMSIG(status), signal.SIGTERM)
        # A retained read fd observes no HUP: this test still holds a writer.
        poller = select.poll()
        poller.register(self.extra_read, select.POLLHUP | select.POLLERR)
        self.assertFalse(any(mask & (select.POLLHUP | select.POLLERR) for _, mask in poller.poll(0)))
        events = self.assert_open_unknown()
        self.assertIn(("ready", "returned"), events)
        self.assertNotIn(("work", "started"), events)
        self.assertNotIn(("go", "started"), events)
        self.assertFalse(self.marker.exists())
        self.report("inherited_blocked_sigterm_extra_writer", os.waitstatus_to_exitcode(status), events)


if __name__ == "__main__":
    unittest.main(verbosity=2)
