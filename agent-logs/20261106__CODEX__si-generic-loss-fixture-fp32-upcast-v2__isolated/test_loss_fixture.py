"""Invented tensors only: compare against an independent float32 CE reference."""

import math
import unittest

import torch
import torch.nn.functional as F
from transformers.loss.loss_utils import ForCausalLMLoss

from loss_fixture import Example, dataset_weights, window_terms

torch.set_num_threads(1)
DTYPES = (torch.bfloat16, torch.float16, torch.float32)
TARGETS = (True, False, True, False, False)


def invented(dtype):
    generator = torch.Generator(device="cpu").manual_seed(12345)
    labels = [[-100, 0, 2, 1, -100], [-100, -100, 1, -100, -100],
              [-100, 3, 2, -100, -100], [-100, 1, 0, 3, 2],
              [-100, -100, 0, 1, -100]]
    return [Example(torch.randn((5, 4), generator=generator, device="cpu").to(dtype).requires_grad_(),
                    torch.tensor(y, dtype=torch.long, device="cpu"), i)
            for i, y in enumerate(labels)]


def reference(rows, arm):
    # One flattened torch-native per-token CE after explicit float32 conversion.
    shifted_logits = torch.cat([row.logits[:-1].float() for row in rows])
    shifted_labels = torch.cat([row.labels[1:] for row in rows])
    token_losses = F.cross_entropy(shifted_logits, shifted_labels, ignore_index=-100, reduction="none")
    alpha = len(TARGETS) / (len(TARGETS) + 3 * sum(TARGETS))
    token_weights = torch.cat([torch.full((row.labels.numel() - 1,),
                                  1.0 if arm == "C1" else alpha * (4 if TARGETS[row.record_index] else 1),
                                  dtype=torch.float32) for row in rows])
    return (token_losses * token_weights).sum() / (shifted_labels != -100).sum()


