import datetime,hashlib,json,sys
from pathlib import Path
root=Path('/home/lizening/wt-r19-recovery-duration-v1');output=root/'artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z'
p=Path(Path('/tmp/r19-live-monitor-path.txt').read_text().strip())
sys.path[:0]=[str(root),str(root/'src')]
from scripts import analyze_r19_recovery_duration as a
schedule_path=root/'configs/experiments/r19_preflight_v3/source_schedule.json';exclusion_path=root/'configs/experiments/r19_preflight_v3/exclusion_manifest.json'
schedule=json.loads(schedule_path.read_text());exclusion=json.loads(exclusion_path.read_text())
events=[];completed=0;raw_hash=hashlib.sha256();offset=0
with (output/'execution_events.jsonl').open('rb') as stream:
 for line in stream:
  if not line.endswith(b'\n'):break
  event=json.loads(line);events.append(event);raw_hash.update(line);offset=stream.tell()
  if event['kind']=='source_episode_completed':completed+=1
  if completed==127:break
assert completed==len(schedule['episodes'])==127,'Full frozen source schedule not yet complete; no subset accepted'
physical=a.validate_event_ledger(events,expected_evidence_class='live')
source_result=a.validate_live_source_schedule(schedule,exclusion,events,[],physical)
assert source_result['status']=='PASS_FROZEN_TRAIN_SCHEDULE_BINDING'
rows=[json.loads(line) for line in (output/'source_trajectories.jsonl').read_text().splitlines() if line.strip()]
assert len(rows)==127
by_id={event['event_id']:event for event in events}
for i,row in enumerate(rows):
 assert row['metadata']['schedule_index']==i
 event=by_id[row['metadata']['r19_source_event_refs']['source_episode_event_id']]
 assert event['payload']['trajectory_sha256']==row['metadata']['source_trajectory_sha256']==a._source_trajectory_digest(row)
registry=json.loads((output/'unit_registry.json').read_text())
source_units=[unit for unit in registry['units'].values() if unit['identity'].get('unit')=='source_episode']
assert len(source_units)==127 and all(unit['status']=='completed' for unit in source_units)
result={'status':'PASS_GENUINE_FULL_127_SOURCE_PREFIX_INTEGRITY','verified_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'run_id':events[-1]['run_id'],'implementation_sha':events[-1]['implementation_sha'],'source_validator':source_result,'source_prefix_physical':physical,
 'source_trajectory_artifact_rows':len(rows),'all_127_source_units_completed':True,'source_prefix_last_sequence':events[-1]['sequence'],
 'source_prefix_last_event_id':events[-1]['event_id'],'source_prefix_byte_length':offset,'source_prefix_raw_sha256':raw_hash.hexdigest(),
 'source_trajectories_raw_sha256':hashlib.sha256((output/'source_trajectories.jsonl').read_bytes()).hexdigest(),
 'original_schedule_raw_sha256':hashlib.sha256(schedule_path.read_bytes()).hexdigest(),'original_exclusion_raw_sha256':hashlib.sha256(exclusion_path.read_bytes()).hexdigest(),
 'schedule_was_not_modified_or_subsampled':True,'only_genuine_events_through_last_source_completion_used':True,
 'G3_recovery_phase_outcome':'NOT_INFERRED_FROM_THIS_SOURCE_ONLY_CHECK','G4_executed':False,'new_scientific_model_environment_calls':0}
(p/'full_source_integrity.json').write_text(json.dumps(result,indent=2)+'\n')
(p/'validate_complete_source_prefix.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps({'status':result['status'],'source_validator':source_result,'source_prefix_physical':{k:physical[k] for k in ('event_count','completed_physical_model_generations','physical_environment_operations','physical_environment_resets','incomplete_operations')}},indent=2))
