#!/usr/bin/env python3
"""Recompute recorded fictional handoff results from this snapshot, on CPU only."""
import collections
import hashlib
import json
import math
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGS = ROOT / 'evidence/sanitized_synthetic_logs'
FILES = {
    'base': ('second-object-visible-acquisition-v1.jsonl', '3149cf08c7226a9a7984a6955ddb7fbeece2d4fb8de53b02f60b04cd91197327'),
    'subgoal': ('incorrect-subgoal-handoff-v1.jsonl', '41fbf15e1e0fc5f00d76fd352279989b70cf77e00950ed740f07e1d4ee073b52'),
    'diagnosis': ('incorrect-diagnosis-handoff-v1.jsonl', 'b5229948da614c74e81a8601ea4a1c3658c4b8d926bc263b5ff95eeade86a350'),
    'scores': ('diagnosis-subgoal-candidate-scores-v1.jsonl', '13252ea885b312b36853389856ca2859ada0765104c5e1c69f380437e6e9cc60'),
}
IDS = {'A000', 'A001', 'A002', 'A003'}
CONDITIONS = ('old_correct', 'old_wrong', 'false_correct', 'false_wrong')
CONTRASTS = (('goal_given_original_diagnosis','old_correct','old_wrong'),
             ('goal_given_injected_diagnosis','false_correct','false_wrong'),
             ('diagnosis_given_original_goal','old_correct','false_correct'),
             ('diagnosis_given_injected_goal','old_wrong','false_wrong'))

def require(ok, message):
    if not ok:
        raise ValueError(message)

def load(name):
    filename, digest = FILES[name]
    data = (LOGS / filename).read_bytes()
    require(hashlib.sha256(data).hexdigest() == digest, 'digest mismatch: ' + filename)
    rows = [json.loads(line) for line in data.splitlines()]
    require(rows[-1]['event'] == 'complete', 'incomplete: ' + filename)
    return rows

def indexed(rows, event):
    result = {}
    for row in rows:
        if row['event'] == event:
            key = row['key']
            require(key not in result, 'duplicate ' + event + ': ' + key)
            result[key] = row
    return result

def one(rows, event):
    found = [r for r in rows if r['event'] == event]
    require(len(found) == 1, 'expected one ' + event)
    return found[0]

def field(prompt, label, following):
    prefix = label + ':\n'
    require(prompt.count(prefix) == 1, 'missing or ambiguous prompt field')
    return prompt.split(prefix, 1)[1].split('\n\n' + following + ':\n', 1)[0]

