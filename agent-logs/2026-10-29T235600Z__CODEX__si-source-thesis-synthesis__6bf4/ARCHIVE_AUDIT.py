import collections, hashlib, json, pathlib, zipfile
R=pathlib.Path('/tmp/si-official-archive-audit-20261029')
DATA=pathlib.Path('/home/lizening/alfworld_data')
OUT=pathlib.Path(__file__).parent
paths={'v022':R/'0.2.2.zip','v022old':R/'0.2.2-old.zip','v040':R/'0.4.0.zip'}
def digest(stream):
 h=hashlib.sha256()
 while b:=stream.read(1024*1024):h.update(b)
 return h.hexdigest()
def family(path):
 p=path.parts[-3]
 for f in ('pick_two_obj_and_place','pick_and_place_simple','pick_clean_then_place_in_recep','pick_cool_then_place_in_recep','pick_heat_then_place_in_recep','look_at_obj_in_light'):
  if p.startswith(f+'-'):return f
 return 'other'
def inspect(z):
 members={}; duplicate=0
 for info in z.infolist():
  if info.is_dir():continue
  p=pathlib.PurePosixPath(info.filename)
  if p.name!='game.tw-pddl' or len(p.parts)!=5 or p.parts[0]!='json_2.1.1' or '..' in p.parts: raise ValueError('unexpected member schema')
  if str(p) in members:duplicate+=1
  with z.open(info) as s:h=digest(s)
  members[str(p)]={'digest':h,'size':info.file_size}
 return members,duplicate
with zipfile.ZipFile(paths['v022']) as a,zipfile.ZipFile(paths['v022old']) as b,zipfile.ZipFile(paths['v040']) as c:
 archives={};dups={}
 for key,z in [('v022',a),('v022old',b),('v040',c)]:archives[key],dups[key]=inspect(z)
 results={'status':'METADATA_AND_DIGEST_AUDIT_ONLY','files':{},'pairwise':{},'old_only_missing_local':{},'notes':['member bytes are read solely to compute hashes and validate ZIP CRC, never printed or copied','aggregate counts do not establish compatible semantics, prior exposure, parent isolation, or solvability','downloaded from official GitHub releases; API supplied no published digest for these assets']}
 for name,ms in archives.items():
  split=collections.Counter();same=collections.Counter();different=collections.Counter();missing=collections.Counter();missing_but_traj=collections.Counter();missing_family=collections.Counter();sizes=[]
  for key,info in ms.items():
   rel=pathlib.PurePosixPath(key);sp=rel.parts[1];split[sp]+=1;sizes.append(info['size']);local=DATA.joinpath(*rel.parts)
   if local.is_file():
    with local.open('rb') as f:h=digest(f)
    (same if h==info['digest'] else different)[sp]+=1
   else:
    missing[sp]+=1
    if local.with_name('traj_data.json').is_file():missing_but_traj[sp]+=1;missing_family[family(rel)]+=1
  p=paths[name]
  with p.open('rb') as f:sh=digest(f)
  results['files'][name]={'local_archive_sha256':sh,'archive_size_bytes':p.stat().st_size,'members_total':len(ms),'duplicate_paths':dups[name],'members_by_split':dict(split),'local_same_by_split':dict(same),'local_different_by_split':dict(different),'local_missing_by_split':dict(missing),'local_missing_but_trajectory_present_by_split':dict(missing_but_traj),'missing_with_trajectory_family_counts':dict(missing_family),'uncompressed_member_size_range':[min(sizes),max(sizes)]}
 for one,two in [('v022','v022old'),('v022','v040')]:
  left,right=archives[one],archives[two];shared=set(left)&set(right)
  results['pairwise'][one+'__'+two]={'shared':len(shared),'shared_identical_hash':sum(left[k]['digest']==right[k]['digest'] for k in shared),'shared_different_hash':sum(left[k]['digest']!=right[k]['digest'] for k in shared),'only_left':len(set(left)-set(right)),'only_right':len(set(right)-set(left))}
 localpaths={str(p.relative_to(DATA)) for p in (DATA/'json_2.1.1').glob('*/*/*/game.tw-pddl') if p.is_file()}
 officialpaths=set(archives['v040'])
 results['local_vs_v040_path_set']={'local_total':len(localpaths),'archive_total':len(officialpaths),'intersection':len(localpaths & officialpaths),'only_local':len(localpaths-officialpaths),'only_v040':len(officialpaths-localpaths)}
 oldonly=set(archives['v022'])-set(archives['v040']);group=collections.defaultdict(lambda:collections.Counter());parent=collections.defaultdict(set)
 for key in oldonly:
  p=pathlib.PurePosixPath(key);local=DATA.joinpath(*p.parts);split=p.parts[1]
  group[split]['archive_022_only']+=1
  if not local.is_file():
   group[split]['missing_local_game']+=1
   if local.with_name('traj_data.json').is_file():
    group[split]['missing_local_game_has_trajectory']+=1;parent[split].add(p.parts[-3]);group[split]['family__'+family(p)]+=1
 results['old_only_missing_local']={k:{**dict(v),'distinct_parent_directories_missing_with_trajectory':len(parent[k])} for k,v in group.items()}
 (OUT/'ARCHIVE_METADATA_AUDIT.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
 print(json.dumps(results,indent=2,sort_keys=True))
