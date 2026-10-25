#!/usr/bin/env python3
"""Read-only stdlib recount of prompt occurrences in the saved SFT JSONL."""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


SOURCE = Path(
    "/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/"
    "sft-policy-bootstrap/sft_expert_dataset_balanced.jsonl"
)
SUMMARY = Path("/home/lizening/wt-codex-r18c2/reports/sft_dataset_summary.json")
DATASET_SOURCE = Path("/home/lizening/wt-codex-r18c2/src/sft/dataset.py")
SOL_RESULT = Path(
    "/home/lizening/research-notes/agent-logs/2026-10-25T054106Z__SOL__"
    "self-improvement-phase0__b1c48c/independent_expert_dataset_check.json"
)
OUTPUT = Path(__file__).with_name("prompt_occurrence_recount.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    source_before = sha256_file(SOURCE)
    prompt_rows: Counter[str] = Counter()
    prompt_targets: dict[str, set[tuple[str, str]]] = defaultdict(set)
    prompt_splits: dict[str, set[str]] = defaultdict(set)
    exact_triplets: Counter[str] = Counter()
    rows = 0
    split_rows: Counter[str] = Counter()
    task_ids: dict[str, set[str]] = defaultdict(set)
    field_errors: Counter[str] = Counter()

    with SOURCE.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            record = json.loads(line)
            rows += 1
            prompt_hash = record["prompt_sha256"]
            split = record["dataset_split"]
            prompt_rows[prompt_hash] += 1
            prompt_targets[prompt_hash].add(
                (record["target_action_id"], record["target_command"])
            )
            prompt_splits[prompt_hash].add(split)
            split_rows[split] += 1
            task_ids[split].add(record["task_id"])
            exact_key = json.dumps(
                [record["prompt"], record["completion"], record["target_command"]],
                ensure_ascii=False,
                separators=(",", ":"),
            )
            exact_triplets[hashlib.sha256(exact_key.encode("utf-8")).hexdigest()] += 1
            if hashlib.sha256(record["prompt"].encode("utf-8")).hexdigest() != prompt_hash:
                field_errors["prompt_sha256_mismatch"] += 1
            if record["indexed_action_map"].get(record["target_action_id"]) != record["target_command"]:
                field_errors["action_map_mismatch"] += 1
            if record["completion"].strip() != record["target_action_id"]:
                field_errors["completion_target_mismatch"] += 1

    source_after = sha256_file(SOURCE)
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    sol = json.loads(SOL_RESULT.read_text(encoding="utf-8"))
    duplicate_counts = summary["duplicate_counts"]
    pre_dedup_prompt_occurrences = duplicate_counts["duplicate_prompt_hash_occurrences"]
    exact_rows_removed = duplicate_counts["duplicate_exact_rows_removed"]
    final_prompt_occurrences = sum(count - 1 for count in prompt_rows.values() if count > 1)

    result = {
        "audit_kind": "independent stdlib-only recount of the already-saved final expert JSONL; no project imports or execution",
        "observed_utc": datetime.now(timezone.utc).isoformat(),
        "source_path": str(SOURCE),
        "source_bytes": SOURCE.stat().st_size,
        "source_sha256_before": source_before,
        "source_sha256_after": source_after,
        "source_unchanged_during_recount": source_before == source_after,
        "source_sha256_matches_summary": source_before == summary["dataset_sha256"],
        "row_count": rows,
        "rows_per_split": dict(sorted(split_rows.items())),
        "task_ids_per_split": {key: len(value) for key, value in sorted(task_ids.items())},
        "final_file_prompt_accounting": {
            "repeated_prompt_groups": sum(count > 1 for count in prompt_rows.values()),
            "repeated_prompt_occurrences": final_prompt_occurrences,
            "groups_with_multiple_action_id_or_command_targets": sum(
                len(targets) > 1 for targets in prompt_targets.values()
            ),
            "cross_split_prompt_groups": sum(
                len(splits) > 1 for splits in prompt_splits.values()
            ),
            "exact_triplet_duplicate_occurrences_in_final_file": sum(
                count - 1 for count in exact_triplets.values() if count > 1
            ),
        },
        "producer_summary_accounting": {
            "duplicate_prompt_hash_occurrences": pre_dedup_prompt_occurrences,
            "duplicate_exact_rows_removed": exact_rows_removed,
            "arithmetic_reconciliation": pre_dedup_prompt_occurrences - exact_rows_removed,
            "final_file_prompt_occurrences": final_prompt_occurrences,
            "arithmetic_matches_final_file": (
                pre_dedup_prompt_occurrences - exact_rows_removed
                == final_prompt_occurrences
            ),
            "accepted_example_count": summary["accepted_example_count"],
        },
        "field_errors": dict(field_errors),
        "source_code": {
            "path": str(DATASET_SOURCE),
            "sha256": sha256_file(DATASET_SOURCE),
            "counter_stage": "deduplicate_exact_rows increments prompt_counts before checking exact_hash and before continuing past an exact duplicate (current lines 274-286)",
            "summary_stage": "dataset_summary receives deduplicated rows but carries duplicate_counts computed by deduplicate_exact_rows",
        },
        "producer_summary": {
            "path": str(SUMMARY),
            "sha256": sha256_file(SUMMARY),
            "split_manifest_sha256": summary["split_manifest_sha256"],
            "exclusion_manifest_sha256": summary["exclusion_manifest_sha256"],
        },
        "independent_sol_check": {
            "path": str(SOL_RESULT),
            "sha256": sha256_file(SOL_RESULT),
            "rows": sol["rows"],
            "retained_repeated_prompt_occurrences": sol["retained_repeated_prompt_occurrences"],
            "repeated_prompt_groups": sol["repeated_prompt_groups"],
            "prompt_groups_with_conflicting_targets": sol["prompt_groups_with_conflicting_targets"],
            "field_errors": sol["field_errors"],
        },
        "interpretation": [
            "The producer's 148 prompt-hash occurrences are counted over accepted_rows before exact-row suppression; the count is retained in duplicate_counts and later reported alongside the deduplicated output.",
            "The saved final JSONL independently contains 127 repeated prompt occurrences; 148 - 21 exact-row removals equals 127, matching the source-code accounting convention and the independent Sol recount.",
            "The 110 prompt groups with differing action targets are genuine label multiplicity in the saved rendered-prompt representation, not a hash/map integrity error by itself.",
            "This does not establish whether each differing expert action is behaviorally interchangeable or whether the prompt omits relevant state.",
        ],
        "limits": [
            "No dataset reconstruction, tokenizer/model/environment, project analyzer/validator, pytest, training, or policy replay was run.",
            "Historical split/exclusion binding limitation from the original SI-P0 audit remains unresolved; current saved manifests do not prove which historical manifest bytes were used at original generation time.",
        ],
        "new_scientific_calls": 0,
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["source_unchanged_during_recount"] and result["producer_summary_accounting"]["arithmetic_matches_final_file"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
