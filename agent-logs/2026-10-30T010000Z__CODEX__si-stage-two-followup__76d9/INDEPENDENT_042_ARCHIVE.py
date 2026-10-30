import hashlib,json,zipfile
from collections import Counter
from pathlib import Path
A=Path('/tmp/si-official-archive-audit-20261029/0.4.0.zip'); B=Path('/tmp/si-official-archive-audit-20261030-042/0.4.2.zip'); O=Path(__file__).parent
def digest_stream(f):
 h=hashlib.sha256()
 for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
def digest(p):
 with p.open('rb') as f:return digest_stream(f)
def mapgames(path):
 out={};allfiles=0
 with zipfile.ZipFile(path) as z:
  for info in z.infolist():
   if info.is_dir():continue
   allfiles+=1
   if Path(info.filename).name!='game.tw-pddl':continue
   if info.filename in out:raise ValueError('duplicate path')
   parts=Path(info.filename).parts
   if len(parts)!=5 or parts[0]!='json_2.1.1':raise ValueError('unexpected path')
   with z.open(info) as f:out[info.filename]=digest_stream(f)
 return out,allfiles
ha,hb=digest(A),digest(B);a,na=mapgames(A);b,nb=mapgames(B)
localroot=Path('/home/lizening/alfworld_data/json_2.1.1');local={}
for split in ('train','valid_train','valid_seen','valid_unseen'):
 for game in (localroot/split).glob('*/*/game.tw-pddl'):
  local['json_2.1.1/'+str(game.relative_to(localroot))]=digest(game)
common=set(a)&set(b);changed={p for p in common if a[p]!=b[p]};same=common-changed
report={'schema':'ALFWORLD_040_042_INDEPENDENT_ZIP_RECOUNT_V1','method':'Zip and local file membership and raw file SHA256 only; no archive extraction, candidate-body parsing, model, GPU, ALFWorld or gameplay.','assets':{'0.4.0':{'path':str(A),'sha256':ha,'all_non_directory_members':na,'game_members':len(a)},'0.4.2':{'path':str(B),'sha256':hb,'all_non_directory_members':nb,'game_members':len(b)}},'local_game_members':len(local),'local_only_paths':len(set(local)-set(a)),'archive_040_only_paths_vs_local':len(set(a)-set(local)),'local_matches_040':sum(local[p]==a[p] for p in set(a)&set(local)),'local_matches_042':sum(local[p]==b[p] for p in set(b)&set(local)),'common_game_paths':len(common),'only_040_game_paths':len(set(a)-set(b)),'only_042_game_paths':len(set(b)-set(a)),'same_bytes_game_paths':len(same),'different_bytes_game_paths':len(changed),'changed_by_split':dict(sorted(Counter(Path(p).parts[1] for p in changed).items())),'all_by_split':dict(sorted(Counter(Path(p).parts[1] for p in common).items())),'limits':['Raw SHA confirms byte equality/inequality only; does not establish function, semantic equivalence, suitability, historical exposure, or solvability.','No task identities or file content emitted.','Archive download authenticity relies on separately documented official release asset access; SHA identifies bytes, not an independent signed upstream checksum.']}
assert digest(A)==ha and digest(B)==hb
(O/'ARCHIVE_RECOUNT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps(report,indent=2,sort_keys=True))
