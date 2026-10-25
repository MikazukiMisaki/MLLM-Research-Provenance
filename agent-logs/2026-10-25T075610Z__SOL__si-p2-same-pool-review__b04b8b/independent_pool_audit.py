"""Independent stdlib fixed-parent contract review, no project imports/execution.

Existing raw source/branch/replay only. Writes compact hashes/lineage in OWN;
never writes training rows or full prompts, never changes a historical record.
"""
import collections
import datetime
import hashlib
import json
import re
from pathlib import Path

OWN = Path(__file__).resolve().parent
assert OWN.name == '2026-10-25T075610Z__SOL__si-p2-same-pool-review__b04b8b'
VALIDATION = Path('/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/validation')
R19 = Path('/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z')
SOURCE = {'R4': VALIDATION / 'sft-recovery-source-pool-r1-20260908T042933Z/trajectories.jsonl',
          'R10_OSR': VALIDATION / 'persistent-recovery-source-pool-r7-20260909T000000Z/trajectories.jsonl',
          'R16_OSR': VALIDATION / 'progress-aware-recovery-r14-20260910T000000Z/raw_trajectories.jsonl',
          'R19_K1': R19 / 'source_trajectories.jsonl'}
CONTROL = {'R4': VALIDATION / 'sft-recovery-replay-continue-r3-20260908T055308Z/continue_branches.jsonl',
           'R10_OSR': VALIDATION / 'persistent-recovery-replay-continue-r9-20260909T033000Z/continue_branches.jsonl',
           'R16_OSR': VALIDATION / 'progress-aware-recovery-r15-b-20260910T000000Z/continue_ledger.jsonl'}
REPLAY = {'R4': VALIDATION / 'sft-recovery-replay-continue-r3-20260908T055308Z/replay_validation.jsonl',
          'R16_OSR': VALIDATION / 'progress-aware-recovery-r16-osr-20260910T000000Z/replay_ledger.jsonl'}
BINDINGS = {}


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def bind(path):
    path = Path(path)
    if str(path) not in BINDINGS:
        BINDINGS[str(path)] = {'path': str(path), 'bytes': path.stat().st_size,
                              'sha256_before': sha(path)}
    return path


def rows(path):
    with bind(path).open('rb') as stream:
        for n, raw in enumerate(stream, 1):
            if raw.strip():
                yield n, hashlib.sha256(raw).hexdigest(), json.loads(raw)


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=True, sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()


def canonical(value):
    parts = str(value).rstrip('/').split('/')
    for index in range(len(parts) - 1, 0, -1):
        if parts[index].startswith('trial_'):
            return parts[index - 1] + '/' + parts[index]
    return str(value)


def anchor(case):
    text = '\n'.join(('SI-P2-anchor-v1', case['canonical_task'], case['stage'], case['prefix_id'], ''))
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def prompt(goal, observation, recent, mapping):
    history = '\n\n'.join('Action: ' + item['action'] + '\nResult: ' + item['resulting_observation'] for item in recent) or '(none)'
    commands = '\n'.join('[' + key + '] ' + value for key, value in mapping.items())
    return ('You are an ALFWorld household agent. Select exactly one next action.\n'
            'Return exactly one bare action ID in the form Axyz. Do not output a label, command, explanation, reasoning, or <think> tags.\n\n'
            'Task goal:\n' + goal + '\n\nCurrent observation:\n' + observation +
            '\n\nRecent action/result transitions (last 4):\n' + history +
            '\n\nIndexed admissible actions:\n' + commands + '\n\nYour response:')


def success(step):
    return int(bool(step and step.get('done') and step.get('reward', 0) > 0))


manifest_path = bind(OWN / 'PARENT_COHORT_MANIFEST.json')
assert sha(manifest_path) == 'a3e2548e89280d150cbe83cceca632f9f91275ede0a4a9d89133e53691826078'
manifest = json.loads(manifest_path.read_text())
parent = {}
for source in manifest['sources']:
    assert sha(bind(source['source_path'])) == source['full_file_sha256']
    parent[source['stage']] = {n: (h, value) for n, h, value in rows(source['source_path'])}
