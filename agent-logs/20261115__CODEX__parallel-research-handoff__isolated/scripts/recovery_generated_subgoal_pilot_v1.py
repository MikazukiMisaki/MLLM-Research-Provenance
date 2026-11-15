#!/usr/bin/env python3
"""One-shot fictional paired observation of generated versus explicit subgoals."""

import hashlib
import json
import os
import re
import resource
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from recovery.two_stage import STAGE_ONE_INSTRUCTIONS  # noqa: E402
from recovery.two_stage_v2 import STAGE_TWO_INSTRUCTIONS  # noqa: E402
from recovery_semantic_handoff_pilot_v1 import gpu_sample  # noqa: E402


# Fictional item/location pairs: first completed, second held and to be placed.
SCENES = (
    ("red mug", "cabinet", "blue bowl", "shelf"),
    ("green book", "drawer", "yellow cup", "box"),
    ("silver spoon", "box", "black plate", "tray"),
    ("white towel", "rack", "purple cloth", "basket"),
    ("orange key", "drawer", "gray pen", "desk"),
    ("striped hat", "box", "brown shoe", "basket"),
    ("teal fork", "cabinet", "pink cup", "tray"),
    ("wooden toy", "shelf", "glass bottle", "box"),
)
STAGE_ONE_PATTERN = re.compile(r"\ADiagnosis: ([^\r\n]+)\r?\nSubgoal: ([^\r\n]+)\Z")
LIMIT_MIB = 43008


def scene_material(scene, index):
    first, first_destination, second, second_destination = scene
    correct = f"put {second} in {second_destination}"
    undo = f"take {first} from {first_destination}"
    actions = (correct, undo, "look", "inventory")
    shift = (index - 1) % 4
    actions = actions[shift:] + actions[:shift]
    context = (
        f"Task goal:\nPut {first} in {first_destination} and put {second} in {second_destination}."
        f"\n\nCurrent pre-action observation:\n{first} is in {first_destination}. "
        f"{second} is held; {second_destination} is accessible."
        f"\n\nCurrent inventory:\n{second}"
        f"\n\nRecent action/result transitions (last 4):\n"
        f"Action: put {first} in {first_destination}\nResult: {first} is in {first_destination}."
        "\n\nObservable recent diagnostics:\nAdjacent repeated actions: 0\nTwo-action cycle events: 0"
    )
    return context, actions, correct, f"Place {second} in {second_destination}."


def stage_one_prompt(context, actions):
    choices = "\n".join("- " + action for action in actions)
    return (STAGE_ONE_INSTRUCTIONS + "\n\n" + context
            + "\n\nCurrently executable commands (unindexed):\n" + choices + "\n\nYour response:")


def stage_two_prompt(context, actions, diagnosis, subgoal):
    mapping = {"A%03d" % index: action for index, action in enumerate(actions)}
    choices = "\n".join("[%s] %s" % (key, action) for key, action in mapping.items())
    prompt = (STAGE_TWO_INSTRUCTIONS + "\n\n" + context
              + "\n\nFrozen Stage-1 diagnosis:\n" + diagnosis
              + "\n\nFrozen Stage-1 immediate subgoal:\n" + subgoal
              + "\n\nIndexed admissible-action mapping:\n" + choices + "\n\nYour response:")
    return prompt, mapping


