"""Independent read-only stdlib audit of existing 11 targets and known-use joins.

Peer references are locators, not accepted truth: rehash files/lines, derive public
input and raw target, and compare existing replay. No project imports or calls.
No training examples, full prompts, tokenizer, schedules, or outcome analysis.
"""
import collections
import datetime
import hashlib
import json
import re
from pathlib import Path

OWN = Path(__file__).resolve().parent
SOL = OWN.parent / '2026-10-25T065200Z__CODEX__si-p1-eleven-targets__caae4c'
LUNA = OWN.parent / '2026-10-25T065200Z__LUNA__si-p1-isolation-budget__caae4c'
BINDINGS = {}


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def bind(path):
    path = Path(path)
    if str(path) not in BINDINGS:
        BINDINGS[str(path)] = {'path': str(path), 'bytes': path.stat().st_size,
                              'sha256_before': digest(path)}
    return path


def load(path):
    return json.loads(bind(path).read_text())


def field_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                    separators=(',', ':'), ensure_ascii=True).encode()).hexdigest()


def rawrow(path, number, expected=None):
    with bind(path).open('rb') as stream:
        for index, raw in enumerate(stream, 1):
            if index == number:
                actual = hashlib.sha256(raw).hexdigest()
                if expected is not None:
                    assert actual == expected, (path, number, 'row hash')
                return json.loads(raw)
    raise AssertionError((path, number, 'missing line'))


def pointer(obj, ptr):
    for part in (ptr or '').split('/')[1:]:
        part = part.replace('~1', '/').replace('~0', '~')
        obj = obj[int(part)] if isinstance(obj, list) else obj[part]
    return obj


def reference(ref):
    row = rawrow(ref['path'], ref['line'], ref['raw_line_sha256'])
    return pointer(row, ref.get('pointer'))


def canonical(task):
    parts = str(task).rstrip('/').split('/')
    for index in range(len(parts) - 1, 0, -1):
        if parts[index].startswith('trial_'):
            return parts[index - 1] + '/' + parts[index]
    return str(task)


def public_text(goal, observation, transitions, commands):
    recent = '\n\n'.join('Action: ' + item['action'] + '\nResult: ' +
                         item['resulting_observation'] for item in transitions) or '(none)'
    actions = '\n'.join('[' + key + '] ' + value for key, value in commands.items())
    return ('You are an ALFWorld household agent. Select exactly one next action.\n'
            'Return exactly one bare action ID in the form Axyz. Do not output a label, command, explanation, reasoning, or <think> tags.\n\n'
            'Task goal:\n' + goal + '\n\nCurrent observation:\n' + observation +
            '\n\nRecent action/result transitions (last 4):\n' + recent +
            '\n\nIndexed admissible actions:\n' + actions + '\n\nYour response:')


