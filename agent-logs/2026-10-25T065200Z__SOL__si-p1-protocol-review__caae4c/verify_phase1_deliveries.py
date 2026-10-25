"""Rehash frozen peer manifests and independent read-only evidence; no peer scripts."""
import datetime
import hashlib
import json
from pathlib import Path

OWN = Path(__file__).resolve().parent
ROOT = OWN.parent.parent
SOL = OWN.parent / '2026-10-25T065200Z__CODEX__si-p1-eleven-targets__caae4c'
LUNA = OWN.parent / '2026-10-25T065200Z__LUNA__si-p1-isolation-budget__caae4c'


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def read(path):
    return json.loads(path.read_text())


inventories = []
for path in [SOL / 'FILE_HASHES.sha256', SOL / 'SUCCESS_AXES_ADDENDUM_HASHES.sha256',
             LUNA / 'FILE_HASHES.sha256', LUNA / 'V2_HASHES.sha256']:
    checked = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        expected, name = line.split('  ', 1)
        item = Path(name)
        if not item.is_absolute():
            item = path.parent / item
        actual = sha(item)
        assert actual == expected, (path, item, 'frozen peer file changed')
        checked.append({'path': str(item), 'sha256': actual})
    inventories.append({'path': str(path), 'sha256': sha(path),
                        'checked_entries': len(checked), 'all_match': True})

audit = read(SOL / 'eleven_target_audit.json')
axes = read(SOL / 'eleven_axes_clarification.json')
assert axes['summary']['input_target_lineage_supported'] == 11
assert axes['frozen_original_audit_sha256'] == sha(SOL / 'eleven_target_audit.json')
assert all(all(case['checks'].values()) for case in audit['cases'])
bindings = []
for binding in audit['input_bindings']:
    path = Path(binding['path'])
    actual = sha(path)
    assert actual == binding['sha256_before'] == binding['sha256_after']
    bindings.append({'path': str(path), 'sha256': actual})

independent = read(OWN / 'independent_target_and_isolation_review.json')
for binding in independent['input_bindings']:
    assert sha(Path(binding['path'])) == binding['sha256_before'] == binding['sha256_after']
assert independent['all_eleven_raw_public_input_target_replay_checks_match']
assert independent['unique_canonical_tasks'] == 10
assert not any(independent['known_use_union_check']['candidate_intersections_with_augmented_known_union'].values())

incident = read(OWN / 'P0_SCOPE_INCIDENT_AND_RESTORATION.json')
for item in incident['items']:
    assert sha(Path(item['snapshot_path'])) == item['observed_sha256']
    path = ROOT / item['path']
    if item['original_sha256']:
        assert sha(path) == item['original_sha256'], ('P0 not restored', path)
    else:
        assert not path.exists(), ('new artifact left in frozen old dir', path)

v2 = read(LUNA / 'corrected_isolation_budget_v2.json')
assert v2['independent_source_identity_join']['sha256'] == sha(OWN / 'independent_source_hash_and_identity_join.json')
assert v2['scope_incident']['incident_receipt_sha256'] == sha(OWN / 'P0_SCOPE_INCIDENT_AND_RESTORATION.json')
assert v2['fixed_case_summary']['rows'] == 11
assert v2['budget_corrections']['r19_cumulative_including_predecessor']['model_generations'] == 5142
assert v2['budget_corrections']['r19_cumulative_including_predecessor']['environment_operations_including_resets'] == 7949
power = read(OWN / 'hypothetical_power_enumeration_v2.json')
assert len(power['rows']) == 112 and all(power['arithmetic_checks'].values())

paths = [SOL / 'ELEVEN_TARGET_AUDIT.md', SOL / 'eleven_target_audit.json',
         SOL / 'SUCCESS_PREDICATE_AND_AXES_ADDENDUM.md', SOL / 'eleven_axes_clarification.json',
         SOL / 'SUCCESS_AXES_FINAL_HANDOFF.md', SOL / 'RECORD.md',
         LUNA / 'CORRECTED_ISOLATION_AND_BUDGET_V2.md', LUNA / 'corrected_isolation_budget_v2.json',
         LUNA / 'KNOWN_USE_IDENTITIES.json', LUNA / 'RECORD.md',
         OWN / 'INDEPENDENT_REVIEW.md', OWN / 'MINIMAL_PROTOCOL_DESIGN.md',
         OWN / 'STATISTICAL_ACCEPTANCE_CRITERIA.md', OWN / 'NEXT_EVIDENCE_SCOPE_DRAFT.md',
         OWN / 'independent_target_and_isolation_review.json',
         OWN / 'independent_source_hash_and_identity_join.json',
         OWN / 'independent_frozen_success_contract.json',
         OWN / 'hypothetical_power_enumeration_v2.json', OWN / 'P0_SCOPE_INCIDENT_AND_RESTORATION.json',
         OWN / 'sol_completion_and_receipt_metadata.json', OWN / 'luna_completion_and_receipt_metadata.json',
         OWN / 'END_STATE_BEFORE_PUBLICATION.json']