class Float32UpcastTests(unittest.TestCase):
    def test_c1_against_transformers_causal_lm_loss(self):
        for dtype in DTYPES:
            for indices in ((0, 1, 2, 3), (4,)):
                with self.subTest(dtype=dtype, indices=indices):
                    actual_rows, native_rows = invented(dtype), invented(dtype)
                    terms = window_terms([actual_rows[i] for i in indices], TARGETS, "C1")
                    native = ForCausalLMLoss(
                        logits=torch.stack([native_rows[i].logits for i in indices]),
                        labels=torch.stack([native_rows[i].labels for i in indices]),
                        vocab_size=4, num_items_in_batch=None, ignore_index=-100, shift_labels=None)
                    self.assertEqual(native.dtype, torch.float32)
                    torch.testing.assert_close(sum(terms), native, rtol=2e-6, atol=2e-6)
                    for term in terms:
                        term.backward()
                    native.backward()
                    tol = {torch.bfloat16: 1e-2, torch.float16: 2e-3, torch.float32: 3e-6}[dtype]
                    for actual, expected in zip(actual_rows, native_rows):
                        if actual.logits.grad is None or expected.logits.grad is None:
                            self.assertIs(actual.logits.grad, expected.logits.grad)
                        else:
                            torch.testing.assert_close(actual.logits.grad.float(), expected.logits.grad.float(), rtol=tol, atol=tol * 0.01)

    def test_losses_and_gradients_float32_reference(self):
        # Full mixed, homogeneous, repeated exposure, and shorter final window.
        for dtype in DTYPES:
            for arm in ("C1", "C4"):
                for indices in ((0, 1, 2, 3), (0, 2), (1, 3), (0, 0, 1), (4,)):
                    with self.subTest(dtype=dtype, arm=arm, indices=indices):
                        candidate_rows, reference_rows = invented(dtype), invented(dtype)
                        candidate_window = [candidate_rows[i] for i in indices]
                        reference_window = [reference_rows[i] for i in indices]
                        terms = window_terms(candidate_window, TARGETS, arm)
                        candidate = sum(terms)
                        expected = reference(reference_window, arm)
                        self.assertEqual(candidate.dtype, torch.float32)
                        torch.testing.assert_close(candidate, expected, rtol=2e-6, atol=2e-6)
                        # Compare independent leaf gradients after individual backwards.
                        for term in terms:
                            term.backward()
                        expected.backward()
                        for actual, wanted in zip(candidate_rows, reference_rows):
                            if actual.logits.grad is None or wanted.logits.grad is None:
                                self.assertIs(actual.logits.grad, wanted.logits.grad)
                            else:
                                # BF16/FP16 backward casts and addition can round differently.
                                tol = {torch.bfloat16: 1e-2, torch.float16: 2e-3, torch.float32: 3e-6}[dtype]
                                torch.testing.assert_close(actual.logits.grad.float(), wanted.logits.grad.float(), rtol=tol, atol=tol * 0.01)
                                self.assertEqual(actual.logits.grad[-1].tolist(), [0.0] * 4)
                                for pos, label in enumerate(actual.labels[1:]):
                                    if label.item() == -100:
                                        self.assertEqual(actual.logits.grad[pos].tolist(), [0.0] * 4)

    def test_hand_computed_shift_and_mask(self):
        # M=3, K=1; active tokens are [1,0] and [1], all logits [0,0].
        for dtype in DTYPES:
            for arm in ("C1", "C4"):
                with self.subTest(dtype=dtype, arm=arm):
                    target = Example(torch.tensor([[0, 0], [0, 0], [8, -8]], dtype=dtype, requires_grad=True),
                                     torch.tensor([-100, 1, 0]), 0)
                    other = Example(torch.tensor([[0, 0], [8, -8], [7, -7]], dtype=dtype, requires_grad=True),
                                    torch.tensor([-100, 1, -100]), 1)
                    loss = sum(window_terms([target, other], (True, False, False), arm))
                    self.assertAlmostEqual(loss.item(), math.log(2) * (1 if arm == "C1" else 1.5), places=6)
                    loss.backward()
                    self.assertEqual(target.logits.grad[-1].tolist(), [0, 0])
                    self.assertEqual(other.logits.grad[1:].tolist(), [[0, 0], [0, 0]])

    def test_nonfinite_and_other_invalid_fail_closed(self):
        for dtype in DTYPES:
            for value in (float("nan"), float("inf"), -float("inf")):
                for arm in ("C1", "C4"):
                    with self.subTest(dtype=dtype, value=value, arm=arm):
                        rows = invented(dtype)
                        with torch.no_grad():
                            rows[1].logits[0, 0] = value
                        with self.assertRaisesRegex(ValueError, "nonfinite logits"):
                            window_terms(rows[:2], TARGETS, arm)
                        self.assertIsNone(rows[0].logits.grad)
        # Finite float32 inputs can still overflow the float32 CE computation.
        rows = invented(torch.float32)
        extreme = torch.tensor([[3e38, -3e38, 0, 0]] * 5, dtype=torch.float32, requires_grad=True)
        with self.assertRaisesRegex(ValueError, "nonfinite loss"):
            window_terms([rows[0], Example(extreme, torch.tensor([-100, 1, 1, 1, 1]), 1)], TARGETS, "C1")
        self.assertIsNone(rows[0].logits.grad)
        for targets in ((True,), (False,), (True, True), (False, False)):
            for arm in ("C1", "C4"):
                with self.assertRaises(ValueError):
                    dataset_weights(targets, arm)
        rows = invented(torch.float32)
        for labels in ([-100, -100, -100, -100, -100], [-100, 4, 0, 0, 0],
                       [-100, -1, 0, 0, 0]):
            with self.assertRaises(ValueError):
                window_terms([Example(rows[0].logits, torch.tensor(labels), 0)], TARGETS, "C1")
        with self.assertRaises(TypeError):
            window_terms(rows[:1], TARGETS, "C1", denominator=1)
        with self.assertRaises(ValueError):
            window_terms([Example(rows[0].logits.double(), rows[0].labels, 0)], TARGETS, "C1")


if __name__ == "__main__":
    unittest.main(verbosity=2)
