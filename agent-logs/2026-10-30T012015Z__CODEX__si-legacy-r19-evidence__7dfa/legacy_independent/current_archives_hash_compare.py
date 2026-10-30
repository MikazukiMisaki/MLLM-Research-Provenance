#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,zipfile
x=Path('/tmp/si-official-archive-audit-20261029/0.4.0.zip');y=Path('/tmp/si-official-archive-audit-20261030-042/0.4.2.zip')
def hstream(f):
 h=hashlib.sha256()
 for block in iter(lambda:f.read(262144),b''):h.update(block)
 return h.hexdigest()
def hd(path):
 with path.open('rb') as f:return hstream(f)
before=[hd(x),hd(y)];assert before==['eea90499df27b9cb3147d1d1927264146d38194b575e25f70a82875545742dcb','5df77ea759f2211a4106082839ddbbb790f1ba4e7d097ed732cf453f72aa36cf']
with zipfile.ZipFile(x) as a,zipfile.ZipFile(y) as b:
 ax={i.filename for i in a.infolist() if not i.is_dir()};by={i.filename for i in b.infolist() if not i.is_dir()};assert ax==by and len(ax)==4027
 changed=0
 for n in ax:
  with a.open(n) as f,b.open(n) as g:changed+=hstream(f)!=hstream(g)
assert before==[hd(x),hd(y)] and changed==334
out={'status':'PASS_SAME_PATHS_BYTES_ONLY','shared_game_members':len(ax),'different_sha256':changed,'equal_sha256':len(ax)-changed,'archive_sha256':before,'limit':'Hash-only comparison; no interpretation of individual task bodies, histories or behavior.'}
Path(__file__).with_name('CURRENT_ARCHIVES_HASH_RECOUNT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,sort_keys=True))
