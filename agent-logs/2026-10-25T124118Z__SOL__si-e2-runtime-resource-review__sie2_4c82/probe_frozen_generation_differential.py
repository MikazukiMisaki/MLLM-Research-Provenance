"""Real cached tokenizer/tiny CPU PEFT; synthetic generate edge, frozen helper comparison."""
import os
os.environ['CUDA_VISIBLE_DEVICES']=''
os.environ['HF_HUB_OFFLINE']='1'
os.environ['TRANSFORMERS_OFFLINE']='1'
from pathlib import Path
import json
import sys
from types import SimpleNamespace
import subprocess

OWN=Path(__file__).resolve().parent
assert OWN.name=='2026-10-25T124118Z__SOL__si-e2-runtime-resource-review__sie2_4c82'
checkout=Path(sys.argv[1]).resolve()
sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=checkout,text=True).strip()
sys.path[:0]=[str(checkout/'src'),str(checkout/'scripts')]
import torch
from transformers import AutoTokenizer,GPT2Config,GPT2LMHeadModel
from peft import LoraConfig,get_peft_model
import run_r19_experiment as frozen
from self_improvement.si_p3.runtime_backend import LocalInference
from self_improvement.si_p3.runtime_gate import Permit,PHASES,MAXIMA,engineering_prompts
from self_improvement.si_p3.runtime_ledger import EngineeringLedger

snapshot='/home/lizening/.cache/huggingface/hub/models--Qwen--Qwen3-8B/snapshots/b968826d9c46dd6066d109eabc6255188de91218'
tok=AutoTokenizer.from_pretrained(snapshot,local_files_only=True,trust_remote_code=False)
short=tok.encode('A000',add_special_tokens=False)+[tok.eos_token_id]
fill=tok.encode('A',add_special_tokens=False)[0]
fixtures=OWN/'independent_probe_fixtures'
fixtures.mkdir(exist_ok=False)
summary=[]
for case in ('short_EOS','cap_no_EOS','EOS_at_cap'):
    out=fixtures/case;out.mkdir()
    auth={'purpose':'ENGINEERING_DIAGNOSTIC_ONLY','source_sha':sha,'science_authorized':False,
          'output_path':str(out),'ceilings':dict(MAXIMA),'software_fixture_explicit':True}
    permit=Permit(auth,{},'EXPLICIT_SOFTWARE_FIXTURE','EXPLICIT_SOFTWARE_FIXTURE',checkout)
    ledger=EngineeringLedger(out/'software_events.jsonl',permit)
    model=get_peft_model(GPT2LMHeadModel(GPT2Config(n_layer=1,n_head=1,n_embd=8,n_positions=8,vocab_size=16)),
                        LoraConfig(r=2,target_modules=['c_attn'],lora_alpha=4))
    for p in model.parameters():p.requires_grad_(False)
    actual_inputs=[]
    def edge(**kwargs):
        assert kwargs['do_sample'] is False and kwargs['return_dict_in_generate'] is True and kwargs['output_scores'] is True
        cap=kwargs['max_new_tokens']
        ids=short if case=='short_EOS' else [fill]*cap if case=='cap_no_EOS' else [fill]*(cap-1)+[tok.eos_token_id]
        actual_inputs.append({'input_ids':kwargs['input_ids'][0].tolist(),
                              'attention_mask':kwargs['attention_mask'][0].tolist()})
        return SimpleNamespace(sequences=torch.cat((kwargs['input_ids'],torch.tensor([ids])),dim=1),
                               scores=tuple(torch.zeros(1,1) for _ in ids))
    model.generate=edge
    real=LocalInference(tok,model,torch,ledger,lambda:{'evidence_class':'synthetic_software_edge'},software_fixture=True)
    backend=SimpleNamespace(_load=lambda:(tok,model,torch))
    for phase,cap,mode in PHASES:
        prompt=engineering_prompts()[phase]
        prepared=real.prepare(prompt)
        new=dict(real.generate(phase,prepared,cap,mode).raw)
        if mode=='BASE':
            with model.disable_adapter():old=frozen._generate_exact(backend,prompt,cap)
            for p in model.parameters():p.requires_grad_(False)
        else:old=frozen._generate_exact(backend,prompt,cap)
        assert actual_inputs[-1]==actual_inputs[-2]
        new.pop('adapter_mode');new.pop('adapter_sha256')
        new.pop('latency_seconds');old.pop('latency_seconds')
        assert new==old,(case,phase,set(new)^set(old))
        summary.append({'case':case,'phase':phase,'frozen_raw_field_equality':'PASS_EXCEPT_LATENCY_AND_ADDED_MODE_ATTESTATION',
                        'same_full_actual_input_ids_and_attention_mask':True,
                        'generated_tokens':new['generated_tokens'],'output_complete':new['output_complete'],
                        'token_cap_reached':new['token_cap_reached']})
    ledger.close()
assert not torch.cuda.is_initialized()
result={'schema':'SI_E2_ROOT_FROZEN_RAW_GENERATION_DIFFERENTIAL_V1','source_sha':sha,
        'cases':summary,'real_cached_tokenizer':snapshot,'tiny_CPU_PEFT_models':3,
        'synthetic_generation_edge_calls':24,'real_8B_generations':0,'real_model_loads':0,'environment_calls':0,
        'optimizer_steps':0,'torch_cuda_initialized':False,
        'raw_fixture_location':str(fixtures),'raw_fixture_publication':'LOCAL_ONLY; compact comparison is published'}
with (OWN/'independent_frozen_generation_differential.json').open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
print(json.dumps({'source_sha':sha,'comparisons_passed':len(summary),'torch_cuda_initialized':False}))
