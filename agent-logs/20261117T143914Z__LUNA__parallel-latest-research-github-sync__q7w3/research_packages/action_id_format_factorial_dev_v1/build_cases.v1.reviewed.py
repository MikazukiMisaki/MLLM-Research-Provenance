#!/usr/bin/env python3
"""Build fictitious action-ID display/response conditions without model access."""
import json

STATES = [
    ('visible', 'cup', 'cabinet', 'counter'), ('visible', 'bowl', 'shelf', 'table'),
    ('cleaning', 'plate', 'cupboard', 'sink'), ('cleaning', 'pan', 'rack', 'sink'),
    ('holding', 'mug', 'cabinet', 'counter'), ('holding', 'glass', 'shelf', 'table'),
    ('unknown', 'book', 'cabinet', 'left drawer'), ('unknown', 'box', 'shelf', 'upper drawer'),
]
CONDITIONS = (('plain', 'bare'), ('plain', 'bracket'), ('bracket', 'bare'), ('bracket', 'bracket'))


def scenario(family, obj, target, source):
    goal = f'Put both {obj}s in the {target}.'
    inv = 'The hand is empty.'
    if family == 'visible':
        obs = f'The first {obj} is in the {target}. The second {obj} is visible on the {source}.'
        primary = f'take second {obj} from {source}'
        actions = [primary, f'take first {obj} from {target}', 'look', 'inventory']
    elif family == 'cleaning':
        goal = f'Put both clean {obj}s in the {target}.'
        obs = (f'Both {obj}s are in the {target}. The first {obj} is dirty and the second is clean. '
               'Cleaning requires holding the dirty object.')
        primary = f'take first {obj} from {target}'
        actions = [primary, f'take second {obj} from {target}', 'look', 'inventory']
    elif family == 'holding':
        obs = f'The first {obj} is in the {target}; the {target} is accessible.'
        inv = f'The second {obj} is held.'
        primary = f'put second {obj} in {target}'
        actions = [primary, f'put second {obj} on {source}', 'look', 'inventory']
    elif family == 'unknown':
        obs = (f'The first {obj} is in the {target}. The second {obj} is not visible. '
               f'Neither the {source} nor the storage box has been inspected.')
        primary = f'open {source}'
        actions = [primary, 'open storage box', f'take first {obj} from {target}', 'inventory']
    else:
        raise ValueError('unknown case family')
    return goal, obs, inv, primary, actions


def main():
    calls = []
    counts = {}
    for index, (family, obj, target, source) in enumerate(STATES):
        goal, obs, inv, primary, actions = scenario(family, obj, target, source)
        counts[family] = counts.get(family, 0) + 1
        case_id = f'{family}-{counts[family]:02d}'
        shift = index % 4
        ordered = actions[-shift:] + actions[:-shift] if shift else actions[:]
        mapping = {f'A{i:03d}': action for i, action in enumerate(ordered)}
        order = CONDITIONS[shift:] + CONDITIONS[:shift]
        for row_format, output_format in order:
            output_rule = ('Return exactly one action ID without surrounding square brackets. '
                           'Do not output anything else.' if output_format == 'bare' else
                           'Return exactly one action ID enclosed in square brackets. '
                           'Do not output anything else.')
            rows = '\n'.join((key if row_format == 'plain' else f'[{key}]') + '  ' + value
                             for key, value in mapping.items())
            prompt = ('Select the currently available action that best executes the given immediate subgoal.\n'
                      f'{output_rule}\n\nTask goal:\n{goal}\n\nCurrent observation:\n{obs}\n\n'
                      f'Current inventory:\n{inv}\n\nImmediate subgoal:\n{primary.capitalize()}.\n\n'
                      f'Currently available actions:\n{rows}\n\nYour response:')
            calls.append({'call_id': f'{case_id}-{row_format}-{output_format}',
                          'case_id': case_id, 'family': family, 'row_format': row_format,
                          'output_format': output_format, 'mapping': mapping,
                          'specified_action': primary, 'prompt': prompt})
    if len(calls) != 32 or len({call['call_id'] for call in calls}) != 32:
        raise ValueError('invalid schedule')
    print(json.dumps({'schema': 'action_id_format_factorial_dev_v1', 'calls': calls},
                     ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
