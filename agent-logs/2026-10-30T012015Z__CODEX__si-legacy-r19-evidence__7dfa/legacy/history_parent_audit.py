#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,zipfile
R=Path('/home/lizening/wt-codex-r18c2');N=Path('/home/lizening/research-notes/agent-logs');P=Path('/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime')
F={'oldzip':Path('/tmp/si-official-archive-audit-20261029/0.2.2.zip'),'newzip':Path('/tmp/si-official-archive-audit-20261029/0.4.0.zip'),'registry':N/'2026-10-25T065200Z__LUNA__si-p1-isolation-budget__caae4c/KNOWN_USE_IDENTITIES.json','sft':R/'configs/sft/sft_task_splits.json','sft_ext':R/'configs/sft/sft_pick_two_balance_extension.json','expert':P/'sft-policy-bootstrap/sft_expert_dataset_balanced.jsonl','eval':N/'2026-10-29T113523Z__ASTRA__three-arm-prospective-design__a55d1af9/PILOT82_PROPOSED_SCHEDULE_PRIVATE.json','b':N/'2026-10-29T115700Z__SOL__si-pilot82-dataset-materialization/B_manifest_candidate_PRIVATE.json','c':N/'2026-10-29T115700Z__SOL__si-pilot82-dataset-materialization/C_manifest_candidate_PRIVATE.json','proposal':N/'2026-10-25T084517Z__LUNA__si-p3-isolation-budget-design__si3_7d91/partition_proposal.json','g1':R/'configs/evaluation/sft_heldout_valid_unseen_schedule.json','g1manifest':P/'validation/sft-valid-unseen-g1-20260829T031028Z/run_manifest.json','g1raw':P/'validation/sft-valid-unseen-g1-20260829T031028Z/trajectories.jsonl'}
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  while x:=f.read(1024*1024):h.update(x)
 return h.hexdigest()
def data(k):return json.loads(F[k].read_text())
def parent(i):return i.split('/')[0]
before={k:sha(v) for k,v in F.items()}
assert before['oldzip']=='d376c4bbb097c068528a2a9805e358e4cd14bc75c4d68a24e5141aebd234ef67' and before['newzip']=='eea90499df27b9cb3147d1d1927264146d38194b575e25f70a82875545742dcb'
with zipfile.ZipFile(F['oldzip']) as old, zipfile.ZipFile(F['newzip']) as new:
 a={i.filename for i in old.infolist() if not i.is_dir()};b={i.filename for i in new.infolist() if not i.is_dir()}; assert len(a-b)==1207
 candidates={Path(i).parts[2] for i in a-b}
assert len(candidates)==556
sources={}
sources['historical_registry_all_categories']={parent(i) for v in data('registry')['registered_identity_members'].values() if isinstance(v,list) for i in v}
sources['sft_initial_and_extension_candidates']={parent(x['task_id']) for k in ('sft','sft_ext') for rows in data(k)['pools'].values() for x in rows}
sources['balanced_expert_training_source']=set()
with F['expert'].open() as f:
 for line in f:sources['balanced_expert_training_source'].add(parent(json.loads(line)['task_id']))
sources['si_u1_evaluation_schedule']={parent(x['task_id']) for x in data('eval')['rows']}
sources['b_and_c_training_materializations']={x for k in ('b','c') for x in data(k)['task_exposures']}
sources['earlier_proposal_reservations']={parent(x['identity']) for x in data('proposal')['rows']}
g1=data('g1');manifest=data('g1manifest');assert before['g1']==manifest['schedule_sha256'] and before['g1raw']==manifest['trajectory_sha256'] and manifest['accepted_episodes']==60
schedule={x['schedule_index']:(x['task_id'],x['split'],x['source_game_sha256']) for x in g1['episodes']};actual={}
with F['g1raw'].open() as f:
 for line in f:
  x=json.loads(line);i=x['metadata']['schedule_index'];assert i not in actual;actual[i]=(x['task']['task_id'],x['task']['split'],x['metadata']['source_game_sha256'])
assert schedule==actual and len(actual)==60
sources['g1_manifest_bound_actual_evaluation']={parent(t) for t,split,g in actual.values()}
counts={k:len(candidates&v) for k,v in sources.items()}
known_sources=['historical_registry_all_categories','sft_initial_and_extension_candidates','balanced_expert_training_source','si_u1_evaluation_schedule','b_and_c_training_materializations','g1_manifest_bound_actual_evaluation']
known=set().union(*(sources[k] for k in known_sources));protect=known|sources['earlier_proposal_reservations']
assert before=={k:sha(v) for k,v in F.items()}
print(json.dumps({'candidate_parents':len(candidates),'sources_parent_overlap':counts,'recorded_and_possible_history_parent_overlap_union':len(candidates&known),'history_and_reserved_parent_overlap_union':len(candidates&protect),'history_and_reserved_parent_absent':len(candidates-protect),'input_sha256':before,'notes':['No byte-hash, split, family, or local-trajectory filter; overlaps are exact parent-name matches, not proof that a candidate trial was executed.','SFT manifests and prior proposal contain candidate/planned tasks, not individually proven executed or trained.','Balanced expert source and B/C materialized parent evidence do not independently prove every per-task GPU use.','Remaining parent names do not prove absence of unrecorded exposure, novel scene, game compatibility or suitability.']},indent=2,sort_keys=True))
