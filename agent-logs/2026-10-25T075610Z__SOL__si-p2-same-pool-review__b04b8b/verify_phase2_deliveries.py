"""Independent frozen-delivery joins and rehashing, no peer/project code execution."""
import datetime
import hashlib
import json
from pathlib import Path

OWN = Path(__file__).resolve().parent
SOL = OWN.parent / '2026-10-25T075610Z__CODEX__si-p2-common-quality__b04b8b'
LUNA = OWN.parent / '2026-10-25T075610Z__LUNA__si-p2-pool-independence__b04b8b'


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def read(path):
    return json.loads(path.read_text())


manifests = []
for path in (SOL / 'FILE_HASHES.sha256', LUNA / 'FILE_HASHES.sha256'):
    entries = []
    for line in path.read_text().splitlines():
        expected, name = line.split('  ', 1)
        item = Path(name)
        if not item.is_absolute():
            item = path.parent / item
        actual = sha(item)
        assert actual == expected, (path, item)
        entries.append({'path': str(item), 'sha256': actual})
    manifests.append({'path': str(path), 'sha256': sha(path), 'entries_checked': len(entries), 'all_match': True})

ind = read(OWN / 'independent_pool_audit.json')
peer = read(SOL / 'pool_quality_audit.json')
other = {r['case_id']: r for r in peer['cases']}
comparisons = []
for case in ind['cases']:
    p = other[case['case_id']]
    checks = {'quality': case['Q_hist_independent_pass'] == (p['Q_hist'] == 'PASS'),
              'projection': case['public_projection_sha256'] == p['source_public']['projection_sha256'],
              'target_ID': case['target_action_id'] == p['first_target']['action_id'],
              'target_command': case['target_command'] == p['first_target']['command'],
              'raw_output_hash': case['raw_output_sha256'] == p['first_target']['raw_output_sha256'],
              'anchor': case['anchor_key'] == p['anchor_key'],
              'labels': (case['continue_success'], case['recovery_success']) == (p['labels']['CONTINUE'], p['labels']['recover']),
              'pinned_stratum': (case['Q_hist_independent_pass'] and case['stage'] == 'R19_K1') == (p['Q_pin'] == 'PASS')}
    assert all(checks.values()), (case['case_id'], checks)
    comparisons.append({'case_id': case['case_id'], 'checks': checks})
assert len(comparisons) == 171

sets = read(SOL / 'pool_sets.json')
for name, source in [('Q_hist', ind['Q_hist_flow']),
                     ('Q_pin', ind['Q_pin_R19_candidate_sensitivity_flow'])]:
    expected = source['exact_input_target_dedup']
    assert set(sets[name]['sets']['B']['case_ids']) == set(expected['B_ids'])
    assert set(sets[name]['sets']['C']['case_ids']) == set(expected['C_ids'])
    assert set(sets[name]['sets']['B_minus_C']['case_ids']) == set(expected['B_ids']) - set(expected['C_ids'])

source_bindings = read(SOL / 'complete_input_bindings.json')
for binding in source_bindings:
    assert sha(binding['path']) == binding['sha256_before'] == binding['sha256_after'], binding['path']
for binding in ind['input_bindings']:
    assert sha(binding['path']) == binding['sha256_before'] == binding['sha256_after'], binding['path']

# Identity-only Luna evidence, intentionally not its limited local quality mask.
luna = read(LUNA / 'pool_identity_audit.json')
rows = {r['case_id']: r for r in luna['parent_rows']}
plan = read(LUNA / 'parent_anchor_plan.json')
plan_rows = {r['case_id']: r for r in plan['pre_q_anchor_plan']}
minimum = {}
for case in ind['cases']:
    key = (case['anchor_key'], case['case_id'])
    task = case['canonical_task']
    minimum[task] = min(minimum.get(task, key), key)
for case in ind['cases']:
    r = rows[case['case_id']]
    p = plan_rows[case['case_id']]
    assert case['canonical_task'] == r['canonical_task'] == p['canonical_task']
    assert case['anchor_key'] == r['anchor_key'] == p['anchor_key']
    assert case['continue_success'] == r['continue_success'] == p['continue_success']
    assert case['recovery_success'] == r['recover_success'] == p['recover_success']
    assert p['selected_pre_q_anchor'] == ((case['anchor_key'], case['case_id']) == minimum[case['canonical_task']])
