"""Reproduce the alias validator conflict using production synthetic orchestration."""
import json, runpy, sys
from pathlib import Path
import pytest
root=Path('/home/lizening/wt-r19-source-contract-review-fixes')
sys.path[:0]=[str(root),str(root/'src')]
ns=runpy.run_path(str(root/'tests/test_r19_source_pipeline.py'))
runner=ns['runner']; analyzer=ns['analyzer']
output_root=Path(__file__).parent/'alias_reproduction'
output_root.mkdir()
with pytest.MonkeyPatch.context() as mp:
 runtime,registry,schedule,output,envs,pending=ns['runtime_fixture'](output_root,mp,restart=True)
 recovery_calls=0
 def generate(backend,prompt,cap):
  global recovery_calls
  if cap==40:
   raw='Diagnosis: Immediate issue\nSubgoal: take pencil 1 from desk 1'
  elif backend is runtime.recovery_backend:
   recovery_calls+=1
   raw='A000' if recovery_calls==1 else 'invalid'
  else: raw='A000'
  return ns['generation'](prompt,raw,cap)
 mp.setattr(runner,'_generate_exact',generate)
 runner._run_frozen_pilot(runtime=runtime,schedule=schedule,output_path=output,registry=registry,sink=runtime.sink,pending_attempts=pending)
 runtime.close_remaining_environments()
 events=ns['read_events'](output)
 branches=[json.loads(l) for l in (output/'branches.jsonl').read_text().splitlines()]
 print('software_only',True,'real_model_or_ALFWorld_calls',0)
 print('aliases',{k:v['derived_identity_from'] for k,v in branches[0]['k_results'].items()})
 try:
  analyzer.validate_branch_evidence(branches,events)
 except Exception as error:
  print(type(error).__name__,str(error))
 else:raise AssertionError('Expected production validator alias conflict did not reproduce')
