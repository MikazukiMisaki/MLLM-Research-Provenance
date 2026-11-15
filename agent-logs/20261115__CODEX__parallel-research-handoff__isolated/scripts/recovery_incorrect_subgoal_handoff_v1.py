#!/usr/bin/env python3
"""One-shot counterfactual subgoal injection on the prior fictional prompts."""

import hashlib
import json
import os
import re
import resource
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
from recovery_semantic_handoff_pilot_v1 import gpu_sample  # noqa: E402

SOURCE = ROOT / "artifacts/runtime/parallel-research/second-object-visible-acquisition-v1/events.jsonl"
SOURCE_SHA = "ea1ef47972d23e5b76e2a6d979650e499ef3002ab34b9ba6b75cc4b4931d2c9b"
MARKER = "\n\nFrozen Stage-1 immediate subgoal:\n"
END = "\n\nIndexed admissible-action mapping:\n"


def load_source():
    raw = SOURCE.read_bytes()
    if len(raw) > 1024 * 1024 or hashlib.sha256(raw).hexdigest() != SOURCE_SHA:
        raise ValueError("source journal mismatch")
    rows = [json.loads(line) for line in raw.splitlines()]
    if not rows or rows[-1].get("event") != "complete":
        raise ValueError("source incomplete")
    stage_one = [r for r in rows if r.get("event") == "prepared" and r["key"].endswith("-stage1")]
    original = [r for r in rows if r.get("event") == "prepared" and r["key"].endswith("-generated")]
    decisions = [r for r in rows if r.get("event") == "decision" and r["condition"] == "generated"]
    expected = ["%02d" % index for index in range(1, 9)]
    if ([r["key"][:2] for r in stage_one] != expected
            or [r["key"][:2] for r in original] != expected
            or [r["key"] for r in decisions] != expected):
        raise ValueError("source key order mismatch")
    cases = []
    for first, second, decision in zip(stage_one, original, decisions):
        undo = first["undo_action"]
        if (not isinstance(undo, str) or not undo.startswith("take ")
                or undo not in second["mapping"].values()
                or decision["category"] != "take_second"
                or decision["selected_action"] != second["correct_action"]):
            raise ValueError("source action mismatch")
        prompt = second["prompt"]
        if prompt.count(MARKER) != 1:
            raise ValueError("source prompt boundary mismatch")
        head, rest = prompt.split(MARKER, 1)
        if rest.count(END) != 1:
            raise ValueError("source prompt boundary mismatch")
        old_goal, tail = rest.split(END, 1)
        injected = undo[0].upper() + undo[1:] + "."
        if old_goal == injected:
            raise ValueError("subgoal did not change")
        cases.append({"key": first["key"][:2], "prompt": head + MARKER + injected + END + tail,
                      "original_subgoal": old_goal, "injected_subgoal": injected,
                      "mapping": second["mapping"], "correct_action": second["correct_action"],
                      "undo_action": undo, "baseline_action": decision["selected_action"]})
    return cases


