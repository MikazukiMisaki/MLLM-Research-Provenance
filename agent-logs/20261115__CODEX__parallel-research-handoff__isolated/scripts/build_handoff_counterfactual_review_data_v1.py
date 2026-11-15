#!/usr/bin/env python3
"""Export only the recorded fictional prompt pairs for local CPU review."""

import argparse
import json
from pathlib import Path

import analyze_incorrect_subgoal_handoff_v1 as source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline")
    parser.add_argument("intervention")
    parser.add_argument("output")
    args = parser.parse_args()

    # Validate the saved raw outputs, prompt pairing and source digests first.
    source.analyze(args.baseline, args.intervention)
    original = source._read(args.baseline, source.BASE_SHA)
    changed = source._read(args.intervention, source.INJECTION_SHA)
    base = source._index(original, "prepared", lambda r: r["key"].endswith("-generated"), lambda k: k[:2])
    generated = source._index(original, "generation", lambda r: r["key"].endswith("-generated"), lambda k: k[:2])
    new = source._index(changed, "prepared", lambda r: True, lambda k: k)
    decisions = source._index(changed, "decision", lambda r: True, lambda k: k)
    base_eos = next(r["eos_ids"] for r in original if r.get("event") == "loading_complete")
    new_eos = next(r["eos_ids"] for r in changed if r.get("event") == "loading_complete")
    records = []
    for key in sorted(base):
        a, b, old, result = base[key], new[key], generated[key], decisions[key]
        records.append({
            "key": key,
            "baseline_prompt": a["prompt"],
            "intervention_prompt": b["prompt"],
            "mapping": a["mapping"],
            "take_second": a["correct_action"],
            "undo_first": b["undo_action"],
            "baseline": {"decoded": old["decoded"], "token_ids": old["token_ids"], "eos_ids": base_eos},
            "intervention": {"decoded": result["decoded"], "token_ids": result["token_ids"], "eos_ids": new_eos},
        })
    data = {
        "schema": "recovery_handoff_counterfactual_v1",
        "source_sha256": {"baseline": source.BASE_SHA, "intervention": source.INJECTION_SHA},
        "records": records,
    }
    with Path(args.output).open("x", encoding="utf-8") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2, sort_keys=True)
        stream.write("\n")


if __name__ == "__main__":
    main()
