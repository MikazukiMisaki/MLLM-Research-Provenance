"""One B-only supervised run. Requires separate independent clearance; no C."""
import hashlib,json,os,subprocess,sys,time
from datetime import datetime,timezone
from pathlib import Path
here=Path(__file__).resolve().parent;repo=Path('/home/lizening/wt-si-self-imitation-train');astra=Path('/home/lizening/research-notes/agent-logs/2026-10-29T113523Z__ASTRA__three-arm-prospective-design__a55d1af9');pre=Path('/home/lizening/research-notes/agent-logs/2026-10-29T134700Z__LUNA__si-pilot82-b-preflight__9bbaa');auth=repo/'configs/local/si_pilot82_b_authorization_064d0c7f39f14414acf24f399188f85f.json';authsha='b34fbf7d608aae53a492fc243d76230442221446974e25f856a0e8948c7f983f';prehash='79033dc27df69c3b6d52d8995cedccc587d41fb682a5764d65f393a7895d3268';source='9bbaa12c2d8177a60ec5a74ed2f970ef29a57bce'
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def tree(path):
 p=Path(path);rows=[]
 for x in sorted(p.rglob('*')):
  if x.is_symlink() and not x.is_file():raise ValueError('bad model symlink')
  if x.is_file():rows.append([x.relative_to(p).as_posix(),x.stat().st_size,sha(x)])
  elif not x.is_dir():raise ValueError('unexpected model tree entry')
 return hashlib.sha256(json.dumps(rows,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def call(args):
 p=subprocess.run(args,cwd=repo,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=15);return {'argv':args,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'utc':now()}
def now():return datetime.now(timezone.utc).isoformat()
def put(path,obj):
 with path.open('x') as f:json.dump(obj,f,indent=2,sort_keys=True);f.write('\n');f.flush();os.fsync(f.fileno())
if len(sys.argv)!=3:raise SystemExit('separate clearance path and sha required')
clear=Path(sys.argv[1]);clearsha=sys.argv[2]
if not clear.is_absolute() or sha(clear)!=clearsha or sha(auth)!=authsha:raise SystemExit('authority mismatch')
A=json.loads(auth.read_text());C=json.loads(clear.read_text());receipt=Path(A['preflight_path']);R=json.loads(receipt.read_text());proc=json.loads((pre/'PREFLIGHT_PROCESS_RECEIPT.json').read_text())
expected={'schema':'SI_CONTINUATION_CLEARANCE_V1','decision':'RELEASE_ONE_ARM','binding':R['binding'],'preflight_sha256':prehash,'maximum_launches':1,'retry_authorized':False}
if C!=expected or sha(receipt)!=prehash or R['status']!='PREFLIGHT_ONLY_PASS' or any(R['effects'].values()) or proc['authentic_returncode']!=0 or proc['authorization_sha256']!=authsha or proc['preflight_receipt_sha256']!=prehash:raise SystemExit('clearance or actual preflight mismatch')
if sha(pre/'child.stdout')!=proc['stdout_sha256'] or sha(pre/'child.stderr')!=proc['stderr_sha256'] or proc['timed_out'] or proc['exception'] is not None:raise SystemExit('preflight process evidence mismatch')
if A['source_sha']!=source or A['arm']!='B' or A['run_id']!='064d0c7f39f14414acf24f399188f85f' or A['allocation_seconds']!=5400 or A['maximum_launches']!=1:raise SystemExit('B authority scope mismatch')
checks=[('BC_AUTHORIZATION_DRAFT_INDEPENDENT_REVIEW_9BBAA.json','f3e789b11cd3bed5bc9a7853443af18578c57314f61ab46accd819984d56d065'),('ENGINEERING_REAL_SUCCESS_AUDIT_9BBAA.json','eeb6cd2f0bbbebfbfea8c24f0c2acf19772480d3e4341c85c384127921cb5a94'),('EVAL_ENGINEERING_REAL_RESULT_REVIEW_8532275.json','0132bc3b58d12c89bbf12cc8da78052d6518a49eb1c8e2fb96d83582358cb195')]
for n,h in checks:
 if sha(astra/n)!=h:raise SystemExit('independent engineering or draft review changed')
if any(sha(A[k]['path'])!=A[k]['sha256'] for k in ('manifest','paired_manifest','protocol','pair_review','review')):raise SystemExit('frozen input or review drift')
for k in ('manifest','paired_manifest'):
 m=json.loads(Path(A[k]['path']).read_text())
 if sha(m['dataset']['path'])!=m['dataset']['sha256'] or sha(m['independent_review']['path'])!=m['independent_review']['sha256']:raise SystemExit('paired dataset or independent review drift')
if tree(A['base']['path'])!=A['base']['sha256'] or tree(A['adapter']['path'])!=A['adapter']['sha256']:raise SystemExit('frozen base/P0 drift')
output=Path(A['output_path']);claim=output.with_name(output.name+'.claim.json')
if output.exists() or output.is_symlink() or claim.exists() or claim.is_symlink():raise SystemExit('B identity consumed; no retry')
head=call(['git','rev-parse','HEAD']);status=call(['git','status','--porcelain'])
if head['returncode'] or head['stdout'].strip()!=source or status['returncode'] or status['stdout'].strip():raise SystemExit('scientific source checkout drift')
gpu=call(['nvidia-smi','--query-gpu=uuid,memory.used,memory.free,utilization.gpu','--format=csv,noheader,nounits']);apps=call(['nvidia-smi','--query-compute-apps=pid,process_name,used_gpu_memory','--format=csv,noheader,nounits']);rows=[x.split(', ') for x in gpu['stdout'].strip().splitlines() if x.startswith(A['gpu']['uuid']+',')]
if gpu['returncode'] or apps['returncode'] or len(rows)!=1 or int(rows[0][2])*1048576<A['gpu']['preweight_free_bytes'] or int(rows[0][3])!=0 or apps['stdout'].strip():raise SystemExit('fresh shared GPU resource check failed')
remaining=(datetime.fromisoformat(A['expires'].replace('Z','+00:00'))-datetime.now(timezone.utc)).total_seconds()
if remaining<5520:raise SystemExit('insufficient time for full 5400-second allocation plus 120-second margin')
argv=[A['interpreter'],'-I',str(repo/'scripts/run_si_continuation.py'),'--live','--authorization',str(auth),'--authorization-sha256',authsha,'--clearance',str(clear),'--clearance-sha256',clearsha]
put(here/'ONE_SHOT_B_DISPATCH.json',{'schema':'SI_U1_LUNA_B_LIVE_DISPATCH_V1','utc':now(),'cwd':str(repo),'argv':argv,'environment':A['environment'],'source_sha':source,'authorization_sha256':authsha,'clearance_sha256':clearsha,'preflight_sha256':prehash,'allocation_seconds':5400,'remaining_authorization_seconds_at_dispatch':remaining,'engineering_device_seconds_separate':455.8560599721968,'gpu_before_devicewide':gpu,'compute_apps_before':apps,'retry_authorized':False,'c_automatically_started':False})
t0=time.monotonic();p=None;rc=None;error=None
with (here/'launcher.stdout').open('xb') as out,(here/'launcher.stderr').open('xb') as err,(here/'gpu_samples.jsonl').open('x') as samples:
 try:
  p=subprocess.Popen(argv,cwd=repo,env=A['environment'],stdout=out,stderr=err,start_new_session=True);put(here/'LAUNCHER_START.json',{'pid':p.pid,'utc':now(),'argv':argv})
  while p.poll() is None:
   sample=call(['nvidia-smi','--query-gpu=uuid,memory.used,memory.free,utilization.gpu','--format=csv,noheader,nounits']);samples.write(json.dumps(sample,sort_keys=True)+'\n');samples.flush();time.sleep(15)
  rc=p.wait()
 except BaseException as exc:
  error={'type':type(exc).__name__,'message':str(exc)}
  if p is not None and p.poll() is None:
   p.terminate()
   try:rc=p.wait(timeout=10)
   except subprocess.TimeoutExpired:p.kill();rc=p.wait()
end={'schema':'SI_U1_LUNA_B_LIVE_PROCESS_V1','end_utc':now(),'elapsed_seconds':time.monotonic()-t0,'supervisor_pid':p.pid if p else None,'authentic_returncode':rc,'wrapper_error':error,'stdout_sha256':sha(here/'launcher.stdout'),'stderr_sha256':sha(here/'launcher.stderr'),'gpu_samples_sha256':sha(here/'gpu_samples.jsonl'),'gpu_after':call(['nvidia-smi','--query-gpu=uuid,memory.used,memory.free,utilization.gpu','--format=csv,noheader,nounits']),'compute_apps_after':call(['nvidia-smi','--query-compute-apps=pid,process_name,used_gpu_memory','--format=csv,noheader,nounits']),'retry_authorized':False,'c_automatically_started':False}
put(here/'LAUNCHER_EXIT.json',end);print(json.dumps(end));raise SystemExit(0 if rc==0 and error is None else 1)
