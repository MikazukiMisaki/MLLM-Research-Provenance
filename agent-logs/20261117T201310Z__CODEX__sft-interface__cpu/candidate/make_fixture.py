"""Create only a hardcoded, fictional v7-shaped test fixture."""
import json
from pathlib import Path

def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()
objects={};rows=[]
for i,group in enumerate(('target','control')):
    refs={'index':i,'source_decision_id':'FAKE-DECISION-'+group,'prompt_ref':group+'-prompt','action_ref':group+'-action','label_ref':group+'-label','mask_ref':group+'-mask'}
    prompt=[11+i,22+i];label=[101,151645];mask=[0,0,1,1]
    objects[refs['prompt_ref']]={'text':'FICTIONAL '+group,'input_ids':prompt}
    objects[refs['action_ref']]={'mapping':{'A000':'do fictional action'},'selected_id':'A000','command':'do fictional action'}
    objects[refs['label_ref']]={'token_ids':label}
    objects[refs['mask_ref']]={'sequence_ids':prompt+label,'loss_mask':mask}
    rows.append({'parent':'FICTIONAL_PARENT','episode_id':'FICTIONAL_EPISODE','episode_ref':'fake-episode','terminal_ref':'fake-terminal',
        'group':group,'selection':{'index':i,'loop':group=='target','eligible_action':True,'action_id':'A000',
        'command':'do fictional action','label':label,'loss_mask':mask,'input_tokens':len(prompt),'refs':refs}})
fixture={'fixture_scope':'FICTIONAL_ONLY_NOT_AUTHENTICATED','rows':rows,'objects':objects}
Path('fixture.json').write_bytes(canon(fixture)+b'\n')
