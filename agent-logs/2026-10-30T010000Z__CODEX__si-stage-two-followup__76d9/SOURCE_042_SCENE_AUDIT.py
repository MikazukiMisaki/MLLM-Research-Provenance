"""Reapply prior conservative identity/byte protection to changed-version local games; print aggregates only."""
import collections,contextlib,hashlib,io,json,pathlib,runpy,zipfile
P=pathlib.Path
base=P('/home/lizening/research-notes/agent-logs/2026-10-30T002244Z__SOL__si-scene-history-static__review/scene_suffix_audit.py')
new=P('/tmp/si-official-archive-audit-20261030-042/0.4.2.zip'); data=P('/home/lizening/alfworld_data')
def sh(p):return hashlib.sha256(p.read_bytes()).hexdigest()
base_sha=sh(base);new_sha=sh(new); assert new_sha=='5df77ea759f2211a4106082839ddbbb790f1ba4e7d097ed732cf453f72aa36cf'
with contextlib.redirect_stdout(io.StringIO()):ctx=runpy.run_path(str(base))
parents=ctx['parents'];reserved_parents=ctx['resparents'];ids=ctx['ids'];reserved=ctx['reserved'];trajs=ctx['trajs'][1];games=set(ctx['games'][1]); old=ctx['I']['archive_small'];assert sh(old)=='eea90499df27b9cb3147d1d1927264146d38194b575e25f70a82875545742dcb'

def sha_stream(f):
 h=hashlib.sha256()
 while b:=f.read(1048576):h.update(b)
 return h.hexdigest()
def archive(p):
 d={}
 with zipfile.ZipFile(p) as z:
  for e in z.infolist():
   if e.is_dir():continue
   x=pathlib.PurePosixPath(e.filename)
   assert len(x.parts)==5 and x.parts[0]=='json_2.1.1' and x.name=='game.tw-pddl' and e.filename not in d
   with z.open(e) as f:d[e.filename]=sha_stream(f)
 return d
n=archive(new);o=archive(old);assert set(n)==set(o) and len(n)==4027
changed=[pathlib.PurePosixPath(k) for k in n if n[k]!=o[k]];assert len(changed)==334
for key,h in n.items():
 p=pathlib.PurePosixPath(key); parent=p.parts[2]; ident=parent+'/'+p.parts[3]
 if parent in parents or parent in reserved_parents or ident in ids or ident in reserved:games.add(h)
eligible={'look_at_obj_in_light','pick_and_place_simple','pick_clean_then_place_in_recep','pick_cool_then_place_in_recep','pick_heat_then_place_in_recep','pick_two_obj_and_place'}
remaining=[]
for p in changed:
 split,parent,trial=p.parts[1:4];ident=parent+'/'+trial;traj=data.joinpath(*p.parts).with_name('traj_data.json')
 if parent.split('-')[0] not in eligible or parent in parents or parent in reserved_parents or ident in ids or ident in reserved or n[str(p)] in games or not traj.is_file() or sh(traj) in trajs:continue
 remaining.append({'parent':parent,'split':split})
scene=ctx['scene'];groups=ctx['category_scenes'];used=set().union(*(groups[k] for k in ('balanced_expert_source','b_and_c_source_materializations','executed_si_u1_schedule','executed_sft_g1_schedule')))
def summary(rows):
 ps={x['parent'] for x in rows};ss={scene(x) for x in ps}
 return {'changed_version_paths':len(rows),'parent_count':len(ps),'distinct_scene_suffixes':len(ss),'parents_matching_any_training_source_or_execution_suffix':sum(scene(p) in used for p in ps),'parents_matching_g1_suffix':sum(scene(p) in groups['executed_sft_g1_schedule'] for p in ps)}
out={'archive_sha256':new_sha,'prior_scene_audit_script_sha256':base_sha,'filter_scope':'prior conservative protected histories and proposal, candidate family, source trajectory exists, game+trajectory byte hashes not in protected sets; changed version games of protected parents added to protected game hashes; unlike old-only filter, local file is expected to exist','changed_total_paths':len(changed),'filtered_summary':summary(remaining),'by_split':{s:summary([x for x in remaining if x['split']==s]) for s in ('train','valid_train','valid_seen','valid_unseen')},'limits':['changed bytes on the same existing identity do not create a new task or prove semantic change','version-specific game compatibility and data licensing unknown','scene suffix is a name proxy and cannot prove model exposure, identical layout or held-out status','no candidate task contents interpreted, IDs emitted, task selected, environment or model run'], 'new_archive_and_prior_script_unchanged':sh(new)==new_sha and sh(base)==base_sha}
assert out['new_archive_and_prior_script_unchanged'];print(json.dumps(out,sort_keys=True,indent=2))
