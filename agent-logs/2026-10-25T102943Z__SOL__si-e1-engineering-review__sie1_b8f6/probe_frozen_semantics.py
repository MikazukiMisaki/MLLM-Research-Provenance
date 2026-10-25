"""Independent frozen-checkout parser and reservation checks; no runtime calls."""
from pathlib import Path
import collections
import dataclasses
import hashlib
import json
import subprocess
import sys

CODE = Path.cwd().resolve()
assert str(CODE).startswith('/tmp/si-e1-independent-review-')
sys.dont_write_bytecode = True
sys.path.insert(0, str(CODE / 'src'))
from self_improvement.si_p3.collector import parse_generation, stage_two_prompt as candidate_prompt
from self_improvement.si_p3.contract import PublicState, Generation, request, freeze_plan, plan_hash, ContractError
from self_improvement.si_p3.reservations import bind_reservations
from recovery.two_stage_v2 import parse_bare_stage_two_output, stage_two_prompt as frozen_prompt
from models.protocol_stability import parse_p2_selection

state = PublicState('pick_and_place_simple-SYNTHETIC-None-Shelf-000/trial_SYNTHETIC',
                    'pick_and_place_simple', 'Synthetic goal', 'Synthetic observation', ('wait', 'look'))

def generation(text, complete=True):
    return Generation({'prompt': 'synthetic', 'raw_output': text, 'generated_tokens': 4 if complete else 16,
                       'input_tokens': 5, 'latency_seconds': 0.0, 'output_complete': complete,
                       'token_cap_reached': not complete, 'max_new_tokens': 16})

cases = []
for text in ('A001', 'Action-ID: A001', 'A999', 'A001\nexplanation', ''):
    for complete in (True, False):
        g = generation(text, complete)
        old = parse_bare_stage_two_output(g.record(), state.valid_actions)
        new = parse_generation('stage_two', g, state)
        assert new['status'] == old.status and new['action_id'] == old.action_id and new['command'] == old.action
        cases.append({'phase': 'stage_two', 'raw': text, 'complete': complete, 'status': old.status})
for phase in ('source', 'suffix'):
    for text in ('A000', 'Action-ID: A000', 'A999', 'A000\nexplanation', ''):
        for complete in (True, False):
            g = generation(text, complete)
            old = parse_p2_selection(text, state.valid_actions, reflection_required=False)
            new = parse_generation(phase, g, state)
            assert new['status'] == old.selection_status and new['action_id'] == old.action_id and new['command'] == old.action
            cases.append({'phase': phase, 'raw': text, 'complete': complete, 'status': old.selection_status})
for valid in (True, False):
    args = {'diagnosis': 'Synthetic diagnosis', 'subgoal': 'Synthetic subgoal', 'stage_one_valid': valid}
    assert candidate_prompt(request(state, []), **args) == frozen_prompt(request(state, []), **args)

metadata = Path('/home/lizening/research-notes/agent-logs/2026-10-25T084517Z__SOL__si-p3-controlled-experience-design__si3_7d91/ADOPTED_METADATA_RESERVATIONS.json')
payload = metadata.read_bytes()
assert hashlib.sha256(payload).hexdigest() == '6ce8a32a2345b59ecdef9c28c3a341e9c0801b8105f79895f9b2cb9545a4937e'
rows = [r for r in json.loads(payload)['rows'] if r['partition'] == 'acquisition_feasibility_96']
identities = [{'task_id': r['identity'], 'family': r['family'], 'seed': 42} for r in rows]
plan = bind_reservations(payload, identities)
assert {s.task_id for s in plan} == {r['identity'] for r in rows}
matrix = collections.defaultdict(collections.Counter)
for slot in plan:
    matrix[slot.family][slot.cutoff] += 1
expected = [[9, 9, 9, 8], [7, 6, 6, 7], [4, 4, 4, 4], [2, 3, 2, 2], [2, 2, 3, 3]]
assert [[matrix[family][d] for d in (5, 10, 15, 20)] for family in matrix] == expected
assert sum(s.cutoff for s in plan) == 1200
expected_cutoffs = {}
for family, counts in zip(matrix, expected):
    ordered = sorted((r['identity'] for r in rows if r['family'] == family),
                     key=lambda t: (hashlib.sha256(('SI-P3-prefix-v1\n' + family + '\n' + t + '\n').encode()).hexdigest(), t))
    cuts = [d for d, count in zip((5, 10, 15, 20), counts) for _ in range(count)]
    expected_cutoffs.update(zip(ordered, cuts))
assert all(s.cutoff == expected_cutoffs[s.task_id] for s in plan)
negatives = []
for kind in ('extra_outcome', 'duplicate_identity', 'quota_transfer'):
    change = [dict(x) for x in identities]
    if kind == 'extra_outcome':
        change[0]['Y0'] = 1
    elif kind == 'duplicate_identity':
        change[0] = dict(change[1])
    else:
        change[0]['family'] = 'pick_two_obj_and_place'
    try:
        freeze_plan(change)
    except (ContractError, ValueError):
        negatives.append(kind)
    else:
        raise AssertionError('unsafe metadata admitted: ' + kind)
dev = next(r for r in json.loads(payload)['rows'] if r['partition'] == 'engineering_development_train' and r['family'] == identities[0]['family'])
changed = [dict(x) for x in identities]
changed[0]['task_id'] = dev['identity']
for kind, supplied_payload, supplied_ids, keywords in (
    ('same_family_D48_substitution', payload, changed, {}),
    ('modified_bytes', payload + b'\n', identities, {}),
    ('historical_hash_override', payload, identities, {'synthetic_expected_sha256': hashlib.sha256(payload).hexdigest()}),
):
    try:
        bind_reservations(supplied_payload, supplied_ids, **keywords)
    except ContractError:
        negatives.append(kind)
    else:
        raise AssertionError('reservation binder bypass: ' + kind)
swapped = list(plan)
other = next(i for i, s in enumerate(plan) if s.family == plan[0].family and s.cutoff != plan[0].cutoff)
swapped[0] = dataclasses.replace(plan[0], cutoff=plan[other].cutoff)
swapped[other] = dataclasses.replace(plan[other], cutoff=plan[0].cutoff)
try:
    plan_hash(swapped)
except ContractError:
    negatives.append('cutoff_swap_same_matrix_and_total')
else:
    raise AssertionError('cutoff assignment changed under identical matrix/total')
print(json.dumps({'status': 'PASS_FROZEN_PARSER_AND_REAL_METADATA_INTERFACE_ONLY',
                  'scientific_sha': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                  'parser_differentials': len(cases), 'cases': cases,
                  'stage_two_prompt_exact_v2_both_stage1_validities': True,
                  'actual_canonical_id_set96_preserved': True, 'cut_matrix': dict(matrix),
                  'software_metadata_plan_hash': plan_hash(plan),
                  'seed42_used_only_in_memory_metadata_probe_not_formal_schedule': True,
                  'metadata_negatives_rejected': negatives,
                  'exact_historical_reservation_binder_and_each_identity_cutoff': True,
                  'limit': 'Metadata software proof only. No model, tokenizer, environment or task payload; no actual schedule/launch released.'}, indent=2))
