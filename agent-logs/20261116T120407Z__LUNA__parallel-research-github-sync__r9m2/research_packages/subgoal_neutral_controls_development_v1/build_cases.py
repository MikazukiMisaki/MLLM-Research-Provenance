#!/usr/bin/env python3
"""Prepare fictional developmental handoff cases; no model or environment."""
import json
import sys

SCENARIOS = [
 ('visible', 'cup', 'cupboard', 'counter'), ('visible', 'bowl', 'hutch', 'table'),
 ('cleaning', 'plate', 'cabinet', 'sink'), ('cleaning', 'pan', 'cupboard', 'sink'),
 ('obstruction', 'box', 'chest', 'workbench'), ('holding', 'mug', 'cabinet', 'table'),
 ('completed', 'glass', 'cabinet', 'table'), ('unknown', 'book', 'cabinet', 'desk drawer'),
]
NEUTRAL='Act appropriately for the task, given the current situation.'

def make():
    result=[]
    family_counts={}
    for i,(family,obj,target,other) in enumerate(SCENARIOS):
        goal=f'Put both {obj}s in the {target}.'
        diag=''
        inv='(empty)'
        if family=='visible':
            obs=f'The {obj} 1 is in the {target}; the {obj} 2 is visible on the {other}. The {target} is accessible.'
            diag=f'The {obj} 2 is not yet in the {target}.'
            good=f'take {obj} 2 from {other}'; bad=f'take {obj} 1 from {target}'
            options=[good,bad,'look','inventory']; acceptable=[good]
        elif family=='cleaning':
            goal=f'Put both clean {obj}s in the {target}.'
            obs=f'The {obj} 1 and {obj} 2 are in the {target}; the {obj} 1 is dirty and the {obj} 2 is clean. The {target} and {other} are accessible. Cleaning requires holding the object at the sink.'
            diag=f'The {obj} 1 is dirty and needs cleaning.'
            good=f'take {obj} 1 from {target}';bad=f'take {obj} 2 from {target}'
            options=[good,bad,'look','inventory'];acceptable=[good]
        elif family=='obstruction':
            obs=f'The {obj} 1 is in the {target} and blocks its entry. The {obj} 2 is on the {other}; both objects fit once rearranged. First moving {obj} 1 aside makes the entry accessible.'
            diag=f'The {obj} 1 blocks access for the {obj} 2.'
            good=f'take {obj} 1 from {target}';bad=f'take {obj} 2 from {other}'
            options=[good,bad,'look','inventory'];acceptable=[good]
        elif family=='holding':
            obs=f'The {obj} 1 is in the {target}; the {target} is open and accessible.'
            inv=f'The {obj} 2 is held.'
            diag=f'The {obj} 2 is held and not yet placed.'
            good=f'put {obj} 2 in {target}';bad=f'put {obj} 2 on {other}'
            options=[good,bad,'look','inventory'];acceptable=[good]
        elif family=='completed':
            obs=f'Both {obj} 1 and {obj} 2 are already in the {target}. The task goal is already satisfied.'
            diag='The stated task goal is already satisfied.'
            good='look';bad=f'take {obj} 1 from {target}'
            options=[good,bad,'inventory',f'take {obj} 2 from {target}'];acceptable=['look','inventory']
        else:
            obs=f'The {obj} 1 is in the {target}. The {obj} 2 is not visible and its location is unknown. The {other} and the storage drawer have not been inspected; both may be opened.'
            diag=f'The location of {obj} 2 is unknown.'
            good=f'open {other}';bad=f'take {obj} 1 from {target}'
            options=[good,bad,'open storage drawer','inventory'];acceptable=[good,'open storage drawer']
        # Rotate the primary acceptable action through each numbered position.
        shift=i%4
        ordered=options[-shift:]+options[:-shift] if shift else options
        mapping={f'A{j:03d}':action for j,action in enumerate(ordered)}
        base=('Select the one currently available action that best executes the frozen immediate subgoal.\n'
            'Return exactly one bare action ID in this format:\nAxyz\n'
            'Choose one ID exactly as written in the indexed admissible-action mapping.\n'
            'Do not output a label, command, explanation, reasoning, extra line, or <think> tag.\n\n'
            f'Task goal:\n{goal}\n\nCurrent pre-action observation:\n{obs}\n\n'
            f'Current inventory:\n{inv}\n\nRecent action/result transitions (last 4):\n(none)\n\n'
            'Observable recent diagnostics:\nAdjacent repeated actions: 0\nTwo-action cycle events: 0\n\n'
            f'Frozen Stage-1 diagnosis:\n{diag}\n\nFrozen Stage-1 immediate subgoal:\n{{subgoal}}\n\n'
            'Indexed admissible-action mapping:\n'+'\n'.join(f'[{k}] {v}' for k,v in mapping.items())+'\n\nYour response:')
        prompts={condition:base.format(subgoal=text) for condition,text in
                 [('compatible',good.capitalize()+'.'),('conflicting',bad.capitalize()+'.'),('neutral',NEUTRAL)]}
        family_counts[family]=family_counts.get(family,0)+1
        result.append({'case_id':f'{family}-{family_counts[family]:02d}','family':family,'mapping':mapping,
                       'goal_consistent_action':good,'conflicting_action':bad,
                       'acceptable_actions':acceptable,'prompts':prompts})
    return result
if __name__=='__main__':
    json.dump(make(),sys.stdout,ensure_ascii=False,indent=2,sort_keys=True);print()
