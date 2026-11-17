"""Fictional fixed-order scheduler; no scientific entrypoint or model loading."""
import json
import hashlib
import static_adapter
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

def run_synthetic_bridge(root,fixture_root,inputs,materialize,verify,*,mode_by_case=None):
    """Four pair fake-only bridge. NEVER starts held scientific worker."""
    root=Path(root);root.mkdir(mode=0o700,parents=True,exist_ok=False)
    owner=GlobalOwner(root/'owner')
    owner.record('synthetic_scope',{'scientific_execution':'DISABLED','prior_real_budget':'UNKNOWN','budget_sufficiency':'NOT_VERIFIED','permission':'UNKNOWN','host_pid_visibility':'UNKNOWN'})
    try:
        if set(inputs)!={case for case,_ in SCHEDULE}:raise Stop('fixture roster mismatch')
        static_adapter.check_source_contract(HERE)
        cases=[{'case':c,'order':list(order),'public_goal':'fictional',
                'input_sha256':{k:v['sha256'] for k,v in inputs[c].items()}} for c,order in SCHEDULE]
        manifest={'schema':'FIXED_PRODUCT_FOUR_PAIR_DEV_V1','cases':cases,'env_seed':42,'horizon':50,'limits':static_adapter.LIMITS}
        manifest_bytes=static_adapter.canonical(manifest);manifest_path=root/'synthetic-manifest.json';manifest_path.write_bytes(manifest_bytes)
        products={'base_path':'/FICTION/base','base_tree_sha256':'1'*64,'products':{'P0':{'adapter_path':'/FICTION/P0','adapter_tree_sha256':'2'*64},'CANDIDATE':{'adapter_path':'/FICTION/C','adapter_tree_sha256':'3'*64}}}
        product_bytes=static_adapter.canonical(products)
        # Fictional placeholders only; neither admission nor proof of real historical costs.
        budget={'historical_ledger_sha256':'5'*64,'historical_used':{'generation':1,'environment_operations':1,'materialize':1},'prospective_ceiling':{'generation':500,'environment_operations':1000,'materialize':5},'proposed_additional':{'generation':400,'environment_operations':800,'materialize':4}}
        plan={'schema':'STATIC_PAIR_ADAPTER_V1','cases':cases,'env_seed':42,'limits':static_adapter.LIMITS,'budget':budget,'products':products}
        code_files=[{'path':str(HERE/name),'sha256':h} for name,h in static_adapter.SOURCE_HASHES.items()]

        for case,order in SCHEDULE:
            binding=owner.materialize_pair(case,inputs[case],materialize,verify)
            for arm in order:
                armroot=root/(case+'-'+arm);armroot.mkdir(mode=0o700)
                work=armroot/'output';work.mkdir(mode=0o700)
                draft=static_adapter.draft_arm_config(plan,product_bytes,hashlib.sha256(product_bytes).hexdigest(),
                    case=case,arm=arm,previous_initial=owner.initial,output=str(work),manifest_path=str(manifest_path),
                    manifest_sha256=hashlib.sha256(manifest_bytes).hexdigest(),manifest_bytes=manifest_bytes,
                    inputs=inputs[case],pair_binding=binding,source_root='/FICTION/source',legacy_dir='/FICTION/legacy',
                    candidate_root=str(HERE),code_files=code_files,
                    runtime_extra={'gpu_uuid':'FICTIONAL','packages':{},'runtime_identity':{}})
                cfg=draft['worker_config'];cfg['synthetic_test_context']={'classification':'FAKE_CPU_ONLY',
                    'fixture_root':str(fixture_root),
                    'port_source':'/home/lizening/research-notes/agent-logs/20261116__CODEX__two-object-paired-eval__candidate/gate-live/eprime_ports.py',
                    'mode':(mode_by_case or {}).get(case,'normal')}
                config_path=armroot/'config.json';config_raw=static_adapter.canonical(cfg);config_path.write_bytes(config_raw)
                config_sha=hashlib.sha256(config_raw).hexdigest()
                owner.begin_arm(case,arm,work/'worker_events.jsonl',inputs[case],verify)
                parent,child=socket.socketpair();parent.setblocking(False);proc=None;ident=None
                stderr_path=armroot/'fake-worker-stderr.log'
                try:
                    with stderr_path.open('wb') as stderr:
                        argv=[sys.executable,'-I','-B',str(HERE/'fake_cli_worker.py'),
                            '--config',str(config_path),'--config-sha256',config_sha,'--budget-fd',str(child.fileno())]
                        owner.record('synthetic_worker_cli',{'case':case,'arm':arm,'argv_sha256':hashlib.sha256(static_adapter.canonical(argv)).hexdigest(),
                            'config_sha256':config_sha,'budget_fd':child.fileno(),'scope':'fake child only; budget sufficiency not verified'})
                        proc=subprocess.Popen(argv,pass_fds=(child.fileno(),),start_new_session=True,stdout=subprocess.DEVNULL,stderr=stderr)
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
                        cleanup=finish_owned(proc,ident,timeout=5)
                    owner.close_arm_after_cleanup(case,arm,cleanup,inputs[case],verify)
                except BaseException as error:
                    if not owner.failed:owner.abort(type(error).__name__+': '+str(error))
                    if proc is not None and ident is None:
                        # Close only our IPC endpoints, then wait on the Popen child.
                        # Without a verified identity we never send a signal.
                        parent.close();child.close()
                        try:rc=proc.wait(timeout=3)
                        except subprocess.TimeoutExpired:rc=None
                        try:owner.record('synthetic_cleanup_after_abort',{'case':case,'arm':arm,'pid':proc.pid,
                            'observed_returncode':rc,'cleanup_status':'DIRECT_CHILD_REAPED_DESCENDANTS_UNKNOWN' if rc is not None else 'UNKNOWN_DIRECT_CHILD_STILL_UNREAPED', 'signal_sent':False,
                            'scope':'direct wait only; identity and descendants unknown'})
                        except BaseException:pass
                    elif proc is not None:
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


def launch_production(*_args,**_kwargs):
    raise RuntimeError('RESEARCH_HOLD: production worker launch bridge is disabled')
