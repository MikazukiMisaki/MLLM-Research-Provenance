#!/usr/bin/env python3
"""One-shot fictional action-ID format comparison; never invokes an environment."""
import hashlib
import json
import os
import re
import resource
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CASE_SHA256 = '2873429462c3fe2b7f4b30e049b258d5caf31826c7fbf2e34342cf3ec851ec46'
OUTPUT = ROOT / 'artifacts/runtime/parallel-research/action-id-format-factorial-dev-v1'


def sample():
    result = subprocess.run(
        ['nvidia-smi', '--query-gpu=uuid,memory.used,utilization.gpu',
         '--format=csv,noheader,nounits'],
        check=True, text=True, capture_output=True, timeout=10)
    lines = result.stdout.strip().splitlines()
    if not lines:
        raise RuntimeError('GPU sampling returned no devices')
    uuid, used, utilization = [v.strip() for v in lines[0].split(',')]
    return uuid, int(used), int(utilization)


def deadline(_signum, _frame):
    raise TimeoutError('generation deadline')


def main():
    if sys.argv[1:] != ['--run-once']:
        raise SystemExit('requires --run-once after shared GPU coordination')
    raw = (HERE / 'cases.json').read_bytes()
    if hashlib.sha256(raw).hexdigest() != CASE_SHA256:
        raise ValueError('case digest changed')
    planned = json.loads(raw)
    calls = planned['calls']
    if planned['schema'] != 'action_id_format_factorial_dev_v1' or len(calls) != 32:
        raise ValueError('invalid call schedule')
    if len({call['call_id'] for call in calls}) != 32:
        raise ValueError('duplicate call ID')
    OUTPUT.mkdir(mode=0o700, parents=False, exist_ok=False)
    started = time.monotonic()
    with (OUTPUT / 'events.jsonl').open('x', encoding='utf-8') as stream:
        def emit(event, **kwargs):
            record = {'event': event, 'elapsed_seconds': round(time.monotonic() - started, 6), **kwargs}
            stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True, allow_nan=False) + '\n')
            stream.flush()
            os.fsync(stream.fileno())

        try:
            resource.setrlimit(resource.RLIMIT_CPU, (1800, 1800))
            resource.setrlimit(resource.RLIMIT_FSIZE, (16 * 1024 * 1024, 16 * 1024 * 1024))
            uuid, used, utilization = sample()
            emit('gpu_sample', when='before_load', uuid=uuid, used_mib=used, utilization=utilization)
            if used >= 8192 or utilization >= 5:
                raise RuntimeError('GPU admission limit')
            os.environ.update(CUDA_VISIBLE_DEVICES=uuid, HF_HUB_OFFLINE='1',
                              TRANSFORMERS_OFFLINE='1', TOKENIZERS_PARALLELISM='false')
            config = json.loads((ROOT / 'configs/local/parallel_research_pilot.json').read_text())
            model_path = config['model_path']
            if not os.path.isabs(model_path):
                raise ValueError('model path must be absolute')
            import torch
            import transformers
            from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
            emit('loading_start', cases_sha256=CASE_SHA256,
                 script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                 python_version=sys.version.split()[0],
                 torch_version=str(torch.__version__), transformers_version=transformers.__version__)
            tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True, trust_remote_code=False)
            model = AutoModelForCausalLM.from_pretrained(model_path, local_files_only=True,
                                                        trust_remote_code=False, torch_dtype=torch.bfloat16).to('cuda:0')
            model.eval()
            eos = model.generation_config.eos_token_id
            eos = [eos] if isinstance(eos, int) else list(eos or [])
            if not eos or any(type(v) is not int or v < 0 for v in eos):
                raise ValueError('invalid EOS')
            pad = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else eos[0]
            generation = GenerationConfig(do_sample=False, num_beams=1, max_new_tokens=16,
                                          eos_token_id=eos, pad_token_id=pad, use_cache=True)
            identity, used, utilization = sample()
            emit('gpu_sample', when='after_load', uuid=identity, used_mib=used, utilization=utilization)
            if identity != uuid or used >= 43008:
                raise RuntimeError('GPU identity or memory limit')
            template = tokenizer.chat_template
            if not isinstance(template, str) or not template:
                raise ValueError('missing chat template')
            emit('loading_complete', model_type=model.config.model_type, tokenizer_class=type(tokenizer).__name__,
                 chat_template_sha256=hashlib.sha256(template.encode()).hexdigest(),
                 effective_model_config_sha256=hashlib.sha256(model.config.to_json_string().encode()).hexdigest(),
                 eos_ids=eos, generation_config=generation.to_dict())
            signal.signal(signal.SIGALRM, deadline)
            count = 0
            for call in calls:
                key = call['call_id']
                identity, used, utilization = sample()
                emit('gpu_sample', when='before_' + key, uuid=identity, used_mib=used, utilization=utilization)
                if identity != uuid or used >= 43008:
                    raise RuntimeError('GPU identity or memory limit')
                prompt = call['prompt']
                rendered = tokenizer.apply_chat_template([{'role': 'user', 'content': prompt}], tokenize=False,
                                                         add_generation_prompt=True, enable_thinking=False)
                inputs = tokenizer(rendered, return_tensors='pt', add_special_tokens=False, truncation=False)
                ids = inputs['input_ids'][0].tolist()
                if not ids or len(ids) > 1024:
                    raise ValueError('input token limit')
                input_sha = hashlib.sha256(json.dumps(ids, separators=(',', ':')).encode()).hexdigest()
                inputs = {k: v.to('cuda:0') for k, v in inputs.items()}
                emit('prepared', call_id=key, case_id=call['case_id'], family=call['family'],
                     row_format=call['row_format'], output_format=call['output_format'],
                     prompt=prompt, rendered_prompt=rendered, input_token_ids=ids,
                     input_token_sha256=input_sha, mapping=call['mapping'])
                t = time.monotonic()
                emit('call_start', call_id=key)
                signal.setitimer(signal.ITIMER_REAL, 120)
                try:
                    with torch.inference_mode():
                        output = model.generate(**inputs, generation_config=generation,
                                                use_model_defaults=False)[0].tolist()
                finally:
                    signal.setitimer(signal.ITIMER_REAL, 0)
                duration = time.monotonic() - t
                if output[:len(ids)] != ids:
                    raise ValueError('input prefix mismatch')
                suffix = output[len(ids):]
                emit('raw_result', call_id=key, output_token_ids=suffix, seconds=round(duration, 6))
                if not suffix or len(suffix) > 16:
                    raise ValueError('invalid generated length')
                positions = [i for i, value in enumerate(suffix) if value in eos]
                if positions == [len(suffix) - 1]:
                    decoded = tokenizer.decode(suffix[:-1], skip_special_tokens=True,
                                               clean_up_tokenization_spaces=False).strip()
                    pattern = r'A[0-9]{3}' if call['output_format'] == 'bare' else r'\[A[0-9]{3}\]'
                    shape_valid = bool(re.fullmatch(pattern, decoded))
                    id_text = decoded if call['output_format'] == 'bare' else decoded[1:-1]
                    action = call['mapping'].get(id_text) if shape_valid else None
                    category = 'format_mismatch' if not shape_valid else 'id_not_in_mapping' if action is None else 'valid'
                elif not positions and len(suffix) == 16:
                    decoded, action, category = None, None, 'truncated'
                else:
                    raise ValueError('unconfirmed termination')
                emit('decision', call_id=key, case_id=call['case_id'], family=call['family'],
                     row_format=call['row_format'], output_format=call['output_format'],
                     decoded=decoded, action=action, category=category)
                count += 1
                identity, used, utilization = sample()
                emit('gpu_sample', when='after_' + key, uuid=identity, used_mib=used, utilization=utilization)
                if identity != uuid or used >= 43008 or duration >= 120:
                    raise RuntimeError('resource or request limit')
            emit('complete', call_count=count, user_cpu_seconds=resource.getrusage(resource.RUSAGE_SELF).ru_utime,
                 system_cpu_seconds=resource.getrusage(resource.RUSAGE_SELF).ru_stime)
            return 0
        except Exception as exc:
            emit('stopped', error_type=type(exc).__name__,
                 message=str(exc) if type(exc).__name__ in ('RuntimeError', 'ValueError', 'TimeoutError')
                 else 'details omitted')
            return 1


if __name__ == '__main__':
    raise SystemExit(main())
