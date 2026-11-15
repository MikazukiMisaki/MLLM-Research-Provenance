#!/usr/bin/env python3
"""Paired score contrasts from one recorded fictional-prompt batch."""

import argparse
import collections
import hashlib
import json
import math
import statistics
from pathlib import Path

SOURCE_SHA = "70b823a1c74c9fdce74337e78e5f93a9c22f1b87567b3931e073da81aec6a035"
IDS = {"A000", "A001", "A002", "A003"}
CONDITIONS = ("old_correct", "old_wrong", "false_correct", "false_wrong")


def summarize(values):
    return {"n": len(values), "median": statistics.median(values),
            "minimum": min(values), "maximum": max(values),
            "positive": sum(x > 0 for x in values),
            "zero": sum(x == 0 for x in values), "negative": sum(x < 0 for x in values)}


def analyze(path):
    raw = Path(path).read_bytes()
    if len(raw) > 8 * 1024 * 1024 or hashlib.sha256(raw).hexdigest() != SOURCE_SHA:
        raise ValueError("input digest or size mismatch")
    rows = [json.loads(line) for line in raw.splitlines()]
    if not rows or rows[-1].get("event") != "complete" or rows[-1].get("forward_count") != 128:
        raise ValueError("incomplete scoring batch")
    pre, scores = {}, collections.defaultdict(dict)
    for row in rows:
        if row.get("event") == "prepared":
            if row["key"] in pre:
                raise ValueError("duplicate prompt")
            pre[row["key"]] = row
        elif row.get("event") == "score":
            key, candidate, value = row["key"], row["candidate"], row["log_probability"]
            if candidate not in IDS or candidate in scores[key] or not math.isfinite(value):
                raise ValueError("invalid score")
            scores[key][candidate] = value
    expected = {"%02d-%s" % (i, c) for i in range(1, 9) for c in CONDITIONS}
    if set(pre) != expected or set(scores) != expected:
        raise ValueError("unexpected prompts")
    contrasts = {name: [] for name in (
        "goal_given_original_diagnosis", "goal_given_injected_diagnosis",
        "diagnosis_given_original_goal", "diagnosis_given_injected_goal", "interaction")}
    per_case = []
    for i in range(1, 9):
        key = "%02d" % i
        current = [pre[key + "-" + c] for c in CONDITIONS]
        mapping, take, undo = current[0]["mapping"], current[0]["correct_action"], current[0]["undo_action"]
        if (set(mapping) != IDS or len(set(mapping.values())) != 4 or take == undo
                or any(r["mapping"] != mapping or r["correct_action"] != take
                       or r["undo_action"] != undo for r in current)):
            raise ValueError("mapping mismatch")
        inverse = {v: k for k, v in mapping.items()}
        take_id, undo_id = inverse[take], inverse[undo]
        log_odds = {}
        for c in CONDITIONS:
            s = scores[key + "-" + c]
            if set(s) != IDS:
                raise ValueError("missing scores")
            log_odds[c] = s[undo_id] - s[take_id]
        a, b, c, d = (log_odds[name] for name in CONDITIONS)
        row = {"key": key, "goal_given_original_diagnosis": b - a,
               "goal_given_injected_diagnosis": d - c,
               "diagnosis_given_original_goal": c - a,
               "diagnosis_given_injected_goal": d - b,
               "interaction": (d - c) - (b - a)}
        per_case.append(row)
        for name in contrasts:
            contrasts[name].append(row[name])
    return {"source_sha256": SOURCE_SHA,
            "scope": "post-result contrasts of same-operator recorded fictional-prompt scores",
            "summaries": {name: summarize(values) for name, values in contrasts.items()},
            "per_case": per_case}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("journal")
    print(json.dumps(analyze(parser.parse_args().journal), indent=2, sort_keys=True))
