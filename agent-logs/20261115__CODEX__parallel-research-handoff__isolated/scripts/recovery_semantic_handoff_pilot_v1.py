#!/usr/bin/env python3
"""One-shot fictional stage-two handoff observation; no environment access."""

import hashlib
import json
import os
import re
import resource
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from recovery.two_stage_v2 import STAGE_TWO_INSTRUCTIONS  # noqa: E402


# Fictional, manually authored commands; these are not environment task data.
SCENES = (
    ("put red mug in cabinet", "put blue bowl on shelf",
     "Place the red mug inside the cabinet.", "Place the blue bowl on the shelf."),
    ("take green book from table", "take yellow cup from counter",
     "Pick up the green book from the table.", "Pick up the yellow cup from the counter."),
    ("open wooden drawer", "close metal cabinet",
     "Make the wooden drawer open.", "Make the metal cabinet closed."),
    ("put silver spoon in box", "put black plate on tray",
     "Place the silver spoon inside the box.", "Place the black plate onto the tray."),
    ("take white towel from rack", "take purple cloth from shelf",
     "Pick up the white towel from the rack.", "Pick up the purple cloth from the shelf."),
    ("open blue box", "close green drawer",
     "Make the blue box open.", "Make the green drawer closed."),
    ("put orange key in drawer", "put gray pen on desk",
     "Place the orange key inside the drawer.", "Place the gray pen onto the desk."),
    ("take striped hat from chair", "take brown shoe from floor",
     "Pick up the striped hat from the chair.", "Pick up the brown shoe from the floor."),
)
LIMIT_MIB = 43008
OUTPUT_LIMIT = 16
INPUT_LIMIT = 1024
REQUEST_SECONDS = 120


def gpu_sample(device):
    result = subprocess.run(
        ["nvidia-smi", "--id=" + str(device), "--query-gpu=uuid,memory.used",
         "--format=csv,noheader,nounits"],
        check=True, capture_output=True, text=True, timeout=5,
    )
    lines = result.stdout.strip().splitlines()
    if len(lines) != 1:
        raise ValueError("invalid GPU sample")
    parts = [part.strip() for part in lines[0].split(",")]
    if len(parts) != 2 or not parts[0].startswith("GPU-") or not parts[1].isdigit():
        raise ValueError("invalid GPU sample")
    return parts[0], int(parts[1])


def build_prompt(subgoal, actions):
    mapping = {"A%03d" % i: action for i, action in enumerate(actions)}
    lines = "\n".join("[%s] %s" % (key, value) for key, value in mapping.items())
    prompt = (
        STAGE_TWO_INSTRUCTIONS
        + "\n\nTask goal:\nComplete the immediate subgoal."
        + "\n\nCurrent pre-action observation:\nThe listed commands are available."
        + "\n\nFrozen Stage-1 diagnosis:\nThe next action should execute the immediate subgoal."
        + "\n\nFrozen Stage-1 immediate subgoal:\n" + subgoal
        + "\n\nIndexed admissible-action mapping:\n" + lines
        + "\n\nYour response:"
    )
    return prompt, mapping


