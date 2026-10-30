from pathlib import Path
import hashlib, json, re, zipfile
from collections import defaultdict
N=Path('/home/lizening/research-notes/agent-logs');R=Path('/home/lizening/wt-codex-r18c2');D=Path('/home/lizening/alfworld_data/json_2.1.1');P=Path('/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime');O=Path(__file__).parent
F={'oldzip':Path('/tmp/si-official-archive-audit-20261029/0.2.2.zip'),'newzip':Path('/tmp/si-official-archive-audit-20261029/0.4.0.zip'),'registry':N/'2026-10-25T065200Z__LUNA__si-p1-isolation-budget__caae4c/KNOWN_USE_IDENTITIES.json','sft':R/'configs/sft/sft_task_splits.json','sft_ext':R/'configs/sft/sft_pick_two_balance_extension.json','expert':P/'sft-policy-bootstrap/sft_expert_dataset_balanced.jsonl','eval':N/'2026-10-29T113523Z__ASTRA__three-arm-prospective-design__a55d1af9/PILOT82_PROPOSED_SCHEDULE_PRIVATE.json','eval_bind':N/'2026-10-29T120900Z__SOL__si-pilot82-game-byte-isolation/EVAL_BYTE_BINDINGS_PRIVATE.json','b':N/'2026-10-29T115700Z__SOL__si-pilot82-dataset-materialization/B_manifest_candidate_PRIVATE.json','c':N/'2026-10-29T115700Z__SOL__si-pilot82-dataset-materialization/C_manifest_candidate_PRIVATE.json','proposal':N/'2026-10-25T084517Z__LUNA__si-p3-isolation-budget-design__si3_7d91/partition_proposal.json','probe1':N/'2026-10-29T121500Z__CODEX__si-eval-engineering-task-metadata/ENGINEERING_CANDIDATE_PRIVATE.json','probe2':N/'2026-10-29T132000Z__LUNA__si-eval-remediation-candidate__metadata/ENGINEERING_CANDIDATE_PRIVATE.json','g1':R/'configs/evaluation/sft_heldout_valid_unseen_schedule.json','g1manifest':P/'validation/sft-valid-unseen-g1-20260829T031028Z/run_manifest.json','g1raw':P/'validation/sft-valid-unseen-g1-20260829T031028Z/trajectories.jsonl','local':N/'2026-10-29T231522Z__CODEX__si-next-data-isolation-readonly__f2a1/CANDIDATE_METADATA_PRIVATE.json'}
def sha_bytes(f):
 h=hashlib.sha256()
 while True:
  b=f.read(1048576)
  if not b:return h.hexdigest()
  h.update(b)
def sha(p):
 with p.open('rb') as f:return sha_bytes(f)
def data(k):return json.loads(F[k].read_text())
def suffix(parent):
 m=re.fullmatch(r'[^/]+-(\d+)',parent)
 if not m:raise ValueError('unexpected parent format')
 return int(m[1])
def parent(identity):return identity.split('/')[0]
H={k:sha(v) for k,v in F.items()}
assert H['oldzip']=='d376c4bbb097c068528a2a9805e358e4cd14bc75c4d68a24e5141aebd234ef67'
assert H['newzip']=='eea90499df27b9cb3147d1d1927264146d38194b575e25f70a82875545742dcb'
g1=data('g1');gm=data('g1manifest');assert H['g1']==gm['schedule_sha256'] and H['g1raw']==gm['trajectory_sha256']
a={x['schedule_index']:(x['task_id'],x['split'],x['source_game_sha256']) for x in g1['episodes']}
b={}
with F['g1raw'].open() as f:
 for line in f:
  x=json.loads(line); index=x['metadata']['schedule_index'];assert index not in b
  b[index]=(x['task']['task_id'],x['task']['split'],x['metadata']['source_game_sha256'])
assert len(a)==len(b)==60 and gm['accepted_episodes']==60 and a==b and all(v[1]=='valid_unseen' for v in b.values())
reg=data('registry')['registered_identity_members'];assert set(reg['valid_unseen_consumed_G1'])=={v[0] for v in b.values()}
identity=set()
for v in reg.values():
 if isinstance(v,list):identity.update(v)
games=set();trajectories=set()
for t,sp,h in a.values():identity.add(t);games.add(h)
for x in data('eval')['rows']:identity.add(x['task_id'])
for x in data('eval_bind'):games.add(x['game']['sha256']);trajectories.add(x['traj_data']['sha256'])
for key in ('sft','sft_ext'):
 for rows in data(key)['pools'].values():
  for x in rows:
   identity.add(x['task_id']);games.add(x.get('source_game_sha256'));trajectories.add(x.get('source_traj_data_sha256'))
for key in ('probe1','probe2'):
 x=data(key)['candidate'];identity.add(x['task_id']);games.add(x['game']['sha256']);trajectories.add(x['traj_data']['sha256'])
expert_ids=set()
with F['expert'].open() as f:
 for line in f:
  x=json.loads(line);expert_ids.add(x['task_id']);games.add(x['source_game_sha256']);trajectories.add(x['source_traj_data_sha256'])
