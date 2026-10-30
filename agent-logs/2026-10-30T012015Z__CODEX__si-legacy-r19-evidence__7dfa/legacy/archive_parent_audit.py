#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import hashlib,json,zipfile
P={'022':Path('/tmp/si-official-archive-audit-20261029/0.2.2.zip'),'040':Path('/tmp/si-official-archive-audit-20261029/0.4.0.zip'),'042':Path('/tmp/si-official-archive-audit-20261030-042/0.4.2.zip')}
W={'022':'d376c4bbb097c068528a2a9805e358e4cd14bc75c4d68a24e5141aebd234ef67','040':'eea90499df27b9cb3147d1d1927264146d38194b575e25f70a82875545742dcb','042':'5df77ea759f2211a4106082839ddbbb790f1ba4e7d097ed732cf453f72aa36cf'}
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  while b:=f.read(1024*1024):h.update(b)
 return h.hexdigest()
assert {k:digest(p) for k,p in P.items()}==W
D={}
for tag,path in P.items():
 with zipfile.ZipFile(path) as z:
  files=[x.filename for x in z.infolist() if not x.is_dir()]
  assert len(files)==len(set(files)) and all(len(Path(x).parts)==5 and Path(x).parts[0]=='json_2.1.1' and Path(x).name=='game.tw-pddl' for x in files)
  D[tag]=set(files)
assert len(D['022'])==5234 and len(D['040'])==len(D['042'])==4027
assert D['040']==D['042'] and D['040']<=D['022']
extra=D['022']-D['040'];assert len(extra)==1207
universe={(Path(p).parts[1],Path(p).parts[2]) for p in D['040']}
uni_name={p for s,p in universe}
by={}
for split in ['train','valid_seen','valid_unseen','valid_train']:
 members=[p for p in extra if Path(p).parts[1]==split]
 parents={Path(p).parts[2] for p in members}
 same={p for p in parents if (split,p) in universe};anysplit=parents&uni_name
 by[split]={'old_only_trial_paths':len(members),'old_only_parent_names':len(parents),'parent_names_with_current_game_same_split':len(same),'parent_names_without_current_game_same_split':len(parents-same),'parent_names_with_current_game_any_split':len(anysplit),'parent_names_without_current_game_any_split':len(parents-anysplit)}
allparents={Path(p).parts[2] for p in extra}; all_same={(Path(p).parts[1],Path(p).parts[2]) for p in extra};
assert {k:digest(p) for k,p in P.items()}==W
out={'archive_sha256':W,'old_only_trials':len(extra),'old_only_parent_names_distinct_across_splits':len(allparents),'old_only_split_parent_pairs':len(all_same),'parents_already_current_archive_any_split':len(allparents&uni_name),'parents_absent_current_archive_any_split':len(allparents-uni_name),'by_split':by,'limitation':'New relative to game-member parent names only; every old-only trial has a local metadata sibling according to prior audit; no claim of unexposed, runnable, new scene/layout, or independent unit. No archive member content parsed or emitted.'}
print(json.dumps(out,indent=2,sort_keys=True))