result = {
    'schema': 'SI_P1_INDEPENDENT_REVIEW_V1',
    'completed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'decision': 'ACCEPT_WITH_CORRECTIONS__AUDIT_AND_DESIGN_ONLY',
    'IMPLEMENTATION_REVIEW': 'NOT_APPLICABLE_NO_SCIENTIFIC_CODE_DELTA',
    'ELEVEN_TARGET_LINEAGE_REVIEW': 'PASS_11_OF_11_MECHANICAL_WITH_DISCLOSED_PROVENANCE_LIMITS',
    'TASK_ISOLATION_REVIEW': 'REGISTERED_IDENTITIES_JOINED__GLOBAL_NEVER_VIEWED_NOT_PROVEN',
    'COST_REVIEW': 'PASS_CORRECTED_FIELD_SEMANTICS__R19_COST_UNCHANGED',
    'PROTOCOL_DESIGN': 'MINIMAL_STRUCTURE_AND_DECISION_CRITERIA_REVIEWED__EXECUTION_ANNEX_BLOCKED',
    'DATA_FEASIBILITY': 'NOT_READY', 'TRAINING_DATA_READY': 'NOT_READY',
    'EXECUTION_READY': 'NOT_READY', 'launch_clearance': 'NOT_GRANTED',
    'training_and_evaluation_authorized': False,
    'source_treatment_semantics_changed': False,
    'scientific_execution_behavior_changed': False,
    'fixed_states': 11, 'canonical_tasks': 10,
    'public_input_target_replay_checks': '11/11 independently matched',
    'model_identity': {'PARTIAL': 10, 'PINNED': 1},
    'raw_terminal_won': {'EXPLICIT_TRUE': 9, 'NOT_RECORDED': 2},
    'original_frozen_success_labels_retained': True,
    'missing_exported_won_is_new_G3_failure': False,
    'qualified_training_N': 'NOT_ESTABLISHED',
    'registered_identity_union': 2612, 'verified_named_prefix_mappings': 351,
    'unique_tasks_across_named_cohorts': 169,
    'supported_known_use_complements': {'TRAIN': 1141, 'valid_seen': 0, 'valid_unseen': 74},
    'candidate_cleanliness_certified': False,
    'r19_cumulative_physical_cost': {'model_generations': 5142,
        'non_reset_environment_operations': 7603, 'resets': 346,
        'environment_operations_including_resets': 7949, 'incomplete_external_operations': 0,
        'includes_old_177_342': True},
    'frozen_scientific_refs': {'review_root': 'e537f441010077123a307e9d50ea40cf8dad8547',
        'analyzer': '85cbb92395e5e2420c2adeb1fa0634653e742910',
        'executed_G3': '2da980f631badc25086d12db60d128ff507d3ae6'},
    'new_scientific_calls': {key: 0 for key in ['model', 'environment', 'tokenizer', 'training',
        'policy_replay', 'G2', 'G3', 'G4', 'preflight', 'project_validator', 'pytest']},
    'peer_hash_inventories_verified': inventories,
    'sol_source_input_bindings_rehashed': len(bindings),
    'Luna_V1_transient_P0_binding_exception': 'Disclosed snapshot correspondence; not asserted equal to restored old paths.',
    'P0_scope_incident': 'ARCHIVED_AND_RESTORED__ADDITIVE_V2_ACCEPTED',
    'hypothetical_planning': {'scenarios': 112, 'arithmetic_checks': power['arithmetic_checks'],
        'not_full_acceptance_power': True, 'N_or_budget_selected': False},
    'conditions': ['Same-pool common quality/anchor and B_pool distinguishability remain unaudited.',
        'No trained-student effect, generalization or algorithmic novelty demonstrated.',
        'Actual supervised tokens, T/U, exposure caps and single recipe/checkpoint must be frozen.',
        'Independent task space/N, limitations and physical budget need an execution annex.',
        'No automatic retry, post-result sample expansion or reuse of consumed clearance.'],
    'next_evidence_scope': 'Same-pool feasibility only; draft not dispatched, no scientific execution.',
    'artifact_bindings': [{'path': str(path), 'bytes': path.stat().st_size, 'sha256': sha(path)} for path in paths]
}
(OWN / 'phase1_independent_review.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'decision': result['decision'], 'peer_hash_entries': sum(x['checked_entries'] for x in inventories),
                  'peer_manifests': len(inventories), 'Sol_inputs_unchanged': len(bindings),
                  'all_11_independent_checks': True, 'DATA_FEASIBILITY': 'NOT_READY',
                  'new_scientific_calls': 0}, indent=2))
