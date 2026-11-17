"""FICTIONAL random tiny Qwen3 + PEFT CPU demonstration; never a real trainer."""
import copy
import hashlib
import json
from pathlib import Path
import types

import torch
from transformers import Qwen3Config,Qwen3ForCausalLM
from peft import LoraConfig,PeftModel,get_peft_model,get_peft_model_state_dict

SOURCE=Path('/home/lizening/research-notes/agent-logs/20261118__CODEX__si-stateful-effect-ipc-v2__private/device_core.py')
FIXTURE=SOURCE.with_name('fixture.json')
SOURCE_SHA='c610f1cf57b5580e62245099f01d58cd4594de644e77478a714e686f335b0696'
FIXTURE_SHA='768fc562e2d32681d13fe8738c4a4804e7b3c0a191d26fd0a634b375102cb3d5'
TARGETS=['q_proj','k_proj','v_proj','o_proj','gate_proj','up_proj','down_proj']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def pinned(path,expected):
    raw=path.read_bytes()
    if sha(raw)!=expected:raise RuntimeError('fictional input/source drift')
    return raw
class FakeOwner:
    def __init__(self):self.pending=None;self.counts={}
    def reserve(self,kind,request):
        if self.pending is not None:raise RuntimeError('overlap')
        ticket=(kind,len(self.counts),sum(self.counts.values()));self.pending=ticket
        self.counts[kind]=self.counts.get(kind,0)+1;return ticket
    def returned(self,ticket,kind,receipt):
        if ticket!=self.pending or kind!=ticket[0]:raise RuntimeError('receipt mismatch')
        self.pending=None
    def unknown(self,ticket,kind,error):self.pending=None

def run_fictional(root):
    """Run only fake rows/random CPU model, using genuine existing injected core."""
    root=Path(root);root.mkdir(mode=0o700,parents=False,exist_ok=False)
    source=pinned(SOURCE,SOURCE_SHA);rows=json.loads(pinned(FIXTURE,FIXTURE_SHA))['rows']
    core=types.ModuleType('pinned_fictional_injected_core');exec(compile(source,str(SOURCE),'exec'),core.__dict__)
    torch.random.default_generator.manual_seed(42)
    cfg=Qwen3Config(vocab_size=16,hidden_size=32,intermediate_size=64,num_hidden_layers=1,
        num_attention_heads=4,num_key_value_heads=4,head_dim=8,max_position_embeddings=64,
        bos_token_id=1,eos_token_id=3,pad_token_id=4,tie_word_embeddings=False)
    cfg._attn_implementation='eager'
    base=Qwen3ForCausalLM(cfg).to('cpu');base_for_reload=copy.deepcopy(base)
    model=get_peft_model(base,LoraConfig(r=32,lora_alpha=64,lora_dropout=0.05,
                          target_modules=TARGETS,bias='none',task_type='CAUSAL_LM'))
    if any(p.device.type!='cpu' for p in model.parameters()):raise RuntimeError('not CPU')
    trainable={n:p for n,p in model.named_parameters() if p.requires_grad}
    if not trainable or any('lora_' not in n for n in trainable):raise RuntimeError('non-LoRA trainable')
    frozen={n:p.detach().clone() for n,p in model.named_parameters() if not p.requires_grad}
    before={n:p.detach().clone() for n,p in trainable.items()}
    optimizer=torch.optim.AdamW(list(trainable.values()),lr=3e-5,betas=(0.9,0.999),eps=1e-8,
        weight_decay=0.0,amsgrad=False,foreach=False,capturable=False,maximize=False,fused=False)
    owner=FakeOwner();adapter_path=root/'FICTIONAL_ADAPTER'
    def fake_checkpoint(m,opt,meta):
        if meta['optimizer_steps']!=16 or adapter_path.exists():raise RuntimeError('not final or target exists')
        m.save_pretrained(str(adapter_path),safe_serialization=True)
        return {'scope':'FICTIONAL_RANDOM_TINY_ONLY','optimizer_steps':16}
    result=core.run_injected_core(model=model,optimizer=optimizer,rows=rows,owner=owner,
        checkpoint_writer=fake_checkpoint,vocab_size=16,eos_token_id=3,pad_token_id=4)
    if owner.pending is not None:raise RuntimeError('unfinished fake effect')
    if any(not torch.equal(p,before[n]) for n,p in trainable.items()) is False:
        raise RuntimeError('no LoRA tensor changed')
    if any(not torch.equal(p,frozen[n]) for n,p in model.named_parameters() if not p.requires_grad):
        raise RuntimeError('frozen tensor drift')
    model.eval();tokens=torch.tensor([[0,1,2,3]],dtype=torch.long,device='cpu')
    with torch.no_grad():original_logits=model(input_ids=tokens,use_cache=False).logits.detach()
    reloaded=PeftModel.from_pretrained(base_for_reload,str(adapter_path),is_trainable=False,local_files_only=True).to('cpu')
    reloaded.eval()
    with torch.no_grad():reloaded_logits=reloaded(input_ids=tokens,use_cache=False).logits.detach()
    original_state=get_peft_model_state_dict(model);reloaded_state=get_peft_model_state_dict(reloaded)
    if set(original_state)!=set(reloaded_state) or any(not torch.equal(original_state[k],reloaded_state[k]) for k in original_state):
        raise RuntimeError('fake adapter tensor mismatch')
    torch.testing.assert_close(original_logits,reloaded_logits,rtol=1e-6,atol=1e-6)
    files={p.name:sha(p.read_bytes()) for p in sorted(adapter_path.iterdir()) if p.is_file()}
    evidence={'scope':'FICTIONAL_RANDOM_TINY_CPU_NOT_QWEN3_8B_NOT_SCIENCE','source_sha256':SOURCE_SHA,
        'fixture_sha256':FIXTURE_SHA,'tiny_config':{'vocab_size':16,'hidden_size':32,'layers':1,'head_dim':8},
        'lora':{'r':32,'alpha':64,'dropout':0.05,'target_modules':TARGETS},
        'fake_owner_counts':owner.counts,'core_metadata':result['metadata'],
        'fake_adapter_files_sha256':files,'fake_adapter_tensor_count':len(original_state),
        'fake_base_unchanged':True,'fake_lora_changed':True,'adapter_tensor_exact':True,
        'fake_logits_max_absolute_difference':float((original_logits-reloaded_logits).abs().max().item()),
        'device':'cpu','scientific_use':'HOLD'}
    (root/'FICTIONAL_EVIDENCE.json').write_text(json.dumps(evidence,sort_keys=True,indent=2)+'\n')
    return evidence

if __name__=='__main__':
    import sys
    print(json.dumps(run_fictional(sys.argv[1]),sort_keys=True))
