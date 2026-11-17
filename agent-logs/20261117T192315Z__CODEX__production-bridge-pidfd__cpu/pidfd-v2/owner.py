"""Synthetic direct-child owner candidate; HOLD, not a production supervisor."""
import json
import os
from pathlib import Path
import signal
import subprocess
import threading
from prior_candidate import checked_pidfd_open

class Owner:
    """A long-lived object owns one Popen even if later operations throw.

    Only for a dedicated single-threaded process with default SIGINT/SIGCHLD and
    no other child waiter.  SIGINT during Popen is deferred until child is stored.
    Never use for a real experiment; all life-cycle boundaries need integration.
    """
    def __init__(self,root):
        self.root=Path(root);self.root.mkdir(mode=0o700,exist_ok=False)
        self.path=self.root/'owner.jsonl';self.child=None;self.state='NEW';self.durable=True
        fd=os.open(self.path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);os.close(fd)
        fd=os.open(self.root,os.O_RDONLY|os.O_DIRECTORY)
        try:os.fsync(fd)
        finally:os.close(fd)
        self._record('CREATED')
    def _record(self,state,**extra):
        row={'state':state,**extra};line=(json.dumps(row,sort_keys=True)+'\n').encode()
        fd=os.open(self.path,os.O_WRONLY|os.O_APPEND|os.O_NOFOLLOW)
        try:
            view=memoryview(line)
            while view:
                n=os.write(fd,view)
                if n<=0:raise OSError('journal write')
                view=view[n:]
            os.fsync(fd)
        finally:os.close(fd)
    def _unknown(self,error):
        self.state='UNKNOWN'
        try:self._record('UNKNOWN',error_type=type(error).__name__,child_pid=self.child.pid if self.child else None)
        except BaseException as record_error:
            self.durable=False
            if isinstance(record_error,(KeyboardInterrupt,SystemExit)):raise
    def launch(self,argv):
        try:count=len(list(Path('/proc/self/task').iterdir()))
        except OSError:count=0
        if (self.state!='NEW' or self.child is not None or count!=1 or len(threading.enumerate())!=1 or
            signal.getsignal(signal.SIGCHLD)!=signal.SIG_DFL or signal.getsignal(signal.SIGINT)!=signal.default_int_handler):
            self.state='UNKNOWN';self._record('UNKNOWN',reason='preconditions');return False
        pending=[]
        def defer(sig,frame):pending.append((sig,frame))
        old=signal.signal(signal.SIGINT,defer)
        try:
            try:
                self._record('SPAWN_START')
                self.child=subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,
                                            stderr=subprocess.DEVNULL,close_fds=True)
                self.state='CHILD_OWNED'
                self._record('CHILD_OWNED',child_pid=self.child.pid)
            finally:
                signal.signal(signal.SIGINT,old)
            if pending:
                signal.default_int_handler(*pending[0])
            return True
        except BaseException as error:
            self._unknown(error)
            raise
    def terminate(self,*,open_pidfd=checked_pidfd_open,send=signal.pidfd_send_signal,wait_seconds=0.25):
        if self.state!='CHILD_OWNED' or self.child is None:raise RuntimeError('not owned')
        fd=None
        try:
            # Child cannot be reaped/reused before binding under declared ownership assumptions.
            fd=open_pidfd(self.child.pid)
            info=Path('/proc/self/fdinfo')/str(fd)
            fields=dict(line.split(':',1) for line in info.read_text().splitlines() if ':' in line)
            if int(fields.get('Pid','-1').strip())!=self.child.pid:raise ValueError('fd/Popen pid mismatch')
            status=os.waitid(os.P_PIDFD,fd,os.WEXITED|os.WNOHANG|os.WNOWAIT)
            if status is None:send(fd,signal.SIGTERM,None,0)
            try:rc=self.child.wait(timeout=wait_seconds)
            except subprocess.TimeoutExpired:
                self._unknown(TimeoutError('direct child still active'));return False
            self.state='REAPED';self._record('REAPED',returncode=rc);return True
        except BaseException as error:
            self._unknown(error)
            if isinstance(error,(KeyboardInterrupt,SystemExit)):raise
            return False
        finally:
            if fd is not None:
                try:os.close(fd)
                except BaseException as error:
                    self._unknown(error)
                    if isinstance(error,(KeyboardInterrupt,SystemExit)):raise
                    raise RuntimeError('pidfd close failed; direct child state UNKNOWN') from error
    def await_natural_exit(self,timeout):
        """Separate test observation; never converts earlier UNKNOWN into success."""
        if self.child is None:raise RuntimeError('no child handle')
        rc=self.child.wait(timeout=timeout)
        try:self._record('NATURAL_REAP_OBSERVED',returncode=rc,prior_state=self.state)
        except BaseException as error:
            self.durable=False
            if isinstance(error,(KeyboardInterrupt,SystemExit)):raise
        return rc
