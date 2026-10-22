import datetime,hashlib,json,runpy,sys,traceback
from pathlib import Path
import pytest
root=Path('/home/lizening/wt-r19-source-contract-review-fixes');sys.path[:0]=[str(root),str(root/'src')]
ns=runpy.run_path(str(root/'tests/test_r19_source_pipeline.py'));runner=ns['runner'];analyzer=ns['analyzer']
now=datetime.datetime.now(datetime.timezone.utc)
p=Path('/home/lizening/research-notes/agent-logs')/(now.strftime('%Y-%m-%dT%H%M%SZ')+'__SOL__r19-alias-validator-scope__'+now.strftime('%f'));p.mkdir()
Path('/tmp/r19-alias-scope-record-path.txt').write_text(str(p)+'\n')
files=[root/'scripts/run_r19_experiment.py',root/'scripts/analyze_r19_recovery_duration.py',root/'src/recovery/r19_duration.py',root/'tests/test_r19_source_pipeline.py']
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
initial={str(f):sha(f) for f in files}
with pytest.MonkeyPatch.context() as mp:
 runtime,registry,schedule,output,envs,pending=ns['runtime_fixture'](p,mp,restart=True)
 recovery_calls=0
 def generate(backend,prompt,cap):
  global recovery_calls
  if cap==40:raw='Diagnosis: Immediate issue\nSubgoal: take pencil 1 from desk 1'
  elif backend is runtime.recovery_backend:
   recovery_calls+=1;raw='A000' if recovery_calls==1 else 'invalid'
  else:raw='A000'
  return ns['generation'](prompt,raw,cap)
 mp.setattr(runner,'_generate_exact',generate)
 result=runner._run_frozen_pilot(runtime=runtime,schedule=schedule,output_path=output,registry=registry,sink=runtime.sink,pending_attempts=pending)
 runtime.close_remaining_environments();events=ns['read_events'](output)
 branches=[json.loads(l) for l in (output/'branches.jsonl').read_text().splitlines()]
 try:analyzer.validate_branch_evidence(branches,events)
 except Exception as e:failure={'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()}
 else:raise AssertionError('expected alias rejection absent')
 arms=branches[0]['k_results']
 order=[e['payload']['order'] for e in events if e['kind']=='suffix_order_frozen']
 completions=[{'k':e['identity']['k'],'sequence':e['sequence'],'event_id':e['event_id'],'alias_source_event':e['payload'].get('derived_source_event_id')} for e in events if e['kind']=='duration_arm_completed']
 summary={'classification':'SOFTWARE_ONLY_NO_LIVE_OR_FORMAL_G4','base_head':'da7d348ffd3677d619dd31357e1e1e3cca28c9ec','uncommitted_source_sha256':initial,'source_unchanged_during_probe':all(sha(f)==initial[str(f)] for f in files),'actual_order':order,'arm_completion_sequence':completions,'aliases':{k:a['derived_identity_from'] for k,a in arms.items()},'checkpoint':{k:a['checkpoint'] for k,a in arms.items()},'recovery_calls':{k:a['logical_cost']['recovery_only']['model_calls'] for k,a in arms.items()},'suffix_ids':{k:a['evidence_refs'].get('suffix_generation_event_ids') for k,a in arms.items()},'costs':{k:a['logical_cost'] for k,a in arms.items()},'validation_failure':failure,'production_execution_result':result,'real_model_or_alfworld_calls':0}
 assert summary['source_unchanged_during_probe']
 assert summary['aliases']=={'1':2,'2':None,'3':2,'4':2,'5':2}
 assert summary['recovery_calls']['1']==2 and summary['recovery_calls']['2']==3
 (p/'independent_reproduction.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps({k:summary[k] for k in ['actual_order','aliases','recovery_calls','checkpoint','validation_failure']},indent=2))
 print('scope_directory',str(p))
