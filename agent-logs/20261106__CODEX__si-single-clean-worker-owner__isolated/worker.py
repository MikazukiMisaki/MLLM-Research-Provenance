"""DISABLED real CLEAN-1 worker. Fake tests never import a real engine."""
import ctypes
import hashlib
import json
import math
import os
from pathlib import Path
import re
import resource
import signal
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import contract

REAL_ENABLED = False
STATIC_AND_POLICY_APPROVED = False
LIMITS = {"RLIMIT_CPU": (25, 30), "RLIMIT_AS": (4 * 1024 ** 3, 4 * 1024 ** 3),
          "RLIMIT_FSIZE": (128 * 1024 ** 2, 128 * 1024 ** 2), "RLIMIT_CORE": (0, 0)}
GOAL = "clean alpha and put it in destination_zero"


def real_guard():
    if not REAL_ENABLED or not STATIC_AND_POLICY_APPROVED:
        raise RuntimeError("REAL_WORKER_DISABLED_NOT_REVIEWED")


def apply_limits(api=resource):
    for name, target in LIMITS.items():
        api.setrlimit(getattr(api, name), target)
    actual = {name: tuple(api.getrlimit(getattr(api, name))) for name in LIMITS}
    if actual != LIMITS:
        raise RuntimeError("direct_worker_limit_mismatch")
    return {key: list(value) for key, value in actual.items()}


def setup_parent_death(parent):
    signal.signal(signal.SIGTERM, signal.SIG_DFL)
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(1, signal.SIGTERM, 0, 0, 0) != 0:
        raise OSError(ctypes.get_errno(), "prctl")
    signal.pthread_sigmask(signal.SIG_UNBLOCK, {signal.SIGTERM})
    if signal.SIGTERM in signal.pthread_sigmask(signal.SIG_BLOCK, set()) or os.getppid() != parent:
        raise RuntimeError("parent_or_signal_mask_invalid")


class PipeRPC:
    """Owner fsyncs each started/returned event and ACKs before continuing."""
    def __init__(self):
        self.sequence = 0

    def event(self, event):
        self.sequence += 1
        msg = {"sequence": self.sequence, **event}
        print(json.dumps(msg, sort_keys=True, separators=(",", ":"), allow_nan=False), flush=True)
        ack = sys.stdin.readline()
        if ack != "ACK %s\n" % self.sequence:
            raise RuntimeError("owner_ack_missing")


class FakeRPC:
    """No persistence: fake call-order tests only."""
    def __init__(self, fail_at=None):
        self.events = []
        self.fail_at = fail_at

    def event(self, event):
        if (event.get("type"), event.get("op"), event.get("index")) == self.fail_at:
            raise RuntimeError("fake_owner_ack_missing")
        self.events.append(event)


class Named:
    def __init__(self, name):
        self.name = name


class Fact:
    def __init__(self, predicate, *args):
        self.name = predicate
        self.arguments = [Named(value) for value in args]


class Ground:
    def __init__(self, row):
        self.name = row["name"]
        self.mapping = {Named(key): Named(value) for key, value in row["mapping"].items()}


class FakeWorld:
    """No PDDL implementation: synthetic action/result objects only."""
    def __init__(self, fault=None):
        self.index = 0
        self.last = None
        self.fault = fault
        self.calls = []

    def load(self, game):
        self.calls.append("load")
        if self.fault == "load":
            raise RuntimeError("fake_load_failure")

    def state(self):
        location = ("process_location", "source_zero_location", "source_zero_location", "process_location",
                    "process_location", "destination_zero_location", "destination_zero_location")[self.index]
        rows = [("atlocation", "actor", location)]
        if self.index < 2:
            rows.extend([("inreceptacle", "alpha", "source_zero"), ("objectatlocation", "alpha", "source_zero_location")])
        elif self.index < 6:
            rows.extend([("holds", "actor", "alpha"), ("holdsany", "actor")])
        else:
            rows.extend([("inreceptacle", "alpha", "destination_zero"), ("objectatlocation", "alpha", "destination_zero_location")])
        if self.index >= 4:
            rows.append(("isclean", "alpha"))
        facts = [Fact(row[0], *row[1:]) for row in rows]
        if self.fault == "wrong-facts" and self.index == 2:
            facts = []
        if self.index < 6:
            command, name, mapping = contract.PLAN[self.index]
            row = {"command": command, "name": name, "mapping": mapping}
            ground = Ground(row)
            raw = [row["command"], "look"]
            grounds = [ground, Ground({"name": "look", "mapping": {}})]
            if self.fault == "duplicate" and self.index == 0:
                raw.append(row["command"])
                grounds.append(ground)
        else:
            raw, grounds = ["look"], [Ground({"name": "look", "mapping": {}})]
        return {"feedback": "Your task is to: " + GOAL + ".\n", "won": self.index == 6,
                "_facts": facts, "_valid_commands": raw, "_valid_actions": grounds,
                "admissible_commands": sorted(set(raw)), "_last_action": self.last}

    def reset(self):
        self.calls.append("reset")
        if self.fault == "reset":
            raise RuntimeError("fake_reset_failure")
        self.current = self.state()
        return self.current

    def step(self, command):
        self.calls.append("step")
        index = self.current["_valid_commands"].index(command)
        self.last = self.current["_valid_actions"][index]
        if self.fault == "step" and self.index == 2:
            raise RuntimeError("fake_step_failure")
        self.index += 1
        self.current = self.state()
        if self.fault == "identity" and self.index == 1:
            _, name, mapping = contract.PLAN[0]
            self.current["_last_action"] = Ground({"name": name, "mapping": mapping})
        return self.current, int(self.index == 6), self.index == 6

    def close(self):
        self.calls.append("close")
        if self.fault == "close":
            raise RuntimeError("fake_close_failure")