assert len(minimum) == 169
assert sha(LUNA / 'CAP_ROLE_SCOPE_CLARIFICATION_ADDENDUM.md') == 'ab1a7b88ba8e742b95838ed6150ced6ac7263bc3ab97483b755a4c445307797d'
assert sha(SOL / 'CAP_AND_ROLE_INTERPRETATION_ADDENDUM.md') == 'bfa5c1e41e70aa0a36ee0ab657a187b55cd6eef9a08431481ce065c2a522e882'

parent_join = read(OWN / 'independent_parent_identity_join.json')
assert parent_join['all_identity_anchor_family_d_and_label_fields_match']
assert not any(parent_join['expert_task_overlap'].values())
capacity = read(OWN / 'independent_capacity.json')
assert capacity['C_data_rows_tasks'] == 10
assert capacity['C_distinct_first_command_count'] == 6
assert all(r['neutral_only_same_size_possible_diagnostic_not_B_sampling_rule'] for r in capacity['strata'])
model = read(OWN / 'independent_prior_bindings_and_model_axes.json')
assert model['strict_pin_sensitivity_R19_supported_by_original_receipts']
assert len(model['matched_prior_raw_files']) == 14
cap = read(OWN / 'cap_completion_static_evidence.json')
assert len(cap['static_contracts']) == 2 and all(x['executed_2da_AST_equal'] for x in cap['static_contracts'])

paths = [OWN / 'PARENT_COHORT_MANIFEST.json', OWN / 'COMMON_AUDIT_RULES.md',
         OWN / 'ADEQUACY_CRITERIA.md', OWN / 'INDEPENDENT_REVIEW_AND_DECISION.md',
         OWN / 'CAP_AND_ROLE_INTERPRETATION.md', OWN / 'cap_completion_static_evidence.json',
         OWN / 'independent_pool_audit.json', OWN / 'independent_capacity.json',
         OWN / 'independent_prior_bindings_and_model_axes.json', OWN / 'independent_parent_identity_join.json',
         SOL / 'COMMON_QUALITY_AUDIT.md', SOL / 'pool_quality_audit.json', SOL / 'pool_sets.json',
         SOL / 'pipeline_counts.json', SOL / 'FROZEN_HANDOFF.json', SOL / 'RECORD.md',
         SOL / 'CAP_AND_ROLE_INTERPRETATION_ADDENDUM.md',
         LUNA / 'POOL_IDENTITY_AND_CAPACITY.md', LUNA / 'pool_identity_audit.json',
         LUNA / 'parent_anchor_plan.json', LUNA / 'COST_LIMITS_NOT_EXECUTABLE.md', LUNA / 'RECORD.md',
         LUNA / 'CAP_ROLE_SCOPE_CLARIFICATION_ADDENDUM.md']
