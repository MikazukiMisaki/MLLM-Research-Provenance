"""Imaginary EffectOwner client. No real environment/model/GPU functionality."""
import hashlib
import json
from pathlib import Path
import sys
import types
SOURCE=Path('/home/lizening/research-notes/agent-logs/20261116__CODEX__two-object-paired-eval__candidate/gate-live/effect_ipc.py')
SHA='046c0c48291efdae06457d87343d084357ae5a1774c3d670e3e232b15fd16dd8'
raw=SOURCE.read_bytes()
if hashlib.sha256(raw).hexdigest()!=SHA:raise SystemExit('source drift')
ipc=types.ModuleType('effect_ipc_bound');exec(compile(raw,str(SOURCE),'exec'),ipc.__dict__)
fd=int(sys.argv[1]);log=sys.argv[2];arm=sys.argv[3];paths=json.loads(sys.argv[4]);mode=sys.argv[5]
journal=ipc.Journal(log,1024*1024)
owner=ipc.EffectOwner(fd,journal,{op:1 for op in ('env_construct','env_init','reset','model_load','generation','step')})
controller=ipc.Controller(owner)
journal.emit('synthetic_input_paths',{'paths':paths})
try:
    controller.effect('env_construct',lambda:'fabricated construct')
    controller.effect('env_init',lambda:'fabricated init')
    state={'task_id':'synthetic','family':'synthetic','goal':'fictional goal',
           'observation':'B differs' if mode=='mismatch' and arm=='B' else 'same fake observation',
           'valid_actions':['fake action'],'done':False,'reward':0,'truncated':False}
    native={'won_batch':[False], 'won_batch_type':'tuple' if mode=='tuple' else 'list'}
    if arm=='B':
        if mode=='bad_true': native['won_batch']=[True]
        if mode=='bad_integer': native['won_batch']=[0]
        if mode=='bad_type': native['won_batch_type']='array'
        if mode=='bad_missing': native.pop('won_batch_type')
        if mode=='bad_extra': native['other']=False
        if mode=='bad_length': native['won_batch']=[False,False]
    controller.effect('reset',lambda:state,lambda x:{'arm':arm,'state':x,'gamefile':paths[0],
                                                      'candidate_native_reset':native})
    if mode=='interrupt' and arm=='A':
        owner.start('model_load',{})
        import os
        os._exit(7)
    controller.effect('model_load',lambda:'no model loaded')
    controller.effect('generation',lambda:'no generation')
    controller.effect('step',lambda:'no environment step')
    owner.finish('COMPLETED')
finally:
    owner.close();journal.close()
