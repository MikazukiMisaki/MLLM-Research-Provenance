#!/usr/bin/env python3
"""Summarize complete or partial fictional pilot journals without inference."""
import collections
import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent

def main(journal):
    cases=json.loads((HERE/'cases.json').read_text())
    expected={c['case_id']+'-'+k:(c,k) for c in cases for k in ('compatible','conflicting')}
    decisions={}
    events=[json.loads(line) for line in Path(journal).read_text().splitlines()]
    for r in events:
        if r['event']=='decision':
            key=r['call_id']
            if key not in expected or key in decisions: raise ValueError('unexpected or duplicate decision')
            c,condition=expected[key]
            if r['family']!=c['family'] or r['condition']!=condition: raise ValueError('condition mismatch')
            decisions[key]=r
    output={}
    for family in ('ordinary','necessary_retrieval'):
        group=[c for c in cases if c['family']==family]
        conditions={}
        for condition in ('compatible','conflicting'):
            counts=collections.Counter()
            for c in group:
                r=decisions.get(c['case_id']+'-'+condition)
                counts['not_recorded' if r is None else r['category']]+=1
            conditions[condition]={'planned':len(group),'counts':dict(counts)}
        paired=[]
        for c in group:
            a=decisions.get(c['case_id']+'-compatible');b=decisions.get(c['case_id']+'-conflicting')
            paired.append({'case_id':c['case_id'],'compatible':None if a is None else a['category'],
                'conflicting':None if b is None else b['category'],
                'action_changed':None if a is None or b is None or a['action'] is None or b['action'] is None else a['action']!=b['action'],
                'first_retrieved_compatible':None if a is None or a['action'] is None else a['action']==c['first_action']})
        output[family]={'conditions':conditions,'pairs':paired}
    return {'scope':'fictional lexical variants of two templates; not an environment evaluation or held-out evidence',
            'planned_calls':16,'recorded_decisions':len(decisions),'journal_completed':bool(events and events[-1]['event']=='complete'),
            'conditions_by_family':output}

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: analyze.py JOURNAL')
    print(json.dumps(main(sys.argv[1]),ensure_ascii=False,indent=2,sort_keys=True))
