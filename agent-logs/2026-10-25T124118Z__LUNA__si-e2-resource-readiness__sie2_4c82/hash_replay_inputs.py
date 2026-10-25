#!/usr/bin/env python3
"""Hash already-selected replay/config inputs; never parse task text or load an environment."""
import hashlib,json
from pathlib import Path
game=Path('/home/lizening/alfworld_data/json_2.1.1/train/pick_and_place_simple-Pencil-None-GarbageCan-316/trial_T20190907_165839_449092/game.tw-pddl')
files=[
 ('selected_historical_game',game),('selected_historical_traj_data',game.parent/'traj_data.json'),
 ('domain',Path('/home/lizening/alfworld_data/logic/alfred.pddl')),
 ('grammar',Path('/home/lizening/alfworld_data/logic/alfred.twl2')),
 ('original_active_alfworld_yaml',Path('/home/lizening/wt-r19-recovery-duration-v1/configs/local/r19_b1_g2_alfworld.yaml')),
 ('local_base_a40_yaml',Path('/home/lizening/wt-r19-recovery-duration-v1/configs/local/alfworld_base_a40.yaml')),
]
rows=[]
for label,p in files:
 if not p.is_file(): rows.append({'label':label,'path':str(p),'exists':False}); continue
 h=hashlib.sha256(); n=0
 with p.open('rb') as f:
  while True:
   b=f.read(4*1024*1024)
   if not b: break
   h.update(b); n+=len(b)
 rows.append({'label':label,'path':str(p),'exists':True,'bytes':n,'sha256':h.hexdigest()})
print(json.dumps({'schema':'SI_E2_REPLAY_INPUT_HASHES_V1','method':'Read-only byte hashing only; task trajectory input is not parsed or printed.','files':rows},sort_keys=True,separators=(',',':')))
