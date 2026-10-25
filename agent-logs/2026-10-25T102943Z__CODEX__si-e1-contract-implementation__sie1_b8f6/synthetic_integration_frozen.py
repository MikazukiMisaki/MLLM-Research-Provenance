from pathlib import Path
import json,subprocess
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
from si_p3_support import collect_synthetic,synthetic_background
from self_improvement.si_p3.audit import audit_run
from self_improvement.si_p3.data import build_pool,adopt_once,paired_slots,CompletionCollator,audit_exposure
folder=OWN/'synthetic_integration_frozen'
assert not folder.exists()
root=Path('/home/lizening/wt-si-p3-engineering-contracts')
head=subprocess.run(['git','rev-parse','HEAD'],cwd=root,capture_output=True,text=True)
assert head.returncode==0 and head.stdout.strip()=='a995d4c3c5f7d31a2cf1fd0afc4bfa4bd72ee3a3'
status=subprocess.run(['git','status','--porcelain'],cwd=root,capture_output=True,text=True)
assert status.returncode==0 and not status.stdout
run,events,tokenizer,raw,envs=collect_synthetic(folder)
print(json.dumps({'collector_status':run['status'],'first_slot_disposition':run['slots'][0]['disposition']}),flush=True)
integrity=audit_run(run,events,tokenizer)
pool=build_pool(run,events,tokenizer)
adopt=adopt_once(pool)
background,_,_,_=synthetic_background(folder,tokenizer)
pairs=paired_slots(adopt,background)
exposure=audit_exposure(pairs,CompletionCollator(tokenizer.pad_token_id))
for name,value in [('integrity',integrity),('quality',pool.dispositions),('adoption',adopt.audit),('exposure',exposure),('encoded_paired_slots',[[b.to_dict(),c.to_dict()] for b,c in pairs])]:
 (folder/(name+'.json')).write_text(json.dumps(value,indent=2)+'\n')
print(json.dumps({'evidence':'SYNTHETIC_SOFTWARE_ONLY','scientific_calls':0,'integrity':{k:v for k,v in integrity.items() if k!='logical_prefix_comparisons'},'adoption':adopt.audit,'microbatches':len(exposure['microbatch_loss_tokens']),'updates':exposure['optimizer_updates'],'prompt_ratios':exposure['prompt_ratios'],'raw_fake_calls':len(raw.calls),'fake_env_resets':sum(e.resets for e in envs)}),flush=True)

(folder/'software_invocation_context.json').write_text(json.dumps({'frozen_sha':head.stdout.strip(),'git_head_returncode':head.returncode,'git_porcelain_returncode':status.returncode,'git_porcelain':status.stdout,'scientific_execution_authorized':False,'evidence_class':'synthetic'},indent=2)+'\n')
