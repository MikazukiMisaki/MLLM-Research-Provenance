from pathlib import Path
import hashlib, json, re, zipfile
from collections import defaultdict
N=Path('/home/lizening/research-notes/agent-logs');R=Path('/home/lizening/wt-codex-r18c2');D=Path('/home/lizening/alfworld_data/json_2.1.1');P=Path('/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime');O=Path(__file__).parent
F={'oldzip':Path('/tmp/si-official-archive-audit-20261029/0.2.2.zip'),'newzip':Path('/tmp/si-official-archive-audit-20261029/0.4.0.zip'),'registry':N/'2026-10-25T065200Z__LUNA__si-p1-isolation-budget__caae4c/KNOWN_USE_IDENTITIES.json','sft':R/'configs/sft/sft_task_splits.json','sft_ext':R/'configs/sft/sft_pick_two_balance_extension.json','expert':P/'sft-policy-bootstrap/sft_expert_dataset_balanced.jsonl','eval':N/'2026-10-29T113523Z__ASTRA__three-arm-prospective-design__a55d1af9/PILOT82_PROPOSED_SCHEDULE_PRIVATE.json','eval_bind':N/'2026-10-29T120900Z__SOL__si-pilot82-game-byte-isolation/EVAL_BYTE_BINDINGS_PRIVATE.json','b':N/'2026-10-29T115700Z__SOL__si-pilot82-dataset-materialization/B_manifest_candidate_PRIVATE.json','c':N/'2026-10-29T115700Z__SOL__si-pilot82-dataset-materialization/C_manifest_candidate_PRIVATE.json','proposal':N/'2026-10-25T084517Z__LUNA__si-p3-isolation-budget-design__si3_7d91/partition_proposal.json','probe1':N/'2026-10-29T121500Z__CODEX__si-eval-engineering-task-metadata/ENGINEERING_CANDIDATE_PRIVATE.json','probe2':N/'2026-10-29T132000Z__LUNA__si-eval-remediation-candidate__metadata/ENGINEERING_CANDIDATE_PRIVATE.json','g1':R/'configs/evaluation/sft_heldout_valid_unseen_schedule.json','g1manifest':P/'validation/sft-valid-unseen-g1-20260829T031028Z/run_manifest.json','g1raw':P/'validation/sft-valid-unseen-g1-20260829T031028Z/trajectories.jsonl','curzip':Path('/tmp/si-official-archive-audit-20261030-042/0.4.2.zip'),'local':N/'2026-10-29T231522Z__CODEX__si-next-data-isolation-readonly__f2a1/CANDIDATE_METADATA_PRIVATE.json'}
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
b_g1={}
with F['g1raw'].open() as f:
 for line in f:
  x=json.loads(line); index=x['metadata']['schedule_index'];assert index not in b_g1
  b_g1[index]=(x['task']['task_id'],x['task']['split'],x['metadata']['source_game_sha256'])
assert len(a)==len(b_g1)==60 and gm['accepted_episodes']==60 and a==b_g1 and all(v[1]=='valid_unseen' for v in b_g1.values())
reg=data('registry')['registered_identity_members'];assert set(reg['valid_unseen_consumed_G1'])=={v[0] for v in b_g1.values()}
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

assert H['curzip']=='5df77ea759f2211a4106082839ddbbb790f1ba4e7d097ed732cf453f72aa36cf'
def archive_games(archive):
 output={}
 for i in archive.infolist():
  if i.is_dir():continue
  p=Path(i.filename);parts=p.parts
  assert len(parts)==5 and parts[0]=='json_2.1.1' and parts[-1]=='game.tw-pddl' and i.filename not in output
  with archive.open(i) as stream:output[i.filename]=sha_bytes(stream)
 return output
