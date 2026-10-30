#!/usr/bin/env python3
"""Hash-bound read-only R19 event ordering audit; outputs only aggregate metadata."""
from pathlib import Path
from collections import Counter
import hashlib,json
root=Path('/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime')
dirs=list(root.glob('r19_b1_g3_successor*'));assert len(dirs)==1
p=dirs[0]/'execution_events.jsonl';b=dirs[0]/'branches.jsonl'
expected_events='05e1d443ff304eaa25d08b92a4e19d204a6c93a4f46bbe50aefef3271f211762';expected_branches='eff9b5e74d3d5daa928cb662dcc59fc3f434f66796b673679d40b374f3c8636f'
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
assert digest(p)==expected_events and digest(b)==expected_branches
rows=[json.loads(x) for x in b.open()];elig={x['prefix_id'] for x in rows if x['eligible_primary']}; assert len(elig)==36
sources=[];attempts=[];freezes={};gens=[];by_prefix={};last=-1
with p.open() as f:
 for line in f:
  e=json.loads(line);seq=e['sequence'];assert isinstance(seq,int) and seq>last;last=seq;k=e['kind'];i=e['identity']; prefix=i.get('prefix_id')
  if k=='source_episode_completed':sources.append(seq)
  if k=='prefix_attempt_completed':attempts.append(seq)
  if k in {'candidate_queues_frozen','enrollment_frozen'}:
   assert k not in freezes;freezes[k]=(seq,e['payload'])
  if k=='generation_started':gens.append((seq,i.get('component'),i.get('stage_two_attempt')))
  if prefix in elig and k in ('recovery_path_extension_completed','duration_arm_started'):
   by_prefix.setdefault(prefix,{}).setdefault(k,[]).append(seq)
q,qp=freezes['candidate_queues_frozen'];en,ep=freezes['enrollment_frozen'];assert max(sources)<q<min(attempts)<=max(attempts)<en
assert len(sources)==127 and len(attempts)==39 and ep['attempted_prefix_count']==39 and ep['additional_stage_two_generations_before_freeze']==0
assert qp['no_quota_transfer'] is True
in_between=Counter((component,attempt) for seq,component,attempt in gens if q<seq<en)
assert in_between=={('stage1',None):39,('stage2',1):39}
assert len(by_prefix)==36
for rr in by_prefix.values():
 assert len(rr.get('recovery_path_extension_completed',[]))==1 and len(rr.get('duration_arm_started',[]))==5
 assert rr['recovery_path_extension_completed'][0]<min(rr['duration_arm_started'])
assert digest(p)==expected_events and digest(b)==expected_branches
out={'status':'PASS_HASH_BOUND_EVENT_ORDER_ONLY_NOT_FULL_VALIDATION','event_sha256':expected_events,'branch_sha256':expected_branches,'source_episodes_completed_before_queues':len(sources),'candidate_queues_frozen_sequence':q,'attempts_completed_before_enrollment_freeze':len(attempts),'enrollment_frozen_sequence':en,'stage1_generations_between_freezes':in_between[('stage1',None)],'first_stage2_generations_between_freezes':in_between[('stage2',1)],'additional_stage2_generations_between_freezes':sum(v for (c,a),v in in_between.items() if c=='stage2' and a!=1),'eligible_prefixes_with_extension_completed_before_all_k_arms':len(by_prefix),'maximum_sequence':last,'limits':'Checks retained event order and selected fields; not an independent full journal chain/producer completeness audit or evidence of no historical exposure.'}
Path(__file__).with_name('EVENT_ORDER_RECOUNT.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps(out,sort_keys=True))
