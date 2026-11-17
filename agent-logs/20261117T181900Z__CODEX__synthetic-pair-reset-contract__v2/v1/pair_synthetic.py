"""One synthetic pair; explicitly not an experiment launcher."""
import json
from pathlib import Path
import socket
import subprocess
import sys
import bridge
from candidate import snapshot

HERE=Path(__file__).parent

def run_pair(root,inputs,setup,verify,mode='normal',hook=None):
    root=Path(root);root.mkdir(mode=0o700,parents=True,exist_ok=False)
    caps={'materialize':1, **{op:2 for op in bridge.OPS}}
    owner=bridge.Budget(root/'owner',caps)
    pairroot=root/'pair';pairroot.mkdir(mode=0o700)
    proc=None
    def journal(event,payload):owner.record('setup_detail',{'event':event,'payload':payload})
    try:
        ticket={'arm':None,'seq':0,'operation':'materialize'}
        owner.record('reserved',ticket);owner.counts['materialize']+=1;owner.active=ticket
        paths=setup(pairroot,inputs,journal,family='two')
        if not isinstance(paths,tuple) or len(paths)!=3:raise bridge.Stop('bad synthetic setup')
        bound=snapshot(paths,pairroot)
        owner.record('returned',dict(ticket,synthetic_paths=bound));owner.active=None
        owner.setup_returned=True;owner.bound_files=bound
        for arm in ('A','B'):
            verify(*paths,inputs,journal,'pre')
            if snapshot(paths,pairroot)!=bound:raise bridge.Stop('input drift before arm')
            owner.record('arm_pre_verified',{'arm':arm,'bound':bound});owner.prepared.add(arm)
            armroot=root/('arm-'+arm);armroot.mkdir(mode=0o700)
            parent,child=socket.socketpair()
            try:
                proc=subprocess.Popen([sys.executable,'-I','-B',str(HERE/'fake_arm.py'),str(child.fileno()),
                     str(armroot/'worker.jsonl'),arm,json.dumps(list(map(str,paths))),mode],
                     pass_fds=(child.fileno(),),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                child.close()
                owner.serve(parent,arm,armroot/'worker.jsonl')
                rc=proc.wait(timeout=8)
                owner.record('synthetic_child_exit',{'arm':arm,'returncode':rc})
                if rc:raise bridge.Stop('fake child nonzero')
            finally:
                parent.close();child.close()
                if proc is not None and proc.poll() is None:
                    proc.terminate();proc.wait(timeout=3)
            if hook is not None:hook(arm,paths)
            verify(*paths,inputs,journal,'post')
            if snapshot(paths,pairroot)!=bound:raise bridge.Stop('input drift after arm')
            owner.record('arm_post_verified',{'arm':arm});owner.closed.add(arm)
        if owner.finished!=['A','B'] or owner.closed!={'A','B'} or owner.counts['materialize']!=1 or owner.active:
            raise bridge.Stop('incomplete synthetic pair')
        owner.record('synthetic_pair_complete',{'counts':owner.counts.copy()})
        return owner
    except BaseException as error:
        if not owner.failed:owner.abort(type(error).__name__+': '+str(error))
        raise
