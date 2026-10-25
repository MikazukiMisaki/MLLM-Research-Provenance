from pathlib import Path
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
ROOT=Path('/home/lizening/wt-si-p3-engineering-contracts')
p=ROOT/'src/self_improvement/si_p3/data.py'
assert not p.exists()
p.write_text(r'''"""Symmetric quality, fixed background, single matched adoption and exposure.

Outcome labels are used only to define the registered sets after all96 slots
are sealed. Tokenization is complete and loss masks are positional, including
EOS when EOS and PAD share the same ID. No task is copied to inflate dose.
"""
from __future__ import annotations

import hashlib
import json
import random
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from models.policy import ActionRequest
from env.base import Task
from sft.masking import tokenize_prompt_completion
from sft.protocol import sft_p0_prompt, validate_example

from .audit import audit_run
from .contract import (ADOPTION_QUOTAS, BACKGROUND_DATA_SHA256, BACKGROUND_QUOTAS, FAMILIES,
                       Q_MIN, PublicState, digest, rank, require, text_hash)


@dataclass(frozen=True)
class Example:
    task_id: str
    family: str
    public_prompt: str
    prompt: str
    completion: str
    command: str
    projection_sha256: str
    origin: str
    input_ids: tuple[int, ...]
    labels: tuple[int, ...]
    prompt_tokens: int

    @property
    def loss_tokens(self) -> int:
        # CausalLM shifts labels by one, so count the actual consumed positions.
        return sum(x != -100 for x in self.labels[1:])

    @property
    def exact_key(self) -> str:
        return digest([self.prompt, self.command])

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def encode_example(tokenizer: Any, *, task_id: str, family: str, public_prompt: str,
                   completion: str, command: str, origin: str) -> Example:
    require(origin in ("new", "background") and family in FAMILIES and task_id.startswith(family + "/"), "example identity")
    require(len(completion) == 4 and completion[0] == "A" and completion[1:].isdigit(), "bare-ID target")
    rendered = tokenizer.apply_chat_template([{"role": "user", "content": public_prompt}], tokenize=False,
                                              add_generation_prompt=True, enable_thinking=False)
    encoded = tokenize_prompt_completion(tokenizer, rendered, completion, max_length=2048)
    ids, labels = tuple(encoded["input_ids"]), tuple(encoded["labels"])
    prompt_tokens = next((i for i, x in enumerate(labels) if x != -100), -1)
    require(prompt_tokens > 0 and labels[-1] == tokenizer.eos_token_id and labels[-1] != -100,
            "nonempty prompt and actual supervised EOS required")
    require(all(x == -100 for x in labels[:prompt_tokens]) and
            all(x == y for x, y in zip(labels[prompt_tokens:], ids[prompt_tokens:])), "completion-only mask")
    return Example(task_id, family, public_prompt, rendered, completion, command, text_hash(public_prompt),
                   origin, ids, labels, prompt_tokens)


@dataclass(frozen=True)
class Candidate:
    example: Example
    Y0: int
    YT: int
    physical_target_event: str


@dataclass(frozen=True)
class Pool:
    candidates: tuple[Candidate, ...]
    dispositions: tuple[dict[str, Any], ...]
    integrity: Mapping[str, Any]


def build_pool(run: Mapping[str, Any], events: list[dict[str, Any]], tokenizer: Any) -> Pool:
    integrity = audit_run(run, events, tokenizer)
    index = {x["event_id"]: x for x in events}
    candidates = []
    dispositions = []
    for row in run["slots"]:
        base = {"slot_key": row["slot_key"], "task_id": row["slot"]["task_id"], "family": row["slot"]["family"],
                "Y0": row["Y0"], "YT": row["YT"]}
        if row["disposition"] != "PAIRED":
            dispositions.append(base | {"Q": False, "reason": row["disposition"]})
            continue
        branch = row["branch"]
        parsed = index[branch["stage_two"]]["payload"]["data"]["parsed"]
        public = row["projection"]
        require(public["action_map"].get(parsed["action_id"]) == parsed["command"], "teacher target map")
        try:
            example = encode_example(tokenizer, task_id=base["task_id"], family=base["family"],
                                     public_prompt=public["public_prompt"], completion=parsed["action_id"],
                                     command=parsed["command"], origin="new")
        except ValueError as error:
            # Only the frozen whole-sequence length quality exclusion is recoverable.
            if "exceeds frozen max_length" not in str(error):
                raise
            dispositions.append(base | {"Q": False, "reason": "WHOLE_SEQUENCE_OVER_2048_NO_TRUNCATION"})
            continue
        candidates.append(Candidate(example, row["Y0"], row["YT"], branch["teacher_step"]))
        dispositions.append(base | {"Q": True, "reason": "MECHANICAL_Q"})
    # One planned task already supplies one anchor. Dedup exact public-input+command
    # across tasks in an outcome-independent order, before B/C membership filtering.
    keep = []
    exact_seen = set()
    for item in sorted(candidates, key=lambda c: (rank("SI-P3-anchor-v1", c.example.task_id), c.example.task_id)):
        if item.example.exact_key in exact_seen:
            for row in dispositions:
                if row["task_id"] == item.example.task_id:
                    row.update(Q=False, reason="EXACT_PUBLIC_INPUT_COMMAND_DUPLICATE")
            continue
        exact_seen.add(item.example.exact_key)
        keep.append(item)
    require(len({c.physical_target_event for c in keep}) == len(keep), "physical target reuse")
    return Pool(tuple(keep), tuple(dispositions), integrity)


def _background_public(row: Mapping[str, Any]) -> str:
    validate_example(dict(row))
    mapping = row["indexed_action_map"]
    require(mapping == {f"A{i:03d}": x for i, x in enumerate(mapping.values())} and
            len(set(mapping.values())) == len(mapping), "background full ordered map")
    recent = row.get("recent_history", [])
    require(len(recent) <= 4 and all(set(x) == {"observation", "action"} for x in recent), "background public H4")
    req = ActionRequest(Task(row["task_id"], row["goal"], "train", row["task_family"]), row["observation"],
                        tuple((x["observation"], x["action"]) for x in recent), tuple(mapping.values()))
    public = sft_p0_prompt(req)
    require(row.get("public_prompt") == public, "background public projection reconstruction")
    return public


def select_background(dataset_path: Path, tokenizer: Any, expert_train_tasks: Sequence[Mapping[str, str]], *,
                      evidence_class: str = "historical", synthetic_sha256: str | None = None) -> tuple[Example, ...]:
    """Fix S task identities first; a selected task with no qualified row stops.

    This reads only an explicitly supplied existing expert dataset, never new
    task bodies. Synthetic fixtures must explicitly bind their own file hash.
    """
    require(evidence_class in ("historical", "synthetic"), "background evidence class")
    payload = Path(dataset_path).read_bytes()
    expected = synthetic_sha256 if evidence_class == "synthetic" else BACKGROUND_DATA_SHA256
    require(hashlib.sha256(payload).hexdigest() == expected, "background source file hash")
    rows = [json.loads(line) for line in payload.splitlines() if line]
    require(all(set(x) == {"task_id", "family"} and x["family"] in FAMILIES and
                x["task_id"].startswith(x["family"] + "/") for x in expert_train_tasks), "expert_train metadata")
    require(len({x["task_id"] for x in expert_train_tasks}) == len(expert_train_tasks), "duplicate expert task")
    selected = []
    for family in FAMILIES:
        tasks = sorted((x["task_id"] for x in expert_train_tasks if x["family"] == family),
                       key=lambda t: (rank("SI-P3-S-v1", family, t), t))
        require(len(tasks) >= BACKGROUND_QUOTAS[family], "background family capacity; no transfer")
        selected.extend((family, t) for t in tasks[:BACKGROUND_QUOTAS[family]])
    result = []
    for family, task_id in selected:
        eligible = []
        for row in rows:
            if row.get("task_id") != task_id or row.get("dataset_split") != "train":
                continue
            try:
                require(row["task_family"] == family, "background task family")
                public = _background_public(row)
                ex = encode_example(tokenizer, task_id=task_id, family=family, public_prompt=public,
                                    completion=row["completion"], command=row["target_command"], origin="background")
                require(ex.prompt == row["prompt"] and text_hash(ex.prompt) == row["prompt_sha256"] and
                        len(ex.input_ids) == row["tokenizer_length"], "background tokenizer/rendered binding")
            except (ValueError, KeyError):
                continue  # Common predeclared mechanical row quality; never select by loss or new outcomes.
            eligible.append((rank("SI-P3-S-row-v1", task_id, row["step_index"], row["prompt_sha256"], row["completion"]),
                             row["step_index"], ex))
        require(bool(eligible), "selected S task has no qualified row; NOT_READY, no replacement: " + task_id)
        result.append(min(eligible, key=lambda x: (x[0], x[1]))[2])
    require(len(result) == 120 and len({x.task_id for x in result}) == 120, "S120 unique tasks")
    return tuple(result)


@dataclass(frozen=True)
class Adoption:
    B: tuple[Candidate, ...]
    C: tuple[Candidate, ...]
    pairs: tuple[tuple[Example, Example], ...]
    audit: Mapping[str, Any]


def _candidate_rank(item: Candidate, domain: str) -> tuple[str, str]:
    ex = item.example
    return rank(domain, ex.family, ex.task_id), ex.task_id


def adopt_once(pool: Pool) -> Adoption:
    """No seed search, redraw, neutral-only B, or alternate length-cell C draw."""
    require(len(pool.dispositions) == 96 and pool.integrity["slots"] == 96, "complete96 before adoption")
    all_rows = pool.candidates
    require(len({x.example.task_id for x in all_rows}) == len(all_rows), "unique canonical anchors")
    require(len(all_rows) >= 72, "Q total guard")
    q_counts = Counter(x.example.family for x in all_rows)
    B_pool = tuple(x for x in all_rows if x.YT == 1)
    C_pool = tuple(x for x in B_pool if x.Y0 == 0)
    neutral = tuple(x for x in B_pool if x.Y0 == 1)
    selected_c = []
    for family in FAMILIES:
        require(q_counts[family] >= Q_MIN[family], "Q family guard: " + family)
        cs = [x for x in C_pool if x.example.family == family]
        ns = [x for x in neutral if x.example.family == family]
        quota = ADOPTION_QUOTAS[family]
        require(len(cs) >= quota and len(ns) >= quota, "C/neutral family coverage: " + family)
        selected_c.extend(sorted(cs, key=lambda c: _candidate_rank(c, "SI-P3-C-v1"))[:quota])
    cells: dict[tuple[str, int], list[Candidate]] = defaultdict(list)
    for c in selected_c:
        cells[(c.example.family, c.example.loss_tokens)].append(c)
    selected_b, pairs = [], []
    for cell in sorted(cells):
        cs = sorted(cells[cell], key=lambda c: _candidate_rank(c, "SI-P3-C-v1"))
        eligible = sorted((x for x in B_pool if (x.example.family, x.example.loss_tokens) == cell),
                          key=lambda c: _candidate_rank(c, "SI-P3-B-v1"))
        require(len(eligible) >= len(cs), "fixed selected-C length cell unavailable")
        bs = eligible[:len(cs)]
        selected_b.extend(bs)
        pairs.extend((b.example, c.example) for b, c in zip(bs, cs))
    require(len(selected_b) == len(selected_c) == 24, "adoption dose24")
    require(sum(x.Y0 == 1 for x in selected_b) >= 8, "selected B neutral<8; fixed draw NO_GO, never redraw")
    require({x.example.task_id for x in selected_b} != {x.example.task_id for x in selected_c}, "B/C identical training multiset")
    for name, values in (("B", selected_b), ("C", selected_c)):
        require(len({x.example.projection_sha256 for x in values}) >= 20, name + " public projections<20")
        require(len({x.example.exact_key for x in values}) == 24, name + " exact duplicate targets")
    report = {"status": "SOFTWARE_RECIPE_CONSTRUCTIBLE_NOT_LEARNING_ACCEPTANCE", "Q": len(all_rows),
              "Q_family": dict(q_counts), "B_pool": len(B_pool), "C_pool": len(C_pool), "neutral_pool": len(neutral),
              "selected_B_neutral": sum(x.Y0 == 1 for x in selected_b),
              "selected_B": [x.example.task_id for x in selected_b], "selected_C": [x.example.task_id for x in selected_c],
              "draws": 1, "hash_domains": ["SI-P3-C-v1", "SI-P3-B-v1"]}
    return Adoption(tuple(selected_b), tuple(selected_c), tuple(pairs), report)


class CompletionCollator:
    def __init__(self, pad_token_id: int) -> None:
        require(type(pad_token_id) is int and pad_token_id >= 0, "PAD ID")
        self.pad_id = pad_token_id

    def __call__(self, examples: Sequence[Example]) -> dict[str, Any]:
        import torch
        require(bool(examples), "empty microbatch")
        width = max(len(x.input_ids) for x in examples)
        require(width <= 2048, "collator cannot truncate")
        ids, masks, labels = [], [], []
        for x in examples:
            require(len(x.labels) == len(x.input_ids) and x.prompt_tokens > 0 and x.loss_tokens > 0, "example mask shape")
            require(all(y == -100 for y in x.labels[:x.prompt_tokens]) and
                    tuple(x.labels[x.prompt_tokens:]) == tuple(x.input_ids[x.prompt_tokens:]), "mask/input tamper")
            extra = width - len(x.input_ids)
            ids.append(list(x.input_ids) + [self.pad_id] * extra)
            masks.append([1] * len(x.input_ids) + [0] * extra)
            labels.append(list(x.labels) + [-100] * extra)
        return {"input_ids": torch.tensor(ids, dtype=torch.long), "attention_mask": torch.tensor(masks, dtype=torch.long),
                "labels": torch.tensor(labels, dtype=torch.long)}


def paired_slots(adoption: Adoption, background: Sequence[Example]) -> tuple[tuple[Example, Example], ...]:
    require(len(background) == 120 and len({x.task_id for x in background}) == 120 and
            Counter(x.family for x in background) == Counter(BACKGROUND_QUOTAS), "S120 family/task identities")
    require(all(x.origin == "background" for x in background), "background source role")
    require(not ({x.task_id for x in background} & {x.example.task_id for x in adoption.B + adoption.C}), "new/S task leakage")
    return tuple((x, x) for x in background) + adoption.pairs


def fixed_schedule() -> tuple[tuple[int, ...], ...]:
    rng = random.Random(42)
    epochs = []
    for _ in range(2):
        order = list(range(144))
        rng.shuffle(order)
        epochs.append(tuple(order))
    return tuple(epochs)


def audit_exposure(pairs: Sequence[tuple[Example, Example]], collator: CompletionCollator,
                   schedule: Sequence[Sequence[int]] | None = None) -> dict[str, Any]:
    schedule = tuple(tuple(x) for x in (schedule if schedule is not None else fixed_schedule()))
    require(len(pairs) == 144 and schedule == fixed_schedule(), "same fixed paired order/epochs; no independent shuffle/drop-last")
    for arm in (0, 1):
        require(len({p[arm].task_id for p in pairs}) == 144 and
                Counter(p[arm].origin for p in pairs) == {"background": 120, "new": 24}, "per-task dose/roles")
    require(all(b.loss_tokens == c.loss_tokens for b, c in pairs), "paired slot actual shifted target length")
    require(all(b == c for b, c in pairs[:120]), "common S row/weight/order")
    prompts = {"new": [0, 0], "all": [0, 0]}
    exposure = [Counter(), Counter()]
    micro_counts, update_counts = [], []
    for epoch in schedule:
        pending = [0, 0]
        for start in range(0, 144, 2):
            slots = epoch[start:start + 2]
            counts = []
            for arm in (0, 1):
                examples = [pairs[i][arm] for i in slots]
                batch = collator(examples)
                active = int((batch["labels"][:, 1:] != -100).sum().item())
                require(active == sum(x.loss_tokens for x in examples), "actual CausalLM shift/padding count")
                counts.append(active)
                pending[arm] += active
                for x in examples:
                    exposure[arm][x.task_id] += 1
                    prompts["all"][arm] += x.prompt_tokens
                    if x.origin == "new":
                        prompts["new"][arm] += x.prompt_tokens
            require(counts[0] == counts[1], "microbatch supervised tokens differ")
            micro_counts.append(counts)
            if (start // 2 + 1) % 8 == 0:
                require(pending[0] == pending[1], "optimizer update supervised tokens differ")
                update_counts.append(pending)
                pending = [0, 0]
    require(len(update_counts) == 18 and all(set(x.values()) == {2} for x in exposure), "final18/2exposures/no duplicate task inflation")
    ratios = {}
    for name, values in prompts.items():
        require(min(values) > 0 and max(values) / min(values) <= 1.05, name + " cumulative prompt ratio>1.05; no redraw")
        ratios[name] = max(values) / min(values)
    return {"status": "SOFTWARE_EXPOSURE_AUDITED_NOT_RUNTIME_READY", "schedule_sha256": digest(schedule),
            "schedule": [list(x) for x in schedule], "epochs": 2, "optimizer_updates": 18,
            "microbatch_loss_tokens": micro_counts, "update_loss_tokens": update_counts,
            "prompt_token_totals": prompts, "prompt_ratios": ratios, "per_task_exposure": [dict(x) for x in exposure]}
''')
print(p.relative_to(ROOT))
