#!/usr/bin/env python3
"""Recompute fixed fictional-control tables from a saved, possibly partial journal."""
import collections
import hashlib
import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
CONDITIONS=('compatible','conflicting','neutral')

def main(journal):
    cases=json.loads((HERE/'cases.json').read_text())
    expected={c['case_id']+'-'+q:(c,q) for c in cases for q in CONDITIONS}
    events=[json.loads(line) for line in Path(journal).read_text().splitlines()]
    by_event={name:{} for name in ('prepared','call_start','raw_result','decision')}
    for r in events:
        event=r.get('event')
        if event not in by_event: continue
        k=r.get('call_id')
        if k not in expected or k in by_event[event]: raise ValueError('unexpected or repeated call event')
        by_event[event][k]=r
    pre,started,raw,dec=(by_event[x] for x in ('prepared','call_start','raw_result','decision'))
    for k,p in pre.items():
        c,q=expected[k]
        sha=hashlib.sha256(json.dumps(p['input_token_ids'],separators=(',',':')).encode()).hexdigest()
        if p['input_token_sha256']!=sha or p['prompt']!=c['prompts'][q] or p['mapping']!=c['mapping']: raise ValueError('prepared input mismatch')
    for k,d in dec.items():
        if k not in pre or k not in started or k not in raw: raise ValueError('decision lacks corresponding events')
        c,q=expected[k]
        if d['case_id']!=c['case_id'] or d['family']!=c['family'] or d['condition']!=q: raise ValueError('decision key mismatch')
        action=d['action']
        if action is not None and c['mapping'].get(d['decoded'])!=action: raise ValueError('action mapping mismatch')
        category='acceptable' if action in c['acceptable_actions'] else 'local_conflict' if action==c['conflicting_action'] else 'other' if action is not None else d['category']
        if category!=d['category'] or category not in ('acceptable','local_conflict','other','format_invalid','truncated'): raise ValueError('category mismatch')
    out={};overall={}
    for q in CONDITIONS:
        counts=collections.Counter()
        for c in cases:
            k=c['case_id']+'-'+q
            counts[dec[k]['category'] if k in dec else 'unknown' if k in started else 'not_run']+=1
        overall[q]={'planned':len(cases),'counts':dict(counts)}
    for c in cases:
        cells={}
        for q in CONDITIONS:
            k=c['case_id']+'-'+q;d=dec.get(k)
            cells[q]={'status':d['category'] if d else 'unknown' if k in started else 'not_run',
                      'action':None if d is None else d['action'],
                      'id':None if d is None else d['decoded']}
        def changed(a,b):
            return None if cells[a]['action'] is None or cells[b]['action'] is None else cells[a]['action']!=cells[b]['action']
        out[c['case_id']]={'family':c['family'],'conditions':cells,'compatible_vs_conflicting_changed':changed('compatible','conflicting'),
                           'neutral_vs_compatible_changed':changed('neutral','compatible')}
    return {'scope':'8 fictional cases in six authored structures; exploration only; no environment or held-out inference',
            'planned_calls':len(expected),'recorded_decisions':len(dec),'started_calls':len(started),
            'journal_completed':bool(events and events[-1].get('event')=='complete'),
            'condition_totals':overall,'by_case':out}

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: analyze.py JOURNAL')
    print(json.dumps(main(sys.argv[1]),ensure_ascii=False,indent=2,sort_keys=True))
