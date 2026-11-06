"""DISABLED: in-memory fake-only state machine, not a process supervisor."""

from dataclasses import asdict, dataclass
import hashlib
import json
import math

REAL_EXECUTION_ENABLED = False


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


@dataclass(frozen=True)
class Row:
    record: int
    target: bool
    sequence: int
    nonpadding: int
    active: int


@dataclass(frozen=True)
class Fixture:
    rows: tuple
    # Invented universe; these are not real dataset statistics.
    universe_targets: tuple


@dataclass(frozen=True)
class MonitorPolicy:
    device_id: str
    min_free_mib: int = 6144
    min_host_gib: int = 4
    max_rss_gib: int = 28
    max_gap_s: int = 20
    max_work_s: int = 600


@dataclass(frozen=True)
class Sample:
    device_id: str
    free_mib: int = 50000
    host_gib: int = 64
    rss_gib: int = 1
    gap_s: int = 1
    work_s: int = 1
    cgroup: str = "mock_safe"
    observable: bool = True


class Stop(Exception):
    pass


class FakeLedger:
    """In-memory only: neither durable, atomic nor independently owned."""
    def __init__(self, fail_from=None, fail_exception=Stop):
        self.claims = set()
        self.events = []
        self.fail_from = fail_from
        self.fail_exception = fail_exception

    def claim(self, run_id):
        if type(run_id) is not str or not run_id or run_id in self.claims:
            raise Stop("invalid or consumed fake claim")
        self.claims.add(run_id)

    def append(self, run_id, operation, state, **detail):
        if self.fail_from is not None and len(self.events) >= self.fail_from:
            raise self.fail_exception("fake ledger unavailable")
        event = {"run_id": run_id, "operation": operation, "state": state,
                 "detail": detail, "previous": self.events[-1]["hash"] if self.events else "0" * 64}
        event["hash"] = digest(event)
        self.events.append(event)


class FakeMonitor:
    def __init__(self, samples):
        self.samples = list(samples)
        self.index = 0

    def check(self, policy):
        if self.index >= len(self.samples):
            raise Stop("mock monitoring unavailable")
        sample = self.samples[self.index]
        self.index += 1
        if type(sample) is not Sample:
            raise Stop("invalid mock sample")
        values = (sample.free_mib, sample.host_gib, sample.rss_gib, sample.gap_s, sample.work_s)
        if any(type(x) not in (int, float) or not math.isfinite(x) or x < 0 for x in values):
            raise Stop("invalid mock metrics")
        if (sample.observable is not True or sample.device_id != policy.device_id or sample.cgroup != "mock_safe"
            or sample.free_mib < policy.min_free_mib or sample.host_gib < policy.min_host_gib
            or sample.rss_gib > policy.max_rss_gib or sample.gap_s > policy.max_gap_s
            or sample.work_s > policy.max_work_s):
            raise Stop("mock monitoring stop")


class FakeAdapter:
    def __init__(self, change_on_check=False):
        self.original_marker = "original synthetic adapter"
        self.change_on_check = change_on_check
        self.checks = 0

    def original_digest(self):
        self.checks += 1
        if self.change_on_check and self.checks > 1:
            self.original_marker = "changed synthetic adapter"
        return digest(self.original_marker)


class FakeWorker:
    """Only scalar arithmetic and synthetic operation counters; no training library."""
    def __init__(self, fail_at=None, nonfinite_at=None, optimizer_isolated=True, base_grad=False, fail_exception=Stop):
        self.fail_at = fail_at
        self.fail_exception = fail_exception
        self.nonfinite_at = nonfinite_at
        self.optimizer_isolated = optimizer_isolated
        self.base_grad = base_grad
        self.calls = []
        self.scales = []
        self.private_value = 1.0

    def call(self, op, index=None, scale=None):
        self.calls.append((op, index))
        if (op, index) == self.fail_at:
            if op == "step":
                self.private_value += 1.0  # potential partial mutation
            raise self.fail_exception("injected mock worker failure")
        if op == "backward":
            self.scales.append(scale)
        if op == "step":
            self.private_value += 1.0
        return float("nan") if (op, index) == self.nonfinite_at else 1.0


