"""New SI-P2 stdlib-only evidence I/O. No imports from previous audit or project."""
from pathlib import Path
import hashlib,json,subprocess,sys,time,datetime
sys.dont_write_bytecode=True
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T075610Z__CODEX__si-p2-common-quality__b04b8b')
COORD=OWN.parent/'2026-10-25T075610Z__SOL__si-p2-same-pool-review__b04b8b'
P1=OWN.parent/'2026-10-25T065200Z__CODEX__si-p1-eleven-targets__caae4c'
FROZEN=Path('/home/lizening/wt-r19-g4-consumer-contract-repair')
RUNTIME=Path('/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime')
R19=Path('/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z')
BINDINGS={}
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def vs(v):return hashlib.sha256(json.dumps(v,ensure_ascii=True,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ts(v):return hashlib.sha256(v.encode()).hexdigest()
def register(p):
 p=Path(p);k=str(p)
 if k not in BINDINGS:BINDINGS[k]={'path':k,'bytes':p.stat().st_size,'sha256_before':sha(p)}
 return p
def readjson(p):return json.loads(register(p).read_bytes())
def rows(p):
 with register(p).open('rb') as f:
  for n,line in enumerate(f,1):
   if line.strip():yield n,hashlib.sha256(line).hexdigest(),json.loads(line)
def output(name,obj):
 p=OWN/name;assert p.parent==OWN
 p.write_text(obj if isinstance(obj,str) else json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 return p
def finish_bindings(name='input_bindings.json'):
 for v in BINDINGS.values():
  v['sha256_after']=sha(v['path']);v['unchanged']=v['sha256_before']==v['sha256_after']
  assert v['unchanged'],v['path']
 output(name,list(BINDINGS.values()))
def authority():
 for name,h in [('SOL_RESEARCH_TASK.md','1fd57bda79a38b14d96a3543d5d325fa581fd11124c5bef6901f8f0b7a88f93a'),('COMMON_AUDIT_RULES.md','ab5e3afe8bb1e65ae1473254810ba56dfa769cefbd0952d0b2a0bdb32368ea69'),('PARENT_COHORT_MANIFEST.json','a3e2548e89280d150cbe83cceca632f9f91275ede0a4a9d89133e53691826078')]:assert sha(register(COORD/name))==h,name
 m=readjson(COORD/'PARENT_COHORT_MANIFEST.json');assert len(m['rows'])==171
 return m
SOURCES={'R4':RUNTIME/'validation/sft-recovery-source-pool-r1-20260908T042933Z/trajectories.jsonl','R10_OSR':RUNTIME/'validation/persistent-recovery-source-pool-r7-20260909T000000Z/trajectories.jsonl','R16_OSR':RUNTIME/'validation/progress-aware-recovery-r14-20260910T000000Z/raw_trajectories.jsonl','R19_K1':R19/'source_trajectories.jsonl'}
CONTROLS={'R4':RUNTIME/'validation/sft-recovery-replay-continue-r3-20260908T055308Z/continue_branches.jsonl','R10_OSR':RUNTIME/'validation/persistent-recovery-replay-continue-r9-20260909T033000Z/continue_branches.jsonl','R16_OSR':RUNTIME/'validation/progress-aware-recovery-r15-b-20260910T000000Z/continue_ledger.jsonl'}
REPLAYS={'R4':RUNTIME/'validation/sft-recovery-replay-continue-r3-20260908T055308Z/replay_validation.jsonl','R16_OSR':RUNTIME/'validation/progress-aware-recovery-r16-osr-20260910T000000Z/replay_ledger.jsonl'}
def canon(t):
 a=str(t).rstrip('/').split('/')
 for i in range(len(a)-1,0,-1):
  if a[i].startswith('trial_'):return a[i-1]+'/'+a[i]
 return str(t)
def parent_rows(m):
 loaded={}
 for spec in m['sources']:
  assert sha(register(spec['source_path']))==spec['full_file_sha256']
  loaded[spec['stage']]={n:(h,r) for n,h,r in rows(spec['source_path'])}
 out=[]
 for c in m['rows']:
  h,r=loaded[c['stage']][c['source_line']]
  assert h==c['source_row_sha256'] and r['prefix_id']==c['prefix_id']
  if c['stage']=='R19_K1':r={k:v for k,v in r.items() if k!='k_results'}|{'k_results':{'1':r.get('k_results',{}).get('1')}}
  out.append((c,r))
 return out

def run_receipt(script,stem):
 script=Path(script);assert script.parent==OWN
 lp=OWN/(stem+'.log');rp=OWN/(stem+'.receipt.json')
 assert not lp.exists() and not rp.exists()
 argv=[sys.executable,'-B',str(script)]
 started=datetime.datetime.now(datetime.timezone.utc).isoformat();start=time.monotonic()
 with lp.open('xb') as f:cp=subprocess.run(argv,cwd=OWN,stdout=f,stderr=subprocess.STDOUT,check=False)
 rec={'argv':argv,'cwd':str(OWN),'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-start,'returncode':cp.returncode,'script_sha256':sha(script),'combined_log_path':str(lp),'combined_log_sha256':sha(lp)}
 output(rp.name,rec)
 with (OWN/'commands.log').open('a') as f:f.write(json.dumps(rec,ensure_ascii=False)+'\n')
 print(json.dumps(rec,ensure_ascii=False));print(lp.read_text()[-18000:]);return cp.returncode
if __name__=='__main__':raise SystemExit(run_receipt(OWN/sys.argv[1],sys.argv[2]))
