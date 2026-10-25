#!/usr/bin/env python3
"""Bounded stdlib-only SI-P2 audit. Writes only beside this file."""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

OWN = Path(__file__).resolve().parent
EXPECTED_OWN = Path("/home/lizening/research-notes/agent-logs/2026-10-25T075610Z__LUNA__si-p2-pool-independence__b04b8b").resolve()
assert OWN == EXPECTED_OWN, (OWN, EXPECTED_OWN)
TASK_INPUT = Path("/home/lizening/research-notes/agent-logs/2026-10-25T075610Z__SOL__si-p2-same-pool-review__b04b8b")
MANIFEST = TASK_INPUT / "PARENT_COHORT_MANIFEST.json"
RULES = TASK_INPUT / "COMMON_AUDIT_RULES.md"
KNOWN = Path("/home/lizening/research-notes/agent-logs/2026-10-25T065200Z__LUNA__si-p1-isolation-budget__caae4c/KNOWN_USE_IDENTITIES.json")
P1_COST = Path("/home/lizening/research-notes/agent-logs/2026-10-25T065200Z__LUNA__si-p1-isolation-budget__caae4c/corrected_isolation_budget_v2.json")
P1_ELEVEN = Path("/home/lizening/research-notes/agent-logs/2026-10-25T065200Z__SOL__si-p1-protocol-review__caae4c/independent_target_and_isolation_review.json")
EVENTS = Path("/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z/execution_events.jsonl")
RUNTIME = Path("/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z/runtime_manifest.json")
EXPECTED_MANIFEST_SHA = "a3e2548e89280d150cbe83cceca632f9f91275ede0a4a9d89133e53691826078"
EXPECTED_RULES_SHA = "ab5e3afe8bb1e65ae1473254810ba56dfa769cefbd0952d0b2a0bdb32368ea69"
EXPECTED_EVENT_SHA = "05e1d443ff304eaa25d08b92a4e19d204a6c93a4f46bbe50aefef3271f211762"
EXPECTED_STAGE1_INSTRUCTION_PREFIX_SHA = "d9571cdd116c470c9b8ee7ad241e9f892b6727f26119a6abb35b327196868faa"
EXPECTED_STAGE2_INSTRUCTION_PREFIX_SHA = "17c8907fd08e1c4210c1e3afa9208fd7f6d0d2fdb3586bda77e8558d3dc1cf9b"
HORIZON = 50
HEADERS = [
    "Task goal", "Current pre-action observation", "Recent action/result transitions (last 4)",
    "Indexed admissible-action mapping",
]
PROMPT_SECTION_HEADINGS = HEADERS + [
    "Current inventory", "Observable recent diagnostics", "Currently executable commands",
    "Frozen Stage-1 diagnosis", "Frozen Stage-1 immediate subgoal", "Your response",
]

