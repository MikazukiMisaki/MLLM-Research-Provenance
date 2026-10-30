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

# Aggregate only: use the final conservative policy materialized by the original audit loop.
import re
def scene(parent):
    m=re.fullmatch(r"[^/]+-(\d+)",parent)
    if not m: raise ValueError("unexpected parent format")
    return int(m.group(1))
assert len(a)==950 and len({x['parent'] for x in a}|{x['parent'] for x in local})==350
source=rd('initial_sft'); hist_checks=collections.Counter(); recorded_trajectory_sha={} 
for pool in source['pools'].values():
 for row in pool:
  source_file=D/'train'/row['task_id']/'traj_data.json'
  raw=source_file.read_bytes(); digest=hashlib.sha256(raw).hexdigest(); prev=recorded_trajectory_sha.setdefault(source_file, digest); assert prev==digest; doc=json.loads(raw); num=doc['scene']['scene_num']; floor=doc['scene']['floor_plan']
  hist_checks['source_rows_checked']+=1;hist_checks['suffix_matches_scene_num']+=scene(row['task_id'].split('/')[0])==num;hist_checks['scene_num_matches_floorplan']+=str(floor).lower()==('floorplan'+str(num)).lower()
assert hist_checks['source_rows_checked']==hist_checks['suffix_matches_scene_num']==hist_checks['scene_num_matches_floorplan']==1410
assert all(sh(p)==digest for p,digest in recorded_trajectory_sha.items())
source_snapshot_sha=hashlib.sha256(''.join(f'{p.relative_to(D)}\t{h}\n' for p,h in sorted(recorded_trajectory_sha.items())).encode()).hexdigest()
scenes_history={scene(p) for p in parents};scenes_reserved={scene(p) for p in resparents}
category_parents={
 'balanced_expert_source':{x.split('/')[0] for x in expert_ids},
 'b_and_c_source_materializations':set(rd('bmanifest')['task_exposures'])|set(rd('cmanifest')['task_exposures']),
 'executed_si_u1_schedule':{x['task_id'].split('/')[0] for x in rd('schedule82')['rows']},
 'executed_sft_g1_schedule':{x['task_id'].split('/')[0] for x in rd('g1_schedule')['episodes']},
 'sft_original_candidate_pools':{x['task_id'].split('/')[0] for pool in source['pools'].values() for x in pool},
 'sft_extension_candidate_pools':{x['task_id'].split('/')[0] for pool in rd('extension_sft')['pools'].values() for x in pool},
 'prior_reservation':resparents}
category_scenes={k:{scene(p) for p in v} for k,v in category_parents.items()}
used_names=['balanced_expert_source','b_and_c_source_materializations','executed_si_u1_schedule','executed_sft_g1_schedule']
used_scenes=set().union(*(category_scenes[k] for k in used_names))
def summary(rows):
 parentset={x['parent'] for x in rows}; ss={scene(p) for p in parentset}; h=ss&scenes_history;r=ss&scenes_reserved
 return {'rows':len(rows),'parents':len(parentset),'distinct_numeric_suffixes':len(ss),'distinct_suffixes_overlapping_recorded_history':len(h),'parents_overlapping_recorded_history_suffix':sum(scene(p) in scenes_history for p in parentset),'distinct_suffixes_overlapping_old_proposal':len(r),'parents_overlapping_old_proposal_suffix':sum(scene(p) in scenes_reserved for p in parentset),'parents_without_either_overlap':sum(scene(p) not in scenes_history|scenes_reserved for p in parentset),'parents_matching_each_category_suffix':{k:sum(scene(p) in ss for p in parentset) for k,ss in category_scenes.items()},'parents_matching_executed_or_training_source_suffix':sum(scene(p) in used_scenes for p in parentset)}
union={x['parent'] for x in a}|{x['parent'] for x in local}; archive_summary=summary(a); local_summary=summary(local)
by_split={}
for s in ['train','valid_train','valid_seen','valid_unseen']:
 rows=[x for x in a if x['split']==s]+[x for x in local if x['split']==s];by_split[s]=summary(rows)
out2={'schema':'SI_HISTORICAL_SCENE_SUFFIX_AUDIT_V1','input_sha256':hashes,'old_script_sha256':sh(Path('/home/lizening/research-notes/agent-logs/2026-10-29T235600Z__CODEX__si-source-thesis-synthesis__6bf4/ARCHIVE_HISTORY_AUDIT.py')),'historical_known_source_mapping_check':dict(hist_checks),'historical_source_trajectory_snapshot':{'unique_files':len(recorded_trajectory_sha),'sorted_relative_path_and_sha256_manifest_sha256':source_snapshot_sha,'individual_files_rehashed_after_read':True},'protected_metadata':{'registered_history_parents':len(parents),'registered_history_distinct_suffixes':len(scenes_history),'old_proposal_distinct_suffixes':len(scenes_reserved)},'archive_candidate_paths_not_selected':archive_summary,'local_candidate_paths_not_selected':local_summary,'union_distinct_parents':len(union),'union_distinct_suffixes':len({scene(p) for p in union}),'union_parents_overlapping_history_suffix':sum(scene(p) in scenes_history for p in union),'union_parents_overlapping_old_proposal_suffix':sum(scene(p) in scenes_reserved for p in union),'union_parents_without_either_overlap':sum(scene(p) not in scenes_history|scenes_reserved for p in union),'union_parents_matching_each_category_suffix':{k:sum(scene(p) in ss for p in union) for k,ss in category_scenes.items()},'union_parents_matching_executed_or_training_source_suffix':sum(scene(p) in used_scenes for p in union),'category_distinct_suffixes':{k:len(ss) for k,ss in category_scenes.items()},'by_split':by_split,'warnings':['Suffix mapping verified for 1410 recorded source rows only, not for candidate bodies or every historical game.','Overlap of scene number is a conservative floorplan proxy, not proof of identical gameplay/semantic layout or contamination.','No-overlap means only not in enumerated records; historical exposure, pretrained-model exposure, identity completeness, compatibility and solvability remain unknown.','Historical-protected union includes candidate and reservation lists; it must not be conflated with observed execution. Source and executed-schedule categories are reported separately.','Candidate games and trajectories were streamed as bytes for SHA256 but their content was not interpreted or emitted; candidate IDs and outcomes were not emitted or selected. No model, CUDA, environment or evaluation was run.']};assert hashes=={k:sh(v) for k,v in I.items()};print(json.dumps(out2,indent=2,sort_keys=True))
