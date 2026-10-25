"""Prepare only the three current SI-E1 task records; never execute old writers."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess

OWN = Path(__file__).resolve().parent
assert OWN.name == '2026-10-25T102943Z__SOL__si-e1-engineering-review__sie1_b8f6'
BASE = OWN.parents[1]
assert BASE == Path('/home/lizening/research-notes')
STATE = json.loads((OWN / 'START_STATE.json').read_text())
DEV, LUNA = (Path(STATE['directories'][k]) for k in ('sol', 'luna'))
SHA = 'a995d4c3c5f7d31a2cf1fd0afc4bfa4bd72ee3a3'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def command(arguments):
    p = subprocess.run(arguments, cwd=BASE, text=True, capture_output=True)
    assert p.returncode == 0, (arguments, p.returncode, p.stdout, p.stderr)
    return p.stdout

assert command(['git', 'rev-parse', 'HEAD']).strip() == STATE['provenance_start']
assert not command(['git', 'diff', '--name-only']).strip()
assert not command(['git', 'diff', '--cached', '--name-only']).strip()
assert not (OWN / 'publication_preparation.json').exists()
manifest = json.loads((DEV / 'PUBLICATION_MANIFEST.json').read_text())
overrides = json.loads((OWN / 'PUBLICATION_SELECTION_OVERRIDES.json').read_text())
excluded = {r['path'] for r in overrides['excluded_from_author_compact_proposal']}
developer_files = []
for r in manifest['selected_compact_files']:
    p = Path(r['path'])
    assert p.is_relative_to(DEV) and digest(p) == r['sha256'] and p.stat().st_size == r['bytes']
    if str(p) not in excluded:
        developer_files.append(p)
developer_files += [DEV / 'PUBLICATION_MANIFEST.json', DEV / 'FILE_HASHES.sha256']

def own_files(directory):
    return [p for p in directory.rglob('*') if p.is_file() and '__pycache__' not in p.parts
            and p.name not in ('post-push-receipt.json', 'FILE_HASHES.sha256')]

files = sorted(set(developer_files + own_files(LUNA) + [LUNA / 'FILE_HASHES.sha256'] + own_files(OWN)))
assert all(p.is_relative_to(BASE) for p in files)
patterns = {'github_token': r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b',
            'openai_key': r'\bsk-(?:proj-)?[A-Za-z0-9_-]{24,}\b',
            'private_key': r'-----BEGIN (?:OPENSSH |RSA |EC |DSA )?PRIVATE KEY-----'}
whitespace, findings, raw_text_bins = [], [], []
for p in files:
    assert p.stat().st_size <= 1000000, ('oversize', p)
    assert p.suffix not in ('.safetensors', '.pt', '.pth', '.ckpt', '.onnx', '.jsonl', '.tar', '.gz', '.zip'), p
    content = p.read_text(encoding='utf-8')
    if p.suffix == '.bin':
        assert p.is_relative_to(LUNA / 'raw') and p.stat().st_size < 10000
        raw_text_bins.append(str(p.relative_to(BASE)))
    for name, pattern in patterns.items():
        if re.search(pattern, content):
            findings.append({'path': str(p.relative_to(BASE)), 'pattern': name})
    lines = [n for n, line in enumerate(content.splitlines(), 1) if line.rstrip(' \t') != line]
    if lines:
        whitespace.append({'path': str(p.relative_to(BASE)), 'sha256': digest(p), 'line_numbers': lines,
                           'reason': 'Preserve original frozen provenance/raw/Markdown bytes; no scientific-code exception'})
assert not findings, findings
(OWN / 'PROVENANCE_WHITESPACE_REVIEW.json').write_text(json.dumps({
    'status': 'NARROW_PROVENANCE_BYTE_PRESERVATION_EXCEPTIONS', 'files': whitespace,
    'no_scientific_source_whitespace_exception': True}, indent=2) + '\n')
(OWN / 'secret_scan.json').write_text(json.dumps({
    'observed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope': 'intended new task files only; targeted credential/private-key patterns, not exhaustive secrecy proof',
    'patterns': list(patterns), 'file_count': len(files), 'matches': findings,
    'all_selected_files_utf8_text': True, 'explicit_small_original_process_text_bins': raw_text_bins,
    'weights_adapters_cache_dataset_rows_token_arrays_excluded': True}, indent=2) + '\n')
(OWN / 'COMPACT_PUBLICATION_SCOPE.md').write_text('''# SI-E1 publication scope

Publish only these three task directories, their own three INDEX rows and the rolling root FILE_HASHES inventory. Developer proposed allowlist317 is narrowed by PUBLICATION_SELECTION_OVERRIDES.json to omit12 tiny-adapter artifact files, including4 weight files; keep safe software receipts and original hash manifests. Raw synthetic fixture/training-row/token-array trees remain local with size/hash inventories. Luna path/receipt records are included under PUBLICATION_SCOPE_ADJUDICATION.md; the original conservative author inventory is preserved. Small captured .bin files are verified UTF8 process text and explicitly enumerated, never a wildcard model-binary exception.

Records include original draft errors, superseded treatment-invalid software results, authentic failed command receipts and final passing software evidence. They do not claim all historical repository tests pass, new pool yield, real P0/GPU readiness or learning efficacy. No source science, weights, adapters, cache, raw training dataset, genuine new-task payload or credential is uploaded. Historical files and unrelated untracked directories are not selected. The task-local developer hash manifest may reference omitted local artifacts; the rolling root inventory binds the actual published set.

Scientific source a995d4c3 is separately pushed on its own branch. This publication is provenance only and grants no collection, model/environment, training, evaluation, preflight or launch permission. Final remote commit/byte verification is in the ignored local post-push-receipt.json and coordinator response.
''')

index = BASE / 'INDEX.md'
text = index.read_text()
assert OWN.name + '/RECORD.md' not in text
rows = [('SOL', 'SI-E1 independent engineering exact-SHA review and actual S120 audit',
         'PASS_ENGINEERING_ONLY;800/3/77 same historical IDs;97new passed;runtime NOT_READY;0science', OWN),
        ('CODEX / Sol Research', 'SI-E1 single-K1, evidence, paired exposure and P0 continuation contracts',
         'FROZEN_DEVELOPER_DELIVERY;343focused;800/3/77;not independent acceptance;0science', DEV),
        ('LUNA', 'SI-E1 cached tokenizer/background/mask and runtime audit',
         'READ_ONLY_AUDIT_COMPLETE;S120/token mask PASS;runtime NOT_READY;0science', LUNA)]
with index.open('a') as f:
    for agent, title, status, directory in rows:
        f.write(f'| 2026-10-25 10:29:43 | {agent} | {title} | {status} | {SHA} | [RECORD.md]({directory.relative_to(BASE)}/RECORD.md) |\n')

preparation = OWN / 'publication_preparation.json'
preparation.write_text(json.dumps({'status': 'PREPARED_NOT_COMMITTED_OR_PUSHED',
                                   'base_sha': STATE['provenance_start'], 'directories': STATE['directories'],
                                   'intended_files': [], 'explicit_text_bins': raw_text_bins,
                                   'excluded_developer_proposed_files': sorted(excluded)}, indent=2) + '\n')
files = sorted(set(developer_files + own_files(LUNA) + [LUNA / 'FILE_HASHES.sha256'] + own_files(OWN)
                   + [OWN / 'FILE_HASHES.sha256']))
intended = sorted({str(p.relative_to(BASE)) for p in files} | {'INDEX.md', 'FILE_HASHES.sha256'})
data = json.loads(preparation.read_text())
data['intended_files'] = intended
data['new_task_file_count'] = len(files)
preparation.write_text(json.dumps(data, indent=2) + '\n')
root_files = sorted(own_files(OWN))
(OWN / 'FILE_HASHES.sha256').write_text(''.join(f'{digest(p)}  {p.relative_to(OWN)}\n' for p in root_files))
tracked = {p for p in command(['git', 'ls-files', '-z']).split('\0') if p}
inventory = sorted((tracked | set(intended)) - {'FILE_HASHES.sha256'})
assert all((BASE / p).is_file() for p in inventory)
(BASE / 'FILE_HASHES.sha256').write_text(''.join(f'{digest(BASE / p)}  {p}\n' for p in inventory))
print(json.dumps({'status': 'PREPARED_NOT_STAGED', 'new_task_files': len(files),
                  'intended_paths': len(intended), 'root_inventory_entries': len(inventory),
                  'selected_bytes': sum(p.stat().st_size for p in files), 'text_bin_count': len(raw_text_bins),
                  'whitespace_files': len(whitespace), 'secret_matches': findings}, indent=2))
