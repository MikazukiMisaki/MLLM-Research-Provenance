from pathlib import Path
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
ROOT=Path('/home/lizening/wt-si-p3-engineering-contracts')
FILES={}
FILES['src/self_improvement/__init__.py']='"""Isolated engineering contracts; no scientific entrypoint is enabled."""\n'
FILES['src/self_improvement/si_p3/__init__.py']='"""SI-P3 v1: software-only collector, adoption and continuation contracts."""\n'
FILES['src/self_improvement/si_p3/contract.py']=r'''"""Versioned SI-P3 boundaries. Nothing here grants scientific execution."""
from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence

from env.base import Task
from models.action_parser import action_id_mapping
from models.policy import ActionRequest, TokenStatistics
from recovery.two_stage import GenerationRecord
from sft.protocol import sft_p0_prompt, validate_public_prompt

VERSION = "si_p3_engineering_v1"
STATUS = "ENGINEERING_ONLY_NO_LIVE"
BASE_SHA = "85cbb92395e5e2420c2adeb1fa0634653e742910"
DESIGN_SHA256 = "2d5ddfddc4c18072fa1b431d9c1e8e0688e1dd180511e49cdfb8112fb90d7d6e"
REVIEW_SHA256 = "2c29a244b279d4637b0e0572a3f139fe806848de8225d362d005feac45845483"
BACKGROUND_DATA_SHA256 = "c547e8f0c5988b29288f2a097169c7859741b7d4f53f222af31f5e2889d516cf"
P0_SHA256 = "6e403d85b150a74dfcc176f1f180ce4baf6fdacd922d2f96b3ceef0a21100f11"
SNAPSHOT = "b968826d9c46dd6066d109eabc6255188de91218"
FAMILIES = ("pick_and_place_simple", "pick_clean_then_place_in_recep",
            "pick_cool_then_place_in_recep", "pick_heat_then_place_in_recep",
            "pick_two_obj_and_place")
SOURCE_QUOTAS = dict(zip(FAMILIES, (35, 26, 16, 9, 10)))
Q_MIN = dict(zip(FAMILIES, (22, 17, 10, 6, 7)))
ADOPTION_QUOTAS = dict(zip(FAMILIES, (9, 6, 4, 2, 3)))
BACKGROUND_QUOTAS = dict(zip(FAMILIES, (44, 32, 20, 11, 13)))
CUTS = (5, 10, 15, 20)
CAPS = {"source": 16, "stage_one": 40, "stage_two": 16, "suffix": 16}


class ContractError(ValueError):
    """A fail-closed engineering contract violation; no retry is implied."""


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise ContractError(reason)


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def text_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def rank(domain: str, *parts: Any) -> str:
    return text_hash(domain + "\n" + "\n".join(map(str, parts)) + "\n")


def integer(value: Any, low: int = 0) -> bool:
    return type(value) is int and value >= low


def software_only(evidence_class: str) -> None:
    require(evidence_class == "synthetic", "scientific execution NOT_GRANTED; synthetic software ports only")


@dataclass(frozen=True)
class Slot:
    task_id: str
    family: str
    seed: int
    cutoff: int

    def __post_init__(self) -> None:
        require(self.family in FAMILIES and self.task_id.startswith(self.family + "/"), "slot canonical family")
        require(bool(self.task_id.split("/", 1)[1]) and ".." not in self.task_id.split("/"), "slot canonical identity")
        require(integer(self.seed) and self.cutoff in CUTS, "slot seed/cutoff")

    @property
    def key(self) -> str:
        return digest(asdict(self))


def cut_matrix() -> dict[str, dict[int, int]]:
    pointer = 0
    result = {}
    for family, count in SOURCE_QUOTAS.items():
        values = [count // 4] * 4
        for _ in range(count % 4):
            values[pointer] += 1
            pointer = (pointer + 1) % 4
        result[family] = dict(zip(CUTS, values))
    return result


def freeze_plan(identities: Sequence[Mapping[str, Any]]) -> tuple[Slot, ...]:
    """Only identity/family/seed metadata is admitted; no outcome-bearing field."""
    require(len(identities) == 96, "all96 slots required before source construction")
    require(all(set(x) == {"task_id", "family", "seed"} for x in identities), "plan metadata fields")
    require(len({x["task_id"] for x in identities}) == 96, "duplicate canonical task")
    require(all(x["family"] in FAMILIES for x in identities), "unsupported family; no quota transfer")
    matrix = cut_matrix()
    result = []
    for family in FAMILIES:
        rows = sorted((x for x in identities if x["family"] == family),
                      key=lambda x: (rank("SI-P3-prefix-v1", family, x["task_id"]), x["task_id"]))
        require(len(rows) == SOURCE_QUOTAS[family], "source family quota")
        cuts = [d for d in CUTS for _ in range(matrix[family][d])]
        result.extend(Slot(x["task_id"], family, x["seed"], d) for x, d in zip(rows, cuts))
    require(sum(s.cutoff for s in result) == 1200, "balanced cutoff sum")
    return tuple(result)


def plan_hash(plan: Sequence[Slot]) -> str:
    require(tuple(plan) == freeze_plan([{"task_id": s.task_id, "family": s.family, "seed": s.seed} for s in plan]),
            "plan order/cutoff changed after preassignment")
    return digest([asdict(s) for s in plan])


@dataclass(frozen=True)
class PublicState:
    task_id: str
    family: str
    goal: str
    observation: str
    valid_actions: tuple[str, ...]
    done: bool = False
    reward: float = 0.0
    truncated: bool = False

    def __post_init__(self) -> None:
        require(all(type(v) is str and bool(v) for v in (self.task_id, self.family, self.goal, self.observation)),
                "public identity/goal/observation")
        require(type(self.valid_actions) is tuple and all(type(x) is str and bool(x) for x in self.valid_actions),
                "full ordered admissible map required")
        require(len(self.valid_actions) <= 1000 and len(set(self.valid_actions)) == len(self.valid_actions),
                "ambiguous/oversized action map")
        require(type(self.done) is bool and type(self.truncated) is bool and
                type(self.reward) in (int, float) and math.isfinite(self.reward), "transition types")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self) | {"valid_actions": list(self.valid_actions)}

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> PublicState:
        require(set(value) == set(cls.__dataclass_fields__), "public state fields (no hidden/future extensions)")
        require(type(value["valid_actions"]) is list, "action list wire type")
        return cls(**(dict(value) | {"valid_actions": tuple(value["valid_actions"])}))

    @property
    def ended(self) -> bool:
        return self.done or self.truncated


def request(state: PublicState, history: Sequence[tuple[str, str]]) -> ActionRequest:
    return ActionRequest(Task(state.task_id, state.goal, "train", state.family), state.observation,
                         tuple(history), state.valid_actions)


def projection(state: PublicState, history: Sequence[tuple[str, str]]) -> dict[str, Any]:
    """Whitelist the causal public pre-action view; never accept a saved teacher prompt."""
    require(not state.ended and bool(state.valid_actions), "projection needs nonterminal full map")
    req = request(state, history)
    prompt = sft_p0_prompt(req)
    mapping = action_id_mapping(state.valid_actions)
    validate_public_prompt(prompt, mapping)
    return {"goal": state.goal, "observation": state.observation,
            "recent_history": [list(x) for x in history[-4:]],
            "valid_actions": list(state.valid_actions), "public_prompt": prompt,
            "public_prompt_sha256": text_hash(prompt), "action_map": mapping}


@dataclass(frozen=True)
class Prepared:
    prompt: str
    rendered_prompt: str
    input_ids: tuple[int, ...]

    def to_dict(self) -> dict[str, Any]:
        return {"prompt": self.prompt, "rendered_prompt": self.rendered_prompt,
                "input_ids": list(self.input_ids)}


@dataclass(frozen=True)
class Generation:
    """Typed adapter for the frozen _generate_exact producer dictionary."""
    raw: Mapping[str, Any]

    @classmethod
    def from_raw(cls, raw: Mapping[str, Any], prepared: Prepared, cap: int, adapter: str,
                 eos_ids: Sequence[int]) -> Generation:
        keys = {"prompt", "rendered_prompt", "rendered_prompt_sha256", "raw_output", "token_ids",
                "token_ids_sha256", "input_tokens", "generated_tokens", "latency_seconds", "output_complete",
                "token_cap_reached", "max_new_tokens", "do_sample", "thinking", "adapter_mode", "adapter_sha256"}
        require(isinstance(raw, Mapping) and set(raw) == keys, "producer mapping contract")
        require(raw["prompt"] == prepared.prompt and raw["rendered_prompt"] == prepared.rendered_prompt and
                raw["rendered_prompt_sha256"] == text_hash(prepared.rendered_prompt), "producer prompt binding")
        ids = raw["token_ids"]
        require(type(ids) is list and all(integer(i) for i in ids) and 0 < len(ids) <= cap, "producer token IDs/cap")
        require(raw["token_ids_sha256"] == text_hash(json.dumps(ids, separators=(",", ":"))), "producer token hash")
        require(type(raw["raw_output"]) is str and integer(raw["input_tokens"], 1) and
                raw["input_tokens"] == len(prepared.input_ids) and raw["generated_tokens"] == len(ids) and
                integer(raw["generated_tokens"], 1), "producer token accounting")
        require(raw["max_new_tokens"] == cap and type(raw["max_new_tokens"]) is int and
                raw["do_sample"] is False and raw["thinking"] is False, "frozen decoding")
        require(type(raw["output_complete"]) is bool and type(raw["token_cap_reached"]) is bool,
                "producer completion booleans")
        reached = len(ids) == cap
        require(raw["token_cap_reached"] == reached and
                raw["output_complete"] == (not reached or ids[-1] in eos_ids), "EOS/cap completeness binding")
        require(type(raw["latency_seconds"]) in (int, float) and math.isfinite(raw["latency_seconds"]) and
                raw["latency_seconds"] >= 0, "producer latency")
        require(adapter in ("P0", "BASE") and raw["adapter_mode"] == adapter and
                raw["adapter_sha256"] == (P0_SHA256 if adapter == "P0" else None), "adapter on/off receipt")
        return cls(json.loads(canonical(raw)))

    def record(self) -> GenerationRecord:
        r = self.raw
        return GenerationRecord(r["prompt"], r["raw_output"],
                                TokenStatistics(r["generated_tokens"], input_tokens=r["input_tokens"]),
                                r["latency_seconds"], r["output_complete"], r["token_cap_reached"], r["max_new_tokens"])
'''
FILES['src/self_improvement/si_p3/evidence.py']=r'''"""Append-only unit receipts and conservative pre-call resource reservations."""
from __future__ import annotations

import json
import math
import os
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping

from .contract import VERSION, canonical, digest, integer, require, software_only


class Journal:
    """Fresh run only; an existing or partially written run cannot be retried."""
    def __init__(self, path: Path, *, plan_sha256: str, evidence_class: str) -> None:
        software_only(evidence_class)
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._handle = self.path.open("x", encoding="utf-8")
        self.events: list[dict[str, Any]] = []
        self.append("run_opened", {"schema": VERSION, "evidence_class": evidence_class,
                                  "plan_sha256": plan_sha256, "execution_authorized": False})

    def append(self, kind: str, payload: Mapping[str, Any]) -> str:
        row = {"sequence": len(self.events), "previous": self.events[-1]["event_id"] if self.events else None,
               "kind": kind, "payload": json.loads(canonical(payload))}
        row["event_id"] = digest(row)
        self._handle.write(canonical(row) + "\n")
        self._handle.flush()
        os.fsync(self._handle.fileno())
        self.events.append(row)
        return row["event_id"]

    def close(self) -> None:
        self._handle.close()


def validate_journal(events: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    require(bool(events), "empty journal")
    previous = None
    index = {}
    states = {}
    for sequence, row in enumerate(events):
        require(set(row) == {"sequence", "previous", "kind", "payload", "event_id"}, "journal shape")
        body = {k: v for k, v in row.items() if k != "event_id"}
        require(row["sequence"] == sequence and row["previous"] == previous and row["event_id"] == digest(body),
                "journal sequence/hash chain")
        require(row["event_id"] not in index, "duplicate receipt")
        previous = row["event_id"]
        index[previous] = row
        if row["kind"].startswith("unit_"):
            p = row["payload"]
            unit = p["unit"]
            if row["kind"] == "unit_started":
                require(unit not in states, "unit retry/duplicate start")
                require(set(p["identity"]) == {"slot", "task_id", "phase", "index", "operation"}, "unit identity fields")
                require(unit == digest(p["identity"]), "unit identity digest")
                states[unit] = row
            else:
                require(row["kind"] in ("unit_completed", "unit_failed") and unit in states and
                        states[unit]["kind"] == "unit_started", "orphan/duplicate unit completion")
                require(p["started_event"] == states[unit]["event_id"], "unit start receipt binding")
                require(p["identity"] == states[unit]["payload"]["identity"], "unit operation identity changed")
                states[unit] = row
    header = events[0]
    require(header["kind"] == "run_opened" and header["payload"]["schema"] == VERSION and
            header["payload"]["evidence_class"] == "synthetic" and
            header["payload"]["execution_authorized"] is False, "journal authorization boundary")
    return index


class UnitRegistry:
    def __init__(self, journal: Journal) -> None:
        self.journal = journal
        self.states: dict[str, str] = {}

    def start(self, identity: Mapping[str, Any], reservation: Mapping[str, Any]) -> tuple[str, str]:
        unit = digest(identity)
        require(unit not in self.states, "physical unit already attempted; no retry")
        event = self.journal.append("unit_started", {"unit": unit, "identity": identity, "reservation": reservation})
        self.states[unit] = "started"
        return unit, event

    def finish(self, identity: Mapping[str, Any], unit: str, started: str,
               data: Mapping[str, Any], *, failed: bool = False) -> str:
        require(self.states.get(unit) == "started", "unit is not open")
        kind = "unit_failed" if failed else "unit_completed"
        event = self.journal.append(kind, {"unit": unit, "identity": identity, "started_event": started, "data": data})
        self.states[unit] = kind
        return event


@dataclass(frozen=True)
class Caps:
    generations: int = 8496
    environment_operations: int = 9792
    generated_tokens: int = 138240
    input_tokens: int = 16000000
    per_call_input: int = 8192
    device_hours: float = 4.0

    def __post_init__(self) -> None:
        defaults = type(self).__dataclass_fields__
        for key in ("generations", "environment_operations", "generated_tokens", "input_tokens", "per_call_input"):
            require(integer(getattr(self, key), 1) and getattr(self, key) <= defaults[key].default, "caps may only tighten")
        require(type(self.device_hours) in (int, float) and 0 < self.device_hours <= 4, "device-hour cap")


class Budget:
    """Count started attempts; failed calls retain their reservations as unknown physical cost."""
    def __init__(self, *, caps: Caps = Caps(), allocated_devices: int = 0,
                 monotonic: Callable[[], float] = time.monotonic) -> None:
        require(integer(allocated_devices), "allocated device count")
        self.caps, self.devices, self.clock = caps, allocated_devices, monotonic
        self.started_at = self.last = monotonic()
        require(math.isfinite(self.started_at), "monotonic clock")
        self.used = Counter(generations=0, environment_operations=0, generated_tokens=0, input_tokens=0)
        self.completed = Counter()
        self.open: dict[str, dict[str, int]] = {}
        self.stopped = False

    def check_time(self) -> float:
        require(not self.stopped, "budget/run already stopped")
        now = self.clock()
        require(math.isfinite(now) and now >= self.last, "monotonic time reversed")
        self.last = now
        elapsed = self.devices * (now - self.started_at) / 3600
        if elapsed > self.caps.device_hours:
            self.stopped = True
            require(False, "allocated GPUs x monotonic exceeds device-hour cap")
        return elapsed

    def reserve(self, unit: str, *, input_tokens: int = 0, output_cap: int = 0) -> dict[str, int]:
        self.check_time()
        require(unit not in self.open, "duplicate budget reservation")
        generation = output_cap > 0
        require(integer(input_tokens) and integer(output_cap), "reservation token types")
        require((generation and input_tokens > 0) or (not generation and input_tokens == 0), "reservation shape")
        require(input_tokens <= self.caps.per_call_input, "per-call input cap (no truncation)")
        debit = {"generations": int(generation), "environment_operations": int(not generation),
                 "generated_tokens": output_cap, "input_tokens": input_tokens}
        for key, amount in debit.items():
            if self.used[key] + amount > getattr(self.caps, key):
                self.stopped = True
                require(False, "pre-call budget cap: " + key)
        self.used.update(debit)
        self.open[unit] = debit
        return debit

    def complete(self, unit: str, *, actual_output: int = 0) -> None:
        require(unit in self.open, "budget completion without reservation")
        debit = self.open.pop(unit)
        require(integer(actual_output) and actual_output <= debit["generated_tokens"], "output debit mismatch")
        self.used["generated_tokens"] -= debit["generated_tokens"] - actual_output
        self.completed.update(debit | {"generated_tokens": actual_output})
        self.check_time()

    def stop(self) -> None:
        self.stopped = True

    def snapshot(self) -> dict[str, Any]:
        # No clock reset at task boundaries; open output reservations stay conservative.
        now = self.clock()
        require(math.isfinite(now) and now >= self.last, "monotonic time reversed")
        return {"reserved_or_spent": dict(self.used), "completed": dict(self.completed),
                "open_units": sorted(self.open), "allocated_devices": self.devices,
                "device_hours": self.devices * (now - self.started_at) / 3600,
                "cost_interpretation": "synthetic software receipts; no scientific expenditure"}
'''
for name,body in FILES.items():
 path=ROOT/name
 assert not path.exists(), path
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(body)
 print(name,len(body))
