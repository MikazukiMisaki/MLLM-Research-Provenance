"""Retain fictional-only bridge receipts."""
import json
from pathlib import Path
import global_owner
import bridge
from test_bridge import fixture
base=Path(__file__).parent/'synthetic_evidence';base.mkdir(mode=0o700,exist_ok=False)
summary={}
for name in ('success','second_arm_reset_mismatch'):
 root=base/name;root.mkdir(mode=0o700);inputs,setup,verify=fixture(root)
 try:
  bridge.run_synthetic_bridge(root/'run',root,inputs,setup,verify,mode_by_case={global_owner.SCHEDULE[0][0]:'mismatch'} if name!='success' else None)
  outcome='COMPLETED'
 except Exception as exc:outcome=type(exc).__name__+': '+str(exc)
 summary[name]=outcome;print(name,outcome,flush=True)
expected=summary['success']=='COMPLETED' and summary['second_arm_reset_mismatch']!='COMPLETED'
(base/'summary.json').write_text(json.dumps({'outcomes':summary,'expected_observed':expected,'scope':'fictional only','budget_sufficiency':'NOT_VERIFIED'},indent=2,sort_keys=True)+'\n')
if not expected:raise SystemExit(1)
