"""Independent synthetic replay of v2 reset-shape controls and fail-stop."""
import json
from pathlib import Path
import sys,tempfile

root=Path('/home/lizening/research-notes/agent-logs/20261118__CODEX__synthetic-pair-reset-v2__private')
sys.path.insert(0,str(root))
import bridge,pair_synthetic
from test_pair import fixture

for mode in ('normal','tuple','bad_integer','bad_true','bad_extra','bad_missing'):
    with tempfile.TemporaryDirectory(prefix='review-fake-reset-v2-') as tmp:
        temp=Path(tmp).resolve();inputs,setup,verify=fixture(temp);output=temp/'run'
        try:
            owner=pair_synthetic.run_pair(output,inputs,setup,verify,mode=mode)
            status='completed'
        except bridge.Stop as error:
            status='stopped:'+str(error)
        rows=[json.loads(line) for line in (output/'owner'/'parent-ledger.jsonl').read_text().splitlines()]
        reserv=[r['payload'] for r in rows if r['event']=='reserved']
        returned=[r['payload'] for r in rows if r['event']=='returned']
        counts={f'{op}_reserved':sum(r.get('operation')==op for r in reserv) for op in ('materialize','reset','model_load')}
        counts['reset_returned']=sum(r.get('operation')=='reset' for r in returned)
        counts['last_event']=rows[-1]['event']
        if mode in ('normal','tuple'):
            assert status=='completed' and owner.finished==['A','B']
            assert counts['model_load_reserved']==2 and counts['last_event']=='synthetic_pair_complete'
        else:
            assert status.startswith('stopped:') and counts=={'materialize_reserved':1,'reset_reserved':2,'model_load_reserved':1,'reset_returned':2,'last_event':'aborted'}
            try:pair_synthetic.run_pair(output,inputs,setup,verify,mode=mode)
            except FileExistsError:counts['same_output_reentry_refused']=True
            else:raise AssertionError('same output was reusable')
        print(mode,status,json.dumps(counts,sort_keys=True))
