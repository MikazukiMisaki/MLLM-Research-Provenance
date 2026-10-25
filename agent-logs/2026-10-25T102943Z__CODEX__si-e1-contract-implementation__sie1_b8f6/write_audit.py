from pathlib import Path
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
ROOT=Path('/home/lizening/wt-si-p3-engineering-contracts')
p=ROOT/'src/self_improvement/si_p3/audit.py'
assert not p.exists()
p.write_text(r'''"""Integrity-only consumer; reconstruct each normal source and K1 handoff.

No inference, environment, policy replay, statistics, or efficacy reporting.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import asdict
from typing import Any, Mapping

from models.action_parser import action_id_mapping
from recovery.two_stage import stage_one_prompt, stage_two_prompt

from .collector import ProducerAdapter, parse_generation
from .contract import (CAPS, VERSION, Generation, PublicState, Slot, digest, plan_hash,
                       projection, request, require)
from .evidence import Caps, validate_journal


class IntegrityAudit:
    def __init__(self, run: Mapping[str, Any], events: list[dict[str, Any]], tokenizer: Any) -> None:
        self.run, self.events = run, events
        self.index = validate_journal(events)
        self.preparer = ProducerAdapter(tokenizer, lambda *_: None)
        self.used: set[str] = set()
        self.previous_sequence = -1
        self.physical = Counter(generations=0, environment_operations=0, generated_tokens=0, input_tokens=0)
        self.components: Counter[str] = Counter()

    def receipt(self, event: str, slot: Slot, phase: str, index: int, operation: str) -> dict[str, Any]:
        require(event in self.index and event not in self.used, "missing or reused physical event")
        row = self.index[event]
        identity = {"slot": slot.key, "task_id": slot.task_id, "phase": phase, "index": index, "operation": operation}
        require(row["kind"] == "unit_completed" and row["payload"]["identity"] == identity, "receipt operation/slot identity")
        require(row["sequence"] > self.previous_sequence, "physical operation order")
        self.previous_sequence = row["sequence"]
        self.used.add(event)
        started = self.index[row["payload"]["started_event"]]
        reservation = started["payload"]["reservation"]
        data = row["payload"]["data"]
        if operation == "generation":
            expected = {"generations": 1, "environment_operations": 0, "generated_tokens": CAPS[phase],
                        "input_tokens": data["raw"]["input_tokens"]}
            self.physical.update(expected | {"generated_tokens": data["raw"]["generated_tokens"]})
        else:
            expected = {"generations": 0, "environment_operations": 1, "generated_tokens": 0, "input_tokens": 0}
            self.physical.update(expected)
        require(reservation == expected, "pre-call reservation binding")
        self.components[phase + ":" + operation] += 1
        return data

    def reset(self, event: str, slot: Slot, phase: str) -> PublicState:
        data = self.receipt(event, slot, phase, 0, "reset")
        require(set(data) == {"session", "seed", "state"} and data["seed"] == slot.seed and
                data["session"] == digest([slot.key, phase]), "reset seed/session binding")
        state = PublicState.from_dict(data["state"])
        require(state.task_id == slot.task_id and state.family == slot.family and not state.ended and state.reward == 0,
                "reset task/state binding")
        return state

    def generation(self, event: str, slot: Slot, phase: str, index: int, state: PublicState,
                   history: list[tuple[str, str]], prompt: str | None = None) -> dict[str, Any]:
        data = self.receipt(event, slot, phase, index, "generation")
        require(set(data) == {"prepared", "raw", "eos_ids", "state", "parsed"}, "generation receipt fields")
        require(data["state"] == state.to_dict(), "generation causal state binding")
        expected = self.preparer.prepare(prompt if prompt is not None else projection(state, history)["public_prompt"])
        require(data["prepared"] == expected.to_dict() and data["eos_ids"] == list(self.preparer.eos_ids),
                "rendered prompt/input/EOS binding")
        adapter = "BASE" if phase in ("stage_one", "stage_two") else "P0"
        generation = Generation.from_raw(data["raw"], expected, CAPS[phase], adapter, self.preparer.eos_ids)
        require(self.preparer.tokenizer.decode(generation.raw["token_ids"], skip_special_tokens=True).strip() ==
                generation.raw["raw_output"], "output decode binding")
        parsed = parse_generation(phase, generation, state)
        require(data["parsed"] == parsed, "strict parser binding")
        return parsed

    def step(self, event: str, slot: Slot, phase: str, index: int, state: PublicState, action_id: str,
             command: str, generation_event: str | None, source_step: str | None = None) -> PublicState:
        data = self.receipt(event, slot, phase, index, "step")
        require(set(data) == {"session", "before", "command", "action_id", "action_map", "generation_event", "source_step", "after"},
                "step receipt fields")
        session_phase = "source" if phase == "source" else "replay"
        require(data["session"] == digest([slot.key, session_phase]), "same-environment in-place handoff binding")
        require(not state.ended and data["before"] == state.to_dict(), "step before-state binding")
        mapping = action_id_mapping(state.valid_actions)
        require(data["action_map"] == mapping and data["action_id"] == action_id and data["command"] == command and
                mapping.get(action_id) == command, "Action-ID/current-map/command binding")
        require(data["generation_event"] == generation_event and data["source_step"] == source_step,
                "action generation/replay receipt binding")
        after = PublicState.from_dict(data["after"])
        require((after.task_id, after.family, after.goal) == (state.task_id, state.family, state.goal), "step task/goal drift")
        return after

    def rollout(self, rollout: Mapping[str, Any], slot: Slot, phase: str, state: PublicState,
                history: list[tuple[str, str]], start: int) -> tuple[PublicState, list[PublicState]]:
        require(set(rollout) == {"generations", "steps", "end_state", "termination", "success"}, "rollout fields")
        states = [state]
        step_index = 0
        invalid = False
        for offset, event in enumerate(rollout["generations"]):
            index = start + step_index
            require(not state.ended and bool(state.valid_actions) and index < 50 and not invalid, "extra rollout generation")
            parsed = self.generation(event, slot, phase, index, state, history)
            if parsed["status"] != "selected":
                require(offset == len(rollout["generations"]) - 1, "generation after invalid actor")
                invalid = True
                continue
            require(step_index < len(rollout["steps"]), "missing selected action receipt")
            before = state
            state = self.step(rollout["steps"][step_index], slot, phase, index, state,
                              parsed["action_id"], parsed["command"], event)
            history.append((before.observation, parsed["command"]))
            states.append(state)
            step_index += 1
        require(step_index == len(rollout["steps"]), "extra environment actions")
        reason = ("terminal" if state.done else "truncated") if state.ended else (
            "empty_map" if not state.valid_actions else "invalid_actor" if invalid else
            "horizon" if start + step_index == 50 else None)
        require(reason is not None and rollout["termination"] == reason and rollout["end_state"] == state.to_dict(),
                "incomplete/forged rollout termination")
        require(type(rollout["success"]) is int and rollout["success"] == int(state.done and state.reward > 0),
                "frozen done && reward>0 success predicate")
        return state, states

    def slot(self, row: Mapping[str, Any], slot: Slot) -> None:
        require(row["slot"] == asdict(slot) and row["slot_key"] == slot.key, "slot source identity")
        source = row["source"]
        require(set(source) == {"reset", "rollout"} and row["source_reference_sha256"] == digest(source), "source reference hash")
        initial = self.reset(source["reset"], slot, "source")
        _, states = self.rollout(source["rollout"], slot, "source", initial, [], 0)
        require(type(row["Y0"]) is int and row["Y0"] == source["rollout"]["success"], "source CONTINUE label")
        eligible = len(states) > slot.cutoff and not states[slot.cutoff].ended and bool(states[slot.cutoff].valid_actions)
        if not eligible:
            require(row["disposition"] == "NO_ELIGIBLE_STATE" and row["YT"] is None and
                    row["projection"] is None and row["branch"] is None, "unreachable state must remain NA")
            return
        state = states[slot.cutoff]
        history = [(s.observation, self.index[e]["payload"]["data"]["command"])
                   for s, e in zip(states, source["rollout"]["steps"][:slot.cutoff])]
        require(row["projection"] == projection(state, history), "public pre-action projection/future leakage")
        branch = row["branch"]
        require(set(branch) == {"replay_reset", "replay_steps", "stage_one", "stage_two", "teacher_step", "suffix",
                                "source_suffix_generation_refs", "source_suffix_step_refs"}, "branch fields")
        require(branch["source_suffix_generation_refs"] == source["rollout"]["generations"][slot.cutoff:] and
                branch["source_suffix_step_refs"] == source["rollout"]["steps"][slot.cutoff:],
                "old source continuation must be references, never a rerun")
        replay_state = self.reset(branch["replay_reset"], slot, "replay")
        require(replay_state == initial and len(branch["replay_steps"]) == slot.cutoff, "prefix reset/count drift")
        for index, event in enumerate(branch["replay_steps"]):
            original = source["rollout"]["steps"][index]
            data = self.index[original]["payload"]["data"]
            replay_state = self.step(event, slot, "replay", index, replay_state,
                                     data["action_id"], data["command"], None, original)
            require(replay_state == states[index + 1], "exact prefix replay state drift")
        require(replay_state == state, "prefix checkpoint mismatch")
        one = self.generation(branch["stage_one"], slot, "stage_one", slot.cutoff, state, history,
                              stage_one_prompt(request(state, history)))
        two = self.generation(branch["stage_two"], slot, "stage_two", slot.cutoff, state, history,
                              stage_two_prompt(request(state, history), diagnosis=one["diagnosis"], subgoal=one["subgoal"],
                                               stage_one_valid=one["status"] == "valid"))
        if one["status"] != "valid" or two["status"] != "selected":
            require(row["disposition"] == "INVALID_TEACHER" and row["YT"] is None and
                    branch["teacher_step"] is None and branch["suffix"] is None, "unexecuted teacher label/action")
            return
        require(row["disposition"] == "PAIRED", "paired disposition")
        after = self.step(branch["teacher_step"], slot, "teacher", slot.cutoff, state,
                          two["action_id"], two["command"], branch["stage_two"])
        history.append((state.observation, two["command"]))
        self.rollout(branch["suffix"], slot, "suffix", after, history, slot.cutoff + 1)
        require(type(row["YT"]) is int and row["YT"] == branch["suffix"]["success"], "teacher+P0 suffix label")

    def validate(self) -> dict[str, Any]:
        run, events = self.run, self.events
        require(run["schema"] == VERSION and run["evidence_class"] == "synthetic" and
                run["execution_authorized"] is False and run["status"] == "COMPLETE", "pool not a complete software run")
        plan = tuple(Slot(**x) for x in run["plan"])
        require(run["plan_sha256"] == plan_hash(plan) == events[0]["payload"]["plan_sha256"], "plan hash binding")
        require(len(run["slots"]) == 96 and len({x["slot_key"] for x in run["slots"]}) == 96, "all96 dispositions")
        planned = [x for x in events if x["kind"] == "slot_planned"]
        closed = [x for x in events if x["kind"] == "slot_closed"]
        require([x["payload"] for x in planned] == [{"slot": asdict(s), "slot_key": s.key} for s in plan] and
                len(closed) == 96, "planned/closed slot registry")
        starts = [x for x in events if x["kind"] == "unit_started"]
        require(bool(starts) and planned[-1]["sequence"] < starts[0]["sequence"], "plan not frozen before first call")
        for slot, row, closing in zip(plan, run["slots"], closed):
            self.slot(row, slot)
            require(closing["payload"] == row and closing["sequence"] > self.previous_sequence, "slot closure receipt")
            self.previous_sequence = closing["sequence"]
        require(not any(x["kind"] == "unit_failed" for x in events), "failed physical unit in complete pool")
        require(self.used == {x["event_id"] for x in events if x["kind"] == "unit_completed"} and
                len(starts) == len(self.used), "unaccounted/shadow/retried physical operations")
        require(all(x["kind"] in {"run_opened", "slot_planned", "unit_started", "unit_completed", "slot_closed", "run_closed"}
                    for x in events), "unexpected event type")
        cost = run["cost"]
        require(cost["open_units"] == [] and cost["reserved_or_spent"] == dict(self.physical) and
                cost["completed"] == dict(self.physical), "physical cost reconstruction mismatch")
        for key in self.physical:
            require(self.physical[key] <= getattr(Caps(), key), "global cost cap")
        require(cost["device_hours"] >= 0 and cost["device_hours"] <= 4 and cost["allocated_devices"] >= 0, "allocation budget")
        last = events[-1]
        require(last["kind"] == "run_closed" and run["journal_last_event"] == last["event_id"] and
                last["payload"]["summary_sha256"] == digest({k: v for k, v in run.items() if k != "journal_last_event"}),
                "run closure binding")
        return {"status": "SOFTWARE_INTEGRITY_CHECKED_NOT_SCIENTIFIC_ACCEPTANCE", "slots": 96,
                "physical": dict(self.physical), "components": dict(self.components), "plan_sha256": run["plan_sha256"]}


def audit_run(run: Mapping[str, Any], events: list[dict[str, Any]], tokenizer: Any) -> dict[str, Any]:
    return IntegrityAudit(run, events, tokenizer).validate()
''')
print(p.relative_to(ROOT))
