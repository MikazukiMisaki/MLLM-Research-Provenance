#!/usr/bin/env python3
"""Capture exact baseline worktree, PID-namespace and future-path absence checks."""
import hashlib,json,os,subprocess,time
from datetime import datetime,timezone
from pathlib import Path
OWN=Path(__file__).resolve().parent; RAW=OWN/'raw'; RAW.mkdir(exist_ok=True)
COMMANDS=[
 ('a995_head',['git','-C','/home/lizening/wt-si-p3-engineering-contracts','rev-parse','HEAD'],'/'),
 ('a995_status',['git','-C','/home/lizening/wt-si-p3-engineering-contracts','status','--short','--branch'],'/'),
 ('a995_remote',['git','-C','/home/lizening/wt-si-p3-engineering-contracts','rev-parse','@{upstream}'],'/'),
]
env={k:os.environ[k] for k in ('PATH','LANG','LC_ALL','HOME','USER') if k in os.environ}; results=[]
for name,argv,cwd in COMMANDS:
 start=datetime.now(timezone.utc).isoformat(); t=time.monotonic_ns()
 try:
  p=subprocess.run(argv,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False); rc,out,err=p.returncode,p.stdout,p.stderr
 except Exception as e: rc,out,err=None,b'',(type(e).__name__+': '+str(e)).encode()
 end=datetime.now(timezone.utc).isoformat(); elapsed=(time.monotonic_ns()-t)/1e9
 op=RAW/f'{name}.stdout.bin'; ep=RAW/f'{name}.stderr.bin'; op.write_bytes(out); ep.write_bytes(err)
 results.append({'name':name,'argv':argv,'cwd':cwd,'started_utc':start,'ended_utc':end,'monotonic_elapsed_seconds':elapsed,'returncode':rc,'stdout':{'path':str(op),'bytes':len(out),'sha256':hashlib.sha256(out).hexdigest()},'stderr':{'path':str(ep),'bytes':len(err),'sha256':hashlib.sha256(err).hexdigest()}})
paths={
 'future_output_candidate':'/home/lizening/wt-si-p3-runtime-adaptation/artifacts/runtime/si_e2_luna_probe_a995d4c_20261025T124118Z',
 'future_record_candidate':str(OWN/'engineering_probe_supervisor'),
 'host_gpu_pid_5364_proc':'/proc/5364',
 'namespace_self':'/proc/self/ns/pid','namespace_pid1':'/proc/1/ns/pid'
}
checks={}
for name,path in paths.items():
 q=Path(path)
 try:
  exists=q.exists(); is_dir=q.is_dir()
  checks[name]={'path':path,'exists':exists,'is_dir':is_dir}
  if name.startswith('namespace_') and exists: checks[name]['link_target']=os.readlink(q)
 except OSError as exc:
  checks[name]={'path':path,'exists':'UNOBSERVABLE','is_dir':'UNOBSERVABLE','error':type(exc).__name__+': '+str(exc)}
(OWN/'state_absence_receipts.json').write_text(json.dumps({'schema':'SI_E2_BASELINE_AND_ABSENCE_CHECK_V1','commands':results,'path_checks':checks},sort_keys=True,indent=2)+'\n')
print(json.dumps({'returncodes':{r['name']:r['returncode'] for r in results},'path_checks':checks,'receipt':str(OWN/'state_absence_receipts.json')},sort_keys=True))
