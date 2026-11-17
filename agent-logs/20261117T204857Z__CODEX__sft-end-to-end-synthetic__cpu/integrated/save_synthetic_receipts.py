"""Save exactly two fictional CPU scenarios under a new output root."""
import hashlib,json,os
from pathlib import Path
import parent_bridge
root=Path(__file__).resolve().parent/'synthetic_evidence';root.mkdir(mode=0o700,exist_ok=False)
summary={}
for scenario in ('normal','interrupt_after_checkpoint'):
 os.environ['FAKE_CHECKPOINT_SCENARIO']=scenario
 out=root/scenario;r=parent_bridge.run_fake(out,'normal')
 weight=out/'fake_final'/'fictional.safetensors';stored=json.loads((out/'fake_final'/'receipt.json').read_text())
 digest=hashlib.sha256(weight.read_bytes()).hexdigest()
 if digest!=stored['sha256']:raise RuntimeError('fake artifact digest')
 summary[scenario]={'result':r,'artifact_sha256':digest,'disk_receipt':stored}
 print(scenario,'outcome',r['outcome'],'rc',r['returncode'],'artifact_sha256',digest,flush=True)
(root/'summary.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n')
if summary['normal']['result']['outcome']!='FICTIONAL_COMPLETE' or summary['interrupt_after_checkpoint']['result']['returncode']!=24 or summary['interrupt_after_checkpoint']['result']['outcome']!='UNKNOWN':raise SystemExit(1)
