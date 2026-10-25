from pathlib import Path
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
ROOT=Path('/home/lizening/wt-si-p3-engineering-contracts')
f=ROOT/'src/self_improvement/si_p3/evidence.py';s=f.read_text().replace('import time\n','import time\nimport uuid\n').replace('CONTRACT_FILE_SHA256, VERSION, canonical','CONTRACT_FILE_SHA256, CAPS, PublicState, Slot, VERSION, canonical')
s=s.replace('self.events: list[dict[str, Any]] = []','self.events: list[dict[str, Any]] = []\n        self.run_id = uuid.uuid4().hex')
s=s.replace('"schema": VERSION, "evidence_class": evidence_class,','"schema": VERSION, "run_id": self.run_id, "evidence_class": evidence_class,')
s=s.replace('    previous = None\n    index = {}','    run_id = events[0]["payload"].get("run_id")\n    require(type(run_id) is str and len(run_id) == 32 and all(c in "0123456789abcdef" for c in run_id), "journal run identity")\n    previous = None\n    index = {}')
s=s.replace('unit == digest(p["identity"])','unit == digest([run_id, p["identity"]])')
start=s.index('class UnitRegistry:');end=s.index('\n\n@dataclass(frozen=True)\nclass Caps:',start)
s=s[:start]+r'''class UnitRegistry:
    """Online run/task/kind/start binding, in addition to the consumer audit."""
    def __init__(self, journal: Journal) -> None:
        self.journal = journal
        self.states: dict[str, str] = {}
        self.starts: dict[str, tuple[dict[str, Any], str]] = {}
        self.completed_events: dict[str, dict[str, Any]] = {}
        self.slots: dict[str, Slot] = {}

    def _slot(self, identity: Mapping[str, Any]) -> Slot:
        if not self.slots:
            self.slots = {row["payload"]["slot_key"]: Slot(**row["payload"]["slot"])
                          for row in self.journal.events if row["kind"] == "slot_planned"}
        require(set(identity) == {"slot", "task_id", "phase", "index", "operation"}, "unit identity fields")
        require(identity["slot"] in self.slots, "unplanned slot/run")
        slot = self.slots[identity["slot"]]
        require(slot.key == identity["slot"] and slot.task_id == identity["task_id"], "unit task/seed identity")
        phase, op, index = identity["phase"], identity["operation"], identity["index"]
        require(integer(index), "operation index")
        allowed = {"source": {"reset", "generation", "step"}, "replay": {"reset", "step"},
                   "stage_one": {"generation"}, "stage_two": {"generation"}, "teacher": {"step"},
                   "suffix": {"generation", "step"}}
        require(phase in allowed and op in allowed[phase], "cross-kind operation")
        require((op == "reset" and index == 0) or
                (op != "reset" and phase == "source" and index < 50) or
                (op == "step" and phase == "replay" and index < slot.cutoff) or
                (phase in {"stage_one", "stage_two", "teacher"} and index == slot.cutoff) or
                (phase == "suffix" and slot.cutoff + 1 <= index < 50), "phase/cutoff index")
        return slot

    def start(self, identity: Mapping[str, Any], reservation: Mapping[str, Any]) -> tuple[str, str]:
        self._slot(identity)
        unit = digest([self.journal.run_id, identity])
        require(unit not in self.states, "physical unit already attempted; no retry")
        event = self.journal.append("unit_started", {"unit": unit, "identity": identity, "reservation": reservation})
        self.states[unit] = "started"
        self.starts[unit] = (dict(identity), event)
        return unit, event

    def _data_contract(self, identity: Mapping[str, Any], data: Mapping[str, Any]) -> None:
        from models.action_parser import action_id_mapping
        slot = self._slot(identity)
        op, phase = identity["operation"], identity["phase"]
        if op == "reset":
            require(set(data) == {"session", "seed", "state"} and data["seed"] == slot.seed and
                    data["session"] == digest([slot.key, phase]), "reset run/task/seed receipt")
            states = [data["state"]]
        elif op == "generation":
            require(set(data) == {"prepared", "raw", "eos_ids", "state", "parsed"}, "cross-kind generation receipt")
            require(data["raw"]["max_new_tokens"] == CAPS[phase], "phase generation cap")
            states = [data["state"]]
        else:
            require(set(data) == {"session", "before", "after", "command", "action_id", "action_map", "generation_event", "source_step"},
                    "cross-kind step receipt")
            require(data["session"] == digest([slot.key, "source" if phase == "source" else "replay"]), "step session")
            before = PublicState.from_dict(data["before"])
            require(data["action_map"] == action_id_mapping(before.valid_actions) and
                    data["action_id"] in data["action_map"] and data["action_map"][data["action_id"]] == data["command"],
                    "Action-ID map receipt")
            reference = data["source_step"] if phase == "replay" else data["generation_event"]
            require(reference in self.completed_events, "foreign run/missing action source receipt")
            proof = self.completed_events[reference]
            expected_phase = "source" if phase == "replay" else "stage_two" if phase == "teacher" else phase
            expected_op = "step" if phase == "replay" else "generation"
            expected = dict(identity) | {"phase": expected_phase, "operation": expected_op}
            require(proof["identity"] == expected, "action source task/kind/index receipt")
            if phase == "replay":
                require(data["generation_event"] is None and proof["data"]["action_id"] == data["action_id"] and
                        proof["data"]["command"] == data["command"], "replay original action binding")
            else:
                require(data["source_step"] is None and proof["data"]["parsed"]["status"] == "selected" and
                        proof["data"]["parsed"]["action_id"] == data["action_id"] and
                        proof["data"]["parsed"]["command"] == data["command"], "selected generation binding")
            states = [data["before"], data["after"]]
        for wire in states:
            state = PublicState.from_dict(wire)
            require(state.task_id == slot.task_id and state.family == slot.family, "receipt public task/family")

    def finish(self, identity: Mapping[str, Any], unit: str, started: str,
               data: Mapping[str, Any], *, failed: bool = False) -> str:
        require(self.states.get(unit) == "started", "unit is not open")
        require(unit == digest([self.journal.run_id, identity]) and
                self.starts[unit] == (dict(identity), started), "completion wrong run/task/kind/start")
        if not failed:
            self._data_contract(identity, data)
        else:
            require(type(data.get("exception")) is str and type(data.get("message")) is str, "failure receipt")
        kind = "unit_failed" if failed else "unit_completed"
        payload = {"unit": unit, "identity": identity, "started_event": started, "data": data}
        event = self.journal.append(kind, payload)
        self.states[unit] = kind
        if not failed:
            self.completed_events[event] = payload
        return event
''' +s[end:]
f.write_text(s)
f=ROOT/'src/self_improvement/si_p3/collector.py';s=f.read_text();s=s.replace('unit = digest(identity)\n        reservation','unit = digest([self.journal.run_id, identity])\n        reservation');s=s.replace('            data = function()\n        except Exception as error:', '            data = function()\n            event = self.registry.finish(identity, unit, started, data)\n        except Exception as error:');s=s.replace('self.registry.finish(identity, unit, started, {"exception": type(error).__name__, "message": str(error)}, failed=True)','self.registry.finish(identity, unit, started, {"exception": type(error).__name__, "message": str(error),\n                                                          "observed_data": locals().get("data"),\n                                                          "raw_evidence": getattr(error, "raw_evidence", None)}, failed=True)');s=s.replace('        event = self.registry.finish(identity, unit, started, data)\n        self.budget.complete','        self.budget.complete');s=s.replace('"plan": [asdict(s) for s in self.plan],','"run_id": self.journal.run_id, "plan": [asdict(s) for s in self.plan],')
old='        value = Generation.from_raw(raw, prepared, cap, adapter_mode, self.eos_ids)\n        decoded = self.tokenizer.decode(value.raw["token_ids"], skip_special_tokens=True).strip()\n        require(decoded == value.raw["raw_output"], "raw output/token decode mismatch")\n        return value'
new='        try:\n            value = Generation.from_raw(raw, prepared, cap, adapter_mode, self.eos_ids)\n            decoded = self.tokenizer.decode(value.raw["token_ids"], skip_special_tokens=True).strip()\n            require(decoded == value.raw["raw_output"], "raw output/token decode mismatch")\n            return value\n        except (ValueError, KeyError, TypeError) as error:\n            failure = ContractError("producer receipt: " + str(error))\n            failure.raw_evidence = {"prepared": prepared.to_dict(), "received": dict(raw) if isinstance(raw, Mapping) else repr(raw)}\n            raise failure from error'
assert old in s;s=s.replace(old,new);f.write_text(s)
f=ROOT/'src/self_improvement/si_p3/audit.py';s=f.read_text().replace('run["execution_authorized"] is False and run["contract_sha256"]', 'run["execution_authorized"] is False and run["run_id"] == events[0]["payload"]["run_id"] and run["contract_sha256"]');f.write_text(s)
print('Strict run-unique online registry, operation completion binding and rejected raw receipt retention added only in new modules.')
