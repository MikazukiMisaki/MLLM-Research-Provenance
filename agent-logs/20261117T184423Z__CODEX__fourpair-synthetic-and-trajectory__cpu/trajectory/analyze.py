#!/usr/bin/env python3
"""Recount recorded development arms; print only anonymous aggregate data."""
import collections
import hashlib
import json
from pathlib import Path

ROOT = Path('/home/lizening/research-notes/agent-logs/20261118__CODEX__fixed_product_per_arm__private/live-output')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def action_kind(s):
    for prefix in ('go to ', 'take ', 'move ', 'put ', 'examine ', 'look', 'inventory', 'open ', 'close ', 'use ', 'heat ', 'cool ', 'clean '):
        if s == prefix or s.startswith(prefix):
            return prefix.strip()
    return 'other'

def read_arm(path):
    file = path / 'worker/worker_events.jsonl'
    rows = [json.loads(x) for x in file.read_text().splitlines()]
    decisions = [x['payload'] for x in rows if x['kind'] == 'dev_decision_committed']
    actions = [x['action'] for x in decisions]
    generations = [x['payload']['evidence'] for x in rows if x['kind'] == 'generation_returned']
    inputs = sum(len(x['sequence']) - len(x['output_ids']) for x in generations)
    outputs = sum(len(x['output_ids']) for x in generations)
    results = [x['payload'] for x in rows if x['kind'] == 'fixed_product_arm_result']
    statuses = collections.Counter(x['payload']['result']['selection_status'] for x in rows if x['kind'] == 'dev_parser_returned')
    owner_path = path / 'owner/supervisor_events.jsonl'
    owner = [json.loads(x) for x in owner_path.read_text().splitlines()]
    reserved = collections.Counter(x['data']['operation'] for x in owner if x['kind'] == 'operation_reserved')
    returned = collections.Counter(x['data']['operation'] for x in owner if x['kind'] == 'operation_returned')
    return {'actions': actions, 'initial': results[0]['initial_public'] if results else None,
            'stats': {'worker_sha256': sha(file), 'owner_sha256': sha(owner_path), 'won': results[0]['won'] if results else 'UNKNOWN',
                      'termination': results[0]['termination'] if results else 'UNKNOWN', 'steps_committed': len(actions),
                      'generation_returned': len(generations), 'input_token_ids': inputs, 'output_token_ids_including_eos': outputs,
                      'selection_statuses': dict(statuses), 'action_types': dict(collections.Counter(map(action_kind, actions))),
                      'consecutive_identical_pairs': sum(a == b for a,b in zip(actions,actions[1:])),
                      'return_to_action_two_steps_later': sum(a == b for a,b in zip(actions,actions[2:])),
                      'reserved': dict(reserved), 'returned': dict(returned)}}

result = {'scope': 'interrupted, previously exposed and related DEV; not an accepted confirmatory comparison', 'cases': {}}
for letter in 'abc':
    case = ROOT / ('eval-two-pair-' + letter)
    arms = {p.name.split('-',1)[1]:read_arm(p) for p in sorted(case.iterdir()) if p.is_dir()}
    p,c = arms['P0'],arms['CANDIDATE']
    pairs = list(zip(p['actions'],c['actions']))
    first = next((i for i,(a,b) in enumerate(pairs) if a != b), None)
    comparison = {'shared_prefix_same_actions': first if first is not None else len(pairs),
                  'first_divergent_action_step_1based': None if first is None else first+1,
                  'first_divergent_types': None if first is None else {'P0': action_kind(p['actions'][first]), 'CANDIDATE': action_kind(c['actions'][first])},
                  'positional_matches_in_common_prefix_length': sum(a==b for a,b in pairs),
                  'public_initial_equal': p['initial']==c['initial'] if p['initial'] is not None and c['initial'] is not None else 'NOT_COMPARABLE',
                  'input_token_difference_candidate_minus_p0': c['stats']['input_token_ids']-p['stats']['input_token_ids'],
                  'output_token_difference_candidate_minus_p0': c['stats']['output_token_ids_including_eos']-p['stats']['output_token_ids_including_eos']}
    result['cases'][letter] = {'P0':p['stats'], 'CANDIDATE':c['stats'], 'comparison':comparison}
print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))
