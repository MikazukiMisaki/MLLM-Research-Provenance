#!/usr/bin/env python3
"""Score canonical action candidates for exposed fictional diagnosis-subgoal pairs."""

import hashlib
import json
import math
import os
import resource
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
from recovery_semantic_handoff_pilot_v1 import gpu_sample  # noqa: E402

SOURCE_HASHES = {
    "original": "ea1ef47972d23e5b76e2a6d979650e499ef3002ab34b9ba6b75cc4b4931d2c9b",
    "goal": "f7257a33a936856b933c6c9b4a12094d7b91d1c5ec75eb5997616fd7608307be",
    "diagnosis": "83b39d630630ab34d9d4fc6627440c0621e2b6400e5cbe26f1a9bca52c4fcdf2",
}
SOURCE_DIRS = {"original": "second-object-visible-acquisition-v1",
               "goal": "incorrect-subgoal-handoff-v1",
               "diagnosis": "incorrect-diagnosis-handoff-v1"}
IDS = ("A000", "A001", "A002", "A003")
EOS = 151645
GPU_LIMIT_MIB = 43008


def load_source():
    records = {}
    for name, directory in SOURCE_DIRS.items():
        data = (ROOT / "artifacts/runtime/parallel-research" / directory / "events.jsonl").read_bytes()
        if len(data) > 2 * 1024 * 1024 or hashlib.sha256(data).hexdigest() != SOURCE_HASHES[name]:
            raise ValueError("source journal mismatch")
        rows = [json.loads(line) for line in data.splitlines()]
        if not rows or rows[-1].get("event") != "complete":
            raise ValueError("source journal incomplete")
        loading = [r for r in rows if r.get("event") == "loading_complete"]
        if len(loading) != 1 or EOS not in loading[0]["eos_ids"]:
            raise ValueError("source EOS mismatch")
        records[name] = rows
    def lookup(name, event, key):
        rows = [r for r in records[name] if r.get("event") == event and r.get("key") == key]
        if len(rows) != 1:
            raise ValueError("source record mismatch")
        return rows[0]
    def split(prompt, marker, end):
        if prompt.count(marker) != 1 or prompt.count(end) != 1:
            raise ValueError("prompt boundary mismatch")
        head, tail = prompt.split(marker, 1)
        value, tail = tail.split(end, 1)
        return head, value, tail
    diag_mark = "\n\nFrozen Stage-1 diagnosis:\n"
    goal_mark = "\n\nFrozen Stage-1 immediate subgoal:\n"
    map_mark = "\n\nIndexed admissible-action mapping:\n"
    result = []
    for i in range(1, 9):
        number = "%02d" % i
        definitions = (("original", number + "-generated", "old_correct"),
                       ("goal", number, "old_wrong"),
                       ("diagnosis", number + "-original_goal", "false_correct"),
                       ("diagnosis", number + "-injected_goal", "false_wrong"))
        cases = []
        for name, key, label in definitions:
            p = lookup(name, "prepared", key)
            raw = lookup(name, "raw_result", key)
            if name == "original":
                g = lookup(name, "generation", key)
                decoded, tokens = g["decoded"], g["token_ids"]
            else:
                g = lookup(name, "decision", key)
                decoded, tokens = g["decoded"], g["token_ids"]
            count = p["input_token_count"]
            if raw["output_ids"][count:] != tokens or not tokens or tokens[-1] not in (151645, 151643):
                raise ValueError("saved generation mismatch")
            if decoded not in IDS or p["mapping"].get(decoded) is None:
                raise ValueError("invalid decoded action")
            cases.append((p, raw["output_ids"][:count], label, decoded, tokens))
        base, bad, false_good, false_bad = cases
        mapping = base[0]["mapping"]
        correct = base[0]["correct_action"]
        undo = bad[0]["undo_action"]
        if (set(mapping) != set(IDS) or len(set(mapping.values())) != 4 or correct == undo
                or correct not in mapping.values() or undo not in mapping.values()
                or any(p["mapping"] != mapping or p["correct_action"] != correct for p, *_ in cases)):
            raise ValueError("mapping mismatch")
        h1, oldgoal, t1 = split(base[0]["prompt"], goal_mark, map_mark)
        h2, badgoal, t2 = split(bad[0]["prompt"], goal_mark, map_mark)
        if h1 != h2 or t1 != t2 or oldgoal == badgoal:
            raise ValueError("goal intervention mismatch")
        for first, second in ((base, false_good), (bad, false_bad)):
            h1, olddiag, t1 = split(first[0]["prompt"], diag_mark, goal_mark)
            h2, newdiag, t2 = split(second[0]["prompt"], diag_mark, goal_mark)
            if h1 != h2 or t1 != t2 or olddiag == newdiag:
                raise ValueError("diagnosis intervention mismatch")
        for p, tokens, label, decoded, suffix in cases:
            result.append(({"key": number + "-" + label, "prompt": p["prompt"],
                            "mapping": mapping, "correct_action": correct, "undo_action": undo,
                            "prior_decoded": decoded, "prior_suffix": suffix}, tokens))
    return result


