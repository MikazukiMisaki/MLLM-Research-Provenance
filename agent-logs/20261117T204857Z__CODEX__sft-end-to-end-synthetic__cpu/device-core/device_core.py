"""Research-only injected stateful update; external effects and identity untrusted.

No model loader, environment, dispatch or CUDA-specific calls. This Python API
is NOT a security sandbox and is not a scientific execution authorization.
"""
class Stop(ValueError):pass

def need(condition,message):
 if not condition:raise Stop(message)

def _validate_rows(rows,*,vocab_size,eos_token_id,pad_token_id):
 need(type(rows) is list and len(rows)==16,'exactly 16 rows')
 need(type(vocab_size) is int and vocab_size>1 and type(eos_token_id) is int and type(pad_token_id) is int and
      0<=eos_token_id<vocab_size and 0<=pad_token_id<vocab_size and eos_token_id!=pad_token_id,'EOS/pad/vocabulary')
 seen=set()
 for row in rows:
  need(type(row) is dict and set(row)=={'row_id','input_ids','loss_mask','prompt_length'},'row shape')
  name=row['row_id'];ids=row['input_ids'];mask=row['loss_mask'];p=row['prompt_length']
  need(type(name) is str and bool(name) and name not in seen,'row identity');seen.add(name)
  need(type(ids) is list and 1<len(ids)<=4096 and all(type(x) is int and 0<=x<vocab_size for x in ids),'token bounds')
  need(type(p) is int and 1<=p<len(ids) and len(ids)-p<=16,'completion length')
  need(type(mask) is list and all(type(x) is int for x in mask) and mask==[0]*p+[1]*(len(ids)-p),'completion mask')
  target=ids[p:];need(target[-1]==eos_token_id and eos_token_id not in target[:-1] and pad_token_id not in target,'EOS/pad')
 return rows

def _effect(owner,kind,request,callback,summarize=lambda _:{'returned':True}):
 """No internal retries; owner is injected and not independently authenticated."""
 ticket=owner.reserve(kind,request)
 if ticket is None:raise Stop('missing effect reservation')
 try:
  value=callback();owner.returned(ticket,kind,summarize(value));return value
 except BaseException as error:
  try:owner.unknown(ticket,kind,type(error).__name__)
  except BaseException:pass
  raise

def run_injected_core(*,model,optimizer,rows,owner,checkpoint_writer,vocab_size,eos_token_id,pad_token_id):
 """Four epochs / 64 micros / 16 steps; callable directly, NOT a sandbox.

 Owner must supply reserve(kind,request), returned(ticket,kind,receipt), and
 unknown(ticket,kind,error_type). Model, optimizer, rows and callback are
 externally supplied; prior identity, budget, device and data claims are unverified.
 """
 _validate_rows(rows,vocab_size=vocab_size,eos_token_id=eos_token_id,pad_token_id=pad_token_id)
 need(callable(checkpoint_writer),'checkpoint callback')
 import torch
 import torch.nn.functional as F
 params=[p for p in model.parameters() if p.requires_grad]
 need(params and all(p.is_floating_point() for p in params),'trainable parameters')
 allparams=list(model.parameters());device=params[0].device
 need(all(p.device==device for p in allparams),'single model device')
 need(type(optimizer) is torch.optim.AdamW and len(optimizer.state)==0,'fresh AdamW required')
 optparams=[p for g in optimizer.param_groups for p in g['params']]
 need(len(optparams)==len(params) and len({id(p) for p in optparams})==len(params) and {id(p) for p in optparams}=={id(p) for p in params},'optimizer parameter binding')
 for g in optimizer.param_groups:
  need(g['lr']==3e-5 and g['weight_decay']==0.0 and g['betas']==(0.9,0.999) and g['eps']==1e-8 and
       g['amsgrad'] is False and g['foreach'] is False and g['capturable'] is False and g['maximize'] is False and g['fused'] is False,'optimizer configuration')
 model_id=id(model);optimizer_id=id(optimizer);param_ids=tuple(id(p) for p in params)
 def validate_trainable():
  need(all(bool(torch.isfinite(p).all().item()) for p in params),'nonfinite trainable parameter')
 _effect(owner,'validate_model',{'scope':'trainable_only'},validate_trainable)
 _effect(owner,'set_train_mode',{'value':True},lambda:model.train(True))
 history=[];micro=0
 for epoch in range(4):
  for start in range(0,16,4):
   batch=rows[start:start+4];active=sum(sum(r['loss_mask'][1:]) for r in batch)
   need(len(batch)==4 and active>0,'zero target count')
   _effect(owner,'zero_grad',{'epoch':epoch,'batch_start':start},lambda:optimizer.zero_grad(set_to_none=True))
   for row in batch:
    def forward(row=row):
     ids=row['input_ids'];labels=[token if flag else -100 for token,flag in zip(ids,row['loss_mask'])]
     x=torch.tensor([ids],dtype=torch.long,device=device);y=torch.tensor([labels],dtype=torch.long,device=device)
     logits=model(input_ids=x,attention_mask=torch.ones_like(x),use_cache=False).logits
     need(tuple(logits.shape)==(1,len(ids),vocab_size) and logits.device==device,'logits shape or device')
     loss=F.cross_entropy(logits[:,:-1,:].float().reshape(-1,vocab_size),y[:,1:].reshape(-1),ignore_index=-100,reduction='sum')
     need(bool(torch.isfinite(loss).item()),'nonfinite loss');return loss
    loss=_effect(owner,'forward',{'row_id':row['row_id'],'active_total':active},forward,
                 lambda v:{'loss_sum':float(v.detach().item())})
    def backward(loss=loss):
     (loss/active).backward()
     need(all(p.grad is not None and bool(torch.isfinite(p.grad).all().item()) for p in params),'nonfinite or absent gradient')
    _effect(owner,'backward',{'row_id':row['row_id'],'active_total':active},backward);micro+=1
   def step():
    optimizer.step()
    for p in params:
     state=optimizer.state[p]
     need(bool(torch.isfinite(p).all().item()) and all(not torch.is_tensor(v) or bool(torch.isfinite(v).all().item()) for v in state.values()),'nonfinite trainable or optimizer state')
     need(int(state['step'].item())==len(history)+1,'optimizer step sequence')
    need(id(model)==model_id and id(optimizer)==optimizer_id and tuple(id(p) for p in model.parameters() if p.requires_grad)==param_ids,'identity changed')
   _effect(owner,'optimizer_step',{'epoch':epoch,'batch_start':start},step)
   history.append({'epoch':epoch,'batch_start':start,'row_ids':[r['row_id'] for r in batch],
                   'active_target_count':active,'optimizer_step':len(history)+1})
 need(micro==64 and len(history)==16,'incomplete updates')
 meta={'selection':'FINAL_ONLY_NO_BEST','epochs':4,'microbatches':micro,'optimizer_steps':16}
 receipt=_effect(owner,'checkpoint_final',dict(meta),lambda:checkpoint_writer(model,optimizer,dict(meta)))
 return {'status':'INJECTED_RESEARCH_CORE_RETURNED_NOT_SCIENTIFIC','history':history,'metadata':meta,'checkpoint_receipt':receipt}

def dispatch_real(*_args,**_kwargs):
 raise RuntimeError('RESEARCH_HOLD: actual model, data, owner, budget and checkpoint are not authorized')
