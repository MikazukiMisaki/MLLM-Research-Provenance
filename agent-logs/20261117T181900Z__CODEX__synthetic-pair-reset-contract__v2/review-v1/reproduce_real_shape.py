"""Synthetic reproduction of the real reset-capture wire shape; no real environment."""
import json
from pathlib import Path
import sys
import tempfile

target=Path('/home/lizening/research-notes/agent-logs/20261118__CODEX__synthetic-pair-combined__private')
sys.path.insert(0,str(target))
import bridge,pair_synthetic
from test_pair import fixture

before="'candidate_native_reset':{'won_batch':[False]}"
after="'candidate_native_reset':{'won_batch':[False],'won_batch_type':'list'}"
text=(target/'fake_arm.py').read_text()
assert text.count(before)==1
with tempfile.TemporaryDirectory(prefix='review-real-reset-shape-') as d:
    root=Path(d).resolve()
    (root/'fake_arm.py').write_text(text.replace(before,after))
    inputs,setup,verify=fixture(root)
    pair_synthetic.HERE=root
    output=root/'run'
    try:pair_synthetic.run_pair(output,inputs,setup,verify)
    except bridge.Stop as error:print('stop:',str(error))
    else:raise AssertionError('real-shape fixture unexpectedly accepted')
    rows=[json.loads(line) for line in (output/'owner'/'parent-ledger.jsonl').read_text().splitlines()]
    reserved=[r['payload'] for r in rows if r['event']=='reserved']
    print('model_load_reservations:',sum(r.get('operation')=='model_load' for r in reserved))
    print('last_event:',rows[-1]['event'])
    print('B_started:',(output/'arm-B').exists())
    assert rows[-1]['event']=='aborted'
    assert not any(r.get('operation')=='model_load' for r in reserved)
    assert not (output/'arm-B').exists()
