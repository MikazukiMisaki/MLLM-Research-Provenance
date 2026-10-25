from pathlib import Path
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
ROOT=Path('/home/lizening/wt-si-p3-engineering-contracts')
p=ROOT/'tests/si_p3_support.py'
assert not p.exists()
p.write_text(r'''"""Explicit synthetic boundaries only. No actual task/model/environment data."""
import hashlib
import json
import re
from pathlib import Path

from env.base import ResetResult, Task, Transition
from models.action_parser import action_id_mapping
from self_improvement.si_p3.collector import Collector, Ports, ProducerAdapter
from self_improvement.si_p3.contract import (ADOPTION_QUOTAS, BACKGROUND_QUOTAS, FAMILIES, P0_SHA256,
                                            SOURCE_QUOTAS, PublicState, digest, freeze_plan, projection, text_hash)
from self_improvement.si_p3.data import select_background
from sft.protocol import sha256_value


class SyntheticTokenizer:
    """Whitespace-preserving text codec, clearly not the real Qwen tokenizer."""
    eos_token = "<eos>"
    eos_token_id = 1
    pad_token_id = 1  # exercise legal EOS==PAD masking

    def __init__(self):
        self.vocab = {"<pad>": 0, "<eos>": 1}
        self.inverse = {0: "<pad>", 1: "<eos>"}

    def token(self, text):
        if text not in self.vocab:
            idx = len(self.vocab)
            self.vocab[text] = idx
            self.inverse[idx] = text
        return self.vocab[text]

    def __call__(self, text, add_special_tokens=True):
        tokens = re.findall(r"<eos>|A\d{3}|[^\s]+|\s", text)
        return {"input_ids": [self.token(x) for x in tokens]}

    def decode(self, ids, skip_special_tokens=False):
        return "".join(self.inverse[i] for i in ids if not skip_special_tokens or i not in (0, 1))

    def apply_chat_template(self, messages, *, tokenize, add_generation_prompt, enable_thinking):
        assert tokenize is False and add_generation_prompt is True and enable_thinking is False
        assert len(messages) == 1 and set(messages[0]) == {"role", "content"} and messages[0]["role"] == "user"
        return "<user>\n" + messages[0]["content"] + "\n<assistant>\n"


class RawBoundary:
    def __init__(self, tokenizer, *, stage_one_cap_eos=False, mutate=None):
        self.tokenizer, self.calls = tokenizer, []
        self.stage_one_cap_eos, self.mutate = stage_one_cap_eos, mutate

    def __call__(self, prompt, max_new_tokens, adapter_mode):
        self.calls.append((prompt, max_new_tokens, adapter_mode))
        if max_new_tokens == 40:
            output = "Diagnosis: Repeated waiting\nSubgoal: Change activity"
        elif prompt.startswith("Select the one currently available action"):
            output = "Action-ID: A001"
        else:
            output = "A000"
        ids = self.tokenizer(output)["input_ids"]
        if max_new_tokens == 40 and self.stage_one_cap_eos:
            ids += [self.tokenizer.token(" ")] * (39 - len(ids))
        ids += [self.tokenizer.eos_token_id]
        rendered = self.tokenizer.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False,
                                                      add_generation_prompt=True, enable_thinking=False)
        raw = {"prompt": prompt, "rendered_prompt": rendered, "rendered_prompt_sha256": text_hash(rendered),
               "raw_output": output, "token_ids": ids, "token_ids_sha256": text_hash(json.dumps(ids, separators=(",", ":"))),
               "input_tokens": len(self.tokenizer(rendered)["input_ids"]), "generated_tokens": len(ids),
               "latency_seconds": 0.001, "output_complete": True, "token_cap_reached": len(ids) == max_new_tokens,
               "max_new_tokens": max_new_tokens, "do_sample": False, "thinking": False,
               "adapter_mode": adapter_mode, "adapter_sha256": P0_SHA256 if adapter_mode == "P0" else None}
        if self.mutate is not None:
            raw = self.mutate(raw, self)
        return raw


class SyntheticEnvironment:
    def __init__(self, slot, phase, *, early=False, empty=False, drift=False, teacher_terminal=False,
                 branch_fail=False, source_success=None):
        self.slot, self.phase = slot, phase
        self.early, self.empty, self.drift = early, empty, drift
        self.teacher_terminal, self.branch_fail = teacher_terminal, branch_fail
        # Fixed test roles, not production sampling or a real-data yield estimate.
        number = int(slot.task_id.rsplit("-", 1)[-1])
        self.source_success = number >= ADOPTION_QUOTAS[slot.family] if source_success is None else source_success
        self.i = 0
        self.changed = False
        self.resets, self.actions, self.closes = 0, [], 0

    def _observation(self):
        return f"Synthetic task {self.slot.task_id.rsplit('/', 1)[-1]} public step {self.i:02d}."

    def _actions(self):
        return () if self.empty and self.i == self.slot.cutoff else ("wait", "change")

    def reset(self, *, seed=None):
        assert seed == self.slot.seed
        self.resets += 1
        self.i, self.changed = 0, False
        self.task = Task(self.slot.task_id, f"Complete synthetic task {self.slot.task_id.rsplit('/', 1)[-1]}.", "train", self.slot.family)
        return ResetResult(self._observation(), self.task, self._actions())

    def step(self, command):
        assert command in self._actions()
        self.actions.append(command)
        self.i += 1
        self.changed |= command == "change"
        reached = self.i >= self.slot.cutoff + 2
        done = (self.early and self.i == 2) or (self.teacher_terminal and self.changed) or (
            reached and (self.source_success or (self.changed and not self.branch_fail)))
        obs = self._observation() + (" drift" if self.drift and self.phase == "replay" and self.i == 1 else "")
        return Transition(obs, float(done), done, False, self._actions())

    def close(self):
        self.closes += 1


def synthetic_plan():
    return freeze_plan([{"task_id": f"{family}/synthetic-{i:03d}", "family": family, "seed": 42}
                        for family in FAMILIES for i in range(SOURCE_QUOTAS[family])])


def collect_synthetic(folder, *, mutate=None, env_options=None, cap_eos=True, budget=None):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    tokenizer = SyntheticTokenizer()
    raw = RawBoundary(tokenizer, mutate=mutate, stage_one_cap_eos=cap_eos)
    environments = []

    def factory(slot, phase):
        options = env_options(slot, phase) if callable(env_options) else (env_options or {})
        value = SyntheticEnvironment(slot, phase, **options)
        environments.append(value)
        return value

    collector = Collector(synthetic_plan(), Ports(ProducerAdapter(tokenizer, raw), factory), folder / "events.jsonl", budget=budget)
    run = collector.run()
    events = [json.loads(x) for x in (folder / "events.jsonl").read_text().splitlines()]
    (folder / "run.json").write_text(json.dumps(run, indent=2) + "\n")
    return run, events, tokenizer, raw, environments


def synthetic_background(folder, tokenizer):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    tasks, rows = [], []
    for family in FAMILIES:
        for i in range(BACKGROUND_QUOTAS[family] + 1):
            task = f"{family}/background-{i:03d}"
            tasks.append({"task_id": task, "family": family})
            state = PublicState(task, family, f"Complete background task {i:03d}.", f"Public background state {i:03d}.", ("wait", "change"))
            public = projection(state, [])
            rendered = tokenizer.apply_chat_template([{"role": "user", "content": public["public_prompt"]}], tokenize=False,
                                                     add_generation_prompt=True, enable_thinking=False)
            mapping = action_id_mapping(state.valid_actions)
            row = {"schema_version": "sft_policy_example_v1", "dataset_split": "train", "task_id": task,
                   "task_family": family, "source_split": "train", "trajectory_id": "synthetic-expert-" + task,
                   "step_index": 0, "goal": state.goal, "observation": state.observation, "recent_history": [],
                   "public_prompt": public["public_prompt"], "prompt": rendered, "completion": "A000",
                   "target_action_id": "A000", "target_command": "wait", "action_count": 2,
                   "indexed_action_map": mapping, "indexed_action_map_sha256": sha256_value(mapping),
                   "prompt_sha256": text_hash(rendered), "trajectory_sha256": digest(task),
                   "tokenizer_length": len(tokenizer(rendered + "A000" + tokenizer.eos_token)["input_ids"]),
                   "terminal_task_success": True}
            rows.append(row)
    file = folder / "synthetic_expert.jsonl"
    file.write_text("".join(json.dumps(x, sort_keys=True) + "\n" for x in rows))
    sha = hashlib.sha256(file.read_bytes()).hexdigest()
    result = select_background(file, tokenizer, tasks, evidence_class="synthetic", synthetic_sha256=sha)
    return result, file, tasks, rows


def rehash(events):
    """Adversarial coherent rehash; does not repair semantic receipt links."""
    previous = None
    replacements = {}
    for row in events:
        old = row["event_id"]
        row["previous"] = previous
        p = row["payload"]
        if "started_event" in p:
            p["started_event"] = replacements.get(p["started_event"], p["started_event"])
        row["event_id"] = digest({k: v for k, v in row.items() if k != "event_id"})
        previous = row["event_id"]
        replacements[old] = previous
    return replacements
''')
print(p.relative_to(ROOT))
