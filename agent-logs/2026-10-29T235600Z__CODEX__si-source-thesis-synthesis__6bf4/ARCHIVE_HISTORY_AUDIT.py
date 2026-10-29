import json,zipfile,hashlib,collections
from pathlib import Path
N=Path('/home/lizening/research-notes/agent-logs'); R=Path('/home/lizening/wt-codex-r18c2'); D=Path('/home/lizening/alfworld_data/json_2.1.1'); O=Path(__file__).parent
I={'archive':Path('/tmp/si-official-archive-audit-20261029/0.2.2.zip'),'archive_small':Path('/tmp/si-official-archive-audit-20261029/0.4.0.zip'),'registry':N/'2026-10-25T065200Z__LUNA__si-p1-isolation-budget__caae4c/KNOWN_USE_IDENTITIES.json','initial_sft':R/'configs/sft/sft_task_splits.json','extension_sft':R/'configs/sft/sft_pick_two_balance_extension.json','expert':Path('/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/sft-policy-bootstrap/sft_expert_dataset_balanced.jsonl'),'schedule82':N/'2026-10-29T113523Z__ASTRA__three-arm-prospective-design__a55d1af9/PILOT82_PROPOSED_SCHEDULE_PRIVATE.json','bindings82':N/'2026-10-29T120900Z__SOL__si-pilot82-game-byte-isolation/EVAL_BYTE_BINDINGS_PRIVATE.json','bmanifest':N/'2026-10-29T115700Z__SOL__si-pilot82-dataset-materialization/B_manifest_candidate_PRIVATE.json','cmanifest':N/'2026-10-29T115700Z__SOL__si-pilot82-dataset-materialization/C_manifest_candidate_PRIVATE.json','proposal':N/'2026-10-25T084517Z__LUNA__si-p3-isolation-budget-design__si3_7d91/partition_proposal.json','probe1':N/'2026-10-29T121500Z__CODEX__si-eval-engineering-task-metadata/ENGINEERING_CANDIDATE_PRIVATE.json','probe2':N/'2026-10-29T132000Z__LUNA__si-eval-remediation-candidate__metadata/ENGINEERING_CANDIDATE_PRIVATE.json','g1_schedule':R/'configs/evaluation/sft_heldout_valid_unseen_schedule.json','local_wide':N/'2026-10-29T231522Z__CODEX__si-next-data-isolation-readonly__f2a1/CANDIDATE_WITHOUT_RESERVATION_METADATA_PRIVATE.json','local_conservative':N/'2026-10-29T231522Z__CODEX__si-next-data-isolation-readonly__f2a1/CANDIDATE_METADATA_PRIVATE.json'}
def hs(f):
 h=hashlib.sha256()
 while b:=f.read(1048576):h.update(b)
 return h.hexdigest()
def sh(p):
 with p.open('rb') as f:return hs(f)
def rd(k):return json.loads(I[k].read_text())
hashes={k:sh(v) for k,v in I.items()}; assert hashes['archive']=='d376c4bbb097c068528a2a9805e358e4cd14bc75c4d68a24e5141aebd234ef67'; assert hashes['archive_small']=='eea90499df27b9cb3147d1d1927264146d38194b575e25f70a82875545742dcb'
reg=rd('registry')['registered_identity_members']; ids=set().union(*(set(v) for v in reg.values() if isinstance(v,list))); game0=set();traj0=set();
for x in rd('schedule82')['rows']:ids.add(x['task_id'])
for x in rd('g1_schedule')['episodes']:ids.add(x['task_id']);game0.add(x['source_game_sha256'])
for x in rd('bindings82'):game0.add(x['game']['sha256']);traj0.add(x['traj_data']['sha256'])
for k in ['initial_sft','extension_sft']:
 for typ,rows in rd(k)['pools'].items():
  for x in rows:
   ids.add(x['task_id']);game0.add(x.get('source_game_sha256'));traj0.add(x.get('source_traj_data_sha256'))
for k in ['probe1','probe2']:
 x=rd(k)['candidate'];ids.add(x['task_id']);game0.add(x['game']['sha256']);traj0.add(x['traj_data']['sha256'])
expert_ids=set()
with I['expert'].open() as f:
 for ln in f:
  x=json.loads(ln);expert_ids.add(x['task_id']);game0.add(x['source_game_sha256']);traj0.add(x['source_traj_data_sha256'])
ids|=expert_ids; parents={x.split('/')[0] for x in ids}
for k in ['bmanifest','cmanifest']:parents|=set(rd(k)['task_exposures'])
reserved={x['identity'] for x in rd('proposal')['rows']};resparents={x.split('/')[0] for x in reserved}
# Historical and reserved game/trajectory byte identities, including games in official archive whose historical local file is absent.
games=[set(game0),set(game0)];trajs=[set(traj0),set(traj0)]
for split in ['train','valid_train','valid_seen','valid_unseen']:
 for task in (D/split).iterdir():
  if not task.is_dir():continue
  t0=task.name in parents;t1=t0 or task.name in resparents
  if not t1:continue
  for trial in task.iterdir():
   if not trial.is_dir():continue
   for filename,stores in [('game.tw-pddl',games),('traj_data.json',trajs)]:
    f=trial/filename
    if f.is_file():
     h=sh(f);stores[1].add(h)
     if t0:stores[0].add(h)
