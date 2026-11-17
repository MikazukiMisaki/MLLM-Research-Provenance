#!/usr/bin/env python3
"""Post-hoc text description; does not repair or reclassify invalid model outputs."""
import collections
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def normalize(command):
    return re.sub(r'\bthe\s+', '', command.strip().rstrip('.'), flags=re.IGNORECASE).casefold()


def main():
    calls = json.loads((HERE / 'cases.json').read_text())['calls']
    result = json.loads((HERE / 'results.json').read_text())
    totals = collections.Counter()
    by_case = {}
    for call in calls:
        key = f"{call['contract']}_{call['directive_index']}"
        value = result['by_case'][call['case_id']]['conditions'][key]
        if value['status'] != 'format_invalid':
            raise ValueError('this post-hoc description expects the observed invalid status')
        match = re.fullmatch(r'\[(A[0-9]{3})\]', value['id'] or '')
        if not match or match.group(1) not in call['mapping']:
            raise ValueError('output not a single mapped bracketed ID')
        action = call['mapping'][match.group(1)]
        text = call['prompt'].split('Frozen immediate subgoal:\n', 1)[1].split('\n', 1)[0]
        expected = [a for a in call['mapping'].values() if normalize(a) == normalize(text)]
        if len(expected) != 1:
            raise ValueError('ambiguous textual subgoal')
        followed = action == expected[0]
        totals['bracketed_outputs'] += 1
        totals['mentioned_subgoal_id'] += int(followed)
        labels = call['labels']
        rule_match = None if labels['adjudication'] != 'determinate' else action in labels['rule_consistent']
        if call['contract'] == 'progress' and rule_match is not None:
            totals['progress_rule_judged'] += 1
            totals['progress_rule_matched'] += int(rule_match)
            totals[f"progress_directive_{call['directive_index']}_judged"] += 1
            totals[f"progress_directive_{call['directive_index']}_matched"] += int(rule_match)
        by_case.setdefault(call['case_id'], {})[key] = {
            'recorded_output': value['id'], 'hypothetical_action': action,
            'mentioned_subgoal_id': followed, 'author_progress_rule_match': rule_match}
    pairs = collections.Counter()
    for row in by_case.values():
        for i in (0, 1):
            left, right = row[f'follow_{i}'], row[f'progress_{i}']
            pairs['same_id' if left['recorded_output'] == right['recorded_output'] else 'different_id'] += 1
    return {'status': 'post-hoc text description, not a valid action, parser repair, or environment execution',
            'totals': dict(totals), 'contract_pairs': dict(pairs), 'by_case': by_case}


if __name__ == '__main__':
    print(json.dumps(main(), ensure_ascii=False, indent=2, sort_keys=True))