fixed = load(OWN / 'FIXED_ELEVEN_CASES.json')
assert digest(OWN / 'FIXED_ELEVEN_CASES.json') == 'e5039568d8213fa5d879ffb2aec8c44e932fa99bc4de67bd527ebcae67ccb45b'
peer = load(SOL / 'eleven_target_audit.json')
peer_cases = {case['case_id']: case for case in peer['cases']}
assert {case['case_id'] for case in fixed['cases']} == set(peer_cases)
results = []
for case in fixed['cases']:
    audit = peer_cases[case['case_id']]
    branch = rawrow(case['source_path'], case['source_line'], case['source_row_sha256'])
    source = reference(audit['source_episode']['reference'])
    d = case['decision_index']
    steps, stage = source['steps'], case['stage']
    state = steps[d]
    actions = state['valid_actions']
    commands = {f'A{i:03d}': command for i, command in enumerate(actions)}
    history = [{'action': steps[i]['action'], 'resulting_observation': steps[i + 1]['observation']}
               for i in range(max(0, d - 4), d)]
    policy = state.get('metadata', {}).get('policy') or state.get('policy_metadata') or {}
    projection = {'goal': source['task']['text'], 'observation': state['observation'],
                  'recent_action_result_transitions': history,
                  'ordered_action_map': list(commands.items())}
    checks = {
        'canonical_task': canonical(source['task']['task_id']) == case['canonical_task'],
        'pre_action_nonterminal': not any(step['done'] for step in steps[:d]),
        'horizon': case['remaining_horizon'] == 50 - d,
        'public_projection_sha': field_hash(projection) == audit['public_projection']['projection_sha256'],
        'stored_P0_public_prompt': public_text(source['task']['text'], state['observation'], history, commands) == policy.get('prompt'),
    }
    replay = reference(audit['existing_replay']['source'])
    if stage == 'R4':
        teacher = branch['raw_generations']['recovery']['stage_two']
        generation, parsed = teacher['generation'], teacher['parsed']
        action_id, command, mapping = parsed['action_id'], parsed['action'], parsed['id_to_command']
        executed = branch['recover']['recovery_action']
        terminal = branch['recover']['continuation']['steps'][-1]
        checks['execution_flag'] = branch['recover']['recovery_action_executed']
        trace = replay['transitions']
        checks['replay_prefix'] = (len(trace) == d and replay['replay_match'] and
            all(t['action'] == steps[i]['action'] and t['replayed_observation'] == steps[i]['observation']
                and t['resulting_observation'] == steps[i + 1]['observation'] and t['exact']
                for i, t in enumerate(trace)))
        checks['replay_current_state'] = replay['branch_observation'] == state['observation'] and replay['branch_valid_actions'] == actions and replay['replay_recent_context'] == history
        recorded_success = branch['recover']['success']
    elif stage in ('R10_OSR', 'R16_OSR'):
        teacher = branch['recovery_full']['stage_two']
        generation, parsed = teacher['generation'], teacher['parsed']
        action_id, command, mapping = parsed['action_id'], parsed['action'], parsed['id_to_command']
        executed = branch['recovery_mapped_command']
        suffix = branch['continuation_full']['steps']
        terminal = suffix[-1] if suffix else branch['recovery_transition']
        checks['execution_flag'] = branch['recovery_action_executed']
        recorded_success = branch['r_osr']
        if stage == 'R10_OSR':
            trace = replay['transitions']
            checks['replay_prefix'] = (len(trace) == d and replay['replay_match'] and
                all(t['action'] == steps[i]['action'] and t['observation_before'] == steps[i]['observation']
                    and t['resulting_observation'] == steps[i + 1]['observation'] and t['exact']
                    for i, t in enumerate(trace)))
            checks['replay_current_state'] = replay['branch_observation'] == state['observation'] and replay['branch_valid_actions'] == actions and replay['replay_recent_context'] == history
        else:
            checks['replay_prefix'] = replay['replay_match'] and len(replay['transition_checks']) == d and all(all(t[k] for k in ('action_admissible', 'action_map_equal', 'done_equal', 'observation_equal', 'result_observation_equal', 'reward_equal', 'truncated_equal')) for t in replay['transition_checks'])
            checks['replay_current_state'] = (replay['current_observation_sha256'] == hashlib.sha256(state['observation'].encode()).hexdigest() and replay['current_indexed_action_map_sha256'] == field_hash(commands) and replay['recent_k4_context_sha256'] == field_hash(history))
    else:
        arm = branch['k_results']['1']
        generation = reference(audit['first_recovery_target']['generation_source'])
        parsed_ref = dict(audit['first_recovery_target']['generation_source'])
        parsed_ref['pointer'] = '/payload/evidence'
        parsed = reference(parsed_ref)
        action_id, command, mapping = parsed['action_id'], parsed['command'], parsed['id_to_command']
        transition_ref = dict(audit['first_recovery_target']['transition_source'])
        transition_ref['pointer'] = '/payload/action'
        action = reference(transition_ref)
        executed = action['command']
        terminal = reference(audit['terminal_corroboration']['recovery_branch_terminal']['source'])
        checks['recovery_before_state'] = (action['history_before'] == [[step['observation'], step['action']] for step in steps[:d]] and action['observation_before'] == state['observation'] and action['valid_actions_before'] == actions and action['action_map'] == commands and action['actions_consumed_before'] == d and action['recovery_action_index'] == 1)
        wanted = set(replay['replay_transition_event_ids'])
        events = {}
        path = audit['existing_replay']['source']['path']
        with bind(path).open('rb') as stream:
            for raw in stream:
                if b'"event_id"' not in raw:
                    continue
                event = json.loads(raw)
                if event['event_id'] in wanted:
                    events[event['event_id']] = event['payload']
        trace = [events[event_id] for event_id in replay['replay_transition_event_ids']]
        checks['replay_prefix'] = len(trace) == d and replay['replay_match'] and all(t['command'] == steps[i]['action'] and t['before_state']['observation'] == steps[i]['observation'] and t['before_state']['valid_actions'] == steps[i]['valid_actions'] and t['transition']['observation'] == steps[i + 1]['observation'] for i, t in enumerate(trace))
        recorded_success = arm['success']
    target = audit['first_recovery_target']
    checks.update({
        'teacher_full_map': commands == mapping,
        'raw_ID_valid': bool(re.fullmatch(r'A\d{3}', generation['raw_output'].strip())) and generation['raw_output'].strip() == action_id,
        'raw_ID_command_execution': commands.get(action_id) == command == executed == target['mapped_command'],
        'generation_complete': generation['output_complete'] is True and generation['token_cap_reached'] is False,
        'parser_selected': parsed['status'] == 'selected',
        'original_recovery_success_predicate': terminal['done'] is True and terminal['reward'] > 0 and int(recorded_success) == 1,
    })
    control = reference(audit['terminal_corroboration']['CONTINUE_terminal']['source'])
    checks['original_continue_failure_predicate'] = control['done'] is True and control['reward'] == 0
    assert all(checks.values()), (case['case_id'], [key for key, value in checks.items() if not value])
    results.append({'case_id': case['case_id'], 'canonical_task': case['canonical_task'],
                    'checks': checks, 'public_projection_sha256': field_hash(projection),
                    'action_id': action_id, 'command': command,
                    'peer_disposition_preserved': audit['disposition'],
                    'terminal_axis_preserved': audit['terminal_corroboration']['axis'],
                    'review_scope': 'Original frozen done/reward predicate supported; explicit raw won missing is separate, not a new G3 error. No training approval.'})

