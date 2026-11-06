"""DISABLED for real workloads: fixed synthetic direct-child process exercise."""

import ctypes
import hashlib
import json
import math
import os
import platform
import re
import signal
import subprocess
import sys

REAL_MODEL_ENABLED = False
GPU_EXECUTION_ENABLED = False

_CHILD = r'''import os, sys, time
mode = sys.argv[1]
if mode == "success":
    sys.exit(0)
if mode == "crash":
    os._exit(17)
if mode == "hang":
    time.sleep(2)
    sys.exit(0)
os._exit(19)
'''


class Stop(Exception):
    pass


def _sync_dir(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _write_all(fd, data):
    while data:
        written = os.write(fd, data)
        if written <= 0:
            raise OSError("zero-length ledger write")
        data = data[written:]


def _encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def _pidfd_open(pid):
    # This interpreter lacks os.pidfd_open; use Linux syscall only on reviewed ABIs.
    if sys.platform != "linux" or platform.machine() not in ("x86_64", "aarch64"):
        raise Stop("unsupported pidfd platform")
    if not hasattr(signal, "pidfd_send_signal"):
        raise Stop("pidfd signal support unavailable")
    libc = ctypes.CDLL(None, use_errno=True)
    fd = libc.syscall(434, pid, 0)
    if fd < 0:
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error))
    return fd


class Ledger:
    """Exclusive, append-only file with one fsync per event; not external custody."""
    def __init__(self, path):
        self.fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_APPEND | os.O_NOFOLLOW, 0o600)
        self.previous = "0" * 64
        self.healthy = True
        try:
            os.fsync(self.fd)
            _sync_dir(os.path.dirname(path))
        except BaseException:
            os.close(self.fd)
            raise

    def append(self, operation, state, **detail):
        if not self.healthy:
            raise Stop("ledger unavailable")
        event = {"operation": operation, "state": state, "detail": detail, "previous": self.previous}
        event_hash = hashlib.sha256(_encode(event)).hexdigest()
        try:
            _write_all(self.fd, _encode({**event, "hash": event_hash}) + b"\n")
            os.fsync(self.fd)
        except BaseException:
            self.healthy = False
            raise
        self.previous = event_hash

    def close(self):
        os.close(self.fd)


def _claim(directory, run_id):
    path = os.path.join(directory, run_id + ".claim")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        _write_all(fd, _encode({"run_id": run_id}) + b"\n")
        os.fsync(fd)
    finally:
        os.close(fd)
    _sync_dir(directory)


def _cleanup_child(worker, pidfd):
    """Only the direct child; never signal a numeric PID or an unrelated process."""
    if worker.poll() is not None:
        return "reaped"
    if pidfd is None:
        # Fixed synthetic child has a finite sleep; no unsafe numeric-PID signal.
        try:
            worker.wait(timeout=2.5)
            return "reaped_without_pidfd"
        except subprocess.TimeoutExpired:
            return "unobserved_no_pidfd"
    try:
        signal.pidfd_send_signal(pidfd, signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        worker.wait(timeout=0.5)
        return "reaped"
    except subprocess.TimeoutExpired:
        pass
    try:
        signal.pidfd_send_signal(pidfd, signal.SIGKILL)
    except ProcessLookupError:
        pass
    try:
        worker.wait(timeout=0.5)
        return "reaped"
    except subprocess.TimeoutExpired:
        return "unobserved_after_signals"


def run_synthetic(run_id, claim_dir, ledger_dir, mode, timeout_s):
    """Run exactly one fixed synthetic program, returning only local observations."""
    if (type(run_id) is not str or re.fullmatch(r"[A-Za-z0-9_-]{1,80}", run_id) is None or
        mode not in ("success", "crash", "hang") or
        type(timeout_s) not in (float, int) or not math.isfinite(timeout_s) or not 0 < timeout_s <= 2):
        raise Stop("invalid synthetic request")
    if os.path.samefile(claim_dir, ledger_dir):
        raise Stop("claim and ledger directories must differ")
    # Fail before claiming if even self pidfd access is unavailable.
    probe = _pidfd_open(os.getpid())
    os.close(probe)
    _claim(claim_dir, run_id)
    ledger = Ledger(os.path.join(ledger_dir, run_id + ".jsonl"))
    worker = None
    pidfd = None
    result = {"status": "INCOMPLETE_UNKNOWN", "pid": None, "cleanup": "not_started"}
    failed = None
    try:
        ledger.append("attempt", "started", run_id=run_id, mode=mode)
        ledger.append("spawn", "started")
        worker = subprocess.Popen([sys.executable, "-I", "-c", _CHILD, mode],
                                  stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                  close_fds=True, env={"PATH": os.defpath, "CUDA_VISIBLE_DEVICES": ""})
        result["pid"] = worker.pid
        pidfd = _pidfd_open(worker.pid)
        ledger.append("spawn", "returned", pid=worker.pid)
        ledger.append("worker", "started", pid=worker.pid)
        try:
            exit_code = worker.wait(timeout=timeout_s)
        except subprocess.TimeoutExpired as exc:
            raise Stop("synthetic worker timeout") from exc
        ledger.append("worker", "returned", exit_code=exit_code)
        if exit_code != 0:
            raise Stop("synthetic worker failed")
        result["cleanup"] = "reaped"
        ledger.append("cleanup", "returned", outcome="reaped", exit_code=worker.returncode)
        ledger.append("attempt", "returned")
        result["status"] = "SYNTHETIC_COMPLETE"
    except Exception as exc:
        failed = exc
        result["reason"] = str(exc)
    finally:
        if worker is not None and result["cleanup"] != "reaped":
            try:
                result["cleanup"] = _cleanup_child(worker, pidfd)
            except Exception:
                result["cleanup"] = "unknown_cleanup_error"
        if pidfd is not None:
            os.close(pidfd)
        if worker is not None:
            result["exit_code"] = worker.returncode
        if failed is not None:
            try:
                ledger.append("cleanup", "returned" if result["cleanup"].startswith("reaped") else "unknown",
                              outcome=result["cleanup"], exit_code=worker.returncode if worker is not None else None)
                ledger.append("attempt", "unknown", reason=str(failed))
            except Exception:
                result["ledger_unavailable"] = True
        ledger.close()
    return result
