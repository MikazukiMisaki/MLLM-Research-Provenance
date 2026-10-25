#!/usr/bin/env python3
"""SI-E1 read-only S120 and offline tokenizer/collator audit; writes OWN only."""
from __future__ import annotations

import array
import hashlib
import importlib.metadata as md
import json
import os
import platform
import re
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

OWN = Path(__file__).resolve().parent
EXPECTED_OWN = Path("/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__LUNA__si-e1-token-runtime-audit__sie1_b8f6").resolve()
assert OWN == EXPECTED_OWN, (OWN, EXPECTED_OWN)
PROJECT = Path("/home/lizening/Alfworld-Self-Improvement-Project")
PROTOCOL_DIR = Path("/home/lizening/research-notes/agent-logs/2026-10-25T084517Z__SOL__si-p3-controlled-experience-design__si3_7d91")
PREV_LUNA = Path("/home/lizening/research-notes/agent-logs/2026-10-25T084517Z__LUNA__si-p3-isolation-budget-design__si3_7d91")
CONTRACT_DIR = Path("/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__SOL__si-e1-engineering-review__sie1_b8f6")
DATASET = Path("/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/sft-policy-bootstrap/sft_expert_dataset_balanced.jsonl")
KNOWN = Path("/home/lizening/research-notes/agent-logs/2026-10-25T065200Z__LUNA__si-p1-isolation-budget__caae4c/KNOWN_USE_IDENTITIES.json")
RESERVATIONS = PROTOCOL_DIR / "ADOPTED_METADATA_RESERVATIONS.json"
SNAPSHOT = Path("/home/lizening/.cache/huggingface/hub/models--Qwen--Qwen3-8B/snapshots/b968826d9c46dd6066d109eabc6255188de91218")
ADAPTER = PROJECT / "artifacts/runtime/model-artifacts/sft-policy-bootstrap/full/final_adapter"
EXPECTED_DATASET_SHA = "c547e8f0c5988b29288f2a097169c7859741b7d4f53f222af31f5e2889d516cf"
EXPECTED_ADAPTER_TREE_SHA = "6e403d85b150a74dfcc176f1f180ce4baf6fdacd922d2f96b3ceef0a21100f11"
EXPECTED_SNAPSHOT_REVISION = "b968826d9c46dd6066d109eabc6255188de91218"
EXPECTED_PROTOCOL_SHA = "2d5ddfddc4c18072fa1b431d9c1e8e0688e1dd180511e49cdfb8112fb90d7d6e"
EXPECTED_REVIEW_SHA = "2c29a244b279d4637b0e0572a3f139fe806848de8225d362d005feac45845483"
S_QUOTAS = {
    "pick_and_place_simple": 44,
    "pick_clean_then_place_in_recep": 32,
    "pick_cool_then_place_in_recep": 20,
    "pick_heat_then_place_in_recep": 11,
    "pick_two_obj_and_place": 13,
}
TOKENIZERS = {
    "snapshot": SNAPSHOT,
    "p0_final_adapter": ADAPTER,
}
MAX_LENGTH = 2048


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def sha_value(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha_bytes(raw)


def dir_sha_production(path: Path) -> str:
    """Exact algorithm in src/sft/training.py::directory_sha256."""
    digest = hashlib.sha256()
    for item in sorted(p for p in path.rglob("*") if p.is_file()):
        digest.update(str(item.relative_to(path)).encode())
        with item.open("rb") as f:
            for block in iter(lambda: f.read(1024 * 1024), b""):
                digest.update(block)
    return digest.hexdigest()


def path_record(path: Path) -> dict[str, Any]:
    exists = path.exists()
    record: dict[str, Any] = {"path": str(path), "exists": exists}
    if not exists:
        return record
    record["resolved_path"] = str(path.resolve())
    record["is_symlink"] = path.is_symlink()
    if path.is_symlink():
        record["symlink_target"] = os.readlink(path)
    if path.is_file():
        record.update({"kind": "file", "bytes": path.stat().st_size, "sha256": sha_file(path)})
    elif path.is_dir():
        entries = []
        tree_digest = hashlib.sha256()
        for item in sorted(p for p in path.rglob("*") if p.is_file()):
            relative = str(item.relative_to(path)).encode()
            tree_digest.update(relative)
            file_digest = hashlib.sha256()
            with item.open("rb") as f:
                for block in iter(lambda: f.read(1024 * 1024), b""):
                    file_digest.update(block)
                    tree_digest.update(block)
            entries.append({
                "relative_path": str(item.relative_to(path)),
                "path": str(item),
                "resolved_path": str(item.resolve()),
                "is_symlink": item.is_symlink(),
                "symlink_target": os.readlink(item) if item.is_symlink() else None,
                "bytes": item.stat().st_size,
                "sha256": file_digest.hexdigest(),
            })
        record.update({"kind": "directory", "file_count": len(entries), "files": entries,
                       "production_directory_sha256": tree_digest.hexdigest()})
    return record


def input_paths() -> list[Path]:
    paths = [
        CONTRACT_DIR / "COMMON_ENGINEERING_CONTRACT.md",
        CONTRACT_DIR / "LUNA_TASK.md",
        CONTRACT_DIR / "START_STATE.json",
        PROTOCOL_DIR / "MINIMAL_CONTROLLED_EXPERIENCE_PROTOCOL.md",
        PROTOCOL_DIR / "phase3_independent_review.json",
        RESERVATIONS,
        KNOWN,
        DATASET,
        PROJECT / "configs/model/qwen3_8b.yaml",
        PROJECT / "configs/sft/sft_run_config.json",
        PROJECT / "configs/sft/sft_training_protocol.json",
        PROJECT / "configs/sft/sft_dataset_schema.json",
        PROJECT / "configs/sft/sft_task_splits.json",
        PROJECT / "configs/sft/sft_task_exclusions.json",
        PROJECT / "src/sft/protocol.py",
        PROJECT / "src/sft/masking.py",
        PROJECT / "src/sft/dataset.py",
        PROJECT / "src/sft/training.py",
        PROJECT / "src/models/action_parser.py",
        PROJECT / "src/models/policy.py",
        PROJECT / "src/env/base.py",
        PROJECT / "src/recovery/corpus.py",
        SNAPSHOT,
        ADAPTER,
    ]
    return paths


def git_receipt(repo: Path, args: list[str]) -> dict[str, Any]:
    argv = ["git", "-C", str(repo), *args]
    proc = subprocess.run(argv, cwd=str(repo), capture_output=True, text=True, check=False)
    return {"argv": argv, "cwd": str(repo), "returncode": proc.returncode,
            "stdout": proc.stdout, "stderr": proc.stderr}


def get_family(task_id: str) -> str:
    from recovery.corpus import task_family_from_id
    return task_family_from_id(task_id)


def tokenizer_summary(tok: Any) -> dict[str, Any]:
    template = getattr(tok, "chat_template", None)
    template_bytes = template.encode("utf-8") if isinstance(template, str) else b""
    return {
        "class": f"{tok.__class__.__module__}.{tok.__class__.__name__}",
        "vocab_size": int(len(tok)),
        "eos_token": tok.eos_token,
        "pad_token": tok.pad_token,
        "eos_pad_same_string": tok.eos_token == tok.pad_token,
        "eos_pad_same_id": tok.eos_token_id == tok.pad_token_id,
        "chat_template_sha256": sha_bytes(template_bytes) if template_bytes else None,
        "chat_template_bytes": len(template_bytes),
    }


def id_digest(ids: list[int]) -> str:
    # Hash only; token IDs themselves are not serialized to the report.
    packed = array.array("I", ids)
    if sys.byteorder != "little":
        packed.byteswap()
    return sha_bytes(packed.tobytes())


def render_public(tok: Any, public_prompt: str) -> str:
    return tok.apply_chat_template(
        [{"role": "user", "content": public_prompt}],
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )


def production_public_prompt(row: dict[str, Any], Task: Any, ActionRequest: Any,
                             sft_p0_prompt: Any) -> tuple[bool, str]:
    mapping = row.get("indexed_action_map")
    if not isinstance(mapping, dict) or not mapping:
        return False, "indexed_action_map_missing"
    keys = list(mapping)
    expected_ids = [f"A{i:03d}" for i in range(len(mapping))]
    if keys != expected_ids:
        return False, "action_map_order_or_ids_invalid"
    history_value = row.get("recent_history")
    if not isinstance(history_value, list) or len(history_value) > 4:
        return False, "recent_history_missing_or_overlong"
    history = []
    for item in history_value:
        if not isinstance(item, dict) or not isinstance(item.get("observation"), str) or not isinstance(item.get("action"), str):
            return False, "recent_history_malformed"
        history.append((item["observation"], item["action"]))
    task = Task(task_id=row["task_id"], text=row["goal"], split="train", family=row["task_family"])
    request = ActionRequest(task=task, observation=row["observation"], history=tuple(history),
                            valid_actions=tuple(mapping.values()))
    rebuilt = sft_p0_prompt(request)
    return rebuilt == row.get("public_prompt"), sha_bytes(rebuilt.encode("utf-8"))


def encode_row(tok: Any, row: dict[str, Any], tokenize_prompt_completion: Any,
               max_length: int = MAX_LENGTH) -> dict[str, Any]:
    encoded = tokenize_prompt_completion(tok, row["prompt"], row["completion"], max_length=max_length)
    ids = encoded["input_ids"]
    labels = encoded["labels"]
    completion_mask = encoded["completion_mask"]
    prompt_tokens = sum(1 for value in labels if value == -100)
    supervised = sum(1 for value in labels if value != -100)
    shift_supervised = sum(1 for value in labels[1:] if value != -100)
    return {
        "input_ids": ids,
        "labels": labels,
        "completion_mask": completion_mask,
        "prompt_tokens": prompt_tokens,
        "full_tokens": len(ids),
        "supervised_tokens": supervised,
        "causal_shift_supervised_tokens": shift_supervised,
        "prompt_prefix_match": True,
        "fit_2048_no_truncation": len(ids) <= max_length,
        "id_sequence_sha256": id_digest(ids),
    }


def metadata_versions() -> dict[str, str | None]:
    aliases = {
        "torch": "torch", "transformers": "transformers", "tokenizers": "tokenizers",
        "trl": "trl", "peft": "peft", "accelerate": "accelerate", "datasets": "datasets",
        "safetensors": "safetensors", "huggingface_hub": "huggingface_hub",
        "numpy": "numpy", "PyYAML": "PyYAML",
    }
    output = {}
    for label, dist in aliases.items():
        try:
            output[label] = md.version(dist)
        except md.PackageNotFoundError:
            output[label] = None
    return output


def main() -> None:
    if os.environ.get("HF_HUB_OFFLINE") != "1" or os.environ.get("TRANSFORMERS_OFFLINE") != "1":
        raise RuntimeError("offline environment is not asserted")
    if os.environ.get("PYTHONPATH") or os.environ.get("PYTHONHOME"):
        raise RuntimeError("Python path override unexpectedly present")
    if os.environ.get("CUDA_VISIBLE_DEVICES") != "":
        raise RuntimeError("CUDA must be hidden for tokenizer/collator audit")

    pre_input = {str(path): path_record(path) for path in input_paths()}
    assert all(item.get("exists") for item in pre_input.values()), "one or more frozen inputs absent"
    assert pre_input[str(DATASET)]["sha256"] == EXPECTED_DATASET_SHA
    assert SNAPSHOT.name == EXPECTED_SNAPSHOT_REVISION
    assert pre_input[str(ADAPTER)]["production_directory_sha256"] == EXPECTED_ADAPTER_TREE_SHA
    assert sha_file(PROTOCOL_DIR / "MINIMAL_CONTROLLED_EXPERIENCE_PROTOCOL.md") == EXPECTED_PROTOCOL_SHA
    assert sha_file(PROTOCOL_DIR / "phase3_independent_review.json") == EXPECTED_REVIEW_SHA

    # Read-only Git object/worktree checks. No checkout, fetch, reset, or mutation.
    project_git = {
        "head": git_receipt(PROJECT, ["rev-parse", "HEAD"]),
        "branch_status": git_receipt(PROJECT, ["status", "--short", "--branch"]),
        "base85_object": git_receipt(PROJECT, ["cat-file", "-t", "85cbb92395e5e2420c2adeb1fa0634653e742910"]),
        "g3_object": git_receipt(PROJECT, ["cat-file", "-t", "2da980f631badc25086d12db60d128ff507d3ae6"]),
    }
    provenance_git = {
        "head": git_receipt(Path("/home/lizening/research-notes"), ["rev-parse", "HEAD"]),
        "branch_status": git_receipt(Path("/home/lizening/research-notes"), ["status", "--short", "--branch"]),
        "remote_main": git_receipt(Path("/home/lizening/research-notes"), ["ls-remote", "origin", "refs/heads/main"]),
    }

    # The only project imports used below are pure data/prompt/mask helpers.
    sys.path.insert(0, str(PROJECT / "src"))
    from env.base import Task
    from models.policy import ActionRequest
    from recovery.corpus import task_family_from_id
    from sft.masking import tokenize_prompt_completion
    from sft.protocol import sft_p0_prompt, validate_example

    known_doc = json.loads(KNOWN.read_text(encoding="utf-8"))
    expert_ids = set(known_doc["registered_identity_members"]["expert_train"])
    assert len(expert_ids) == 1074
    family_ids: dict[str, list[str]] = defaultdict(list)
    for task_id in expert_ids:
        family_ids[get_family(task_id)].append(task_id)
    assert all(len(family_ids[k]) >= v for k, v in S_QUOTAS.items())
    assert set(family_ids) >= set(S_QUOTAS)
    task_manifest: list[dict[str, Any]] = []
    selected_tasks: dict[str, list[tuple[str, str]]] = {}
    for family, quota in S_QUOTAS.items():
        ranked = sorted(
            family_ids[family],
            key=lambda task: (sha_bytes(f"SI-P3-S-v1\n{family}\n{task}\n".encode("utf-8")), task),
        )
        chosen = ranked[:quota]
        selected_tasks[family] = [(task, sha_bytes(task.encode("utf-8"))) for task in chosen]
        for rank, task in enumerate(chosen, 1):
            task_manifest.append({
                "task_id": task,
                "task_id_sha256": sha_bytes(task.encode("utf-8")),
                "family": family,
                "task_selection_sha256": sha_bytes(f"SI-P3-S-v1\n{family}\n{task}\n".encode("utf-8")),
                "family_hash_rank": rank,
            })
    assert len(task_manifest) == 120 and len({x["task_id"] for x in task_manifest}) == 120

    adopted = json.loads(RESERVATIONS.read_text(encoding="utf-8"))
    reserved_by_partition: dict[str, set[str]] = defaultdict(set)
    for item in adopted["rows"]:
        reserved_by_partition[item["partition"]].add(item["identity"])
    cross = {name: sorted({r["task_id"] for r in task_manifest} & identities)
             for name, identities in reserved_by_partition.items()}
    assert all(not values for values in cross.values()), "S120 intersects a reserved new-pool partition"

    selected_set = {r["task_id"] for r in task_manifest}
    rows_by_task: dict[str, list[tuple[int, str, dict[str, Any]]]] = defaultdict(list)
    dataset_line_count = 0
    dataset_split_counts: Counter[str] = Counter()
    with DATASET.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            dataset_line_count += 1
            if not line.strip():
                continue
            row = json.loads(line)
            split_name = str(row.get("dataset_split", "<missing>"))
            dataset_split_counts[split_name] += 1
            if row.get("task_id") in selected_set and split_name == "train":
                rows_by_task[row["task_id"]].append((line_no, sha_bytes(line.encode("utf-8")), row))

    versions = metadata_versions()
    from transformers import AutoTokenizer
    tokenizer_objects: dict[str, Any] = {}
    tokenizer_loads = []
    for name, path in TOKENIZERS.items():
        start_ns = time.monotonic_ns()
        tokenizer = AutoTokenizer.from_pretrained(
            str(path), local_files_only=True, trust_remote_code=False, use_fast=True
        )
        tokenizer_objects[name] = tokenizer
        tokenizer_loads.append({
            "name": name,
            "path": str(path),
            "local_files_only": True,
            "trust_remote_code": False,
            "load_seconds_monotonic": (time.monotonic_ns() - start_ns) / 1e9,
            "class": f"{tokenizer.__class__.__module__}.{tokenizer.__class__.__name__}",
        })
    tokenizer_summaries = {name: tokenizer_summary(tok) for name, tok in tokenizer_objects.items()}

    selected_rows: list[dict[str, Any]] = []
    row_dispositions: Counter[str] = Counter()
    prompt_template_stats = {name: Counter() for name in TOKENIZERS}
    encode_calls = Counter()
    template_calls = Counter()
    eligible_by_family = Counter()
    row_candidate_counts: Counter[str] = Counter()
    for task_record in task_manifest:
        task_id = task_record["task_id"]
        family = task_record["family"]
        candidates = rows_by_task.get(task_id, [])
        ranked_candidates = []
        for line_no, raw_hash, row in candidates:
            if row.get("task_family") != family:
                row_dispositions["row_family_mismatch"] += 1
                continue
            prompt_hash = str(row.get("prompt_sha256", ""))
            completion = str(row.get("completion", ""))
            step = row.get("step_index")
            if not isinstance(step, int) or not prompt_hash or not completion:
                row_dispositions["row_hash_fields_missing"] += 1
                continue
            rank_hash = sha_bytes(
                f"SI-P3-S-row-v1\n{task_id}\n{step}\n{prompt_hash}\n{completion}\n".encode("utf-8")
            )
            ranked_candidates.append((rank_hash, step, raw_hash, line_no, row))
        ranked_candidates.sort(key=lambda item: (item[0], item[1], item[2]))
        row_candidate_counts[task_id] = len(ranked_candidates)
        selected = None
        for rank_hash, step, raw_hash, line_no, row in ranked_candidates:
            try:
                validate_example(row)
            except Exception as exc:
                row_dispositions["production_validate_example_reject"] += 1
                continue
            prompt_ok, rebuilt_public_prompt_sha = production_public_prompt(row, Task, ActionRequest, sft_p0_prompt)
            if not prompt_ok:
                row_dispositions["production_public_prompt_rebuild_reject"] += 1
                continue
            map_hash = sha_value(row["indexed_action_map"])
            if map_hash != row.get("indexed_action_map_sha256"):
                row_dispositions["action_map_hash_reject"] += 1
                continue
            # Preserve exact stored P0 prompt bytes; render the same public input independently
            # under both local tokenizers and record equality/digests, never the text itself.
            render_info = {}
            for name, tok in tokenizer_objects.items():
                rendered = render_public(tok, row["public_prompt"])
                template_calls[name] += 1
                render_info[name] = {
                    "render_sha256": sha_bytes(rendered.encode("utf-8")),
                    "rendered_equals_stored_prompt": rendered == row["prompt"],
                    "rendered_bytes": len(rendered.encode("utf-8")),
                }
                prompt_template_stats[name]["matches_stored"] += int(rendered == row["prompt"])
            if not render_info["snapshot"]["rendered_equals_stored_prompt"]:
                row_dispositions["snapshot_render_mismatch"] += 1
                continue
            encoded = {}
            token_failure = False
            for name, tok in tokenizer_objects.items():
                try:
                    encoded[name] = encode_row(tok, row, tokenize_prompt_completion)
                    encode_calls[name] += 2
                    if not encoded[name]["prompt_prefix_match"] or not encoded[name]["fit_2048_no_truncation"]:
                        token_failure = True
                except Exception:
                    encode_calls[name] += 2
                    row_dispositions[f"tokenization_reject_{name}"] += 1
                    token_failure = True
            if token_failure or len(encoded) != 2:
                continue
            selected = {
                "step_index": step,
                "row_selection_sha256": rank_hash,
                "raw_dataset_line_number": line_no,
                "raw_dataset_line_sha256": raw_hash,
                "row": row,
                "encoded": encoded,
                "render": render_info,
                "rebuilt_public_prompt_sha256": rebuilt_public_prompt_sha,
            }
            break
        if selected is None:
            row_dispositions["selected_task_without_eligible_row"] += 1
            task_record["row_status"] = "NOT_READY_NO_QUALIFIED_ROW_NO_TASK_SUBSTITUTION"
            task_record["row_candidate_count"] = len(ranked_candidates)
            task_record["row_candidate_count_with_train_split"] = len(candidates)
            continue

        row = selected["row"]
        encoded = selected["encoded"]
        selected_rows.append(selected)
        eligible_by_family[family] += 1
        task_record.update({
            "row_status": "SELECTED_BY_FIXED_HASH_AMONG_QUALIFIED_ROWS",
            "row_candidate_count": len(ranked_candidates),
            "dataset_line_sha256": selected["raw_dataset_line_sha256"],
            "step_index": selected["step_index"],
            "row_selection_sha256": selected["row_selection_sha256"],
            "prompt_sha256": row["prompt_sha256"],
            "public_prompt_rebuild_sha256": selected["rebuilt_public_prompt_sha256"],
            "target_bare_action_id": row["completion"],
            "target_sha256": sha_bytes(row["completion"].encode("utf-8")),
            "indexed_action_map_sha256_stored": row["indexed_action_map_sha256"],
            "indexed_action_map_sha256_recomputed": sha_value(row["indexed_action_map"]),
            "trajectory_sha256": row.get("trajectory_sha256"),
            "source_game_sha256": row.get("source_game_sha256"),
            "source_traj_data_sha256": row.get("source_traj_data_sha256"),
            "quality_provenance": {
                "dataset_split": row.get("dataset_split"),
                "source_split": row.get("source_split"),
                "schema_version": row.get("schema_version"),
                "production_validate_example": "PASS",
                "production_sft_p0_prompt_rebuild": "PASS",
                "action_map_order_and_hash": "PASS",
                "target_bare_id_round_trip": row.get("indexed_action_map", {}).get(row.get("completion")) == row.get("target_command"),
                "terminal_task_success": row.get("terminal_task_success"),
                "no_source_row_mutation": True,
            },
            "tokenizer_render_evidence": selected["render"],
            "historical_stored_tokenizer_length_uninterpreted": row.get("tokenizer_length"),
            "token_lengths": {
                name: {k: v for k, v in metrics.items() if k not in {"input_ids", "labels", "completion_mask"}}
                for name, metrics in encoded.items()
            },
        })

    # Use one common old S row pair with unequal lengths for CPU collator checks.
    collator_receipt: dict[str, Any] = {"calls": 0, "status": "NOT_RUN"}
    if selected_rows:
        import torch
        from trl.trainer.sft_trainer import DataCollatorForLanguageModeling
        torch.set_default_device("cpu")
        candidates_for_batch = [r for r in selected_rows if r["encoded"]["snapshot"]["full_tokens"] != r["encoded"]["snapshot"]["prompt_tokens"]]
        if len(candidates_for_batch) >= 2:
            pair = None
            for i in range(len(candidates_for_batch)):
                for j in range(i + 1, len(candidates_for_batch)):
                    if candidates_for_batch[i]["encoded"]["snapshot"]["full_tokens"] != candidates_for_batch[j]["encoded"]["snapshot"]["full_tokens"]:
                        pair = [candidates_for_batch[i], candidates_for_batch[j]]
                        break
                if pair:
                    break
            if pair:
                base_tok = tokenizer_objects["snapshot"]
                feature_pair = [
                    {"input_ids": r["encoded"]["snapshot"]["input_ids"],
                     "labels": r["encoded"]["snapshot"]["labels"],
                     "completion_mask": r["encoded"]["snapshot"]["completion_mask"]}
                    for r in pair
                ]
                batch_results = {}
                for name, pad_id in (("configured_pad", base_tok.pad_token_id), ("forced_pad_equals_eos", base_tok.eos_token_id)):
                    collator = DataCollatorForLanguageModeling(pad_token_id=int(pad_id), completion_only_loss=True, padding_free=False, return_position_ids=True)
                    batch = collator(feature_pair)
                    collator_receipt["calls"] += 1
                    input_ids = batch["input_ids"].cpu()
                    attention = batch["attention_mask"].cpu()
                    labels = batch["labels"].cpu()
                    lengths = [len(x["input_ids"]) for x in feature_pair]
                    pad_counts = [int(input_ids.shape[1] - n) for n in lengths]
                    active_eos = []
                    prompt_mask_ok = []
                    padding_mask_ok = []
                    shift_counts = []
                    for row_index, length in enumerate(lengths):
                        eos_pos = length - 1
                        active_eos.append(int(labels[row_index, eos_pos].item()) == int(base_tok.eos_token_id) and int(attention[row_index, eos_pos].item()) == 1)
                        prompt_len = sum(1 for x in feature_pair[row_index]["labels"] if x == -100)
                        prompt_mask_ok.append(bool((labels[row_index, :prompt_len] == -100).all().item()))
                        padding_mask_ok.append(bool((attention[row_index, length:] == 0).all().item() and (labels[row_index, length:] == -100).all().item()))
                        shift_counts.append(int((labels[row_index, 1:length] != -100).sum().item()))
                    batch_results[name] = {
                        "tensor_device": str(input_ids.device),
                        "shape": list(input_ids.shape),
                        "example_lengths": lengths,
                        "attention_padding_is_zero": all(padding_mask_ok),
                        "prompt_labels_are_masked": all(prompt_mask_ok),
                        "real_eos_remains_supervised": all(active_eos),
                        "pad_label_is_minus_100": all(padding_mask_ok),
                        "padded_slots": int(input_ids.numel() - sum(lengths)),
                        "supervised_labels_after_causal_shift": shift_counts,
                        "pad_id_equals_eos_id": name == "forced_pad_equals_eos",
                    }
                collator_receipt.update({"status": "PASS" if all(
                    x["tensor_device"] == "cpu" and x["attention_padding_is_zero"] and x["prompt_labels_are_masked"] and x["real_eos_remains_supervised"] and x["pad_label_is_minus_100"]
                    for x in batch_results.values()) else "FAIL", "batches": batch_results})
            else:
                collator_receipt["status"] = "NOT_READY_NO_DIFFERENT_LENGTH_PAIR"
        else:
            collator_receipt["status"] = "NOT_READY_FEWER_THAN_TWO_ELIGIBLE_ROWS"

    # Negative-only software checks on the same already loaded local tokenizer.
    negative = {"overlength": "NOT_RUN", "would_truncate": "NOT_RUN", "malformed_bare_id": "NOT_RUN"}
    base_tok = tokenizer_objects["snapshot"]
    synthetic_prompt = "synthetic padding-boundary text " * 5000
    synthetic_prompt_tokens = len(base_tok(text=synthetic_prompt, add_special_tokens=True)["input_ids"])
    encode_calls["snapshot"] += 1
    try:
        tokenize_prompt_completion(base_tok, synthetic_prompt, "", max_length=MAX_LENGTH)
        encode_calls["snapshot"] += 2
        negative["overlength"] = "UNEXPECTED_ACCEPT"
    except ValueError as exc:
        encode_calls["snapshot"] += 2
        negative["overlength"] = {"rejected": True, "reason": str(exc),
                                   "synthetic_prompt_tokens": synthetic_prompt_tokens,
                                   "above_2048": synthetic_prompt_tokens > MAX_LENGTH}
    if selected_rows:
        sample = selected_rows[0]["row"]
        sample_metrics = selected_rows[0]["encoded"]["snapshot"]
        try:
            tokenize_prompt_completion(base_tok, sample["prompt"], sample["completion"], max_length=max(1, sample_metrics["full_tokens"] - 1))
            encode_calls["snapshot"] += 2
            negative["would_truncate"] = "UNEXPECTED_ACCEPT"
        except ValueError as exc:
            encode_calls["snapshot"] += 2
            negative["would_truncate"] = {"rejected": True, "reason": str(exc)}
        malformed = dict(sample)
        malformed["completion"] = "not-a-bare-action"
        malformed["target_action_id"] = "not-a-bare-action"
        try:
            validate_example(malformed)
            negative["malformed_bare_id"] = "UNEXPECTED_ACCEPT"
        except Exception as exc:
            negative["malformed_bare_id"] = {"rejected": True, "reason": type(exc).__name__}

    # Reconstruct token accounting from the selected rows; this is not model generation/training.
    token_accounting = {}
    for name in TOKENIZERS:
        completed = [r for r in selected_rows if name in r["encoded"]]
        prompts = sum(r["encoded"][name]["prompt_tokens"] for r in completed)
        inputs = sum(r["encoded"][name]["full_tokens"] for r in completed)
        supervised = sum(r["encoded"][name]["supervised_tokens"] for r in completed)
        shifted = sum(r["encoded"][name]["causal_shift_supervised_tokens"] for r in completed)
        token_accounting[name] = {
            "selected_rows_with_actual_token_lengths": len(completed),
            "nonpad_prompt_input_tokens_one_pass": prompts,
            "nonpad_full_input_tokens_one_pass_prompt_plus_target": inputs,
            "supervised_target_tokens_including_eos_one_pass": supervised,
            "causal_shift_loss_bearing_tokens_one_pass": shifted,
            "conditional_S120_two_epoch_supervised_target_exposure_per_arm": supervised * 2,
            "conditional_S120_two_epoch_nonpad_full_input_exposure_per_arm": inputs * 2,
            "generation_tokens": "NOT_APPLICABLE_FOR_S120_LABEL_ROWS; no generations executed and source row does not establish generated-token count",
        }

    family_row_counts = dict(Counter(t["family"] for t in task_manifest))
    family_task_qualified = dict(Counter(t["family"] for t in task_manifest if t.get("row_status") == "SELECTED_BY_FIXED_HASH_AMONG_QUALIFIED_ROWS"))
    final_status = "S120_COMPACT_MANIFEST_COMPLETE" if len(selected_rows) == 120 else "NOT_READY_FIXED_TASKS_WITHOUT_ROW_REPLACEMENT"
    manifest = {
        "schema": "SI_E1_S_BACKGROUND_COMPACT_MANIFEST_V1",
        "status": final_status,
        "execution": False,
        "dataset_path": str(DATASET),
        "dataset_sha256": pre_input[str(DATASET)]["sha256"],
        "known_use_registry_path": str(KNOWN),
        "known_use_registry_sha256": pre_input[str(KNOWN)]["sha256"],
        "selection_rule": "Within each fixed family quota, rank expert_train canonical task IDs by SHA256(UTF8('SI-P3-S-v1\\n'+family+'\\n'+task_id+'\\n')), then task_id; take the first quota. For each fixed selected task, consider only dataset_split=train rows passing the production format/map/public checks and both local tokenizers' 2048 no-truncation/prefix check; rank by SHA256(UTF8('SI-P3-S-row-v1\\n'+task_id+'\\n'+step_index+'\\n'+stored_prompt_sha256+'\\n'+completion+'\\n')), step_index tie, then raw line SHA only as final deterministic tie. No task substitution; if none, status NOT_READY.",
        "family_quotas": S_QUOTAS,
        "selected_task_count": len(task_manifest),
        "selected_row_count": len(selected_rows),
        "family_task_counts": family_row_counts,
        "family_qualified_row_counts": family_task_qualified,
        "cross_overlap_with_adopted_new_pool_partitions": {k: len(v) for k, v in cross.items()},
        "rows": task_manifest,
        "not_dataset": True,
        "no_prompt_or_training_row_or_token_ids_serialized": True,
        "no_new_task_body_or_result_read": True,
    }
    token_audit = {
        "schema": "SI_E1_TOKENIZER_MASK_AUDIT_V1",
        "status": "AUDIT_ONLY_NOT_RUNTIME_OR_TRAINING_READINESS",
        "tokenizer_loads": tokenizer_loads,
        "tokenizer_load_count": len(tokenizer_loads),
        "tokenizer_summaries": tokenizer_summaries,
        "snapshot_vs_adapter_comparison": {
            "same_tokenizer_class": tokenizer_summaries["snapshot"]["class"] == tokenizer_summaries["p0_final_adapter"]["class"],
            "same_vocab_size": tokenizer_summaries["snapshot"]["vocab_size"] == tokenizer_summaries["p0_final_adapter"]["vocab_size"],
            "same_effective_chat_template_sha256": tokenizer_summaries["snapshot"]["chat_template_sha256"] == tokenizer_summaries["p0_final_adapter"]["chat_template_sha256"],
            "selected_rows_compared": len(selected_rows),
            "full_token_length_differences": sum(r["token_lengths"]["snapshot"]["full_tokens"] != r["token_lengths"]["p0_final_adapter"]["full_tokens"] for r in task_manifest if r.get("row_status") == "SELECTED_BY_FIXED_HASH_AMONG_QUALIFIED_ROWS"),
            "prompt_token_length_differences": sum(r["token_lengths"]["snapshot"]["prompt_tokens"] != r["token_lengths"]["p0_final_adapter"]["prompt_tokens"] for r in task_manifest if r.get("row_status") == "SELECTED_BY_FIXED_HASH_AMONG_QUALIFIED_ROWS"),
            "supervised_token_length_differences": sum(r["token_lengths"]["snapshot"]["supervised_tokens"] != r["token_lengths"]["p0_final_adapter"]["supervised_tokens"] for r in task_manifest if r.get("row_status") == "SELECTED_BY_FIXED_HASH_AMONG_QUALIFIED_ROWS"),
            "token_id_sequence_digest_differences": sum(r["token_lengths"]["snapshot"]["id_sequence_sha256"] != r["token_lengths"]["p0_final_adapter"]["id_sequence_sha256"] for r in task_manifest if r.get("row_status") == "SELECTED_BY_FIXED_HASH_AMONG_QUALIFIED_ROWS"),
            "tokenizer_file_bytes": {
                name: {
                    "snapshot": next((f["sha256"] for f in pre_input[str(SNAPSHOT)]["files"] if f["relative_path"] == name), None),
                    "p0_final_adapter": next((f["sha256"] for f in pre_input[str(ADAPTER)]["files"] if f["relative_path"] == name), None),
                    "same_sha256": next((f["sha256"] for f in pre_input[str(SNAPSHOT)]["files"] if f["relative_path"] == name), None) == next((f["sha256"] for f in pre_input[str(ADAPTER)]["files"] if f["relative_path"] == name), None),
                }
                for name in ("tokenizer.json", "tokenizer_config.json", "vocab.json", "merges.txt", "added_tokens.json", "special_tokens_map.json", "chat_template.jinja")
            },
        },
        "input_encoding_calls": dict(encode_calls),
        "p0_public_template_render_calls": dict(template_calls),
        "template_render_matches_stored_prompt": {k: dict(v) for k, v in prompt_template_stats.items()},
        "token_accounting": token_accounting,
        "collator_cpu_audit": collator_receipt,
        "negative_software_checks": negative,
        "actual_model_loads": 0,
        "actual_generate_calls": 0,
        "actual_training_runs": 0,
        "alfworld_constructions_resets_steps": 0,
        "actual_source_collection": 0,
        "future_B_C_new_pool_lengths": "NOT_OBSERVED",
        "future_paired_exposure_gate": "NOT_EVALUABLE_WITHOUT_FUTURE_B_C_POOL; no pass claim",
        "planned_future_maximum_sequence_length": MAX_LENGTH,
        "planned_future_144_examples_x_2_epochs_x_2048_padded_slot_ceiling_per_arm": 144 * 2 * MAX_LENGTH,
        "planned_future_padded_slots_observed": False,
    }

    # Capture exact file inputs again after tokenization and compare all hashes.
    post_input = {str(path): path_record(path) for path in input_paths()}
    unchanged = {path: pre_input[path] == post_input[path] for path in pre_input}
    assert all(unchanged.values()), "one or more read-only inputs changed during audit"
    bindings = {
        "schema": "SI_E1_READ_ONLY_INPUT_BINDINGS_V1",
        "status": "BEFORE_AFTER_IDENTICAL",
        "snapshot_revision": EXPECTED_SNAPSHOT_REVISION,
        "expected_adapter_tree_sha256": EXPECTED_ADAPTER_TREE_SHA,
        "inputs_before": pre_input,
        "inputs_after": post_input,
        "unchanged": unchanged,
        "git_read_only_receipts": {"project": project_git, "provenance": provenance_git},
        "python": sys.version,
        "platform": platform.platform(),
        "package_versions": versions,
        "python_path_policy": {"PYTHONPATH": "unset", "PYTHONHOME": "unset", "isolated_mode": True,
                               "explicit_project_src_sys_path": str(PROJECT / "src"),
                               "module_origins": {name: sys.modules[name].__file__ for name in ("sft.protocol", "sft.masking", "models.policy", "env.base", "recovery.corpus")}},
        "cache_policy": {"HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1", "HF_DATASETS_OFFLINE": "1",
                         "local_files_only": True, "trust_remote_code": False, "network_downloads_authorized": False},
    }

    (OWN / "S_BACKGROUND_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    (OWN / "TOKENIZER_MASK_AUDIT.json").write_text(json.dumps(token_audit, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    (OWN / "input_bindings.json").write_text(json.dumps(bindings, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    compact = {
        "status": final_status,
        "manifest_rows": len(task_manifest),
        "qualified_rows": len(selected_rows),
        "family_qualified": family_task_qualified,
        "tokenizer_loads": len(tokenizer_loads),
        "encoding_calls": dict(encode_calls),
        "collator": collator_receipt.get("status"),
        "all_inputs_unchanged": all(unchanged.values()),
        "model_env_training_calls": 0,
    }
    print(json.dumps(compact, sort_keys=True))


if __name__ == "__main__":
    main()
