#!/usr/bin/env python3
"""Exploratory candidate-sequence scoring for the prior fictional pilot."""

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

SOURCE = ROOT / "artifacts/runtime/parallel-research/semantic-handoff-pilot-v1/events.jsonl"
SOURCE_SHA = "0ff8b9ed99a0b98d2453cef1c1b243fb3b5c342d7b3369164b11f4e42bf8df82"
IDS = ("A000", "A001", "A002", "A003")
EOS = 151645
GPU_LIMIT_MIB = 43008


def load_source():
    data = SOURCE.read_bytes()
    if len(data) > 1024 * 1024 or hashlib.sha256(data).hexdigest() != SOURCE_SHA:
        raise ValueError("source journal mismatch")
    rows = [json.loads(line) for line in data.splitlines()]
    if not rows or rows[-1].get("event") != "complete":
        raise ValueError("source journal incomplete")
    prepared = [row for row in rows if row.get("event") == "prepared"]
    raw = [row for row in rows if row.get("event") == "raw_result"]
    expected = ["%02d-%d-C%d" % (scene, target, condition)
                for scene in range(1, 9) for target in (1, 2) for condition in (1, 2)]
    if ([row.get("key") for row in prepared] != expected
            or [row.get("key") for row in raw] != expected):
        raise ValueError("source key order mismatch")
    return [(p, r["output_ids"][:p["input_token_count"]]) for p, r in zip(prepared, raw)]


def main():
    if sys.argv[1:] != ["--run-once"]:
        raise SystemExit("explicit --run-once required")
    os.chdir(ROOT)
    output = ROOT / "artifacts/runtime/parallel-research/handoff-candidate-scores-v1"
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
             source_sha256=SOURCE_SHA, torch_version=str(torch.__version__),
             transformers_version=transformers.__version__)
        tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True, trust_remote_code=False)
        model = AutoModelForCausalLM.from_pretrained(
            model_path, local_files_only=True, trust_remote_code=False, torch_dtype=torch.bfloat16,
        ).to("cuda:0")
        model.eval()
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
                 input_token_count=len(prompt_ids))
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
