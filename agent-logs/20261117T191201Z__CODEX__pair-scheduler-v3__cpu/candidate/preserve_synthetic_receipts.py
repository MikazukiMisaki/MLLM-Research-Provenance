"""Reproduce only fictional fixtures for persistent review evidence."""
import json
from pathlib import Path
from unittest.mock import patch
import global_owner
import scheduler_synthetic
from test_scheduler import fixture

base=Path(__file__).parent/'synthetic_evidence'
base.mkdir(mode=0o700,exist_ok=False)
summary={}
for name in ('success','bad_kwargs','capture_failure'):
    root=base/name
    root.mkdir(mode=0o700)
    inputs,setup,verify=fixture(root)
    try:
        if name=='bad_kwargs':
            scheduler_synthetic.run_fixture(root/'run',root,inputs,setup,verify,mode_by_case={global_owner.SCHEDULE[0][0]:'bad_kwargs'})
        elif name=='capture_failure':
            with patch.object(scheduler_synthetic,'capture_owned',side_effect=RuntimeError('synthetic capture failure')):
                scheduler_synthetic.run_fixture(root/'run',root,inputs,setup,verify)
        else:
            scheduler_synthetic.run_fixture(root/'run',root,inputs,setup,verify)
        outcome='COMPLETED'
    except Exception as exc:
        outcome=type(exc).__name__+': '+str(exc)
    summary[name]=outcome
    print(name,outcome,flush=True)
expected=summary['success']=='COMPLETED' and summary['bad_kwargs']!='COMPLETED' and summary['capture_failure'].startswith('RuntimeError: synthetic capture failure')
(base/'summary.json').write_text(json.dumps({'outcomes':summary,'expected_outcomes_observed':expected,'scope':'synthetic only'},sort_keys=True,indent=2)+'\n')
if not expected:raise SystemExit(1)
