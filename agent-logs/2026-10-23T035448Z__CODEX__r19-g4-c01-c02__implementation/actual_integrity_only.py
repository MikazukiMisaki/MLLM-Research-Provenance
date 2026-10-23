"""Read-only original G3 integrity calls. No main/statistics/report invocation."""
import hashlib
import json
from pathlib import Path
import runpy
import sys
import subprocess
import traceback

own = Path(__file__).resolve().parent
candidate = Path(sys.argv[1]).resolve()
label = sys.argv[2]
assignment = Path('/home/lizening/research-notes/agent-logs/2026-10-23T035119Z__SOL__r19-g4-minimal-contract-repair-assignment__9c5a99')
bound = json.loads((assignment / 'observed_state_and_evidence_bindings.json').read_text())['exact_byte_sha256']
output = Path('/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z')
supervisor = Path('/home/lizening/research-notes/agent-logs/2026-10-23T002200Z__LUNA__r19-g3-live-successor__2da980f/supervisor_live')
paths = set(map(Path, bound)) | set(p for p in output.rglob('*') if p.is_file()) | set(p for p in supervisor.rglob('*') if p.is_file())
paths |= {assignment / name for name in ('SOL_RESEARCH_TASK.md', 'USER_SCOPE_AUTHORIZATION.json', 'observed_state_and_evidence_bindings.json')}
paths |= set((candidate / 'configs/experiments').glob('r19*.json'))
paths |= set((candidate / 'configs/experiments/r19_preflight_v3').glob('*.json'))
paths |= {candidate / 'R19_PROTOCOL.md'}
launch = json.loads((supervisor / 'launch_context.json').read_text())
original_root = Path(launch['cwd'])
for option in ('--protocol', '--manifest', '--config'):
    paths.add(Path(launch['command_argv'][launch['command_argv'].index(option) + 1]))
paths.add(original_root / 'R19_PROTOCOL.md')
restart = json.loads((candidate / 'configs/experiments/r19_b1_g3_source_contract_restart_authorization_v1.json').read_text())
predecessor = original_root / restart['predecessor']['output_relative_path']
paths |= {p for p in predecessor.rglob('*') if p.is_file()}

def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()

def hashes():
    return {str(path): digest(path) for path in sorted(paths)}

before = hashes()
assert all(before[path] == value for path, value in bound.items())
assert digest(assignment / 'SOL_RESEARCH_TASK.md') == 'd9e3b00a3b83f3a3ac250a5772b3cb41b7c4070f05515e2860218c761f7e02f4'
(own / 'evidence' / (label + '.pre_hashes.json')).write_text(json.dumps(before, indent=2) + '\n')
module = runpy.run_path(str(candidate / 'scripts/analyze_r19_recovery_duration.py'))
import recovery.r19_duration as duration
assert Path(duration.__file__).resolve() == candidate / 'src/recovery/r19_duration.py'
assert module['PROJECT_ROOT'] == candidate
result = {'class': 'ENGINEERING_ACTUAL_DATA_INTEGRITY_ONLY', 'scientific_analysis_invoked': False,
          'argv': sys.argv,
          'candidate_source_sha': subprocess.check_output(['git', '-C', str(candidate), 'rev-parse', 'HEAD'], text=True).strip(),
          'candidate_analyzer': str(candidate / 'scripts/analyze_r19_recovery_duration.py'),
          'analyzer_sha256': digest(candidate / 'scripts/analyze_r19_recovery_duration.py'),
          'origins': {'recovery.r19_duration': duration.__file__}, 'checks': {}}

def check(name, function):
    try:
        value = function()
        result['checks'][name] = {'engineering_status': 'RETURNED', 'result': value}
        print(name, 'RETURNED', flush=True)
        return value
    except Exception:
        result['checks'][name] = {'engineering_status': 'REJECTED', 'traceback': traceback.format_exc()}
        print(name, result['checks'][name]['traceback'], flush=True)
        return None

def read(name):
    return json.loads((output / name).read_text())

try:
    events = module['_read_jsonl'](output / 'execution_events.jsonl')
    branches = module['_read_jsonl'](output / 'branches.jsonl')
    physical = check('validate_event_ledger', lambda: module['validate_event_ledger'](events, expected_evidence_class='live'))
    branch = check('validate_branch_evidence', lambda: module['validate_branch_evidence'](branches, events, return_operation_ids=True))
    operations = branch.pop('_operation_event_ids') if branch else []
    schedule_path = candidate / 'configs/experiments/r19_preflight_v3/source_schedule.json'
    exclusions_path = candidate / 'configs/experiments/r19_preflight_v3/exclusion_manifest.json'
    protocol_path = candidate / 'configs/experiments/r19_recovery_duration_v1.json'
    if physical is not None and branch is not None:
        check('validate_live_source_schedule', lambda: module['validate_live_source_schedule'](
            json.loads(schedule_path.read_text()), json.loads(exclusions_path.read_text()), events, operations, physical))
    if physical is not None:
        check('validate_live_execution_provenance', lambda: module['validate_live_execution_provenance'](
            execution_manifest=read('execution_manifest.json'), runtime_manifest=read('runtime_manifest.json'),
            environment_manifest=read('environment_manifest.json'), schedule_path=schedule_path,
            exclusion_path=exclusions_path, protocol_path=protocol_path,
            events_path=output / 'execution_events.jsonl', branches_path=output / 'branches.jsonl',
            g3_gate_receipt_path=output / 'g3_gate_receipt.json', events=events, physical=physical))
    check('validate_live_exit_receipt', lambda: module['validate_live_exit_receipt'](
        json.loads((supervisor / 'runner_exit.json').read_text()), events=events,
        protocol_sha256=digest(protocol_path), events_path=output / 'execution_events.jsonl',
        branches_path=output / 'branches.jsonl', receipt_path=supervisor / 'runner_exit.json',
        supervisor_status_path=supervisor / 'supervisor_status.json', runner_log_path=supervisor / 'runner.log'))
finally:
    after = hashes()
    result['original_inputs_unchanged'] = before == after
    (own / 'evidence' / (label + '.post_hashes.json')).write_text(json.dumps(after, indent=2) + '\n')
    (own / 'evidence' / (label + '.json')).write_text(json.dumps(result, indent=2) + '\n')
assert before == after
sys.exit(0 if len(result['checks']) == 5 and all(value['engineering_status'] == 'RETURNED' for value in result['checks'].values()) else 1)
