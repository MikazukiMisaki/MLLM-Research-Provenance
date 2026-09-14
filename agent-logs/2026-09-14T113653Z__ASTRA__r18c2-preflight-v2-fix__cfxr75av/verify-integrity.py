"""Read-only scientific and historical integrity checks; saves new task evidence."""
from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone
from infra_helpers import run

P = Path(__file__).resolve().parent
ROOT = P.parents[1]
initial = json.loads((P / 'initial-state.json').read_text())
repo = Path('/home/lizening/Alfworld-Self-Improvement-Project')
runtime = repo / 'artifacts/runtime/validation/progress-aware-r18-c2-formal-aa9fa3c34520941e'
v1 = ROOT / 'agent-logs/2026-09-14T054711Z__ASTRA__r18c2-operational-forensics__nvrcqcpb'
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
science = {}
for key, args in [('branch', ['branch', '--show-current']), ('head', ['rev-parse', 'HEAD']), ('remote', ['rev-parse', 'origin/codex/progress-aware-recovery']), ('status', ['status', '--porcelain=v1'])]:
    r = run(['git', *args], cwd=repo, log='final-integrity.log')
    r.check_returncode()
    science[key] = r.stdout.strip()
assert science == initial['science'], science
current_runtime = {str(f.relative_to(runtime)): {'sha256': sha(f), 'bytes': f.stat().st_size} for f in runtime.rglob('*') if f.is_file()}
assert current_runtime == initial['runtime_files']
current_v1 = {str(f.relative_to(v1)): sha(f) for f in v1.rglob('*') if f.is_file()}
assert current_v1 == initial['v1_files']
baseline = json.loads((P / 'baseline-runtime.json').read_text())
control = repo / 'artifacts/runtime/progress-aware-r18-c2-control'
for name, evidence in baseline['control'].items():
    if isinstance(evidence, dict):
        assert sha(control / name) == evidence['sha256']
for name in initial['reports']:
    assert not (repo / 'reports' / name).exists()
manifest = json.loads((runtime / 'run_manifest.json').read_text())
assert manifest == initial['manifest']
assert not (ROOT / 'r18c2-launch-control/launcher.lock').exists()
result = {'status': 'PASS', 'observed_utc': datetime.now(timezone.utc).isoformat(), 'scientific': science, 'runtime_files': current_runtime, 'runtime_unchanged': True, 'manifest_unchanged': True, 'control_hashes_unchanged': True, 'formal_reports_absent': True, 'v1_files_checked': len(current_v1), 'all_v1_files_unchanged': True, 'real_external_lock_created': False}
(P / 'final-integrity.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
