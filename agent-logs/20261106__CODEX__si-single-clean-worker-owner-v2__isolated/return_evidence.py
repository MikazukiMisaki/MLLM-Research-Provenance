"""Bounded local evidence of a returned synthetic/engine object, not validation."""
import json
import math
import itertools
import hashlib
import os

FIELDS = ("feedback", "won", "_facts", "_valid_commands", "_valid_actions", "admissible_commands", "_last_action")
MAX_STRING = 2048
MAX_ITEMS = 128
MAX_DEPTH = 8
MAX_BYTES = 32768
MISSING = object()


class Capture:
    def __init__(self):
        self.incomplete = False
        self.active = set()
        self.nodes = 0

    def marker(self, reason, **details):
        self.incomplete = True
        return {"marker": reason, **details}

    def value(self, obj, depth=0):
        self.nodes += 1
        if self.nodes > 512:
            return self.marker("NODE_LIMIT")
        if obj is MISSING:
            return {"marker": "MISSING"}
        if obj is None or type(obj) in (bool, int):
            if type(obj) is int and obj.bit_length() > 256:
                return self.marker("INTEGER_TOO_LARGE", bits=obj.bit_length())
            return obj
        if type(obj) is float:
            if not math.isfinite(obj):
                return {"marker": "NONFINITE_FLOAT", "value": "nan" if math.isnan(obj) else ("+inf" if obj > 0 else "-inf")}
            return obj
        if type(obj) is str:
            if len(obj) > MAX_STRING:
                return self.marker("STRING_TRUNCATED", prefix=obj[:MAX_STRING], original_length=len(obj))
            return obj
        if depth >= MAX_DEPTH:
            return self.marker("DEPTH_LIMIT")
        identity = id(obj)
        if identity in self.active:
            return self.marker("CYCLE")
        self.active.add(identity)
        try:
            if isinstance(obj, (tuple, list)):
                result = [self.value(item, depth + 1) for item in obj[:MAX_ITEMS]]
                if len(obj) > MAX_ITEMS:
                    result.append(self.marker("ITEMS_TRUNCATED", original_length=len(obj)))
                return result
            if isinstance(obj, dict):
                entries = list(itertools.islice(obj.items(), MAX_ITEMS + 1))
                result = [[self.value(key, depth + 1), self.value(value, depth + 1)] for key, value in entries[:MAX_ITEMS]]
                if len(entries) > MAX_ITEMS:
                    result.append(self.marker("ITEMS_TRUNCATED", original_length_at_least=len(entries)))
                return {"kind": "mapping", "entries": result}
            attrs = {}
            for key in ("name", "arguments", "mapping"):
                try:
                    value = getattr(obj, key, MISSING)
                except Exception as exc:
                    attrs[key] = self.marker("ATTRIBUTE_UNAVAILABLE", exception_type=type(exc).__name__)
                    continue
                if value is not MISSING:
                    attrs[key] = self.value(value, depth + 1)
            if not attrs:
                return self.marker("OBJECT_UNSERIALIZABLE", type=type(obj).__name__)
            return {"kind": "object", "type": type(obj).__name__, "attributes": attrs}
        except Exception as exc:
            return self.marker("VALUE_UNAVAILABLE", exception_type=type(exc).__name__)
        finally:
            self.active.remove(identity)


def returned(operation, result, selected=None):
    """Capture selected raw fields before semantic validation; never use repr."""
    capture = Capture()
    out = {"scope": "SELECTED_FIELDS_ONLY", "operation_returned": True, "operation": operation}
    try:
        if operation == "step":
            if not isinstance(result, tuple) or len(result) != 3:
                out["result"] = capture.marker("STEP_SHAPE_UNAVAILABLE", type=type(result).__name__)
                state = None
            else:
                state, score, done = result
                out["score"] = capture.value(score)
                out["done"] = capture.value(done)
        else:
            state = result
        if state is None or not callable(getattr(state, "get", None)):
            out["state"] = capture.marker("STATE_UNAVAILABLE", type=type(state).__name__)
        else:
            fields = {}
            for key in FIELDS:
                try:
                    fields[key] = capture.value(state.get(key, MISSING))
                except Exception as exc:
                    fields[key] = capture.marker("FIELD_UNAVAILABLE", exception_type=type(exc).__name__)
            out["fields"] = fields
            if operation == "step":
                try:
                    out["selected_identity"] = state.get("_last_action", MISSING) is selected
                except Exception as exc:
                    out["selected_identity"] = capture.marker("IDENTITY_UNAVAILABLE", exception_type=type(exc).__name__)
    except Exception as exc:
        out["capture_failure"] = capture.marker("CAPTURE_UNAVAILABLE", exception_type=type(exc).__name__)
    out["status"] = "PARTIAL_UNKNOWN" if capture.incomplete else "COMPLETE_SELECTED_FIELDS"
    try:
        size = len(json.dumps(out, sort_keys=True, separators=(",", ":"), allow_nan=False).encode())
    except Exception as exc:
        return {"scope": "SELECTED_FIELDS_ONLY", "operation_returned": True, "operation": operation,
                "status": "PARTIAL_UNKNOWN", "capture_failure": {"marker": "ENCODING_UNAVAILABLE", "exception_type": type(exc).__name__}}
    if size > MAX_BYTES:
        return {"scope": "SELECTED_FIELDS_ONLY", "operation_returned": True, "operation": operation,
                "status": "PARTIAL_UNKNOWN", "capture_failure": {"marker": "SERIALIZED_SIZE_LIMIT", "observed_bytes": size}}
    return out


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


class FakeRawJournal:
    def __init__(self, fail=False):
        self.entries = []
        self.fail = fail

    def append(self, op, index, evidence):
        if self.fail:
            raise OSError("fake_raw_journal_failure")
        self.entries.append({"op": op, "index": index, "evidence": evidence})


class WorkerRawJournal:
    """Exclusive local evidence; failed or partial writes are UNKNOWN."""
    def __init__(self, dir_fd):
        self.fd = os.open("worker_raw.jsonl", os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_APPEND | os.O_CLOEXEC, 0o600, dir_fd=dir_fd)
        self.previous = "0" * 64
        self.healthy = True
        try:
            os.fsync(self.fd)
            os.fsync(dir_fd)
        except BaseException:
            os.close(self.fd)
            raise

    def append(self, op, index, evidence):
        if not self.healthy:
            raise RuntimeError("raw_journal_unavailable")
        body = {"op": op, "index": index, "evidence": evidence, "previous": self.previous}
        digest = hashlib.sha256(encode(body)).hexdigest()
        data = encode({**body, "hash": digest}) + b"\n"
        try:
            while data:
                n = os.write(self.fd, data)
                if n <= 0:
                    raise OSError("zero_write")
                data = data[n:]
            os.fsync(self.fd)
        except BaseException:
            self.healthy = False
            raise
        self.previous = digest

    def close(self):
        os.close(self.fd)
