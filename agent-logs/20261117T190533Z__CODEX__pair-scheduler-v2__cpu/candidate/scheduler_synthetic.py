"""Fictional fixed-order scheduler; no scientific entrypoint or model loading."""
import json
from pathlib import Path
import select
import socket
import subprocess
import sys
import time
from dataclasses import asdict
from global_owner import GlobalOwner,SCHEDULE,Stop
from fixed_product_dev.arm_budget import StageBudgetChannel
from process_guard import capture_owned,finish_owned,stop_direct_if_same

HERE=Path(__file__).parent
class ChannelJournal:
    def __init__(self,owner,case,arm):self.owner=owner;self.case=case;self.arm=arm
    def emit(self,event,payload):self.owner.record('channel_'+event,{'case':self.case,'arm':self.arm,'payload':payload})

def run_fixture(root,fixture_root,inputs,materialize,verify,*,linger_case=None):
    """Fixed fake executable only. It cannot launch the scientific worker."""
    root=Path(root);root.mkdir(mode=0o700,parents=True,exist_ok=False)
    owner=GlobalOwner(root/'owner')
    try:
        if set(inputs)!={case for case,_ in SCHEDULE}:raise Stop('fixture roster mismatch')
        for case,order in SCHEDULE:
            binding=owner.materialize_pair(case,inputs[case],materialize,verify)
            for arm in order:
                armroot=root/(case+'-'+arm);armroot.mkdir(mode=0o700)
                work=armroot/'output';work.mkdir(mode=0o700)
                case_cfg={'case':case,'order':list(order),'seed':42,'public_goal':'fictional',
                          'input_sha256':{k:v['sha256'] for k,v in inputs[case].items()}}
                cfg={'output':str(work),'case':case_cfg,'arm':arm,'inputs':inputs[case],
                     'binding':binding,'port_source':'/home/lizening/research-notes/agent-logs/20261116__CODEX__two-object-paired-eval__candidate/gate-live/eprime_ports.py',
                     'fixture_root':str(fixture_root),'previous_initial':owner.initial}
                config_path=armroot/'config.json';config_path.write_text(json.dumps(cfg,sort_keys=True)+'\n')
                owner.begin_arm(case,arm,work/'worker_events.jsonl',inputs[case],verify)
                parent,child=socket.socketpair();parent.setblocking(False);proc=None;ident=None
                stderr_path=armroot/'fake-worker-stderr.log'
                try:
                    with stderr_path.open('wb') as stderr:
                        proc=subprocess.Popen([sys.executable,'-I','-B',str(HERE/'fake_worker.py'),
                            str(config_path),str(child.fileno()),'linger' if linger_case==case else 'normal'],
                            pass_fds=(child.fileno(),),start_new_session=True,stdout=subprocess.DEVNULL,stderr=stderr)
                        child.close();ident=capture_owned(proc)
                        owner.record('synthetic_child_started',{'case':case,'arm':arm,'pid':proc.pid,'identity':ident})
                        channel=StageBudgetChannel('EVAL',parent,ChannelJournal(owner,case,arm),
                                                   global_owner=owner,case=case,arm=arm)
                        deadline=time.monotonic()+10
                        while True:
                            if time.monotonic()>=deadline:raise Stop('fictional worker deadline')
                            if channel.ack_deadline is not None and time.monotonic()>=channel.ack_deadline:raise Stop('ACK deadline')
                            readable,writable,_=select.select([parent],[parent] if channel.pending_ack else [],[],0.05)
                            if writable:channel.write_ack()
                            if readable:
                                data=parent.recv(8192)
                                if not data:channel.eof();break
                                channel.receive(data)
                        if channel.finished!='COMPLETED':raise Stop('worker channel not complete')
                        cleanup=finish_owned(proc,ident,timeout=0.5 if linger_case==case else 5)
                    owner.close_arm_after_cleanup(case,arm,cleanup,inputs[case],verify)
                except BaseException as error:
                    if not owner.failed:owner.abort(type(error).__name__+': '+str(error))
                    if proc is not None and ident is not None:
                        try:
                            stop_direct_if_same(proc,ident)
                            owner.record('synthetic_cleanup_after_abort',{'case':case,'arm':arm,'pid':proc.pid,
                                'observed_returncode':proc.poll(),'scope':'own direct child only; other descendants unknown'})
                        except BaseException:
                            try:owner.record('synthetic_cleanup_after_abort',{'case':case,'arm':arm,'pid':proc.pid,
                                'observed_returncode':None,'scope':'cleanup unknown'})
                            except BaseException:pass
                    raise
                finally:
                    parent.close();child.close()
        owner.complete()
        return owner
    except BaseException as error:
        if not owner.failed:owner.abort(type(error).__name__+': '+str(error))
        raise
