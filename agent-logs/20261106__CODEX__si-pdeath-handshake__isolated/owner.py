"""DISABLED real workload: one fixed child, parent-death test protocol only."""
import ctypes
import json
import os
from pathlib import Path
import platform
import signal
import subprocess
import sys

REAL_MODEL_ENABLED = False
GPU_EXECUTION_ENABLED = False


def pidfd_open(pid):
    if sys.platform != "linux" or platform.machine() != "x86_64" or not hasattr(signal, "pidfd_send_signal"):
        raise RuntimeError("Linux x86_64 pidfd support required")
    libc = ctypes.CDLL(None, use_errno=True)
    fd = libc.syscall(434, pid, 0)  # tested only on Linux x86_64
    if fd < 0:
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error))
    return fd


def emit(value):
    print(json.dumps(value, sort_keys=True), flush=True)


def main():
    ledger_path = sys.argv[1]
    mode = sys.argv[2]
    if mode not in ("normal", "prearm"):
        raise ValueError("fixed test mode required")
    ledger_fd = os.open(ledger_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_APPEND, 0o600)
    child = None
    child_pidfd = None

    def log(operation, state, **detail):
        encoded = (json.dumps({"operation": operation, "state": state, "detail": detail}, sort_keys=True) + "\n").encode()
        while encoded:
            written = os.write(ledger_fd, encoded)
            if written <= 0:
                raise OSError("short ledger write")
            encoded = encoded[written:]
        os.fsync(ledger_fd)

    try:
        log("attempt", "started")
        log("spawn", "started")
        child_path = str(Path(__file__).with_name("child.py"))
        child = subprocess.Popen([sys.executable, "-I", child_path, str(os.getpid()), mode],
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                 text=True, bufsize=1, close_fds=True,
                                 env={"PATH": os.defpath, "CUDA_VISIBLE_DEVICES": ""})
        child_pidfd = pidfd_open(child.pid)
        log("spawn", "returned", child_pid=child.pid)
        emit({"event": "SPAWNED", "child_pid": child.pid})
        if child.stdout.readline() != "READY\n":
            raise RuntimeError("child not ready")
        log("ready", "returned")
        emit({"event": "READY"})
        if sys.stdin.readline() != "GO\n":
            raise RuntimeError("GO not provided")
        log("go", "started")
        child.stdin.write("GO\n")
        child.stdin.flush()
        if child.stdout.readline() != "BEGIN\n":
            raise RuntimeError("child did not begin")
        log("work", "started")
        emit({"event": "BEGIN"})
        if child.stdout.readline() != "DONE\n":
            raise RuntimeError("child work did not return")
        log("work", "returned")
        exit_code = child.wait(timeout=2)
        log("child", "returned", exit_code=exit_code)
        if exit_code != 0:
            raise RuntimeError("child failed")
        log("attempt", "returned")
        emit({"event": "DONE", "child_exit": exit_code})
    except Exception as exc:
        try:
            log("attempt", "unknown", reason=str(exc))
        except Exception:
            pass
        raise
    finally:
        if child is not None and child.poll() is None:
            if child_pidfd is not None:
                try:
                    signal.pidfd_send_signal(child_pidfd, signal.SIGTERM)
                    child.wait(timeout=1)
                except (ProcessLookupError, subprocess.TimeoutExpired):
                    if child.poll() is None:
                        signal.pidfd_send_signal(child_pidfd, signal.SIGKILL)
                        child.wait(timeout=1)
            else:
                # No numeric-PID signal fallback; EOF lets this fixed child exit.
                child.stdin.close()
                try:
                    child.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    pass  # unresolved child; not a production cleanup guarantee
        if child_pidfd is not None:
            os.close(child_pidfd)
        if child is not None:
            child.stdin.close()
            child.stdout.close()
        os.close(ledger_fd)


if __name__ == "__main__":
    main()
