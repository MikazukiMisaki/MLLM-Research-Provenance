#!/usr/bin/env python3
"""Recompute the eight fictional-prompt pairs from two explicitly supplied logs.

This checks saved records, not model provenance or physical execution. The
caller must have permission to read both paths; the program never selects tasks.
"""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

BASE_SHA = "ea1ef47972d23e5b76e2a6d979650e499ef3002ab34b9ba6b75cc4b4931d2c9b"
INJECTION_SHA = "f7257a33a936856b933c6c9b4a12094d7b91d1c5ec75eb5997616fd7608307be"
MAX_BYTES = 2 * 1024 * 1024
MARKER = "\n\nFrozen Stage-1 immediate subgoal:\n"
END = "\n\nIndexed admissible-action mapping:\n"
IDS = ("A000", "A001", "A002", "A003")


def _pairs(items):
    out = {}
    for key, value in items:
        if key in out:
            raise ValueError("duplicate JSON key")
        out[key] = value
    return out


def _read(path, expected_sha):
    with Path(path).open("rb") as stream:
        data = stream.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES or hashlib.sha256(data).hexdigest() != expected_sha:
        raise ValueError("input size or digest mismatch")
    rows = [json.loads(line, object_pairs_hook=_pairs) for line in data.splitlines()]
    if not rows or rows[-1].get("event") != "complete":
        raise ValueError("incomplete input")
    return rows


def _index(rows, event, predicate, normalize):
    indexed = {}
    for row in rows:
        if row.get("event") == event and predicate(row):
            key = normalize(row["key"])
            if key in indexed:
                raise ValueError("duplicate record")
            indexed[key] = row
    if set(indexed) != {"%02d" % i for i in range(1, 9)}:
        raise ValueError("missing or extra planned key")
    return indexed


def _split(prompt):
    if prompt.count(MARKER) != 1:
        raise ValueError("prompt boundary mismatch")
    head, rest = prompt.split(MARKER, 1)
    if rest.count(END) != 1:
        raise ValueError("prompt boundary mismatch")
    goal, tail = rest.split(END, 1)
    return head, goal, tail


def analyze(baseline_path, intervention_path):
    baseline, changed = _read(baseline_path, BASE_SHA), _read(intervention_path, INJECTION_SHA)
    base_prompt = _index(baseline, "prepared", lambda r: r["key"].endswith("-generated"), lambda k: k[:2])
    base_stage = _index(baseline, "prepared", lambda r: r["key"].endswith("-stage1"), lambda k: k[:2])
    base_result = _index(baseline, "decision", lambda r: r.get("condition") == "generated", lambda k: k)
    base_generation = _index(baseline, "generation", lambda r: r["key"].endswith("-generated"), lambda k: k[:2])
    base_raw = _index(baseline, "raw_result", lambda r: r["key"].endswith("-generated"), lambda k: k[:2])
    new_prompt = _index(changed, "prepared", lambda r: True, lambda k: k)
    new_raw = _index(changed, "raw_result", lambda r: True, lambda k: k)
    new_result = _index(changed, "decision", lambda r: True, lambda k: k)
    eos_rows = [r for r in changed if r.get("event") == "loading_complete"]
    base_eos_rows = [r for r in baseline if r.get("event") == "loading_complete"]
    if (len(eos_rows) != 1 or len(base_eos_rows) != 1
            or not isinstance(eos_rows[0].get("eos_ids"), list)
            or not isinstance(base_eos_rows[0].get("eos_ids"), list)):
        raise ValueError("missing EOS declaration")
    eos = eos_rows[0]["eos_ids"]
    base_eos = base_eos_rows[0]["eos_ids"]
    baseline_counts, changed_counts, target_ids = Counter(), Counter(), Counter()
    changes = to_undo = 0
    for key in sorted(base_prompt):
        a, b, old, generation, result = (
            base_prompt[key], new_prompt[key], base_result[key], base_generation[key], new_result[key]
        )
        mapping = a["mapping"]
        if (set(mapping) != set(IDS) or len(set(mapping.values())) != 4 or mapping != b["mapping"]
                or a["correct_action"] != b["correct_action"]
                or base_stage[key]["undo_action"] != b["undo_action"]):
            raise ValueError("mapping mismatch")
        old_head, old_goal, old_tail = _split(a["prompt"])
        new_head, new_goal, new_tail = _split(b["prompt"])
        undo = b["undo_action"]
        if (old_head != new_head or old_tail != new_tail or old_goal != b["original_subgoal"]
                or new_goal != b["injected_subgoal"] or new_goal != undo[0].upper() + undo[1:] + "."
                or old_goal == new_goal):
            raise ValueError("unexpected prompt difference")
        base_tokens = generation["token_ids"]
        if (generation["status"] != "complete" or not base_tokens or base_tokens[-1] not in base_eos
                or base_raw[key]["output_ids"][a["input_token_count"]:] != base_tokens
                or mapping.get(generation["decoded"]) != old["selected_action"]):
            raise ValueError("baseline action mismatch")
        tokens = result["token_ids"]
        if (not isinstance(tokens, list) or not tokens or tokens[-1] not in eos
                or new_raw[key]["output_ids"][b["input_token_count"]:] != tokens
                or mapping.get(result["decoded"]) != result["selected_action"]):
            raise ValueError("intervention token or action mismatch")
        correct = b["correct_action"]
        if old["selected_action"] != correct or old["category"] != "take_second":
            raise ValueError("unexpected baseline outcome")
        action = result["selected_action"]
        category = ("undo_first" if action == undo else "take_second" if action == correct
                    else action if action in ("look", "inventory") else None)
        if category is None or result["category"] != category:
            raise ValueError("intervention category mismatch")
        baseline_counts["take_second"] += 1
        changed_counts[category] += 1
        target_ids[next(name for name in IDS if mapping[name] == undo)] += 1
        changes += action != old["selected_action"]
        to_undo += action == undo
    return {
        "schema": "incorrect_subgoal_handoff_analysis_v1",
        "source_sha256": {"baseline": BASE_SHA, "intervention": INJECTION_SHA},
        "planned_pairs": 8, "valid_pairs": 8,
        "baseline_actions": dict(sorted(baseline_counts.items())),
        "intervention_actions": dict(sorted(changed_counts.items())),
        "semantic_action_changes": changes, "take_second_to_undo_first": to_undo,
        "injected_action_id_counts": dict(sorted(target_ids.items())),
        "scope": "saved fictional-prompt logs; no provenance or physical-execution authentication",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline")
    parser.add_argument("intervention")
    args = parser.parse_args()
    print(json.dumps(analyze(args.baseline, args.intervention), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
