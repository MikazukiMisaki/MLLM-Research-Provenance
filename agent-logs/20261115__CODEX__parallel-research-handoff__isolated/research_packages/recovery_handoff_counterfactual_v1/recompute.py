#!/usr/bin/env python3
"""Recompute an eight-pair fictional-prompt model observation on CPU.

The input is a local export of recorded outputs, not proof of model execution.
No model, tokenizer, task archive, or external service is accessed.
"""

import argparse
import json
from collections import Counter
from pathlib import Path

IDS = ("A000", "A001", "A002", "A003")
MARKER = "\n\nFrozen Stage-1 immediate subgoal:\n"
END = "\n\nIndexed admissible-action mapping:\n"


def _pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _split(prompt):
    if prompt.count(MARKER) != 1:
        raise ValueError("invalid prompt boundary")
    head, rest = prompt.split(MARKER, 1)
    if rest.count(END) != 1:
        raise ValueError("invalid prompt boundary")
    goal, tail = rest.split(END, 1)
    return head, goal, tail


def recompute(data):
    if (not isinstance(data, dict) or data.get("schema") != "recovery_handoff_counterfactual_v1"
            or not isinstance(data.get("records"), list) or len(data["records"]) != 8):
        raise ValueError("invalid dataset")
    records = data["records"]
    if [r.get("key") for r in records] != ["%02d" % i for i in range(1, 9)]:
        raise ValueError("invalid case keys")
    before, after, target_ids = Counter(), Counter(), Counter()
    changes = to_undo = 0
    for row in records:
        mapping = row["mapping"]
        if set(mapping) != set(IDS) or len(set(mapping.values())) != 4:
            raise ValueError("invalid action mapping")
        first_head, first_goal, first_tail = _split(row["baseline_prompt"])
        second_head, second_goal, second_tail = _split(row["intervention_prompt"])
        undo, correct = row["undo_first"], row["take_second"]
        if (first_head != second_head or first_tail != second_tail or first_goal == second_goal
                or second_goal != undo[0].upper() + undo[1:] + "."
                or undo == correct or undo not in mapping.values() or correct not in mapping.values()):
            raise ValueError("invalid paired intervention")
        actions = []
        for condition in ("baseline", "intervention"):
            result = row[condition]
            tokens, eos = result["token_ids"], result["eos_ids"]
            if (not isinstance(tokens, list) or not tokens or tokens[-1] not in eos
                    or result["decoded"] not in mapping):
                raise ValueError("invalid saved response")
            actions.append(mapping[result["decoded"]])
        if actions[0] != correct:
            raise ValueError("unexpected baseline action")
        category = ("undo_first" if actions[1] == undo else "take_second" if actions[1] == correct
                    else actions[1] if actions[1] in ("look", "inventory") else None)
        if category is None:
            raise ValueError("unexpected action")
        before["take_second"] += 1
        after[category] += 1
        target_ids[next(key for key in IDS if mapping[key] == undo)] += 1
        changes += actions[0] != actions[1]
        to_undo += actions[1] == undo
    return {
        "planned_pairs": 8, "valid_pairs": 8,
        "baseline_actions": dict(sorted(before.items())),
        "intervention_actions": dict(sorted(after.items())),
        "semantic_action_changes": changes, "take_second_to_undo_first": to_undo,
        "injected_action_id_counts": dict(sorted(target_ids.items())),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", help="explicit path to the fictional-prompt export")
    args = parser.parse_args()
    with Path(args.data).open("rb") as stream:
        raw = stream.read(1024 * 1024 + 1)
    if len(raw) > 1024 * 1024:
        raise ValueError("dataset too large")
    data = json.loads(raw, object_pairs_hook=_pairs)
    print(json.dumps(recompute(data), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
