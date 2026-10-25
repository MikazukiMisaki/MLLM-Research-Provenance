"""Coordinator launcher/monitor, executed only by Luna with exact external file hashes.

No model/environment APIs here. One Popen of the reviewed engineering CLI;
no retry. Kill signals are confined to recorded task-owned process identities.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import csv
import hashlib
import io
import json
import os
import signal
import subprocess
import time

ROOT=Path(__file__).resolve().parent
assert ROOT.name=='2026-10-25T124118Z__SOL__si-e2-runtime-resource-review__sie2_4c82'
def H(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=True,sort_keys=True,separators=(',',':'),allow_nan=False)
def fresh(path,x):
    with path.open('x') as f:f.write(json.dumps(x,indent=2)+'\n');f.flush();os.fsync(f.fileno())
def identity(pid):
    p=Path('/proc')/str(pid)
    try:
        s=(p/'stat').read_text().rsplit(')',1)[1].split()
        return {'pid':pid,'ppid':int(s[1]),'pgid':int(s[2]),'sid':int(s[3]),'start_tick':int(s[19]),'uid':p.stat().st_uid}
    except (FileNotFoundError,ProcessLookupError):return None
def same(a,b):return a is not None and b is not None and all(a[k]==b[k] for k in ('pid','start_tick','uid'))
def signal_owned(pid,original,sig):
    now=identity(pid)
    if same(original,now) and now['uid']==os.getuid():
        try:os.kill(pid,sig)
        except ProcessLookupError:pass
def readjson(path):return json.loads(path.read_bytes())

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--invocation',type=Path,required=True);parser.add_argument('--sha256',required=True)
    args=parser.parse_args();assert H(args.invocation)==args.sha256
    inv=readjson(args.invocation)
    assert inv['schema']=='SI_E2_ROOT_APPROVED_INVOCATION_V1' and inv['science_authorized'] is False
    assert inv['maximum_engineering_invocations']==1 and inv['automatic_retry'] is False
    for row in inv['bound_files']:assert H(row['path'])==row['sha256'],row['path']
    source=Path(inv['cwd']);output=Path(inv['output_path']);own=Path(inv['evidence_directory'])
    assert own==output.parent and not output.exists() and not output.is_symlink()
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip()==inv['source_SHA']
    assert not subprocess.check_output(['git','status','--porcelain'],cwd=source,text=True).strip()
    assert inv['environment_inherit'] is False
    env=inv['environment_set']
    assert not set(env)&{'PYTHONPATH','PYTHONHOME','VIRTUAL_ENV','LD_PRELOAD','HF_TOKEN','HUGGING_FACE_HUB_TOKEN'}
    assert env['CUDA_VISIBLE_DEVICES']==inv['gpu_uuid'] and env['HF_HUB_OFFLINE']==env['TRANSFORMERS_OFFLINE']=='1'
    assert hashlib.sha256(canonical(inv['argv']).encode()).hexdigest()==inv['argv_canonical_sha256']
    assert '--worker' not in inv['argv'] and inv['argv'][1]=='-I'
    assert Path(inv['argv'][2]).resolve()==source/'scripts/run_si_p3_engineering_probe.py'
    assert inv['argv'][0]=='/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python'
    fresh(own/'launcher_invocation.json',{'invocation_path':str(args.invocation),'invocation_sha256':args.sha256,
         'argv':inv['argv'],'cwd':str(source),'environment':env,'source_SHA':inv['source_SHA'],
         'UTC':datetime.now(timezone.utc).isoformat(),'science_authorized':False})
    started=time.monotonic();proc=None;owner=None;worker=None;stop_reason=None;error=None;peak=None;samples=0;code=None
    def sample():
        nonlocal worker,peak,samples
        if (output/'worker_start.json').exists():
            # The production marker is created before its JSON write completes.
            # A partial marker authorizes no PID; ownership checks below stay strict.
            try:r=readjson(output/'worker_start.json')
            except json.JSONDecodeError:r=None
            current=identity(r['pid']) if r is not None else None
            if current is not None:
                assert current['uid']==os.getuid() and current['ppid']==proc.pid and current['pgid']==current['sid']==current['pid'],'foreign worker identity'
                if worker is None:worker=current
                else:assert same(worker,current),'worker PID reused'
        allowed={proc.pid}
        if worker is not None:allowed.add(worker['pid'])
        raw={}
        queries={
          'gpu':['/usr/bin/nvidia-smi','--id='+inv['gpu_uuid'],'--query-gpu=uuid,memory.used,memory.free,utilization.gpu,power.draw','--format=csv,noheader,nounits'],
          'compute':['/usr/bin/nvidia-smi','--query-compute-apps=gpu_uuid,pid,process_name,used_gpu_memory','--format=csv,noheader,nounits']}
        for name,argv in queries.items():
            r=subprocess.run(argv,capture_output=True,text=True,timeout=5)
            raw[name]={'argv':argv,'subprocess_returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
        observation={'sequence':samples,'UTC':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-started,
                     'supervisor_identity':owner,'worker_identity':worker,'raw':raw}
        monitor.write(canonical(observation)+'\n');monitor.flush();os.fsync(monitor.fileno());samples+=1
        assert all(v['subprocess_returncode']==0 for v in raw.values()),'resource query failed'
        gpu=list(csv.reader(io.StringIO(raw['gpu']['stdout']),skipinitialspace=True))
        assert len(gpu)==1 and len(gpu[0])==5 and gpu[0][0]==inv['gpu_uuid'],'bound GPU drift'
        used=float(gpu[0][1]);peak=used if peak is None else max(peak,used)
        for row in csv.reader(io.StringIO(raw['compute']['stdout']),skipinitialspace=True):
            assert len(row)==4 and row[1].isdigit(),'unreadable compute row'
            if row[0]!=inv['gpu_uuid']:continue
            pid=int(row[1]);assert pid in allowed,'foreign compute PID'
            now=identity(pid);expected=owner if pid==proc.pid else worker
            assert same(now,expected) and now['uid']==os.getuid(),'unproven compute PID ownership'
        assert time.monotonic()-started<=inv['outer_wall_seconds_cap'],'outer deadline'
    with (own/'launcher.stdout').open('xb') as stdout,(own/'launcher.stderr').open('xb') as stderr,(own/'gpu_monitor.jsonl').open('x') as monitor:
        try:
            proc=subprocess.Popen(inv['argv'],cwd=source,env=env,stdout=stdout,stderr=stderr,start_new_session=True)
            owner=identity(proc.pid);assert owner is not None and owner['uid']==os.getuid()
            fresh(own/'launcher_start.json',{'supervisor_identity':owner,'started_monotonic':started,'UTC':datetime.now(timezone.utc).isoformat()})
            while proc.poll() is None:
                sample();time.sleep(1)
            code=proc.wait()
        except BaseException as exc:
            error={'exception':type(exc).__name__,'message':str(exc)};stop_reason='MONITOR_OR_LAUNCH_STOP'
        finally:
            if proc is not None:
                if proc.poll() is None:
                    signal_owned(proc.pid,owner,signal.SIGINT)
                    try:proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        # Parent cannot clean itself; only the recorded worker session may be killed.
                        if worker is not None and same(identity(worker['pid']),worker):
                            assert identity(worker['pid'])['pgid']==worker['pid']
                            try:os.killpg(worker['pid'],signal.SIGKILL)
                            except ProcessLookupError:pass
                        signal_owned(proc.pid,owner,signal.SIGKILL)
                try:code=proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    code=None;stop_reason='OWNED_PROCESS_STOP_NOT_CONFIRMED'
                    error={'exception':'TimeoutExpired','message':'Owned process remains after stop signals; no returncode fabricated'}
            receipt={'schema':'SI_E2_LUNA_LAUNCHER_RECEIPT_V1','source_SHA':inv['source_SHA'],
                     'invocation_sha256':args.sha256,'argv':inv['argv'],'cwd':str(source),
                     'authentic_launcher_returncode':code,'monitor_stop_reason':stop_reason,'error':error,
                     'elapsed_seconds':time.monotonic()-started,'sampled_peak_device_memory_used_MiB':peak,
                     'sample_count':samples,'supervisor_identity':owner,'worker_identity':worker,
                     'remaining_supervisor':identity(owner['pid']) if owner else None,
                     'remaining_worker':identity(worker['pid']) if worker else None,
                     'automatic_retry':False,'science_authorized':False}
            fresh(own/'launcher_receipt.json',receipt)
    print(json.dumps(receipt))
    return 0 if code==0 and error is None else 1

if __name__=='__main__':raise SystemExit(main())
