#!/usr/bin/env python3
"""Aggregate-only identity linkage; emits neither task identities nor outcomes."""
from pathlib import Path
import hashlib,json,zipfile
V=Path('/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/validation'); N=Path('/home/lizening/research-notes/agent-logs'); T=Path('/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/model-artifacts/sft-policy-bootstrap/full')
D={'R14':V/'progress-aware-recovery-r14-20260910T000000Z','R15':V/'progress-aware-recovery-r15-b-20260910T000000Z','R16':V/'progress-aware-recovery-r16-osr-20260910T000000Z','R17':V/'progress-aware-recovery-r17-par-20260911T000000Z','R18C1':V/'progress-aware-r18-c1-20260911T000000Z','R18C2':V/'progress-aware-r18-c2-formal-aa9fa3c34520941e'}
F={'r14raw':D['R14']/'raw_trajectories.jsonl','registry':N/'2026-10-25T065200Z__LUNA__si-p1-isolation-budget__caae4c/KNOWN_USE_IDENTITIES.json','oldzip':Path('/tmp/si-official-archive-audit-20261029/0.2.2.zip'),'newzip':Path('/tmp/si-official-archive-audit-20261029/0.4.0.zip'),'training_result':T/'training_result.json','trainer_state':T/'checkpoints/checkpoint-2354/trainer_state.json'}
for name,d in D.items():
 F[name+'_manifest']=d/'run_manifest.json'
 if name!='R14':
  F[name+'_replay']=d/('replay_validation.jsonl' if name.startswith('R18') else 'replay_ledger.jsonl')
  F[name+'_branch']=d/({'R15':'continue_ledger.jsonl','R16':'osr_ledger.jsonl','R17':'par_ledger.jsonl','R18C1':'fact_text_branches.jsonl','R18C2':'card_v2_branches.jsonl'}[name])
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for x in iter(lambda:f.read(1024*1024),b''):h.update(x)
 return h.hexdigest()
H={k:sha(p) for k,p in F.items()}
assert H['oldzip']=='d376c4bbb097c068528a2a9805e358e4cd14bc75c4d68a24e5141aebd234ef67' and H['newzip']=='eea90499df27b9cb3147d1d1927264146d38194b575e25f70a82875545742dcb'
def load(k):return json.loads(F[k].read_bytes())
m=load('R14_manifest');assert m['status']=='completed' and m['accepted_episodes']==180 and m['raw_trajectory_sha256']==H['r14raw']
raw=[json.loads(x) for x in F['r14raw'].read_bytes().splitlines() if x];source={x['metadata']['schedule_index']:x['task']['task_id'] for x in raw};assert len(raw)==len(source)==len(set(source.values()))==180
registered=set(load('registry')['registered_identity_members']['R14_completed_schedule_positions']);assert registered==set(source.values())
with zipfile.ZipFile(F['oldzip']) as a,zipfile.ZipFile(F['newzip']) as b:
 extra={x.filename for x in a.infolist() if not x.is_dir()}-{x.filename for x in b.infolist() if not x.is_dir()}
oldids={'/'.join(Path(x).parts[2:4]) for x in extra};oldparents={Path(x).parts[2] for x in extra};sourceids=set(source.values());sourceparents={x.split('/')[0] for x in sourceids}
result={};mapped_sets=[]
for name in ('R15','R16','R17','R18C1','R18C2'):
 mm=load(name+'_manifest');assert mm['status']=='completed'
 records=[json.loads(x) for x in F[name+'_replay'].read_bytes().splitlines() if x];seen={(r['prefix_id'],r['schedule_index'],r['task_id']) for r in records};assert len(records)==len(seen)==60
 assert all(source.get(r['schedule_index'])==r['task_id'] for r in records)
 assert all(r.get('replay_pass',r.get('replay_match')) is True for r in records)
 tasks={r['task_id'] for r in records};assert len(tasks)==60
 branch=[json.loads(x) for x in F[name+'_branch'].read_bytes().splitlines() if x]
 bset={(r['prefix_id'],r['schedule_index'],r['task_id']) for r in branch};assert len(branch)==60 and bset==seen
 result[name]={'replay_rows':len(records),'matching_source_schedule_rows':len(records),'replay_pass_rows':len(records),'branch_rows_matching_replay_identity':len(branch),'unique_task_ids':len(tasks),'old_only_exact_trial_identity_matches':len(tasks&oldids),'old_only_parent_name_matches':len({t.split('/')[0] for t in tasks}&oldparents)};mapped_sets.append(seen)
assert all(x==mapped_sets[0] for x in mapped_sets)
tstate=load('trainer_state');tres=load('training_result');history=tstate.get('log_history',[]);keys={k for r in history for k in r};assert all('task' not in k.lower() and 'sample' not in k.lower() or k in ('eval_samples_per_second',) for k in keys)
assert H=={k:sha(p) for k,p in F.items()}
out={'status':'PASS_BOUNDED_IDENTITY_LINKAGE_ONLY','input_sha256':H,'r14_raw_manifest_sha_match':True,'r14_completed_rows':len(raw),'r14_unique_task_ids':len(sourceids),'r14_unique_parent_names':len(sourceparents),'registry_r14_category_matches_all_180_exact':registered==sourceids,'r14_old_only_trial_identity_matches':len(sourceids&oldids),'r14_old_only_parent_name_matches':len(sourceparents&oldparents),'five_stage_same_60_identity_index_tuples':True,'later_replays':result,'p0_training_result_and_trainer_state_present':True,'p0_trainer_log_rows':len(history),'p0_trainer_log_contains_task_id_or_sample_id_keys':False,'p0_trainer_state_cannot_prove_per_task_optimizer_exposure':True,'limits':['R14 raw hash is bound by saved run manifest; later replay files are current saved files with independently recorded byte hashes, not newly authenticated supervisor receipts.','All 180 R14 identities were already in the protected registry; no reclassification of historical candidates and no newly usable pool.','A parent-name match is not proof the corresponding old-only trial ran; exact-ID nonmatch is not proof of lifetime nonexposure.','No individual outcomes, prompts, raw states, task IDs or model outputs are emitted.']}
Path(__file__).with_name('HISTORY_LINKAGE.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('input_sha256','limits')},sort_keys=True))