def main():
    if sys.argv[1:] != ["--run-once"]:
        raise SystemExit("explicit --run-once required")
    os.chdir(ROOT)
    output = ROOT / "artifacts/runtime/parallel-research/semantic-handoff-pilot-v1"
    output.mkdir(mode=0o700, parents=False, exist_ok=False)
    journal = (output / "events.jsonl").open("x", encoding="utf-8")
    started = time.monotonic()

    def emit(event, **fields):
        row = {"event": event, "elapsed_seconds": round(time.monotonic() - started, 6), **fields}
        journal.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        journal.flush()
        os.fsync(journal.fileno())

    def sample(device, label, expected=None):
        identity, used = gpu_sample(device)
        emit("gpu_sample", label=label, uuid=identity, used_mib=used)
        if (expected is not None and identity != expected) or used >= LIMIT_MIB:
            raise RuntimeError("GPU identity or sampled limit")
        return identity

    try:
        resource.setrlimit(resource.RLIMIT_CPU, (1800, 1800))
        resource.setrlimit(resource.RLIMIT_FSIZE, (8 * 1024 * 1024, 8 * 1024 * 1024))
        device_uuid = sample(0, "before_loading")
        os.environ["CUDA_VISIBLE_DEVICES"] = device_uuid
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        with (ROOT / "configs/local/parallel_research_pilot.json").open(encoding="utf-8") as stream:
            config = json.load(stream)
        model_path = config.get("model_path")
        if not isinstance(model_path, str) or not os.path.isabs(model_path):
            raise ValueError("invalid project model path")
        import torch
        import transformers
        from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

        emit("loading_start", script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             torch_version=str(torch.__version__), transformers_version=transformers.__version__)
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
        generation = GenerationConfig(
            do_sample=False, num_beams=1, max_new_tokens=OUTPUT_LIMIT,
            eos_token_id=eos, pad_token_id=pad, use_cache=True,
        )
        template = tokenizer.chat_template
        if not isinstance(template, str) or not template:
            raise ValueError("missing chat template")
        sample(device_uuid, "after_loading", device_uuid)
        emit("loading_complete", tokenizer_class=type(tokenizer).__name__,
             chat_template_sha256=hashlib.sha256(template.encode("utf-8")).hexdigest(),
             eos_ids=eos, pad_id=pad, generation_config=generation.to_dict(),
             gpu_uuid=device_uuid)
        for scene_index, (action_one, action_two, goal_one, goal_two) in enumerate(SCENES, 1):
            for target_index, subgoal in enumerate((goal_one, goal_two), 1):
                correct = (action_one, action_two)[target_index - 1]
                for condition in ("C1", "C2"):
                    key = "%02d-%d-%s" % (scene_index, target_index, condition)
                    actions = (action_one, action_two, "look", "inventory")
                    if condition == "C2":
                        actions = tuple(reversed(actions))
                    prompt, mapping = build_prompt(subgoal, actions)
                    sample(device_uuid, "before_" + key, device_uuid)
                    rendered = tokenizer.apply_chat_template(
                        [{"role": "user", "content": prompt}], tokenize=False,
                        add_generation_prompt=True, enable_thinking=False,
                    )
                    inputs = tokenizer(rendered, return_tensors="pt", add_special_tokens=False,
                                       truncation=False)
                    input_ids = inputs["input_ids"][0].tolist()
                    if not input_ids or len(input_ids) > INPUT_LIMIT:
                        raise ValueError("input exceeds limit")
                    inputs = {name: value.to("cuda:0") for name, value in inputs.items()}
                    emit("prepared", key=key, prompt=prompt, mapping=mapping,
                         correct_action=correct, input_token_count=len(input_ids))
                    request_start = time.monotonic()
                    emit("call_start", key=key)
                    with torch.inference_mode():
                        output_ids = model.generate(
                            **inputs, generation_config=generation, use_model_defaults=False,
                        )[0].tolist()
                    duration = time.monotonic() - request_start
                    emit("raw_result", key=key, output_ids=output_ids,
                         request_seconds=round(duration, 6))
                    if output_ids[:len(input_ids)] != input_ids:
                        raise ValueError("input prefix mismatch")
                    suffix = output_ids[len(input_ids):]
                    if not suffix or len(suffix) > OUTPUT_LIMIT:
                        raise ValueError("invalid output length")
                    eos_positions = [index for index, token in enumerate(suffix) if token in eos]
                    if eos_positions == [len(suffix) - 1]:
                        text = tokenizer.decode(suffix[:-1], skip_special_tokens=True,
                                                clean_up_tokenization_spaces=False).strip()
                        selected = mapping.get(text) if re.fullmatch(r"A[0-9]{3}", text) else None
                        category = ("correct" if selected == correct else
                                    "incorrect" if selected is not None else "format_invalid")
                    elif not eos_positions and len(suffix) == OUTPUT_LIMIT:
                        text, selected, category = "", None, "truncated"
                    else:
                        raise ValueError("unconfirmed termination")
                    emit("result", key=key, output_token_ids=suffix, decoded=text,
                         selected_action=selected, category=category,
                         request_seconds=round(duration, 6))
                    sample(device_uuid, "after_" + key, device_uuid)
                    if duration >= REQUEST_SECONDS:
                        raise TimeoutError("request exceeded time limit")
        usage = resource.getrusage(resource.RUSAGE_SELF)
        emit("complete", request_count=32, max_rss_kib=usage.ru_maxrss,
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
