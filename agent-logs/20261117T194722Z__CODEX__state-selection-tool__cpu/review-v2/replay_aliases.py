import json,os,sys,tempfile,copy
from pathlib import Path
sys.path.insert(0,'/home/lizening/research-notes/agent-logs/20261118__CODEX__si-state-selection-cpu-v2__private')
import select_pairs as s, test_selector as f

def run(case):
    with tempfile.TemporaryDirectory() as t:
        root=Path(t)/'inputs';m=f.build_fixture(root)
        r0,r1=[item['episode_ref'] for item in m['train'][:2]]
        e0=json.loads((root/r0).read_bytes());e1=json.loads((root/r1).read_bytes())
        if case=='original_alias':
            for k in ('episode_id','terminal_ref','decisions'):e1[k]=e0[k]
        elif case=='terminal_hardlink':
            name='fake-hardlinked-terminal.json';os.link(root/e0['terminal_ref'],root/name)
            m['files'][name]=m['files'][e0['terminal_ref']];e1['terminal_ref']=name
        elif case=='decision_hardlinks':
            for key in ('prompt_ref','action_ref','label_ref','mask_ref'):
                source=e0['decisions'][0][key];name='link-'+source
                os.link(root/source,root/name);m['files'][name]=m['files'][source];e1['decisions'][0][key]=name
        elif case=='shared_label':e1['decisions'][0]['label_ref']=e0['decisions'][0]['label_ref']
        elif case=='copied_untrusted_identity':
            e1['episode_id']='FAKE-NEW-CLAIM';name='copied-terminal.json'
            (root/name).write_bytes((root/e0['terminal_ref']).read_bytes());m['files'][name]=m['files'][e0['terminal_ref']];e1['terminal_ref']=name
            e1['decisions']=copy.deepcopy(e0['decisions'])
            for i,d in enumerate(e1['decisions']):
                d['source_decision_id']='COPIED-CLAIM-'+str(i)
                for key in ('prompt_ref','action_ref','label_ref','mask_ref'):
                    source=d[key];name='copy-'+str(i)+'-'+key+'.json'
                    (root/name).write_bytes((root/source).read_bytes());m['files'][name]=m['files'][source];d[key]=name
        raw=f.encode(e1);(root/r1).write_bytes(raw);m['files'][r1]=f.sha(raw)
        try:result=s.build(m,root.resolve())
        except s.Reject as e:
            if case in ('shared_label','copied_untrusted_identity'):raise
            print(case,'REJECTED:',str(e))
        else:
            assert case in ('shared_label','copied_untrusted_identity') and len(result)==16
            print(case,'ACCEPTED: 16 caller-claimed parents only, identity remains UNKNOWN')
for case in ('original_alias','terminal_hardlink','decision_hardlinks','shared_label','copied_untrusted_identity'):run(case)
