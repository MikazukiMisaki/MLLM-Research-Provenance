"""Only synthetic, in-memory doubles; proves no OS/process/hardware property."""

from dataclasses import asdict, replace
import unittest

from fit_mock import (REAL_EXECUTION_ENABLED, FakeAdapter, FakeLedger, FakeMonitor, FakeWorker,
                      Fixture, MonitorPolicy, Row, Sample, Stop, digest, run_fake)


def setup():
    targets = (True,) * 4 + (False,) * 12
    fixture = Fixture(tuple(Row(i, targets[i], 2048, 100 + i, 1 + 2 * i) for i in range(8)), targets)
    policy = MonitorPolicy("FAKE-DEVICE")
    return fixture, policy, FakeLedger(), FakeMonitor([Sample("FAKE-DEVICE")] * 30), FakeAdapter(), FakeWorker()


def run(parts, run_id="fake-run", input_digest=None, policy_digest=None):
    fixture, policy, ledger, monitor, adapter, worker = parts
    return run_fake(run_id, fixture, input_digest or digest(asdict(fixture)), policy,
                    policy_digest or digest(asdict(policy)), ledger, monitor, adapter, worker)


class MockTests(unittest.TestCase):
    def test_success_order_counts_denominator_and_original(self):
        self.assertIs(REAL_EXECUTION_ENABLED, False)
        parts = setup()
        fixture, _, ledger, _, adapter, worker = parts
        before = adapter.original_digest()
        result = run(parts)
        self.assertEqual(result["status"], "FAKE_COMPLETE")
        self.assertEqual(adapter.original_digest(), before)
        expected_calls = [("zero_grad", None)]
        for i in range(8):
            expected_calls.extend([("forward", i), ("backward", i)])
        expected_calls.extend([("clip", None), ("step", None)])
        self.assertEqual(worker.calls, expected_calls)
        denominator = sum(r.active for r in fixture.rows)
        for row, scale in zip(fixture.rows, worker.scales):
            self.assertAlmostEqual(scale, (16 / 7 if row.target else 4 / 7) * row.active / denominator)
        self.assertEqual(len(worker.scales), 8)
        self.assertTrue(result["started_step"] and result["returned_step"])
        for previous, current in zip(ledger.events, ledger.events[1:]):
            self.assertEqual(current["previous"], previous["hash"])
        for event in ledger.events:
            body = {k: v for k, v in event.items() if k != "hash"}
            self.assertEqual(event["hash"], digest(body))

    def test_duplicate_claim_and_no_automatic_retry(self):
        parts = setup()
        parts[-1].fail_at = ("forward", 3)
        result = run(parts)
        self.assertEqual(result["status"], "INCOMPLETE_UNKNOWN")
        self.assertEqual(parts[-1].calls[-1], ("forward", 3))
        self.assertEqual(parts[2].events[-1]["state"], "unknown")
        previous = list(parts[-1].calls)
        with self.assertRaises(Stop):
            run(parts)
        self.assertEqual(parts[-1].calls, previous)

    def test_bindings_and_input_validation_precede_worker(self):
        for kind in ("input", "policy", "count", "order", "target"):
            with self.subTest(kind=kind):
                parts = list(setup())
                input_digest = "bad" if kind == "input" else None
                policy_digest = "bad" if kind == "policy" else None
                fixture = parts[0]
                if kind in ("count", "order", "target"):
                    changes = {"count": {"active": 0}, "order": {"record": 7}, "target": {"target": False}}
                    parts[0] = replace(fixture, rows=(replace(fixture.rows[0], **changes[kind]),) + fixture.rows[1:])
                result = run(parts, input_digest=input_digest, policy_digest=policy_digest)
                self.assertEqual(result["status"], "INCOMPLETE_UNKNOWN")
                self.assertEqual(parts[-1].calls, [])
                with self.assertRaises(Stop):
                    run(parts)

    def test_resource_failures_stop_owned_fake_work(self):
        samples = [Sample("other"), Sample("FAKE-DEVICE", free_mib=6143),
                   Sample("FAKE-DEVICE", host_gib=3), Sample("FAKE-DEVICE", rss_gib=29),
                   Sample("FAKE-DEVICE", gap_s=21), Sample("FAKE-DEVICE", work_s=601),
                   Sample("FAKE-DEVICE", cgroup="unknown"), Sample("FAKE-DEVICE", observable=False),
                   Sample("FAKE-DEVICE", free_mib=float("nan"))]
        for sample in samples:
            with self.subTest(sample=sample):
                parts = list(setup())
                parts[3] = FakeMonitor([Sample("FAKE-DEVICE"), sample])
                result = run(parts)
                self.assertEqual(result["status"], "INCOMPLETE_UNKNOWN")
                self.assertEqual(parts[-1].calls, [("zero_grad", None)])
                self.assertFalse(result["started_step"])
        parts = list(setup())
        parts[3] = FakeMonitor([])
        self.assertEqual(run(parts)["status"], "INCOMPLETE_UNKNOWN")
        self.assertEqual(parts[-1].calls, [])

    def test_partial_step_is_open_unknown_and_never_retried(self):
        parts = setup()
        parts[-1].fail_at = ("step", None)
        result = run(parts)
        self.assertEqual(result["status"], "INCOMPLETE_UNKNOWN")
        self.assertTrue(result["started_step"])
        self.assertFalse(result["returned_step"])
        self.assertEqual(parts[-1].private_value, 2.0)
        self.assertIn(("step", "started"), [(e["operation"], e["state"]) for e in parts[2].events])
        self.assertNotIn(("step", "returned"), [(e["operation"], e["state"]) for e in parts[2].events])
        self.assertEqual(parts[2].events[-1]["state"], "unknown")
        with self.assertRaises(Stop):
            run(parts)
        self.assertEqual(parts[-1].calls.count(("step", None)), 1)

    def test_failed_persistence_cannot_claim_durable_unknown(self):
        parts = list(setup())
        parts[2] = FakeLedger(fail_from=38)  # step starts, then its return cannot be recorded
        result = run(parts)
        self.assertEqual(result["status"], "INCOMPLETE_UNKNOWN")
        self.assertTrue(result["started_step"])
        self.assertFalse(result["returned_step"])
        self.assertTrue(result["ledger_unavailable"])
        self.assertEqual(parts[2].events[-1]["operation"], "step")
        self.assertEqual(parts[2].events[-1]["state"], "started")

    def test_fake_optimizer_and_numeric_faults_stop(self):
        workers = (FakeWorker(optimizer_isolated=False), FakeWorker(base_grad=True),
                   FakeWorker(nonfinite_at=("forward", 2)), FakeWorker(nonfinite_at=("backward", 3)))
        for worker in workers:
            with self.subTest(worker=worker):
                parts = list(setup())
                parts[-1] = worker
                result = run(parts)
                self.assertEqual(result["status"], "INCOMPLETE_UNKNOWN")
                self.assertNotIn(("step", None), worker.calls)

    def test_original_digest_change_is_not_accepted(self):
        parts = list(setup())
        parts[-2] = FakeAdapter(change_on_check=True)
        result = run(parts)
        self.assertEqual(result["status"], "INCOMPLETE_UNKNOWN")
        self.assertEqual(result["reason"], "fake original adapter changed")
        self.assertTrue(result["started_step"] and result["returned_step"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
