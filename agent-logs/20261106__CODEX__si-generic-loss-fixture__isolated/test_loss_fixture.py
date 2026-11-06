"""Synthetic CPU-only checks. No real dataset, model, or environment."""

import math
import unittest

import torch
import torch.nn.functional as F

from loss_fixture import Example, dataset_weights, window_terms

torch.set_num_threads(1)
DTYPE = torch.float64


def invented_examples():
    generator = torch.Generator(device="cpu").manual_seed(726)
    labels = [
        [-100, 0, 2, 1, -100],
        [-100, -100, 1, -100, -100],
        [-100, 3, 2, -100, -100],
        [-100, 1, 0, 3, 2],
        [-100, -100, 0, 1, -100],
    ]
    return [Example(torch.randn((5, 4), generator=generator, dtype=DTYPE, requires_grad=True),
                    torch.tensor(y, dtype=torch.long), i) for i, y in enumerate(labels)]


def reference(window, targets, arm):
    # Direct independent per-token negative log likelihood, no native mean scaling.
    m, k = len(targets), sum(targets)
    alpha = m / (m + 3 * k)
    numerator = 0
    n = 0
    for row in window:
        for position, label in enumerate(row.labels[1:]):
            if label.item() != -100:
                weight = 1.0 if arm == "C1" else alpha * (4 if targets[row.record_index] else 1)
                numerator = numerator - weight * torch.log_softmax(row.logits[position], dim=-1)[label]
                n += 1
    return numerator / n


