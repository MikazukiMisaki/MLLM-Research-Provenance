#!/usr/bin/env python3
"""Build a non-executable identity-only family-capacity addendum."""
import hashlib
import json
from collections import Counter
from pathlib import Path

OWN = Path(__file__).resolve().parent
EXPECTED = Path("/home/lizening/research-notes/agent-logs/2026-10-25T084517Z__LUNA__si-p3-isolation-budget-design__si3_7d91").resolve()
assert OWN == EXPECTED
SOURCE = OWN / "partition_proposal.json"
EXPECTED_SOURCE_SHA = "fd145fe6abee849b44231e1d0c816aa65813be2b67c48715f7ce7d2635e98d23"

def sha_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def largest_remainder(populations, target):
    total = sum(populations.values())
    floors = {k: target * v // total for k, v in populations.items()}
    remainder = {k: target * v % total for k, v in populations.items()}
    left = target - sum(floors.values())
    for key in sorted(populations, key=lambda k: (-remainder[k], k))[:left]:
        floors[key] += 1
    assert sum(floors.values()) == target
    assert all(floors[k] <= populations[k] for k in floors)
    return floors

assert sha_file(SOURCE) == EXPECTED_SOURCE_SHA
old = json.loads(SOURCE.read_text(encoding="utf-8"))
rows = old["rows"]
assert len(rows) == 1141
assert Counter(row["family"] for row in rows) == {
    "look_at_obj_in_light": 2,
    "pick_and_place_simple": 419,
    "pick_clean_then_place_in_recep": 301,
    "pick_cool_then_place_in_recep": 194,
    "pick_heat_then_place_in_recep": 106,
    "pick_two_obj_and_place": 119,
}

excluded_light = [r for r in rows if r["family"] == "look_at_obj_in_light"]
eligible = [r for r in rows if r["family"] != "look_at_obj_in_light"]
assert len(excluded_light) == 2 and len(eligible) == 1139
family_counts = dict(sorted(Counter(r["family"] for r in eligible).items()))
remaining = family_counts.copy()
quotas = {}
for partition, n in (("final_evaluation_train", 600), ("engineering_development_train", 48), ("acquisition_train", 480)):
    q = largest_remainder(remaining, n)
    quotas[partition] = q
    remaining = {family: remaining[family] - q[family] for family in remaining}
quotas["unallocated_nonlight_reserve"] = remaining
assert sum(remaining.values()) == 11
assert {k: sum(v.values()) for k, v in quotas.items()} == {
    "final_evaluation_train": 600,
    "engineering_development_train": 48,
    "acquisition_train": 480,
    "unallocated_nonlight_reserve": 11,
}

domain = "SI-P3-task-partition-v1\n"
assigned = []
for family in sorted(family_counts):
    pool = [r for r in eligible if r["family"] == family]
    ordered = sorted(pool, key=lambda r: hashlib.sha256((domain + family + "\n" + r["identity"] + "\n").encode("utf-8")).hexdigest())
    cursor = 0
    for partition in ("final_evaluation_train", "engineering_development_train", "acquisition_train", "unallocated_nonlight_reserve"):
        n = quotas[partition][family]
        for row in ordered[cursor:cursor+n]:
            rank = hashlib.sha256((domain + family + "\n" + row["identity"] + "\n").encode("utf-8")).hexdigest()
            assigned.append({"identity": row["identity"], "identity_sha256": row["identity_sha256"], "family": family, "partition": partition, "partition_rank_sha256": rank})
        cursor += n
    assert cursor == len(ordered)

assert len(assigned) == 1139
assert not {r["identity"] for r in assigned} & {r["identity"] for r in excluded_light}
counts = dict(Counter(r["partition"] for r in assigned))
assert counts == {"final_evaluation_train": 600, "engineering_development_train": 48, "acquisition_train": 480, "unallocated_nonlight_reserve": 11}
result = {
    "schema": "SI_P3_FAMILY_CAPACITY_ADJUSTMENT_NON_EXECUTABLE_V1",
    "status": "DESIGN_ADDENDUM_ONLY_NOT_A_SCHEDULE_NOT_AUTHORIZED",
    "supersedes_for_review_only": "original 480/60/600/1 allocation; original files remain unchanged",
    "input_partition_proposal_sha256": sha_file(SOURCE),
    "allocation_rule": "Exclude both look_at_obj_in_light candidates from every partition. For each stage in fixed order final_evaluation_train=600, engineering_development_train=48, acquisition_train=480, apportion the target across the remaining five-family capacities by Hamilton largest remainder (remainder descending, lexical family tie-break). Within family, order by SHA256(UTF8('SI-P3-task-partition-v1\\n'+family+'\\n'+canonical_identity+'\\n')); assign contiguous quotas in that fixed stage order. Remaining 11 are reserve.",
    "family_capacities": family_counts,
    "family_quotas": quotas,
    "partition_counts": counts,
    "excluded_light_candidates": [{"identity": r["identity"], "identity_sha256": r["identity_sha256"], "family": r["family"], "status": "RETAINED_UNRUN_NOT_REALLOCATED"} for r in excluded_light],
    "rows": assigned,
    "limits": ["identity/hash/family only", "no task body or result read", "no schedule/gate/argv", "all splits remain TRAIN task-disjoint, not held-out", "no light-family generality claim", "development identities reserved for engineering interface only; no effect-based recipe selection", "not an execution/training authorization"]
}
out = OWN / "partition_proposal_family_capacity_addendum.json"
out.write_text(json.dumps(result, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"source_sha256": sha_file(SOURCE), "candidate_counts": family_counts, "family_quotas": quotas, "partition_counts": counts, "excluded_light": len(excluded_light), "output": str(out), "output_sha256": sha_file(out)}, sort_keys=True))
