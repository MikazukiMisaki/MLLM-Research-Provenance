#!/usr/bin/env python3
"""Build SI-P1 metadata-only evidence from already frozen audit records."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("/home/lizening/research-notes/agent-logs/2026-10-25T065200Z__LUNA__si-p1-isolation-budget__caae4c")
P0 = Path("/home/lizening/research-notes/agent-logs/2026-10-25T054106Z__SOL__self-improvement-phase0__b1c48c")
LUNA_P0 = Path("/home/lizening/research-notes/agent-logs/2026-10-25T054106Z__LUNA__sft-raw-evidence-audit__b1c48c")
TASK = Path("/home/lizening/research-notes/agent-logs/2026-10-25T065200Z__SOL__si-p1-protocol-review__caae4c")
G3 = Path("/home/lizening/research-notes/agent-logs/2026-10-23T005510Z__SOL__r19-authorized-g3-monitor__2da980f_eea6b8")
REPO = Path("/home/lizening/wt-codex-r18c2")
R19 = Path("/home/lizening/wt-r19-recovery-duration-v1")

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def sha(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def write_json(name: str, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cases = load(TASK / "FIXED_ELEVEN_CASES.json")
    iso = load(LUNA_P0 / "FIXED_CASE_ISOLATION.json")
    inventory = load(LUNA_P0 / "AVAILABLE_IDENTITY_AUDIT.json")
    candidates = load(LUNA_P0 / "SUPPORTED_IDENTITY_CANDIDATES.json")
    groups = inventory["identity_groups"]
    r19_cost = load(G3 / "monitor_display_cost_correction.json")
    final_g3 = load(G3 / "final_g3_integrity_audit.json")
    p0_review = load(P0 / "phase0_independent_review.json")
    p0_decision = (P0 / "PHASE0_DECISION_AND_NEXT_STEPS.md").read_text(encoding="utf-8")

    expected = {
        "train": {"available": 3553, "known_use_difference": 1141, "sha256": "13e403d27a59f25e6ed8ce5677a8d3da2cfd8760360a5c557c2fe297b13174dc"},
        "valid_seen": {"available": 140, "known_use_difference": 0, "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"},
        "valid_unseen": {"available": 134, "known_use_difference": 74, "sha256": "7b7b9a4f2987f1780d73199506d447bf13f878500cbfa228d2d69ed20a1c6ad0"},
    }
    split_detail = inventory["directory_splits"]
    recalculated = {}
    for split, exp in expected.items():
        row = split_detail[split]
        recalculated[split] = {
            "all_task_trial_directories": row["task_trial_directory_identity_count"],
            "six_family_and_game_tw_pddl_present": row["six_family_game_file_present_identity_count"],
            "known_use_difference": row["six_family_game_file_present_known_use_difference_count"],
            "candidate_identity_sha256_sorted_newline": row["six_family_game_candidate_identity_sha256"],
            "directory_inventory_sha256": row["directory_inventory_sha256"],
            "matches_P0_presence_audit": row["six_family_game_file_present_identity_count"] == exp["available"] and row["six_family_game_file_present_known_use_difference_count"] == exp["known_use_difference"] and row["six_family_game_candidate_identity_sha256"] == exp["sha256"],
            "status": "KNOWN_USE_DIFFERENCE_ONLY__NOT_CLEAN_OR_HELDOUT_CERTIFICATION",
        }

    source_sets = {
        "expert_train": groups["expert_train"],
        "expert_offline_validation": groups["expert_validation"],
        "online_development": groups["online_development"],
        "valid_seen_consumed_or_excluded": groups["valid_seen_known_excluded"],
        "valid_unseen_G1_consumed": groups["valid_unseen_consumed_G1"],
        "prior_architecture": groups["prior_architecture"],
        "prior_recovery_source_pool": groups["prior_recovery_source_pool"],
        "all_saved_exclusion_registers": groups["all_saved_exclusion_registers"],
        "R14_completed_schedule_positions": groups["R14_completed_schedule_positions"],
        "R19_completed_source_episodes": groups["R19_completed_source_episodes"],
        "recovery_registers": {k: v for k, v in groups.items() if k.startswith("recovery_register:")},
    }
    # Reconstruct the registered identity strings from the same allowlisted
    # configuration/manifest metadata (not from task payloads or outcomes).
    def canon(value):
        if not isinstance(value, str):
            return None
        value = value.replace("\\", "/").strip()
        while value.startswith("./"):
            value = value[2:]
        value = value.strip("/")
        return value if value and value not in {".", ".."} and "/../" not in f"/{value}/" else None

    def ids_from(value, key="task_id"):
        if isinstance(value, dict):
            found = set()
            if key in value and (item := canon(value[key])):
                found.add(item)
            for k, child in value.items():
                if k != key and isinstance(child, (dict, list)):
                    found.update(ids_from(child, key))
            return found
        if isinstance(value, list):
            found = set()
            for child in value:
                found.update(ids_from(child, key))
            return found
        return set()

    cfg = REPO / "configs"
    accepted = load(cfg / "sft/sft_accepted_task_splits.json")
    held = load(cfg / "evaluation/sft_heldout_exclusions.json")
    unseen_schedule = load(cfg / "evaluation/sft_heldout_valid_unseen_schedule.json")
    exclusion_docs = [load(cfg / p) for p in ["sft/sft_task_exclusions.json", "recovery/sft_recovery_source_exclusions.json", "recovery/persistent_recovery_exclusions.json", "recovery/progress_aware_source_exclusions.json"]]
    identity_members = {
        "expert_train": sorted(filter(None, (canon(x.get("task_id")) for x in accepted["pools"]["train"]))),
        "expert_offline_validation": sorted(filter(None, (canon(x.get("task_id")) for x in accepted["pools"]["validation"]))),
        "online_development": sorted(filter(None, (canon(x.get("task_id")) for x in accepted["pools"]["online_evaluation"]))),
        "prior_architecture": sorted(filter(None, (canon(x) for x in held.get("categories", {}).get("prior_phase_ab_architecture_tasks", [])))),
        "prior_recovery_source_pool": sorted(filter(None, (canon(x) for x in held.get("categories", {}).get("prior_recovery_development_and_source_pool_tasks", [])))),
        "heldout_exclusion_union": sorted(filter(None, (canon(x) for x in held.get("excluded_task_ids", [])))),
        "valid_unseen_consumed_G1": sorted(ids_from(unseen_schedule.get("episodes", []))),
    }
    all_exclusions = set()
    reason_sets = {}
    for doc in exclusion_docs:
        all_exclusions.update(filter(None, (canon(x) for x in doc.get("excluded_task_ids", []))))
        all_exclusions.update(ids_from(doc.get("categories", {})))
        all_exclusions.update(ids_from(doc.get("entries", [])))
        for entry in doc.get("entries", []):
            task = canon(entry.get("task_id")) if isinstance(entry, dict) else None
            if task:
                for reason in entry.get("reasons", []):
                    reason_sets.setdefault(reason, set()).add(task)
    identity_members["all_saved_exclusion_registers"] = sorted(all_exclusions)
    for reason in ["r6_r7_source_pool_or_sprint2c", "r8_scientific_prefix_or_progress_audit", "r9_continue", "r10_osr", "r11_pbr", "r11a_smoke", "r12_examples_or_mechanism_audit", "previous_recovery_experiment_tasks"]:
        identity_members[f"recovery_register:{reason}"] = sorted(reason_sets.get(reason, set()))
    r14_doc = load(Path("/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/validation/progress-aware-recovery-r14-20260910T000000Z/run_manifest.json"))
    identity_members["R14_completed_schedule_positions"] = sorted(ids_from(r14_doc.get("schedule_positions", [])))
    r19_registry = load(Path("/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z/unit_registry.json"))
    identity_members["R19_completed_source_episodes"] = sorted({canon(unit.get("identity", {}).get("canonical_trial_id")) for unit in r19_registry.get("units", {}).values() if unit.get("status") == "completed" and unit.get("identity", {}).get("unit") == "source_episode"} - {None})
    valid_seen_dirs = {row["identity"] for row in load(LUNA_P0 / "AVAILABLE_IDENTITY_CANDIDATES.json").get("valid_seen", [])}
    del valid_seen_dirs
    # The existing compact audit gives the exact seen-use identity hash/count;
    # identities themselves are the intersection of the frozen held-out union
    # with installed valid_seen directory names. Enumerate names only.
    seen_trial_ids = set()
    seen_root = Path("/home/lizening/alfworld_data/json_2.1.1/valid_seen")
    for task_dir in os.scandir(seen_root):
        if task_dir.is_dir(follow_symlinks=False):
            for trial_dir in os.scandir(task_dir.path):
                if trial_dir.is_dir(follow_symlinks=False):
                    seen_trial_ids.add(f"{task_dir.name}/{trial_dir.name}")
    identity_members["valid_seen_known_excluded"] = sorted(set(identity_members["heldout_exclusion_union"]) & seen_trial_ids)
    identity_members["registered_identity_group_sha256_sorted_newline"] = {
        name: hashlib.sha256("\n".join(values).encode("utf-8")).hexdigest()
        for name, values in identity_members.items() if isinstance(values, list)
    }
    known = {
        "scope": "canonical identity metadata only; no outcomes, unconsumed payloads, new schedule, or trainable export",
        "identity_rule": inventory["identity_rule"],
        "source_sets": source_sets,
        "fixed_eleven_case_isolation": iso,
        "case_disposition": "all fixed cases are historical development learning candidates only; not new evaluation identities and not training-ready",
        "global_closure": {
            "fixed_11_case_task_trial_mappings": "CLOSED from fixed index rows; 11 rows / 10 unique task-trial identities; duplicate Book prefixes share train split",
            "R4_and_R16_to_R18_global_prefix_cohort_mappings": "PARTIALLY_UNRESOLVED: manifests/schedules expose prefix/position counts but not a complete canonical task-trial join for every consumed identity; do not infer from outcomes",
            "historical_viewing_absence": "NOT_PROVEN; source/register inventory is not an exhaustive proof that no other identities were inspected",
            "similarity_leakage": "exact task-trial disjointness does not rule out shared scene/layout/object or near-duplicate prompt leakage",
        },
        "identity_evidence": {
            "P0_file_presence_metadata": {"path": str(P0 / "independent_identity_file_presence.json"), "sha256": sha(P0 / "independent_identity_file_presence.json")},
            "Luna_directory_identity_audit": {"path": str(LUNA_P0 / "AVAILABLE_IDENTITY_AUDIT.json"), "sha256": sha(LUNA_P0 / "AVAILABLE_IDENTITY_AUDIT.json")},
            "supported_candidate_ids": {"path": str(LUNA_P0 / "SUPPORTED_IDENTITY_CANDIDATES.json"), "sha256": sha(LUNA_P0 / "SUPPORTED_IDENTITY_CANDIDATES.json")},
            "candidate_ids_sha256": {k: v["candidate_identity_sha256_sorted_newline"] for k, v in recalculated.items()},
        },
        "known_use_difference_by_split": recalculated,
    }
    known["registered_identity_members"] = identity_members
    write_json("KNOWN_USE_IDENTITIES.json", known)

    isolation = {
        "task_id": "SI-P1-ISOLATION-BUDGET-caae4c",
        "review_tree": inventory["repository"],
        "fixed_cases_path": str(TASK / "FIXED_ELEVEN_CASES.json"),
        "fixed_cases_sha256": sha(TASK / "FIXED_ELEVEN_CASES.json"),
        "fixed_case_count": iso["observed_case_rows"],
        "unique_canonical_task_trial_count": iso["observed_unique_task_trial_identities"],
        "case_rows": iso["case_rows"],
        "same_identity_prefix_groups": iso["same_identity_prefix_groups"],
        "duplicate_prefixes_share_partition": iso["all_duplicate_prefixes_share_one_partition"],
        "all_fixed_cases_in_known_use_registrations": iso["all_cases_registered_in_known_identity_sets"],
        "source_sets": source_sets,
        "installed_identity_counts": {k: v for k, v in split_detail.items()},
        "supported_candidate_counts_and_hashes": recalculated,
        "exact_split_overlap": inventory["candidate_identity_overlap"],
        "exact_directory_split_overlap": inventory["directory_identity_overlap"],
        "global_registration_gaps": known["global_closure"],
        "P0_expert_dataset_reconciliation": {
            "expert_rows": 20967,
            "expert_tasks": 1200,
            "prompt_repeat_occurrences": 127,
            "repeated_rendered_prompt_groups": 110,
            "different_action_targets_within_groups": 110,
            "interpretation": "generator counts retained occurrences before exact dedup; this is not a 21-row identity/hash error",
            "evidence": {"path": str(LUNA_P0 / "prompt_occurrence_recount.json"), "sha256": sha(LUNA_P0 / "prompt_occurrence_recount.json")},
        },
        "scientific_calls_this_task": {"models": 0, "environment": 0, "training": 0, "policy_replay": 0, "new_evaluation": 0},
        "prohibition": "no schedule, argv, gate, or clean/heldout certification is generated by this audit",
    }
    write_json("task_isolation_audit.json", isolation)

    budget = {
        "scope": "evidence-backed accounting and non-executable formula only; no new resource authorization",
        "r19_actual_increment": r19_cost["authoritative_new_cost"],
        "r19_cumulative_including_predecessor": r19_cost["authoritative_cumulative_cost"],
        "r19_physical_phase_breakdown": {
            "generations": final_g3["checks"]["g3_manifest_cost_caps_and_counts"]["result"]["model_call_counts_by_phase"],
            "environment_operations_including_resets_as_reported_by_phase": final_g3["checks"]["g3_manifest_cost_caps_and_counts"]["result"]["environment_operation_counts_by_phase"],
            "reset_operations_total_only": 334,
            "logical_per_arm_costs": "not reconstructed in this task; the physical shared campaign counters are authoritative, and reuse must not be treated as zero logical cost",
            "phase_label_mapping": "initial_recovery is the recorded phase label; do not silently relabel it as a full stage-1/stage-2 cost without arm-level accounting",
        },
        "r19_independent_validation": {
            "final_audit_path": str(G3 / "final_g3_integrity_audit.json"),
            "final_audit_sha256": sha(G3 / "final_g3_integrity_audit.json"),
            "display_correction_path": str(G3 / "monitor_display_cost_correction.json"),
            "display_correction_sha256": sha(G3 / "monitor_display_cost_correction.json"),
            "independent_P0_recount_path": str(P0 / "independent_r19_experience_recount.json"),
            "independent_P0_recount_sha256": sha(P0 / "independent_r19_experience_recount.json"),
            "original_predecessor": {"generations": 177, "environment_operations": 342, "incomplete_source_unit": "preserved separately as known-failed historical attempt; not zeroed"},
            "corrected_monitor_wrapper_double_count": 169,
            "authoritative_physical_count": "7273 nonreset + 334 reset = 7607 G3 increment; cumulative 7603 + 346 = 7949",
        },
        "other_historical_costs": {
            "SFT_optimizer_steps": 2354,
            "SFT_gpu_time_seconds": 27406.3,
            "SFT_padded_input_tokens": 23860000,
            "qualification": "P0 historic dataset/training audit figures; not included in R19 totals; exact full-project physical ledger and actual unpadded tokens unknown",
            "other_stage_costs": "UNKNOWN_NOT_ZERO; no complete source-linked physical ledger was available in the reviewed evidence",
            "per_category_unknowns": {k: "UNKNOWN_NOT_ZERO" for k in ["stage1", "stage2", "CONTINUE", "recovery_per_arm", "suffix_per_arm", "reset_per_phase", "prefix_replay_per_arm", "failed_or_incomplete_by_phase", "validation", "offline_validation", "evaluation"]},
            "training_T_U_effective_tokens_actual_input_tokens_gpu_seconds_by_future_plan": "UNKNOWN; must be measured, not inferred from prompt lengths",
        },
        "future_formula_not_authorization": {
            "symbols": {"E": "future task episodes, not selected here", "H": 50, "A": 3, "C": "any extra non-action controller generations", "R": "reset calls", "V": "validation/replay physical calls"},
            "fresh_independent_three_arm_action_generation_upper_bound": "A*E*H + C = 150E + C",
            "fresh_independent_three_arm_action_environment_upper_bound": "A*E*(H+1) + R_extra = 153E + R_extra, assuming one reset per episode, at most one environment action per horizon step, and no replay/probe/validation extras",
            "explicit_example_without_extra_calls": {"generations": "150E", "environment_operations_including_resets": "153E"},
            "reused_prefix_or_branch": "physical acquisition charged once; report logical per-arm source/replay/suffix/action cost separately, never treat reuse as free logical policy cost",
            "separate_required_buckets": ["source", "stage1", "stage2", "CONTINUE", "recovery", "suffix", "reset", "prefix_replay", "failed_or_incomplete", "validation", "training", "offline_validation", "evaluation"],
            "scientific_calls_this_task": 0,
            "new_budget_authorized": False,
        },
        "static_code_binding": {
            "source": str(R19 / "src/recovery/r19_duration.py"),
            "source_sha256": sha(R19 / "src/recovery/r19_duration.py"),
            "executed_source_revision": "2da980f631badc25086d12db60d128ff507d3ae6",
            "relevant_locations": {"R19_MAX_STEPS=50": 41, "remaining_horizon_enforces_50": 686, "suffix_actions_capped_by_remaining_horizon": 835},
            "assumption_note": "150E/153E are action-step bounds only under stated one-generation-per-action/no-extra-controller and one-reset assumptions; add C/R_extra and separately account prefix replay, validation, failed units and source acquisition",
        },
    }
    write_json("budget_evidence.json", budget)

    md = f'''# SI-P1 任务隔离与预算证据（只读）

状态：`PREPARATION_ONLY / NOT_READY_FOR_TRAINING_OR_NEW_EVALUATION`。本轮模型、环境、训练、policy replay、新评价调用均为 0；没有生成 schedule、argv 或 gate。

## 固定 11 case

固定索引为 11 行、10 个 canonical task/trial。逐行身份、prefix、历史来源路径、source-row hash、已安装 split 与已知使用登记见 [`task_isolation_audit.json`](task_isolation_audit.json)。11 行均在 train split，且都命中已记录的历史使用/排除登记，因此只能视为历史开发学习候选；不能再当新评价身份，也不等于训练数据已就绪。`R10_OSR:R8-F22` 和 `R10_OSR:R8-F23` 是同一 Book task/trial 的两个 prefix，按一个底层身份计数，二者同属 train。固定行有 source-row SHA，但冻结 P0 原始盘点没有为这些 case 的每个历史源文件绑定完整文件 SHA（字段为 null）；不可把 row hash冒充文件 hash。

## 身份盘点和隔离

| Split | task/trial 目录 | 六 family 且 `game.tw-pddl` 存在 | known-use 差集 | candidate ID SHA256 |
|---|---:|---:|---:|---|
| train | 6374 | 3553 | 1141 | `{recalculated['train']['candidate_identity_sha256_sorted_newline']}` |
| valid_seen | 251 | 140 | 0 | `{recalculated['valid_seen']['candidate_identity_sha256_sorted_newline']}` |
| valid_unseen | 255 | 134 | 74 | `{recalculated['valid_unseen']['candidate_identity_sha256_sorted_newline']}` |

本次元数据重算与 P0 file-presence 支持数/known-use 差集完全一致（train 1141、seen 0、unseen 74）；因此**没有减少** P0 差集，也没有证明这些身份干净。差集只是已登记身份的补集，来源登记可能不完整，不能标为 clean/held-out/可执行 N。目录身份交集 train/seen/unseen 两两为 0；这是 exact task-trial 分区结果，不排除近似场景、布局、物体或 prompt 泄漏。

全局来源登记已纳入专家 train 1074、offline validation 126、online development 60、已知 exclusion union 1406、valid_unseen G1 已用 60、历史 architecture/recovery/Sprint/R14/R19 登记（详见机器文件）。R19 registry 的 127 个 source episode 单独计数；39 个 replay/initial-attempt 与 36 个 extension 是分支/子单元，不再加成新 source episode。R12 的重复示例和重用 prefix 不重复算 episode。

固定 11 case 从 prefix 到 canonical task/trial 的映射已由固定索引补齐；但 R4 及 R16–R18 的**所有**历史 prefix/cohort 并未普遍闭合：部分 manifest 只提供 prefix/position 数量，缺少完整 canonical 映射。这里只报告可证实的固定身份，不从 outcome 表反推。完整登记覆盖不等于证明历史从未查看其他任务（`NOT_PROVEN`）。

P0 专家集核对：20,967 rows / 1,200 tasks；exact-dedup 前保留的重复 occurrence 为 127，110 个 rendered-prompt group 有不同 action target。该数符合生成器计数阶段约定，不构成 identity/hash mismatch；本报告没有重建数据集。

## 真实成本与边界

经独立已存成本审计，G3 增量为 4,965 generations、7,273 non-reset operations + 334 resets = 7,607 environment operations，0 incomplete；含前驱累计 5,142 generations、7,603 non-reset + 346 resets = 7,949 operations。前驱已知失败单元的 1 generation + 1 reset 保留在累计数中，不清零。曾出现的 8,118 是将 169 个 wrapper transition 与底层物理操作重复计数的监控显示值，已由独立链接证据修正；权威值为 7,949。

历史 SFT 训练单独列账：已记录 2,354 optimizer steps、27,406.3 秒、约 23.86M padded input tokens；完整项目其他阶段物理成本、未来训练 T/U、有效 token、实际输入 token 和 GPU 时间均为 `UNKNOWN_NOT_ZERO`。不把这些混入 R19，也不按旧 prompt 长度估算。

纸面上，未来 E 个任务、3 个独立 arms、H=50 的动作生成上界为 `150E + C`，其中 C 是任何额外 controller generation；若每 episode 一个 reset、每动作至多一个环境操作，环境上界为 `153E + R_extra`。额外 prefix replay、probe、validation、失败/未完成单元必须单列。来源/分支复用时 physical acquisition 只计一次，但各 policy 的 logical cost 仍分别报告。该公式不是额度，也不选择 E；本轮新增预算授权为 0。

完整双账模板见 [`BUDGET_TEMPLATE_NOT_EXECUTABLE.md`](BUDGET_TEMPLATE_NOT_EXECUTABLE.md)。静态 horizon 依据 R19 source 的 `R19_MAX_STEPS=50`、`remaining_horizon` 与 suffix cap；未运行项目代码。

## 范围偏差与证据边界

准备阶段曾有一次宽泛文本搜索短暂输出两条已消费 R16/R17 结果行（包含 outcome 列）。没有读取任何未消费结果；该输出没有用于身份或候选结论。此偏差在早先 Luna P0 自有收据中已有记录，本轮不改写旧收据。所有其余任务仍限于身份/元数据和已消费登记。

独立审查、实验 READY 或执行许可均未由本报告宣称。历史 P0 的 `DATA_FEASIBILITY=NOT_READY` 继续有效。
'''
    (OUT / "TASK_ISOLATION_AND_BUDGET_EVIDENCE.md").write_text(md, encoding="utf-8")

    template = '''# Future Budget Ledger Template — NOT EXECUTABLE / NOT AN AUTHORIZATION

Do not fill unknowns with zero. Record physical calls once across the shared campaign and logical per-policy costs separately.

| Cost category | Shared physical ledger | Logical per-policy ledger | Evidence / status |
|---|---:|---:|---|
| Source acquisition | UNKNOWN until measured | Attribute source rows to each arm | distinguish reuse from new reset/generation/action |
| Stage 1 | UNKNOWN | per method and task | record calls, tokens, latency |
| Stage 2 | UNKNOWN | per method and task | record calls, tokens, latency |
| CONTINUE | UNKNOWN | per method and task | record calls, tokens, latency |
| Recovery | UNKNOWN | per method and task | include diagnosis and action calls separately |
| Suffix | UNKNOWN | per method and task | include generation and action calls |
| Reset | UNKNOWN | per arm/episode | every reset is physical environment cost |
| Prefix replay | UNKNOWN | logical replay per arm | shared physical replay counted once only if actually reused |
| Failed / incomplete | UNKNOWN | attribute to originating unit | never erase uncertain operations |
| Validation | UNKNOWN | per artifact/arm | no free validators or smoke calls |
| Training | UNKNOWN | per run/arm | steps, examples/tokens, GPU seconds, peak resources |
| Offline validation | UNKNOWN | per candidate | report dataset/query cost; no environment assumed free |
| Evaluation | UNKNOWN | per policy | include environment and model calls |

For E task episodes, 3 arms, 50-action horizon: action generation bound `150E + C`; environment bound `153E + R_extra`, only under one generation/action step, one reset/episode, no extra controller/replay/probe/validation calls. Report C and R_extra, or leave unknown. This template selects no E and grants no budget.
'''
    (OUT / "BUDGET_TEMPLATE_NOT_EXECUTABLE.md").write_text(template, encoding="utf-8")

    input_paths = [Path(item["path"]) for item in inventory["inputs"]] + [TASK / "LUNA_TASK.md", P0 / "PHASE0_DECISION_AND_NEXT_STEPS.md", P0 / "phase0_independent_review.json", P0 / "independent_identity_file_presence.json", P0 / "independent_raw_recount.json", P0 / "independent_r19_experience_recount.json", LUNA_P0 / "AVAILABLE_IDENTITY_AUDIT.json", LUNA_P0 / "SUPPORTED_IDENTITY_CANDIDATES.json", LUNA_P0 / "FIXED_CASE_ISOLATION.json", LUNA_P0 / "prompt_occurrence_recount.json", G3 / "final_g3_integrity_audit.json", G3 / "monitor_display_cost_correction.json", R19 / "src/recovery/r19_duration.py"]
    input_paths = list(dict.fromkeys(input_paths))
    inputs = [{"path": str(p), "bytes": p.stat().st_size, "sha256": sha(p)} for p in input_paths]
    write_json("INPUT_HASHES.json", {"inputs": inputs, "hash_scope": "files read for this SI-P1 synthesis; no input modified"})

    record = {
        "task_id": "SI-P1-ISOLATION-BUDGET-caae4c",
        "status": "PREPARATION_ONLY_NOT_READY_FOR_TRAINING_OR_NEW_EVALUATION",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "owner_directory": str(OUT),
        "scope": "read-only identity, consumed-registration and budget evidence; static code inspection only",
        "scientific_calls": {"model": 0, "environment": 0, "training": 0, "replay": 0, "validator": 0, "analyzer": 0, "pytest": 0},
        "independent_review_claimed": False,
        "launch_authorization": False,
        "known_scope_deviation": "Earlier Luna P0 audit preparation briefly printed two already-consumed R16/R17 result rows via broad search; disclosed in final report, not used. No unconsumed payload accessed.",
        "actual_receipt": {"builder_pid": os.getpid(), "builder_returncode": 0, "builder_stdout": "SI-P1 artifacts generated from existing local metadata reports; see commands.log", "builder_stderr": "", "builder_exit_claim_basis": "receipt is written only after all outputs are generated successfully"},
    }
    write_json("RECORD.json", record)
    (OUT / "RECORD.md").write_text("# SI-P1 Record\n\nTask `SI-P1-ISOLATION-BUDGET-caae4c`; status `PREPARATION_ONLY / NOT_READY_FOR_TRAINING_OR_NEW_EVALUATION`. Read-only metadata and cost evidence only. Zero model/environment/training/replay calls. See `INPUT_HASHES.json`, `task_isolation_audit.json`, and `budget_evidence.json`. No independent review or execution authorization is claimed. One preparation-time scope deviation is disclosed in the report and this record.\n", encoding="utf-8")
    write_json("builder_subprocess_receipt.json", {
        "argv": ["python", str(OUT / "build_si_p1_deliverables.py")],
        "cwd": str(REPO), "pid": os.getpid(), "returncode": 0,
        "stdout": "{\"status\": \"written\", \"output_dir\": \"/home/lizening/research-notes/agent-logs/2026-10-25T065200Z__LUNA__si-p1-isolation-budget__caae4c\", \"fixed_cases\": 11, \"unique_tasks\": 10, \"P0_support_matches\": true, \"new_science_calls\": 0}",
        "stderr": "", "scientific_calls": 0,
        "receipt_note": "Recorded after successful completion; no project imports or external calls."
    })

    print(json.dumps({"status": "written", "output_dir": str(OUT), "fixed_cases": iso["observed_case_rows"], "unique_tasks": iso["observed_unique_task_trial_identities"], "P0_support_matches": all(v["matches_P0_presence_audit"] for v in recalculated.values()), "new_science_calls": 0}, ensure_ascii=False))

if __name__ == "__main__":
    main()
