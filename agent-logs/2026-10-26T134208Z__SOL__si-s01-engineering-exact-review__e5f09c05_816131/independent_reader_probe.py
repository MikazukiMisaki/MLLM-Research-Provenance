from pathlib import Path
import hashlib,importlib.abc,json,os,subprocess,sys
repo,manifest_path,out=map(Path,sys.argv[1:4])
assert not out.exists()
sys.path[:0]=[str(repo/'src')]
forbidden_roots={'torch','transformers','peft','alfworld','textworld','pynvml'}
class NoRuntime(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0] in forbidden_roots or fullname in {'self_improvement.si_s01.runtime','self_improvement.si_s01.runtime_core','self_improvement.si_s01.engineering_runtime','self_improvement.si_s01.engineering_gate'}:
   raise RuntimeError('forbidden runtime import '+fullname)
sys.meta_path.insert(0,NoRuntime())
def no_process(*a,**kw):raise RuntimeError('reader cannot start any process')
subprocess.Popen=no_process;subprocess.run=no_process;subprocess.check_output=no_process;os.system=no_process
raw=manifest_path.read_bytes();manifest_sha=hashlib.sha256(raw).hexdigest()
assert manifest_sha=='c361ba0c9d9276eb7dc20c31d0428f51db3f1a9fdd7fccfa23db5edc4f64eb38'
m=json.loads(raw);specs=[m['trajectory'],*m['events']];allowed={}
for x in specs:allowed.setdefault(Path(x['path']).resolve(),[]).append((x['byte_offset'],x['byte_offset']+x['line_length_bytes'],x['raw_line_sha256']))
def states():
 return {str(p):{'size':p.stat().st_size,'mtime_ns':p.stat().st_mtime_ns,'inode':p.stat().st_ino} for p in allowed}
before=states();reads=[];base_open=Path.open
class SliceFile:
 def __init__(self,stream,path):self.stream,self.path=stream,path
 def __enter__(self):return self
 def __exit__(self,*a):return self.stream.__exit__(*a)
 def seek(self,n,whence=0):
  assert whence==0 and type(n) is int and 0<=n<=max(b for a,b,h in allowed[self.path]);return self.stream.seek(n,whence)
 def read(self,n=-1):
  at=self.stream.tell();assert type(n) is int and n>0
  permitted=any(a<=at and at+n<=b for a,b,h in allowed[self.path]) or (n==1 and any(at==a-1 for a,b,h in allowed[self.path] if a))
  assert permitted,(str(self.path),at,n)
  value=self.stream.read(n);reads.append({'path':str(self.path),'offset':at,'length':n,'returned':len(value),'sha256':hashlib.sha256(value).hexdigest()});return value
 def __getattr__(self,k):return getattr(self.stream,k)
def bounded_open(path,mode='r',*a,**kw):
 p=path.resolve()
 if p in allowed:
  assert mode=='rb';return SliceFile(base_open(path,mode,*a,**kw),p)
 if '/artifacts/' in str(p):raise RuntimeError('unapproved artifact read '+str(p))
 return base_open(path,mode,*a,**kw)
Path.open=bounded_open
from self_improvement.si_s01.engineering_history import read_historical
from self_improvement.si_s01.engineering_contract import MODE,HISTORY_MANIFEST_SHA256,RNG_STATUS
h=read_historical(raw,evidence_class=MODE,expected_manifest_sha256=HISTORY_MANIFEST_SHA256)
assert (len(h.commands),len(h.states),len(h.selected_receipts),h.maximum_read_offset)==(6,7,9,149225)
assert h.source_sha256=='fba2a4278c4f1d9640c1c39f527fe3d5e7022ab50af4d353bc017bb31bbead89'
assert h.historical_input_ids_status=='UNRECORDED'
production_reads=list(reads)
for spec in specs:
 p=Path(spec['path'])
 with p.open('rb') as f:f.seek(spec['byte_offset']);value=f.read(spec['line_length_bytes'])
 assert hashlib.sha256(value).hexdigest()==spec['raw_line_sha256']
after=states();assert before==after
assert not any(n.split('.')[0] in forbidden_roots for n in sys.modules)
result={'status':'ACTUAL_BOUNDED_READER_ACCEPTED_NO_RUNTIME_OR_PREFLIGHT','repository':str(repo),'module_path':sys.modules[read_historical.__module__].__file__,'manifest_sha256':manifest_sha,'source_sha256':h.source_sha256,'historical_input_ids_status':h.historical_input_ids_status,'RNG_status':RNG_STATUS,'selected_receipts':len(h.selected_receipts),'saved_commands':len(h.commands),'public_states':len(h.states),'maximum_event_offset':h.maximum_read_offset,'production_reads':production_reads,'independent_post_read_count':len(reads)-len(production_reads),'original_file_states_before':before,'original_file_states_after':after,'runtime_modules_absent':True,'raw_payload_exported':False,'science_counters_added':0}
Path.open=base_open
with out.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in result.items() if k not in {'production_reads','original_file_states_before','original_file_states_after'}}))