def main():
    if sys.argv[1:] != ["--run-once"]:
        raise SystemExit("explicit --run-once required")
    os.chdir(ROOT)
    output = ROOT / "artifacts/runtime/parallel-research/diagnosis-subgoal-candidate-scores-v1"
    output.mkdir(mode=0o700, parents=False, exist_ok=False)
    journal = (output / "events.jsonl").open("x", encoding="utf-8")
    started = time.monotonic()
    forwards = 0

    def emit(event, **fields):
        row = {"event": event, "elapsed_seconds": round(time.monotonic() - started, 6), **fields}
        journal.write(json.dumps(row, ensure_ascii=False, sort_keys=True, allow_nan=False) + "\n")
        journal.flush()
        os.fsync(journal.fileno())

    def sample(device, label, expected=None):
        identity, used = gpu_sample(device)
        emit("gpu_sample", label=label, uuid=identity, used_mib=used)
        if (expected is not None and identity != expected) or used >= GPU_LIMIT_MIB:
            raise RuntimeError("GPU identity or sampled limit")
        return identity

    try:
        resource.setrlimit(resource.RLIMIT_CPU, (1800, 1800))
        resource.setrlimit(resource.RLIMIT_FSIZE, (8 * 1024 * 1024, 8 * 1024 * 1024))
        source = load_source()
        device_uuid = sample(0, "before_loading")
        os.environ.update(CUDA_VISIBLE_DEVICES=device_uuid, HF_HUB_OFFLINE="1",
                          TRANSFORMERS_OFFLINE="1", TOKENIZERS_PARALLELISM="false")
        with (ROOT / "configs/local/parallel_research_pilot.json").open(encoding="utf-8") as stream:
            config = json.load(stream)
        model_path = config.get("model_path")
        if not isinstance(model_path, str) or not os.path.isabs(model_path):
            raise ValueError("invalid project model path")
        import torch
        import transformers
        from transformers import AutoModelForCausalLM, AutoTokenizer

        emit("loading_start", script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             sources_sha256=SOURCE_HASHES, torch_version=str(torch.__version__),
             transformers_version=transformers.__version__)
        tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True, trust_remote_code=False)
        model = AutoModelForCausalLM.from_pretrained(
            model_path, local_files_only=True, trust_remote_code=False, torch_dtype=torch.bfloat16,
        ).to("cuda:0")
        model.eval()
        current_eos = model.generation_config.eos_token_id
        current_eos = [current_eos] if isinstance(current_eos, int) else list(current_eos or [])
        if EOS not in current_eos:
            raise ValueError("current EOS mismatch")
        template = tokenizer.chat_template
        if not isinstance(template, str) or not template:
            raise ValueError("missing chat template")
        suffixes = {key: tokenizer.encode(key, add_special_tokens=False) + [EOS] for key in IDS}
        if (any(not 1 < len(seq) <= 16 or EOS in seq[:-1] for seq in suffixes.values())
                or len({tuple(seq) for seq in suffixes.values()}) != 4):
            raise ValueError("invalid candidate encodings")
        sample(device_uuid, "after_loading", device_uuid)
        emit("loading_complete", tokenizer_class=type(tokenizer).__name__, suffixes=suffixes,
             chat_template_sha256=hashlib.sha256(template.encode("utf-8")).hexdigest(),
             gpu_uuid=device_uuid)
        for previous, expected_input in source:
            key, prompt = previous["key"], previous["prompt"]
            mapping, correct = previous["mapping"], previous["correct_action"]
            if set(mapping) != set(IDS) or correct not in mapping.values():
                raise ValueError("source mapping mismatch")
            sample(device_uuid, "before_" + key, device_uuid)
            rendered = tokenizer.apply_chat_template(
                [{"role": "user", "content": prompt}], tokenize=False,
                add_generation_prompt=True, enable_thinking=False,
            )
            inputs = tokenizer(rendered, return_tensors="pt", add_special_tokens=False, truncation=False)
            prompt_ids = inputs["input_ids"][0].tolist()
            if not prompt_ids or len(prompt_ids) > 1024 or prompt_ids != expected_input:
                raise ValueError("prompt input mismatch")
            emit("prepared", key=key, mapping=mapping, correct_action=correct,
                 undo_action=previous["undo_action"], prior_decoded=previous["prior_decoded"],
                 prior_suffix=previous["prior_suffix"], input_token_count=len(prompt_ids))
            request_start = time.monotonic()
            for candidate in IDS:
                suffix = suffixes[candidate]
                tokens = torch.tensor([prompt_ids + suffix], dtype=torch.long, device="cuda:0")
                emit("forward_start", key=key, candidate=candidate)
                forwards += 1
                with torch.inference_mode():
                    logits = model(input_ids=tokens, use_cache=False).logits
                    rows = logits[0, len(prompt_ids) - 1:len(prompt_ids) + len(suffix) - 1, :].float()
                    chosen = torch.tensor(suffix, dtype=torch.long, device="cuda:0").unsqueeze(1)
                    logprob = float(torch.log_softmax(rows, dim=-1).gather(1, chosen).sum().item())
                if not math.isfinite(logprob):
                    raise ValueError("nonfinite candidate score")
                emit("score", key=key, candidate=candidate, suffix_token_ids=suffix,
                     log_probability=logprob, forward_input_tokens=len(prompt_ids) + len(suffix))
                del logits, rows, chosen, tokens
            duration = time.monotonic() - request_start
            emit("prompt_complete", key=key, request_seconds=round(duration, 6))
            sample(device_uuid, "after_" + key, device_uuid)
            if duration >= 120:
                raise TimeoutError("prompt scoring exceeded time limit")
        usage = resource.getrusage(resource.RUSAGE_SELF)
        emit("complete", prompt_count=len(source), forward_count=forwards,
             max_rss_kib=usage.ru_maxrss, user_cpu_seconds=usage.ru_utime,
             system_cpu_seconds=usage.ru_stime)
        return 0
    except Exception as error:
        try:
            usage = resource.getrusage(resource.RUSAGE_SELF)
            emit("stopped", error_type=type(error).__name__, forward_count=forwards,
                 max_rss_kib=usage.ru_maxrss, user_cpu_seconds=usage.ru_utime,
                 system_cpu_seconds=usage.ru_stime)
        except Exception:
            pass
        return 1
    finally:
        journal.close()


if __name__ == "__main__":
    raise SystemExit(main())
