"""Prepare developer-owned compact review evidence; does not publish anything."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

own = Path(__file__).resolve().parent
evidence = own / 'evidence'
root = Path('/home/lizening/wt-r19-g4-consumer-contract-repair')
candidate = '85cbb92395e5e2420c2adeb1fa0634653e742910'
base = '2da980f631badc25086d12db60d128ff507d3ae6'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text())

assert read(evidence / 'source_freeze.json')['candidate_source_sha'] == candidate
assert read(evidence / 'remote_equality.json')['local_live_remote_equal']
assert read(evidence / 'regression_comparison.json')['identical_failure_error_ids']
assert read(evidence / 'actual_final.json')['original_inputs_unchanged']
assert read(evidence / 'final_focused.receipt.json')['exit_code'] == 0
assert read(evidence / 'final_full.receipt.json')['exit_code'] == 1
states = {}
for worktree, expected in (
    (root, candidate),
    (Path('/home/lizening/wt-r19-source-contract-review-fixes'), base),
    (Path('/home/lizening/wt-r19-recovery-duration-v1'), base),
    (Path('/home/lizening/wt-codex-r18c2'), 'e537f441010077123a307e9d50ea40cf8dad8547'),
):
    def git(*args):
        return subprocess.check_output(['git', '-C', str(worktree), *args], text=True)
    states[str(worktree)] = {'head': git('rev-parse', 'HEAD').strip(),
                             'branch': git('branch', '--show-current').strip(),
                             'status': git('status', '--porcelain=v1')}
    assert states[str(worktree)]['head'] == expected and not states[str(worktree)]['status']
(evidence / 'final_worktree_states.json').write_text(json.dumps(states, indent=2) + '\n')
(evidence / 'github_connector_remote.json').write_text(json.dumps({
    'tool': 'mcp__codex_apps__github_fetch_commit',
    'request_ref': 'codex/r19-g4-consumer-contract-repair',
    'repo_full_name': 'MikazukiMisaki/Alfworld-Self-Improvement-Project',
    'observed_commit_sha': candidate,
    'observed_commit_html_url': 'https://github.com/MikazukiMisaki/Alfworld-Self-Improvement-Project/commit/' + candidate,
    'note': 'Compact fields transcribed from the successful native connector response; independent live git receipt is separate.'
}, indent=2) + '\n')
synthetic_root = own / 'raw_final_focused/test_fresh_process_synthetic_s0'
destination = evidence / 'synthetic'
destination.mkdir(exist_ok=True)
for relative in ('synthetic_cli_receipt.json', 'synthetic_process_receipt.json',
                 'synthetic_integration_evidence.json', 'report/summary.json',
                 'report/R19_OPPORTUNITY_REPORT.md', 'report/report_hashes.json'):
    source = synthetic_root / relative
    target = destination / Path(relative).name
    shutil.copyfile(source, target)
    assert digest(source) == digest(target)
bindings = {}
assignment = Path('/home/lizening/research-notes/agent-logs/2026-10-23T035119Z__SOL__r19-g4-minimal-contract-repair-assignment__9c5a99')
for path in [*(assignment / name for name in ('SOL_RESEARCH_TASK.md', 'USER_SCOPE_AUTHORIZATION.json',
                                             'observed_state_and_evidence_bindings.json')),
             Path('/home/lizening/research-notes/agent-logs/2026-10-23T041035Z__SOL__r19-g4-fingerprint-test-scope__b0f8de/SCOPE_RULING.md')]:
    bindings[str(path)] = digest(path)
assert bindings[str(assignment / 'SOL_RESEARCH_TASK.md')] == 'd9e3b00a3b83f3a3ac250a5772b3cb41b7c4070f05515e2860218c761f7e02f4'
assert list(bindings.values())[-1] == 'de6a5b81f44c4c3adbecd5e765fded1d0667a8ecb838768c49088ce7ffb6e821'
(evidence / 'authority_bindings.json').write_text(json.dumps(bindings, indent=2) + '\n')
commands = ['# Reversible isolated source setup and freeze; no shared source checkout edits.',
            'git worktree add -b codex/r19-g4-consumer-contract-repair /home/lizening/wt-r19-g4-consumer-contract-repair 2da980f631badc25086d12db60d128ff507d3ae6',
            'git worktree add --detach /home/lizening/wt-r19-g4-consumer-baseline 2da980f631badc25086d12db60d128ff507d3ae6',
            "git add scripts/analyze_r19_recovery_duration.py tests/test_r19_g3_authorization.py tests/test_r19_recovery_duration.py tests/test_r19_g4_consumer_contracts.py",
            "git commit -m 'Support authenticated R19 G4 consumer contracts'",
            '# Below: actual subprocess argv/cwd/exit values, not shell reconstructions.']
for path in sorted(evidence.glob('*.receipt.json')):
    commands.append(json.dumps({'receipt': str(path.relative_to(own)), **read(path)}, sort_keys=True))
commands.append(json.dumps(read(evidence / 'remote_equality.json'), sort_keys=True))
(own / 'commands.log').write_text('\n'.join(commands) + '\n')
handoff = {
    'assignment_identity': '2026-10-23T035119Z__SOL__r19-g4-minimal-contract-repair-assignment__9c5a99',
    'candidate_source_sha': candidate, 'parent_sha': base, 'executed_g3_source_sha': base,
    'executed_g3_run_id': '260422ac02bd42a8b2929d7ef240526b',
    'branch': 'codex/r19-g4-consumer-contract-repair',
    'remote_ref': 'refs/heads/codex/r19-g4-consumer-contract-repair',
    'local_live_remote_equal': True, 'clean_worktree': True,
    'source_treatment_semantics_changed': False,
    'scientific_execution_behavior_changed': False,
    'offline_evidence_validation_behavior_changed': True,
    'science_operations_added': 0,
    'cumulative_scientific_cost_unchanged': {'model_generations': 5142, 'environment_operations': 7949,
                                           'historical_retained_generations': 177, 'historical_retained_operations': 342},
    'developer_checks': {'focused': {'passed': 246, 'exit': 0},
                         'full': {'passed': 703, 'failed': 3, 'errors': 77, 'exit': 1},
                         'exact_2da_full': {'passed': 617, 'failed': 3, 'errors': 77, 'exit': 1},
                         'failure_error_ids_unchanged': 80, 'actual_integrity_validators_returned': 5,
                         'original_input_hash_count': 48, 'original_pre_post_equal': True,
                         'compile_exit': 0, 'diff_check_exit': 0},
    'evidence_paths': {name: str(evidence / name) for name in (
        'source_freeze.json', 'source_delta.patch', 'remote_equality.json',
        'final_focused.log', 'final_focused.receipt.json', 'final_full.log', 'final_full.receipt.json',
        'baseline_full.log', 'baseline_full.receipt.json', 'regression_comparison.json',
        'actual_final.json', 'actual_final.log', 'actual_final.receipt.json',
        'actual_final.pre_hashes.json', 'actual_final.post_hashes.json',
        'synthetic/synthetic_integration_evidence.json', 'synthetic/synthetic_cli_receipt.json')},
    'raw_software_fixture_paths': [str(own / 'raw_final_focused'), str(own / 'raw_final_full'), str(own / 'raw_baseline_full')],
    'coverage_boundary': 'Synthetic CLI runs synthetic branch. Separate wire-format unit fixtures exercise fixed consumer methods; original actual-data calls invoke only the five integrity validators. Actual live CLI statistics/report not executed.',
    'independent_review': 'PENDING_FROZEN_SHA', 'luna_preparation': 'NOT_RELEASED',
    'formal_g4': 'NOT_AUTHORIZED', 'additional_concrete_blocker': None,
    'provenance_publication': 'LOCAL_ONLY_COORDINATOR_RECONCILIATION_PENDING',
    'shared_index_inventory_or_other_agent_files_staged': False,
}
(own / 'HANDOFF.json').write_text(json.dumps(handoff, indent=2) + '\n')
# Compact developer-owned files only; raw fixture trees remain local. No original
# scientific archive, data or model is selected for publication.
selected = [own / 'RECORD.md', own / 'HANDOFF.json', own / 'commands.log',
            *(own / name for name in ('run_check.py', 'actual_integrity_only.py',
                                     'freeze_metadata.py', 'compare_regression.py', 'finalize_evidence.py'))]
selected += [path for path in evidence.rglob('*') if path.is_file()]
secret_markers = re.compile(rb'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9]{32,}')
hits = [str(path.relative_to(own)) for path in selected if secret_markers.search(path.read_bytes())]
assert not hits, hits
(own / 'secret_scan.json').write_text(json.dumps({'status': 'NO_SELECTED_SECRET_MARKER_MATCH',
                                                'pattern_scope': 'private key headers / GitHub tokens / API-key patterns',
                                                'selected_file_count': len(selected), 'hits': hits}, indent=2) + '\n')
selected.append(own / 'secret_scan.json')
inventory = {str(path.relative_to(own)): {'sha256': digest(path), 'bytes': path.stat().st_size}
             for path in sorted(selected)}
(own / 'evidence_inventory.json').write_text(json.dumps(inventory, indent=2) + '\n')
manifest = {'status': 'LOCAL_ONLY_NOT_PUBLISHED', 'owner': 'CODEX_R19_G4_C01_C02',
            'source_sha': candidate, 'root': str(own), 'inventory_sha256': digest(own / 'evidence_inventory.json'),
            'files': sorted([*inventory, 'evidence_inventory.json']),
            'excluded': ['raw_* software fixture trees', 'shared INDEX/root inventory', 'other agents files', 'original G3 archive/data/weights'],
            'coordinator_action': 'Publish only manifest-selected developer files in a separate coordinated commit; do not stage shared files on developer behalf without reconciliation.'}
(own / 'publication_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
hash_paths = [*selected, own / 'evidence_inventory.json', own / 'publication_manifest.json']
(own / 'FILE_HASHES.sha256').write_text(''.join(f'{digest(path)}  {path.relative_to(own)}\n' for path in sorted(hash_paths)))
print(json.dumps({'candidate': candidate, 'handoff_path': str(own / 'HANDOFF.json'),
                  'handoff_sha256': digest(own / 'HANDOFF.json'),
                  'record_sha256': digest(own / 'RECORD.md'), 'selected_files': len(hash_paths),
                  'selected_bytes': sum(path.stat().st_size for path in hash_paths),
                  'publication_manifest_sha256': digest(own / 'publication_manifest.json')}, indent=2))
