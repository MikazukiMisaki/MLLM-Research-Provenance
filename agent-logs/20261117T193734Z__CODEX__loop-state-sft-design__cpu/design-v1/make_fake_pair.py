#!/usr/bin/env python3
"""Deterministic FICTIONAL filtering example; never scientific training data."""
import hashlib
import json

def row(index,prompt,history):
    return {'index':index,'prompt':prompt,'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),
            'history':history,'action_map':{'A000':'look','A001':'go to example'},
            'target_id':'A001','target_command':'go to example'}
def loop(history):
    return len(history)>=4 and history[-4:]==['look','examine example','look','examine example']
def valid(row):
    return (row['prompt_sha256']==hashlib.sha256(row['prompt'].encode()).hexdigest() and
            row['action_map'].get(row['target_id'])==row['target_command'] and
            not row['target_command'].startswith(('look','examine')))
def select_pair(episodes):
    out=[];seen=set()
    for ep in sorted(episodes,key=lambda e:(e['parent'],e['episode'])):
        if not ep['completed'] or not ep['won'] or ep['parent'] in seen:continue
        seen.add(ep['parent']) # max one parent, even if no match; never fish alternatives
        ordered=sorted(ep['rows'],key=lambda r:r['index'])
        targets=[r for r in ordered if valid(r) and loop(r['history'])]
        controls=[r for r in ordered if valid(r) and not loop(r['history'])]
        matches=[(t,c) for t in targets for c in controls if t['index']!=c['index'] and
                 (t['target_id'],t['target_command'])==(c['target_id'],c['target_command'])]
        if matches:
            t,c=matches[0];out.append({'parent':ep['parent'],'episode':ep['episode'],'target':t,'control':c})
    return out

episodes=[{'parent':'FAKE_PARENT_1','episode':'FAKE_SUCCESS','completed':True,'won':True,
           'rows':[row(0,'FICTIONAL control',['look']),
                   row(8,'FICTIONAL target',['look','examine example','look','examine example'])]},
          {'parent':'FAKE_PARENT_2','episode':'FAKE_FAILURE','completed':True,'won':False,
           'rows':[row(0,'FICTIONAL failure',['look'])]}]
selected=select_pair(episodes)
assert len(selected)==1 and selected[0]['episode']=='FAKE_SUCCESS'
assert loop(selected[0]['target']['history']) and not loop(selected[0]['control']['history'])
print(json.dumps({'status':'FICTIONAL_NOT_TRAINING_DATA','n_pairs':len(selected),'pairs':selected},
                 sort_keys=True,indent=2))
