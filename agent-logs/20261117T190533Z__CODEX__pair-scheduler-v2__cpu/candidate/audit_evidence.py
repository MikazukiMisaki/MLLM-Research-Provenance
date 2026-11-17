"""Check only fictional file integrity; does not prove physical operations."""
import hashlib
import json
from pathlib import Path

def canon(value):return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def check(path):
    data=path.read_bytes()
    if not data or not data.endswith(b'\n'):raise ValueError('partial ledger')
    previous='0'*64;rows=[]
    for i,line in enumerate(data.splitlines()):
        row=json.loads(line);digest=row.pop('digest')
        if row['seq']!=i or row['previous']!=previous or hashlib.sha256(canon(row)).hexdigest()!=digest:raise ValueError('chain')
        previous=digest;rows.append(row)
    return {'path':str(path),'rows':len(rows),'sha256':hashlib.sha256(data).hexdigest()},rows
root=Path(__file__).parent/'synthetic-evidence'
result={}
for case,expected in [('complete',8),('stopped',3)]:
    run=root/case/'run';parent,rows=check(run/'owner'/'global.jsonl')
    workers=sorted(run.glob('*/output/worker_events.jsonl'))
    if len(workers)!=expected:raise ValueError('worker count')
    if case=='complete' and rows[-1]['event']!='synthetic_batch_complete':raise ValueError('complete missing')
    if case=='stopped' and not any(row['event']=='aborted' for row in rows):raise ValueError('abort missing')
    result[case]={'parent':parent,'workers':[check(path)[0] for path in workers]}
print(json.dumps({'scope':'fictional journal hash chains; not physical evidence','results':result},sort_keys=True,indent=2))