sources = {}
for stage, path in SOURCE.items():
    wanted = {case['canonical_task'] for case in manifest['rows'] if case['stage'] == stage}
    by_task = collections.defaultdict(list)
    for n, h, value in rows(path):
        task = canonical(value['task']['task_id'])
        if task in wanted:
            by_task[task].append((n, h, value))
    sources[stage] = by_task
controls = {stage: {r['prefix_id']: (n, h, r) for n, h, r in rows(path)} for stage, path in CONTROL.items()}
replays = {stage: {r['prefix_id']: (n, h, r) for n, h, r in rows(path)} for stage, path in REPLAY.items()}

# Stream only referenced K1 generations/transitions and initial replay evidence.
wanted_events = set()
for h, branch in parent['R19_K1'].values():
    arm = branch['k_results']['1']
    wanted_events.add(branch['evidence_refs']['prefix_attempt_event_id'])
    for key in ('recovery_generation_event_ids', 'recovery_transition_event_ids', 'suffix_transition_event_ids'):
        wanted_events.update(arm['evidence_refs'][key])
events = {}
for n, h, event in rows(R19 / 'execution_events.jsonl'):
    if event['event_id'] in wanted_events:
        events[event['event_id']] = (n, h, event)
replay_ids = set()
for h, branch in parent['R19_K1'].values():
    evidence = events[branch['evidence_refs']['prefix_attempt_event_id']][2]['payload'].get('replay_evidence', {})
    replay_ids.update(evidence.get('replay_transition_event_ids', []))
for n, h, event in rows(R19 / 'execution_events.jsonl'):
    if event['event_id'] in replay_ids:
        events[event['event_id']] = (n, h, event)

