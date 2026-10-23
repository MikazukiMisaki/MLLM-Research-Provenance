"""Capture source delta and immutable review bindings, no scientific operations."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess

own = Path(__file__).resolve().parent
root = Path('/home/lizening/wt-r19-g4-consumer-contract-repair')
base = '2da980f631badc25086d12db60d128ff507d3ae6'
expected = '85cbb92395e5e2420c2adeb1fa0634653e742910'

def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args])

def digest(data):
    return hashlib.sha256(data).hexdigest()

assert git('rev-parse', 'HEAD').decode().strip() == expected
assert git('rev-parse', 'HEAD^').decode().strip() == base
assert not git('status', '--porcelain=v1')
paths = git('diff', '--name-only', base, expected).decode().splitlines()
assert set(paths) == {'scripts/analyze_r19_recovery_duration.py', 'tests/test_r19_recovery_duration.py',
                      'tests/test_r19_g4_consumer_contracts.py', 'tests/test_r19_g3_authorization.py'}
patch = git('diff', '--binary', base, expected)
(own / 'evidence/source_delta.patch').write_bytes(patch)

def methods(source):
    text = source.decode()
    return {node.name: digest(ast.get_source_segment(text, node).encode())
            for node in ast.parse(text).body if isinstance(node, (ast.FunctionDef, ast.ClassDef))}

analyzer = 'scripts/analyze_r19_recovery_duration.py'
before = methods(git('show', base + ':' + analyzer))
after = methods((root / analyzer).read_bytes())
changed = {name: {'old': before.get(name), 'new': after.get(name)}
           for name in sorted(set(before) | set(after)) if before.get(name) != after.get(name)}
assert set(changed) == {'validate_live_execution_provenance', 'validate_live_exit_receipt',
                        '_validate_local_inference_runtime', '_supervisor_option',
                        '_read_supervisor_object', '_validate_supervisor_launch_context'}
record = {'candidate_source_sha': expected, 'parent_source_sha': base,
          'executed_g3_source_sha': base, 'branch': git('branch', '--show-current').decode().strip(),
          'worktree': str(root), 'clean_worktree': True,
          'source_treatment_semantics_changed': False, 'scientific_execution_behavior_changed': False,
          'offline_evidence_validation_behavior_changed': True, 'independent_review': 'PENDING',
          'luna_preparation': 'NOT_RELEASED', 'formal_g4': 'NOT_AUTHORIZED',
          'diff_sha256': digest(patch), 'changed_production_methods': changed,
          'changed_files': {path: {'new_sha256': digest((root / path).read_bytes()),
                                   'old_sha256': digest(git('show', base + ':' + path))
                                   if path != 'tests/test_r19_g4_consumer_contracts.py' else None}
                            for path in paths}}
(own / 'evidence/source_freeze.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
