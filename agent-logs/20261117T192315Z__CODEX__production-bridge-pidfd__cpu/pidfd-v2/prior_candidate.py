"""HOLD: isolated direct-child pidfd experiment, not a process-tree supervisor."""
import ctypes
import errno
import os
import platform
import re
import signal
import subprocess
import threading
import time
from pathlib import Path

def checked_pidfd_open(pid):
    """Use Python API, or x86_64 Linux syscall only when local UAPI confirms it."""
    if hasattr(os, 'pidfd_open'):
        return os.pidfd_open(pid, 0)
    if platform.system() != 'Linux' or platform.machine() != 'x86_64':
        raise OSError(errno.ENOSYS, 'pidfd_open unavailable on this platform')
    header = Path('/usr/include/x86_64-linux-gnu/asm/unistd_64.h')
    try:
        match = re.search(r'^\s*#\s*define\s+__NR_pidfd_open\s+(\d+)\s*$', header.read_text(), re.M)
    except OSError as exc:
        raise OSError(errno.ENOSYS, 'no local syscall header') from exc
    if match is None or int(match.group(1)) != 434:
        raise OSError(errno.ENOSYS, 'unverified syscall number')
    libc = ctypes.CDLL(None, use_errno=True)
    libc.syscall.restype = ctypes.c_long
    fd = libc.syscall(ctypes.c_long(434), ctypes.c_int(pid), ctypes.c_uint(0))
    if fd < 0:
        code = ctypes.get_errno()
        raise OSError(code, os.strerror(code))
    try:os.set_inheritable(fd, False)
    except BaseException:
        os.close(fd)
        raise
    return int(fd)

def start_and_terminate(argv, *, open_pidfd=checked_pidfd_open, send=None,
                        wait_seconds=0.4, readiness_seconds=0.5):
    """Own direct Popen child; first bind pidfd before any wait/poll/signalling.

    Dedicated single-threaded caller, default SIGCHLD, no external child reaper.
    These are necessary assumptions, not a proof about descendants, other tasks,
    GPU processes, or callers that violate the API's isolation requirement.
    Unknown returns the Popen object so the owner may await natural exit; no
    numeric PID or process group is ever used as a signal target.
    """
    if send is None:send=getattr(signal,'pidfd_send_signal',None)
    try:
        kernel_threads=len(list(Path('/proc/self/task').iterdir()))
    except OSError:
        kernel_threads=0
    if (not callable(send) or not callable(open_pidfd) or len(threading.enumerate()) != 1 or kernel_threads != 1 or signal.getsignal(signal.SIGCHLD) != signal.SIG_DFL or
        not all(hasattr(os, k) for k in ('P_PIDFD','WNOHANG','WNOWAIT'))):
        return {'status':'UNKNOWN_PRECONDITION','signalled':False},None
    p=subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       close_fds=True, start_new_session=False)
    result={'pid':p.pid,'status':'UNKNOWN','signalled':False,'method':'pidfd_direct_child_only'}
    fd=None
    try:
        # No intervening poll/wait: SIGCHLD default and no external waiter mean
        # the direct child PID cannot be reused before pidfd_open, even if exited.
        fd=open_pidfd(p.pid)
        # P_PIDFD waitid confirms the file descriptor is our waitable child,
        # without reaping it; a child that already exited needs no signal.
        state=os.waitid(os.P_PIDFD,fd,os.WEXITED|os.WNOHANG|os.WNOWAIT)
        if state is not None:
            result.update(status='EXITED_BEFORE_SIGNAL',returncode=p.wait(timeout=wait_seconds))
            return result,p
        # A finite test child may install its own handler; the descriptor, not a
        # numeric identity, remains the only signal target. Sleep is test-only.
        if readiness_seconds:time.sleep(readiness_seconds)
        state=os.waitid(os.P_PIDFD,fd,os.WEXITED|os.WNOHANG|os.WNOWAIT)
        if state is not None:
            result.update(status='EXITED_BEFORE_SIGNAL',returncode=p.wait(timeout=wait_seconds))
            return result,p
        send(fd,signal.SIGTERM,None,0)
        result['signalled']=True
        try:
            result.update(status='DIRECT_CHILD_REAPED',returncode=p.wait(timeout=wait_seconds))
        except subprocess.TimeoutExpired:
            result.update(status='UNKNOWN_CHILD_NOT_EXITED')
        return result,p
    except (OSError,ChildProcessError,ValueError) as exc:
        result.update(status='UNKNOWN_BIND_OR_SIGNAL',error_type=type(exc).__name__,errno=getattr(exc,'errno',None))
        return result,p
    finally:
        if fd is not None:os.close(fd)
