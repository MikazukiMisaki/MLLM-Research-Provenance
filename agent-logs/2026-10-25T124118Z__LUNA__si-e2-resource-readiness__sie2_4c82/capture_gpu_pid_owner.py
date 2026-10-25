#!/usr/bin/env python3
"""Read process ownership for the graphics PID reported by nvidia-smi."""
import hashlib,json,os,subprocess,time
from datetime import datetime,timezone
from pathlib import Path
OWN=Path(__file__).resolve().parent; RAW=OWN/'raw'; RAW.mkdir(exist_ok=True)
pid='5364'
commands=[
 ('gpu_pid_ps',['ps','-p',pid,'-o','pid,ppid,user,lstart,etime,comm'], '/'),
 ('gpu_pid_status',['bash','-c',f"awk '/^(Name|State|Pid|PPid|Uid|Gid|Threads):/{{print}}' /proc/{pid}/status"],'/'),
 ('gpu_pid_cgroup',['cat',f'/proc/{pid}/cgroup'],'/'),
]
env={k:os.environ[k] for k in ('PATH','LANG','LC_ALL','HOME','USER') if k in os.environ}; rows=[]
for name,argv,cwd in commands:
 start=datetime.now(timezone.utc).isoformat(); t=time.monotonic_ns()
 try:
  p=subprocess.run(argv,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False); rc,out,err=p.returncode,p.stdout,p.stderr
 except Exception as e: rc,out,err=None,b'',(type(e).__name__+': '+str(e)).encode()
 end=datetime.now(timezone.utc).isoformat(); elapsed=(time.monotonic_ns()-t)/1e9
 op=RAW/f'{name}.stdout.bin'; ep=RAW/f'{name}.stderr.bin'; op.write_bytes(out); ep.write_bytes(err)
 rows.append({'name':name,'argv':argv,'cwd':cwd,'started_utc':start,'ended_utc':end,'monotonic_elapsed_seconds':elapsed,'returncode':rc,'stdout':{'path':str(op),'bytes':len(out),'sha256':hashlib.sha256(out).hexdigest()},'stderr':{'path':str(ep),'bytes':len(err),'sha256':hashlib.sha256(err).hexdigest()}})
(OWN/'gpu_pid_owner_receipts.json').write_text(json.dumps({'schema':'SI_E2_GPU_PID_OWNER_CAPTURE_V1','source_pid':pid,'commands':rows},sort_keys=True,indent=2)+'\n')
print(json.dumps({'source_pid':pid,'returncodes':{r['name']:r['returncode'] for r in rows},'receipt':str(OWN/'gpu_pid_owner_receipts.json')},sort_keys=True))
