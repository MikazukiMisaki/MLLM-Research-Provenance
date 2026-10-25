"""Narrow provenance-only scan, inventories and staging. Never run scientific code."""
import datetime
import hashlib
import json
import re
import subprocess
from pathlib import Path

OWN = Path(__file__).resolve().parent
ROOT = OWN.parent.parent
DIRS = [OWN, OWN.parent / '2026-10-25T065200Z__CODEX__si-p1-eleven-targets__caae4c',
        OWN.parent / '2026-10-25T065200Z__LUNA__si-p1-isolation-budget__caae4c']
BASE = '57747744922bf7d44d0c30f1bd24cb6624f8216e'
RECEIPTS = []


def run(argv):
    r = subprocess.run(argv, cwd=ROOT, capture_output=True)
    RECEIPTS.append({'argv': argv, 'cwd': str(ROOT), 'actual_returncode': r.returncode,
                     'returncode_source': 'subprocess.returncode',
                     'stdout': r.stdout.decode(errors='replace'),
                     'stderr': r.stderr.decode(errors='replace')})
    if r.returncode:
        raise RuntimeError(RECEIPTS[-1])
    return r.stdout


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


assert run(['git', 'rev-parse', 'HEAD']).decode().strip() == BASE
assert not run(['git', 'diff', '--cached', '--name-only']).strip(), 'pre-existing staged changes'
changed = set(run(['git', 'diff', '--name-only']).decode().splitlines())
assert changed <= {'notes/HISTORICAL_CORRECTIONS.md'}, changed
index = ROOT / 'INDEX.md'
body = index.read_text()
marker = '\n## Import omissions\n'
assert body.count(marker) == 1
assert 'si-p1-protocol-review__caae4c' not in body
rows = '''
| 2026-10-25 06:52:00 | SOL | SI-P1 fixed-eleven independent review and minimal protocol/statistical design | ACCEPT_WITH_CORRECTIONS;11 mechanical lineages/10tasks;351 mappings;DATA_NOT_READY;no experiment;5142/7949unchanged | analyzer85cbb923 / G3source2da980f unchanged | [RECORD.md](agent-logs/2026-10-25T065200Z__SOL__si-p1-protocol-review__caae4c/RECORD.md) |
| 2026-10-25 06:52:00 | CODEX / Sol Research | SI-P1 eleven learning-target lineage audit and additive terminal-predicate clarification | 11/11 mechanical lineage;10partial/1pinned model identities;9explicit/2missing rawwon;trainingNOT_READY;no science | analyzer85cbb923 / G3source2da980f unchanged | [RECORD.md](agent-logs/2026-10-25T065200Z__CODEX__si-p1-eleven-targets__caae4c/RECORD.md) |
| 2026-10-25 06:52:00 | LUNA | SI-P1 isolation and budget evidence with additive V2 corrections | Registered mappings closed;known-use complement not clean certificate;P0 scope incident archived/restored;no science | analyzer85cbb923 / G3source2da980f unchanged | [RECORD.md](agent-logs/2026-10-25T065200Z__LUNA__si-p1-isolation-budget__caae4c/RECORD.md) |
'''
index.write_text(body.replace(marker, '\n' + rows + marker))

files = {p for directory in DIRS for p in directory.rglob('*')
         if p.is_file() and '__pycache__' not in p.parts and
         p.name != 'post-push-receipt.json' and p.suffix not in ('.pyc', '.pyo')}
files.update({index, ROOT / 'notes/HISTORICAL_CORRECTIONS.md'})
forbidden_suffixes = {'.safetensors', '.pt', '.pth', '.ckpt', '.onnx', '.bin', '.pem', '.key'}
assert not any(p.suffix in forbidden_suffixes for p in files)
assert max(p.stat().st_size for p in files) < 1048576, 'inspect large files before publication'
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
scan = {'completed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'scope': 'Only proposed new SI-P1 files and intended INDEX/correction content; no full-home scan.',
        'files_scanned_before_generated_inventories': len(files),
        'largest_scanned_file_bytes': max(p.stat().st_size for p in files),
        'targeted_credential_categories': list(patterns), 'findings': findings,
        'status': 'NO_TARGETED_MATCHES' if not findings else 'STOP_REVIEW_REQUIRED',
        'raw_dataset_weights_adapter_cache_imported': False}
(OWN / 'secret_scan.json').write_text(json.dumps(scan, indent=2) + '\n')
assert not findings, findings

files.update({OWN / 'secret_scan.json', OWN / 'publication_preparation.json', OWN / 'FILE_HASHES.sha256'})
planned = sorted(str(path.relative_to(ROOT)) for path in files)
planned.append('FILE_HASHES.sha256')
planned = sorted(set(planned))
prep = {'observed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'provenance_base': BASE, 'scope': 'Only these new task directories, own INDEX rows, corrections and root inventory.',
        'intended_staged_paths': planned, 'expected_staged_path_count': len(planned),
        'preserve_all_other_untracked_paths': True, 'peer_files_not_edited_by_coordinator': True,
        'incident_bytes_preserved_and_original_P0_restored': True,
        'science_or_launch_authorization': False,
        'new_scientific_calls': 0}
(OWN / 'publication_preparation.json').write_text(json.dumps(prep, indent=2) + '\n')
own_files = sorted(p for p in OWN.rglob('*') if p.is_file() and
                   p.name not in ('FILE_HASHES.sha256', 'post-push-receipt.json') and
                   '__pycache__' not in p.parts)
(OWN / 'FILE_HASHES.sha256').write_text(''.join(sha(p) + '  ' + str(p.relative_to(OWN)) + '\n' for p in own_files))
tracked = {ROOT / p.decode() for p in run(['git', 'ls-files', '-z']).split(b'\0') if p}
all_files = tracked | files
all_files.discard(ROOT / 'FILE_HASHES.sha256')
(ROOT / 'FILE_HASHES.sha256').write_text(''.join(sha(p) + '  ' + str(p.relative_to(ROOT)) + '\n' for p in sorted(all_files)))
run(['git', 'add', '--'] + planned)
staged = sorted(run(['git', 'diff', '--cached', '--name-only']).decode().splitlines())
assert staged == planned, {'unexpected': sorted(set(staged) - set(planned)),
                           'missing': sorted(set(planned) - set(staged))}
run(['git', 'diff', '--cached', '--check'])
receipt = {'state': 'STAGED_NOT_COMMITTED', 'prepared_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'base': BASE, 'exact_staged_path_count': len(staged), 'exact_staged_paths': staged,
           'root_inventory_entries': len(all_files), 'own_inventory_entries': len(own_files),
           'subprocess_receipts': RECEIPTS, 'published': False}
(OWN / 'post-push-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({'staged_paths': len(staged), 'root_inventory_entries': len(all_files),
                  'own_inventory_entries': len(own_files), 'credential_findings': 0,
                  'cached_diff_check_exit': 0, 'state': 'STAGED_NOT_COMMITTED'}, indent=2))
