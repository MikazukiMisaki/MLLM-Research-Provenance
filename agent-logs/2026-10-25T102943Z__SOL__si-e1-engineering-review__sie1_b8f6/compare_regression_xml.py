"""Compare raw JUnit outcomes rather than trusting a developer's summary."""
from pathlib import Path
import collections
import hashlib
import json
import sys
import xml.etree.ElementTree as ET

OWN = Path(__file__).resolve().parent
assert OWN.name == '2026-10-25T102943Z__SOL__si-e1-engineering-review__sie1_b8f6'
baseline, candidate, output_name = sys.argv[1:]
assert Path(output_name).name == output_name and not (OWN / output_name).exists()

def read(path):
    content = Path(path).read_bytes()
    outcomes = {}
    for case in ET.fromstring(content).iter('testcase'):
        key = case.attrib.get('classname', '') + '::' + case.attrib['name']
        state = next((name for name in ('error', 'failure', 'skipped') if case.find(name) is not None), 'passed')
        assert key not in outcomes, ('duplicate test case', key)
        outcomes[key] = state
    return outcomes, hashlib.sha256(content).hexdigest()

before, before_sha = read(baseline)
after, after_sha = read(candidate)
bad = lambda x: {k: v for k, v in x.items() if v in ('error', 'failure')}
old_bad, new_bad = bad(before), bad(after)
added = {k: v for k, v in new_bad.items() if k not in old_bad}
changed = {k: {'old': old_bad[k], 'new': v} for k, v in new_bad.items() if k in old_bad and old_bad[k] != v}
removed = sorted(set(old_bad) - set(new_bad))
result = {'status': 'PASS_NO_NEW_FAILURE_ERROR_IDS' if not added and not changed else 'FAIL_NEW_OR_CHANGED_FAILURE_ERROR_IDS',
          'baseline': {'path': baseline, 'sha256': before_sha, 'counts': dict(collections.Counter(before.values()))},
          'candidate': {'path': candidate, 'sha256': after_sha, 'counts': dict(collections.Counter(after.values()))},
          'new_failure_error_ids': added, 'changed_failure_error_kind': changed,
          'removed_failure_error_ids': removed,
          'same_historical_failure_error_id_set': old_bad == new_bad,
          'missing_baseline_test_ids': sorted(set(before) - set(after)),
          'added_passing_ids': sorted(k for k in after if k not in before and after[k] == 'passed'),
          'historical_failure_error_ids': old_bad,
          'limit': 'Historical missing artifacts not repaired; new path must not require them. Separate focused/protocol review required.'}
(OWN / output_name).write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k not in ('historical_failure_error_ids', 'added_passing_ids')}, indent=2))
sys.exit(0 if not added and not changed and not result['missing_baseline_test_ids'] else 1)