def main():
    logs = {name: load(name) for name in FILES}
    pre = {n: indexed(logs[n], 'prepared') for n in ('base','subgoal','diagnosis','scores')}
    gen = indexed(logs['base'], 'generation')
    decisions = {n: indexed(logs[n], 'decision') for n in ('subgoal','diagnosis')}
    raw = {n: indexed(logs[n], 'raw_result') for n in ('base','subgoal','diagnosis')}
    suffixes = one(logs['scores'], 'loading_complete')['suffixes']
    require(set(suffixes) == IDS, 'bad suffixes')
    scores = collections.defaultdict(dict)
    for r in logs['scores']:
        if r['event'] != 'score': continue
        key, candidate, value = r['key'], r['candidate'], r['log_probability']
        require(candidate in IDS and candidate not in scores[key] and math.isfinite(value), 'invalid score')
        require(r['suffix_token_ids'] == suffixes[candidate], 'candidate suffix mismatch')
        require(r['forward_input_tokens'] == pre['scores'][key]['input_token_count'] + len(suffixes[candidate]), 'forward length mismatch')
        scores[key][candidate] = value
    expected = {f'{i:02d}-{c}' for i in range(1, 9) for c in CONDITIONS}
    require(set(scores) == set(pre['scores']) == expected, 'incomplete scoring grid')
    require(one(logs['scores'], 'complete')['forward_count'] == 128, 'forward count')
    values, margins, groups, table = {}, {}, {}, {}
    for condition in CONDITIONS:
        probs, diffs = [], []
        table[condition] = collections.Counter()
        for i in range(1,9):
            case = f'{i:02d}'
            source, skey = {'old_correct': ('base',case+'-generated'), 'old_wrong': ('subgoal',case),
                            'false_correct': ('diagnosis',case+'-original_goal'),
                            'false_wrong': ('diagnosis',case+'-injected_goal')}[condition]
            key = case+'-'+condition
            p, original, entries = pre['scores'][key], pre[source][skey], scores[key]
            require(set(entries) == IDS and set(p['mapping']) == IDS and len(set(p['mapping'].values())) == 4, 'invalid mapping')
            require(p['mapping'] == original['mapping'] and p['correct_action'] == original['correct_action'], 'source mapping mismatch')
            require(p['input_token_count'] == original['input_token_count'], 'prompt length mismatch')
            choice = gen[skey] if source == 'base' else decisions[source][skey]
            decoded, tokens = choice['decoded'], choice['token_ids']
            require(decoded in IDS and tokens == suffixes[decoded], 'greedy suffix mismatch')
            require(raw[source][skey]['output_ids'][original['input_token_count']:] == tokens, 'raw output suffix mismatch')
            if source != 'base': require(choice['selected_action'] == p['mapping'][decoded], 'action mismatch')
            winners = [k for k in IDS if entries[k] == max(entries.values())]
            require(winners == [decoded], 'argmax mismatch')
            inverse = {v:k for k,v in p['mapping'].items()}
            undo, take = inverse[p['undo_action']], inverse[p['correct_action']]
            exps = {k: math.exp(v - max(entries.values())) for k,v in entries.items()}
            prob = exps[undo] / sum(exps.values())
            margin = entries[undo]-entries[take]
            values[key], margins[key] = prob, margin
            probs.append(prob); diffs.append(margin)
            table[condition]['take_second' if decoded == take else 'undo_first' if decoded == undo else 'other'] += 1
        groups[condition] = {'planned': 8, 'valid': 8, 'undo_weight_median': statistics.median(probs),
            'undo_weight_range': [min(probs),max(probs)], 'undo_weight_above_0_9': sum(x > .9 for x in probs),
            'undo_minus_take_log_score_median': statistics.median(diffs), 'undo_minus_take_log_score_range': [min(diffs),max(diffs)],
            'canonical_argmax_matches_recorded_greedy': 8, 'canonical_suffix_matches_recorded': 8}
    for i in range(1,9):
        case=f'{i:02d}'
        ps=[pre['base'][case+'-generated']['prompt'],pre['subgoal'][case]['prompt'],
            pre['diagnosis'][case+'-original_goal']['prompt'],pre['diagnosis'][case+'-injected_goal']['prompt']]
        diag='Frozen Stage-1 diagnosis'; goal='Frozen Stage-1 immediate subgoal'; mapping='Indexed admissible-action mapping'
        d=[field(p,diag,goal) for p in ps]; g=[field(p,goal,mapping) for p in ps]
        require(d[0] == d[1] and d[2] == d[3] and g[0] == g[2] and g[1] == g[3], 'condition field mismatch')
        normalized=[p.replace(diag+':\n'+x,diag+':\n<diagnosis>').replace(goal+':\n'+y,goal+':\n<subgoal>') for p,x,y in zip(ps,d,g)]
        require(len(set(normalized)) == 1, 'uncontrolled prompt difference')
    pairs, interaction = {}, []
    for name,a,b in CONTRASTS:
        delta=[values[f'{i:02d}-{b}']-values[f'{i:02d}-{a}'] for i in range(1,9)]
        pairs[name]={'valid':8,'increase':sum(x>0 for x in delta),'equal':sum(x==0 for x in delta),'decrease':sum(x<0 for x in delta)}
    for i in range(1,9):
        c=f'{i:02d}'
        row={'key':c}
        for name,a,b in CONTRASTS: row[name]=margins[c+'-'+b]-margins[c+'-'+a]
        row['interaction']=row['goal_given_injected_diagnosis']-row['goal_given_original_diagnosis']
        interaction.append(row)
    summary=json.loads((ROOT/'reports/parallel_research_round5/DIAGNOSIS_SUBGOAL_CANDIDATE_SCORES_SUMMARY_V1.json').read_text())
    existing=json.loads((ROOT/'reports/parallel_research_round5/HANDOFF_GOAL_DIAGNOSIS_INTERACTION_V1.json').read_text())
    require(groups == summary['conditions'] and pairs == summary['paired_undo_weight_changes'], 'score summary mismatch')
    require(interaction == existing['per_case'], 'interaction mismatch')
    summaries = {}
    for name in [x[0] for x in CONTRASTS] + ['interaction']:
        xs = [row[name] for row in interaction]
        summaries[name] = {'n':len(xs),'minimum':min(xs),'maximum':max(xs),'median':statistics.median(xs),
                           'negative':sum(x<0 for x in xs),'positive':sum(x>0 for x in xs),'zero':sum(x==0 for x in xs)}
    require(summaries == existing['summaries'], 'interaction summary mismatch')
    token_counts = {}
    for n in ('base','subgoal','diagnosis'):
        outputs = gen if n == 'base' else decisions[n]
        token_counts[n] = {'input':sum(pre[n][k]['input_token_count'] for k in outputs),
                           'generated':sum(len(v['token_ids']) for v in outputs.values())}
        require(len(outputs) == one(logs[n], 'complete')['call_count'], 'generation count mismatch')
    total=sum(r['forward_input_tokens'] for r in logs['scores'] if r['event']=='score')
    require(total == summary['forward_input_tokens'], 'total tokens mismatch')
    changes={f'{i:02d}': values[f'{i:02d}-false_wrong']-values[f'{i:02d}-old_wrong'] for i in range(1,9)}
    return {'scope':'Saved fictional-prompt outputs and scores only; no model/environment execution or authentication.',
            'inputs_sha256':{v[0]:v[1] for v in FILES.values()}, 'decision_counts':{k:dict(v) for k,v in table.items()},
            'conditions':groups, 'paired_undo_weight_changes':pairs, 'interaction_per_case':interaction, 'interaction_summaries':summaries, 'generation_tokens':token_counts,
            'forward_count':128,'forward_input_tokens':total,'greedy_argmax_and_suffix_matches':32,
            'generation_call_counts':{n:one(logs[n],'complete')['call_count'] for n in ('base','subgoal','diagnosis')},
            'diagnosis_given_injected_goal_weight_decreases':{k:v for k,v in changes.items() if v < 0},
            'matched_uploaded_summaries':True}

if __name__ == '__main__':
    print(json.dumps(main(), ensure_ascii=False, indent=2, sort_keys=True))