hist = ind['Q_hist_flow']['exact_input_target_dedup']
pin = ind['Q_pin_R19_candidate_sensitivity_flow']['exact_input_target_dedup']
assert sum(r['Q_hist_independent_pass'] for r in ind['cases']) == 164
assert (hist['rows'], hist['B'], hist['C'], hist['B_minus_C']) == (162, 95, 10, 85)
assert (pin['rows'], pin['B'], pin['C'], pin['B_minus_C']) == (36, 29, 1, 28)
result = {
    'schema': 'SI_P2_INDEPENDENT_REVIEW_V1',
    'completed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'AUDIT_DELIVERY': 'ACCEPT_WITH_CORRECTIONS_AND_SCOPE_LIMITS',
    'POOL_DISTINGUISHABLE': True,
    'LINEAGE_REVIEW': 'PASS_FOR_FROZEN_HISTORICAL_MECHANICAL_CRITERIA_WITH_DISCLOSED_LIMITS',
    'FORMAL_LEARNING_VALIDATION_WITH_CURRENT_POOL': 'NO_GO_RESEARCH_INVESTMENT_DECISION',
    'training_feasibility': 'NOT_ESTABLISHED', 'learning_gain': 'NOT_PROVEN',
    'TRAINING_DATA_READY': 'NOT_READY', 'SCIENTIFIC_EXECUTION': 'NOT_AUTHORIZED',
    'launch_clearance': 'NOT_GRANTED',
    'IMPLEMENTATION_REVIEW': 'NOT_APPLICABLE_NO_SCIENTIFIC_CODE_CHANGE',
    'source_treatment_semantics_changed': False, 'scientific_execution_behavior_changed': False,
    'raw_parent': {'rows': 171, 'tasks': 169, 'B_raw_fields': 99, 'C': 11, 'B_minus_C': 88},
    'Q_hist': {'quality_pass': 164, 'quality_exclude': 7, 'quality_hold': 0,
        'quality_stage_tasks': 162, 'final_rows_tasks': hist['rows'],
        'B': hist['B'], 'C': hist['C'], 'B_minus_C': hist['B_minus_C'],
        'C_families': hist['C_families'], 'C_sources': hist['C_sources']},
    'Q_pin': {'quality_pass': 36, 'final_rows_tasks': pin['rows'],
        'B': pin['B'], 'C': pin['C'], 'B_minus_C': pin['B_minus_C']},
    'C_independent_task_identities': 10,
    'C_model_identity': {'PARTIAL_HISTORICAL': 9, 'PINNED_R19': 1},
    'C_distinct_first_commands': 6, 'C_go_to_desk_1': 5,
    'current_pool_study_capacity': 'Count-level ten-target-per-arm comparison can be described; no equal-token/update sampling/training dataset is approved.',
    'why_no_go': ['Only ten first-action targets across ten task identities, not complete teacher trajectories.',
        'Six light tasks and five identical desk navigation commands; no clean/cool C examples.',
        'Nine historical identities are partial; exact pinned sensitivity has only one C.',
        'Actual supervised tokens/exposure/T/U, independent evaluation space/N and budget remain unfrozen.',
        'Binary value selection within successful recoveries equals selecting baseline failures; no unique value-estimation algorithm is identified.'],
    'no_go_limit': 'Not a theorem that ten examples cannot learn; no arbitrary universal minimum training N was invented.',
    'peer_comparison': {'Sol_rows_with_eight_independent_fields_matched': len(comparisons),
        'Sol_source_inputs_rehashed_unchanged': len(source_bindings),
        'Sol_exact_B_C_neutral_sets_match_both_policies': True,
        'Luna_parent_rows_identity_labels_anchor_matched': 171, 'Luna_preQ_minimum_selections_matched': 169,
        'Luna_local_quality_mask_used': False,
        'Luna_local_81_90_scope': 'Preserved limited branch-locator mask, not the final common quality result or proof of missing source data.',
        'frozen_manifests': manifests},
    'corrections': ['EOS at cap with output_complete=true is complete under original parser; neutral case preserved without altering scientific rules.',
        'Luna additional limited quality mask is not authoritative; original files plus scope addendum remain unchanged.',
        'Raw all-171 success fields99 differ from preliminary97 due R19 ineligible denominator, not changed G4 result.'],
    'r19_cumulative_cost_carried_forward': {'generations': 5142,
        'environment_operations_including_resets': 7949, 'non_reset': 7603, 'resets': 346,
        'incomplete_external_operations': 0, 'includes_predecessor_177_342': True,
        'not_full_project_cost': True},
    'new_scientific_calls': {key: 0 for key in ('model', 'environment', 'tokenizer', 'training',
        'policy_replay', 'G2', 'G3', 'G4', 'preflight', 'project_analyzer', 'project_validator', 'pytest')},
    'next_step': 'Close this historical-pool audit; retain examples as evidence. Controlled new-experience protocol design is a separate task, no collection or training automatically authorized.',
    'artifact_bindings': [{'path': str(path), 'bytes': path.stat().st_size, 'sha256': sha(path)} for path in paths]
}
(OWN / 'independent_peer_comparison.json').write_text(json.dumps({'cases': comparisons, 'all_match': True}, indent=2) + '\n')
(OWN / 'phase2_independent_review.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'decision': result['AUDIT_DELIVERY'], 'POOL_DISTINGUISHABLE': True,
                  'final_B': hist['B'], 'final_C': hist['C'], 'B_minus_C': hist['B_minus_C'],
                  'Q_pin_B_C': [pin['B'], pin['C']],
                  'Sol_field_comparison_rows': len(comparisons), 'Luna_identity_rows': 171,
                  'source_inputs_unchanged': len(source_bindings),
                  'current_pool_formal_learning': result['FORMAL_LEARNING_VALIDATION_WITH_CURRENT_POOL'],
                  'new_scientific_calls': 0}, indent=2))
