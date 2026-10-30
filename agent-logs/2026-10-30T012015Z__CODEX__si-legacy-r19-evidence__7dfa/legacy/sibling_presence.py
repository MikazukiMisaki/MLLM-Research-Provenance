#!/usr/bin/env python3
from pathlib import Path
import zipfile,json,hashlib
D=Path('/home/lizening/alfworld_data/json_2.1.1');O=Path('/tmp/si-official-archive-audit-20261029/0.2.2.zip');N=Path('/tmp/si-official-archive-audit-20261029/0.4.0.zip')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  while b:=f.read(1048576):h.update(b)
 return h.hexdigest()
hashes={str(p):sha(p) for p in (O,N)}
assert list(hashes.values())==['d376c4bbb097c068528a2a9805e358e4cd14bc75c4d68a24e5141aebd234ef67','eea90499df27b9cb3147d1d1927264146d38194b575e25f70a82875545742dcb']
with zipfile.ZipFile(O) as a,zipfile.ZipFile(N) as b:
 extra={x.filename for x in a.infolist() if not x.is_dir()}-{x.filename for x in b.infolist() if not x.is_dir()}
 vals=[]
 for x in extra:
  pieces=Path(x).parts;assert len(pieces)==5 and pieces[0]=='json_2.1.1' and pieces[-1]=='game.tw-pddl'
  _,split,parent,trial,_=pieces;p=D/split/parent/trial;vals.append((parent,(p/'traj_data.json').is_file(),(p/'game.tw-pddl').is_file(),p.is_dir()))
 assert len(vals)==1207
 parents={p for p,t,g,d in vals};present={p for p,t,g,d in vals if t}
 assert all(t and d and not g for p,t,g,d in vals) and len(parents)==556 and parents==present
assert hashes=={str(p):sha(p) for p in (O,N)}
print(json.dumps({'old_only_trial_paths':len(vals),'distinct_parent_names':len(parents),'local_sibling_trajectory_present':sum(t for p,t,g,d in vals),'local_game_present':sum(g for p,t,g,d in vals),'local_trial_directory_present':sum(d for p,t,g,d in vals),'parents_with_local_trajectory_sibling':len(present),'input_sha256':hashes,'limitation':'Presence only, not byte/version alignment, execution or prior exposure; no task text or outcomes read.'},indent=2,sort_keys=True))