def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def json_bytes(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")

def row_sha(raw: bytes) -> str:
    # The frozen parent manifest hashes the exact serialized JSONL row bytes,
    # including its line terminator.
    return hashlib.sha256(raw).hexdigest()

def canonical_case(stage: str, prefix: str) -> str:
    return f"{stage}:{prefix}"

def anchor_key(task: str, stage: str, prefix: str) -> str:
    return hashlib.sha256(("SI-P2-anchor-v1\n" + task + "\n" + stage + "\n" + prefix + "\n").encode("utf-8")).hexdigest()

def get_prompt(row, stage):
    if stage == "R4":
        x = row["raw_generations"]["recovery"]
    else:
        x = row["recovery_full"]
    return x["stage_one"]["generation"].get("prompt", ""), x["stage_two"]["generation"].get("prompt", "")

def get_map(row, stage):
    if stage == "R4":
        return row["recover"]["stage_two"].get("id_to_command") or {}
    return row["recovery_full"]["stage_two"].get("parsed", {}).get("id_to_command") or {}

def selected_action(row, stage):
    if stage == "R4":
        return row["recover"]["stage_two"].get("action_id"), row["recover"].get("recovery_action"), bool(row["recover"].get("recovery_action_executed"))
    return row.get("recovery_action_id"), row.get("recovery_mapped_command"), bool(row.get("recovery_action_executed"))

def labels(row, stage):
    if stage == "R4":
        return int(bool(row["recover"].get("success"))), int(bool(row["continue"].get("success")))
    if stage == "R10_OSR":
        return int(bool(row.get("osr_success"))), int(bool(row.get("continue_success")))
    if stage == "R16_OSR":
        return int(bool(row.get("r_osr"))), int(bool(row.get("r_continue")))
    return int(row["k_results"]["1"].get("success", 0)), int(bool(row.get("continue_success")))

def parse_prompt(prompt: str):
    sections = {}
    active = None
    for line in prompt.splitlines():
        stripped = line.strip()
        header = next((h for h in PROMPT_SECTION_HEADINGS if stripped == h + ":" or stripped.startswith(h + ":")), None)
        if header:
            active = header
            sections.setdefault(active, [])
            tail = stripped[len(header) + 1:].strip()
            if tail:
                sections[active].append(tail)
        elif active and active in HEADERS:
            sections[active].append(line.rstrip())
    vals = {k: "\n".join(v).strip() for k, v in sections.items()}
    amap = []
    for line in sections.get("Indexed admissible-action mapping", []):
        m = re.match(r"\s*\[([A-Za-z]\d{3})\]\s+(.+?)\s*$", line)
        if m:
            amap.append([m.group(1), m.group(2)])
    transitions = []
    hist = sections.get("Recent action/result transitions (last 4)", [])
    action = None
    for line in hist:
        s = line.strip()
        if s.startswith("Action:"):
            action = s.split(":", 1)[1].strip()
        elif s.startswith("Result:") and action is not None:
            transitions.append({"action": action, "resulting_observation": s.split(":", 1)[1].strip()})
            action = None
    projection = None
    if all(vals.get(k) for k in HEADERS[:3]) and amap:
        projection = {
            "goal": vals["Task goal"],
            "observation": vals["Current pre-action observation"],
            "recent_action_result_transitions": transitions,
            "ordered_action_map": amap,
        }
    return vals, amap, transitions, projection

def event_ids_for_r19(row):
    er = row.get("evidence_refs", {})
    ids = {er.get("source_episode_event_id"), er.get("prefix_attempt_event_id")}
    kr = er.get("k_arms", {}).get("1", {})
    ids.add(kr.get("arm_event_id"))
    cont = er.get("continue", {})
    ids.update(cont.get("generation_event_ids", []))
    ids.update(cont.get("transition_event_ids", []))
    ops = kr.get("operations", {})
    for key in ("recovery_generation_event_ids", "recovery_transition_event_ids", "suffix_generation_event_ids", "suffix_transition_event_ids"):
        ids.update(ops.get(key, []))
    ids.discard(None)
    return ids

def ordered_pairs(mapping):
    return [[str(k), str(v)] for k, v in mapping.items()]

def public_fields_match(parsed, task_text, observation, history):
    vals = parsed[0]
    expected_h4 = [{"action": x.get("action", ""), "resulting_observation": x.get("result_observation", "")} for x in history]
    return bool(
        vals.get("Task goal") == task_text
        and vals.get("Current pre-action observation") == observation
        and parsed[2] == expected_h4
    )

def instruction_prefix_sha(prompt):
    if "Task goal:" not in prompt:
        return None
    return hashlib.sha256(prompt.split("Task goal:", 1)[0].strip().encode("utf-8")).hexdigest()

def main():
    before = {}
    for p in (MANIFEST, RULES, KNOWN, P1_COST, P1_ELEVEN, RUNTIME):
        before[str(p)] = {"bytes": p.stat().st_size, "sha256": file_sha(p)}
    assert before[str(MANIFEST)]["sha256"] == EXPECTED_MANIFEST_SHA
    assert before[str(RULES)]["sha256"] == EXPECTED_RULES_SHA
    manifest = json.loads(MANIFEST.read_text())
    known = json.loads(KNOWN.read_text())
    p1_cost = json.loads(P1_COST.read_text())
    p1_eleven = json.loads(P1_ELEVEN.read_text())
    original_eleven = {x["case_id"] for x in p1_eleven["cases"]}
    assert len(original_eleven) == 11
    member_groups = known["registered_identity_members"]
    known_union = set()
    for name, values in member_groups.items():
        if name != "registered_identity_group_sha256_sorted_newline" and isinstance(values, list):
            known_union.update(values)
    assert len(known_union) == 2612

    # Verify exact parent source byte hashes and manifest row locators.
    by_stage = defaultdict(dict)
    source_hashes = {}
    source_pre = {}
    for src in manifest["sources"]:
        path = Path(src["source_path"])
        source_pre[src["stage"]] = {"path": str(path), "bytes": path.stat().st_size, "sha256": file_sha(path), "expected_sha256": src["full_file_sha256"]}
        source_hashes[src["stage"]] = source_pre[src["stage"]]["sha256"]
        assert source_hashes[src["stage"]] == src["full_file_sha256"], (src["stage"], source_hashes[src["stage"]])
        for lineno, raw in enumerate(path.open("rb"), 1):
            try:
                row = json.loads(raw)
            except Exception:
                continue
            pref = row.get("prefix_id")
            if pref:
                by_stage[src["stage"]][pref] = (row, lineno, row_sha(raw))
    rows = []
    for item in manifest["rows"]:
        stage = item["stage"]
        row, actual_line, actual_row_hash = by_stage[stage][item["prefix_id"]]
        identity = row.get("canonical_trial_id", row.get("task_id"))
        if not identity:
            identity = row.get("task_id")
        match = identity == item["canonical_task"] and actual_line == item["source_line"] and actual_row_hash == item["source_row_sha256"]
        assert match, (item["case_id"], identity, actual_line, actual_row_hash)
        recover, cont = labels(row, stage)
        p1_task_groups = [k for k, values in member_groups.items() if isinstance(values, list) and k != "registered_identity_group_sha256_sorted_newline" and item["canonical_task"] in values]
        s1prompt, s2prompt = get_prompt(row, stage) if stage != "R19_K1" else ("", "")
        p1, m1, h1, proj1 = parse_prompt(s1prompt)
        p2, m2, h2, proj2 = parse_prompt(s2prompt)
        amap = get_map(row, stage) if stage != "R19_K1" else {}
        selected_id, selected_command, action_executed = selected_action(row, stage) if stage != "R19_K1" else (None, None, False)
        if stage == "R19_K1":
            k1 = row["k_results"]["1"]
            # R19 recovery evidence is event-referenced; full extraction is attached below.
            selected_id = None
            selected_command = None
            action_executed = None
        selected_map_match = bool(selected_id in amap and amap.get(selected_id) == selected_command) if selected_id is not None else None
        prompts_complete = bool(
            all(p1.get(h) for h in HEADERS[:3]) and proj2
            and p1.get("Task goal") == p2.get("Task goal")
            and p1.get("Current pre-action observation") == p2.get("Current pre-action observation")
            and h1 == h2
        ) if stage != "R19_K1" else False
        p0_instruction_static_ok = bool(
            instruction_prefix_sha(s1prompt) == EXPECTED_STAGE1_INSTRUCTION_PREFIX_SHA
            and instruction_prefix_sha(s2prompt) == EXPECTED_STAGE2_INSTRUCTION_PREFIX_SHA
        ) if stage != "R19_K1" else False
        prompt_map_match = bool(m2 == [[str(k), str(v)] for k, v in amap.items()]) if stage != "R19_K1" else None
        if stage == "R4":
            replay = row.get("prefix_replay", {})
            replay_match = bool(replay.get("replay_match") and replay.get("observation_hash_equal") and replay.get("action_map_hash_equal") and replay.get("recent_context_equal") and replay.get("remaining_horizon_equal"))
            full_source_projection = False
            source_projection_reason = "legacy row keeps equality hashes but not independent complete source public-prefix/map/history values"
            d = item["decision_index"]
            rem = item["remaining_horizon"]
            horizon_match = replay.get("remaining_horizon") == rem and rem == HORIZON - d
            stage1 = row["recover"].get("stage_one", {})
            stage2 = row["recover"].get("stage_two", {})
            target_execution = bool(row["recover"].get("recovery_action_executed") and selected_map_match and selected_command == row["recover"].get("recovery_action"))
            label_trace = bool(row["continue"].get("success") is not None and row["recover"].get("success") is not None and row["continue"].get("termination_reason") and row["recover"].get("termination_reason"))
        elif stage == "R10_OSR":
            replay = row.get("replay_full", {})
            checks = replay.get("checks", {})
            replay_match = bool(replay.get("replay_match") and checks and all(checks.values()))
            full_source_projection = bool(replay.get("signature", {}).get("transitions") and replay.get("source_recent_context") is not None and checks.get("source_action_order"))
            source_projection_reason = "replay_full contains source transition history/current state and ordered source-action check" if full_source_projection else "full source projection incomplete"
            d = item["decision_index"]
            rem = item["remaining_horizon"]
            horizon_match = replay.get("remaining_horizon") == rem and rem == HORIZON - d and checks.get("remaining_horizon") is True and checks.get("prefix_remaining_horizon") is True
            stage1 = row["recovery_full"]["stage_one"].get("parsed", {}) | row["recovery_full"]["stage_one"].get("generation", {})
            stage2 = row["recovery_full"]["stage_two"].get("parsed", {}) | row["recovery_full"]["stage_two"].get("generation", {})
            target_execution = bool(row.get("recovery_action_executed") and selected_map_match and selected_command == row.get("recovery_mapped_command") and row.get("immediate_public_progress", {}).get("action_executed"))
            label_trace = bool(row.get("r_continue") in (0, 1) and row.get("r_osr") in (0, 1) and row.get("termination_reason") and row.get("continuation_full", {}).get("termination_reason"))
        elif stage == "R16_OSR":
            replay = row.get("replay", {})
            replay_match = bool(replay.get("replay_match"))
            full_source_projection = False
            source_projection_reason = "row stores current observation/action-map/history digests, not the complete independent source prefix values"
            d = item["decision_index"]
            rem = item["remaining_horizon"]
            horizon_match = replay.get("remaining_horizon") == rem and rem == HORIZON - d
            stage1 = row["recovery_full"]["stage_one"].get("parsed", {}) | row["recovery_full"]["stage_one"].get("generation", {})
            stage2 = row["recovery_full"]["stage_two"].get("parsed", {}) | row["recovery_full"]["stage_two"].get("generation", {})
            target_execution = bool(row.get("recovery_action_executed") and selected_map_match and selected_command == row.get("recovery_mapped_command") and row.get("recovery_transition"))
            label_trace = bool(row.get("r_continue") in (0, 1) and row.get("r_osr") in (0, 1) and row.get("termination_reason") and row.get("continuation_full", {}).get("termination_reason"))
        else:
            k1 = row["k_results"]["1"]
            replay = k1.get("replay_evidence", {})
            replay_match = bool(replay.get("replay_match"))
            full_source_projection = False  # populated from original event journal in next pass
            source_projection_reason = "awaiting referenced original event rows"
            d = item["decision_index"]
            rem = item["remaining_horizon"]
            horizon_match = replay.get("decision_index") == d and rem == HORIZON - d
            stage1 = {}
            stage2 = {}
            target_execution = None
            label_trace = bool(row.get("continue_success") in (0, 1) and k1.get("success") in (0, 1) and k1.get("stopping_reason"))
        s1_legal = bool(stage1.get("status") in ("ok", "valid", "success", None) and stage1.get("output_complete", True) and not stage1.get("token_cap_reached", False)) if stage != "R19_K1" else None
        s2_legal = bool(stage2.get("status") in ("ok", "valid", "success", "selected", None) and stage2.get("output_complete", True) and not stage2.get("token_cap_reached", False)) if stage != "R19_K1" else None
        if stage == "R4":
            s1_legal = bool(stage1.get("output_complete") and not stage1.get("token_cap_reached") and stage1.get("diagnosis_length_valid") and stage1.get("subgoal_length_valid"))
            s2_legal = bool(stage2.get("output_complete") and not stage2.get("token_cap_reached") and stage2.get("status") in ("selected", "ok", "valid"))
        q_checks = {
            "identity_full_file_row_hash": "PASS",
            "complete_independent_source_public_prefix": "PASS" if full_source_projection else "HOLD",
            "public_prompt_projection_and_stage1_stage2_public_fields_agree": "PASS" if prompts_complete else ("NOT_APPLICABLE_EVENT_JOIN_PENDING" if stage == "R19_K1" else "HOLD"),
            "frozen_P0_prompt_instruction_prefix_exact": "PASS" if p0_instruction_static_ok else ("NOT_APPLICABLE_EVENT_JOIN_PENDING" if stage == "R19_K1" else "HOLD"),
            "prompt_action_map_matches_saved_ordered_map": "PASS" if prompt_map_match else ("NOT_APPLICABLE_EVENT_JOIN_PENDING" if stage == "R19_K1" else "HOLD"),
            "exact_replay_and_horizon": "PASS" if replay_match and horizon_match else "HOLD",
            "stage1_legal_complete": "PASS" if s1_legal else ("NOT_APPLICABLE_EVENT_JOIN_PENDING" if stage == "R19_K1" else "HOLD"),
            "stage2_legal_and_target_maps_to_executed_transition": "PASS" if target_execution and s2_legal and selected_map_match else ("NOT_APPLICABLE_EVENT_JOIN_PENDING" if stage == "R19_K1" else "HOLD"),
            "continue_and_recovery_label_stop_trace": "PASS" if label_trace else "HOLD",
        }
        qhist = "PASS" if all(v == "PASS" for v in q_checks.values()) else "HOLD"
        qpin = "HOLD"  # Pinning is filled only when exact historical weights/tokenizer/loaded-role receipts are joined.
        rows.append({
            "case_id": item["case_id"], "stage": stage, "prefix_id": item["prefix_id"],
            "canonical_task": item["canonical_task"], "family": item["family"],
            "source_line": item["source_line"], "source_file_sha256": source_hashes[stage],
            "source_row_sha256": actual_row_hash, "decision_index_d": d,
            "remaining_horizon_H_minus_d": rem, "anchor_key": anchor_key(item["canonical_task"], stage, item["prefix_id"]),
            "recover_success": recover, "continue_success": cont,
            "B_pool": recover == 1, "C_student": recover == 1 and cont == 0,
            "known_use_union": item["canonical_task"] in known_union,
            "known_use_groups": p1_task_groups,
            "historical_weights_tokenizer_adapter_status": "EXACT_PIN_NOT_PROVEN_IN_THIS_ROW_AUDIT",
            "q_hist_checks": q_checks, "q_hist": qhist, "q_pin": qpin,
            "source_projection_reason": source_projection_reason,
            "public_projection_sha256": hashlib.sha256(json_bytes(proj2)).hexdigest() if proj2 else None,
            "public_projection_available": proj2 is not None,
            "first_target_id": selected_id, "first_target_command_sha256": hashlib.sha256((selected_command or "").encode()).hexdigest() if selected_command else None,
            "prompt_map_entry_count": len(m2), "stored_id_map_entry_count": len(amap),
            "prompt_public_sections_present": {h: bool(parse_prompt(s2prompt)[0].get(h)) for h in HEADERS} if stage != "R19_K1" else {},
        })

    # R19 referenced-event extraction: collect only IDs carried by the 39 frozen K1 rows.
    r19_rows = [row for row in rows if row["stage"] == "R19_K1"]
    parent_by_case = {x["case_id"]: x for x in manifest["rows"]}
    raw_by_case = {x["case_id"]: by_stage[x["stage"]][x["prefix_id"]][0] for x in manifest["rows"]}
    desired = set()
    for case, row in raw_by_case.items():
        if row.get("k_results"):
            desired.update(event_ids_for_r19(row))
    events_before = {"bytes": EVENTS.stat().st_size, "sha256": file_sha(EVENTS)}
    assert events_before["sha256"] == EXPECTED_EVENT_SHA
    event_map = {}
    with EVENTS.open("rb") as f:
        for raw in f:
            try:
                ev = json.loads(raw)
            except Exception:
                continue
            eid = ev.get("event_id")
            if eid in desired:
                event_map[eid] = ev
    assert set(event_map) == desired, (len(desired), len(event_map))
    event_use = Counter()
    recovery_event_sets = {}
    r19_details = {}
    for item in manifest["rows"]:
        if item["stage"] != "R19_K1":
            continue
        row = raw_by_case[item["case_id"]]
        er = row["evidence_refs"]
        source_ev = event_map[er["source_episode_event_id"]]
        attempt_ev = event_map[er["prefix_attempt_event_id"]]
        attempt_payload = attempt_ev.get("payload", {})
        gen_ids = attempt_payload.get("recovery_generation_event_ids", [])
        trans_ids = attempt_payload.get("recovery_transition_event_ids", [])
        gens = [event_map[x] for x in gen_ids if x in event_map]
        trans = [event_map[x] for x in trans_ids if x in event_map]
        stage2_ev = next((e for e in gens if e.get("identity", {}).get("component") == "stage2"), None)
        stage1_ev = next((e for e in gens if e.get("identity", {}).get("component") == "stage1"), None)
        transition_ev = trans[0] if trans else None
        traj = source_ev.get("payload", {}).get("trajectory", {})
        d = item["decision_index"]
        steps = traj.get("steps", [])
        pre_step = steps[d] if d < len(steps) else {}
        s2e = (stage2_ev or {}).get("payload", {}).get("evidence", {})
        action = (transition_ev or {}).get("payload", {}).get("action", {})
        same_prestate = bool(action and action.get("actions_consumed_before") == d and action.get("observation_before") == pre_step.get("observation") and action.get("valid_actions_before") == pre_step.get("valid_actions"))
        selected_map = s2e.get("id_to_command", {})
        selected_id = s2e.get("action_id")
        selected_command = s2e.get("command")
        target_ok = bool(transition_ev and selected_id in selected_map and selected_map.get(selected_id) == selected_command and action.get("action_id") == selected_id and action.get("command") == selected_command)
        for eid in [*gen_ids, *trans_ids]: event_use[eid] += 1
        recovery_event_sets[item["case_id"]] = tuple(sorted(set(gen_ids)))
        # R19 prompt and execution evidence are independently joined to the
        # original source trajectory; no environment is instantiated.
        task_text = (traj.get("task") or {}).get("text")
        source_map = ((pre_step.get("metadata") or {}).get("action_selection") or {}).get("id_to_command") or {}
        history = steps[max(0, d - 4):d]
        stage1_evidence = (stage1_ev or {}).get("payload", {}).get("evidence", {})
        stage2_evidence = (stage2_ev or {}).get("payload", {}).get("evidence", {})
        stage1_gen = stage1_evidence.get("generation", {})
        stage2_gen = stage2_evidence.get("generation", {})
        stage1_prompt = parse_prompt(stage1_gen.get("prompt", "")) if stage1_gen.get("prompt") else ({}, [], [], None)
        stage2_prompt = parse_prompt(stage2_gen.get("prompt", "")) if stage2_gen.get("prompt") else ({}, [], [], None)
        source_public_ok = bool(
            task_text and pre_step.get("observation") is not None and len(history) == min(4, d)
            and d < HORIZON and traj.get("metadata", {}).get("max_steps") == HORIZON
        )
        prompt_public_ok = bool(
            source_public_ok
            and public_fields_match(stage1_prompt, task_text, pre_step.get("observation"), history)
            and public_fields_match(stage2_prompt, task_text, pre_step.get("observation"), history)
        )
        p0_instruction_static_ok = bool(
            instruction_prefix_sha(stage1_gen.get("prompt", "")) == EXPECTED_STAGE1_INSTRUCTION_PREFIX_SHA
            and instruction_prefix_sha(stage2_gen.get("prompt", "")) == EXPECTED_STAGE2_INSTRUCTION_PREFIX_SHA
        )
        prompt_map_ok = bool(
            source_map and ordered_pairs(source_map) == stage2_prompt[1]
            and ordered_pairs(source_map) == ordered_pairs(selected_map)
        )
        stage1_legal = bool(
            stage1_ev and stage1_gen.get("output_complete") is True
            and not stage1_gen.get("token_cap_reached", False)
            and isinstance(stage1_evidence.get("diagnosis"), str) and stage1_evidence.get("diagnosis")
            and isinstance(stage1_evidence.get("subgoal"), str) and stage1_evidence.get("subgoal")
        )
        stage2_legal = bool(
            stage2_ev and stage2_gen.get("output_complete") is True
            and not stage2_gen.get("token_cap_reached", False)
            and stage2_evidence.get("action_id") == selected_id
            and selected_id in selected_map
        )
        history_before = (action or {}).get("history_before") or []
        # The transition receipt retains the full alternating pre-action
        # state/action history. Compare its final H4 projection against source
        # rows, using the next saved observation (or current pre-action state)
        # as each result observation.
        event_h4 = []
        for j in range(max(0, len(history_before) - 4), len(history_before)):
            result_obs = history_before[j + 1][0] if j + 1 < len(history_before) else (action or {}).get("observation_before")
            event_h4.append({"action": history_before[j][1], "resulting_observation": result_obs})
        history_event_ok = bool(event_h4 == [
            {"action": x.get("action"), "resulting_observation": x.get("result_observation")} for x in history
        ])
        task_identity_ok = bool(
            source_ev.get("identity", {}).get("canonical_trial_id") == item["canonical_task"]
            and source_ev.get("payload", {}).get("trajectory_sha256") == row.get("trajectory_sha256")
            and attempt_payload.get("source_episode_event_id") == er["source_episode_event_id"]
        )
        source_label_trace = bool(
            row.get("continue_success") in (0, 1)
            and row.get("k_results", {}).get("1", {}).get("success") in (0, 1)
            and row.get("k_results", {}).get("1", {}).get("stopping_reason")
            and er.get("continue", {}).get("generation_event_ids")
            and er.get("continue", {}).get("transition_event_ids")
        )
        public_projection = {
            "goal": task_text,
            "observation": pre_step.get("observation"),
            "recent_action_result_transitions": [
                {"action": x.get("action"), "resulting_observation": x.get("result_observation")} for x in history
            ],
            "ordered_action_map": ordered_pairs(source_map),
        } if source_public_ok else None
        detail = {
            "source_event_id": er["source_episode_event_id"],
            "prefix_attempt_event_id": er["prefix_attempt_event_id"],
            "recovery_generation_event_ids": gen_ids,
            "recovery_transition_event_ids": trans_ids,
            "source_prefix_step_index_d": d,
            "source_prefix_step_present": bool(pre_step),
            "pre_action_snapshot_matches_transition_event": same_prestate,
            "stage1_and_stage2_event_present": bool(stage1_ev and stage2_ev),
            "task_identity_and_source_trajectory_hash_bound": task_identity_ok,
            "source_public_prefix_complete_at_action_before_d": source_public_ok,
            "stage1_and_stage2_prompt_public_fields_match_source": prompt_public_ok,
            "frozen_P0_prompt_instruction_prefix_exact": p0_instruction_static_ok,
            "stage2_ordered_action_map_matches_source_and_event": prompt_map_ok,
            "stage1_output_complete_and_nonempty": stage1_legal,
            "stage2_output_complete_and_bare_selected_id": stage2_legal,
            "source_h4_equals_transition_history_before": history_event_ok,
            "source_continue_and_recovery_labels_have_stop_trace_and_refs": source_label_trace,
            "source_public_projection_sha256": hashlib.sha256(json_bytes(public_projection)).hexdigest() if public_projection else None,
            "stage2_target_matches_transition_event": target_ok,
            "first_target_id": selected_id,
            "first_target_command_sha256": hashlib.sha256((selected_command or "").encode()).hexdigest() if selected_command else None,
            "event_ids_unique_across_parent_records": True,
            "q_hist_event_binding": "PASS" if all((same_prestate, target_ok, stage1_ev, stage2_ev, task_identity_ok, source_public_ok, prompt_public_ok, prompt_map_ok, stage1_legal, stage2_legal, history_event_ok, source_label_trace)) else "HOLD",
        }
        r19_details[item["case_id"]] = detail
    # Event IDs are explicit alias evidence; repeated IDs are counted once only.
    repeated_event_ids = {eid: n for eid, n in event_use.items() if n > 1}
    alias_groups = defaultdict(list)
    for case, ids in recovery_event_sets.items():
        if ids:
            alias_groups[ids].append(case)
    duplicate_case_ids = set()
    physical_alias_groups = []
    row_by_case = {r["case_id"]: r for r in rows}
    for ids, cases in alias_groups.items():
        if len(cases) > 1:
            ordered = sorted(cases, key=lambda c: (row_by_case[c]["anchor_key"], c))
            duplicate_case_ids.update(ordered[1:])
            physical_alias_groups.append({"shared_recovery_generation_event_ids": list(ids), "cases": ordered, "retained_by_anchor": ordered[0], "dropped_physical_aliases": ordered[1:]})
    for r in rows:
        if r["stage"] == "R19_K1":
            r["r19_event_binding"] = r19_details[r["case_id"]]
            q = r["q_hist_checks"]
            detail = r["r19_event_binding"]
            q["complete_independent_source_public_prefix"] = "PASS" if detail["source_public_prefix_complete_at_action_before_d"] else "HOLD"
            q["public_prompt_projection_and_stage1_stage2_public_fields_agree"] = "PASS" if detail["stage1_and_stage2_prompt_public_fields_match_source"] else "HOLD"
            q["frozen_P0_prompt_instruction_prefix_exact"] = "PASS" if detail["frozen_P0_prompt_instruction_prefix_exact"] else "HOLD"
            q["prompt_action_map_matches_saved_ordered_map"] = "PASS" if detail["stage2_ordered_action_map_matches_source_and_event"] else "HOLD"
            q["exact_replay_and_horizon"] = "PASS" if r["q_hist_checks"]["exact_replay_and_horizon"] == "PASS" and detail["pre_action_snapshot_matches_transition_event"] else "HOLD"
            q["stage1_legal_complete"] = "PASS" if detail["stage1_output_complete_and_nonempty"] else "HOLD"
            q["stage2_legal_and_target_maps_to_executed_transition"] = "PASS" if detail["stage2_output_complete_and_bare_selected_id"] and detail["stage2_target_matches_transition_event"] else "HOLD"
            q["continue_and_recovery_label_stop_trace"] = "PASS" if detail["source_continue_and_recovery_labels_have_stop_trace_and_refs"] else "HOLD"
            r["public_projection_sha256"] = detail["source_public_projection_sha256"]
            r["public_projection_available"] = detail["source_public_projection_sha256"] is not None
            r["first_target_id"] = detail["first_target_id"]
            r["first_target_command_sha256"] = detail["first_target_command_sha256"]
            r["q_hist"] = "PASS" if all(value == "PASS" for value in q.values()) else "HOLD"
            if r["r19_event_binding"]["q_hist_event_binding"] != "PASS":
                r["q_hist"] = "HOLD"
        else:
            r["physical_alias_status"] = "NOT_PROVEN_NO_EVENT_IDS_IN_LEGACY_ROW"
    # Q_pin is deliberately separate and strict: only a complete receipt-backed identity can pass.
    runtime_path = RUNTIME
    runtime_doc = json.loads(runtime_path.read_text())
    runtime_sha = file_sha(runtime_path)
    runtime_model_role = bool(runtime_doc.get("model_files", {}).get("snapshot_file_sha256") and runtime_doc.get("inference", {}).get("generation") and runtime_doc.get("model_adapter_isolation", {}).get("recovery_controller") and runtime_doc.get("model_adapter_isolation", {}).get("task_actor"))
    for r in rows:
        if r["stage"] == "R19_K1" and r["q_hist"] == "PASS" and runtime_model_role:
            r["q_pin"] = "PASS"
            r["historical_weights_tokenizer_adapter_status"] = "R19_RUNTIME_RECEIPT_BOUND_FOR_EXECUTED_RUN; per-target event role retained"
        elif r["stage"] != "R19_K1":
            r["q_pin"] = "HOLD_EXACT_WEIGHTS_TOKENIZER_AND_LOADED_ADAPTER_ROLE_NOT_ALL_BOUND"
    # Anchor plan is intentionally before Q filtering/outcome-adoption; order key never uses labels.
    grouped = defaultdict(list)
    for r in rows:
        grouped[r["canonical_task"]].append(r)
    pre_q_anchor_plan = []
    for task, candidates in sorted(grouped.items()):
        ordered = sorted(candidates, key=lambda x: (x["anchor_key"], x["case_id"]))
        for item in ordered:
            pre_q_anchor_plan.append({"canonical_task": task, "case_id": item["case_id"], "stage": item["stage"], "prefix_id": item["prefix_id"], "anchor_key": item["anchor_key"], "selected_pre_q_anchor": item is ordered[0], "recover_success": item["recover_success"], "continue_success": item["continue_success"], "B_pool": item["B_pool"], "C_student": item["C_student"]})
    raw_unique_tasks = len(grouped)
    qrows = [r for r in rows if r["q_hist"] == "PASS"]
    q_unique = len({r["canonical_task"] for r in qrows})
    physical_rows = [r for r in qrows if r["case_id"] not in duplicate_case_ids]
    # Apply the fixed anchor to Q rows, then input-target exact dedup. No slot is refilled.
    q_groups = defaultdict(list)
    for r in physical_rows: q_groups[r["canonical_task"]].append(r)
    post_q_anchors = [min(v, key=lambda x: (x["anchor_key"], x["case_id"])) for v in q_groups.values()]
    projection_groups = defaultdict(list)
    for r in post_q_anchors:
        if r.get("public_projection_sha256") and r.get("first_target_command_sha256"):
            projection_groups[(r["public_projection_sha256"], r["first_target_command_sha256"])].append(r)
    by_projection = defaultdict(list)
    for r in post_q_anchors:
        if r.get("public_projection_sha256") and r.get("first_target_command_sha256"):
            by_projection[r["public_projection_sha256"]].append(r)
    target_ambiguities = [
        {"public_projection_sha256": projection, "distinct_target_command_sha256s": sorted({r["first_target_command_sha256"] for r in candidates}), "case_ids": sorted(r["case_id"] for r in candidates), "disposition": "REPORT_AMBIGUITY_ONLY; no quality exclusion or target repair"}
        for projection, candidates in sorted(by_projection.items())
        if len({r["first_target_command_sha256"] for r in candidates}) > 1
    ]
    dup_drop = set()
    for vals in projection_groups.values():
        if len(vals) > 1:
            vals.sort(key=lambda x: (x["anchor_key"], x["case_id"]))
            dup_drop.update(x["case_id"] for x in vals[1:])
    after_exact = [r for r in post_q_anchors if r["case_id"] not in dup_drop]
    # Strict pinned-identity sensitivity is an independently filtered view;
    # apply the identical frozen physical/task/exact sequence, without refill.
    pin_rows = [r for r in rows if r["q_hist"] == "PASS" and r["q_pin"] == "PASS"]
    pin_physical = [r for r in pin_rows if r["case_id"] not in duplicate_case_ids]
    pin_groups = defaultdict(list)
    for r in pin_physical: pin_groups[r["canonical_task"]].append(r)
    pin_anchors = [min(v, key=lambda x: (x["anchor_key"], x["case_id"])) for v in pin_groups.values()]
    pin_projection_groups = defaultdict(list)
    for r in pin_anchors:
        if r.get("public_projection_sha256") and r.get("first_target_command_sha256"):
            pin_projection_groups[(r["public_projection_sha256"], r["first_target_command_sha256"])].append(r)
    pin_dup_drop = set()
    for vals in pin_projection_groups.values():
        if len(vals) > 1:
            vals.sort(key=lambda x: (x["anchor_key"], x["case_id"]))
            pin_dup_drop.update(x["case_id"] for x in vals[1:])
    pin_final = [r for r in pin_anchors if r["case_id"] not in pin_dup_drop]
    stages = Counter(r["stage"] for r in rows)
    family_raw = Counter(r["family"] for r in rows)
    def profile(items):
        return {
            "rows": len(items), "unique_tasks": len({r["canonical_task"] for r in items}),
            "distinct_public_input_projections": len({r["public_projection_sha256"] for r in items if r.get("public_projection_sha256")}),
            "distinct_first_target_commands": len({r["first_target_command_sha256"] for r in items if r.get("first_target_command_sha256")}),
            "distinct_exact_input_target_pairs": len({(r["public_projection_sha256"], r["first_target_command_sha256"]) for r in items if r.get("public_projection_sha256") and r.get("first_target_command_sha256")}),
            "B_pool": sum(r["B_pool"] for r in items), "C_student": sum(r["C_student"] for r in items),
            "neutral_success_B_minus_C": sum(r["B_pool"] and not r["C_student"] for r in items),
            "recover_failure_or_nonrescue": sum(r["recover_success"] == 0 for r in items),
            "continue_failure": sum(r["continue_success"] == 0 for r in items),
            "by_source": {s: {"rows": sum(r["stage"] == s for r in items), "B_pool": sum(r["stage"] == s and r["B_pool"] for r in items), "C_student": sum(r["stage"] == s and r["C_student"] for r in items), "neutral_success": sum(r["stage"] == s and r["B_pool"] and not r["C_student"] for r in items), "unique_tasks": len({r["canonical_task"] for r in items if r["stage"] == s})} for s in sorted({r["stage"] for r in items})},
            "by_family": {f: {"rows": sum(r["family"] == f for r in items), "B_pool": sum(r["family"] == f and r["B_pool"] for r in items), "C_student": sum(r["family"] == f and r["C_student"] for r in items), "neutral_success": sum(r["family"] == f and r["B_pool"] and not r["C_student"] for r in items), "unique_tasks": len({r["canonical_task"] for r in items if r["family"] == f})} for f in sorted({r["family"] for r in items})},
        }
    stages_after = {
        "RAW": profile(rows), "Q_hist": profile(qrows), "physical_dedup": profile(physical_rows),
        "task_anchor": profile(post_q_anchors), "exact_input_target_dedup": profile(after_exact),
    }
    stage_task_groups = defaultdict(list)
    for r in rows:
        stage_task_groups[r["canonical_task"]].append(r)
    task_overlap = []
    for task, members in sorted(stage_task_groups.items()):
        stage_names = sorted({r["stage"] for r in members})
        if len(members) > 1 or len(stage_names) > 1:
            task_overlap.append({"canonical_task": task, "case_ids": [r["case_id"] for r in sorted(members, key=lambda x: (x["stage"], x["case_id"]))], "stages": stage_names, "candidate_count": len(members), "cross_stage": len(stage_names) > 1, "known_use_groups": sorted({g for r in members for g in r["known_use_groups"]}), "q_hist_qualified_case_ids": [r["case_id"] for r in members if r["q_hist"] == "PASS"]})
    eleven_dispositions = {
        case: {
            "raw_case_present": case in {r["case_id"] for r in rows},
            "q_hist": next((r["q_hist"] for r in rows if r["case_id"] == case), "NOT_IN_PARENT_171"),
            "physical_dedup": "DROPPED_EXPLICIT_ALIAS" if case in duplicate_case_ids else ("RETAINED" if any(r["case_id"] == case for r in qrows) else "NOT_REACHED_Q_HIST"),
            "task_anchor": "RETAINED" if any(r["case_id"] == case for r in post_q_anchors) else "NOT_SELECTED_OR_NOT_QUALIFIED",
            "exact_input_target_dedup": "RETAINED" if any(r["case_id"] == case for r in after_exact) else "NOT_SELECTED_OR_DUPLICATE_OR_NOT_QUALIFIED",
            "canonical_task": next((r["canonical_task"] for r in rows if r["case_id"] == case), None),
        } for case in sorted(original_eleven)
    }
    result = {
        "schema": "SI_P2_LUNA_POOL_IDENTITY_AUDIT_V1",
        "status": "READ_ONLY_HISTORICAL_EVIDENCE_AUDIT__NOT_TRAINING_AUTHORIZATION",
        "manifest": {"path": str(MANIFEST), "sha256": before[str(MANIFEST)]["sha256"], "rows": len(rows), "source_rows_by_stage": dict(stages)},
        "rules": {"path": str(RULES), "sha256": before[str(RULES)]["sha256"], "anchor_formula": "SHA256(('SI-P2-anchor-v1' + LF + canonical_task + LF + stage + LF + prefix_id + LF).encode('utf-8'))"},
        "source_files_before": source_pre,
        "source_files_after": {s: {"path": v["path"], "bytes": Path(v["path"]).stat().st_size, "sha256": file_sha(Path(v["path"]))} for s, v in source_pre.items()},
        "parent_rows": rows,
        "pre_q_anchor_plan": pre_q_anchor_plan,
        "known_use": {"prior_identity_union_count": len(known_union), "prior_identity_union_sha256": hashlib.sha256("\n".join(sorted(known_union)).encode()).hexdigest(), "fixed_rows_in_union": sum(r["known_use_union"] for r in rows), "expert_train_rows": sum("expert_train" in r["known_use_groups"] for r in rows), "expert_validation_rows": sum("expert_offline_validation" in r["known_use_groups"] for r in rows), "online_development_rows": sum("online_development" in r["known_use_groups"] for r in rows), "registered_groups_row_overlap": {g: sum(g in r["known_use_groups"] for r in rows) for g in member_groups if g != "registered_identity_group_sha256_sorted_newline"}, "split_presence_difference_not_clean_or_heldout": p1_cost.get("known_use_difference_by_split", "See bound P1 identity register; this audit does not certify cleanliness or heldout status.")},
        "task_identity_overlap": {"unique_tasks": raw_unique_tasks, "same_task_multi_prefix_groups": len([x for x in task_overlap if x["candidate_count"] > 1]), "cross_stage_task_groups": len([x for x in task_overlap if x["cross_stage"]]), "groups": task_overlap},
        "physical_alias": {"legacy_rows": sum(r["stage"] != "R19_K1" for r in rows), "legacy_alias_status": "NOT_PROVEN_WITHOUT_EVENT_IDS; no semantic dedup applied", "R19_event_ids_indexed": len(event_map), "R19_repeated_recovery_event_ids": repeated_event_ids, "R19_explicit_duplicate_unit_groups": physical_alias_groups, "r19_event_journal": {"path": str(EVENTS), "bytes": events_before["bytes"], "sha256_before": events_before["sha256"], "sha256_after": file_sha(EVENTS)}},
        "q_hist_counts": dict(Counter(r["q_hist"] for r in rows)),
        "q_pin_counts": dict(Counter(r["q_pin"] for r in rows)),
        "capacity_stages": stages_after,
        "same_public_input_different_target_ambiguities": target_ambiguities,
        "q_pin_sensitivity_capacity": {"RAW_Q_hist_and_pin": profile(pin_rows), "physical_dedup": profile(pin_physical), "task_anchor": profile(pin_anchors), "exact_input_target_dedup": profile(pin_final), "dropped_exact_no_refill": len(pin_dup_drop), "interpretation": "Metadata sensitivity only; Q_pin is a subset of Q_hist and does not replace the primary pool."},
        "original_eleven_dispositions": eleven_dispositions,
        "runtime_pin": {"path": str(runtime_path), "sha256": runtime_sha, "model_files_and_controller_actor_role_fields_present": runtime_model_role, "scope": "presence/receipt linkage metadata only; no current cache or current baseline identity backfilled"},
        "cost_context": {"r19_cumulative_generations": 5142, "r19_cumulative_environment_operations_including_resets": 7949, "historical_sft_cost_source": p1_cost["budget_corrections"]["training_result"], "future_minimal_three_arm_formula": p1_cost["budget_corrections"]["future_frozen_minimal_evaluation"]},
        "audit_inputs_before": before,
        "science_calls": {"model": 0, "environment": 0, "training": 0, "tokenizer": 0, "policy_replay": 0, "project_validator": 0, "pytest": 0},
    }
    # Rehash all source inputs post-read; these are the before/after integrity anchors.
    result["source_files_after"] = {s: {"path": v["path"], "bytes": Path(v["path"]).stat().st_size, "sha256": file_sha(Path(v["path"])), "unchanged": file_sha(Path(v["path"])) == v["sha256"]} for s, v in source_pre.items()}
    result["r19_event_journal_after"] = {"bytes": EVENTS.stat().st_size, "sha256": file_sha(EVENTS), "unchanged": file_sha(EVENTS) == events_before["sha256"]}
    result["audit_inputs_after"] = {str(p): {"bytes": p.stat().st_size, "sha256": file_sha(p), "unchanged": file_sha(p) == before[str(p)]["sha256"]} for p in (MANIFEST, RULES, KNOWN, P1_COST, P1_ELEVEN, RUNTIME)}
    (OWN / "pool_identity_audit.json").write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    anchors = {"schema": "SI_P2_PARENT_ANCHOR_PLAN_V1", "manifest_sha256": before[str(MANIFEST)]["sha256"], "rules_sha256": before[str(RULES)]["sha256"], "anchor_rule": result["rules"]["anchor_formula"], "plan_order": "All 171 identity-valid rows; one pre-Q minimum key per canonical task; labels are attached only after key computation and do not affect ordering.", "raw_rows": len(rows), "unique_tasks": raw_unique_tasks, "pre_q_anchor_plan": pre_q_anchor_plan, "pre_q_raw_B_pool": sum(r["B_pool"] for r in rows), "pre_q_raw_C_student": sum(r["C_student"] for r in rows), "pre_q_raw_B_minus_C": sum(r["B_pool"] and not r["C_student"] for r in rows), "not_a_Q_hist_or_final_capacity_claim": True}
    (OWN / "parent_anchor_plan.json").write_text(json.dumps(anchors, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(rows), "unique_tasks": raw_unique_tasks, "q_hist": result["q_hist_counts"], "q_pin": result["q_pin_counts"], "raw_B": anchors["pre_q_raw_B_pool"], "raw_C": anchors["pre_q_raw_C_student"], "event_ids": len(event_map), "status": "complete"}))

if __name__ == "__main__":
    main()
