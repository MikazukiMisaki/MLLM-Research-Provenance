"""Fiction-only socket client for exact, unmodified EffectOwner/Journal."""
import hashlib,json,os,sys,types
from pathlib import Path
import torch
import torch.nn.functional as F
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import device_core
EFFECT=Path('/home/lizening/research-notes/agent-logs/20261115__CODEX__multi-source-training-r4__candidate/effect_ipc.py')
raw=EFFECT.read_bytes()
if hashlib.sha256(raw).hexdigest()!='046c0c48291efdae06457d87343d084357ae5a1774c3d670e3e232b15fd16dd8':raise RuntimeError('frozen effect source mismatch')
ipc=types.ModuleType('effect_ipc_bound');exec(compile(raw,str(EFFECT),'exec'),ipc.__dict__)
fixture=(HERE/'fixture.json').read_bytes()
if hashlib.sha256(fixture).hexdigest()!='768fc562e2d32681d13fe8738c4a4804e7b3c0a191d26fd0a634b375102cb3d5':raise RuntimeError('fictional fixture mismatch')
rows=json.loads(fixture)['rows'];fd=int(sys.argv[1]);out=Path(sys.argv[2]);mode=sys.argv[3]
CAPS={'validate_model':1,'set_train_mode':1,'zero_grad':16,'forward':64,'backward':64,'optimizer_step':16,'checkpoint_final':1}
journal=ipc.Journal(out/'worker_events.jsonl',16*1024*1024);under=ipc.EffectOwner(fd,journal,CAPS)
class Adapter:
 def reserve(self,kind,request):return under.start(kind,request)
 def returned(self,ticket,kind,receipt):
  if mode=='interrupt_after_first_step' and kind=='optimizer_step':os._exit(23)
  return under.returned(ticket,kind,receipt)
 def unknown(self,ticket,kind,error_type):return under.unknown(ticket,kind)
class FakeModel(torch.nn.Module):
 def __init__(self):super().__init__();self.weight=torch.nn.Parameter(torch.zeros((5,5),dtype=torch.float32))
 def forward(self,*,input_ids,attention_mask,use_cache):return types.SimpleNamespace(logits=F.one_hot(input_ids,num_classes=5).to(torch.float32) @ self.weight)
model=FakeModel();optimizer=torch.optim.AdamW(model.parameters(),lr=3e-5,betas=(0.9,0.999),eps=1e-8,weight_decay=0.0,amsgrad=False,foreach=False,capturable=False,maximize=False,fused=False)
try:
 result=device_core.run_injected_core(model=model,optimizer=optimizer,rows=rows,owner=Adapter(),
  checkpoint_writer=lambda m,o,meta:{'scope':'FICTIONAL_NO_CHECKPOINT','step':int(o.state[m.weight]['step'].item())},
  vocab_size=5,eos_token_id=3,pad_token_id=4)
 journal.emit('fake_run_result',{'scope':'FICTIONAL_CHILD_CLAIM','metadata':result['metadata']})
 under.finish('COMPLETED')
finally:
 under.close();journal.close()
