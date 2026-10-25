"""Bounded one-shot launcher for pure CUDA identity, no model/environment import."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,signal,subprocess,time
ROOT=Path(__file__).resolve().parent
permit=Path(__import__('sys').argv[1]);expected=__import__('sys').argv[2]
assert hashlib.sha256(permit.read_bytes()).hexdigest()==expected
p=json.loads(permit.read_bytes());assert p['purpose']=='PURE_CUDA_IDENTITY_ONLY' and p['maximum_invocations']==1 and not p['science_authorized'] and not p['automatic_retry']
assert 0<p['seconds_cap']<=60
assert p['argv']==['/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python','-I',p['script_path']]
assert datetime.now(timezone.utc)<datetime.fromisoformat(p['expires_utc'])
script=Path(p['script_path']);assert hashlib.sha256(script.read_bytes()).hexdigest()==p['script_sha256']
out=Path(p['output_directory']);out.mkdir(exist_ok=False)
env=dict(p['environment']);env['SI_E2_IDENTITY_OUTPUT']=str(out/'identity_observation.json')
assert not set(env)&{'PYTHONPATH','PYTHONHOME','VIRTUAL_ENV','LD_PRELOAD'}
def identity(pid):
 try:
  f=Path('/proc')/str(pid);s=(f/'stat').read_text().rsplit(')',1)[1].split()
  return {'pid':pid,'uid':f.stat().st_uid,'start_tick':s[19],'pgid':int(s[2])}
 except FileNotFoundError:return None
start=time.monotonic();deadline=start+p['seconds_cap'];timeout=False;code=None;child=None;owner=None
with (out/'stdout.log').open('xb') as stdout,(out/'stderr.log').open('xb') as stderr:
 try:
  child=subprocess.Popen(p['argv'],env=env,cwd=ROOT,stdout=stdout,stderr=stderr,start_new_session=True)
  owner=identity(child.pid);assert owner and owner['uid']==os.getuid() and owner['pgid']==child.pid
  try:code=child.wait(timeout=max(0.001,deadline-time.monotonic()-5))
  except subprocess.TimeoutExpired:
   timeout=True
   if identity(child.pid)==owner:
    os.killpg(child.pid,signal.SIGKILL)
   code=child.wait(timeout=max(0.001,deadline-time.monotonic()))
 finally:
  if child is not None and child.poll() is None:
   if owner is not None and identity(child.pid)==owner:
    try:os.killpg(child.pid,signal.SIGKILL)
    except ProcessLookupError:pass
   try:code=child.wait(timeout=max(0.001,deadline-time.monotonic()))
   except subprocess.TimeoutExpired:code=None
  receipt={'UTC':datetime.now(timezone.utc).isoformat(),'permit_sha256':expected,'argv':p['argv'],'environment':env,'owner':owner,'authentic_returncode':code,'deadline_triggered':timeout,'elapsed_seconds':time.monotonic()-start,'within_seconds_cap':time.monotonic()<=deadline,'remaining':identity(child.pid) if child else None,'science_authorized':False,'automatic_retry':False}
  with (out/'launcher_receipt.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps(receipt))
raise SystemExit(0 if code==0 and not timeout and receipt['within_seconds_cap'] else 1)
