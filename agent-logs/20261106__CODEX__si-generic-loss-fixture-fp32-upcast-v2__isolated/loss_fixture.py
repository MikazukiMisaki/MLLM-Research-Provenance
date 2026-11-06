"""Invented CPU-tensor arithmetic fixture. Not a training integration."""

from dataclasses import dataclass
import math

import torch
import torch.nn.functional as F


@dataclass(frozen=True)
class Example:
    logits: torch.Tensor  # [sequence, vocabulary]
    labels: torch.Tensor  # [sequence], including ignored prompt/padding
    record_index: int


def dataset_weights(targets, arm):
    """Weights based on distinct records, never occurrences or tokens."""
    if not isinstance(targets, (tuple, list)) or not targets:
        raise ValueError("targets must be a nonempty sequence")
    if any(type(value) is not bool for value in targets):
        raise ValueError("target labels must be explicit booleans")
    if arm not in ("C1", "C4"):
        raise ValueError("unknown arm")
    m, k = len(targets), sum(targets)
    if not 0 < k < m:
        raise ValueError("no informative target weighting contrast")
    alpha = m / (m + 3 * k)
    return tuple(1.0 if arm == "C1" else alpha * (4 if t else 1) for t in targets)


def window_terms(examples, targets, arm):
    """Return each occurrence's scaled native mean CE for one full window.

    Call backward on each term, once, then clip and step once per window.
    This fixture implements no external denominator, batching or distributed mode.
    """
    weights = dataset_weights(targets, arm)
    if not isinstance(examples, (tuple, list)) or not examples:
        raise ValueError("window must be nonempty")
    counts = []
    for example in examples:
        if not isinstance(example, Example):
            raise ValueError("invalid example")
        x, y, index = example.logits, example.labels, example.record_index
        if type(index) is not int or not 0 <= index < len(weights):
            raise ValueError("invalid record index")
        if not isinstance(x, torch.Tensor) or not isinstance(y, torch.Tensor):
            raise ValueError("expected tensors")
        if x.device.type != "cpu" or y.device.type != "cpu":
            raise ValueError("CPU tensors required")
        if x.ndim != 2 or y.ndim != 1 or x.shape[0] != y.shape[0] or x.shape[0] < 2 or x.shape[1] < 2:
            raise ValueError("invalid tensor shapes")
        if x.dtype not in (torch.bfloat16, torch.float16, torch.float32) or not x.requires_grad or y.dtype != torch.long:
            raise ValueError("invalid tensor dtype or gradients")
        if not bool(torch.isfinite(x).all()):
            raise ValueError("nonfinite logits")
        if bool(((y != -100) & ((y < 0) | (y >= x.shape[1]))).any()):
            raise ValueError("invalid vocabulary label")
        count = int((y[1:] != -100).sum())
        if count == 0:
            raise ValueError("zero shifted supervision")
        counts.append(count)
    denominator = sum(counts)
    terms = []
    for example, count in zip(examples, counts):
        native_mean = F.cross_entropy(example.logits[:-1].float(), example.labels[1:], ignore_index=-100, reduction="mean")
        term = native_mean * (weights[example.record_index] * count / denominator)
        if not math.isfinite(term.item()):
            raise ValueError("nonfinite loss")
        terms.append(term)
    return tuple(terms)
