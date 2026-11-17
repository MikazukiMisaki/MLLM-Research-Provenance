#!/usr/bin/env python3
"""Prepare small fictional finite-horizon decision cases; no environment or model."""
import json

FOLLOW = 'Select the one currently available action that best executes the frozen immediate subgoal.'
PROGRESS = ('Treat the immediate subgoal as a suggestion. Select one currently available action along a path '
            'toward completing the overall task, including preparatory actions. Prefer such an action that '
            'does not undo a condition already achieved. If undoing an achieved condition is necessary to '
            'complete the task within the remaining steps, allow that undoing. When the suggestion conflicts '
            'with this rule, follow the rule. If an available preparatory action changes object state and '
            'can advance the task, do not choose an action that neither changes object state nor reveals information.')

COMMON = ('Each listed action consumes exactly one step, including the action you choose now. '
          'An action that reaches the goal on the last allowed step counts as success. '
          'Only one object can be held at a time. You can take an object only with an empty hand. '
          'Putting a held object down leaves the hand empty. Look and inventory each consume one step, '
          'change no objects, and reveal no information beyond the stated current state. Facts not explicitly '
          'changed by an action remain unchanged, including cleanliness when taking or putting an object. '
          'There is no automatic placement, swapping, teleporting, or hidden action.')

CASES = [
    {'case_id': 'tight', 'family': 'unnecessary_budget_critical',
     'goal': 'Both A and B are clean and in the target.',
     'state': 'A is clean and in the target. B is clean and at the source. The hand is empty. '
              'Exactly 2 steps remain, including the current action.',
     'rules': 'The target is unobstructed. A held object can be put in the target or at the source. '
              'Taking and putting each consume one action. No other action changes object locations.',
     'actions': ['take B from source', 'take A from target', 'look', 'inventory'],
     'directives': ['Take B from the source.', 'Take A from the target.'],
     'labels': {'rule_consistent': ['take B from source'], 'reversal': ['take A from target'],
                'nonadvancing': ['look', 'inventory'], 'adjudication': 'determinate'}},
    {'case_id': 'wide', 'family': 'unnecessary_budget_slack',
     'goal': 'Both A and B are clean and in the target.',
     'state': 'A is clean and in the target. B is clean and at the source. The hand is empty. '
              'Exactly 4 steps remain, including the current action.',
     'rules': 'The target is unobstructed. A held object can be put in the target or at the source. '
              'Taking and putting each consume one action. No other action changes object locations.',
     'actions': ['take B from source', 'take A from target', 'look', 'inventory'],
     'directives': ['Take B from the source.', 'Take A from the target.'],
     'labels': {'rule_consistent': ['take B from source'], 'reversal': ['take A from target'],
                'nonadvancing': ['look', 'inventory'], 'adjudication': 'determinate'}},
    {'case_id': 'clean', 'family': 'necessary_rollback',
     'goal': 'Both A and B are clean and in the target.',
     'state': 'A and B are both in the target. A is dirty and B is clean. The hand is empty. '
              'Exactly 3 steps remain, including the current action.',
     'rules': 'The only way to clean A is to hold A and use one clean action. '
              'Cleaning A does not put it down. A held object can be put into the target or at the source. '
              'Taking, cleaning, and putting each consume one action. No other action cleans an object.',
     'actions': ['take A from target', 'take B from target', 'look', 'inventory'],
     'directives': ['Take A from the target.', 'Take B from the target.'],
     'labels': {'rule_consistent': ['take A from target'], 'reversal': ['take A from target', 'take B from target'],
                'nonadvancing': ['look', 'inventory'], 'adjudication': 'determinate'}},
    {'case_id': 'unknown', 'family': 'unobserved_obstruction',
     'goal': 'Both A and B are in the target.',
     'state': 'A is in the target and B is at the source. The hand is empty. '
              'Exactly 6 steps remain, including the current action. '
              'A may or may not obstruct B\'s target slot; this cannot currently be observed.',
     'rules': 'If A obstructs B\'s slot, A must be removed and put at the staging area before B can be put '
              'into the target. If A does not obstruct it, B can be put into the target immediately. '
              'After B is in the target, A can be returned to the target without displacing B. '
              'A held object can be put at the source, staging area, or target, subject to the stated '
              'obstruction. Taking and putting each consume one action. No other action changes locations.',
     'actions': ['take A from target', 'take B from source', 'look', 'inventory'],
     'directives': ['Take A from the target.', 'Take B from the source.'],
     'labels': {'rule_consistent': [], 'reversal': ['take A from target'],
                'nonadvancing': ['look', 'inventory'], 'adjudication': 'unknown'}},
]


def main():
    calls = []
    for index, case in enumerate(CASES):
        # Tight and wide differ only in the stated budget, so their mappings match.
        shift = (0, 0, 2, 3)[index]
        ordered = case['actions'][-shift:] + case['actions'][:-shift] if shift else case['actions'][:]
        mapping = {f'A{i:03d}': action for i, action in enumerate(ordered)}
        conditions = [('follow', 0), ('follow', 1), ('progress', 0), ('progress', 1)]
        conditions = conditions[index:] + conditions[:index]
        for contract, directive_index in conditions:
            prompt = (f'{FOLLOW if contract == "follow" else PROGRESS}\n'
                      'Return exactly one bare action ID from the mapping. Do not give an explanation.\n\n'
                      f'Task goal:\n{case["goal"]}\n\nCurrent state:\n{case["state"]}\n\n'
                      f'Action rules:\n{COMMON} {case["rules"]}\n\n'
                      f'Frozen immediate subgoal:\n{case["directives"][directive_index]}\n\n'
                      'Currently available action IDs:\n' +
                      '\n'.join(f'[{key}] {value}' for key, value in mapping.items()) + '\n\nYour response:')
            calls.append({'call_id': f'{case["case_id"]}-{contract}-{directive_index}',
                          'case_id': case['case_id'], 'family': case['family'],
                          'contract': contract, 'directive_index': directive_index,
                          'mapping': mapping, 'labels': case['labels'], 'prompt': prompt})
    if len(calls) != 16 or len({call['call_id'] for call in calls}) != 16:
        raise ValueError('unexpected call schedule')
    print(json.dumps({'schema': 'progress_rule_probe_development_v1', 'calls': calls},
                     ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
