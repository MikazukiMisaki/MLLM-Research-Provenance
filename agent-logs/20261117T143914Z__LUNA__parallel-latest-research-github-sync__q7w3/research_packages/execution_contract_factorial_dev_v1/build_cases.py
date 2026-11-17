#!/usr/bin/env python3
"""Build prospective, fictional execution-contract comparisons; no model calls."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'subgoal_neutral_controls_development_v1' / 'cases.json'
SOURCE_SHA256 = '03a9fee21f68605bb83467c41573e91997220366fe52e1173daf02cb857cc5eb'
ORIGINAL = 'Select the one currently available action that best executes the frozen immediate subgoal.'
PRIORITY = ('Select the one currently available action that best advances the overall task goal. '
            'If the frozen immediate subgoal conflicts with the task goal or the current situation, '
            'prioritize the task goal.')
CONDITIONS = ('follow_compatible', 'follow_conflicting',
              'task_priority_compatible', 'task_priority_conflicting')


def main():
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError('source cases changed')
    source = json.loads(raw)
    if len(source) != 8 or len({case['case_id'] for case in source}) != 8:
        raise ValueError('expected eight distinct source case IDs')
    calls = []
    for index, case in enumerate(source):
        mapping = case['mapping']
        values = list(mapping.values())
        if len(mapping) != 4 or len(set(values)) != 4:
            raise ValueError('invalid action mapping')
        if case['conflicting_action'] not in values or not set(case['acceptable_actions']) <= set(values):
            raise ValueError('unmapped action label')
        if case['conflicting_action'] in case['acceptable_actions']:
            raise ValueError('overlapping label sets')
        shift = index % 4
        order = CONDITIONS[shift:] + CONDITIONS[:shift]
        for condition in order:
            contract, subgoal = condition.rsplit('_', 1)
            prompt = case['prompts'][subgoal]
            if not prompt.startswith(ORIGINAL + '\n') or prompt.count(ORIGINAL) != 1:
                raise ValueError('original contract does not match exactly once')
            if contract == 'task_priority':
                prompt = PRIORITY + prompt[len(ORIGINAL):]
            elif contract != 'follow':
                raise ValueError('invalid contract')
            calls.append({
                'call_id': case['case_id'] + '-' + condition,
                'case_id': case['case_id'], 'family': case['family'],
                'contract': contract, 'subgoal_condition': subgoal,
                'prompt': prompt, 'mapping': mapping,
                'acceptable_actions': case['acceptable_actions'],
                'conflicting_action': case['conflicting_action'],
            })
    if len(calls) != 32 or len({call['call_id'] for call in calls}) != 32:
        raise ValueError('invalid planned call schedule')
    output = {'schema': 'fictional_contract_factorial_dev_v1',
              'source_sha256': SOURCE_SHA256, 'calls': calls}
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
