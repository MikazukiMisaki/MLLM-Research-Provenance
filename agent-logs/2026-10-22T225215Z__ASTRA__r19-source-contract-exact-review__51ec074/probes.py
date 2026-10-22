"""Independent read-only source review probes; generation and environment edges synthetic."""
import copy,hashlib,json,os,runpy,subprocess,sys,tempfile,shutil
from pathlib import Path
root=Path('/tmp/r19-source-review-51ec074')
sys.path[:0]=[str(root),str(root/'src')]
import pytest
from env.base import Task,ResetResult
from recovery.r19_duration import UnitRegistry
from scripts import run_r19_experiment as runner
helpers=runpy.run_path(str(root/'tests/test_r19_source_contract.py'))
base=Path('/tmp/r19-source-review-evidence-51ec074')
with tempfile.TemporaryDirectory(prefix='first-source-',dir=base) as d,pytest.MonkeyPatch.context() as mp:
 tmp=Path(d)
 row,events,physical,runtime,env,schedule,exclusions=helpers['run_source'](tmp,mp,['A001'],restart_expected=True)
 output=tmp/'source'
 comparison_path=output/'source_restart_comparison.json'
 print('FIRST_SOURCE_INTEGRATION','PASS','REAL_MODEL_CALLS',0,'REAL_ALFWORLD_CALLS',0)
 shutil.copytree(output,base/'first_source_fixture')
 expected=helpers['_expected_restart_snapshot']('A001')
 manifest={'source_restart_comparison_sha256':runner.sha256_file(comparison_path),'source_restart_comparison_status':'PASS','source_restart_predecessor_run_id':'preserved-failed-source-run','source_restart_repeated_generation_count':1,'source_restart_repeated_reset_count':1}
 fixture={'execution_manifest':manifest,'events':events,'predecessor_run_id':'preserved-failed-source-run','expected_snapshot':expected,'expected_snapshot_sha256':runner.sha256_json(expected),'comparison_path':str(base/'first_source_fixture/source_restart_comparison.json')}
 fixturepath=base/'fresh-comparator-input.json';fixturepath.write_text(json.dumps(fixture)+'\n')
 code='''import json,runpy,sys\nfrom pathlib import Path\nns=runpy.run_path(sys.argv[1])\nargs=json.loads(Path(sys.argv[2]).read_text())\nargs["comparison_path"]=Path(args["comparison_path"])\nprint(ns["validate_source_restart_comparison"](**args))\n'''
 clean=dict(os.environ)
 for key in ('PYTHONPATH','PYTHONHOME','VIRTUAL_ENV'):clean.pop(key,None)
 cmd=[sys.executable,'-c',code,str(root/'scripts/analyze_r19_recovery_duration.py'),str(fixturepath)]
 child=subprocess.run(cmd,cwd=tmp,env=clean,capture_output=True,text=True)
 (base/'fresh_comparator_result.json').write_text(json.dumps({'argv':cmd,'exit_code':child.returncode,'stdout':child.stdout,'stderr':child.stderr},indent=2)+'\n')
 print('FRESH_G4_COMPARATOR','EXIT',child.returncode,'STDERR',child.stderr.strip().replace('\n',' | '))
 print('RETURNED_TRAJECTORY_HASH',row['metadata']['source_trajectory_sha256'],'RECOMPUTED',runner._trajectory_sha256(row),'MATCH',row['metadata']['source_trajectory_sha256']==runner._trajectory_sha256(row))
 stored=[json.loads(l) for l in (output/'source_trajectories.jsonl').read_text().splitlines()]
 print('STORED_TRAJECTORY_CANONICAL_HASH_MATCH',runner._trajectory_sha256(stored[0])==stored[0]['metadata']['source_trajectory_sha256'])
 episode2=copy.deepcopy(schedule['episodes'][0]); episode2.update(canonical_trial_id='synthetic-second-source/trial-002',schedule_index=1,nominal_seed=30001,reset_order_position=1)
 env2=helpers['ToyEnvironment'](terminal_after=1)
 env2.task=Task(task_id=episode2['canonical_trial_id'],text='put a pencil in garbagecan',split='train',family='pick_and_place_simple')
 env2.reset=lambda seed:ResetResult('state 0',env2.task,('look','go to garbagecan 1'))
 mp.setattr(runner,'_generate_exact',lambda _backend,prompt,_cap:helpers['_synthetic_generation'](prompt,'A001'))
 registry=UnitRegistry(output/'registry.json')
 uid=registry.begin({'unit':'source_episode','canonical_trial_id':episode2['canonical_trial_id'],'schedule_index':1})
 before=(runtime.model_call_counts.copy(),runtime.environment_operation_counts.copy())
 try:
  runtime._collect_one_source(env2,episode2,output,{episode2['canonical_trial_id']:uid})
 except Exception as e:
  print('SECOND_SOURCE_AFTER_VALID_FIRST',type(e).__name__,str(e))
  print('SECOND_SOURCE_SYNTHETIC_GENERATIONS',runtime.model_call_counts['source']-before[0]['source'],'SECOND_SOURCE_SYNTHETIC_RESETS',runtime.environment_operation_counts['source']-before[1]['source'],'SECOND_SOURCE_ACTIONS',len(env2.actions))
 else:print('SECOND_SOURCE_AFTER_VALID_FIRST','UNEXPECTED_PASS')
 shutil.copytree(output,base/'second_source_failure_fixture')
