#!/usr/bin/env python3
"""Read-only task/trial identity inventory; never opens task outcome files."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path


ROOT = Path("/home/lizening/wt-codex-r18c2")
DATA = Path("/home/lizening/alfworld_data/json_2.1.1")
OUT = Path(__file__).with_name("AVAILABLE_IDENTITY_AUDIT.json")
CANDIDATES_OUT = Path(__file__).with_name("AVAILABLE_IDENTITY_CANDIDATES.json")
R19 = Path(
    "/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/"
    "r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z/unit_registry.json"
)
RUNTIME = Path("/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/validation")
FIXED_CASES = Path("/home/lizening/research-notes/agent-logs/2026-10-25T065200Z__SOL__si-p1-protocol-review__caae4c/FIXED_ELEVEN_CASES.json")
RAW_INVENTORY = Path(__file__).with_name("raw_artifact_inventory.json")
P0_FILE_PRESENCE = Path("/home/lizening/research-notes/agent-logs/2026-10-25T054106Z__SOL__self-improvement-phase0__b1c48c/independent_identity_file_presence.json")
SUPPORTED_OUT = Path(__file__).with_name("SUPPORTED_IDENTITY_CANDIDATES.json")
CASES_OUT = Path(__file__).with_name("FIXED_CASE_ISOLATION.json")


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def canon(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    value = value.replace("\\", "/").strip()
    while value.startswith("./"):
        value = value[2:]
    value = value.strip("/")
    if not value or value in {".", ".."} or "/../" in f"/{value}/":
        return None
    return value


def ids_from(value: object, key: str = "task_id") -> set[str]:
    if isinstance(value, dict):
        found: set[str] = set()
        if key in value:
            item = canon(value[key])
            if item:
                found.add(item)
        for k, child in value.items():
            if k != key and isinstance(child, (dict, list)):
                found |= ids_from(child, key)
        return found
    if isinstance(value, list):
        found: set[str] = set()
        for child in value:
            found |= ids_from(child, key)
        return found
    return set()


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def directory_inventory(split: str) -> tuple[set[str], set[str], dict[str, int]]:
    base = DATA / split
    tasks: set[str] = set()
    trials: set[str] = set()
    trials_per_task: Counter[str] = Counter()
    for task in os.scandir(base):
        if not task.is_dir(follow_symlinks=False):
            continue
        tasks.add(task.name)
        for trial in os.scandir(task.path):
            if trial.is_dir(follow_symlinks=False):
                identity = canon(f"{task.name}/{trial.name}")
                if identity:
                    trials.add(identity)
                    trials_per_task[task.name] += 1
    return tasks, trials, dict(trials_per_task)


def hashed_ids(items: set[str]) -> list[dict[str, str]]:
    return [
        {"identity": x, "identity_sha256": hashlib.sha256(x.encode("utf-8")).hexdigest()}
        for x in sorted(items)
    ]


def input_record(path: Path, role: str) -> dict[str, object]:
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": file_sha(path), "role": role}


def main() -> int:
    cfg = ROOT / "configs"
    accepted_path = cfg / "sft/sft_accepted_task_splits.json"
    sft_excl_path = cfg / "sft/sft_task_exclusions.json"
    heldout_excl_path = cfg / "evaluation/sft_heldout_exclusions.json"
    seen_schedule_path = cfg / "evaluation/sft_heldout_valid_seen_schedule.json"
    unseen_schedule_path = cfg / "evaluation/sft_heldout_valid_unseen_schedule.json"
    sft_rec_excl_path = cfg / "recovery/sft_recovery_source_exclusions.json"
    persistent_excl_path = cfg / "recovery/persistent_recovery_exclusions.json"
    progress_excl_path = cfg / "recovery/progress_aware_source_exclusions.json"
    r4_manifest = RUNTIME / "sft-recovery-feasibility-r4-20260908T080000Z/run_manifest.json"
    round_manifests = {
        "R14": RUNTIME / "progress-aware-recovery-r14-20260910T000000Z/run_manifest.json",
        "R15": RUNTIME / "progress-aware-recovery-r15-b-20260910T000000Z/run_manifest.json",
        "R16": RUNTIME / "progress-aware-recovery-r16-osr-20260910T000000Z/run_manifest.json",
        "R17": RUNTIME / "progress-aware-recovery-r17-par-20260911T000000Z/run_manifest.json",
        "R18_C1": RUNTIME / "progress-aware-r18-c1-20260911T000000Z/run_manifest.json",
        "R18_C2": RUNTIME / "progress-aware-r18-c2-formal-aa9fa3c34520941e/run_manifest.json",
    }
    paths = [
        accepted_path, sft_excl_path, heldout_excl_path, seen_schedule_path,
        unseen_schedule_path, sft_rec_excl_path, persistent_excl_path,
        progress_excl_path, r4_manifest, R19, *round_manifests.values(),
        FIXED_CASES, RAW_INVENTORY, P0_FILE_PRESENCE,
    ]
    inputs = [input_record(p, "identity/schedule/exclusion/consumed-registration metadata only") for p in paths]

    accepted = load_json(accepted_path)
    accepted_pools = accepted["pools"]
    groups: dict[str, set[str]] = {
        "expert_train": {canon(x.get("task_id")) for x in accepted_pools["train"]},
        "expert_validation": {canon(x.get("task_id")) for x in accepted_pools["validation"]},
        "online_development": {canon(x.get("task_id")) for x in accepted_pools["online_evaluation"]},
    }
    for group in groups.values():
        group.discard(None)

    heldout = load_json(heldout_excl_path)
    heldout_categories = {
        k: {canon(x) for x in values if canon(x)}
        for k, values in heldout.get("categories", {}).items()
    }
    groups["prior_architecture"] = heldout_categories.get("prior_phase_ab_architecture_tasks", set())
    groups["prior_recovery_source_pool"] = heldout_categories.get("prior_recovery_development_and_source_pool_tasks", set())
    groups["heldout_exclusion_union"] = {canon(x) for x in heldout.get("excluded_task_ids", []) if canon(x)}

    # The old valid_seen identities are already-consumed IDs within the held-out
    # exclusion register; take the split intersection after listing directory names.
    unseen_schedule = load_json(unseen_schedule_path)
    groups["valid_unseen_consumed_G1"] = ids_from(unseen_schedule.get("episodes", []))

    exclusion_paths = [sft_excl_path, sft_rec_excl_path, persistent_excl_path, progress_excl_path]
    exclusion_values = [load_json(p) for p in exclusion_paths]
    all_exclusion_ids: set[str] = set()
    for doc in exclusion_values:
        all_exclusion_ids |= {canon(x) for x in doc.get("excluded_task_ids", []) if canon(x)}
        all_exclusion_ids |= ids_from(doc.get("categories", {}))
        all_exclusion_ids |= ids_from(doc.get("entries", []))
    groups["all_saved_exclusion_registers"] = all_exclusion_ids

    progress = load_json(progress_excl_path)
    reason_sets: dict[str, set[str]] = {}
    for entry in progress.get("entries", []):
        task = canon(entry.get("task_id"))
        if not task:
            continue
        for reason in entry.get("reasons", []):
            reason_sets.setdefault(reason, set()).add(task)
    for reason in [
        "r6_r7_source_pool_or_sprint2c", "r8_scientific_prefix_or_progress_audit",
        "r9_continue", "r10_osr", "r11_pbr", "r11a_smoke",
        "r12_examples_or_mechanism_audit", "previous_recovery_experiment_tasks",
    ]:
        groups[f"recovery_register:{reason}"] = reason_sets.get(reason, set())

    # Completed R14 task/trial identities are registered in its run manifest.
    r14 = load_json(round_manifests["R14"])
    r14_ids = ids_from(r14.get("schedule_positions", [])) if r14.get("status") == "completed" else set()
    groups["R14_completed_schedule_positions"] = r14_ids

    # R16/R17 contain consumed prefix IDs, not canonical task/trial IDs; record them separately.
    prefix_registrations = {}
    for round_name in ["R15", "R16", "R17"]:
        doc = load_json(round_manifests[round_name])
        prefix_ids = doc.get("prefix_order", []) if doc.get("status") == "completed" else []
        prefix_registrations[round_name] = {
            "status": doc.get("status"),
            "prefix_id_count": len(prefix_ids),
            "prefix_ids_sha256": hashlib.sha256("\n".join(sorted(prefix_ids)).encode()).hexdigest(),
            "canonical_task_trial_mapping": "not read from outcome-bearing reports in this metadata-only task",
        }
    for round_name in ["R18_C1", "R18_C2"]:
        doc = load_json(round_manifests[round_name])
        prefix_registrations[round_name] = {
            "status": doc.get("status"),
            "registered_prefix_count": doc.get("prefixes"),
            "heldout_consumption_count": doc.get("held_out_consumption"),
            "canonical_task_trial_ids_present_in_manifest": False,
        }

    r4 = load_json(r4_manifest)
    r4_prefix_ids = r4.get("completed_prefix_ids", [])
    r4_registration = {
        "status": r4.get("status"),
        "completed_prefix_id_count": len(r4_prefix_ids),
        "prefix_ids_sha256": hashlib.sha256("\n".join(sorted(r4_prefix_ids)).encode()).hexdigest(),
        "canonical_task_trial_mapping": "not reconstructed from outcome-bearing source records",
    }

    r19_doc = load_json(R19)
    r19_units = r19_doc["units"].values()
    r19_source_ids = {
        canon(x["identity"].get("canonical_trial_id"))
        for x in r19_units
        if x.get("status") == "completed" and x.get("identity", {}).get("unit") == "source_episode"
    }
    r19_source_ids.discard(None)
    r19_prefix_units = sum(
        x.get("status") == "completed" and x.get("identity", {}).get("unit") in {
            "recovery_path_extension", "prefix_replay_and_initial_recovery_attempt"
        }
        for x in r19_doc["units"].values()
    )
    groups["R19_completed_source_episodes"] = r19_source_ids

    split_data = {}
    split_trial_sets: dict[str, set[str]] = {}
    candidate_rows: dict[str, list[dict[str, str]]] = {}
    supported_candidate_rows: dict[str, list[dict[str, str]]] = {}
    directory_data = {split: directory_inventory(split) for split in ["train", "valid_seen", "valid_unseen"]}
    valid_seen_trial_ids = directory_data["valid_seen"][1]
    groups["valid_seen_known_excluded"] = groups["heldout_exclusion_union"] & valid_seen_trial_ids
    family_names = {
        "look_at_obj_in_light", "pick_and_place_simple", "pick_clean_then_place_in_recep",
        "pick_cool_then_place_in_recep", "pick_heat_then_place_in_recep", "pick_two_obj_and_place",
    }
    for split in ["train", "valid_seen", "valid_unseen"]:
        task_dirs, trial_ids, task_trial_counts = directory_data[split]
        split_trial_sets[split] = trial_ids
        used_union = set().union(*groups.values())
        exact_used = trial_ids & used_union
        parent_used = {
            x for x in trial_ids
            if x.split("/", 1)[0] in used_union
        }
        used = exact_used | parent_used
        candidates = trial_ids - used
        candidate_rows[split] = hashed_ids(candidates)
        supported = {
            identity for identity in trial_ids
            if identity.split("-", 1)[0] in family_names
            and (DATA / split / identity / "game.tw-pddl").is_file()
        }
        supported_candidates = supported & candidates
        supported_candidate_rows[split] = hashed_ids(supported_candidates)
        membership = {
            name: len(trial_ids & ids) + len({x for x in trial_ids if x.split("/", 1)[0] in ids})
            for name, ids in groups.items()
        }
        split_data[split] = {
            "task_directory_count": len(task_dirs),
            "task_trial_directory_identity_count": len(trial_ids),
            "tasks_without_trial_subdirectories": len(task_dirs - {x.split("/", 1)[0] for x in trial_ids}),
            "known_exact_or_parent_used_excluded_count": len(used),
            "known_identity_group_intersections_counts": membership,
            "known_unlisted_candidate_count": len(candidates),
            "six_family_game_file_present_identity_count": len(supported),
            "six_family_game_file_present_known_use_difference_count": len(supported_candidates),
            "six_family_game_candidate_identity_sha256": hashlib.sha256("\n".join(sorted(supported_candidates)).encode()).hexdigest(),
            "candidate_status": "KNOWN_SET_DIFFERENCE_ONLY__POLLUTION_UNVERIFIED__NOT_CLEAN_HELDOUT",
            "directory_inventory_sha256": hashlib.sha256("\n".join(sorted(trial_ids)).encode()).hexdigest(),
        }

    split_overlap = {
        f"{a}__{b}": len(split_trial_sets[a] & split_trial_sets[b])
        for i, a in enumerate(split_trial_sets)
        for b in list(split_trial_sets)[i + 1:]
    }
    # Candidate identity overlap between splits is explicitly checked, but no outcome data is opened.
    candidate_sets = {s: {x["identity"] for x in candidate_rows[s]} for s in split_data}
    candidate_overlap = {
        f"{a}__{b}": len(candidate_sets[a] & candidate_sets[b])
        for i, a in enumerate(candidate_sets)
        for b in list(candidate_sets)[i + 1:]
    }

    fixed = load_json(FIXED_CASES)
    inventory_doc = load_json(RAW_INVENTORY)
    source_file_hashes = {x["path"]: x.get("sha256") for x in inventory_doc.get("artifacts", [])}
    case_rows = []
    case_identity_counts: Counter[str] = Counter()
    for row in fixed.get("cases", []):
        identity = canon(row.get("canonical_task"))
        if not identity:
            continue
        case_identity_counts[identity] += 1
        split_matches = [s for s, values in split_trial_sets.items() if identity in values]
        memberships = [name for name, values in groups.items() if identity in values]
        source_path = row.get("source_path")
        case_rows.append({
            "case_id": row.get("case_id"),
            "stage": row.get("stage"),
            "prefix_id": row.get("prefix_id"),
            "canonical_task_trial_id": identity,
            "canonical_identity_sha256": hashlib.sha256(identity.encode()).hexdigest(),
            "family": row.get("family"),
            "source_path": source_path,
            "source_file_sha256_from_frozen_P0_inventory": source_file_hashes.get(source_path),
            "source_row_sha256_from_fixed_index": row.get("source_row_sha256"),
            "installed_split_matches": split_matches,
            "known_identity_registrations": memberships,
            "disposition": "HISTORICAL_DEVELOPMENT_LEARNING_CANDIDATE_ONLY__NOT_NEW_EVALUATION__NOT_TRAINING_READY",
        })
    case_duplicate_groups = {identity: count for identity, count in case_identity_counts.items() if count > 1}
    case_isolation = {
        "source_path": str(FIXED_CASES),
        "source_sha256": file_sha(FIXED_CASES),
        "declared_case_count": fixed.get("case_count"),
        "declared_unique_task_count": fixed.get("canonical_task_count"),
        "observed_case_rows": len(case_rows),
        "observed_unique_task_trial_identities": len(case_identity_counts),
        "case_rows": case_rows,
        "same_identity_prefix_groups": case_duplicate_groups,
        "all_duplicate_prefixes_share_one_partition": all(
            len({tuple(x["installed_split_matches"]) for x in case_rows if x["canonical_task_trial_id"] == identity}) <= 1
            for identity in case_duplicate_groups
        ),
        "all_cases_registered_in_known_identity_sets": all(x["known_identity_registrations"] for x in case_rows),
        "selection_status": "fixed audit index only; not a training dataset or permission to select more cases",
    }

    p0_presence = load_json(P0_FILE_PRESENCE)
    p0_comparison = {
        split: {
            "p0_supported_identity_count": p0_presence["splits"][split]["six_family_with_existing_game_file"],
            "recomputed_supported_identity_count": split_data[split]["six_family_game_file_present_identity_count"],
            "p0_known_use_difference_count": p0_presence["splits"][split]["file_presence_candidate_difference_count"],
            "recomputed_known_use_difference_count": split_data[split]["six_family_game_file_present_known_use_difference_count"],
            "supported_candidate_hash_matches_P0": p0_presence["splits"][split]["candidate_ids_hash"] == split_data[split]["six_family_game_candidate_identity_sha256"],
        }
        for split in split_data
    }
    SUPPORTED_OUT.write_text(json.dumps(supported_candidate_rows, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    CASES_OUT.write_text(json.dumps(case_isolation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    CANDIDATES_OUT.write_text(
        json.dumps(candidate_rows, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    result = {
        "audit_kind": "bounded read-only identity/consumed-registration metadata inventory; no task payloads or outcomes read",
        "observed_utc": datetime.now(timezone.utc).isoformat(),
        "repository": {"root": str(ROOT), "branch": "agent/codex-r18c2", "head": "e537f441010077123a307e9d50ea40cf8dad8547"},
        "identity_rule": {
            "canonical_task_trial_id": "normalized relative POSIX path task_directory/trial_directory; schedule task_id values use the same slash form",
            "task_level_exclusion": "if a consumed registration has only task-directory identity, conservatively exclude all trial-directory identities below that task",
            "prefix_rule": "prefixes are not additional task episodes; count by underlying canonical task/trial once where the mapping is present",
        },
        "directory_splits": split_data,
        "candidate_identity_file": {
            "path": str(CANDIDATES_OUT),
            "bytes": CANDIDATES_OUT.stat().st_size,
            "sha256": file_sha(CANDIDATES_OUT),
            "encoding": "compact JSON; per split, identity and SHA-256 of canonical relative task/trial ID",
        },
        "directory_identity_overlap": split_overlap,
        "candidate_identity_overlap": candidate_overlap,
        "identity_groups": {
            name: {"count": len(values), "identity_sha256": hashlib.sha256("\n".join(sorted(values)).encode()).hexdigest()}
            for name, values in groups.items()
        },
        "r4_registration": r4_registration,
        "r14_r19_registration": {
            "R14_completed_source_task_trials": {"count": len(r14_ids), "sha256": hashlib.sha256("\n".join(sorted(r14_ids)).encode()).hexdigest()},
            "R15_R16_R17_prefix_registers": prefix_registrations,
            "R18_C1_C2_prefix_registers": {k: v for k, v in prefix_registrations.items() if k.startswith("R18")},
            "R19_completed_source_episode_ids": {"count": len(r19_source_ids), "sha256": hashlib.sha256("\n".join(sorted(r19_source_ids)).encode()).hexdigest()},
            "R19_other_completed_prefix_or_branch_units_not_added_as_new_source_episodes": r19_prefix_units,
            "R19_unit_status_count": len(r19_doc["units"]),
        },
        "planned_but_not_counted_as_consumed": {
            "sft_recovery_source_schedule_status": load_json(cfg / "recovery/sft_recovery_source_schedule.json").get("status"),
            "persistent_recovery_source_schedule_status": load_json(cfg / "recovery/persistent_recovery_source_schedule.json").get("status"),
            "progress_aware_source_schedule_status": load_json(cfg / "recovery/progress_aware_source_schedule.json").get("status"),
            "reason": "these saved schedules are explicitly frozen_unexecuted; they were not treated as proof of consumption",
        },
        "inputs": inputs,
        "limitations": [
            "Candidate sets are only the difference between installed task/trial directory names and located consumed/exclusion registrations; global contamination is not disproven, so no candidate is called clean or held out.",
            "R4 prefix-only IDs and R16/R17 prefix IDs are not mapped to extra canonical task/trial identities from outcome-bearing files in this task.",
            "R18 C1/C2 run manifests provide prefix counts but no canonical task/trial IDs; exact round-specific mapping remains incomplete.",
            "R19 127 source_episode identities are counted once; its 36 recovery_path_extension and other prefix/branch units are not added as extra source episodes.",
            "No new schedule, argv, experiment, heldout authorization, power claim, or scientific permission is created.",
        ],
        "scope_note": "A broad text search during preparation briefly emitted two already-consumed R16/R17 pair rows including outcome columns. No unconsumed task content was opened or used; those outcome values were not used in this identity analysis. The final audit script reads only directory names and allowlisted metadata/registration JSON.",
        "scientific_execution": False,
        "unconsumed_outcomes_read_by_final_audit": 0,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUT),
        "splits": {k: {q: v[q] for q in ["task_directory_count", "task_trial_directory_identity_count", "known_exact_or_parent_used_excluded_count", "known_unlisted_candidate_count"]} for k, v in split_data.items()},
        "r19_sources": len(r19_source_ids),
        "r19_prefix_branch_units_not_added": r19_prefix_units,
        "directory_overlap": split_overlap,
        "candidate_overlap": candidate_overlap,
        "overall_candidate_cleanliness": "NOT_ESTABLISHED",
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
