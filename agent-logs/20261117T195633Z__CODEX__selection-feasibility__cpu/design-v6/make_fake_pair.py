#!/usr/bin/env python3
"""Deterministic FICTIONAL filtering example; never scientific training data."""
import hashlib
import json

def row(index,prompt,history,target_ids=None):
    return {'index':index,'prompt':prompt,'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),
            'history':history,'action_map':{'A000':'look','A001':'go to example'},
            'target_id':'A001','target_command':'go to example',
            'prompt_token_ids':[11,12], 'supervised_token_ids':target_ids if target_ids is not None else [21,22],
            'loss_mask':[0,0,1,1]}
def loop(history):
    return len(history)>=4 and history[-4:]==['look','examine example','look','examine example']
def valid(row):
    return (row['prompt_sha256']==hashlib.sha256(row['prompt'].encode()).hexdigest() and
            row['action_map'].get(row['target_id'])==row['target_command'] and
            not row['target_command'].startswith(('look','examine')) and
            type(row['prompt_token_ids']) is list and type(row['supervised_token_ids']) is list and
            bool(row['prompt_token_ids']) and 1<=len(row['supervised_token_ids'])<=16 and
            all(type(i) is int and i>=0 for i in row['prompt_token_ids']+row['supervised_token_ids']) and
            type(row['loss_mask']) is list and all(type(i) is int for i in row['loss_mask']) and
            row['loss_mask']==[0]*len(row['prompt_token_ids'])+[1]*len(row['supervised_token_ids']) and
            len(row['prompt_token_ids'])+len(row['supervised_token_ids'])<=4096)
def select_pair(episodes):
    out=[];seen=set()
    for ep in sorted(episodes,key=lambda e:(e['parent'],e['episode'])):
        if ep['parent'] in seen:continue
        seen.add(ep['parent']) # first episode of preselected parent only, even when failed
        if not ep['completed'] or not ep['won']:continue
        ordered=sorted(ep['rows'],key=lambda r:r['index'])
        targets=[r for r in ordered if valid(r) and loop(r['history'])]
        controls=[r for r in ordered if valid(r) and not loop(r['history'])]
        matches=[(t,c) for t in targets for c in controls if t['index']!=c['index'] and
                 (t['target_id'],t['target_command'],t['supervised_token_ids'],t['loss_mask'])==
                 (c['target_id'],c['target_command'],c['supervised_token_ids'],c['loss_mask'])]
        if matches:
            t,c=matches[0];out.append({'parent':ep['parent'],'episode':ep['episode'],'target':t,'control':c})
    return out

episodes=[{'parent':'FAKE_PARENT_1','episode':'FAKE_SUCCESS','completed':True,'won':True,
           'rows':[row(0,'FICTIONAL control',['look']),
                   row(8,'FICTIONAL target',['look','examine example','look','examine example'])]},
          {'parent':'FAKE_PARENT_2','episode':'FAKE_FAILURE','completed':True,'won':False,
           'rows':[row(0,'FICTIONAL failure',['look'])]},
          {'parent':'FAKE_PARENT_3','episode':'FAKE_UNMATCHED_LABEL','completed':True,'won':True,
           'rows':[row(0,'FICTIONAL control different target IDs',['look'],[99,22]),
                   row(8,'FICTIONAL target',['look','examine example','look','examine example'])]},
          {'parent':'FAKE_PARENT_4','episode':'FAKE_UNMATCHED_MASK','completed':True,'won':True,
           'rows':[dict(row(0,'FICTIONAL different mask',['look']),prompt_token_ids=[11,12,13],loss_mask=[0,0,0,1,1]),
                   row(8,'FICTIONAL target',['look','examine example','look','examine example'])]}]
selected=select_pair(episodes)
assert len(selected)==1 and selected[0]['episode']=='FAKE_SUCCESS'
assert loop(selected[0]['target']['history']) and not loop(selected[0]['control']['history'])
assert selected[0]['target']['supervised_token_ids']==selected[0]['control']['supervised_token_ids']
oversize=row(0,'FICTIONAL over limit',['look']);oversize['prompt_token_ids']=[1]*4095;oversize['loss_mask']=[0]*4095+[1,1]
assert not valid(oversize)
print(json.dumps({'status':'FICTIONAL_NOT_TRAINING_DATA','n_pairs':len(selected),'pairs':selected},
                 sort_keys=True,indent=2))
