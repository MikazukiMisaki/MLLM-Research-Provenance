"""Reconstruct two-stage input-token costs without treating unknown as zero.

Functions accept already-authorized in-memory recovery records. They do not
open files, run models, verify provenance, or authorize access to a dataset.
The unit is a recovery record, not necessarily an independent task.
"""

from collections.abc import Iterable, Mapping
from typing import Any


def _optional_count(value: Any) -> int | None:
    if value is None:
        return None
    if type(value) is not int or value < 0:
        raise ValueError("token counts must be nonnegative integers or None")
    return value


def reconstruct_input_cost(recovery: Mapping[str, Any]) -> dict[str, int | None]:
    """Use the separately saved stage records, not a zero-filled cost summary."""
    if not isinstance(recovery, Mapping):
        raise ValueError("recovery must be a mapping")
    first, second = recovery.get("stage_one"), recovery.get("stage_two")
    if not isinstance(first, Mapping) or not isinstance(second, Mapping):
        raise ValueError("both stage records are required")
    one = _optional_count(first.get("input_tokens"))
    two = _optional_count(second.get("input_tokens"))
    return {
        "stage_one_input_tokens": one,
        "stage_two_input_tokens": two,
        "total_input_tokens": one + two if one is not None and two is not None else None,
    }


def summarize_input_costs(recoveries: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """Report missing counts and full-record means; no missing-value imputation."""
    rows = [reconstruct_input_cost(recovery) for recovery in recoveries]
    metrics = {}
    for name in ("stage_one_input_tokens", "stage_two_input_tokens", "total_input_tokens"):
        values = [row[name] for row in rows]
        missing = sum(value is None for value in values)
        metrics[name] = {
            "observed_count": len(values) - missing,
            "missing_count": missing,
            "full_record_mean": (
                sum(values) / len(values) if values and missing == 0 else None
            ),
        }
    return {"record_count": len(rows), "metrics": metrics}
