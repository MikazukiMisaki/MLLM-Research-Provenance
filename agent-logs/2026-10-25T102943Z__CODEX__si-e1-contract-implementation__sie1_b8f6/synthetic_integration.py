from pathlib import Path
import json
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
from si_p3_support import collect_synthetic,synthetic_background
from self_improvement.si_p3.audit import audit_run
from self_improvement.si_p3.data import build_pool,adopt_once,paired_slots,CompletionCollator,audit_exposure
folder=OWN/'synthetic_integration_v1'
assert not folder.exists()
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
print(json.dumps({'evidence':'SYNTHETIC_SOFTWARE_ONLY','scientific_calls':0,'integrity':integrity,'adoption':adopt.audit,'microbatches':len(exposure['microbatch_loss_tokens']),'updates':exposure['optimizer_updates'],'prompt_ratios':exposure['prompt_ratios'],'raw_fake_calls':len(raw.calls),'fake_env_resets':sum(e.resets for e in envs)}),flush=True)
