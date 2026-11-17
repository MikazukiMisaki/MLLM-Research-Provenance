#!/usr/bin/env python3
"""Recompute descriptive fictional-case tables from a saved complete or partial journal."""
import collections
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONDITIONS = ('follow_compatible', 'follow_conflicting',
              'task_priority_compatible', 'task_priority_conflicting')


def main(journal):
    schedule = json.loads((HERE / 'cases.json').read_text())['calls']
    expected = {call['call_id']: call for call in schedule}
    events = [json.loads(line) for line in Path(journal).read_text().splitlines()]
    event_maps = {name: {} for name in ('prepared', 'call_start', 'raw_result', 'decision')}
    for record in events:
        event = record.get('event')
        if event not in event_maps:
            continue
        key = record.get('call_id')
        if key not in expected or key in event_maps[event]:
            raise ValueError('unexpected or repeated call event')
        event_maps[event][key] = record
    prepared, started, raw, decisions = (event_maps[x] for x in event_maps)
    for key, record in prepared.items():
        call = expected[key]
        digest = hashlib.sha256(json.dumps(record['input_token_ids'], separators=(',', ':')).encode()).hexdigest()
        if record['input_token_sha256'] != digest or record['prompt'] != call['prompt'] or record['mapping'] != call['mapping']:
            raise ValueError('prepared input mismatch')
        for field in ('case_id', 'family', 'contract', 'subgoal_condition'):
            if record[field] != call[field]:
                raise ValueError('prepared identity mismatch')
    for key, record in decisions.items():
        if key not in prepared or key not in started or key not in raw:
            raise ValueError('decision lacks corresponding events')
        call = expected[key]
        for field in ('case_id', 'family', 'contract', 'subgoal_condition'):
            if record[field] != call[field]:
                raise ValueError('decision identity mismatch')
        action = record['action']
        if action is not None and call['mapping'].get(record['decoded']) != action:
            raise ValueError('action mapping mismatch')
        category = ('acceptable' if action in call['acceptable_actions'] else
                    'local_conflict' if action == call['conflicting_action'] else
                    'other' if action is not None else record['category'])
        if category != record['category'] or category not in ('acceptable', 'local_conflict', 'other',
                                                                'format_invalid', 'truncated'):
            raise ValueError('category mismatch')
    by_case = {}
    totals = {condition: collections.Counter() for condition in CONDITIONS}
    for call in schedule:
        key = call['call_id']
        condition = call['contract'] + '_' + call['subgoal_condition']
        decision = decisions.get(key)
        status = decision['category'] if decision else 'unknown' if key in started else 'not_run'
        totals[condition][status] += 1
        case = by_case.setdefault(call['case_id'], {'family': call['family'], 'conditions': {}})
        case['conditions'][condition] = {'status': status,
                                         'action': None if decision is None else decision['action'],
                                         'id': None if decision is None else decision['decoded']}
    pairs = {}
    for subgoal in ('compatible', 'conflicting'):
        count = collections.Counter()
        for case in by_case.values():
            one = case['conditions']['follow_' + subgoal]['action']
            two = case['conditions']['task_priority_' + subgoal]['action']
            count['not_comparable' if one is None or two is None else 'different' if one != two else 'same'] += 1
        pairs[subgoal] = dict(count)
    return {'scope': '8 previously exposed fictional cases, six structures; no environment or held-out inference',
            'planned_calls': len(schedule), 'prepared_calls': len(prepared), 'started_calls': len(started),
            'recorded_decisions': len(decisions),
            'journal_completed': bool(events and events[-1].get('event') == 'complete'),
            'condition_totals': {k: {'planned': 8, 'counts': dict(v)} for k, v in totals.items()},
            'contract_pairs': pairs, 'by_case': by_case}


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: analyze.py JOURNAL')
    print(json.dumps(main(sys.argv[1]), ensure_ascii=False, indent=2, sort_keys=True))
