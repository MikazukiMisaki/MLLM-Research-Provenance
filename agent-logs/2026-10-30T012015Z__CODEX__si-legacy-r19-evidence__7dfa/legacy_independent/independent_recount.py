#!/usr/bin/env python3
"""Independent read-only archive metadata and historical G1 aggregate audit."""
from pathlib import Path
import hashlib,json,zipfile,collections
import os
repo=Path('/home/lizening/wt-codex-r18c2');notes=Path('/home/lizening/research-notes/agent-logs');art=Path('/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime');root=Path('/home/lizening/alfworld_data')
files={
 '022':Path('/tmp/si-official-archive-audit-20261029/0.2.2.zip'),
 '040':Path('/tmp/si-official-archive-audit-20261029/0.4.0.zip'),
 '042':Path('/tmp/si-official-archive-audit-20261030-042/0.4.2.zip'),
 'g1_schedule':repo/'configs/evaluation/sft_heldout_valid_unseen_schedule.json',
 'g1_manifest':art/'validation/sft-valid-unseen-g1-20260829T031028Z/run_manifest.json',
 'g1_raw':art/'validation/sft-valid-unseen-g1-20260829T031028Z/trajectories.jsonl',
 'registry':notes/'2026-10-25T065200Z__LUNA__si-p1-isolation-budget__caae4c/KNOWN_USE_IDENTITIES.json',
 'sft':repo/'configs/sft/sft_task_splits.json',
 'sft_extension':repo/'configs/sft/sft_pick_two_balance_extension.json',
 'expert':art/'sft-policy-bootstrap/sft_expert_dataset_balanced.jsonl',
 'eval_schedule':notes/'2026-10-29T113523Z__ASTRA__three-arm-prospective-design__a55d1af9/PILOT82_PROPOSED_SCHEDULE_PRIVATE.json',
 'B_manifest':notes/'2026-10-29T115700Z__SOL__si-pilot82-dataset-materialization/B_manifest_candidate_PRIVATE.json',
 'C_manifest':notes/'2026-10-29T115700Z__SOL__si-pilot82-dataset-materialization/C_manifest_candidate_PRIVATE.json',
 'reserved':notes/'2026-10-25T084517Z__LUNA__si-p3-isolation-budget-design__si3_7d91/partition_proposal.json'}
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for buf in iter(lambda:f.read(1024*1024),b''):h.update(buf)
 return h.hexdigest()
hashes={k:digest(p) for k,p in files.items()}
expected={'022':'d376c4bbb097c068528a2a9805e358e4cd14bc75c4d68a24e5141aebd234ef67','040':'eea90499df27b9cb3147d1d1927264146d38194b575e25f70a82875545742dcb','042':'5df77ea759f2211a4106082839ddbbb790f1ba4e7d097ed732cf453f72aa36cf','g1_schedule':'7ce71ad01bd03ad8a018104f3edacc4310e9a1b5fc6e015d808152f316e4e13e','g1_raw':'aaf6c90fc686eebb8efffd1ef80ef702677426dadbe127d8ca6a6013bc692f8e'}
assert all(hashes[k]==v for k,v in expected.items())
sets={}
for k in ('022','040','042'):
 with zipfile.ZipFile(files[k]) as z:
  names=[x.filename for x in z.infolist() if not x.is_dir()]
  assert len(names)==len(set(names))
  assert all(len(Path(n).parts)==5 and Path(n).parts[0]=='json_2.1.1' and Path(n).parts[-1]=='game.tw-pddl' for n in names)
  sets[k]=set(names)
assert sets['040']==sets['042'] and sets['040']<=sets['022']
extra=sets['022']-sets['040']; parents={Path(n).parts[2] for n in extra};present_parents={Path(n).parts[2] for n in sets['040']}
by_split={}
for split in ('train','valid_seen','valid_unseen','valid_train'):
 members=[n for n in extra if Path(n).parts[1]==split];oldparents={Path(n).parts[2] for n in members};same={Path(n).parts[2] for n in sets['040'] if Path(n).parts[1]==split}
 by_split[split]={'old_only_trials':len(members),'old_only_parent_names':len(oldparents),'same_split_current_parent_matches':len(oldparents&same),'any_split_current_parent_matches':len(oldparents&present_parents)}
local=collections.Counter()
for n in extra:
 trial=root.joinpath(*Path(n).parts[:-1]);local['directories']+=trial.is_dir();local['trajectory_siblings']+=(trial/'traj_data.json').is_file();local['game_files']+=(trial/'game.tw-pddl').is_file()
