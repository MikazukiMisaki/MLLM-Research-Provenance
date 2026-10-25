"""Direct production-parser differential; metadata only, no runtime objects."""
from pathlib import Path
import hashlib
import json
import sys

OWN = Path(__file__).resolve().parent
assert OWN.name == '2026-10-25T102943Z__SOL__si-e1-engineering-review__sie1_b8f6'
CODE = Path('/home/lizening/wt-si-p3-engineering-contracts')
files = [CODE / 'src/self_improvement/si_p3/collector.py', CODE / 'src/self_improvement/si_p3/audit.py']
before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
sys.dont_write_bytecode = True
sys.path.insert(0, str(CODE / 'src'))
from self_improvement.si_p3.collector import parse_generation, stage_two_prompt as current_prompt
from self_improvement.si_p3.contract import PublicState, Generation, request
from recovery.two_stage_v2 import parse_bare_stage_two_output, stage_two_prompt as frozen_prompt
from models.protocol_stability import parse_p2_selection

state = PublicState('pick_and_place_simple-SYNTHETIC-None-Shelf-000/trial_SYNTHETIC',
                    'pick_and_place_simple', 'Synthetic goal', 'Synthetic observation', ('wait', 'look'))

def generation(text, complete=True):
    return Generation({'prompt': 'synthetic', 'raw_output': text, 'generated_tokens': 4,
                       'input_tokens': 5, 'latency_seconds': 0.0, 'output_complete': complete,
                       'token_cap_reached': not complete, 'max_new_tokens': 16})

cases = []
for text in ('A001', 'Action-ID: A001'):
    g = generation(text)
    old = parse_bare_stage_two_output(g.record(), state.valid_actions)
    new = parse_generation('stage_two', g, state)
    cases.append({'case': 'teacher_' + text, 'frozen_status': old.status,
                  'draft_status': new['status'], 'equal': old.status == new['status']})
g = generation('A000', complete=False)
old = parse_p2_selection(g.raw['raw_output'], state.valid_actions, reflection_required=False)
for phase in ('source', 'suffix'):
    new = parse_generation(phase, g, state)
    cases.append({'case': phase + '_valid_bare_EOS_incomplete', 'frozen_status': old.selection_status,
                  'draft_status': new['status'], 'equal': old.selection_status == new['status']})
req = request(state, [])
args = {'diagnosis': 'Synthetic diagnosis', 'subgoal': 'Synthetic subgoal', 'stage_one_valid': True}
same_prompt = current_prompt(req, **args) == frozen_prompt(req, **args)
after = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
assert before == after, 'draft changed during probe; preserve this attempt but re-probe frozen bytes'
result = {'classification': 'DRAFT_DIFFERENTIAL_ONLY_NOT_EXACT_SHA_REVIEW', 'before_after_file_sha256': before,
          'teacher_prompt_exactly_frozen_v2': same_prompt, 'cases': cases,
          'confirmed_current_draft_treatment_drift': not same_prompt or not all(c['equal'] for c in cases),
          'activity': 'No model, tokenizer, environment, training or new task payload; only metadata/dataclass/parser calls'}
(OWN / 'draft_semantics_differential.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
