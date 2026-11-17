"""Build deterministic fiction only, no model or data access."""
import json
from pathlib import Path
rows=[]
for i in range(16):
    prompt=[i%3,(i+1)%3];generated=[(i+2)%3,3] if i%2==0 else [i%3,(i+2)%3,3]
    rows.append({'row_id':f'FAKE-{i:02d}','input_ids':prompt+generated,
                 'loss_mask':[0]*len(prompt)+[1]*len(generated),'prompt_length':len(prompt)})
Path('fixture.json').write_bytes(json.dumps({'scope':'FICTIONAL_UNAUTHENTICATED','rows':rows},sort_keys=True,separators=(',',':')).encode()+b'\n')
