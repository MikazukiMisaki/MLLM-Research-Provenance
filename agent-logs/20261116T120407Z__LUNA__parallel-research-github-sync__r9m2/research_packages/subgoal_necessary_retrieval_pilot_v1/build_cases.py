#!/usr/bin/env python3
"""Create eight fictional developmental states for a two-condition handoff pilot."""
import json
import sys

PROGRESS = [
 ('teacup','display cupboard','side table'), ('saucer','wall cabinet','worktop'),
 ('glass','wooden hutch','coffee table'), ('mug','metal cupboard','breakfast bar'),
]
REPAIR = [
 ('plate','cupboard','dirty','clean','clean'), ('bowl','hutch','dirty','clean','clean'),
 ('pan','storage cabinet','dirty','clean','clean'), ('vase','glass cabinet','dirty','clean','clean'),
]

def make():
    cases=[]
    for category, settings in [('ordinary',PROGRESS), ('necessary_retrieval',REPAIR)]:
        for i, item in enumerate(settings):
            obj,target,third=item[:3]
            if category=='ordinary':
                place=third
                goal=f'Put both {obj}s in the {target}.'
                observation=f'The {obj} 1 is in the {target}; the {obj} 2 is visible on the {place}. The {target} is accessible.'
                diagnosis=f'The {obj} 2 is not yet in the {target}.'
                first=f'take {obj} 1 from {target}'
                second=f'take {obj} 2 from {place}'
                good,bad=second,first
            else:
                goal=f'Put both clean {obj}s in the {target}.'
                observation=f'The {obj} 1 and {obj} 2 are both in the {target}. The {obj} 1 is dirty; the {obj} 2 is clean. A sink is available. The {target} is accessible.'
                diagnosis=f'The {obj} 1 is dirty and needs cleaning.'
                first=f'take {obj} 1 from {target}'
                second=f'take {obj} 2 from {target}'
                good,bad=first,second
            actions=[good,bad,'look','inventory']
            # Deterministic rotation; normative correct ID is each position once per category.
            actions=actions[-i:]+actions[:-i] if i else actions
            mapping={f'A{k:03}':a for k,a in enumerate(actions)}
            base=('Select the one currently available action that best executes the frozen immediate subgoal.\n'
                'Return exactly one bare action ID in this format:\nAxyz\n'
                'Choose one ID exactly as written in the indexed admissible-action mapping.\n'
                'Do not output a label, command, explanation, reasoning, extra line, or <think> tag.\n\n'
                f'Task goal:\n{goal}\n\nCurrent pre-action observation:\n{observation}\n\n'
                'Current inventory:\n(empty)\n\nRecent action/result transitions (last 4):\n(none)\n\n'
                'Observable recent diagnostics:\nAdjacent repeated actions: 0\nTwo-action cycle events: 0\n\n'
                f'Frozen Stage-1 diagnosis:\n{diagnosis}\n\nFrozen Stage-1 immediate subgoal:\n{{subgoal}}\n\n'
                'Indexed admissible-action mapping:\n'+ '\n'.join(f'[{k}] {v}' for k,v in mapping.items())+'\n\nYour response:')
            case={'case_id':f'{category}-{i+1:02d}','family':category,'mapping':mapping,
                  'goal_consistent_action':good,'conflicting_action':bad,'first_action':first,'second_action':second,
                  'prompts':{condition:base.format(subgoal=command.capitalize()+'.') for condition,command in [('compatible',good),('conflicting',bad)]}}
            cases.append(case)
    return cases
if __name__=='__main__':
    json.dump(make(),sys.stdout,ensure_ascii=False,indent=2,sort_keys=True);print()
