from pathlib import Path
import hashlib,importlib.abc,json,os,subprocess,sys
REPO=Path(sys.argv[1]);OUT=Path(sys.argv[2]);MANIFEST=Path('/home/lizening/research-notes/agent-logs/2026-10-26T110000Z__LUNA__si-s01-input-readiness__f1a52e8c/FIRST_SOURCE_EVENT_BINDINGS_V2.json')
sys.path[:0]=[str(REPO/'src')]
class NoRuntime(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0] in ('torch','transformers','peft','alfworld','textworld','pynvml') or fullname in ('self_improvement.si_s01.runtime','self_improvement.si_s01.engineering_runtime','self_improvement.si_s01.engineering_gate'):
   raise AssertionError('model-free reader attempted runtime import '+fullname)
sys.meta_path.insert(0,NoRuntime())
def forbidden(*args,**kwargs):raise AssertionError('model-free reader attempted process/runtime entry')
subprocess.Popen=forbidden;subprocess.run=forbidden;subprocess.check_output=forbidden;os.system=forbidden
raw=MANIFEST.read_bytes();assert hashlib.sha256(raw).hexdigest()=='c361ba0c9d9276eb7dc20c31d0428f51db3f1a9fdd7fccfa23db5edc4f64eb38'
m=json.loads(raw);allowed={Path(m['trajectory']['path']).resolve():[(0,m['trajectory']['line_length_bytes'])]}
for item in m['events']:allowed.setdefault(Path(item['path']).resolve(),[]).append((item['byte_offset'],item['byte_offset']+item['line_length_bytes']))
reads=[];original=Path.open
class Window:
 def __init__(self,stream,path):self.stream,self.path=stream,path
 def __enter__(self):return self
 def __exit__(self,*args):return self.stream.__exit__(*args)
 def seek(self,offset,whence=0):
  assert whence==0 and type(offset) is int and 0<=offset<=max(b for a,b in allowed[self.path]);return self.stream.seek(offset,whence)
 def read(self,length=-1):
  offset=self.stream.tell();assert type(length) is int and length>0
  assert any(a<=offset and offset+length<=b for a,b in allowed[self.path]) or (length==1 and any(offset==a-1 for a,b in allowed[self.path] if a>0)),(str(self.path),offset,length)
  result=self.stream.read(length);reads.append({'path':str(self.path),'byte_offset':offset,'requested_bytes':length,'returned_bytes':len(result),'sha256':hashlib.sha256(result).hexdigest()});return result
 def __getattr__(self,name):return getattr(self.stream,name)
def bounded_open(path,mode='r',*args,**kwargs):
 resolved=path.resolve()
 if resolved in allowed:
  assert mode=='rb','unbounded/text historical read forbidden';return Window(original(path,mode,*args,**kwargs),resolved)
 if '/artifacts/' in str(resolved):raise AssertionError('reader attempted an unapproved artifact '+str(resolved))
 return original(path,mode,*args,**kwargs)
Path.open=bounded_open
from self_improvement.si_s01.engineering_history import read_historical
from self_improvement.si_s01.engineering_contract import MODE,HISTORY_MANIFEST_SHA256,RNG_STATUS
h=read_historical(raw,evidence_class=MODE,expected_manifest_sha256=HISTORY_MANIFEST_SHA256)
assert len(h.states)==7 and len(h.commands)==6 and len(h.selected_receipts)==9
assert h.maximum_read_offset==149225 and h.source_sha256=='fba2a4278c4f1d9640c1c39f527fe3d5e7022ab50af4d353bc017bb31bbead89'
assert not any(k.split('.')[0] in ('torch','transformers','peft','alfworld','textworld','pynvml') for k in sys.modules)
value={'status':'ACTUAL_BOUNDED_HISTORICAL_READER_VALIDATED_NOT_PREFLIGHT_OR_RUNTIME','evidence_class':'original_frozen_historical_bytes','manifest_sha256':h.manifest_sha256,'source_sha256':h.source_sha256,'trajectory_bytes':35486,'selected_event_receipts':9,'states':7,'commands':6,'maximum_event_offset':h.maximum_read_offset,'historical_input_ids_status':h.historical_input_ids_status,'RNG_status':RNG_STATUS,'raw_reads':reads,'no_runtime_modules_imported':True,'no_process_or_runtime_entry':True,'model_generation_environment_operations_added':0,'payload_values_emitted':False}
with OUT.open('x') as f:json.dump(value,f,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in value.items() if k!='raw_reads'}))
