#!/usr/bin/env python3
"""Read-only, stdlib-only audit of frozen SFT evidence and records."""
import collections
import hashlib
import json
import pathlib
import sys

PROJECT = pathlib.Path("/home/lizening/Alfworld-Self-Improvement-Project")
WORK = pathlib.Path("/home/lizening/wt-codex-r18c2")
OUT = pathlib.Path("/home/lizening/research-notes/agent-logs/2026-10-25T054106Z__LUNA__sft-raw-evidence-audit__b1c48c")
ART = PROJECT / "artifacts/runtime"


def sha(path):
    h = hashlib.sha256()
    with pathlib.Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def directory_sha(path):
    digest = hashlib.sha256()
    path = pathlib.Path(path)
    for file_path in sorted(item for item in path.rglob("*") if item.is_file()):
        digest.update(str(file_path.relative_to(path)).encode())
        with file_path.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
    return digest.hexdigest()


def read_json(path):
    with pathlib.Path(path).open(encoding="utf-8") as f:
        return json.load(f)


def jsonl(path):
    with pathlib.Path(path).open(encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if line.strip():
                yield n, json.loads(line)


def episode(path, line_no, obj):
    md = obj.get("metadata", {})
    steps = obj.get("steps", [])
    last = steps[-1] if steps else {}
    env = last.get("metadata", {}).get("environment", {}).get("alfworld_info", {})
    won = env.get("won")
    if isinstance(won, list):
        won = won[0] if len(won) == 1 else None
    return {
        "source_file": str(path), "line": line_no,
        "task_id": obj.get("task", {}).get("task_id"),
        "split": obj.get("task", {}).get("split"),
        "family": md.get("task_family"), "nominal_seed": md.get("nominal_seed", obj.get("seed")),
        "schedule_index": md.get("schedule_index"), "reset_order_position": md.get("reset_order_position"),
        "horizon": md.get("max_steps"), "steps": len(steps), "truncated": obj.get("truncated"),
        "termination_reason": md.get("termination_reason"), "terminal_done": last.get("done"),
        "terminal_reward": last.get("reward"), "terminal_won": won,
        "success": won is True, "adapter_loaded": md.get("adapter_loaded"),
        "condition": md.get("condition"), "pipeline_version": md.get("pipeline_version"),
        "model_version": obj.get("model_version"), "trajectory_id": obj.get("trajectory_id"),
        "initial_observation_sha256": hashlib.sha256(obj.get("initial_observation", "").encode()).hexdigest(),
        "reset_sha256": hashlib.sha256(json.dumps(md.get("reset"), sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest(),
        "action_modes": sorted({s.get("metadata", {}).get("action_selection_mode") for s in steps if s.get("metadata", {}).get("action_selection_mode") is not None}),
        "selection_failure_steps": sum(1 for s in steps if s.get("metadata", {}).get("action_selection", {}).get("selection_status") not in (None, "selected")),
        "step_action_valid_false": sum(1 for s in steps if s.get("action_valid") is False),
        "steps_done_true": sum(1 for s in steps if s.get("done") is True),
    }


def load_episodes(rel):
    path = ART / rel
    return [episode(path, n, obj) for n, obj in jsonl(path)]


def summarize(rows):
    families = collections.Counter(r["family"] for r in rows)
    return {
        "n": len(rows), "unique_task_ids": len({r["task_id"] for r in rows}),
        "successes": sum(r["success"] for r in rows), "families": dict(sorted(families.items())),
        "seeds": sorted(r["nominal_seed"] for r in rows),
        "schedule_indices": sorted(r["schedule_index"] for r in rows),
        "truncated": sum(r["truncated"] is True for r in rows),
        "incomplete_or_nonterminal": sum(r["terminal_done"] is not True or r["termination_reason"] not in ("environment_terminal", "selection_failure") for r in rows),
        "selection_failure_episodes": sum(r["termination_reason"] == "selection_failure" for r in rows),
    }


def inventory(paths):
    result = []
    for p in paths:
        p = pathlib.Path(p)
        item = {"path": str(p), "role": "", "historical_identity_source": ""}
        if not p.exists():
            item.update({"status": "MISSING", "status_detail": "not located", "bytes": None, "sha256": None})
        elif p.is_file():
            item.update({"status": "OBSERVED", "status_detail": "present and hashed", "bytes": p.stat().st_size, "sha256": sha(p)})
        else:
            item.update({"status": "DIRECTORY", "bytes": None, "sha256": None})
        result.append(item)
    return result


def main():
    base_rel = "sft-policy-bootstrap/online_evaluation/base_trajectories.jsonl"
    sft_rel = "sft-policy-bootstrap/online_evaluation/sft_trajectories.jsonl"
    unseen_rel = "validation/sft-valid-unseen-g1-20260829T031028Z/trajectories.jsonl"
    base, sft, unseen = load_episodes(base_rel), load_episodes(sft_rel), load_episodes(unseen_rel)
    bootstrap_summary = read_json(PROJECT / "reports/sft_policy_bootstrap_summary.json")
    unseen_summary = read_json(PROJECT / "reports/sft_valid_unseen_summary.json")
    dataset_summary = read_json(PROJECT / "reports/sft_dataset_summary.json")
    protocol_summary = read_json(PROJECT / "reports/sft_heldout_generalization_protocol.json")
    schedules = read_json(PROJECT / "configs/evaluation/sft_heldout_valid_unseen_schedule.json")
    exclusions = read_json(PROJECT / "configs/evaluation/sft_heldout_exclusions.json")
    splits = read_json(PROJECT / "configs/sft/sft_task_splits.json")
    accepted_splits = read_json(PROJECT / "configs/sft/sft_accepted_task_splits.json")
    train_result = read_json(ART / "model-artifacts/sft-policy-bootstrap/full/training_result.json")
    trainer_state = read_json(ART / "model-artifacts/sft-policy-bootstrap/full/checkpoints/checkpoint-2354/trainer_state.json")
    run_config = read_json(PROJECT / "configs/sft/sft_run_config.json")
    train_protocol = read_json(PROJECT / "configs/sft/sft_training_protocol.json")

    def byid(rows):
        return {r["task_id"]: r for r in rows}
    bm, sm, um = byid(base), byid(sft), byid(unseen)
    dev_ids = set(bm) | set(sm)
    bmatched = []
    for task_id in sorted(set(bm) | set(sm)):
        a, b = bm.get(task_id), sm.get(task_id)
        diffs = []
        if a is None or b is None:
            diffs.append("missing_condition_row")
        else:
            for key in ("task_id", "split", "family", "nominal_seed", "schedule_index", "reset_order_position", "horizon", "initial_observation_sha256", "reset_sha256", "pipeline_version", "action_modes"):
                if a.get(key) != b.get(key): diffs.append(key)
        bmatched.append({
            "task_id": task_id, "family": (a or b or {}).get("family"),
            "base_seed": (a or {}).get("nominal_seed"), "sft_seed": (b or {}).get("nominal_seed"),
            "base_schedule_index": (a or {}).get("schedule_index"), "sft_schedule_index": (b or {}).get("schedule_index"),
            "base_pipeline_version": (a or {}).get("pipeline_version"), "sft_pipeline_version": (b or {}).get("pipeline_version"),
            "base_action_modes": (a or {}).get("action_modes"), "sft_action_modes": (b or {}).get("action_modes"),
            "base_success": None if a is None else a["success"], "sft_success": None if b is None else b["success"],
            "base_terminal_won": None if a is None else a["terminal_won"], "sft_terminal_won": None if b is None else b["terminal_won"],
            "base_steps": None if a is None else a["steps"], "sft_steps": None if b is None else b["steps"],
            "base_termination": None if a is None else a["termination_reason"], "sft_termination": None if b is None else b["termination_reason"],
            "pair_mismatch_fields": diffs,
        })
    wins = sum(x["base_success"] is False and x["sft_success"] is True for x in bmatched)
    losses = sum(x["base_success"] is True and x["sft_success"] is False for x in bmatched)
    ties = sum(x["base_success"] == x["sft_success"] for x in bmatched)

    sched_items = schedules.get("episodes", schedules.get("tasks", schedules.get("schedule", [])))
    if isinstance(sched_items, dict): sched_items = sched_items.get("episodes", sched_items.get("tasks", []))
    if not sched_items and isinstance(schedules, list): sched_items = schedules
    sched_map = {x.get("task_id"): x for x in sched_items if isinstance(x, dict) and x.get("task_id")}
    unseen_rows = []
    for tid in sorted(set(um) | set(sched_map)):
        r, q = um.get(tid), sched_map.get(tid)
        mismatches = []
        if r is None: mismatches.append("missing_raw_episode")
        if q is None: mismatches.append("not_in_frozen_schedule")
        if r and q:
            for k, a, b in (("family", r.get("family"), q.get("task_family")), ("nominal_seed", r.get("nominal_seed"), q.get("nominal_seed")), ("schedule_index", r.get("schedule_index"), q.get("schedule_index")), ("horizon", r.get("horizon"), q.get("horizon")), ("split", r.get("split"), q.get("split"))):
                if a != b: mismatches.append(k)
        unseen_rows.append({"task_id":tid,"family":(r or {}).get("family",(q or {}).get("task_family")),"nominal_seed":(r or {}).get("nominal_seed",(q or {}).get("nominal_seed")),"schedule_index":(r or {}).get("schedule_index",(q or {}).get("schedule_index")),"success":None if r is None else r["success"],"terminal_won":None if r is None else r["terminal_won"],"steps":None if r is None else r["steps"],"mismatches":mismatches})

    expert_path = ART / "sft-policy-bootstrap/sft_expert_dataset_balanced.jsonl"
    split_counts = collections.Counter(); task_splits = collections.defaultdict(set); family_tasks=collections.defaultdict(set); source_splits=collections.Counter(); row_count=0; dup_task_step=collections.Counter(); source_sha_counts=collections.Counter(); trajectory_sha_counts=collections.Counter(); targets=collections.Counter(); source_terminal=collections.Counter()
    # Streaming audit only: no rows copied to the report.
    for _, row in jsonl(expert_path):
        row_count += 1
        ds = row.get("dataset_split"); tid = row.get("task_id"); fam = row.get("task_family")
        split_counts[ds] += 1; source_splits[row.get("source_split")] += 1
        if tid is not None: task_splits[tid].add(ds); family_tasks[(ds,fam)].add(tid)
        if row.get("source_traj_data_sha256"): source_sha_counts[row["source_traj_data_sha256"]] += 1
        if row.get("trajectory_sha256"): trajectory_sha_counts[row["trajectory_sha256"]] += 1
        source_terminal[str(row.get("terminal_task_success"))] += 1
        if row.get("target_action_id"): targets[row["target_action_id"]] += 1
        dup_task_step[(tid,row.get("step_index"))] += 1
    dataset_audit = {
        "rows":row_count,"split_rows":dict(split_counts),"source_split_rows":dict(source_splits),
        "unique_tasks":len(task_splits),"task_counts_by_split":dict(collections.Counter(s for tid,ss in task_splits.items() for s in ss)),
        "family_unique_task_counts":{f"{split}/{fam}":len(ids) for (split,fam),ids in sorted(family_tasks.items())},
        "tasks_with_multiple_dataset_splits":sum(len(ss)>1 for ss in task_splits.values()),
        "duplicate_task_step_keys_in_balanced_file":sum(v>1 for v in dup_task_step.values()),
        "distinct_source_traj_data_sha256":len(source_sha_counts),"source_traj_hash_missing_rows":row_count-sum(source_sha_counts.values()),
        "distinct_expert_trajectory_sha256":len(trajectory_sha_counts),"expert_trajectory_hash_missing_rows":row_count-sum(trajectory_sha_counts.values()),
        "terminal_task_success_row_counts":dict(source_terminal),
        "target_action_counts":dict(sorted(targets.items())),
    }

    unbalanced_path = ART / "sft-policy-bootstrap/sft_expert_dataset.jsonl"
    extension_path = ART / "sft-policy-bootstrap/sft_pick_two_extension.jsonl"
    unbalanced_rows=0; unbalanced_tasks=set(); unbalanced_splits=collections.Counter(); unbalanced_dups=collections.Counter()
    for _, row in jsonl(unbalanced_path):
        unbalanced_rows += 1; unbalanced_tasks.add(row.get("task_id")); unbalanced_splits[row.get("dataset_split")] += 1
        unbalanced_dups[(row.get("task_id"),row.get("step_index"))] += 1
    extension_rows=0; extension_tasks=set(); extension_splits=collections.Counter(); extension_dups=collections.Counter(); expected_source_hashes={}
    for _, row in jsonl(extension_path):
        extension_rows += 1; extension_tasks.add(row.get("task_id")); extension_splits[row.get("dataset_split")] += 1
        extension_dups[(row.get("task_id"),row.get("step_index"))] += 1
        expected_source_hashes.setdefault(row.get("task_id"), set()).add((row.get("source_traj_data_sha256"), row.get("source_game_sha256")))
    for _, row in jsonl(unbalanced_path):
        expected_source_hashes.setdefault(row.get("task_id"), set()).add((row.get("source_traj_data_sha256"), row.get("source_game_sha256")))
    unbalanced_audit={"initial_rows":unbalanced_rows,"initial_unique_tasks":len(unbalanced_tasks),"initial_rows_by_split":dict(unbalanced_splits),"initial_duplicate_task_step_keys":sum(v>1 for v in unbalanced_dups.values()),"extension_rows":extension_rows,"extension_unique_tasks":len(extension_tasks),"extension_rows_by_split":dict(extension_splits),"extension_duplicate_task_step_keys":sum(v>1 for v in extension_dups.values()),"initial_extension_task_overlap":len(unbalanced_tasks & extension_tasks),"candidate_union_unique_tasks":len(unbalanced_tasks | extension_tasks),"final_balanced_task_intersection_initial":len(set(task_splits)&unbalanced_tasks),"final_balanced_task_intersection_extension":len(set(task_splits)&extension_tasks),"candidate_union_not_in_final_balanced":len((unbalanced_tasks|extension_tasks)-set(task_splits)),"final_balanced_not_in_candidate_union":len(set(task_splits)-(unbalanced_tasks|extension_tasks))}
    source_raw_checks=[]
    source_root=pathlib.Path("/home/lizening/alfworld_data/json_2.1.1/train")
    for tid, expected in sorted(expected_source_hashes.items()):
        parts=tid.split("/")
        task_dir=source_root.joinpath(*parts)
        traj_file=task_dir/"traj_data.json"; game_file=task_dir/"game.tw-pddl"
        observed=(sha(traj_file) if traj_file.is_file() else None, sha(game_file) if game_file.is_file() else None)
        source_raw_checks.append({"task_id":tid,"expected_hash_pair_count":len(expected),"expected_traj_game_hashes":sorted([list(x) for x in expected]),"traj_data_present":traj_file.is_file(),"game_file_present":game_file.is_file(),"observed_traj_data_sha256":observed[0],"observed_game_sha256":observed[1],"matches_any_expected_pair":observed in expected})
    source_raw_summary={"candidate_task_count":len(source_raw_checks),"traj_data_present":sum(x["traj_data_present"] for x in source_raw_checks),"game_file_present":sum(x["game_file_present"] for x in source_raw_checks),"both_hash_match":sum(x["matches_any_expected_pair"] for x in source_raw_checks),"tasks_with_conflicting_expected_source_hash_pairs":sum(x["expected_hash_pair_count"]!=1 for x in source_raw_checks),"mismatches":[x for x in source_raw_checks if not x["matches_any_expected_pair"]]}

    valid_seen_categories = {k:v for k,v in exclusions.get("categories",{}).items() if "valid_seen" in k or "prior_phase_ab" in k or "prior_recovery" in k}
    # Metadata-only identity inventory; no outcomes for unrun tasks are read.
    def ids_in(value):
        if isinstance(value, list): return [x for x in value if isinstance(x,str)]
        return []
    consumed_valid_seen_ids = sorted(set(i for v in valid_seen_categories.values() for i in ids_in(v)))
    unseen_ids = set(sched_map)

    invpaths = [
        PROJECT/"reports/SFT_POLICY_BOOTSTRAP.md", PROJECT/"reports/SFT_DATASET_AUDIT.md",
        PROJECT/"reports/SFT_VALID_UNSEEN_EVALUATION.md", PROJECT/"reports/SFT_HELDOUT_GENERALIZATION_PROTOCOL.md",
        PROJECT/"reports/sft_policy_bootstrap_summary.json", PROJECT/"reports/sft_dataset_summary.json",
        PROJECT/"reports/sft_valid_unseen_summary.json", PROJECT/"reports/sft_heldout_generalization_protocol.json",
        PROJECT/"configs/sft/sft_run_config.json", PROJECT/"configs/sft/sft_training_protocol.json",
        PROJECT/"configs/sft/sft_task_splits.json", PROJECT/"configs/sft/sft_accepted_task_splits.json",
        PROJECT/"configs/sft/sft_task_exclusions.json", PROJECT/"configs/evaluation/sft_heldout_generalization_protocol.json",
        PROJECT/"configs/sft/sft_dataset_schema.json", PROJECT/"configs/sft/sft_pick_two_balance_extension.json",
        PROJECT/"configs/evaluation/sft_heldout_valid_unseen_schedule.json", PROJECT/"configs/evaluation/sft_heldout_exclusions.json",
        PROJECT/"artifacts/runtime/sft-policy-bootstrap/sft_expert_dataset_balanced.jsonl",
        PROJECT/"artifacts/runtime/sft-policy-bootstrap/sft_expert_dataset.jsonl",
        PROJECT/"artifacts/runtime/sft-policy-bootstrap/sft_pick_two_extension.jsonl",
        PROJECT/"artifacts/runtime/sft-policy-bootstrap/offline_evaluation.json",
        PROJECT/"artifacts/runtime/sft-policy-bootstrap/online_evaluation/base_trajectories.jsonl",
        PROJECT/"artifacts/runtime/sft-policy-bootstrap/online_evaluation/sft_trajectories.jsonl",
        PROJECT/"artifacts/runtime/sft-policy-bootstrap/online_evaluation/summary.json",
        PROJECT/"artifacts/runtime/model-artifacts/sft-policy-bootstrap/full/training_result.json",
        PROJECT/"artifacts/runtime/model-artifacts/sft-policy-bootstrap/full/checkpoints/checkpoint-2354/trainer_state.json",
        PROJECT/"artifacts/runtime/model-artifacts/sft-policy-bootstrap/full/checkpoints/checkpoint-1177/trainer_state.json",
        PROJECT/"artifacts/runtime/model-artifacts/sft-policy-bootstrap/full/final_adapter/adapter_config.json",
        PROJECT/"artifacts/runtime/model-artifacts/sft-policy-bootstrap/full/final_adapter/adapter_model.safetensors",
        PROJECT/"artifacts/runtime/validation/sft-valid-unseen-g1-20260829T031028Z/run_manifest.json",
        PROJECT/"artifacts/runtime/validation/sft-valid-unseen-g1-20260829T031028Z/summary.json",
        PROJECT/"artifacts/runtime/validation/sft-valid-unseen-g1-20260829T031028Z/trajectories.jsonl",
        PROJECT/"artifacts/runtime/validation/sft-recovery-source-pool-r1-20260908T042933Z/trajectories.jsonl",
        PROJECT/"artifacts/runtime/validation/persistent-recovery-source-pool-r7-20260909T000000Z/trajectories.jsonl",
        PROJECT/"artifacts/runtime/validation/sft-recovery-replay-continue-r3-20260908T055308Z/continue_branches.jsonl",
        PROJECT/"artifacts/runtime/validation/persistent-recovery-replay-continue-r9-20260909T033000Z/continue_branches.jsonl",
    ]
    inv = inventory(invpaths)
    for x in inv:
        p=pathlib.Path(x["path"])
        name=p.name
        if "expert_dataset" in name: role="hand-coded expert-derived SFT dataset JSONL"
        elif "trajectories" in name or "branches" in name: role="original per-episode actor/environment trajectory evidence"
        elif "training_result" in name or "trainer_state" in name: role="training receipt/checkpoint-selection state"
        elif "adapter" in str(p): role="adapter metadata/weight bytes; weights not loaded"
        elif "summary" in name or name.startswith("SFT_"): role="versioned report or aggregate summary"
        else: role="frozen protocol/configuration/schedule/exclusion input"
        x["role"]=role
        x["historical_identity_source"]="path+content SHA; cross-referenced to declared historical report/config values; current runtime was not substituted"
    inv.extend([
      {"path":str(ART/"sft-policy-bootstrap/online_evaluation/run_manifest.json"),"status":"MISSING","status_detail":"not located in enumerated SFT artifacts","bytes":None,"sha256":None,"role":"contemporaneous bootstrap evaluation launch/runtime receipt","historical_identity_source":"searched specified SFT artifact directory; no file present"},
      {"path":str(ART/"model-artifacts/sft-policy-bootstrap/full/runtime_manifest.json"),"status":"MISSING","status_detail":"not located in enumerated SFT artifacts","bytes":None,"sha256":None,"role":"contemporaneous training runtime/base/tokenizer identity receipt","historical_identity_source":"no such raw receipt located; adapter_config revision is null"},
      {"path":str(ART/"sft-policy-bootstrap/rejected_candidate_episode_records.jsonl"),"status":"MISSING","status_detail":"not located in enumerated SFT artifacts","bytes":None,"sha256":None,"role":"per-candidate raw records for 596 rejected expert trajectories","historical_identity_source":"aggregate count/reason exists in report; per-candidate raw file not located"},
    ])
    training_protocol_exclusion_sha=train_protocol.get("dataset",{}).get("exclusion_manifest_sha256")
    training_protocol_split_sha=train_protocol.get("dataset",{}).get("split_manifest_sha256")
    actual_split_sha=sha(PROJECT/"configs/sft/sft_task_splits.json")
    actual_exclusion_sha=sha(PROJECT/"configs/sft/sft_task_exclusions.json")

    report = {
      "schema_version":"sft_raw_evidence_audit_v1","status":"PARTIAL_RAW_EVIDENCE_AUDIT",
      "worktree":{"path":str(WORK),"branch":"agent/codex-r18c2","head":"e537f441010077123a307e9d50ea40cf8dad8547","clean_at_start":True},
      "scope":{"execution":"none","project_analyzer_validator_pytest":"not_run","model_environment_training":"not_run","project_runtime_import":"not_run","stdlib_only":True,"source_dataset_rows_streamed":row_count,"unrun_task_outcomes_opened":False},
      "inputs":inv,
      "bootstrap":{
        "base":summarize(base),"sft":summarize(sft),"pair_counts":{"wins_base_fail_sft_success":wins,"losses_base_success_sft_fail":losses,"ties":ties,"pair_rows":len(bmatched)},
        "pair_mismatch_count":sum(bool(r["pair_mismatch_fields"]) for r in bmatched),"pair_rows":bmatched,
        "reported_base_sft_successes":[bootstrap_summary.get("online_evaluation",{}).get("base",{}).get("successes"),bootstrap_summary.get("online_evaluation",{}).get("sft",{}).get("successes")],
        "raw_matches_reported":[sum(r["success"] for r in base)==bootstrap_summary.get("online_evaluation",{}).get("base",{}).get("successes"),sum(r["success"] for r in sft)==bootstrap_summary.get("online_evaluation",{}).get("sft",{}).get("successes")],
        "success_definition":"terminal environment metadata alfworld_info.won is exactly true on final recorded step; generic done/terminal alone is not success",
      },
      "dataset":{"raw_stream_audit_balanced":dataset_audit,"raw_stream_audit_prebalance":unbalanced_audit,"source_file_raw_hash_checks":source_raw_summary,"reported_summary":{k:dataset_summary.get(k) for k in ("accepted_task_count","accepted_example_count","tasks_per_split","examples_per_split","candidate_replay_task_count","candidate_accepted_task_count","candidate_rejected_task_count","duplicate_counts","leakage_checks","dataset_sha256","split_manifest_sha256","accepted_split_manifest_sha256","exclusion_manifest_sha256")},"train_result_summary_sha256":sha(ART/"model-artifacts/sft-policy-bootstrap/full/training_result.json"),"accepted_dataset_id_overlap_with_bootstrap_online":len(set(task_splits)&dev_ids),"accepted_dataset_id_overlap_with_valid_unseen":len(set(task_splits)&unseen_ids),"training_protocol_manifest_binding":{"protocol_declared_split_manifest_sha256":training_protocol_split_sha,"current_sft_task_splits_file_sha256":actual_split_sha,"protocol_declared_exclusion_sha256":training_protocol_exclusion_sha,"current_sft_task_exclusions_file_sha256":actual_exclusion_sha,"split_hash_matches_current_file":training_protocol_split_sha==actual_split_sha,"exclusion_hash_matches_current_file":training_protocol_exclusion_sha==actual_exclusion_sha,"classification":"CONTRADICTED_CURRENT_BINDING" if training_protocol_split_sha!=actual_split_sha or training_protocol_exclusion_sha!=actual_exclusion_sha else "MATCH"}},
      "valid_unseen":{"raw":summarize(unseen),"frozen_schedule_count":len(sched_map),"raw_schedule_join_count":len(unseen_rows),"identity_overlap_with_sft_development":len(set(um)&dev_ids),"schedule_case_rows":unseen_rows,"raw_matches_reported_successes":sum(r["success"] for r in unseen)==unseen_summary.get("primary",{}).get("successes"),"reported_summary_successes":unseen_summary.get("primary",{}).get("successes"),"valid_seen_consumed_identity_count_in_exclusion_categories":len(consumed_valid_seen_ids),"valid_seen_consumed_ids":consumed_valid_seen_ids,"base_arm_status":"no base arm is present in the located valid_unseen G1 artifact directory; this is a one-arm evaluation"},
      "training_identity":{"training_result":{k:train_result.get(k) for k in ("base_model","adapter_path","adapter_sha256","best_checkpoint","best_metric","optimizer_steps","training_loss","wall_time_seconds","dependencies","schema_version")},"checkpoint_state":{"best_model_checkpoint":trainer_state.get("best_model_checkpoint"),"best_metric":trainer_state.get("best_metric"),"best_global_step":trainer_state.get("best_global_step"),"global_step":trainer_state.get("global_step")},"run_config_pretraining_git_revision":run_config.get("pretraining_git_revision"),"training_result_revision_recorded_in_bootstrap":bootstrap_summary.get("provenance",{}).get("training_result_sha256"),"current_adapter_directory_sha256":directory_sha(ART/"model-artifacts/sft-policy-bootstrap/full/final_adapter"),"current_adapter_model_file_sha256":sha(ART/"model-artifacts/sft-policy-bootstrap/full/final_adapter/adapter_model.safetensors"),"base_model_revision":None,"tokenizer_revision":None,"historical_runtime_receipt":None,"adapter_config_revision":read_json(ART/"model-artifacts/sft-policy-bootstrap/full/final_adapter/adapter_config.json").get("revision"),"interpretation":"checkpoint selection and current adapter bytes can be verified against raw training_result/trainer_state; historical base weight/tokenizer commit and exact loaded runtime snapshot lack a contemporaneous receipt; current cache/artifact presence cannot fill that gap"},
      "findings":[
        {"status":"OBSERVED","claim":"Raw bootstrap trajectories contain 60 unique identities per arm, 10 per family; all 60 pairs match task id, split, family, nominal seed, schedule index, reset-order position, horizon, initial observation hash, and reset hash; raw success is 3/60 vs 48/60, with 45 wins, 0 losses, 15 ties.","scope":"episode records and matching fields, not hidden launch/runtime state"},
        {"status":"OBSERVED","claim":"The final base-arm CellPhone episode has one row but termination_reason=selection_failure, only one recorded step, truncated=true, and no terminal won value. It is a recorded failed/invalid episode, not a missing identity; it is not evidence of an unrecorded retry.","scope":"raw trajectory only"},
        {"status":"OBSERVED","claim":"Valid-unseen raw 60 episode rows join one-to-one to all 60 frozen schedule identities; 49 terminal wins, 10 per family, no overlap with the SFT train-development identities or the 1200 accepted dataset tasks.","scope":"valid_unseen frozen schedule and completed raw rows"},
        {"status":"OBSERVED","claim":"The balanced dataset contains 1200 unique tasks/20967 rows; its source train traj_data.json and game.tw-pddl hashes match the raw data files for all 1273 accepted-candidate task IDs across initial and pick-two extension files.","scope":"source file identity/hash only; planner authorship is supported by contemporaneous report labeling, not independently reconstructible from missing rejected-run logs"},
        {"status":"MISSING","claim":"Contemporaneous SFT base-model/tokenizer revision and full loaded runtime identity receipt are unavailable; adapter_config.revision is null.","scope":"cannot prove historical base/tokenizer bytes from current cache"},
        {"status":"MISSING","claim":"A bootstrap online-evaluation launch/run manifest and per-candidate raw records for the 596 rejected trajectories were not located in the enumerated artifact tree.","scope":"report-level aggregate cannot establish hidden attempts or candidate-by-candidate disposition"},
        {"status":"CONTRADICTED","claim":"The versioned sft_training_protocol.json declares split manifest e6695359... and exclusion manifest 8e0d04d3..., while the corresponding currently preserved sft_task_splits.json and sft_task_exclusions.json byte hashes are 53471633... and fdbe3b1c... respectively; the files do not satisfy those declared hashes.","scope":"byte-level current-source binding mismatch; does not by itself establish what files were actually loaded during historical training, and earlier manifest versions were not found"}
      ],
      "provenance_gaps":["No full model-load/runtime receipt or preserved base/tokenizer revision found among the specified raw SFT artifacts; adapter_config.revision is null.","No per-run launch/supervisor receipt found beside bootstrap online trajectories in the enumerated artifact tree; single observed record per schedule identity does not prove there were no discarded/retried attempts.","Raw valid_unseen trajectories and exact 60-row schedule are present; no same-schedule base arm exists, so 49/60 is a one-arm descriptive result, not a causal SFT gain.","Expert task-level outcomes include only accepted dataset rows; 596 rejected-candidate outcomes are summarized by count/reason but underlying per-candidate raw evidence was not found in listed artifacts."],
      "self_improvement_interpretation":{"source":"hand-coded successful expert trajectories, not actor-generated self-sampling","autonomous_self_improvement_proven":False,"strongest_supported_claim":"SFT-P0 expert-policy imitation is associated with a large matched improvement on the same 60 consumed train-development episodes, conditional on historical model identity claims; source audit confirms expert labels, not self-generated experience.","cannot_claim":["autonomous self-improvement","49/60 valid_unseen improvement over base","causal held-out advantage","verified exact historical base/tokenizer runtime revision"],"paper_main_table_risk":"The 48/60 matched development result is a potentially important main-table competence-bootstrap result, but primary reporting should disclose expert imitation and missing historical base/tokenizer/runtime binding; valid_unseen 49/60 should be clearly single-arm descriptive and must not support a paired improvement claim."},
      "trajectory_entrypoints":[
        {"path":str(ART/"sft-policy-bootstrap/online_evaluation/base_trajectories.jsonl"),"role":"consumed train-development base arm; 60 raw episodes"},
        {"path":str(ART/"sft-policy-bootstrap/online_evaluation/sft_trajectories.jsonl"),"role":"consumed train-development SFT arm; 60 raw episodes"},
        {"path":str(ART/"validation/sft-valid-unseen-g1-20260829T031028Z/trajectories.jsonl"),"role":"completed valid_unseen single-arm 60 episode history"},
        {"path":str(ART/"validation/sft-recovery-source-pool-r1-20260908T042933Z/trajectories.jsonl"),"role":"later self-policy source-pool trajectories; entrypoint only, no selection/relabeling"},
        {"path":str(ART/"validation/persistent-recovery-source-pool-r7-20260909T000000Z/trajectories.jsonl"),"role":"later R7 self-policy source trajectories; entrypoint only"},
        {"path":str(ART/"validation/sft-recovery-replay-continue-r3-20260908T055308Z/continue_branches.jsonl"),"role":"R3 continuation branches; entrypoint only"},
        {"path":str(ART/"validation/persistent-recovery-replay-continue-r9-20260909T033000Z/continue_branches.jsonl"),"role":"R9 continuation branches; entrypoint only"},
        {"path":str(ART/"validation/persistent-recovery-pbr-comparison-r11-20260909T000000Z"),"role":"R11 recovery comparison artifact directory; inspect its existing run manifest/summary before any future sampling"},
      ],
      "r19_cost_boundary":{"campaign_total_generations":5142,"campaign_total_environment_operations_including_resets":7949,"historical_predecessor_generations":177,"historical_predecessor_operations":342,"historical_sft_training_cost_included":False},
    }
    (OUT/"sft_raw_evidence_audit.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    (OUT/"raw_artifact_inventory.json").write_text(json.dumps({"schema_version":"raw_artifact_inventory_v1","artifacts":inv},indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    (OUT/"source_hash_case_checks.json").write_text(json.dumps(source_raw_checks,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    (OUT/"case_level_sft_bootstrap.json").write_text(json.dumps(bmatched,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    (OUT/"case_level_valid_unseen.json").write_text(json.dumps(unseen_rows,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"bootstrap_base":summarize(base),"bootstrap_sft":summarize(sft),"paired":{"wins":wins,"losses":losses,"ties":ties,"mismatch":sum(bool(r['pair_mismatch_fields']) for r in bmatched)},"valid_unseen":summarize(unseen),"schedule_rows":len(sched_map),"dataset":dataset_audit,"outputs":[str(OUT/"sft_raw_evidence_audit.json"),str(OUT/"case_level_sft_bootstrap.json"),str(OUT/"case_level_valid_unseen.json")]},indent=2,ensure_ascii=False))


if __name__ == "__main__":
    main()
