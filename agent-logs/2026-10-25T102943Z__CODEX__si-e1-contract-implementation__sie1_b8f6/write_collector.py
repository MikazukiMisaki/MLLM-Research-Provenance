from pathlib import Path
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
ROOT=Path('/home/lizening/wt-si-p3-engineering-contracts')
p=ROOT/'src/self_improvement/si_p3/collector.py'
assert not p.exists()
p.write_text(r'''"""Production single-K1 orchestration over explicit, software-gated runtime ports.

The only substituted boundaries in integration tests are raw generation and
normalized environment I/O. Public prompts, parsers, journal, registry,
budgets, exact replay, handoff and consumers are the production functions.
There is deliberately no live driver or scientific execution permission.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Protocol, Sequence

from env.base import InteractiveEnvironment
from models.action_parser import action_id_mapping
from models.protocol_stability import parse_p2_selection
from recovery.two_stage import (parse_stage_one_output, parse_stage_two_output,
                                stage_one_prompt, stage_two_prompt)

from .contract import (CAPS, VERSION, ContractError, Generation, Prepared, PublicState, Slot,
                       digest, plan_hash, projection, request, require, software_only)
from .evidence import Budget, Journal, UnitRegistry


class RawProducer(Protocol):
    def __call__(self, prompt: str, max_new_tokens: int, adapter_mode: str) -> Mapping[str, Any]: ...


class ProducerAdapter:
    """Adapt the frozen raw dictionary; never parse it as an object or rename operations.

    A future driver must supply an adapter-state-attesting producer. The raw
    frozen `_generate_exact` fields are retained, with adapter_mode/adapter_sha256
    receipts added at that boundary. No backend is loaded by this class.
    """
    def __init__(self, tokenizer: Any, producer: RawProducer) -> None:
        self.tokenizer, self.producer = tokenizer, producer
        eos = tokenizer.eos_token_id
        self.eos_ids = (eos,) if type(eos) is int else tuple(eos or ())
        require(bool(self.eos_ids), "EOS IDs required")

    def prepare(self, prompt: str) -> Prepared:
        rendered = self.tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}], tokenize=False,
            add_generation_prompt=True, enable_thinking=False)
        ids = self.tokenizer(text=rendered, add_special_tokens=True)["input_ids"]
        require(type(ids) is list and bool(ids) and all(type(i) is int and i >= 0 for i in ids), "input IDs")
        return Prepared(prompt, rendered, tuple(ids))

    def generate(self, prepared: Prepared, cap: int, adapter_mode: str) -> Generation:
        raw = self.producer(prepared.prompt, cap, adapter_mode)
        value = Generation.from_raw(raw, prepared, cap, adapter_mode, self.eos_ids)
        decoded = self.tokenizer.decode(value.raw["token_ids"], skip_special_tokens=True).strip()
        require(decoded == value.raw["raw_output"], "raw output/token decode mismatch")
        return value


@dataclass(frozen=True)
class Ports:
    producer: ProducerAdapter
    environment_factory: Callable[[Slot, str], InteractiveEnvironment]
    evidence_class: str = "synthetic"


class EnvironmentAdapter:
    """Normalize the existing InteractiveEnvironment contract without hidden metadata."""
    def __init__(self, environment: InteractiveEnvironment, slot: Slot, session: str) -> None:
        self.environment, self.slot, self.session = environment, slot, session
        self.state: PublicState | None = None

    def reset(self) -> PublicState:
        result = self.environment.reset(seed=self.slot.seed)
        task = result.task
        require(task.task_id == self.slot.task_id and task.family == self.slot.family and task.split == "train",
                "reset task/partition identity drift")
        require(result.valid_actions is not None, "reset missing full action map")
        self.state = PublicState(task.task_id, task.family, task.text, result.observation, tuple(result.valid_actions))
        return self.state

    def step(self, command: str) -> PublicState:
        require(self.state is not None and not self.state.ended and command in self.state.valid_actions,
                "unavailable/terminal command")
        value = self.environment.step(command)
        require(value.valid_actions is not None, "transition missing full action map")
        self.state = PublicState(self.state.task_id, self.state.family, self.state.goal, value.observation,
                                 tuple(value.valid_actions), value.done, value.reward, value.truncated)
        return self.state

    def close(self) -> None:
        closer = getattr(self.environment, "close", None)
        if closer is not None:
            closer()


def parse_generation(phase: str, generation: Generation, state: PublicState) -> dict[str, Any]:
    if phase == "stage_one":
        parsed = parse_stage_one_output(generation.record())
        return {"status": parsed.status, "diagnosis": parsed.diagnosis, "subgoal": parsed.subgoal}
    if phase == "stage_two":
        parsed = parse_stage_two_output(generation.record(), state.valid_actions)
        return {"status": parsed.status, "action_id": parsed.action_id, "command": parsed.action}
    require(phase in ("source", "suffix"), "generation phase")
    if not generation.raw["output_complete"]:
        return {"status": "truncated_actor", "action_id": None, "command": ""}
    parsed = parse_p2_selection(generation.raw["raw_output"], state.valid_actions, reflection_required=False)
    return {"status": parsed.selection_status, "action_id": parsed.action_id, "command": parsed.action}


class Collector:
    def __init__(self, plan: Sequence[Slot], ports: Ports, journal_path: Path, *, budget: Budget | None = None) -> None:
        # Reject before constructing environments or calling tokenizer/model boundaries.
        software_only(ports.evidence_class)
        self.plan, self.ports = tuple(plan), ports
        self.plan_sha256 = plan_hash(self.plan)
        self.journal = Journal(journal_path, plan_sha256=self.plan_sha256, evidence_class=ports.evidence_class)
        self.registry = UnitRegistry(self.journal)
        self.budget = budget if budget is not None else Budget()
        self.environments: list[EnvironmentAdapter] = []
        self._partial: dict[str, Any] = {}
        self._ran = False
        for slot in self.plan:
            self.journal.append("slot_planned", {"slot": asdict(slot), "slot_key": slot.key})

    def _identity(self, slot: Slot, phase: str, index: int, operation: str) -> dict[str, Any]:
        return {"slot": slot.key, "task_id": slot.task_id, "phase": phase, "index": index, "operation": operation}

    def _call(self, identity: Mapping[str, Any], function: Callable[[], Mapping[str, Any]], *,
              input_tokens: int = 0, output_cap: int = 0) -> str:
        unit = digest(identity)
        reservation = self.budget.reserve(unit, input_tokens=input_tokens, output_cap=output_cap)
        unit, started = self.registry.start(identity, reservation)
        try:
            data = function()
        except Exception as error:
            self.registry.finish(identity, unit, started, {"exception": type(error).__name__, "message": str(error)}, failed=True)
            self.budget.stop()
            raise
        event = self.registry.finish(identity, unit, started, data)
        self.budget.complete(unit, actual_output=data["raw"]["generated_tokens"] if output_cap else 0)
        return event

    def _data(self, event: str) -> dict[str, Any]:
        # Receipts are authoritative; no shadow call or duplicated baseline execution.
        return next(x["payload"]["data"] for x in reversed(self.journal.events) if x["event_id"] == event)

    def _new_environment(self, slot: Slot, phase: str) -> tuple[EnvironmentAdapter, str]:
        session = digest([slot.key, phase])
        env = self.ports.environment_factory(slot, phase)
        require(all(x.environment is not env for x in self.environments), "environment factory reused another session")
        adapted = EnvironmentAdapter(env, slot, session)
        self.environments.append(adapted)
        event = self._call(self._identity(slot, phase, 0, "reset"),
                           lambda: {"session": session, "seed": slot.seed, "state": adapted.reset().to_dict()})
        return adapted, event

    def _generate(self, slot: Slot, phase: str, index: int, state: PublicState,
                  history: list[tuple[str, str]], *, prompt: str | None = None) -> tuple[str, dict[str, Any]]:
        public = projection(state, history)
        prepared = self.ports.producer.prepare(prompt if prompt is not None else public["public_prompt"])
        cap = CAPS[phase]
        adapter = "BASE" if phase in ("stage_one", "stage_two") else "P0"

        def generate() -> dict[str, Any]:
            value = self.ports.producer.generate(prepared, cap, adapter)
            return {"prepared": prepared.to_dict(), "raw": dict(value.raw), "eos_ids": list(self.ports.producer.eos_ids),
                    "state": state.to_dict(), "parsed": parse_generation(phase, value, state)}

        event = self._call(self._identity(slot, phase, index, "generation"), generate,
                           input_tokens=len(prepared.input_ids), output_cap=cap)
        return event, self._data(event)["parsed"]

    def _step(self, slot: Slot, phase: str, index: int, env: EnvironmentAdapter,
              action_id: str, command: str, *, generation_event: str | None, source_step: str | None = None) -> str:
        require(env.state is not None, "unreset environment")
        before = env.state
        mapping = action_id_mapping(before.valid_actions)
        require(mapping.get(action_id) == command, "action ID/command does not bind current map")
        return self._call(self._identity(slot, phase, index, "step"),
                          lambda: {"session": env.session, "before": before.to_dict(), "command": command,
                                   "action_id": action_id, "action_map": mapping, "generation_event": generation_event,
                                   "source_step": source_step, "after": env.step(command).to_dict()})

    def _rollout(self, slot: Slot, phase: str, env: EnvironmentAdapter,
                 history: list[tuple[str, str]], start: int) -> dict[str, Any]:
        generations, steps = [], []
        reason = "horizon"
        require(env.state is not None, "unreset rollout")
        for index in range(start, 50):
            if env.state.ended:
                reason = "terminal" if env.state.done else "truncated"
                break
            if not env.state.valid_actions:
                reason = "empty_map"
                break
            generated, parsed = self._generate(slot, phase, index, env.state, history)
            generations.append(generated)
            if parsed["status"] != "selected":
                reason = "invalid_actor"
                break
            before = env.state
            stepped = self._step(slot, phase, index, env, parsed["action_id"], parsed["command"], generation_event=generated)
            steps.append(stepped)
            history.append((before.observation, parsed["command"]))
        if env.state.ended:
            reason = "terminal" if env.state.done else "truncated"
        return {"generations": generations, "steps": steps, "end_state": env.state.to_dict(),
                "termination": reason, "success": int(env.state.done and env.state.reward > 0)}

    def _collect(self, slot: Slot) -> dict[str, Any]:
        self._partial = {}
        source_env, reset = self._new_environment(slot, "source")
        initial = self._data(reset)["state"]
        source = {"reset": reset, "rollout": self._rollout(slot, "source", source_env, [], 0)}
        self._partial["source"] = source
        source_env.close()
        state = PublicState.from_dict(initial)
        history: list[tuple[str, str]] = []
        source_steps = source["rollout"]["steps"]
        for event in source_steps[:slot.cutoff]:
            data = self._data(event)
            history.append((data["before"]["observation"], data["command"]))
            state = PublicState.from_dict(data["after"])
        row = {"slot": asdict(slot), "slot_key": slot.key, "source": source,
               "source_reference_sha256": digest(source), "Y0": source["rollout"]["success"],
               "YT": None, "branch": None, "projection": None}
        if len(source_steps) < slot.cutoff or state.ended or not state.valid_actions:
            return row | {"disposition": "NO_ELIGIBLE_STATE"}
        public = projection(state, history)
        env, replay_reset = self._new_environment(slot, "replay")
        require(self._data(replay_reset)["state"] == initial, "exact replay reset drift")
        replay = []
        for index, source_step in enumerate(source_steps[:slot.cutoff]):
            original = self._data(source_step)
            require(env.state is not None and env.state.to_dict() == original["before"], "exact replay before-state drift")
            event = self._step(slot, "replay", index, env, original["action_id"], original["command"],
                               generation_event=None, source_step=source_step)
            replay.append(event)
            require(self._data(event)["after"] == original["after"], "exact replay transition drift")
        require(env.state == state, "exact replay prefix state")
        branch = {"replay_reset": replay_reset, "replay_steps": replay, "stage_one": None, "stage_two": None,
                  "teacher_step": None, "suffix": None,
                  "source_suffix_generation_refs": source["rollout"]["generations"][slot.cutoff:],
                  "source_suffix_step_refs": source_steps[slot.cutoff:]}
        row.update(projection=public, branch=branch)
        self._partial.update(row)
        one, parsed_one = self._generate(slot, "stage_one", slot.cutoff, state, history,
                                        prompt=stage_one_prompt(request(state, history)))
        branch["stage_one"] = one
        two, parsed_two = self._generate(slot, "stage_two", slot.cutoff, state, history,
                                        prompt=stage_two_prompt(request(state, history), diagnosis=parsed_one["diagnosis"],
                                                                subgoal=parsed_one["subgoal"],
                                                                stage_one_valid=parsed_one["status"] == "valid"))
        branch["stage_two"] = two
        # Both fixed teacher calls are retained even when Stage 1 is invalid.
        if parsed_one["status"] != "valid" or parsed_two["status"] != "selected":
            return row | {"disposition": "INVALID_TEACHER"}
        step = self._step(slot, "teacher", slot.cutoff, env, parsed_two["action_id"], parsed_two["command"],
                          generation_event=two)
        branch["teacher_step"] = step
        history.append((state.observation, parsed_two["command"]))
        # Same env object and same state; no handoff reset/replay/gate call.
        suffix = self._rollout(slot, "suffix", env, history, slot.cutoff + 1)
        branch["suffix"] = suffix
        row["YT"] = suffix["success"]
        return row | {"disposition": "PAIRED"}

    def run(self) -> dict[str, Any]:
        require(not self._ran, "collector cannot run/retry twice")
        self._ran = True
        rows = []
        stopped = False
        for slot in self.plan:
            if stopped:
                row = {"slot": asdict(slot), "slot_key": slot.key, "disposition": "NOT_ATTEMPTED_AFTER_STOP", "Y0": None, "YT": None}
            else:
                try:
                    row = self._collect(slot)
                except Exception as error:
                    stopped = True
                    self.budget.stop()
                    row = {"slot": asdict(slot), "slot_key": slot.key, "disposition": "TECHNICAL_STOP",
                           "Y0": None, "YT": None, "partial": self._partial,
                           "exception": type(error).__name__, "message": str(error)}
            rows.append(row)
            self.journal.append("slot_closed", row)
        # close() performs no scientific operation and is deliberately outside the debit ledger.
        for env in self.environments:
            env.close()
        summary = {"schema": VERSION, "evidence_class": "synthetic", "execution_authorized": False,
                   "plan": [asdict(s) for s in self.plan], "plan_sha256": self.plan_sha256,
                   "status": "STOPPED" if stopped else "COMPLETE", "slots": rows, "cost": self.budget.snapshot()}
        self.journal.append("run_closed", {"summary_sha256": digest(summary)})
        summary["journal_last_event"] = self.journal.events[-1]["event_id"]
        self.journal.close()
        return summary
''')
print(p.relative_to(ROOT))