g1=json.loads(files['g1_schedule'].read_bytes());manifest=json.loads(files['g1_manifest'].read_bytes());assert hashes['g1_schedule']==manifest['schedule_sha256'] and hashes['g1_raw']==manifest['trajectory_sha256'] and manifest['accepted_episodes']==60
schedule={x['schedule_index']:(x['split'],x['task_id'],x['source_game_sha256']) for x in g1['episodes']};actual={}
with files['g1_raw'].open() as f:
 for line in f:
  x=json.loads(line); idx=x['metadata']['schedule_index'];assert idx not in actual;actual[idx]=(x['task']['split'],x['task']['task_id'],x['metadata']['source_game_sha256'])
assert len(schedule)==60 and actual==schedule
common=collections.Counter();fields=('grammar','pddl_domain','pddl_problem','solvable','walkthrough');old_presence=collections.Counter();new_presence=collections.Counter();unequal=collections.Counter()
with zipfile.ZipFile(files['022']) as old,zipfile.ZipFile(files['040']) as new:
 for split,task,dg in schedule.values():
  name=f'json_2.1.1/{split}/{task}/game.tw-pddl';a=old.read(name);b=new.read(name)
  common['040_matches_g1_game_hash']+=hashlib.sha256(b).hexdigest()==dg;common['byte_equal']+=a==b
  oa,ob=json.loads(a),json.loads(b);assert isinstance(oa,dict) and isinstance(ob,dict)
  for k in fields:
   old_presence[k]+=k in oa;new_presence[k]+=k in ob;unequal[k]+=(k in oa)!=(k in ob) or (k in oa and oa[k]!=ob[k])
def par(x):return x.split('/')[0]
def read(key):return json.loads(files[key].read_bytes())
registry={par(x) for xs in read('registry')['registered_identity_members'].values() if isinstance(xs,list) for x in xs}
sft={par(x['task_id']) for k in ('sft','sft_extension') for rows in read(k)['pools'].values() for x in rows}
expert=set()
with files['expert'].open() as f:
 for line in f:expert.add(par(json.loads(line)['task_id']))
evalp={par(x['task_id']) for x in read('eval_schedule')['rows']}
bc={x for k in ('B_manifest','C_manifest') for x in read(k)['task_exposures']}
reserve={par(x['identity']) for x in read('reserved')['rows']};g1p={par(task) for split,task,dg in actual.values()}
groups={'registry':registry,'sft_candidate':sft,'expert_source':expert,'si_u1_evaluation_schedule':evalp,'bc_materialized':bc,'g1_executed':g1p,'prior_proposal_reserved':reserve}
known=registry|sft|expert|evalp|bc|g1p;protected=known|reserve
assert len(extra)==1207 and len(parents)==556 and len(parents&present_parents)==210 and len(parents-present_parents)==346
assert dict(local)=={'directories':1207,'trajectory_siblings':1207,'game_files':0}
assert common['040_matches_g1_game_hash']==60 and common['byte_equal']==0
assert all(old_presence[k]==new_presence[k]==60 and unequal[k]==60 for k in ('grammar','pddl_domain'))
assert all(old_presence[k]==new_presence[k]==60 and unequal[k]==0 for k in ('pddl_problem','solvable'))
assert old_presence['walkthrough']==0 and new_presence['walkthrough']==60
assert len(parents&known)==200 and len(parents&protected)==209
assert hashes=={k:digest(p) for k,p in files.items()}
out={'status':'PASS_INDEPENDENT_STATIC_RECOUNT_ONLY','source_input_sha256':hashes,'archive_game_counts':{k:len(s) for k,s in sets.items()},'old_only_trial_paths':len(extra),'old_only_split_parent_pairs':len({(Path(n).parts[1],Path(n).parts[2]) for n in extra}),'globally_distinct_parent_names':len(parents),'current_archive_any_split_parent_matches':len(parents&present_parents),'current_archive_any_split_parent_nonmatches':len(parents-present_parents),'old_only_by_split':by_split,'local_sibling_presence':dict(local),'historical_g1_matched_count':len(schedule),'historical_common_path_comparison':dict(common),'historical_field_old_presence':dict(old_presence),'historical_field_current_presence':dict(new_presence),'historical_field_unequal':dict(unequal),'history_parent_name_overlap':{k:len(parents&v) for k,v in groups.items()},'known_and_possible_history_parent_union':len(parents&known),'with_proposal_reserved_parent_union':len(parents&protected),'parent_only_remainder':len(parents-protected),'limits':['ZIP retrieved bytes lack independently authenticated upstream signed digest; member names and presence are not runtime or independent-sample proofs.','Metadata sibling presence does not prove historical old-game/metadata version correspondence or prior execution.','60 field comparisons are already-executed G1 common paths, not the old-only candidates; semantic equivalence and migration behavior remain unproved.','History membership includes candidate and proposed task lists, not individually proved execution; remainder is not a verified unexposed task pool.']}
Path(__file__).with_name('RECOUNT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('source_input_sha256','limits')},sort_keys=True))
