"""Only no-side-effect Python callbacks. Imports pinned worker IPC from exact bytes."""
import hashlib
import os
from pathlib import Path
import sys
import types

SOURCE=Path('/home/lizening/research-notes/agent-logs/20261116__CODEX__two-object-paired-eval__candidate/gate-live/effect_ipc.py')
EXPECTED='046c0c48291efdae06457d87343d084357ae5a1774c3d670e3e232b15fd16dd8'
raw=SOURCE.read_bytes()
if hashlib.sha256(raw).hexdigest()!=EXPECTED:raise SystemExit('source hash mismatch')
mod=types.ModuleType('pinned_effect_ipc');mod.__file__=str(SOURCE)
exec(compile(raw,str(SOURCE),'exec'),mod.__dict__)
fd=int(sys.argv[1]);journal_path=sys.argv[2];mode=sys.argv[3]
journal=mod.Journal(journal_path,1024*1024)
owner=mod.EffectOwner(fd,journal,{'model_load':1,'generation':2 if mode=='over_arm' else 1})
controller=mod.Controller(owner)
try:
    if mode in ('orphan','wrong_started'):
        owner._exchange({'kind':'reserve','seq':0,'operation':'generation'})
        if mode=='wrong_started': journal.emit('model_load_started',{'owner_seq':0})
        receipt=journal.emit('generation_returned',{'owner_seq':0,'evidence':{'synthetic':True}})
        owner._exchange({'kind':'returned','seq':0,'operation':'generation','receipt_sha256':receipt})
    elif mode=='interrupt':
        owner.start('model_load',{})
        os._exit(7)
    if mode=='unknown':
        def failure():raise ValueError('fabricated failure')
        controller.effect('model_load',failure)
    else:
        def synthetic_load():
            if mode=='interleaved': journal.emit('synthetic_note',{'text':'not an effect event'})
            return 'synthetic load'
        controller.effect('model_load',synthetic_load)
        if mode=='old_duplicate': journal.emit('model_load_started',{'owner_seq':0})
        controller.effect('generation',lambda: 'synthetic generation')
        if mode=='over_arm': controller.effect('generation',lambda: 'extra synthetic generation')
        owner.finish('COMPLETED')
finally:
    owner.close();journal.close()
