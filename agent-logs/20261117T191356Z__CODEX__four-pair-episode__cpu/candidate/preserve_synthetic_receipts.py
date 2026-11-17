"""Persist only fictional fixtures and their unchanged raw journals."""
import json
from pathlib import Path
import global_owner
import scheduler_synthetic
from test_episode_scheduler import fixture
base=Path(__file__).parent/'synthetic_evidence'
base.mkdir(mode=0o700,exist_ok=False)
summary={}
for name in ('success','second_arm_reset_mismatch'):
    root=base/name;root.mkdir(mode=0o700)
    inputs,setup,verify=fixture(root)
    try:
        scheduler_synthetic.run_fixture(root/'run',root,inputs,setup,verify,mode_by_case={global_owner.SCHEDULE[0][0]:'mismatch'} if name!='success' else None)
        outcome='COMPLETED'
    except Exception as exc:
        outcome=type(exc).__name__+': '+str(exc)
    summary[name]=outcome;print(name,outcome,flush=True)
expected=summary['success']=='COMPLETED' and summary['second_arm_reset_mismatch']!='COMPLETED'
(base/'summary.json').write_text(json.dumps({'outcomes':summary,'expected_observed':expected,'scope':'synthetic only'},indent=2,sort_keys=True)+'\n')
if not expected:raise SystemExit(1)
