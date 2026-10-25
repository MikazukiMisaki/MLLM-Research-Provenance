"""Run the candidate historical S adapter with a cached tokenizer, never a model."""
from pathlib import Path
import hashlib
import json
import sys
from transformers import AutoTokenizer
from self_improvement.si_p3.contract import FAMILIES
from self_improvement.si_p3.data import select_background

CODE = Path.cwd().resolve()
assert str(CODE).startswith('/tmp/si-e1-independent-review-')
OWN = Path(__file__).resolve().parent
prior = json.loads((OWN / 'independent_S_background_metadata.json').read_text())
encoded_prior = json.loads((OWN / 'independent_token_mask_check.json').read_text())
rows = {r['task_id']: r for r in prior['rows']}
encoded = {r['task_id']: r for r in encoded_prior['result']['snapshot']['compact_rows']}
manifest = json.loads((CODE / 'configs/sft/sft_accepted_task_splits.json').read_text())
identities = [{'task_id': r['task_id'], 'family': r['task_id'].split('-', 1)[0]}
              for r in manifest['pools']['train'] if r['task_id'].split('-', 1)[0] in FAMILIES]
assert len(identities) == 895
tokenizer = AutoTokenizer.from_pretrained(
    '/home/lizening/.cache/huggingface/hub/models--Qwen--Qwen3-8B/snapshots/b968826d9c46dd6066d109eabc6255188de91218',
    local_files_only=True, trust_remote_code=False)

class Meter:
    def __init__(self, actual):
        self.actual = actual
        self.encoding_calls = self.template_calls = 0
    def __getattr__(self, name):
        return getattr(self.actual, name)
    def __call__(self, *args, **kwargs):
        self.encoding_calls += 1
        return self.actual(*args, **kwargs)
    def apply_chat_template(self, *args, **kwargs):
        self.template_calls += 1
        return self.actual.apply_chat_template(*args, **kwargs)

meter = Meter(tokenizer)
examples = select_background(Path('/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/sft-policy-bootstrap/sft_expert_dataset_balanced.jsonl'),
                             meter, identities, evidence_class='historical')
assert len(examples) == 120 and {r.task_id for r in examples} == set(rows)
for ex in examples:
    r = rows[ex.task_id]
    assert ex.completion == r['completion'] and hashlib.sha256(ex.prompt.encode()).hexdigest() == r['prompt_sha256']
    assert hashlib.sha256(ex.public_prompt.encode()).hexdigest() == r['public_prompt_sha256']
    assert hashlib.sha256(json.dumps(ex.input_ids, separators=(',', ':')).encode()).hexdigest() == encoded[ex.task_id]['input_ids_sha256']
assert sum(len(r.input_ids) for r in examples) == 64922
assert sum(r.prompt_tokens for r in examples) == 64322
assert sum(r.loss_tokens for r in examples) == 600
print(json.dumps({'status': 'PASS_CANDIDATE_ACTUAL_HISTORICAL_S120_ADAPTER',
                  'complete_original_expert_train_nonlight_identities': 895,
                  'all120_selected_id_target_prompt_and_full_token_hashes_match_independent_audit': True,
                  'total_full_input_tokens': 64922, 'total_prompt_tokens': 64322, 'total_shifted_target_tokens': 600,
                  'tokenizer_loads': 1, 'actual_encoding_api_calls': meter.encoding_calls,
                  'actual_template_renders': meter.template_calls,
                  'module_origin': sys.modules['self_improvement.si_p3.data'].__file__,
                  'real_8B_P0_model_environment_training_calls': 0,
                  'future_new_B_C_data_exposure': 'NOT_OBSERVED'}, indent=2))