class TestFixture(unittest.TestCase):
    def test_hand_computed_shift_mask_and_partial_window(self):
        targets = [True, False, False]
        for arm in ("C1", "C4"):
            theta = torch.tensor(0.0, dtype=DTYPE, requires_grad=True)
            def logits(values):
                base = torch.tensor(values, dtype=DTYPE)
                return base + theta * torch.tensor([1.0, 0.0], dtype=DTYPE)
            t = Example(logits([[0, 0], [0, 0], [8, -8]]), torch.tensor([-100, 1, 0]), 0)
            n1 = Example(logits([[0, 0], [9, -9], [7, -7]]), torch.tensor([-100, 1, -100]), 1)
            n2 = Example(logits([[math.log(3), 0], [6, -6]]), torch.tensor([-100, 0]), 2)
            mixed = sum(window_terms([t, n1], targets, arm))
            partial = sum(window_terms([n2], targets, arm))
            factor = 1.0 if arm == "C1" else 1.5
            self.assertAlmostEqual(mixed.item(), factor * math.log(2), places=12)
            self.assertAlmostEqual(partial.item(), (1.0 if arm == "C1" else 0.5) * math.log(4 / 3), places=12)
            theta_grad, t_grad, n1_grad = torch.autograd.grad(mixed, (theta, t.logits, n1.logits))
            self.assertAlmostEqual(theta_grad.item(), 1 / 6 if arm == "C1" else 1 / 12, places=12)
            self.assertEqual(t_grad[-1].tolist(), [0.0, 0.0])
            self.assertEqual(n1_grad[1:].tolist(), [[0.0, 0.0], [0.0, 0.0]])
            theta_grad, n2_grad = torch.autograd.grad(partial, (theta, n2.logits))
            self.assertAlmostEqual(theta_grad.item(), -1 / 4 if arm == "C1" else -1 / 8, places=12)
            self.assertEqual(n2_grad[-1].tolist(), [0.0, 0.0])

    def test_weights_general(self):
        for m, k in [(2, 1), (5, 2), (11, 7)]:
            targets = [True] * k + [False] * (m - k)
            alpha = m / (m + 3 * k)
            weights = dataset_weights(targets, "C4")
            self.assertAlmostEqual(sum(weights) / m, 1.0)
            for target, weight in zip(targets, weights):
                self.assertAlmostEqual(weight, alpha * (4 if target else 1))
            self.assertEqual(dataset_weights(targets, "C1"), (1.0,) * m)

    def test_uninformative_contrast_fails_closed(self):
        for targets in ([False], [True], [False, False, False], [True, True, True]):
            for arm in ("C1", "C4"):
                with self.subTest(targets=targets, arm=arm):
                    with self.assertRaisesRegex(ValueError, "no informative target weighting contrast"):
                        dataset_weights(targets, arm)
                    with self.assertRaisesRegex(ValueError, "no informative target weighting contrast"):
                        window_terms([invented_examples()[0]], targets, arm)

    def test_c1_native_and_c4_direct_losses_and_gradients(self):
        targets = [True, False, True, False, False]
        # Unequal lengths, target-only and non-target-only windows, mixed windows,
        # repeated occurrence, and a short final window.
        for indices in ([0, 2], [1, 3], [0, 1, 3], [0, 0, 1], [4]):
            for arm in ("C1", "C4"):
                rows = invented_examples()
                window = [rows[i] for i in indices]
                terms = window_terms(window, targets, arm)
                got = sum(terms)
                expected = reference(window, targets, arm)
                torch.testing.assert_close(got, expected, rtol=1e-12, atol=1e-12)
                if arm == "C1":
                    native = F.cross_entropy(torch.cat([r.logits[:-1] for r in window]),
                                             torch.cat([r.labels[1:] for r in window]),
                                             ignore_index=-100, reduction="mean")
                    torch.testing.assert_close(got, native, rtol=1e-12, atol=1e-12)
                    expected = native
                got_grads = torch.autograd.grad(got, [r.logits for r in rows], retain_graph=True, allow_unused=True)
                expected_grads = torch.autograd.grad(expected, [r.logits for r in rows], allow_unused=True)
                for a, b in zip(got_grads, expected_grads):
                    if a is None or b is None:
                        self.assertIs(a, b)
                    else:
                        torch.testing.assert_close(a, b, rtol=1e-12, atol=1e-12)

    def test_sequential_backwards_and_partial_window(self):
        targets = [True, False, True, False, False]
        left, right = invented_examples(), invented_examples()
        # Two updates; second has one occurrence. One clip and step per window.
        opt_a = torch.optim.SGD([r.logits for r in left], lr=0.03, momentum=0.9)
        opt_b = torch.optim.SGD([r.logits for r in right], lr=0.03, momentum=0.9)
        for indices in ([0, 1, 2, 3], [4]):
            opt_a.zero_grad(set_to_none=True)
            opt_b.zero_grad(set_to_none=True)
            window_a, window_b = [left[i] for i in indices], [right[i] for i in indices]
            for term in window_terms(window_a, targets, "C1"):
                term.backward()
            F.cross_entropy(torch.cat([r.logits[:-1] for r in window_b]),
                            torch.cat([r.labels[1:] for r in window_b]),
                            ignore_index=-100).backward()
            for a, b in zip(left, right):
                if a.logits.grad is None or b.logits.grad is None:
                    self.assertIs(a.logits.grad, b.logits.grad)
                else:
                    torch.testing.assert_close(a.logits.grad, b.logits.grad, rtol=1e-12, atol=1e-12)
            torch.nn.utils.clip_grad_norm_([r.logits for r in left], 0.3)
            torch.nn.utils.clip_grad_norm_([r.logits for r in right], 0.3)
            opt_a.step()
            opt_b.step()
            for a, b in zip(left, right):
                torch.testing.assert_close(a.logits, b.logits, rtol=1e-12, atol=1e-12)
                self.assertEqual(bool(opt_a.state[a.logits]), bool(opt_b.state[b.logits]))
                if opt_a.state[a.logits]:
                    torch.testing.assert_close(opt_a.state[a.logits]["momentum_buffer"],
                                               opt_b.state[b.logits]["momentum_buffer"], rtol=1e-12, atol=1e-12)

    def test_invalid_inputs_fail_before_any_backward(self):
        rows = invented_examples()
        targets = [True, False, True, False, False]
        x = rows[0].logits
        bad_rows = [
            Example(x, torch.tensor([-100, -100, -100, -100, -100]), 0),
            Example(x, torch.tensor([-100, 4, 0, 0, 0]), 0),
            Example(x, torch.tensor([4, 0, 0, 0, 0]), 0),
            Example(x, torch.tensor([-100, -1, 0, 0, 0]), 0),
            Example(x, torch.tensor([-100, 0, 0, 0]), 0),
            Example(x, torch.tensor([-100, 0, 0, 0, 0], dtype=torch.int32), 0),
            Example(x, torch.tensor([-100, 0, 0, 0, 0]), 5),
            Example(x.detach(), torch.tensor([-100, 0, 0, 0, 0]), 0),
            Example(torch.full((5, 4), float("nan"), requires_grad=True), torch.tensor([-100, 0, 0, 0, 0]), 0),
        ]
        for row in bad_rows:
            with self.subTest(row=row), self.assertRaises(ValueError):
                window_terms([rows[0], row], targets, "C4")
            self.assertIsNone(rows[0].logits.grad)
        for bad_targets, arm in [([], "C1"), ([1, False], "C4"), (targets, "other")]:
            with self.assertRaises(ValueError):
                dataset_weights(bad_targets, arm)
        with self.assertRaises(ValueError):
            window_terms([], targets, "C1")
        with self.assertRaises(TypeError):
            window_terms([rows[0]], targets, "C1", denominator=1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
