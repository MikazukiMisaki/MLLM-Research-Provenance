import hashlib
import json
from pathlib import Path
import re

own = Path(__file__).resolve().parent
paths = {
    'exact_2da_rerun': own / 'evidence/baseline_full.log',
    'archived_2da': Path('/home/lizening/research-notes/agent-logs/2026-10-22T231628Z__CODEX__r19-source-contract-review-fixes__implementation/evidence/final_full_suite.log'),
    'candidate_85cbb92': own / 'evidence/final_full.log',
}

def parse(path):
    raw = path.read_bytes()
    text = raw.decode()
    ids = set()
    for line in text.splitlines():
        if line.startswith(('FAILED tests/', 'ERROR tests/')):
            # Parametrized node IDs may contain spaces: preserve the whole ID.
            kind, node = line.split(' - ', 1)[0].split(' ', 1)
            ids.add((kind, node))
    summaries = [line for line in text.splitlines()
                 if re.search(r'\d+ passed', line) and ' in ' in line]
    return {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(),
            'summary': summaries[-1], 'failure_error_ids': sorted(ids)}

result = {name: parse(path) for name, path in paths.items()}
baseline = set(map(tuple, result['exact_2da_rerun']['failure_error_ids']))
archived = set(map(tuple, result['archived_2da']['failure_error_ids']))
candidate = set(map(tuple, result['candidate_85cbb92']['failure_error_ids']))
result.update(new_failure_error_ids=sorted(candidate - baseline),
              removed_failure_error_ids=sorted(baseline - candidate),
              baseline_matches_archive=baseline == archived,
              identical_failure_error_ids=baseline == candidate,
              historical_failure_error_count=len(baseline))
assert len(baseline) == 80 and baseline == archived and baseline == candidate
before = json.loads((own / 'evidence/actual_baseline.pre_hashes.json').read_text())
after = json.loads((own / 'evidence/actual_final.post_hashes.json').read_text())
common = set(before) & set(after)
assert common and all(before[path] == after[path] for path in common)
result['common_original_paths_unchanged_across_baseline_and_candidate'] = len(common)
(own / 'evidence/regression_comparison.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({name: value['summary'] for name, value in result.items() if name in paths}, indent=2))
print('Exact historical failure/error ID set unchanged:', len(baseline))
