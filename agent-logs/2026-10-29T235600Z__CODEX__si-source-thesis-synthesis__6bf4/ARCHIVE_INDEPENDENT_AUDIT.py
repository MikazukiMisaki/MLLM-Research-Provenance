import collections,hashlib,json,pathlib,zipfile
root=pathlib.Path('/tmp/si-official-archive-audit-20261029');data=pathlib.Path('/home/lizening/alfworld_data')
paths={ '0.2.2':root/'0.2.2.zip',
 '0.2.2-old':root/'0.2.2-old.zip',
 '0.4.0':root/'0.4.0.zip'}
def hashfile(f):
 h=hashlib.sha256()
 for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def archive_hash(p):
 with p.open('rb') as f:return hashfile(f)
archives={};filehash={key:archive_hash(p) for key,p in paths.items()}; summary={}
for label,p in paths.items():
 games={}; n=0; dupe=0; bad=0;split=collections.Counter()
 with zipfile.ZipFile(p,'r') as z:
  for e in z.infolist():
   if e.is_dir():continue
   x=pathlib.PurePosixPath(e.filename)
   if len(x.parts)!=5 or x.parts[0]!='json_2.1.1' or x.name!='game.tw-pddl' or '..' in x.parts:
    bad+=1;continue
   n+=1;key=x.as_posix();dupe+=key in games
   with z.open(e) as s:digest=hashfile(s)
   games[key]=digest;split[x.parts[1]]+=1
 archives[label]=games;summary[label]={'sha256':filehash[label],'member_count':n,'unique_member_paths':len(games),'duplicate_member_paths':dupe,'unexpected_files':bad,'split_counts':dict(split)}
assert all(v['duplicate_member_paths']==0 and v['unexpected_files']==0 for v in summary.values())
installed={p.relative_to(data).as_posix():p for p in (data/'json_2.1.1').glob('*/*/*/game.tw-pddl') if p.is_file()}
current=archives['0.4.0'];existing=set(installed);official=set(current)
matching=0;bad=0
for name in existing & official:
 with installed[name].open('rb') as f: digest=hashfile(f)
 if digest==current[name]:matching+=1
 else:bad+=1
extra=set(archives['0.2.2'])-official
extra_split=collections.Counter();parents=collections.defaultdict(set);trajectory=collections.Counter()
for name in extra:
 p=pathlib.PurePosixPath(name);sp=p.parts[1];extra_split[sp]+=1;parents[sp].add(p.parts[2]);local=data.joinpath(*p.parts)
 if local.with_name('traj_data.json').is_file():trajectory[sp]+=1
pair={}
for one,two in [('0.2.2','0.2.2-old'),('0.2.2','0.4.0')]:
 a,b=archives[one],archives[two];shared=set(a)&set(b);same=sum(a[k]==b[k] for k in shared)
 pair[one+'__'+two]={'shared':len(shared),'only_first':len(set(a)-set(b)),'only_second':len(set(b)-set(a)),'same_digest':same,'different_digest':len(shared)-same}
assert filehash=={key:archive_hash(p) for key,p in paths.items()}
out={'scope':'independent read-only zip streaming and local game byte hash, no archive extraction, task content/output or env/model/CUDA','archives':summary,'installed_vs_040':{'local_count':len(existing),'archive_count':len(official),'shared_paths':len(existing&official),'local_only':len(existing-official),'archive_only':len(official-existing),'same_sha256':matching,'different_sha256':bad},'older_only':{'member_count':len(extra),'by_split':dict(extra_split),'distinct_parent_by_split':{k:len(v) for k,v in parents.items()},'has_local_trajectory_file_by_split':dict(trajectory)},'pairwise':pair,'limits':['Version compatibility, game solvability and historical or semantic exposure were not tested.','Upstream release API digest was null; computed hashes identify downloaded bytes, not an official published checksum.','Parent counts by split not deduplicated across splits or checked against historical usage.','No inference that old-only members are eligible or that original absent files are recoverable in current treatment.']}
print(json.dumps(out,indent=2,sort_keys=True))