results = []
for case in manifest['rows']:
    stage, pid, d = case['stage'], case['prefix_id'], case['decision_index']
    row_hash, branch = parent[stage][case['source_line']]
    assert row_hash == case['source_row_sha256'] and branch['prefix_id'] == pid
    matches = sources[stage][case['canonical_task']]
    assert len(matches) == 1, (case['case_id'], 'source ambiguous/missing', len(matches))
    sn, sh, source = matches[0]
    steps = source['steps']
    state = steps[d]
    mapping = {f'A{index:03d}': action for index, action in enumerate(state['valid_actions'])}
    history = [{'action': steps[i]['action'], 'resulting_observation': steps[i + 1]['observation']} for i in range(max(0, d - 4), d)]
    projection = {'goal': source['task']['text'], 'observation': state['observation'],
                  'recent_action_result_transitions': history, 'ordered_action_map': list(mapping.items())}
    policy = state.get('metadata', {}).get('policy') or state.get('policy_metadata') or {}
    checks = {'public_prompt_matches_original_source': policy.get('prompt') == prompt(source['task']['text'], state['observation'], history, mapping),
              'pre_action_nonterminal': not any(step['done'] for step in steps[:d]),
              'remaining_horizon': case['remaining_horizon'] == 50 - d,
              'source_identity': canonical(source['task']['task_id']) == case['canonical_task']}
    event_id, terminal, raw, parsed, transition = None, None, {}, {}, None
    if stage == 'R4':
        teacher = branch['raw_generations']['recovery']['stage_two']
        raw, parsed = teacher['generation'], teacher['parsed']
        s1 = branch['recover']['stage_one']
        executed = branch['recover']['recovery_action']
        transition = branch['recover']['recovery_transition']
        suffix = branch['recover']['continuation']['steps']
        terminal = suffix[-1] if suffix else transition
        ctl = controls[stage][pid][2]['continue']
        cont, rec = int(branch['continue']['success']), int(branch['recover']['success'])
        trace = replays[stage][pid][2]
        checks['exact_replay'] = trace['replay_match'] and branch['prefix_replay']['replay_match']
        checks['replay_public_state'] = trace['branch_observation'] == state['observation'] and trace['branch_valid_actions'] == state['valid_actions'] and trace['replay_recent_context'] == history
        checks['replay_actions_and_results'] = len(trace['transitions']) == d and all(t['action'] == steps[i]['action'] and t['replayed_observation'] == steps[i]['observation'] and t['resulting_observation'] == steps[i + 1]['observation'] and t['exact'] for i, t in enumerate(trace['transitions']))
        checks['executed'] = branch['recover']['recovery_action_executed']
    elif stage in ('R10_OSR', 'R16_OSR'):
        teacher = branch['recovery_full']['stage_two']
        raw, parsed = teacher['generation'], teacher['parsed']
        s1 = branch['recovery_full']['stage_one']['parsed']
        executed = branch['recovery_mapped_command']
        transition = branch['recovery_transition']
        suffix = branch['continuation_full']['steps']
        terminal = suffix[-1] if suffix else transition
        control = controls[stage][pid][2]
        ctl = control['continue_full'] if stage == 'R10_OSR' else control
        cont, rec = int(branch['r_continue']), int(branch['r_osr'])
        checks['executed'] = branch['recovery_action_executed']
        if stage == 'R10_OSR':
            trace = branch['replay_full']
            checks['exact_replay'] = trace['replay_match']
            checks['replay_public_state'] = trace['branch_observation'] == state['observation'] and trace['branch_valid_actions'] == state['valid_actions'] and trace['replay_recent_context'] == history
            checks['replay_actions_and_results'] = len(trace['transitions']) == d and all(t['action'] == steps[i]['action'] and t['observation_before'] == steps[i]['observation'] and t['resulting_observation'] == steps[i + 1]['observation'] and t['exact'] for i, t in enumerate(trace['transitions']))
        else:
            trace = replays[stage][pid][2]
            checks['exact_replay'] = trace['replay_match']
            checks['replay_public_state'] = (trace['current_observation_sha256'] == hashlib.sha256(state['observation'].encode()).hexdigest() and trace['current_indexed_action_map_sha256'] == digest(mapping) and trace['recent_k4_context_sha256'] == digest(history))
            checks['replay_actions_and_results'] = len(trace['transition_checks']) == d and all(all(t[k] for k in ('action_admissible', 'action_map_equal', 'done_equal', 'observation_equal', 'result_observation_equal', 'reward_equal', 'truncated_equal')) for t in trace['transition_checks'])
    else:
        arm = branch['k_results']['1']
        cont, rec = int(branch['continue_success']), int(arm['success'])
        gens = [events[eid][2] for eid in arm['evidence_refs']['recovery_generation_event_ids']]
        second = [event for event in gens if event['identity']['component'] == 'stage2']
        first = [event for event in gens if event['identity']['component'] == 'stage1']
        assert len(second) <= 1 and len(first) <= 1
        s1 = first[0]['payload']['evidence'] if first else {'status': 'invalid_or_unreferenced'}
        if second:
            event_id = second[0]['event_id']
            parsed = second[0]['payload']['evidence']
            raw = parsed['generation']
        transitions = arm['evidence_refs']['recovery_transition_event_ids']
        action = events[transitions[0]][2]['payload']['action'] if transitions else None
        executed = action['command'] if action else None
        transition = action['transition'] if action else None
        checks['executed'] = action is not None
        checks['recovery_before_state'] = bool(action and action['observation_before'] == state['observation'] and action['valid_actions_before'] == state['valid_actions'] and action['history_before'] == [[step['observation'], step['action']] for step in steps[:d]] and action['action_map'] == mapping)
        suffix = arm['evidence_refs']['suffix_transition_event_ids']
        terminal = events[suffix[-1]][2]['payload']['transition'] if suffix else transition
        ctl = {'steps': steps}
        initial = events[branch['evidence_refs']['prefix_attempt_event_id']][2]['payload'].get('replay_evidence', {})
        replay = [events[eid][2]['payload'] for eid in initial.get('replay_transition_event_ids', [])]
        checks['exact_replay'] = initial.get('replay_match') is True
        checks['replay_actions_and_results'] = len(replay) == d and all(t['command'] == steps[i]['action'] and t['before_state']['observation'] == steps[i]['observation'] and t['before_state']['valid_actions'] == steps[i]['valid_actions'] and t['transition']['observation'] == steps[i + 1]['observation'] for i, t in enumerate(replay))
    aid = parsed.get('action_id')
    command = parsed.get('command', parsed.get('action'))
    checks.update({'stage1_valid': s1.get('status') == 'valid',
                   'selected': parsed.get('status') == 'selected',
                   'bare_ID': bool(aid and re.fullmatch(r'A\d{3}', raw.get('raw_output', '').strip()) and raw.get('raw_output', '').strip() == aid),
                   'full_map': parsed.get('id_to_command') == mapping,
                   'ID_to_command': bool(aid and mapping.get(aid) == command == executed),
                   'generation_complete': raw.get('output_complete') is True and raw.get('token_cap_reached') is False,
                   'CONTINUE_frozen_predicate': success(ctl.get('steps', [])[-1] if ctl.get('steps') else None) == cont,
                   'recovery_frozen_predicate': success(terminal) == rec})
    failed = [key for key, value in checks.items() if not value]
    results.append({'case_id': case['case_id'], 'stage': stage, 'prefix_id': pid,
                    'canonical_task': case['canonical_task'], 'family': case['family'], 'decision_index': d,
                    'source_episode_line': sn, 'source_episode_row_sha256': sh,
                    'continue_success': cont, 'recovery_success': rec,
                    'checks': checks, 'failed_checks': failed, 'Q_hist_independent_pass': not failed,
                    'quality_scope': 'Independent raw/source/map/target/replay/labels; model role binding separately checked from frozen stage manifests.',
                    'public_projection_sha256': digest(projection), 'target_command': command,
                    'target_action_id': aid, 'raw_output_sha256': hashlib.sha256(raw.get('raw_output', '').encode()).hexdigest(),
                    'physical_generation_event_id': event_id, 'legacy_physical_identity': 'NOT_PROVEN' if stage != 'R19_K1' else 'EVENT_BOUND',
                    'anchor_key': anchor(case)})


