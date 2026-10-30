#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import hashlib,json,zipfile
R=Path('/home/lizening/wt-codex-r18c2');P=Path('/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime')
F={'oldzip':Path('/tmp/si-official-archive-audit-20261029/0.2.2.zip'),'newzip':Path('/tmp/si-official-archive-audit-20261029/0.4.0.zip'),'g1':R/'configs/evaluation/sft_heldout_valid_unseen_schedule.json','manifest':P/'validation/sft-valid-unseen-g1-20260829T031028Z/run_manifest.json','trajectories':P/'validation/sft-valid-unseen-g1-20260829T031028Z/trajectories.jsonl'}
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  while data:=f.read(1048576):h.update(data)
 return h.hexdigest()
H={k:sha(v) for k,v in F.items()};assert H['oldzip']=='d376c4bbb097c068528a2a9805e358e4cd14bc75c4d68a24e5141aebd234ef67' and H['newzip']=='eea90499df27b9cb3147d1d1927264146d38194b575e25f70a82875545742dcb'
g=json.loads(F['g1'].read_text());m=json.loads(F['manifest'].read_text());assert H['g1']==m['schedule_sha256'] and H['trajectories']==m['trajectory_sha256'] and m['accepted_episodes']==60
rows={r['schedule_index']:(r['split'],r['task_id'],r['source_game_sha256']) for r in g['episodes']};actual={}
with F['trajectories'].open() as f:
 for line in f:
  a=json.loads(line);i=a['metadata']['schedule_index'];assert i not in actual;actual[i]=(a['task']['split'],a['task']['task_id'],a['metadata']['source_game_sha256'])
assert len(rows)==60 and actual==rows
changed=Counter();old_present=Counter();new_present=Counter();type_mismatch=Counter();history_bind=0;old_equals_new=0;old_parse=new_parse=0
with zipfile.ZipFile(F['oldzip']) as old,zipfile.ZipFile(F['newzip']) as new:
 for split,task_id,game_sha in rows.values():
  name='json_2.1.1/'+split+'/'+task_id+'/game.tw-pddl';oldraw=old.read(name);newraw=new.read(name)
  old_equals_new+=oldraw==newraw;history_bind+=hashlib.sha256(newraw).hexdigest()==game_sha
  o=json.loads(oldraw);n=json.loads(newraw);assert isinstance(o,dict) and isinstance(n,dict);old_parse+=1;new_parse+=1
  old_present.update(o.keys());new_present.update(n.keys())
  for key in set(o)|set(n):
   changed[key]+=o.get(key)!=n.get(key)
   type_mismatch[key]+=type(o.get(key))!=type(n.get(key))
assert H=={k:sha(v) for k,v in F.items()}
print(json.dumps({'scope':'Already-recorded historical G1 identities only; archived JSON root-field presence, type, and exact value equality in memory, no task content, IDs, outcomes or game execution emitted. These are not the 1207 old-only prospective paths.','historical_matched_episodes':len(rows),'new_archive_bytes_match_recorded_g1_game_sha':history_bind,'old_equals_new_bytes':old_equals_new,'both_root_json_decodable':old_parse==new_parse==60,'root_fields_old_presence':dict(old_present),'root_fields_new_presence':dict(new_present),'root_fields_unequal_value_counts':dict(changed),'root_fields_type_unequal_counts':dict(type_mismatch),'input_sha256':H,'limits':['Root-field differences are structural evidence only; values are not exported and semantic or operational differences are not established.','Historical common paths cannot prove runnable/solvable status or faithful conversion for old-only paths.','Old version does not match historical actual bytes merely by path.']},indent=2,sort_keys=True))