identity.update(expert_ids)
protected={parent(x) for x in identity};protected.update(data('b')['task_exposures']);protected.update(data('c')['task_exposures'])
reserved={x['identity'] for x in data('proposal')['rows']}; allparents=protected|{parent(x) for x in reserved}; allident=identity|reserved
for split in ('train','valid_train','valid_seen','valid_unseen'):
 for p in (D/split).iterdir():
  if not p.is_dir() or p.name not in allparents:continue
  for t in p.iterdir():
   if not t.is_dir():continue
   for name,store in [('game.tw-pddl',games),('traj_data.json',trajectories)]:
    file=t/name
    if file.is_file():store.add(sha(file))
with zipfile.ZipFile(F['oldzip']) as old,zipfile.ZipFile(F['newzip']) as new:
 oldnames={x.filename for x in old.infolist() if not x.is_dir()};newnames={x.filename for x in new.infolist() if not x.is_dir()}
 assert len(oldnames)==5234 and len(oldnames-newnames)==1207
 for name in oldnames:
  pieces=Path(name).parts;assert len(pieces)==5 and pieces[-1]=='game.tw-pddl'
  split,p,t=pieces[1:4]
  if p in allparents or p+'/'+t in allident:
   with old.open(name) as file:games.add(sha_bytes(file))
 archive=[]
 eligible={'look_at_obj_in_light','pick_and_place_simple','pick_clean_then_place_in_recep','pick_cool_then_place_in_recep','pick_heat_then_place_in_recep','pick_two_obj_and_place'}
 for name in oldnames-newnames:
  _,split,p,t,_=Path(name).parts;td=D/split/p/t/'traj_data.json';gf=D/split/p/t/'game.tw-pddl'
  if p.split('-')[0] not in eligible or gf.exists() or not td.is_file() or p in allparents or p+'/'+t in allident:continue
  with old.open(name) as file:g=sha_bytes(file)
  if g in games or sha(td) in trajectories:continue
  archive.append((split,p))
local=[(x['split'],x['parent']) for x in data('local')['rows'] if x['parent'] not in allparents and x['task'] not in allident and x['game'] not in games and x['traj'] not in trajectories]
assert len(archive)==950 and len({p for s,p in archive})==345 and len(local)==17 and len({p for s,p in local})==6
allcandidate={p for s,p in archive+local}; bysplit=defaultdict(set)
for s,p in archive+local:bysplit[s].add(p)
category={'expert_dataset_source':{suffix(parent(x)) for x in expert_ids},'b_c_materialized_source':{suffix(x) for key in ('b','c') for x in data(key)['task_exposures']},'si_u1_schedule':{suffix(parent(x['task_id'])) for x in data('eval')['rows']},'g1_actual':{suffix(parent(v[0])) for v in b.values()}}
union=set().union(*category.values())
counts={k:sum(suffix(p) in v for p in allcandidate) for k,v in category.items()}
counts['union']=sum(suffix(p) in union for p in allcandidate)
valid=bysplit['valid_unseen'];vcounts={k:sum(suffix(p) in v for p in valid) for k,v in category.items()}
# Test suffix semantics only on earlier SFT-candidate source trajectories; never open current candidate contents.
check=defaultdict(int)
for rows in data('sft')['pools'].values():
 for x in rows:
  doc=json.loads((D/'train'/x['task_id']/'traj_data.json').read_text());num=doc['scene']['scene_num']; floor=doc['scene']['floor_plan'];check['historical_rows']+=1;check['suffix_matches_scene_num']+=suffix(parent(x['task_id']))==num;check['floorplan_matches_num']+=str(floor).lower()==('floorplan'+str(num)).lower()
result={'scope':'independent archive metadata+hash recount; no candidate task content inspected, no model/CUDA/ALFWorld','input_sha256':H,'g1_actual':{'raw_rows':len(b),'matched_by_index_task_split_game':len(a),'manifest_hash_bindings_match':True,'actual_ids_match_registry':True,'unique_parents':len({parent(v[0]) for v in b.values()})},'candidate':{'old_archive_added_rows':len(archive),'old_archive_parents':len({p for s,p in archive}),'local_rows':len(local),'local_parents':len({p for s,p in local}),'union_parents':len(allcandidate),'unseen_parents':len(valid)},'union_parent_suffix_overlap':counts,'unseen_parent_suffix_overlap':vcounts,'historical_sft_candidate_suffix_check':dict(check),'limitations':['Integer suffix is an operational proxy, supported by old training rows only; equal suffix is not verified geometry, individual exposure, leakage, or task outcome.','Source materialization, actual schedule execution, candidate pool, and reservation are different evidence classes.','Candidate content was hashed as bytes only, not parsed.','G1 raw index/task/split/game matched the accepted run and bound schedule; does not prove other historical activities are fully captured.']}
assert H=={k:sha(v) for k,v in F.items()}
(O/'INDEPENDENT_SCENE_RECOUNT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:result[k] for k in ('g1_actual','candidate','union_parent_suffix_overlap','unseen_parent_suffix_overlap','historical_sft_candidate_suffix_check')},indent=2))
