#!/usr/bin/env python3
"""Summarize one recorded fictional-prompt scoring batch, without model access."""

import argparse
import collections
import hashlib
import json
import math
import statistics
from pathlib import Path

EXPECTED_SHA = "70b823a1c74c9fdce74337e78e5f93a9c22f1b87567b3931e073da81aec6a035"
IDS = {"A000", "A001", "A002", "A003"}
CONDITIONS = ("old_correct", "old_wrong", "false_correct", "false_wrong")


def analyze(path):
    raw = Path(path).read_bytes()
    if len(raw) > 8 * 1024 * 1024 or hashlib.sha256(raw).hexdigest() != EXPECTED_SHA:
        raise ValueError("journal digest or size mismatch")
    rows = [json.loads(line) for line in raw.splitlines()]
    if not rows or rows[-1].get("event") != "complete":
        raise ValueError("incomplete journal")
    loaded = [r for r in rows if r.get("event") == "loading_complete"]
    if len(loaded) != 1:
        raise ValueError("missing model metadata")
    prepared, scores = {}, collections.defaultdict(dict)
    for row in rows:
        if row.get("event") == "prepared":
            if row["key"] in prepared:
                raise ValueError("duplicate prompt")
            prepared[row["key"]] = row
        elif row.get("event") == "score":
            key, candidate, value = row["key"], row["candidate"], row["log_probability"]
            if candidate not in IDS or candidate in scores[key] or not math.isfinite(value):
                raise ValueError("invalid candidate score")
            scores[key][candidate] = value
    expected = {"%02d-%s" % (i, condition) for i in range(1, 9) for condition in CONDITIONS}
    if set(prepared) != expected or set(scores) != expected or rows[-1]["forward_count"] != 128:
        raise ValueError("missing planned result")
    values, groups = {}, {}
    for condition in CONDITIONS:
        probabilities, margins = [], []
        match = suffix_match = 0
        for i in range(1, 9):
            key = "%02d-%s" % (i, condition)
            row, entries = prepared[key], scores[key]
            if set(entries) != IDS or set(row["mapping"]) != IDS or len(set(row["mapping"].values())) != 4:
                raise ValueError("invalid mapping or candidates")
            inverse = {v: k for k, v in row["mapping"].items()}
            undo, take = inverse[row["undo_action"]], inverse[row["correct_action"]]
            maximum = max(entries.values())
            winners = [k for k, value in entries.items() if value == maximum]
            if len(winners) != 1:
                raise ValueError("candidate maximum is tied")
            exp_scores = {k: math.exp(v - maximum) for k, v in entries.items()}
            probability = exp_scores[undo] / sum(exp_scores.values())
            probabilities.append(probability)
            margins.append(entries[undo] - entries[take])
            match += winners[0] == row["prior_decoded"]
            suffix_match += row["prior_suffix"] == loaded[0]["suffixes"][row["prior_decoded"]]
            values[key] = probability
        groups[condition] = {
            "planned": 8, "valid": len(probabilities),
            "undo_weight_median": statistics.median(probabilities),
            "undo_weight_range": [min(probabilities), max(probabilities)],
            "undo_weight_above_0_9": sum(value > 0.9 for value in probabilities),
            "undo_minus_take_log_score_median": statistics.median(margins),
            "undo_minus_take_log_score_range": [min(margins), max(margins)],
            "canonical_argmax_matches_recorded_greedy": match,
            "canonical_suffix_matches_recorded": suffix_match,
        }
    pairs = {}
    for name, first, second in (
        ("goal_given_original_diagnosis", "old_correct", "old_wrong"),
        ("goal_given_injected_diagnosis", "false_correct", "false_wrong"),
        ("diagnosis_given_original_goal", "old_correct", "false_correct"),
        ("diagnosis_given_injected_goal", "old_wrong", "false_wrong"),
    ):
        diffs = [values["%02d-%s" % (i, second)] - values["%02d-%s" % (i, first)] for i in range(1, 9)]
        pairs[name] = {"valid": len(diffs), "increase": sum(x > 0 for x in diffs),
                       "equal": sum(x == 0 for x in diffs), "decrease": sum(x < 0 for x in diffs)}
    return {
        "source_sha256": EXPECTED_SHA,
        "scope": "same-operator recomputation of recorded fictional-prompt scores; no model execution or provenance authentication",
        "conditions": groups, "paired_undo_weight_changes": pairs,
        "forward_input_tokens": sum(r["forward_input_tokens"] for r in rows if r.get("event") == "score"),
        "sampled_gpu_max_mib": max(r["used_mib"] for r in rows if r.get("event") == "gpu_sample"),
        "max_prompt_seconds": max(r["request_seconds"] for r in rows if r.get("event") == "prompt_complete"),
        "completion": {k: rows[-1][k] for k in ("elapsed_seconds", "forward_count", "prompt_count",
                        "user_cpu_seconds", "system_cpu_seconds", "max_rss_kib")},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("journal")
    print(json.dumps(analyze(parser.parse_args().journal), indent=2, sort_keys=True))
