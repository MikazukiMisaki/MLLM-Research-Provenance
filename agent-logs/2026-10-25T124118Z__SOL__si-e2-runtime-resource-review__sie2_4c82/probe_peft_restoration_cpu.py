"""Observe installed PEFT disable-context behavior on a tiny CPU model only."""
import os
os.environ['CUDA_VISIBLE_DEVICES']=''
import json
import torch
from peft import LoraConfig, get_peft_model
from transformers import GPT2Config, GPT2LMHeadModel

model=get_peft_model(GPT2LMHeadModel(GPT2Config(n_layer=1,n_head=1,n_embd=8,n_positions=8,vocab_size=16)),
                     LoraConfig(r=2,target_modules=['c_attn'],lora_alpha=4))
for p in model.parameters(): p.requires_grad_(False)
def state():
    s=model.get_model_status()
    return {'enabled':s.enabled,'active_adapters':s.active_adapters,'trainable_params':s.trainable_params,
            'all_cpu':all(str(p.device)=='cpu' for p in model.parameters())}
before=state()
with model.disable_adapter(): during=state()
after=state()
print(json.dumps({'evidence_class':'CPU_TOY_INSTALLED_PEFT_BEHAVIOR_NO_8B_LOAD_NO_GENERATION',
                  'before':before,'inside_disable_context':during,'after_default_context':after,
                  'parameters':sum(p.numel() for p in model.parameters()),
                  'optimizer_steps':0,'generations':0}))
