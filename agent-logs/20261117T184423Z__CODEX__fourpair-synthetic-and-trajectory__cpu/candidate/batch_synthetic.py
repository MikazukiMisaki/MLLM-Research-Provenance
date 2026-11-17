"""Four fictional pairs; no scientific entrypoint and no real environment."""
import json
from pathlib import Path
import socket
import subprocess
import sys
import bridge
from candidate import snapshot

HERE=Path(__file__).parent

def run_batch(root,inputs,setup,verify,*,schedule=None,mode_by_pair=None):
    root=Path(root);root.mkdir(mode=0o700,parents=True,exist_ok=False)
    caps={'materialize':4, **{op:(16 if op in ('generation','step') else 8) for op in bridge.OPS}}
    owner=bridge.Budget(root/'owner',caps)
    schedule=bridge.SCHEDULE if schedule is None else tuple(schedule)
    mode_by_pair={} if mode_by_pair is None else mode_by_pair
    def journal(event,payload):owner.record('setup_detail',{'event':event,'payload':payload})
    try:
        if schedule!=bridge.SCHEDULE or set(inputs)!={p for p,_ in bridge.SCHEDULE}:
            raise bridge.Stop('fictional schedule mismatch before setup')
        for pair,order in schedule:
            if owner.failed or bridge.SCHEDULE[owner.pair_index]!=(pair,order) or owner.active:
                raise bridge.Stop('pair order or unfinished operation')
            owner.arm_index=0;owner.setup_returned=False;owner.public_claim=None;owner.bound_files=None
            pairroot=root/('pair-'+pair);pairroot.mkdir(mode=0o700)
            if pair in owner.setups or owner.counts['materialize']>=owner.caps['materialize']:
                raise bridge.Stop('fictional setup cap')
            ticket={'pair':pair,'arm':None,'seq':0,'operation':'materialize'}
            owner.record('reserved',ticket);owner.counts['materialize']+=1;owner.active=ticket;owner.setups.add(pair)
            paths=setup(pairroot,inputs[pair],journal,family='two')
            if not isinstance(paths,tuple) or len(paths)!=3:raise bridge.Stop('bad synthetic setup')
            bound=snapshot(paths,pairroot)
            owner.record('returned',dict(ticket,synthetic_paths=bound));owner.active=None
            owner.setup_returned=True;owner.bound_files=bound
            for arm in order:
                verify(*paths,inputs[pair],journal,'pre')
                if snapshot(paths,pairroot)!=bound:raise bridge.Stop('input drift before arm')
                key=(pair,arm)
                owner.record('arm_pre_verified',{'pair':pair,'arm':arm,'bound':bound});owner.prepared.add(key)
                armroot=root/('arm-'+pair+'-'+arm);armroot.mkdir(mode=0o700)
                parent,child=socket.socketpair();proc=None
                try:
                    proc=subprocess.Popen([sys.executable,'-I','-B',str(HERE/'fake_arm.py'),str(child.fileno()),
                        str(armroot/'worker.jsonl'),arm,json.dumps(list(map(str,paths))),mode_by_pair.get(pair,'normal'),
                        json.dumps(owner.public_claim)],pass_fds=(child.fileno(),),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                    child.close();owner.serve(parent,pair,arm,armroot/'worker.jsonl')
                    rc=proc.wait(timeout=8);owner.record('synthetic_child_exit',{'pair':pair,'arm':arm,'returncode':rc})
                    if rc:raise bridge.Stop('fake child nonzero')
                finally:
                    parent.close();child.close()
                    if proc is not None and proc.poll() is None:
                        proc.terminate();proc.wait(timeout=3)
                verify(*paths,inputs[pair],journal,'post')
                if snapshot(paths,pairroot)!=bound:raise bridge.Stop('input drift after arm')
                owner.record('arm_post_verified',{'pair':pair,'arm':arm});owner.closed.add(key);owner.arm_index+=1
            owner.pair_index+=1
        expected=[(p,a) for p,order in bridge.SCHEDULE for a in order]
        if (owner.failed or owner.active or owner.pair_index!=4 or owner.counts['materialize']!=4 or
            owner.finished!=expected or owner.closed!=set(expected) or owner.setups!={p for p,_ in bridge.SCHEDULE}):
            raise bridge.Stop('incomplete synthetic batch')
        owner.record('synthetic_batch_complete',{'counts':owner.counts.copy()})
        return owner
    except BaseException as error:
        if not owner.failed:owner.abort(type(error).__name__+': '+str(error))
        raise
