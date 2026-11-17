#!/usr/bin/env python3
"""Descriptive paired format-compliance analysis; no model or environment."""
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONDITIONS = ((r, f) for r in ('plain', 'bracket') for f in ('bare', 'bracket'))
CONDITIONS = tuple(CONDITIONS)


def main(path):
    calls = json.loads((HERE / 'cases.json').read_text())['calls']
    expected = {call['call_id']: call for call in calls}
    events = [json.loads(line) for line in Path(path).read_text().splitlines()]
    kinds = ('prepared', 'call_start', 'raw_result', 'decision')
    index = {kind: {} for kind in kinds}
    for event in events:
        kind = event.get('event')
        if kind not in index:
            continue
        key = event.get('call_id')
        if key not in expected or key in index[kind]:
            raise ValueError('unexpected or repeated event')
        index[kind][key] = event
    prepared, started, raw, decisions = (index[kind] for kind in kinds)
    for key, record in prepared.items():
        call = expected[key]
        digest = hashlib.sha256(json.dumps(record['input_token_ids'], separators=(',', ':')).encode()).hexdigest()
        if record['input_token_sha256'] != digest or record['prompt'] != call['prompt'] or record['mapping'] != call['mapping']:
            raise ValueError('prepared input mismatch')
        for name in ('case_id', 'family', 'row_format', 'output_format'):
            if record[name] != call[name]:
                raise ValueError('prepared key mismatch')
    for key, record in decisions.items():
        if key not in prepared or key not in started or key not in raw:
            raise ValueError('decision missing events')
        call = expected[key]
        for name in ('case_id', 'family', 'row_format', 'output_format'):
            if record[name] != call[name]:
                raise ValueError('decision key mismatch')
        value = record['decoded']
        if record['category'] == 'truncated':
            if value is not None or record['action'] is not None:
                raise ValueError('inconsistent truncation')
            continue
        pattern = r'A[0-9]{3}' if call['output_format'] == 'bare' else r'\[A[0-9]{3}\]'
        token = value if call['output_format'] == 'bare' else (value or '')[1:-1]
        shape_valid = bool(value is not None and re.fullmatch(pattern, value))
        expected_action = call['mapping'].get(token) if shape_valid else None
        category = 'format_mismatch' if not shape_valid else 'id_not_in_mapping' if expected_action is None else 'valid'
        if record['action'] != expected_action or record['category'] != category:
            raise ValueError('recorded decision disagrees with fixed parser')
    cases = {}
    totals = {f'{row}_{fmt}': collections.Counter() for row, fmt in CONDITIONS}
    for call in calls:
        key = call['call_id']
        condition = call['row_format'] + '_' + call['output_format']
        decision = decisions.get(key)
        status = decision['category'] if decision else 'unknown' if key in started else 'not_run'
        totals[condition][status] += 1
        text = None if decision is None else decision['decoded']
        pattern = r'A[0-9]{3}' if call['output_format'] == 'bare' else r'\[A[0-9]{3}\]'
        shape = None if decision is None else bool(text is not None and re.fullmatch(pattern, text))
        bare_shape = None if decision is None else bool(text is not None and re.fullmatch(r'A[0-9]{3}', text))
        bare_mapped = None if decision is None else bool(bare_shape and text in call['mapping'])
        action = None if decision is None else decision['action']
        specified = None if action is None else action == call['specified_action']
        for label, matched in (('shape_valid', shape), ('eligible', status == 'valid' if decision else None),
                               ('strict_bare_shape', bare_shape), ('strict_bare_mapped', bare_mapped),
                               ('valid_and_specified', specified)):
            if matched is True:
                totals[condition][label] += 1
        item = {'status': status, 'output': text, 'action': action, 'condition_shape_valid': shape,
                'strict_bare_shape': bare_shape, 'strict_bare_mapped': bare_mapped,
                'matches_specified_subgoal': specified}
        cases.setdefault(call['case_id'], {'family': call['family'], 'conditions': {}})['conditions'][condition] = item
    paired = {}
    for fmt in ('bare', 'bracket'):
        shape_pairs, eligible_pairs, action_pairs = collections.Counter(), collections.Counter(), collections.Counter()
        for case in cases.values():
            left = case['conditions']['plain_' + fmt]
            right = case['conditions']['bracket_' + fmt]
            if left['status'] in ('not_run', 'unknown') or right['status'] in ('not_run', 'unknown'):
                shape_pairs['missing'] += 1
                eligible_pairs['missing'] += 1
            else:
                for counts, lv, rv in ((shape_pairs, left['condition_shape_valid'], right['condition_shape_valid']),
                                       (eligible_pairs, left['status'] == 'valid', right['status'] == 'valid')):
                    counts['both_valid' if lv and rv else 'only_plain' if lv else 'only_bracket' if rv else 'neither_valid'] += 1
            if left['action'] is None or right['action'] is None:
                action_pairs['not_comparable'] += 1
            else:
                action_pairs['same' if left['action'] == right['action'] else 'different'] += 1
        paired[fmt] = {'format_shape': dict(shape_pairs), 'eligible_id': dict(eligible_pairs),
                       'semantic_action': dict(action_pairs)}
    status_names = ('valid', 'format_mismatch', 'id_not_in_mapping', 'truncated', 'unknown', 'not_run')
    measures = ('shape_valid', 'eligible', 'strict_bare_shape', 'strict_bare_mapped', 'valid_and_specified')
    condition_totals = {}
    for key, counts in totals.items():
        statuses = {name: counts[name] for name in status_names}
        observed = sum(statuses[name] for name in ('valid', 'format_mismatch', 'id_not_in_mapping', 'truncated'))
        condition_totals[key] = {'planned': 8, 'observed': observed, 'statuses': statuses,
                                 'measures_among_observed': {name: counts[name] for name in measures}}
    return {'scope': '8 fictional cases, 4 structures; developmental only; no environment or held-out inference',
            'planned_calls': len(calls), 'prepared_calls': len(prepared), 'started_calls': len(started),
            'recorded_decisions': len(decisions), 'journal_completed': bool(events and events[-1].get('event') == 'complete'),
            'condition_totals': condition_totals,
            'row_format_pairs_by_output_requirement': paired, 'by_case': cases}


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: analyze.py JOURNAL')
    print(json.dumps(main(sys.argv[1]), ensure_ascii=False, indent=2, sort_keys=True))
