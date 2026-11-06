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
    if mode not in ("normal", "prearm", "gofail", "fail_work_sync", "pause_after_started", "blocked_mask"):
        raise ValueError("fixed test mode required")
    ledger_fd = os.open(ledger_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_APPEND, 0o600)
    child = None
    child_pidfd = None
    child_in = None

    def log(operation, state, **detail):
        encoded = (json.dumps({"operation": operation, "state": state, "detail": detail}, sort_keys=True) + "\n").encode()
        while encoded:
            written = os.write(ledger_fd, encoded)
            if written <= 0:
                raise OSError("short ledger write")
            encoded = encoded[written:]
        if mode == "fail_work_sync" and (operation, state) == ("work", "started"):
            raise OSError("injected work-start fsync failure")
        os.fsync(ledger_fd)

    try:
        log("attempt", "started")
        log("spawn", "started")
        child_path = str(Path(__file__).with_name("child.py"))
        marker_path = str(Path(ledger_path).with_name("child_work_started"))
        # Test-only supplied pipe permits the harness to keep an extra writer.
        child_stdin = int(sys.argv[3]) if mode == "blocked_mask" else subprocess.PIPE
        child = subprocess.Popen([sys.executable, "-I", child_path, str(os.getpid()), mode, marker_path],
                                 stdin=child_stdin, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                 text=True, bufsize=1, close_fds=True,
                                 env={"PATH": os.defpath, "CUDA_VISIBLE_DEVICES": ""})
        if mode == "blocked_mask":
            os.close(child_stdin)
            child_in = os.fdopen(int(sys.argv[4]), "w", buffering=1)
        else:
            child_in = child.stdin
        child_pidfd = pidfd_open(child.pid)
        log("spawn", "returned", child_pid=child.pid)
        emit({"event": "SPAWNED", "child_pid": child.pid})
        ready = child.stdout.readline()
        if ready == "TERM_BLOCKED\n":
            log("ready", "rejected", reason="SIGTERM blocked")
            raise RuntimeError("child inherited blocked SIGTERM")
        if ready != "READY\n":
            raise RuntimeError("child not ready")
        log("ready", "returned")
        emit({"event": "READY"})
        if sys.stdin.readline() != "GO\n":
            raise RuntimeError("GO not provided")
        # Persist liability before any GO can permit the child to work.
        log("work", "started")
        emit({"event": "ARMED"})
        if mode == "pause_after_started" and sys.stdin.readline() != "RELEASE\n":
            raise RuntimeError("release not provided")
        log("go", "started")
        child_in.write("GO\n")
        child_in.flush()
        if child.stdout.readline() != "BEGIN\n":
            raise RuntimeError("child did not begin")
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
                if child_in is not None:
                    child_in.close()
                try:
                    child.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    pass  # unresolved child; not a production cleanup guarantee
        if child_pidfd is not None:
            os.close(child_pidfd)
        if child is not None:
            try:
                if child_in is not None:
                    child_in.close()
            except OSError:
                pass
            child.stdout.close()
        os.close(ledger_fd)


if __name__ == "__main__":
    main()
