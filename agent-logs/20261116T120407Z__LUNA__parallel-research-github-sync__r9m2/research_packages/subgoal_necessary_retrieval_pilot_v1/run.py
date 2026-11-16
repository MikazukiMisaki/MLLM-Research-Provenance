#!/usr/bin/env python3
"""One-shot fictional handoff pilot; acquire shared GPU through project coordination first."""
import hashlib
import json
import os
import re
import resource
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CASE_SHA = '0b4fe41d9378def250ade4e1e71049878e9e34643108108034c28d2728ccdc6f'
OUTPUT = ROOT / 'artifacts/runtime/parallel-research/necessary-retrieval-pilot-v1'

def sample():
    result = subprocess.run(['nvidia-smi','--query-gpu=uuid,memory.used,utilization.gpu',
                             '--format=csv,noheader,nounits'], check=True, text=True, capture_output=True, timeout=10)
    lines=result.stdout.strip().splitlines()
    if not lines: raise RuntimeError('GPU sampling returned no devices')
    uuid, used, utilization = [v.strip() for v in lines[0].split(',')]
    return uuid, int(used), int(utilization)

def main():
    if sys.argv[1:] != ['--run-once']:
        raise SystemExit('requires --run-once after shared GPU coordination')
    raw=(HERE/'cases.json').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=CASE_SHA: raise ValueError('case digest changed')
    cases=json.loads(raw)
    if len(cases)!=8: raise ValueError('expected eight cases')
    OUTPUT.mkdir(mode=0o700,parents=False,exist_ok=False)
    started=time.monotonic()
    with (OUTPUT/'events.jsonl').open('x',encoding='utf-8') as f:
        def emit(event, **kwargs):
            f.write(json.dumps({'event':event,'elapsed_seconds':round(time.monotonic()-started,6),**kwargs},ensure_ascii=False,sort_keys=True,allow_nan=False)+'\n'); f.flush(); os.fsync(f.fileno())
        try:
            resource.setrlimit(resource.RLIMIT_CPU,(1800,1800));resource.setrlimit(resource.RLIMIT_FSIZE,(16*1024*1024,16*1024*1024))
            uuid, used, utilization=sample()
            emit('gpu_sample',when='before_load',uuid=uuid,used_mib=used,utilization=utilization)
            if used>=43008 or utilization>=5: raise RuntimeError('GPU admission limit')
            os.environ.update(CUDA_VISIBLE_DEVICES=uuid,HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',TOKENIZERS_PARALLELISM='false')
            config=json.loads((ROOT/'configs/local/parallel_research_pilot.json').read_text())
            model_path=config['model_path']
            if not os.path.isabs(model_path): raise ValueError('model path must be absolute')
            import torch, transformers
            from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
            emit('loading_start',cases_sha256=CASE_SHA,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),torch_version=str(torch.__version__),transformers_version=transformers.__version__)
            tokenizer=AutoTokenizer.from_pretrained(model_path,local_files_only=True,trust_remote_code=False)
            model=AutoModelForCausalLM.from_pretrained(model_path,local_files_only=True,trust_remote_code=False,torch_dtype=torch.bfloat16).to('cuda:0')
            model.eval()
            eos=model.generation_config.eos_token_id;eos=[eos] if isinstance(eos,int) else list(eos or [])
            if not eos or any(type(v) is not int or v<0 for v in eos): raise ValueError('invalid EOS')
            pad=tokenizer.pad_token_id if tokenizer.pad_token_id is not None else eos[0]
            generation=GenerationConfig(do_sample=False,num_beams=1,max_new_tokens=16,eos_token_id=eos,pad_token_id=pad,use_cache=True)
            identity,used,utilization=sample()
            emit('gpu_sample',when='after_load',uuid=identity,used_mib=used,utilization=utilization)
            if identity!=uuid or used>=43008: raise RuntimeError('GPU identity or memory limit')
            template=tokenizer.chat_template
            if not isinstance(template,str) or not template: raise ValueError('missing chat template')
            emit('loading_complete',model_type=model.config.model_type,tokenizer_class=type(tokenizer).__name__,chat_template_sha256=hashlib.sha256(template.encode()).hexdigest(),eos_ids=eos,generation_config=generation.to_dict())
            count=0
            for index,case in enumerate(cases):
                order=('compatible','conflicting') if index%2==0 else ('conflicting','compatible')
                for condition in order:
                    key=case['case_id']+'-'+condition
                    identity,used,utilization=sample()
                    emit('gpu_sample',when='before_'+key,uuid=identity,used_mib=used,utilization=utilization)
                    if identity!=uuid or used>=43008: raise RuntimeError('GPU identity or memory limit')
                    prompt=case['prompts'][condition]
                    rendered=tokenizer.apply_chat_template([{'role':'user','content':prompt}],tokenize=False,add_generation_prompt=True,enable_thinking=False)
                    inputs=tokenizer(rendered,return_tensors='pt',add_special_tokens=False,truncation=False)
                    ids=inputs['input_ids'][0].tolist()
                    if not ids or len(ids)>1024: raise ValueError('input token limit')
                    input_sha=hashlib.sha256(json.dumps(ids,separators=(',',':')).encode()).hexdigest()
                    inputs={k:v.to('cuda:0') for k,v in inputs.items()}
                    emit('prepared',call_id=key,case_id=case['case_id'],family=case['family'],condition=condition,prompt=prompt,rendered_prompt=rendered,input_token_ids=ids,input_token_sha256=input_sha,mapping=case['mapping'])
                    t=time.monotonic();emit('call_start',call_id=key)
                    with torch.inference_mode():
                        output=model.generate(**inputs,generation_config=generation,use_model_defaults=False)[0].tolist()
                    duration=time.monotonic()-t
                    if output[:len(ids)]!=ids: raise ValueError('input prefix mismatch')
                    suffix=output[len(ids):]
                    emit('raw_result',call_id=key,output_token_ids=suffix,seconds=round(duration,6))
                    if not suffix or len(suffix)>16: raise ValueError('invalid generated length')
                    positions=[i for i,x in enumerate(suffix) if x in eos]
                    if positions==[len(suffix)-1]:
                        decoded=tokenizer.decode(suffix[:-1],skip_special_tokens=True,clean_up_tokenization_spaces=False).strip()
                        action=case['mapping'].get(decoded) if re.fullmatch(r'A[0-9]{3}',decoded) else None
                        category='format_invalid' if action is None else 'goal_consistent' if action==case['goal_consistent_action'] else 'conflicting' if action==case['conflicting_action'] else 'other'
                    elif not positions and len(suffix)==16:
                        decoded=None;action=None;category='truncated'
                    else: raise ValueError('unconfirmed termination')
                    emit('decision',call_id=key,case_id=case['case_id'],family=case['family'],condition=condition,decoded=decoded,action=action,category=category)
                    count+=1
                    identity,used,utilization=sample();emit('gpu_sample',when='after_'+key,uuid=identity,used_mib=used,utilization=utilization)
                    if identity!=uuid or used>=43008 or duration>=120: raise RuntimeError('resource or request limit')
            emit('complete',call_count=count,user_cpu_seconds=resource.getrusage(resource.RUSAGE_SELF).ru_utime,system_cpu_seconds=resource.getrusage(resource.RUSAGE_SELF).ru_stime)
            return 0
        except Exception as e:
            emit('stopped',error_type=type(e).__name__,message=str(e) if type(e).__name__ in ('RuntimeError','ValueError') else 'details omitted')
            return 1

if __name__=='__main__':
    raise SystemExit(main())
