"""Fixed invented child. No model, accelerator, environment or real work."""
import ctypes
import os
import select
import signal
import sys
import time

PR_SET_PDEATHSIG = 1
expected_parent = int(sys.argv[1])
test_mode = sys.argv[2]
marker_path = sys.argv[3]

# A test-only pre-registration pause exposes the unresolved setup window.
# It performs no synthetic workload.
if test_mode == "prearm":
    time.sleep(0.35)

signal.signal(signal.SIGTERM, signal.SIG_DFL)
libc = ctypes.CDLL(None, use_errno=True)
if libc.prctl(PR_SET_PDEATHSIG, signal.SIGTERM, 0, 0, 0) != 0:
    os._exit(40)
signal.pthread_sigmask(signal.SIG_UNBLOCK, {signal.SIGTERM})
if signal.SIGTERM in signal.pthread_sigmask(signal.SIG_BLOCK, set()):
    # Do not treat an installed but blocked parent-death signal as protection.
    print("TERM_BLOCKED", flush=True)
    os._exit(44)


def parent_and_pipe_alive():
    if os.getppid() != expected_parent:
        return False
    try:
        os.kill(expected_parent, 0)  # liveness check only; never a signal delivery
    except OSError:
        return False
    poller = select.poll()
    poller.register(sys.stdin.fileno(), select.POLLHUP | select.POLLERR)
    return not any(mask & (select.POLLHUP | select.POLLERR | select.POLLNVAL) for _, mask in poller.poll(0))


if not parent_and_pipe_alive():
    os._exit(41)
if test_mode == "gofail":
    # Close the pipe reader before READY so the owner's real pipe write fails.
    os.close(sys.stdin.fileno())
    print("READY", flush=True)
    time.sleep(0.8)
    os._exit(43)
print("READY", flush=True)
if sys.stdin.readline() != "GO\n" or not parent_and_pipe_alive():
    os._exit(42)
marker = os.open(marker_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
try:
    os.write(marker, b"synthetic work entered\n")
finally:
    os.close(marker)
print("BEGIN", flush=True)
time.sleep(0.8)  # invented, bounded test-only work
print("DONE", flush=True)