def main():
    if sys.argv[1:] != ["--run-once"]:
        raise SystemExit("explicit --run-once required")
    os.chdir(ROOT)
    output = ROOT / "artifacts/runtime/parallel-research/generated-subgoal-handoff-v1"
    output.mkdir(mode=0o700, parents=False, exist_ok=False)
    journal = (output / "events.jsonl").open("x", encoding="utf-8")
    started = time.monotonic()
    call_count = 0

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
        template = tokenizer.chat_template
        if not isinstance(template, str) or not template:
            raise ValueError("missing chat template")
        sample(device_uuid, "after_loading", device_uuid)
        emit("loading_complete", tokenizer_class=type(tokenizer).__name__,
             chat_template_sha256=hashlib.sha256(template.encode("utf-8")).hexdigest(),
             eos_ids=eos, pad_id=pad, gpu_uuid=device_uuid)

        def generate(key, prompt, limit, **metadata):
            nonlocal call_count
            sample(device_uuid, "before_" + key, device_uuid)
            rendered = tokenizer.apply_chat_template(
                [{"role": "user", "content": prompt}], tokenize=False,
                add_generation_prompt=True, enable_thinking=False,
            )
            inputs = tokenizer(rendered, return_tensors="pt", add_special_tokens=False, truncation=False)
            input_ids = inputs["input_ids"][0].tolist()
            if not input_ids or len(input_ids) > 1024:
                raise ValueError("input exceeds limit")
            inputs = {name: value.to("cuda:0") for name, value in inputs.items()}
            generation = GenerationConfig(do_sample=False, num_beams=1, max_new_tokens=limit,
                                          eos_token_id=eos, pad_token_id=pad, use_cache=True)
            emit("prepared", key=key, prompt=prompt, input_token_count=len(input_ids),
                 generation_config=generation.to_dict(), **metadata)
            request_start = time.monotonic()
            emit("call_start", key=key)
            call_count += 1
            with torch.inference_mode():
                output_ids = model.generate(**inputs, generation_config=generation,
                                            use_model_defaults=False)[0].tolist()
            duration = time.monotonic() - request_start
            emit("raw_result", key=key, output_ids=output_ids, request_seconds=round(duration, 6))
            if output_ids[:len(input_ids)] != input_ids:
                raise ValueError("input prefix mismatch")
            suffix = output_ids[len(input_ids):]
            if not suffix or len(suffix) > limit:
                raise ValueError("invalid output length")
            positions = [index for index, token in enumerate(suffix) if token in eos]
            if positions == [len(suffix) - 1]:
                text = tokenizer.decode(suffix[:-1], skip_special_tokens=True,
                                        clean_up_tokenization_spaces=False).strip()
                status = "complete"
            elif not positions and len(suffix) == limit:
                text = tokenizer.decode(suffix, skip_special_tokens=True,
                                        clean_up_tokenization_spaces=False).strip()
                status = "truncated"
            else:
                raise ValueError("unconfirmed termination")
            emit("generation", key=key, token_ids=suffix, decoded=text, status=status,
                 request_seconds=round(duration, 6))
            sample(device_uuid, "after_" + key, device_uuid)
            if duration >= 120:
                raise TimeoutError("request exceeded time limit")
            return text, status

        for index, scene in enumerate(SCENES, 1):
            context, actions, correct, reference = scene_material(scene, index)
            key = "%02d" % index
            text, status = generate(key + "-stage1", stage_one_prompt(context, actions), 40,
                                    scene=list(scene), correct_action=correct)
            match = STAGE_ONE_PATTERN.fullmatch(text) if status == "complete" else None
            valid = bool(match and all(len(value.split()) <= 12 for value in match.groups())
                         and not re.search(r"\bA[0-9]{3}\b", text))
            diagnosis = match.group(1).strip() if valid else "The next action should complete the task."
            subgoal = match.group(2).strip() if valid else None
            emit("stage_one_classification", key=key, status="valid" if valid else status + "_invalid",
                 diagnosis=diagnosis if valid else None, subgoal=subgoal)
            for condition in ("generated", "reference"):
                if condition == "generated" and not valid:
                    emit("condition_not_run", key=key, condition=condition, reason="stage_one_invalid")
                    continue
                condition_goal = subgoal if condition == "generated" else reference
                prompt, mapping = stage_two_prompt(context, actions, diagnosis, condition_goal)
                output_text, output_status = generate(key + "-" + condition, prompt, 16,
                                                      mapping=mapping, correct_action=correct)
                action = mapping.get(output_text) if output_status == "complete" and re.fullmatch(r"A[0-9]{3}", output_text) else None
                category = ("truncated" if output_status == "truncated" else
                            "format_invalid" if action is None else
                            "correct" if action == correct else "incorrect")
                emit("decision", key=key, condition=condition, category=category,
                     selected_action=action, correct_action=correct)
        usage = resource.getrusage(resource.RUSAGE_SELF)
        emit("complete", call_count=call_count, max_rss_kib=usage.ru_maxrss,
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
