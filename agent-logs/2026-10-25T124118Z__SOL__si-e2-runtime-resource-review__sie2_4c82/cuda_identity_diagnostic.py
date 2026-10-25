"""One separately released device-identity observation. No model or environment API."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,time
OUT=Path(os.environ['SI_E2_IDENTITY_OUTPUT'])
UUID='GPU-b08bc603-ebdb-787d-b5b6-ec796ea3022a'
def query(args):
 r=subprocess.run(['/usr/bin/nvidia-smi',*args],capture_output=True,text=True,timeout=5)
 return {'argv':r.args,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
def gpu():return query(['--id='+UUID,'--query-gpu=uuid,name,memory.used,memory.free','--format=csv,noheader,nounits'])
def compute():return query(['--query-compute-apps=gpu_uuid,pid,process_name,used_gpu_memory','--format=csv,noheader,nounits'])
def fresh(x,path=OUT):
 with path.open('x') as f:json.dump(x,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
assert not OUT.exists() and os.environ['CUDA_VISIBLE_DEVICES']==UUID
started=time.monotonic();r={'schema':'SI_E2_PURE_CUDA_IDENTITY_OBSERVATION_V1','UTC':datetime.now(timezone.utc).isoformat(),'expected_uuid':UUID,'pid':os.getpid(),'ppid':os.getppid(),'uid':os.getuid(),'science_authorized':False,'model_loads':0,'generations':0,'environment_calls':0,'automatic_retry':False,'cuda_init_entered':False,'one_byte_allocation_completed':False}
try:
 r['namespace']={k:Path('/proc/self/'+k).read_text() for k in ('status','cgroup')}
 r['nspid_namespace_link']=os.readlink('/proc/self/ns/pid')
 r['GPU_before']=gpu();r['compute_before']=compute()
 assert r['GPU_before']['returncode']==r['compute_before']['returncode']==0
 assert not r['compute_before']['stdout'].strip(),'foreign compute before identity diagnostic'
 import torch
 p=Path(torch.__file__)
 r['torch']={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'version':torch.__version__}
 assert r['torch']['sha256']=='5a190666c3853aa236c4d48ed64e2d4bbcd23bd32c21e64c0867646a6852e43f'
 r['CUDA_VISIBLE_DEVICES']=os.environ['CUDA_VISIBLE_DEVICES'];r['cuda_available']=torch.cuda.is_available();r['device_count']=torch.cuda.device_count()
 assert r['cuda_available'] and r['device_count']==1
 r['cuda_init_entered']=True;torch.cuda.init()
 prop=torch.cuda.get_device_properties(0);value=getattr(prop,'uuid',None)
 r['device_properties_repr']=repr(prop)
 r['uuid']={'present':hasattr(prop,'uuid'),'type_module':type(value).__module__,'type_name':type(value).__qualname__,'repr':repr(value),'str':str(value),'direct_str_matches_expected':str(value)==UUID}
 fresh(r,OUT.parent/'pre_allocation_identity.json')
 r['current_device']=torch.cuda.current_device()
 t=torch.empty(1,dtype=torch.uint8,device='cuda:0');torch.cuda.synchronize();r['one_byte_allocation_completed']=True
 r['cuda_memory']={'allocated':torch.cuda.memory_allocated(),'reserved':torch.cuda.memory_reserved(),'max_allocated':torch.cuda.max_memory_allocated()}
 r['GPU_after']=gpu();r['compute_after']=compute()
 assert r['GPU_after']['returncode']==r['compute_after']['returncode']==0,'post-allocation resource query failed'
 rows=[x.strip().split(', ') for x in r['compute_after']['stdout'].splitlines() if x.strip()]
 r['own_compute_row_observed']=any(len(x)>=2 and x[0]==UUID and x[1]==str(os.getpid()) for x in rows)
 r['unexpected_compute_rows']=[x for x in rows if len(x)<2 or x[0]!=UUID or x[1]!=str(os.getpid())]
 r['status']='IDENTITY_RAW_OBSERVED_OWNERSHIP_PROVEN' if r['own_compute_row_observed'] and not r['unexpected_compute_rows'] else 'IDENTITY_RAW_OBSERVED_OWNERSHIP_UNPROVEN'
 del t
except BaseException as e:
 r['status']='IDENTITY_DIAGNOSTIC_FAILED_NO_RETRY';r['error']={'type':type(e).__name__,'message':str(e)}
finally:
 r['elapsed_seconds']=time.monotonic()-started;r['device_hours_upper_bound']=r['elapsed_seconds']/3600
 fresh(r)
print(json.dumps({'status':r['status'],'output':str(OUT),'elapsed_seconds':r['elapsed_seconds']}))
raise SystemExit(0 if r['status']=='IDENTITY_RAW_OBSERVED_OWNERSHIP_PROVEN' else 1)
