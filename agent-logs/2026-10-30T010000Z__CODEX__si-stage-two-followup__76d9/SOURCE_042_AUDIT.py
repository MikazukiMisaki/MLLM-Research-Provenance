"""Compare official archive path and SHA metadata only. Never emit task names/content."""
import collections,hashlib,json,pathlib,zipfile
P=pathlib.Path;data=P('/home/lizening/alfworld_data')
paths={'0.2.2':P('/tmp/si-official-archive-audit-20261029/0.2.2.zip'),'0.4.0':P('/tmp/si-official-archive-audit-20261029/0.4.0.zip'),'0.4.2':P('/tmp/si-official-archive-audit-20261030-042/0.4.2.zip')}
def digest(f):
 h=hashlib.sha256()
 while b:=f.read(1024*1024):h.update(b)
 return h.hexdigest()
def sh(p):
 with p.open('rb') as f:return digest(f)
start={k:sh(v) for k,v in paths.items()}
assert start=={'0.2.2':'d376c4bbb097c068528a2a9805e358e4cd14bc75c4d68a24e5141aebd234ef67','0.4.0':'eea90499df27b9cb3147d1d1927264146d38194b575e25f70a82875545742dcb','0.4.2':'5df77ea759f2211a4106082839ddbbb790f1ba4e7d097ed732cf453f72aa36cf'}
allgames={};sums={}
for ver,path in paths.items():
 games={};split=collections.Counter()
 with zipfile.ZipFile(path) as z:
  for ent in z.infolist():
   if ent.is_dir():continue
   rel=pathlib.PurePosixPath(ent.filename)
   if len(rel.parts)!=5 or rel.parts[0]!='json_2.1.1' or rel.name!='game.tw-pddl' or '..' in rel.parts or ent.filename in games:raise ValueError('unexpected or duplicate archive member')
   with z.open(ent) as f:games[ent.filename]=digest(f)
   split[rel.parts[1]]+=1
 allgames[ver]=games;sums[ver]={'files':len(games),'by_split':dict(split),'archive_sha256':start[ver]}
new=allgames['0.4.2'];pair={}
for ver in ('0.2.2','0.4.0'):
 a=allgames[ver];common=set(a)&set(new); identical=sum(a[x]==new[x] for x in common)
 pair[ver]={'common_paths':len(common),'new_version_only_paths':len(set(new)-set(a)),'old_version_only_paths':len(set(a)-set(new)),'shared_identical_sha256':identical,'shared_changed_sha256':len(common)-identical}
local={str(p.relative_to(data)):p for p in (data/'json_2.1.1').glob('*/*/*/game.tw-pddl') if p.is_file()};common=set(local)&set(new);identical=sum(sh(local[x])==new[x] for x in common)
changed_by_split=collections.Counter(pathlib.PurePosixPath(p).parts[1] for p in common if sh(local[p])!=new[p]);only_by_split=collections.Counter(pathlib.PurePosixPath(p).parts[1] for p in set(new)-set(local))
out={'archives':sums,'v042_vs_archive':pair,'v042_vs_local':{'common_paths':len(common),'v042_only_paths':len(set(new)-set(local)),'local_only_paths':len(set(local)-set(new)),'shared_identical_sha256':identical,'shared_changed_sha256':len(common)-identical,'v042_only_by_split':dict(only_by_split),'shared_changed_by_split':dict(changed_by_split)},'archive_inputs_unchanged':start=={k:sh(v) for k,v in paths.items()},'source':'official GitHub 0.4.2 release, API digest null; obtained archive SHA identifies downloaded bytes not vendor-signed checksum','scope':'stream archive game bytes only for SHA, local game bytes for comparison; no task content parsed, no execution, no candidate IDs emitted'}
assert out['archive_inputs_unchanged'];print(json.dumps(out,sort_keys=True,indent=2))