def counts(candidates):
    b = [r for r in candidates if r['recovery_success'] == 1]
    c = [r for r in b if r['continue_success'] == 0]
    return {'rows': len(candidates), 'tasks': len({r['canonical_task'] for r in candidates}),
            'B': len(b), 'C': len(c), 'B_minus_C': len(b) - len(c),
            'B_ids': [r['case_id'] for r in b], 'C_ids': [r['case_id'] for r in c],
            'C_families': dict(collections.Counter(r['family'] for r in c)),
            'B_families': dict(collections.Counter(r['family'] for r in b)),
            'C_sources': dict(collections.Counter(r['stage'] for r in c))}


def flow(candidates):
    stages = {'quality': counts(candidates)}
    seen = set()
    physical = []
    for item in sorted(candidates, key=lambda r: (r['anchor_key'], r['case_id'])):
        pid = item['physical_generation_event_id']
        if pid is not None and pid in seen:
            continue
        if pid is not None:
            seen.add(pid)
        physical.append(item)
    stages['physical_dedup'] = counts(physical)
    seen = set()
    anchors = []
    for item in physical:
        if item['canonical_task'] not in seen:
            anchors.append(item)
            seen.add(item['canonical_task'])
    stages['task_anchor'] = counts(anchors)
    seen = set()
    exact = []
    for item in anchors:
        key = (item['public_projection_sha256'], item['target_command'])
        if key not in seen:
            exact.append(item)
            seen.add(key)
    stages['exact_input_target_dedup'] = counts(exact)
    return stages, exact


main_flow, final = flow([r for r in results if r['Q_hist_independent_pass']])
pin_flow, pin_final = flow([r for r in results if r['Q_hist_independent_pass'] and r['stage'] == 'R19_K1'])
for value in BINDINGS.values():
    value['sha256_after'] = sha(value['path'])
    value['unchanged'] = value['sha256_before'] == value['sha256_after']
assert all(value['unchanged'] for value in BINDINGS.values())
output = {'schema': 'SI_P2_COORDINATOR_INDEPENDENT_POOL_V1',
          'observed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'cases': results, 'raw_counts': counts(results), 'Q_hist_flow': main_flow,
          'Q_pin_R19_candidate_sensitivity_flow': pin_flow,
          'Q_pin_limitation': 'Stage identity stratum is only a candidate proxy; actual pinned runtime receipts separately reviewed.',
          'input_bindings': list(BINDINGS.values()),
          'scientific_calls_added': 0, 'training_N_approved': False,
          'not_a_training_dataset': True}
(OWN / 'independent_pool_audit.json').write_text(json.dumps(output, indent=2) + '\n')
print(json.dumps({'raw': output['raw_counts'], 'quality_failures': [{'case_id': r['case_id'], 'failed': r['failed_checks']} for r in results if r['failed_checks']], 'Q_hist_flow': main_flow, 'Q_pin_candidate_flow': pin_flow}, indent=2))
