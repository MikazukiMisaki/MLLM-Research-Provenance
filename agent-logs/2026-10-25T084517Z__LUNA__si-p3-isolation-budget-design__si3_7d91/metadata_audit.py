#!/usr/bin/env python3
"""Metadata-only SI-P3 audit and non-executable partition proposal."""
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

OWN = Path(__file__).resolve().parent
EXPECTED_OWN = Path("/home/lizening/research-notes/agent-logs/2026-10-25T084517Z__LUNA__si-p3-isolation-budget-design__si3_7d91").resolve()
assert OWN == EXPECTED_OWN, (OWN, EXPECTED_OWN)

TASK = Path("/home/lizening/research-notes/agent-logs/2026-10-25T084517Z__SOL__si-p3-controlled-experience-design__si3_7d91")
CONSTRAINTS = TASK / "COMMON_DESIGN_CONSTRAINTS.md"
KNOWN = Path("/home/lizening/research-notes/agent-logs/2026-10-25T065200Z__LUNA__si-p1-isolation-budget__caae4c/KNOWN_USE_IDENTITIES.json")
SUPPORTED = Path("/home/lizening/research-notes/agent-logs/2026-10-25T065200Z__SOL__si-p1-protocol-review__caae4c/P0_SCOPE_INCIDENT_SNAPSHOT/SUPPORTED_IDENTITY_CANDIDATES.json")
PRESENCE = Path("/home/lizening/research-notes/agent-logs/2026-10-25T054106Z__SOL__self-improvement-phase0__b1c48c/independent_identity_file_presence.json")
COST = Path("/home/lizening/research-notes/agent-logs/2026-10-25T065200Z__LUNA__si-p1-isolation-budget__caae4c/corrected_isolation_budget_v2.json")
EXPECTED_CONSTRAINTS_SHA = "33e090877817c47a8fd4f046a3567fe06bc4498e52f343a3e3ca61dc21168647"

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def canon(obj):
    return json.dumps(obj, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")

def family(identity):
    return identity.split("/", 1)[0].split("-", 1)[0]

def largest_remainder(populations, total):
    denom = sum(populations.values())
    floors = {k: (total * v) // denom for k, v in populations.items()}
    residues = {k: (total * v) % denom for k, v in populations.items()}
    left = total - sum(floors.values())
    for k in sorted(populations, key=lambda x: (-residues[x], x))[:left]:
        floors[k] += 1
    assert sum(floors.values()) == total and all(floors[k] <= populations[k] for k in floors)
    return floors

paths = (CONSTRAINTS, KNOWN, SUPPORTED, PRESENCE, COST)
before = {str(p): {"bytes": p.stat().st_size, "sha256": sha(p)} for p in paths}
assert before[str(CONSTRAINTS)]["sha256"] == EXPECTED_CONSTRAINTS_SHA
known_doc = json.loads(KNOWN.read_text(encoding="utf-8"))
supported_doc = json.loads(SUPPORTED.read_text(encoding="utf-8"))
presence_doc = json.loads(PRESENCE.read_text(encoding="utf-8"))
cost_doc = json.loads(COST.read_text(encoding="utf-8"))

members = known_doc["registered_identity_members"]
known = set()
for name, values in members.items():
    if name == "registered_identity_group_sha256_sorted_newline":
        continue
    if isinstance(values, list):
        known.update(values)
assert len(known) == 2612

candidate_sets = {}
candidate_rows = {}
for split in ("train", "valid_seen", "valid_unseen"):
    rows = supported_doc[split]
    ids = []
    for row in rows:
        identity = row["identity"]
        actual_hash = hashlib.sha256(identity.encode("utf-8")).hexdigest()
        assert row["identity_sha256"] == actual_hash
        ids.append(identity)
        candidate_rows[identity] = {"identity": identity, "identity_sha256": actual_hash, "family": family(identity)}
    assert len(ids) == len(set(ids))
    candidate_sets[split] = set(ids)
assert len(candidate_sets["train"]) == 1141
assert len(candidate_sets["valid_seen"]) == 0
assert len(candidate_sets["valid_unseen"]) == 74
assert not any(candidate_sets[a] & candidate_sets[b] for a,b in (("train","valid_seen"),("train","valid_unseen"),("valid_seen","valid_unseen")))
known_overlaps = {split: sorted(ids & known) for split, ids in candidate_sets.items()}
assert {k: len(v) for k,v in known_overlaps.items()} == {"train": 0, "valid_seen": 0, "valid_unseen": 0}

candidate_family = {s: dict(sorted(Counter(family(x) for x in ids).items())) for s, ids in candidate_sets.items()}
presence_family = {s: v["family_counts_with_existing_game"] for s,v in presence_doc["splits"].items()}
presence_totals = {s: v["file_presence_candidate_difference_count"] for s,v in presence_doc["splits"].items()}
assert presence_totals == {"train": 1141, "valid_seen": 0, "valid_unseen": 74}
assert sum(presence_family["train"].values()) == presence_doc["splits"]["train"]["six_family_with_existing_game_file"]
assert sum(presence_family["valid_seen"].values()) == presence_doc["splits"]["valid_seen"]["six_family_with_existing_game_file"]
assert sum(presence_family["valid_unseen"].values()) == presence_doc["splits"]["valid_unseen"]["six_family_with_existing_game_file"]

# Fixed targets are discussion-only. A sequential, family-stratified apportionment
# preserves exact split totals and assigns from an outcome-blind keyed hash order.
targets = {"final_evaluation_train": 600, "development_train": 60, "acquisition_train": 480}
families = sorted(candidate_family["train"])
remaining = dict(candidate_family["train"])
quotas = {}
for split in ("final_evaluation_train", "development_train", "acquisition_train"):
    q = largest_remainder(remaining, targets[split])
    quotas[split] = q
    remaining = {f: remaining[f] - q[f] for f in families}
quotas["unallocated_reserve"] = remaining
assert sum(remaining.values()) == 1

partition_rows = []
partition_hash_domain = "SI-P3-task-partition-v1\n"
for fam in families:
    pool = [x for x in candidate_sets["train"] if family(x) == fam]
    order = sorted(pool, key=lambda x: hashlib.sha256((partition_hash_domain + fam + "\n" + x + "\n").encode("utf-8")).hexdigest())
    cursor = 0
    for split in ("final_evaluation_train", "development_train", "acquisition_train", "unallocated_reserve"):
        n = quotas[split][fam]
        for ident in order[cursor:cursor+n]:
            h = hashlib.sha256((partition_hash_domain + fam + "\n" + ident + "\n").encode("utf-8")).hexdigest()
            partition_rows.append({"identity": ident, "identity_sha256": candidate_rows[ident]["identity_sha256"], "family": fam, "partition": split, "partition_rank_sha256": h})
        cursor += n
    assert cursor == len(order)
assert len(partition_rows) == 1141
partition_counts = Counter(r["partition"] for r in partition_rows)
assert dict(partition_counts) == {"final_evaluation_train":600,"development_train":60,"acquisition_train":480,"unallocated_reserve":1}
partition_id_sets = {p: {r["identity"] for r in partition_rows if r["partition"] == p} for p in partition_counts}
for p1 in partition_id_sets:
    for p2 in partition_id_sets:
        if p1 < p2:
            assert not partition_id_sets[p1] & partition_id_sets[p2]
assert set().union(*partition_id_sets.values()) == candidate_sets["train"]
assert set().union(*partition_id_sets.values()).isdisjoint(known)
partition_by_family = {p: dict(sorted(Counter(r["family"] for r in partition_rows if r["partition"] == p).items())) for p in partition_counts}

source_split = known_doc["known_use_difference_by_split"]
audit = {
    "schema": "SI_P3_METADATA_AUDIT_V1",
    "status": "METADATA_ONLY_DESIGN_NOT_EXECUTION_AUTHORIZATION",
    "inputs_before": before,
    "known_use_registry": {"registered_union_count":len(known),"registered_union_sha256":hashlib.sha256("\n".join(sorted(known)).encode()).hexdigest(),"candidate_overlap_counts":{k:len(v) for k,v in known_overlaps.items()}},
    "supported_candidate_crosscheck": {"candidate_counts":{k:len(v) for k,v in candidate_sets.items()},"family_counts_from_identity_metadata":candidate_family,"metadata_file_presence_family_counts":presence_family,"file_presence_difference_counts_from_independent_record":presence_totals,"file_presence_status":{k:source_split[k]["status"] for k in source_split},"identity_hashes_verified":True,"split_sets_disjoint":True},
    "task_identity_rule": "canonical task/trial identity; exclude every known-use identity and all prefixes/seeds/aliases mapped to that identity; candidate file exposes identity hashes/families only.",
    "partition_proposal": {"targets":targets,"unallocated_reserve":1,"family_quotas":quotas,"family_counts":partition_by_family,"hash_rule":"SHA256('SI-P3-task-partition-v1\\n' + family + LF + canonical_identity + LF); within each family ascending hash; apportion final-evaluation, then development over remaining, then acquisition over remaining using largest remainder (fraction descending, family-name lexical tie-break).","rows":partition_rows,"non_executable":True,"valid_unseen_used":False,"task_body_or_result_read":False},
    "science_calls":{"model":0,"environment":0,"tokenizer":0,"training":0,"project_validator":0,"pytest":0},
}
after = {str(p): {"bytes":p.stat().st_size,"sha256":sha(p),"unchanged":sha(p)==before[str(p)]["sha256"]} for p in paths}
assert all(x["unchanged"] for x in after.values())
audit["inputs_after"] = after
(OWN/"metadata_audit.json").write_text(json.dumps(audit,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
proposal = {"schema":"SI_P3_NON_EXECUTABLE_TASK_PARTITION_PROPOSAL_V1","status":"DISCUSSION_ONLY_NOT_A_SCHEDULE_NOT_AUTHORIZED","source_supported_candidate_metadata_sha256":before[str(SUPPORTED)]["sha256"],"known_use_registry_sha256":before[str(KNOWN)]["sha256"],"allocation_rule":audit["partition_proposal"]["hash_rule"],"family_quotas":quotas,"family_counts":partition_by_family,"counts":dict(partition_counts),"rows":partition_rows,"known_use_union_count":len(known),"candidate_known_use_overlap":0,"valid_unseen_74_used":False,"limits":["identity/hash/family metadata only","no task body/results read","canonical task/trial is the exclusion unit","not proof against unregistered prior viewing or aliases","no schedule/gate/argv","not launch or training authorization"]}
(OWN/"partition_proposal.json").write_text(json.dumps(proposal,ensure_ascii=True,sort_keys=True,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"candidate_counts":audit["supported_candidate_crosscheck"]["candidate_counts"],"candidate_family_counts":candidate_family,"presence_family_counts":presence_family,"known_union":len(known),"candidate_known_overlap":audit["known_use_registry"]["candidate_overlap_counts"],"partition_counts":dict(partition_counts),"partition_family_counts":partition_by_family,"inputs_unchanged":all(x["unchanged"] for x in after.values()),"status":"complete"},sort_keys=True))
