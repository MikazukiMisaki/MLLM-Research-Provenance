from pathlib import Path
import hashlib,json
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
CACHE=Path('/home/lizening/.cache/huggingface/hub/models--Qwen--Qwen3-8B/snapshots/b968826d9c46dd6066d109eabc6255188de91218')
EXPECTED={'tokenizer.json':'aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4','tokenizer_config.json':'d5d09f07b48c3086c508b30d1c9114bd1189145b74e982a265350c923acd8101','vocab.json':'ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910','merges.txt':'8831e4f1a044471340f7c0a83d7bd71306a5b867e95fd870f74d0c5308a904d5'}
def bindings():
 out=[]
 for name,expected in EXPECTED.items():
  p=CACHE/name;sha=hashlib.sha256(p.read_bytes()).hexdigest();assert sha==expected
  out.append({'path':str(p),'sha256':sha,'bytes':p.stat().st_size})
 return out
before=bindings()
from transformers import AutoTokenizer
from self_improvement.si_p3.contract import PublicState,projection
from self_improvement.si_p3.data import encode_example,CompletionCollator
base=AutoTokenizer.from_pretrained(str(CACHE),local_files_only=True,trust_remote_code=False)
base.pad_token=base.eos_token
class CountTokenizer:
 def __init__(self,tokenizer):self.inner=tokenizer;self.calls={'text_encoding':0,'chat_render':0,'decode':0}
 def __getattr__(self,name):return getattr(self.inner,name)
 def __call__(self,*args,**kwargs):self.calls['text_encoding']+=1;return self.inner(*args,**kwargs)
 def apply_chat_template(self,*args,**kwargs):self.calls['chat_render']+=1;return self.inner.apply_chat_template(*args,**kwargs)
 def decode(self,*args,**kwargs):self.calls['decode']+=1;return self.inner.decode(*args,**kwargs)
tok=CountTokenizer(base)
examples=[]
for i,target in enumerate(('A000','A001','A010','A099')):
 state=PublicState(f'pick_and_place_simple-software-{i}/trial-{i}','pick_and_place_simple',f'Complete synthetic public task {i}.',f'Synthetic current observation {i}.',tuple(f'command {j}' for j in range(100)))
 view=projection(state,[])
 ex=encode_example(tok,task_id=state.task_id,family=state.family,public_prompt=view['public_prompt'],completion=target,command=state.valid_actions[int(target[1:])],origin='new')
 examples.append(ex)
 assert tok.decode(ex.input_ids[ex.prompt_tokens:],skip_special_tokens=False)==target+tok.eos_token
batch=CompletionCollator(tok.pad_token_id)(examples)
assert int((batch['labels'][:,1:]!=-100).sum())==sum(x.loss_tokens for x in examples)
assert all(batch['labels'][i,len(ex.input_ids)-1].item()==tok.eos_token_id for i,ex in enumerate(examples))
# Oversized full maps must be rejected intact; never truncated to fake fit.
state=PublicState('pick_and_place_simple-software-long/trial-0','pick_and_place_simple','Synthetic long public goal','Synthetic observation',tuple('synthetic household admissible command number '+str(j) for j in range(1000)))
try:
 encode_example(tok,task_id=state.task_id,family=state.family,public_prompt=projection(state,[])['public_prompt'],completion='A000',command=state.valid_actions[0],origin='new')
except ValueError as e:
 assert 'exceeds frozen max_length' in str(e)
 oversized_rejected=True
else:raise AssertionError('oversized map was truncated or accepted')
after=bindings();assert before==after
result={'scope':'CACHED_TOKENIZER_TEXT_ONLY_SYNTHETIC_PUBLIC_INPUTS','scientific_model_generations':0,'real_model_or_env_constructed':False,'actual_new_task_bodies_read':0,'actual_P0_training_or_full_new_data_readiness':False,'before':before,'after':after,'tokenizer_class':type(base).__name__,'chat_template_sha256':hashlib.sha256(base.chat_template.encode()).hexdigest(),'tokenizer_activity':tok.calls,'EOS_equals_PAD':tok.eos_token_id==tok.pad_token_id,'examples':[{'target':x.completion,'whole_sequence_tokens':len(x.input_ids),'prompt_tokens':x.prompt_tokens,'actual_shifted_loss_tokens':x.loss_tokens,'completion_ids_with_EOS':list(x.input_ids[x.prompt_tokens:])} for x in examples],'actual_microbatch_shifted_tokens':int((batch['labels'][:,1:]!=-100).sum()),'oversized_full_map_rejected_without_truncation':oversized_rejected}
(OWN/'cached_tokenizer_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