with zipfile.ZipFile(I['archive']) as z,zipfile.ZipFile(I['archive_small']) as zsmall:
 names={x.filename for x in z.infolist() if not x.is_dir()};small={x.filename for x in zsmall.infolist() if not x.is_dir()};add=sorted(names-small)
 assert len(names)==5234 and len(add)==1207
 parsed=[]
 for name in names:
  p=Path(name);assert len(p.parts)==5 and p.parts[0]=='json_2.1.1' and p.parts[-1]=='game.tw-pddl';split,parent,trial=p.parts[1:4];ident=parent+'/'+trial
  in0=parent in parents or ident in ids;in1=in0 or parent in resparents or ident in reserved
  if in1:
   with z.open(name) as f:h=hs(f)
   games[1].add(h)
   if in0:games[0].add(h)
 for name in add:
  p=Path(name);split,parent,trial=p.parts[1:4];ident=parent+'/'+trial;traj=D/split/parent/trial/'traj_data.json';game=D/split/parent/trial/'game.tw-pddl'
  with z.open(name) as f: g=hs(f)
  th=sh(traj) if traj.is_file() else None
  parsed.append({'split':split,'parent':parent,'id':ident,'game':g,'traj':th,'local_game_exists':game.exists()})
result={}
eligible={'look_at_obj_in_light','pick_and_place_simple','pick_clean_then_place_in_recep','pick_cool_then_place_in_recep','pick_heat_then_place_in_recep','pick_two_obj_and_place'}
for k,protp,proti,j in [('recorded_and_sft_replay',parents,ids,0),('plus_old_proposal_reservation',parents|resparents,ids|reserved,1)]:
 a=[x for x in parsed if x['parent'].split('-')[0] in eligible and not x['local_game_exists'] and x['traj'] and x['parent'] not in protp and x['id'] not in proti and x['game'] not in games[j] and x['traj'] not in trajs[j]]
 local=rd('local_wide' if j==0 else 'local_conservative')['rows']; local=[x for x in local if x['parent'] not in protp and x['task'] not in proti and x['game'] not in games[j] and x['traj'] not in trajs[j]]; ap={x['parent'] for x in a};lp={x['parent'] for x in local}; ag={x['game'] for x in a}; at={x['traj'] for x in a}
 result[k]={'existing_local_rows_after_same_policy':len(local),'existing_local_parents_after_same_policy':len(lp),'archive_vs_local_parent_overlap':len(ap&lp),'archive_vs_local_game_sha_overlap':len(ag&{x['game'] for x in local}),'archive_vs_local_trajectory_sha_overlap':len(at&{x['traj'] for x in local}),'union_distinct_parents':len(ap|lp),'archive_distinct_game_hashes':len(ag),'archive_distinct_trajectory_hashes':len(at),'rows':len(a),'parents':len({x['parent'] for x in a}),'by_split':{s:{'rows':sum(x['split']==s for x in a),'parents':len({x['parent'] for x in a if x['split']==s}),'local_parents':len({x['parent'] for x in local if x['split']==s}),'archive_local_parent_overlap':len({x['parent'] for x in a if x['split']==s}&{x['parent'] for x in local if x['split']==s}),'archive_local_union_parents':len({x['parent'] for x in a if x['split']==s}|{x['parent'] for x in local if x['split']==s}),'families':dict(collections.Counter(p.split('-')[0] for p in {x['parent'] for x in a if x['split']==s}))} for s in ['train','valid_train','valid_seen','valid_unseen']},'limitations':'path+hash evidence only; no extraction; task not executed; unknown historical records, original local data version, semantic/layout identity and historical upstream model exposure'}
out={'schema':'SI_OFFICIAL_ARCHIVE_HISTORY_JOIN_V1','inputs_sha256':hashes,'archive_added_game_members':len(add),'local_missing_and_sibling_trajectory_present':sum(not x['local_game_exists'] and bool(x['traj']) for x in parsed),'baseline_and_conservative_results':result,'operation':'Metadata-only task/parent and streaming SHA256; no candidate content emitted; no environment/model/CUDA/selection','comparison_scope':'registry, full 1200 balanced expert, 1350 initial and 519 extension SFT candidate IDs, authentic 82 eval and B/C parents, two engineering probes, available local protected game/traj SHA and matching archive protected games; prior proposal reservation in second policy only','does_not_prove':'unseen layout, heldout, original archive game version, runnable state, absent unknown history, suitable power or approved experiment'}
assert hashes=={k:sh(v) for k,v in I.items()};(O/'OFFICIAL_ARCHIVE_HISTORY_JOIN.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,sort_keys=True))
