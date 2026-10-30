#!/usr/bin/env python3
"""Read ZIP directory metadata and hash local source files; no archive members opened."""
from pathlib import Path
from collections import Counter,defaultdict
import hashlib,json,zipfile,zlib,os
zips={'trajectory':Path('/tmp/si-source-join-archives-20261030/json_2.1.1_json.zip'),'pddl':Path('/tmp/si-source-join-archives-20261030/json_2.1.1_pddl.zip'),'old_games':Path('/tmp/si-official-archive-audit-20261029/0.2.2.zip'),'current_games':Path('/tmp/si-official-archive-audit-20261029/0.4.0.zip')}
expected={'trajectory':'25171f16e20ad7b048c47275c45b0babf3aa1cbab29cec97387922350a9844bc','pddl':'913942ebed06659ea0da2f8122512d98bc6add30d84961ca803132d8fbcad585','old_games':'d376c4bbb097c068528a2a9805e358e4cd14bc75c4d68a24e5141aebd234ef67','current_games':'eea90499df27b9cb3147d1d1927264146d38194b575e25f70a82875545742dcb'}
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
assert {k:digest(p) for k,p in zips.items()}==expected
Z={}
for kind,basename in [('trajectory','traj_data.json'),('pddl','initial_state.pddl'),('old_games','game.tw-pddl'),('current_games','game.tw-pddl')]:
 with zipfile.ZipFile(zips[kind]) as a:
  entries=[i for i in a.infolist() if not i.is_dir() and Path(i.filename).name==basename]
  names=[i.filename for i in entries];assert len(names)==len(set(names))
  assert all(len(Path(n).parts)==5 and Path(n).parts[0]=='json_2.1.1' and not Path(n).is_absolute() and '..' not in Path(n).parts for n in names)
  Z[kind]={i.filename:(i.file_size,i.CRC) for i in entries}
assert len(Z['old_games'])==5234 and len(Z['current_games'])==4027 and set(Z['current_games'])<=set(Z['old_games'])
extra={str(Path(n).parent) for n in set(Z['old_games'])-set(Z['current_games'])};assert len(extra)==1207
assert {str(Path(n).parent) for n in Z['trajectory']}=={str(Path(n).parent) for n in Z['pddl']} and len({str(Path(n).parent) for n in Z['trajectory']})==7080
results={};inventory=[];localroot=Path('/home/lizening/alfworld_data')
for kind in ('trajectory','pddl'):
 assert len(Z[kind])==7080
 total=Counter();splits=defaultdict(Counter);old_only=Counter()
 for name,(want_size,want_crc) in Z[kind].items():
  path=localroot/name;split=Path(name).parts[1];extra_here=str(Path(name).parent) in extra
  buckets=[total,splits[split]]+([old_only] if extra_here else [])
  for b in buckets:b['members']+=1
  if not path.is_file():
   for b in buckets:b['missing']+=1
   continue
  h=hashlib.sha256();crc=0;size=0
  with path.open('rb') as f:
   first=os.fstat(f.fileno())
   for chunk in iter(lambda:f.read(262144),b''):size+=len(chunk);crc=zlib.crc32(chunk,crc);h.update(chunk)
   last=os.fstat(f.fileno())
  assert (first.st_ino,first.st_size,first.st_mtime_ns)==(last.st_ino,last.st_size,last.st_mtime_ns)
  inventory.append(name+'\0'+h.hexdigest())
  ok=(size==want_size and (crc & 0xffffffff)==want_crc)
  for b in buckets:b['local_present']+=1;b['crc_size_match' if ok else 'crc_or_size_mismatch']+=1
 assert total['members']==total['local_present']==total['crc_size_match']==7080
 assert old_only['members']==old_only['local_present']==old_only['crc_size_match']==1207
 results[kind]={'total':dict(total),'old_only':dict(old_only),'by_split':{k:dict(v) for k,v in sorted(splits.items())}}
assert {k:digest(p) for k,p in zips.items()}==expected
inv=hashlib.sha256(('\n'.join(sorted(inventory))+'\n').encode()).hexdigest()
assert inv=='e60d28a4715f992c1ca85cbc11e77f855fe46b6af8e9ff9a75f69582275d1333'
out={'status':'PASS_CENTRAL_DIRECTORY_CRC_SIZE_COMPARISON_ONLY','archive_sha256':expected,'counts':results,'local_path_sha_inventory_digest':inv,'limits':['ZIP central directories only; compressed archive members were not opened or checked against stored CRC.','CRC32+length are not cryptographic identity; hash of downloaded ZIP is not an upstream authenticated digest.','Local hash inventory does not compare individual archive member SHA256; no historical generation event, compatibility, eligibility or task independence established.','Local fstat stability during reads, not full after-scan per-file rehash.']}
Path(__file__).with_name('INDEPENDENT_CRC_RECOUNT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,sort_keys=True))