# Metadata-only corroboration that newly closed historical mappings do not
# invalidate the already reported known-use complement. Not a clean certificate.
known = load(LUNA / 'KNOWN_USE_IDENTITIES.json')
join = load(OWN / 'independent_source_hash_and_identity_join.json')
members = known['registered_identity_members']
registered = set().union(*(set(value) for value in members.values() if isinstance(value, list)))
cohort_tasks = {row['canonical_task'] for stage in join['stage_proofs'].values() for row in stage['units']}
snap = load(OWN / 'P0_SCOPE_INCIDENT_SNAPSHOT/SUPPORTED_IDENTITY_CANDIDATES.json')
candidates = {split: {item['identity'] for item in rows} for split, rows in snap.items()}
overlap = {split: sorted(ids & (registered | cohort_tasks)) for split, ids in candidates.items()}
assert not any(overlap.values()), overlap
same_task_groups = collections.defaultdict(list)
for result in results:
    same_task_groups[result['canonical_task']].append(result['case_id'])
for value in BINDINGS.values():
    value['sha256_after'] = digest(value['path'])
    value['unchanged'] = value['sha256_before'] == value['sha256_after']
assert all(item['unchanged'] for item in BINDINGS.values())
output = {'schema': 'SI_P1_COORDINATOR_INDEPENDENT_TARGET_REVIEW_V1',
          'observed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'cases': results, 'all_eleven_raw_public_input_target_replay_checks_match': True,
          'unique_canonical_tasks': len(same_task_groups),
          'same_task_groups': {task: ids for task, ids in same_task_groups.items() if len(ids) > 1},
          'known_use_union_check': {'registered_union_tasks': len(registered),
                                  'mapped_cohort_unique_tasks': len(cohort_tasks),
                                  'mapped_tasks_not_previously_in_known_union': sorted(cohort_tasks - registered),
                                  'candidate_complement_counts': {key: len(value) for key, value in candidates.items()},
                                  'candidate_intersections_with_augmented_known_union': overlap,
                                  'clean_or_historical_never_seen_certification': 'NOT_PROVEN'},
          'input_bindings': list(BINDINGS.values()),
          'new_scientific_calls': 0,
          'qualified_training_N': 'NOT_ESTABLISHED', 'execution_authorized': False}
(OWN / 'independent_target_and_isolation_review.json').write_text(json.dumps(output, indent=2) + '\n')
print(json.dumps({'raw_target_checks': '11/11', 'unique_tasks': len(same_task_groups),
                  'known_use_union_check': output['known_use_union_check'],
                  'all_inputs_unchanged': True, 'new_scientific_calls': 0}, indent=2))