with zipfile.ZipFile(F['oldzip']) as old,zipfile.ZipFile(F['newzip']) as v040,zipfile.ZipFile(F['curzip']) as v042:
 allversions=[archive_games(x) for x in (old,v040,v042)]
 oldgames,a,b=allversions
 assert len(oldgames)==5234 and len(a)==len(b)==4027 and set(a)==set(b)
 changed={p for p in a if a[p]!=b[p]};assert len(changed)==334
 # Protect bytes from any version when the game's identity or parent was ever protected.
 for version in allversions:
  for name,h in version.items():
   _,split,pa,tr,_=Path(name).parts
   if pa in allparents or pa+'/'+tr in allident:games.add(h)
 selected=[]
 eligible={'look_at_obj_in_light','pick_and_place_simple','pick_clean_then_place_in_recep','pick_cool_then_place_in_recep','pick_heat_then_place_in_recep','pick_two_obj_and_place'}
 reasons=defaultdict(int)
 for name in changed:
  _,split,pa,tr,_=Path(name).parts; ident=pa+'/'+tr;traj=D/split/pa/tr/'traj_data.json'
  if pa.split('-')[0] not in eligible:reasons['ineligible_family']+=1;continue
  if pa in allparents or ident in allident:reasons['protected_identity_or_parent']+=1;continue
  if b[name] in games:reasons['protected_any_version_game_sha']+=1;continue
  if not traj.is_file():reasons['local_trajectory_missing']+=1;continue
  if sha(traj) in trajectories:reasons['protected_trajectory_sha']+=1;continue
  selected.append((split,pa,tr))
assert len(changed)==sum(reasons.values())+len(selected)
actual_g1_scenes={suffix(parent(v[0])) for v in b_g1.values()}
parents_selected={pa for split,pa,tr in selected}
previous_local={x['task'] for x in data('local')['rows'] if x['parent'] not in allparents and x['task'] not in allident and x['game'] not in games and x['traj'] not in trajectories}
selected_ids={pa+'/'+tr for split,pa,tr in selected}
by=defaultdict(lambda:{'paths':0,'parents':set(),'scenes':set(),'g1_matching_parents':set()})
for split,pa,tr in selected:
 z=by[split];z['paths']+=1;z['parents'].add(pa);z['scenes'].add(suffix(pa))
 if suffix(pa) in actual_g1_scenes:z['g1_matching_parents'].add(pa)
by_split={split:{'paths':v['paths'],'parents':len(v['parents']),'suffixes':len(v['scenes']),'g1_matching_parents':len(v['g1_matching_parents'])} for split,v in by.items()}
result={'schema':'SI_042_CONSERVATIVE_VERSION_CANDIDATE_INDEPENDENT_V1','scope':'Independent version-byte inventory on protected historical identities and parents and protected game byte hashes in 0.2.2,0.4.0,0.4.2; candidate local trajectory hashed not parsed; no candidate tasks or outcomes emitted','input_sha256':H,'changed_version_paths':len(changed),'disjoint_rejection_reasons_in_declared_order':dict(reasons),'retained':{'paths':len(selected),'parents':len(parents_selected),'scene_number_suffixes':len({suffix(p) for p in parents_selected}),'parents_suffix_matching_actual_g1':sum(suffix(p) in actual_g1_scenes for p in parents_selected),'by_split':by_split,'identities_matching_previous_local':len(selected_ids & previous_local),'identities_identical_to_previous_local':selected_ids==previous_local},'g1_raw_rows_equal_manifest_and_schedule':len(b_g1),'version_byte_identity_does_not_make_new_task':True,'limitations':['Filtering considers known histories and protected proposal only; no exhaustive historical-exposure guarantee.','A parent or scene suffix is a naming proxy, not verified geometry, actual exposure, task solvability or held-out status.','Changed bytes are not an observed behavior or treatment change; eligibility and compatibility remain unproven.','No candidate body or result was inspected and no model, CUDA or environment was run.']}
assert H=={k:sha(v) for k,v in F.items()}
(O/'INDEPENDENT_042_CANDIDATE_RECOUNT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ('changed_version_paths','disjoint_rejection_reasons_in_declared_order','retained','g1_raw_rows_equal_manifest_and_schedule')},indent=2))
