"""Offline verification of fictional journals; not physical-effect proof."""
import hashlib
import json
from pathlib import Path

root=Path(__file__).parent/'synthetic-evidence'/'run'
def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def audit(path):
    data=path.read_bytes()
    if not data or not data.endswith(b'\n'):raise ValueError('partial journal')
    prev='0'*64;rows=[]
    for i,line in enumerate(data.splitlines(),0):
        row=json.loads(line);h=row.pop('digest')
        if row['seq']!=i or row['previous']!=prev or hashlib.sha256(canonical(row)).hexdigest()!=h:
            raise ValueError('broken journal chain')
        prev=h;rows.append(row)
    return rows,{'rows':len(rows),'sha256':hashlib.sha256(data).hexdigest(),'last_digest':prev}
parent,parent_info=audit(root/'owner'/'parent-ledger.jsonl')
if parent[-1]['event']!='synthetic_batch_complete':raise ValueError('incomplete fictional transcript')
children={}
for pair in ('one','two','three','four'):
    for arm in ('A','B'):
        path=root/('arm-'+pair+'-'+arm)/'worker.jsonl';rows,info=audit(path)
        outcome=[r['payload']['result'] for r in rows if r['kind']=='synthetic_observed_episode_returned']
        if len(outcome)!=1 or outcome[0]['steps']!=2 or outcome[0]['won'] is not True:raise ValueError('missing fake outcome')
        children[pair+'-'+arm]=info
print(json.dumps({'scope':'hash checks on fabricated journals, not proof of physical effects','parent':parent_info,'children':children},sort_keys=True,indent=2))