class FakeFactory:
    def __init__(self, fault=None):
        self.world = FakeWorld(fault)

    def construct(self):
        if self.world.fault == "construct":
            raise RuntimeError("fake_construct_failure")
        return self.world


class RealFactory:
    def construct(self):
        real_guard()
        # This branch must remain unreachable until new source, policy, exact
        # runtime snapshot and explicit authority are independently reviewed.
        import random
        import numpy as np
        import bindings
        from textworld.core import EnvInfos
        from textworld.envs.pddl.pddl import PddlEnv
        from textworld.utils import g_rng
        if (Path(sys.modules["textworld.core"].__file__).resolve() != (bindings.SITE / "textworld/core.py").resolve() or
            Path(sys.modules["textworld.envs.pddl.pddl"].__file__).resolve() != (bindings.SITE / "textworld/envs/pddl/pddl.py").resolve()):
            raise RuntimeError("runtime_module_origin_mismatch")
        random.seed(20261106)
        np.random.seed(20261106)
        g_rng.set_seed(20261106)
        infos = EnvInfos(policy_commands=False, extras=[], won=True, admissible_commands=True)
        if infos.policy_commands or "walkthrough" in infos.extras:
            raise RuntimeError("expert_interface_enabled")
        return PddlEnv(infos=infos)


def invoke(rpc, name, index, fn):
    rpc.event({"type": "START", "op": name, "index": index})
    try:
        result = fn()
    except Exception as exc:
        try:
            rpc.event({"type": "FAIL", "op": name, "index": index, "exception": type(exc).__name__})
        except Exception:
            pass
        raise
    rpc.event({"type": "RETURN", "op": name, "index": index})
    return result


def run_contract(factory, game, rpc):
    if type(factory) is RealFactory:
        real_guard()
        if type(rpc) is not PipeRPC:
            raise TypeError("real owner protocol required")
    elif type(factory) is not FakeFactory or type(rpc) is not FakeRPC:
        raise TypeError("exact fake or guarded real interfaces required")
    world, failure = None, None
    try:
        world = invoke(rpc, "construct", None, factory.construct)
        invoke(rpc, "load", None, lambda: world.load(game))
        state = invoke(rpc, "reset", None, world.reset)
        feedback = state.get("feedback")
        tasks = re.findall(r"Your task is to:\s*(.+?)(?:\n|$)", feedback or "", flags=re.IGNORECASE) if isinstance(feedback, str) else []
        if (len(tasks) != 1 or tasks[0].strip().rstrip(".") != GOAL or state.get("won") is not False):
            raise ValueError("initial_goal_or_won_mismatch")
        contract.check_facts(state, 0)
        rpc.event({"type": "OBS", "stage": 0, "state": contract.observe(state)})
        for index, (command, name, mapping) in enumerate(contract.PLAN):
            selected = contract.select_ground(state, index)
            rpc.event({"type": "GROUND", "index": index, "command": command,
                       "name": name, "mapping": mapping})
            next_state, score, done = invoke(rpc, "step", index, lambda: world.step(command))
            final = index == 5
            if (next_state.get("_last_action") is not selected or type(done) is not bool or done is not final or
                next_state.get("won") is not final or type(score) not in (int, float) or
                not math.isfinite(score) or score != int(final)):
                raise ValueError("step_outcome_or_selected_identity_mismatch")
            contract.check_facts(next_state, index + 1)
            rpc.event({"type": "OBS", "stage": index + 1, "state": contract.observe(next_state),
                       "score": score, "done": done, "selected_identity": True})
            state = next_state
    except Exception as exc:
        failure = exc
    if world is not None:
        try:
            invoke(rpc, "close", None, world.close)
        except Exception as exc:
            if failure is None:
                failure = exc
    if failure is not None:
        raise failure
    rpc.event({"type": "COMPLETE", "steps": 6})


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def real_main():
    real_guard()  # precedes input access, engine imports, claims, or native work
    parent = int(sys.argv[1])
    owner_hash, worker_hash, contract_hash, bindings_hash = sys.argv[2:6]
    if (file_hash(Path(__file__).with_name("owner.py")) != owner_hash or file_hash(__file__) != worker_hash or
        file_hash(Path(__file__).with_name("contract.py")) != contract_hash or
        file_hash(Path(__file__).with_name("bindings.py")) != bindings_hash):
        raise RuntimeError("source_binding_mismatch")
    setup_parent_death(parent)
    effective = apply_limits()
    import bindings
    snapshots = bindings.read_inputs()
    print(json.dumps({"type": "READY", "pid": os.getpid(), "limits": effective}, sort_keys=True), flush=True)
    if sys.stdin.readline() != "GO\n" or os.getppid() != parent:
        raise RuntimeError("owner_go_or_parent_invalid")
    # Appending the actual reviewed site is left as an explicit fixed binding.
    sys.path.insert(0, str(bindings.SITE))
    run_contract(RealFactory(), {"pddl_domain": snapshots["domain"].decode(),
                                "grammar": snapshots["grammar"].decode(),
                                "pddl_problem": snapshots["problem"].decode()}, PipeRPC())


if __name__ == "__main__":
    real_main()
