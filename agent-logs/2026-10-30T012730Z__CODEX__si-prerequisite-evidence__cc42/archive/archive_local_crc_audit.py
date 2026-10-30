#!/usr/bin/env python3
from pathlib import Path
from collections import Counter,defaultdict
import hashlib,json,zipfile,zlib
D=Path('/home/lizening/alfworld_data');stage=Path('/tmp/si-source-join-archives-20261030');games0=Path('/tmp/si-official-archive-audit-20261029/0.2.2.zip');games4=Path('/tmp/si-official-archive-audit-20261029/0.4.0.zip')
F={'json':stage/'json_2.1.1_json.zip','pddl':stage/'json_2.1.1_pddl.zip','old_game':games0,'current_game':games4}
W={'json':'25171f16e20ad7b048c47275c45b0babf3aa1cbab29cec97387922350a9844bc','pddl':'913942ebed06659ea0da2f8122512d98bc6add30d84961ca803132d8fbcad585','old_game':'d376c4bbb097c068528a2a9805e358e4cd14bc75c4d68a24e5141aebd234ef67','current_game':'eea90499df27b9cb3147d1d1927264146d38194b575e25f70a82875545742dcb'}
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  while b:=f.read(1048576):h.update(b)
 return h.hexdigest()
assert {k:sha(p) for k,p in F.items()}==W

def infos(path,basename):
 with zipfile.ZipFile(path) as z:
  allinfo=[i for i in z.infolist() if not i.is_dir()]
  chosen=[i for i in allinfo if Path(i.filename).name==basename]
  assert len(chosen)==len({i.filename for i in chosen})
  for i in chosen:
   p=Path(i.filename);assert len(p.parts)==5 and p.parts[0]=='json_2.1.1' and '..' not in p.parts and not p.is_absolute()
  return {i.filename:(i.file_size,i.CRC) for i in chosen}
old=infos(F['old_game'],'game.tw-pddl');new=infos(F['current_game'],'game.tw-pddl');assert len(old)==5234 and len(new)==4027 and set(new)<=set(old)
extra=set(old)-set(new);assert len(extra)==1207
extra_trials={str(Path(p).parent) for p in extra};local_hashes=[];out={}
for kind,basename in [('json','traj_data.json'),('pddl','initial_state.pddl')]:
 entries=infos(F[kind],basename);assert len(entries)==7080
 stats={'all':Counter(),'old_only':Counter()};splits=defaultdict(Counter)
 for name,(size,crc) in entries.items():
  p=D/name;rel=Path(name);isextra=str(rel.parent) in extra_trials;split=rel.parts[1]
  keys=[stats['all'],splits[split]]+([stats['old_only']] if isextra else [])
  for c in keys:c['archive_members']+=1
  if not p.is_file():
   for c in keys:c['local_missing']+=1
   continue
  actual=0;sz=0;hashobj=hashlib.sha256()
  with p.open('rb') as f:
   bstat0=__import__('os').fstat(f.fileno())
   while b:=f.read(1048576):actual=zlib.crc32(b,actual);sz+=len(b);hashobj.update(b)
   bstat1=__import__('os').fstat(f.fileno())
  assert (bstat0.st_size,bstat0.st_mtime_ns,bstat0.st_ino)==(bstat1.st_size,bstat1.st_mtime_ns,bstat1.st_ino)
  local_hashes.append(name+'\0'+hashobj.hexdigest())
  same=(sz==size and (actual & 0xffffffff)==crc)
  for c in keys:c['local_present']+=1;c['crc_size_match' if same else 'crc_or_size_mismatch']+=1
 out[kind]={'all':dict(stats['all']),'old_only':dict(stats['old_only']),'by_split':{s:dict(c) for s,c in sorted(splits.items())}}
assert {k:sha(p) for k,p in F.items()}==W
fingerprint=hashlib.sha256(('\n'.join(sorted(local_hashes))+'\n').encode()).hexdigest()
print(json.dumps({'counts':out,'archive_sha256_before_and_after':W,'local_path_sha_inventory_digest':fingerprint,'limits':['Read ZIP central directory only; no compressed member opened, extracted or decompressed.','Local CRC32 and size match ZIP metadata are weak evidence, not cryptographic byte verification, official digest, version identity, contemporaneous generation, or compatibility.','Local files were fstat checked during read; no separate full after-scan byte rehash.','Task texts and identifiers were not emitted.']},indent=2,sort_keys=True))
