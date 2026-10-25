"""Resume narrow provenance staging; retain exact immutable raw-log whitespace."""
import datetime
import hashlib
import json
import re
import subprocess
from pathlib import Path

OWN = Path(__file__).resolve().parent
assert OWN.name == '2026-10-25T075610Z__SOL__si-p2-same-pool-review__b04b8b'
ROOT = OWN.parent.parent
DIRS = [OWN, OWN.parent / '2026-10-25T075610Z__CODEX__si-p2-common-quality__b04b8b',
        OWN.parent / '2026-10-25T075610Z__LUNA__si-p2-pool-independence__b04b8b']
BASE = '34109ab3f950d321a80b6e70c5905a95c55a4034'
RECEIPTS = []


def run(argv):
    r = subprocess.run(argv, cwd=ROOT, capture_output=True)
    RECEIPTS.append({'argv': argv, 'cwd': str(ROOT), 'actual_returncode': r.returncode,
                     'returncode_source': 'subprocess.returncode',
                     'stdout': r.stdout.decode(errors='replace'), 'stderr': r.stderr.decode(errors='replace')})
    if r.returncode:
        raise RuntimeError(RECEIPTS[-1])
    return r.stdout


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


prep = json.loads((OWN / 'publication_preparation.json').read_text())
assert run(['git', 'rev-parse', 'HEAD']).decode().strip() == BASE
assert run(['git', 'diff', '--cached', '--name-only']).decode().splitlines() == prep['intended_staged_paths']
assert set(run(['git', 'diff', '--name-only']).decode().splitlines()) <= set(prep['intended_staged_paths'])
exception = json.loads((OWN / 'publication_whitespace_exception.json').read_text())
raw_log = exception['exception_paths'][0]
assert exception['actual_returncode'] == 2 and len(exception['expected_diagnostics']) == 2
expected_log_hash = None
for line in (DIRS[1] / 'FILE_HASHES.sha256').read_text().splitlines():
    expected, name = line.split('  ', 1)
    path = Path(name)
    if not path.is_absolute():
        path = DIRS[1] / path
    if path == ROOT / raw_log:
        expected_log_hash = expected
assert expected_log_hash is not None and sha(ROOT / raw_log) == expected_log_hash

files = {p for directory in DIRS for p in directory.rglob('*') if p.is_file()
         and '__pycache__' not in p.parts and p.suffix not in ('.pyc', '.pyo')
         and p.name != 'post-push-receipt.json'}
files.update({ROOT / 'INDEX.md', ROOT / 'notes/HISTORICAL_CORRECTIONS.md'})
assert max(p.stat().st_size for p in files) < 10 * 1048576
large = json.loads((OWN / 'large_metadata_payload_review.json').read_text())['files']
assert {str(p) for p in files if p.stat().st_size > 1048576} == {item['path'] for item in large}
assert all(sha(Path(item['path'])) == item['sha256'] for item in large)
patterns = {
    'github_token': re.compile(rb'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})'),
    'api_key': re.compile(rb'sk-[A-Za-z0-9_-]{24,}'),
    'private_key': re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'literal_bearer': re.compile(rb'(?i)authorization\s*[:=]\s*[\x22\x27]?bearer\s+[A-Za-z0-9._-]{20,}'),
    'aws_access_key': re.compile(rb'AKIA[0-9A-Z]{16}')}
findings = []
for path in sorted(files):
    raw = path.read_bytes()
    for category, regex in patterns.items():
        if regex.search(raw):
            findings.append({'path': str(path.relative_to(ROOT)), 'category': category})
assert not findings, findings
(OWN / 'secret_scan.json').write_text(json.dumps({'completed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status': 'NO_TARGETED_MATCHES', 'files_scanned': len(files), 'findings': findings,
    'targeted_categories': list(patterns), 'reviewed_metadata_files_over1MB': large,
    'no_raw_dataset_weights_adapter_or_cache_imported': True}, indent=2) + '\n')
planned = sorted({str(path.relative_to(ROOT)) for path in files} | {'FILE_HASHES.sha256'})
prep.update({'intended_staged_paths': planned, 'expected_staged_path_count': len(planned),
             'resume_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'immutable_raw_log_whitespace_exception': {'path': raw_log,
                 'strict_diff_check_returncode': 2, 'diagnostics': exception['expected_diagnostics'],
                 'original_bytes_preserved': True}})
(OWN / 'publication_preparation.json').write_text(json.dumps(prep, indent=2) + '\n')
own_files = sorted(p for p in OWN.rglob('*') if p.is_file() and
                   p.name not in ('FILE_HASHES.sha256', 'post-push-receipt.json') and '__pycache__' not in p.parts)
(OWN / 'FILE_HASHES.sha256').write_text(''.join(sha(p) + '  ' + str(p.relative_to(OWN)) + '\n' for p in own_files))
tracked = {ROOT / name.decode() for name in run(['git', 'ls-files', '-z']).split(b'\0') if name}
all_files = (tracked | files) - {ROOT / 'FILE_HASHES.sha256'}
(ROOT / 'FILE_HASHES.sha256').write_text(''.join(sha(p) + '  ' + str(p.relative_to(ROOT)) + '\n' for p in sorted(all_files)))
run(['git', 'add', '--'] + planned)
assert run(['git', 'diff', '--cached', '--name-only']).decode().splitlines() == planned
run(['git', 'diff', '--cached', '--check', '--', '.', ':(exclude)' + raw_log])
# Independently keep the author's frozen manifest byte checks, including raw log.
for directory in DIRS[1:]:
    for line in (directory / 'FILE_HASHES.sha256').read_text().splitlines():
        expected, name = line.split('  ', 1)
        path = Path(name)
        if not path.is_absolute():
            path = directory / path
        assert sha(path) == expected
receipt = {'state': 'STAGED_NOT_COMMITTED', 'published': False, 'base': BASE,
           'prepared_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'exact_staged_paths': planned, 'exact_staged_path_count': len(planned),
           'root_inventory_entries': len(all_files), 'own_inventory_entries': len(own_files),
           'subprocess_receipts': RECEIPTS, 'strict_diff_check_exception': exception,
           'all_other_content_diff_check_actual_returncode': 0, 'new_scientific_calls': 0}
(OWN / 'post-push-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({'staged_paths': len(planned), 'root_inventory_entries': len(all_files),
                  'raw_log_whitespace_preserved': True, 'all_other_diff_check_exit': 0,
                  'credential_findings': 0, 'state': 'STAGED_NOT_COMMITTED'}, indent=2))