def validate_fixture(fixture):
    if type(fixture) is not Fixture or len(fixture.universe_targets) != 16:
        raise Stop("invalid fake fixture")
    if any(type(x) is not bool for x in fixture.universe_targets) or sum(fixture.universe_targets) != 4:
        raise Stop("invalid fake universe")
    if len(fixture.rows) != 8:
        raise Stop("invalid fake window size")
    for index, row in enumerate(fixture.rows):
        if type(row) is not Row or row.record != index or type(row.record) is not int:
            raise Stop("invalid fake row order")
        if type(row.target) is not bool or row.target != fixture.universe_targets[index]:
            raise Stop("fake target mismatch")
        if any(type(x) is not int for x in (row.sequence, row.nonpadding, row.active)):
            raise Stop("invalid fake counts")
        if row.sequence != 2048 or not 1 <= row.nonpadding <= row.sequence or not 1 <= row.active < row.nonpadding:
            raise Stop("invalid fake counts")
    if sum(row.target for row in fixture.rows) != 4:
        raise Stop("fake window is not mixed 4/4")


def run_fake(run_id, fixture, expected_input_digest, policy, expected_policy_digest, ledger, monitor, adapter, worker):
    """Single fake attempt; returns in-memory observation, never a release decision."""
    if any(type(obj) is not required for obj, required in ((ledger, FakeLedger), (monitor, FakeMonitor),
                                                           (adapter, FakeAdapter), (worker, FakeWorker),
                                                           (policy, MonitorPolicy))):
        raise Stop("only exact fake types permitted")
    ledger.claim(run_id)  # one attempt, including preflight failures
    result = {"status": "INCOMPLETE_UNKNOWN", "started_step": False, "returned_step": False}
    try:
        ledger.append(run_id, "attempt", "started")
        validate_fixture(fixture)
        if digest(asdict(fixture)) != expected_input_digest or digest(asdict(policy)) != expected_policy_digest:
            raise Stop("fake input or monitor binding mismatch")
        if (type(policy.device_id) is not str or not policy.device_id or
            (policy.min_free_mib, policy.min_host_gib, policy.max_rss_gib, policy.max_gap_s, policy.max_work_s)
            != (6144, 4, 28, 20, 600)):
            raise Stop("invalid fake monitoring policy")
        original = adapter.original_digest()
        if worker.optimizer_isolated is not True or worker.base_grad is not False:
            raise Stop("fake optimizer isolation failure")
        denominator = sum(row.active for row in fixture.rows)
        alpha = 16 / (16 + 3 * 4)

        def operation(op, index=None, scale=None):
            monitor.check(policy)
            ledger.append(run_id, op, "started", index=index)
            if op == "step":
                result["started_step"] = True
            observed = worker.call(op, index, scale)
            if type(observed) not in (int, float) or not math.isfinite(observed):
                raise Stop("nonfinite fake operation output")
            ledger.append(run_id, op, "returned", index=index)
            if op == "step":
                result["returned_step"] = True
            return observed

        operation("zero_grad")
        for index, row in enumerate(fixture.rows):
            operation("forward", index)
            weight = alpha * (4 if row.target else 1)
            operation("backward", index, weight * row.active / denominator)
        operation("clip")
        operation("step")
        if adapter.original_digest() != original:
            raise Stop("fake original adapter changed")
        ledger.append(run_id, "attempt", "returned")
        result["status"] = "FAKE_COMPLETE"
    except Exception as exc:
        result["reason"] = str(exc)
        try:
            ledger.append(run_id, "attempt", "unknown", reason=str(exc))
        except Exception:
            result["ledger_unavailable"] = True
    return result
