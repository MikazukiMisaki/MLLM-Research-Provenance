#!/usr/bin/env python3
"""Recompute a fictional progress-rule probe without invoking a model or environment."""
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def normalize(command):
    return re.sub(r'\bthe\s+', '', command.strip().rstrip('.'), flags=re.IGNORECASE).casefold()


def main(journal):
    schedule = json.loads((HERE / 'cases.json').read_text())['calls']
    expected = {call['call_id']: call for call in schedule}
    events = [json.loads(line) for line in Path(journal).read_text().splitlines()]
    kinds = ('prepared', 'call_start', 'raw_result', 'decision')
    maps = {kind: {} for kind in kinds}
    for event in events:
        kind = event.get('event')
        if kind not in maps:
            continue
        key = event.get('call_id')
        if key not in expected or key in maps[kind]:
            raise ValueError('unexpected or duplicate event')
        maps[kind][key] = event
    prepared, started, raw, decisions = (maps[kind] for kind in kinds)
    for key, record in prepared.items():
        call = expected[key]
        digest = hashlib.sha256(json.dumps(record['input_token_ids'], separators=(',', ':')).encode()).hexdigest()
        if record['input_token_sha256'] != digest or record['prompt'] != call['prompt'] or record['mapping'] != call['mapping']:
            raise ValueError('prepared input mismatch')
        for field in ('case_id', 'family', 'contract', 'directive_index'):
            if record[field] != call[field]:
                raise ValueError('prepared identity mismatch')
    for key, record in decisions.items():
        if key not in prepared or key not in started or key not in raw:
            raise ValueError('decision lacks supporting events')
        call = expected[key]
        for field in ('case_id', 'family', 'contract', 'directive_index'):
            if record[field] != call[field]:
                raise ValueError('decision identity mismatch')
        if record['action'] is not None and call['mapping'].get(record['decoded']) != record['action']:
            raise ValueError('action mapping mismatch')
        if record['category'] not in ('valid', 'format_invalid', 'truncated'):
            raise ValueError('unknown generation status')
        if (record['category'] == 'valid') != (record['action'] is not None):
            raise ValueError('generation status disagrees with action')
    cases = {}
    for call in schedule:
        key = call['call_id']
        decision = decisions.get(key)
        action = None if decision is None else decision['action']
        status = decision['category'] if decision else 'unknown' if key in started else 'not_run'
        text = call['prompt'].split('Frozen immediate subgoal:\n', 1)[1].split('\n', 1)[0]
        targets = [value for value in call['mapping'].values() if normalize(value) == normalize(text)]
        if len(targets) != 1:
            raise ValueError('subgoal cannot be mapped uniquely')
        labels = call['labels']
        rule_match = None if action is None or labels['adjudication'] != 'determinate' else action in labels['rule_consistent']
        # Finite-horizon reachability is an author-specified separate dimension.
        reachability = None
        if action is not None:
            if call['case_id'] == 'tight':
                reachability = action == 'take B from source'
            elif call['case_id'] == 'wide':
                reachability = True
            elif call['case_id'] == 'clean':
                reachability = action == 'take A from target'
        entry = {'status': status, 'action': action, 'id': None if decision is None else decision['decoded'],
                 'subgoal_followed': None if action is None else action == targets[0],
                 'external_progress_rule_match': rule_match,
                 'reversal': None if action is None else action in labels['reversal'],
                 'nonadvancing': None if action is None else action in labels['nonadvancing'],
                 'author_budget_reachable': reachability}
        case = cases.setdefault(call['case_id'], {'family': call['family'],
                                                  'adjudication': labels['adjudication'], 'conditions': {}})
        case['conditions'][f"{call['contract']}_{call['directive_index']}"] = entry
    paired = {}
    for i in (0, 1):
        counts = collections.Counter()
        for case in cases.values():
            one = case['conditions'][f'follow_{i}']['action']
            two = case['conditions'][f'progress_{i}']['action']
            counts['not_comparable' if one is None or two is None else 'different' if one != two else 'same'] += 1
        paired[str(i)] = dict(counts)
    return {'scope': 'four fictional cases, three structures; no environment or held-out inference',
            'planned_calls': len(schedule), 'prepared_calls': len(prepared), 'started_calls': len(started),
            'recorded_decisions': len(decisions),
            'journal_completed': bool(events and events[-1].get('event') == 'complete'),
            'contract_pairs_by_directive': paired, 'by_case': cases}


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: analyze.py JOURNAL')
    print(json.dumps(main(sys.argv[1]), ensure_ascii=False, indent=2, sort_keys=True))
