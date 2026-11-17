"""Recompute the public fictional format study using only two JSON inputs.

Uses saved decoded strings, never saved category/action as scoring inputs.
No package imports, tokenizer, model, environment, or execution of input text.
Run: python3 -I -S -B check.py /path/to/cases.json /path/to/sanitized_events.jsonl
"""
import collections
import hashlib
import json
import sys
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON member: " + key)
        result[key] = value
    return result


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def bare_shape(value):
    return (isinstance(value, str) and len(value) == 4
            and value[0] == "A"
            and all(ch in "0123456789" for ch in value[1:]))


def classify(text, output_format, mapping):
    # No strip, bracket repair, substring extraction, or case normalization.
    if output_format == "bare":
        shape = bare_shape(text)
        candidate = text if shape else None
    else:
        shape = (len(text) == 6 and text[0] == "[" and text[-1] == "]"
                 and bare_shape(text[1:-1]))
        candidate = text[1:-1] if shape else None
    valid = shape and candidate in mapping
    return {
        "shape": shape,
        "valid": valid,
        "candidate": candidate,
        "action": mapping[candidate] if valid else None,
        "bare_reference": bare_shape(text) and text in mapping,
    }


def main():
    require(len(sys.argv) == 3, "provide cases.json and sanitized_events.jsonl")
    paths = [Path(arg) for arg in sys.argv[1:]]
    blobs = [path.read_bytes() for path in paths]
    expected_hashes = [
        "2873429462c3fe2b7f4b30e049b258d5caf31826c7fbf2e34342cf3ec851ec46",
        "4a8b5a4a5251d9060bfc95603d9925ea9c7e3dfc92e5f9270646dbd753957d0e",
    ]
    require([sha(b) for b in blobs] == expected_hashes, "input hash mismatch")
    design = json.loads(blobs[0], object_pairs_hook=unique_object)
    events = [json.loads(line, object_pairs_hook=unique_object)
              for line in blobs[1].splitlines() if line.strip()]
    calls = design["calls"]
    require(len(calls) == 32, "expected 32 planned calls")
    planned_ids = [c["call_id"] for c in calls]
    require(len(set(planned_ids)) == 32, "duplicate planned call_id")
    planned_set = set(planned_ids)
    conditions = {(r, f) for r in ("plain", "bracket")
                  for f in ("bare", "bracket")}
    by_case = collections.defaultdict(dict)
    for c in calls:
        condition = (c["row_format"], c["output_format"])
        require(condition in conditions, "unknown condition")
        require(condition not in by_case[c["case_id"]], "duplicate case/condition")
        by_case[c["case_id"]][condition] = c
        require(set(c["mapping"]) == {"A000", "A001", "A002", "A003"},
                "unexpected candidate IDs")
        require(list(c["mapping"].values()).count(c["specified_action"]) == 1,
                "specified action not uniquely mapped")
        # Bind the expected target and rows to the fixed prompt itself.
        directive = c["prompt"].split("Immediate subgoal:\n", 1)[1].split("\n", 1)[0]
        require(directive == c["specified_action"][0].upper()
                + c["specified_action"][1:] + ".", "subgoal/mapping discrepancy")
        actual_rows = c["prompt"].split("Currently available actions:\n", 1)[1]
        actual_rows = actual_rows.split("\n\nYour response:", 1)[0]
        intended_rows = "\n".join(
            (key if c["row_format"] == "plain" else "[" + key + "]")
            + "  " + value for key, value in c["mapping"].items())
        require(actual_rows == intended_rows, "prompt row/mapping discrepancy")
        instruction = ("Return exactly one action ID without surrounding square brackets. "
                       "Do not output anything else." if c["output_format"] == "bare" else
                       "Return exactly one action ID enclosed in square brackets. "
                       "Do not output anything else.")
        require(c["prompt"].splitlines()[1] == instruction,
                "output-format instruction discrepancy")
    require(len(by_case) == 8, "expected eight cases")
    for case_id, cells in by_case.items():
        require(set(cells) == conditions, "incomplete factorial for " + case_id)
        reference = next(iter(cells.values()))
        for c in cells.values():
            require(list(c["mapping"].items()) == list(reference["mapping"].items()),
                    "within-case mapping or order differs")
            require(c["specified_action"] == reference["specified_action"],
                    "within-case subgoal differs")

    stages = ("prepared", "call_start", "raw_result", "decision")
    indexed = {stage: {} for stage in stages}
    stage_order = {stage: [] for stage in stages}
    event_counts = collections.Counter(e["event"] for e in events)
    for index, event in enumerate(events):
        stage = event["event"]
        if "call_id" in event:
            require(event["call_id"] in planned_set, "unplanned event call_id")
        if stage in indexed:
            key = event["call_id"]
            require(key not in indexed[stage], "duplicate " + stage + ": " + key)
            indexed[stage][key] = (index, event)
            stage_order[stage].append(key)
    for stage in stages:
        require(set(indexed[stage]) == planned_set, "missing keys for " + stage)
        require(stage_order[stage] == planned_ids, "plan-order discrepancy: " + stage)
    loading = [e for e in events if e["event"] == "loading_start"]
    require(len(loading) == 1 and loading[0]["cases_sha256"] == expected_hashes[0],
            "recorded fixed-case binding discrepancy")
    completed = [(i, e) for i, e in enumerate(events) if e["event"] == "complete"]
    require(len(completed) == 1 and completed[0][1]["call_count"] == 32,
            "completion/count discrepancy")

    totals = {condition: collections.Counter(planned=0, shape=0, valid=0,
              specified_joint=0, bare_reference=0) for condition in conditions}
    computed = {}
    discrepancies = []
    invalid = []
    for c in calls:
        key = c["call_id"]
        indexes = [indexed[stage][key][0] for stage in stages]
        require(indexes == sorted(indexes) and len(set(indexes)) == 4,
                "event chronology discrepancy: " + key)
        require(indexes[-1] < completed[0][0], "completion precedes a decision")
        prepared = indexed["prepared"][key][1]
        returned = indexed["raw_result"][key][1]
        decision = indexed["decision"][key][1]
        for field in ("case_id", "family", "row_format", "output_format"):
            require(prepared[field] == c[field] == decision[field],
                    "metadata discrepancy: " + key + "/" + field)
        require(prepared["prompt"] == c["prompt"], "prompt mismatch: " + key)
        require(list(prepared["mapping"].items()) == list(c["mapping"].items()),
                "recorded mapping/order mismatch: " + key)
        require(prepared["rendered_prompt"].count(c["prompt"]) == 1,
                "fixed prompt not uniquely embedded in rendered prompt")
        require(isinstance(returned["output_token_ids"], list)
                and len(returned["output_token_ids"]) > 0,
                "missing returned token sequence")
        text = decision["decoded"]
        require(isinstance(text, str), "decoded output is not text")
        score = classify(text, c["output_format"], c["mapping"])
        score["specified_joint"] = score["valid"] and score["action"] == c["specified_action"]
        computed[key] = score
        # Original classification is used only after independent scoring, as a comparator.
        if ((decision["category"] == "valid") != score["valid"]
                or decision["action"] != score["action"]
                or (not score["shape"] and decision["category"] != "format_mismatch")):
            discrepancies.append(key)
        count = totals[(c["row_format"], c["output_format"])]
        count["planned"] += 1
        for field in ("shape", "valid", "specified_joint", "bare_reference"):
            count[field] += int(score[field])
        if not score["valid"]:
            invalid.append({"call_id": key, "decoded": text,
                            "shape": score["shape"], "action": score["action"]})

    pairs = {}
    for requested in ("bare", "bracket"):
        count = collections.Counter(planned_pairs=0, both_valid=0, plain_only=0,
                                    bracket_only=0, neither=0, same_valid_id=0,
                                    same_valid_action=0, both_match_subgoal=0)
        for cells in by_case.values():
            left = computed[cells[("plain", requested)]["call_id"]]
            right = computed[cells[("bracket", requested)]["call_id"]]
            count["planned_pairs"] += 1
            if left["valid"] and right["valid"]:
                count["both_valid"] += 1
                count["same_valid_id"] += int(left["candidate"] == right["candidate"])
                count["same_valid_action"] += int(left["action"] == right["action"])
                count["both_match_subgoal"] += int(left["specified_joint"] and right["specified_joint"])
            elif left["valid"]:
                count["plain_only"] += 1
            elif right["valid"]:
                count["bracket_only"] += 1
            else:
                count["neither"] += 1
        pairs[requested] = dict(count)

    require([path.read_bytes() for path in paths] == blobs, "inputs changed during check")
    result = {
        "scope": "Independent recomputation from saved decoded text; no token decoding or physical attestation",
        "input_sha256": dict(zip(("cases.json", "sanitized_events.jsonl"), expected_hashes)),
        "unique_planned_keys": len(planned_set),
        "event_counts": dict(event_counts),
        "each_key_once_in_each_stage": True,
        "stage_order_matches_plan": True,
        "per_key_event_chronology": True,
        "fixed_prompts_metadata_and_ordered_mappings_match": True,
        "loading_record_cases_hash_matches": True,
        "completion_after_all_decisions": True,
        "conditions": [{"row_format": r, "output_format": f, **totals[(r, f)]}
                       for r, f in (("plain", "bare"), ("bracket", "bare"),
                                    ("plain", "bracket"), ("bracket", "bracket"))],
        "pairs_by_output_requirement": pairs,
        "invalid_calls": invalid,
        "classification_discrepancies": discrepancies,
        "source_bytes_unchanged": True,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if discrepancies else 0


if __name__ == "__main__":
    sys.exit(main())
