"""Independent CPU text/collator audit; no model/environment objects or new data."""
from pathlib import Path
import hashlib
import json
import sys

OWN = Path(__file__).resolve().parent
assert OWN.name == '2026-10-25T102943Z__SOL__si-e1-engineering-review__sie1_b8f6'
CODE = Path('/home/lizening/wt-r19-g4-consumer-contract-repair')
DATA = Path('/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/sft-policy-bootstrap/sft_expert_dataset_balanced.jsonl')
LUNA = OWN.parent / '2026-10-25T102943Z__LUNA__si-e1-token-runtime-audit__sie1_b8f6'
OUTPUT = OWN / 'independent_token_mask_check.json'
assert not OUTPUT.exists()

def sha(b):
    return hashlib.sha256(b).hexdigest()

def file_sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda: f.read(2**20), b''):
            h.update(block)
    return h.hexdigest()

assert file_sha(DATA) == 'c547e8f0c5988b29288f2a097169c7859741b7d4f53f222af31f5e2889d516cf'
sys.path.insert(0, str(CODE / 'src'))
from sft.masking import tokenize_prompt_completion
from sft.dataset import render_training_prompt
from transformers import AutoTokenizer
from trl.trainer.sft_trainer import DataCollatorForLanguageModeling
import torch

root_manifest = json.loads((OWN / 'independent_S_background_metadata.json').read_text())
luna_manifest = json.loads((LUNA / 'S_BACKGROUND_MANIFEST.json').read_text())
expected = {r['task_id']: r for r in root_manifest['rows']}
actual = {r['task_id']: r for r in luna_manifest['rows']}
assert len(expected) == len(actual) == 120 and expected.keys() == actual.keys()
for task, r in expected.items():
    l = actual[task]
    assert r['completion'] == l['target_bare_action_id']
    assert r['selected_row_rank_sha256'] == l['row_selection_sha256']
    assert r['prompt_sha256'] == l['prompt_sha256']
    assert r['map_sha256'] == l['indexed_action_map_sha256_recomputed']
    assert r['step_index'] == l['step_index']

selected = {}
with DATA.open() as f:
    for number, line in enumerate(f, 1):
        row = json.loads(line)
        task = row['task_id']
        if task in expected and number == expected[task]['dataset_line_1_based']:
            assert row['completion'] == expected[task]['completion']
            selected[task] = row
assert len(selected) == 120

tokenizer_paths = {
    'snapshot': Path('/home/lizening/.cache/huggingface/hub/models--Qwen--Qwen3-8B/snapshots/b968826d9c46dd6066d109eabc6255188de91218'),
    'p0_final_adapter': Path('/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/model-artifacts/sft-policy-bootstrap/full/final_adapter'),
}
result = {}
signatures = {}
for name, path in tokenizer_paths.items():
    tok = AutoTokenizer.from_pretrained(path, local_files_only=True, trust_remote_code=False)
    encoded = []
    compact = []
    for task in expected:
        row = selected[task]
        assert render_training_prompt(tok, row['public_prompt']) == row['prompt']
        item = tokenize_prompt_completion(tok, row['prompt'], row['completion'], max_length=2048)
        full = len(item['input_ids'])
        prompt = item['completion_mask'].count(0)
        target = item['completion_mask'].count(1)
        assert item['input_ids'][-1] == tok.eos_token_id
        assert item['labels'][:prompt] == [-100] * prompt
        assert item['labels'][prompt:] == item['input_ids'][prompt:]
        assert full <= 2048 and full == actual[task]['token_lengths'][name]['full_tokens']
        compact.append({'task_id': task, 'full': full, 'prompt': prompt, 'target': target,
                        'input_ids_sha256': sha(json.dumps(item['input_ids'], separators=(',', ':')).encode())})
        encoded.append(item)
    collations = []
    for pad in (tok.pad_token_id, tok.eos_token_id):
        batch = DataCollatorForLanguageModeling(pad_token_id=pad, completion_only_loss=True)(encoded)
        assert batch['input_ids'].device.type == 'cpu'
        assert torch.all(batch['labels'][batch['attention_mask'] == 0] == -100)
        per_row = (batch['labels'][:, 1:] != -100).sum(1).tolist()
        assert per_row == [r['target'] for r in compact]
        for i, r in enumerate(compact):
            assert (batch['labels'][i, :r['prompt']] == -100).all()
            assert batch['labels'][i, r['full'] - 1].item() == tok.eos_token_id
            assert (batch['attention_mask'][i, r['full']:] == 0).all()
        collations.append({'pad_id': pad, 'pad_equals_eos': pad == tok.eos_token_id,
                           'shifted_loss_tokens': sum(per_row), 'shape': list(batch['input_ids'].shape),
                           'padding_positions': int((batch['attention_mask'] == 0).sum()), 'pass': True})
    first = selected[next(iter(expected))]
    try:
        tokenize_prompt_completion(tok, first['prompt'], first['completion'], max_length=compact[0]['full'] - 1)
    except ValueError as e:
        assert 'exceeds frozen max_length' in str(e)
        overlength = str(e)
    else:
        raise AssertionError('would-truncate row accepted')
    signatures[name] = compact
    result[name] = {'rows': 120, 'nonpad_full_tokens': sum(r['full'] for r in compact),
                    'nonpad_prompt_tokens': sum(r['prompt'] for r in compact),
                    'target_plus_eos_tokens': sum(r['target'] for r in compact),
                    'target_length_set': sorted({r['target'] for r in compact}),
                    'all_120_masks_checked': True, 'collations': collations,
                    'would_truncate_rejected': overlength,
                    'tokenizer_files': {p.name: file_sha(p) for p in path.iterdir()
                                        if p.name in ('tokenizer.json', 'tokenizer_config.json', 'special_tokens_map.json', 'chat_template.jinja')},
                    'compact_rows': compact}
assert signatures['snapshot'] == signatures['p0_final_adapter']
assert file_sha(DATA) == 'c547e8f0c5988b29288f2a097169c7859741b7d4f53f222af31f5e2889d516cf'
out = {'status': 'PASS_EXISTING_S120_TOKENIZATION_AND_CPU_MASK_ONLY',
       'independent_selection_matches_all_120_luna_rows': True,
       'base_and_adapter_tokenization_identical_for_all_120': True,
       'input_bindings': {str(p): file_sha(p) for p in (DATA, OWN / 'independent_S_background_metadata.json', LUNA / 'S_BACKGROUND_MANIFEST.json')},
       'production_modules': {'masking': sys.modules['sft.masking'].__file__, 'dataset': sys.modules['sft.dataset'].__file__},
       'result': result,
       'accounting': {'tokenizers_loaded': 2, 'selected_rows_encoded_per_tokenizer': 120,
                      'successful_encoding_api_calls': 480, 'overlength_negative_encoding_calls': 4,
                      'cpu_collator_calls': 4, 'actual_8b_or_P0_model_objects': 0,
                      'scientific_generations': 0, 'alfworld_construct_reset_step': 0, 'training_runs': 0},
       'future_new_B_C_data_and_exposure': 'NOT_OBSERVED; no acquisition/train/runtime PASS'}
OUTPUT.write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({k: v for k, v in out.items() if k not in ('result', 'input_bindings')}, indent=2))
print(json.dumps({n: {k: v for k, v in r.items() if k not in ('compact_rows', 'tokenizer_files')} for n, r in result.items()}, indent=2))
