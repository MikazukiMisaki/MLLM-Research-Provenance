from pathlib import Path
import hashlib
import sys
import tempfile
import types

root=Path('/home/lizening/research-notes/agent-logs/20261118__CODEX__pair-owned-real-interface__private')
sys.path.insert(0,str(root))
import global_owner
source=Path('/home/lizening/research-notes/agent-logs/20261116__CODEX__two-object-paired-eval__candidate/gate-live/effect_ipc.py')
raw=source.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='046c0c48291efdae06457d87343d084357ae5a1774c3d670e3e232b15fd16dd8'
ipc=types.ModuleType('effect_ipc_bound')
exec(compile(raw,str(source),'exec'),ipc.__dict__)
with tempfile.TemporaryDirectory() as tmp:
    path=Path(tmp)/'worker.jsonl'
    journal=ipc.Journal(path,100000)
    claim={'input_ids':[4,5],'attention_mask':[1,1],
           'kwargs':{'max_new_tokens':16,'do_sample':False,'num_return_sequences':2},
           'generation_config':{'eos_token_id':[151645,151643],'pad_token_id':151643,'forced_eos_token_id':None}}
    journal.emit('prepared',claim)
    journal.close()
    result=global_owner.claimed_prepared(path)
    assert result['input_ids']==[4,5] and result['seq']==0
    print('ACCEPTED: num_return_sequences=2, public missing, rendered_prompt missing')
    print('No model or generation was invoked; this demonstrates validation acceptance only.')