def main():
    if sys.argv[1:] != ["--run-once"]:
        raise SystemExit("explicit --run-once required")
    os.chdir(ROOT)
    output = ROOT / "artifacts/runtime/parallel-research/incorrect-subgoal-handoff-v1"
    output.mkdir(mode=0o700, parents=False, exist_ok=False)
    journal = (output / "events.jsonl").open("x", encoding="utf-8")
    started = time.monotonic()

    def emit(event, **fields):
        row = {"event": event, "elapsed_seconds": round(time.monotonic() - started, 6), **fields}
        journal.write(json.dumps(row, ensure_ascii=False, sort_keys=True, allow_nan=False) + "\n")
        journal.flush()
        os.fsync(journal.fileno())

    def sample(device, label, expected=None):
        identity, used = gpu_sample(device)
        emit("gpu_sample", label=label, uuid=identity, used_mib=used)
        if (expected is not None and identity != expected) or used >= 43008:
            raise RuntimeError("GPU identity or sampled limit")
        return identity

    try:
        resource.setrlimit(resource.RLIMIT_CPU, (1800, 1800))
        resource.setrlimit(resource.RLIMIT_FSIZE, (8 * 1024 * 1024, 8 * 1024 * 1024))
        cases = load_source()
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
        from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

        emit("loading_start", script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             source_sha256=SOURCE_SHA, torch_version=str(torch.__version__),
             transformers_version=transformers.__version__)
        tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True, trust_remote_code=False)
        model = AutoModelForCausalLM.from_pretrained(
            model_path, local_files_only=True, trust_remote_code=False, torch_dtype=torch.bfloat16,
        ).to("cuda:0")
        model.eval()
        eos = model.generation_config.eos_token_id
        eos = [eos] if isinstance(eos, int) else list(eos or [])
        if not eos or any(type(token) is not int or token < 0 for token in eos):
            raise ValueError("missing EOS IDs")
        pad = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else eos[0]
        template = tokenizer.chat_template
        if not isinstance(template, str) or not template:
            raise ValueError("missing chat template")
        generation = GenerationConfig(do_sample=False, num_beams=1, max_new_tokens=16,
                                      eos_token_id=eos, pad_token_id=pad, use_cache=True)
        sample(device_uuid, "after_loading", device_uuid)
        emit("loading_complete", tokenizer_class=type(tokenizer).__name__,
             chat_template_sha256=hashlib.sha256(template.encode("utf-8")).hexdigest(),
             eos_ids=eos, pad_id=pad, generation_config=generation.to_dict(), gpu_uuid=device_uuid)
        for case in cases:
            key = case["key"]
            sample(device_uuid, "before_" + key, device_uuid)
            rendered = tokenizer.apply_chat_template(
                [{"role": "user", "content": case["prompt"]}], tokenize=False,
                add_generation_prompt=True, enable_thinking=False,
            )
            inputs = tokenizer(rendered, return_tensors="pt", add_special_tokens=False, truncation=False)
            input_ids = inputs["input_ids"][0].tolist()
            if not input_ids or len(input_ids) > 1024:
                raise ValueError("input exceeds limit")
            inputs = {name: value.to("cuda:0") for name, value in inputs.items()}
            emit("prepared", input_token_count=len(input_ids), **case)
            request_start = time.monotonic()
            emit("call_start", key=key)
            with torch.inference_mode():
                output_ids = model.generate(**inputs, generation_config=generation,
                                            use_model_defaults=False)[0].tolist()
            duration = time.monotonic() - request_start
            emit("raw_result", key=key, output_ids=output_ids, request_seconds=round(duration, 6))
            if output_ids[:len(input_ids)] != input_ids:
                raise ValueError("input prefix mismatch")
            suffix = output_ids[len(input_ids):]
            if not suffix or len(suffix) > 16:
                raise ValueError("invalid output length")
            positions = [index for index, token in enumerate(suffix) if token in eos]
            if positions == [len(suffix) - 1]:
                text = tokenizer.decode(suffix[:-1], skip_special_tokens=True,
                                        clean_up_tokenization_spaces=False).strip()
                action = case["mapping"].get(text) if re.fullmatch(r"A[0-9]{3}", text) else None
                category = ("format_invalid" if action is None else
                            "undo_first" if action == case["undo_action"] else
                            "take_second" if action == case["correct_action"] else action)
            elif not positions and len(suffix) == 16:
                text, action, category = "", None, "truncated"
            else:
                raise ValueError("unconfirmed termination")
            emit("decision", key=key, token_ids=suffix, decoded=text, selected_action=action,
                 category=category, request_seconds=round(duration, 6))
            sample(device_uuid, "after_" + key, device_uuid)
            if duration >= 120:
                raise TimeoutError("request exceeded time limit")
        usage = resource.getrusage(resource.RUSAGE_SELF)
        emit("complete", call_count=len(cases), max_rss_kib=usage.ru_maxrss,
             user_cpu_seconds=usage.ru_utime, system_cpu_seconds=usage.ru_stime)
        return 0
    except Exception as error:
        try:
            usage = resource.getrusage(resource.RUSAGE_SELF)
            emit("stopped", error_type=type(error).__name__, max_rss_kib=usage.ru_maxrss,
                 user_cpu_seconds=usage.ru_utime, system_cpu_seconds=usage.ru_stime)
        except Exception:
            pass
        return 1
    finally:
        journal.close()


if __name__ == "__main__":
    raise SystemExit(main())
