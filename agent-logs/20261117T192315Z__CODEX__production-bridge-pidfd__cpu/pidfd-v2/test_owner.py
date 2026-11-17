"""Direct finite dummy children only; interrupted/failed state is not repaired."""
import errno
import json
import os
from pathlib import Path
import signal
import sys
import tempfile
import unittest
from unittest import mock
from owner import Owner
from prior_candidate import checked_pidfd_open

EVIDENCE=Path('test-evidence');EVIDENCE.mkdir(exist_ok=True)
def fake():return [sys.executable,'-I','-B','-c','import time;time.sleep(0.6)']

class Tests(unittest.TestCase):
    def setUp(self):
        self.root=Path(tempfile.mkdtemp(prefix='fake-',dir=EVIDENCE));self.owner=Owner(self.root/'owner')
    def tearDown(self):
        p=self.owner.child
        if p is not None and p.returncode is None:p.wait(timeout=4)
    def evidence(self,case,rc):
        print('EVIDENCE '+json.dumps({'case':case,'child_pid':self.owner.child.pid,'state':self.owner.state,
              'durable':self.owner.durable,'reap_returncode':rc,'journal':str(self.owner.path)},sort_keys=True),flush=True)
    def test_open_runtimeerror_retains_child(self):
        self.assertTrue(self.owner.launch(fake()))
        def fail(_):raise RuntimeError('injected pidfd failure')
        self.assertFalse(self.owner.terminate(open_pidfd=fail))
        self.assertEqual(self.owner.state,'UNKNOWN');self.assertIsNotNone(self.owner.child)
        rc=self.owner.await_natural_exit(3);self.evidence('open_runtimeerror',rc);self.assertEqual(rc,0)
    def test_sigint_before_popen_return_is_deferred_until_owned(self):
        import subprocess
        real_popen=subprocess.Popen
        def interrupted_popen(*args,**kwargs):
            proc=real_popen(*args,**kwargs)
            signal.raise_signal(signal.SIGINT)
            return proc
        with mock.patch('owner.subprocess.Popen',side_effect=interrupted_popen):
            with self.assertRaises(KeyboardInterrupt):self.owner.launch(fake())
        self.assertEqual(self.owner.state,'UNKNOWN');self.assertIsNotNone(self.owner.child)
        self.assertIs(signal.getsignal(signal.SIGINT),signal.default_int_handler)
        rc=self.owner.await_natural_exit(3);self.evidence('spawn_sigint',rc);self.assertEqual(rc,0)
    def test_open_keyboardinterrupt_propagates_and_retains(self):
        self.assertTrue(self.owner.launch(fake()))
        def fail(_):raise KeyboardInterrupt()
        with self.assertRaises(KeyboardInterrupt):self.owner.terminate(open_pidfd=fail)
        self.assertEqual(self.owner.state,'UNKNOWN');self.assertIsNotNone(self.owner.child)
        rc=self.owner.await_natural_exit(3);self.evidence('open_interrupt',rc);self.assertEqual(rc,0)
    def test_send_runtimeerror_closes_fd_and_retains(self):
        self.assertTrue(self.owner.launch(fake()));seen=[]
        def bind(pid):
            fd=checked_pidfd_open(pid);seen.append(fd);return fd
        def fail(*args):raise RuntimeError('injected send failure')
        self.assertFalse(self.owner.terminate(open_pidfd=bind,send=fail))
        with self.assertRaises(OSError) as ex:os.fstat(seen[0])
        self.assertEqual(ex.exception.errno,errno.EBADF)
        rc=self.owner.await_natural_exit(3);self.evidence('send_runtimeerror',rc);self.assertEqual(rc,0)
    def test_sigint_propagates_after_open_closes_fd_retains(self):
        self.assertTrue(self.owner.launch(fake()));seen=[]
        def bind(pid):
            fd=checked_pidfd_open(pid);seen.append(fd);return fd
        def interrupt(*args):signal.raise_signal(signal.SIGINT)
        with self.assertRaises(KeyboardInterrupt):self.owner.terminate(open_pidfd=bind,send=interrupt)
        self.assertEqual(self.owner.state,'UNKNOWN')
        with self.assertRaises(OSError) as ex:os.fstat(seen[0])
        self.assertEqual(ex.exception.errno,errno.EBADF)
        rc=self.owner.await_natural_exit(3);self.evidence('send_sigint',rc);self.assertEqual(rc,0)
    def test_actual_pidfd_signal_and_reap(self):
        self.assertTrue(self.owner.launch(fake()))
        self.assertTrue(self.owner.terminate(wait_seconds=1));self.assertEqual(self.owner.state,'REAPED')
        self.assertEqual(self.owner.child.returncode,-signal.SIGTERM)
        self.evidence('actual_pidfd',self.owner.child.returncode)

if __name__=='__main__':unittest.main(verbosity=2)
