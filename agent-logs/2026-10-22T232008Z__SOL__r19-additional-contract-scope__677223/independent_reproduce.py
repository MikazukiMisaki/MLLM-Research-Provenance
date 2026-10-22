import datetime,hashlib,json,runpy,sys,traceback
from pathlib import Path
import pytest
root=Path('/home/lizening/wt-r19-source-contract-review-fixes');sys.path[:0]=[str(root),str(root/'src')]
from scripts import run_r19_experiment as runner
from scripts import analyze_r19_recovery_duration as analyzer
now=datetime.datetime.now(datetime.timezone.utc)
p=Path('/home/lizening/research-notes/agent-logs')/(now.strftime('%Y-%m-%dT%H%M%SZ')+'__SOL__r19-additional-contract-scope__'+now.strftime('%f'));p.mkdir()
Path('/tmp/r19-scope-record-path.txt').write_text(str(p)+'\n')
files=[root/'scripts/run_r19_experiment.py',root/'scripts/analyze_r19_recovery_duration.py',root/'tests/test_r19_source_pipeline.py']
source_hashes={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
helper=runpy.run_path(str(root/'tests/test_r19_source_pipeline.py'))
with pytest.MonkeyPatch.context() as mp:
 runtime,registry,schedule,output,envs,pending=helper['runtime_fixture'](p,mp,restart=True)
 execution=runner._run_frozen_pilot(runtime=runtime,schedule=schedule,output_path=output,registry=registry,sink=runtime.sink,pending_attempts=pending)
 runtime.close_remaining_environments()
 events=helper['read_events'](output)
 try:analyzer.validate_event_ledger(events,expected_evidence_class='synthetic')
 except Exception as e:validation={'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()}
 else:raise AssertionError('expected unrepaired replay receipt failure missing')
 replay=[e for e in events if e['kind']=='environment_operation_completed' and e['identity'].get('operation') in ('replay_environment_step','branch_replay_environment_step')]
 phys=[e['identity']['recovery_action_index'] for e in events if e['kind']=='environment_operation_completed' and e['identity'].get('operation')=='recovery_environment_operation']
 scheduler=[e['payload']['action']['recovery_action_index'] for e in events if e['kind']=='recovery_action_completed']
 summary={'classification':'independent_software_only_reproduction_no_scientific_operations','base_head':'da7d348ffd3677d619dd31357e1e1e3cca28c9ec','uncommitted_source_sha256':source_hashes,'execution':execution,'validation_failure':validation,'replay_completions':len(replay),'first_replay_receipt':{'identity':replay[0]['identity'],'command':replay[0]['payload']['command'],'action_id':replay[0]['payload']['action_id'],'action_map':replay[0]['payload']['action_map']},'physical_recovery_indices':phys,'scheduler_recovery_indices':scheduler,'recovery_events':[{'kind':e['kind'],'identity':e['identity'],'payload_keys':list(e['payload'])} for e in events if 'recovery_action' in e['kind']],'phase_env_operation_counts':dict(runtime.environment_operation_counts),'source_snapshot_unchanged_during_probe':all(hashlib.sha256(f.read_bytes()).hexdigest()==source_hashes[str(f)] for f in files)}
 assert summary['source_snapshot_unchanged_during_probe']
 (p/'independent_reproduction.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps({'directory':str(p),'failure':validation['message'],'first_replay':summary['first_replay_receipt'],'physical_indices':phys,'scheduler_indices':scheduler,'phase_counts':summary['phase_env_operation_counts']},indent=2))
