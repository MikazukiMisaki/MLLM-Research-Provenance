import hashlib,json,pathlib
P=pathlib.Path
R=P('/home/lizening/wt-codex-r18c2')
G=P('/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/validation/sft-valid-unseen-g1-20260829T031028Z')
L=P('/home/lizening/research-notes/agent-logs/2026-10-29T115700Z__SOL__si-pilot82-dataset-materialization')
T=P('/home/lizening/research-notes/agent-logs/2026-10-29T125500Z__SOL__si-pilot82-bc-authorization-drafts__9bbaa/run_parent')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
gfiles={'g1_schedule':R/'configs/evaluation/sft_heldout_valid_unseen_schedule.json','g1_manifest':G/'run_manifest.json','g1_trajectory':G/'trajectories.jsonl'}
hash0={k:sha(v) for k,v in gfiles.items()}; sch=read(gfiles['g1_schedule']);manifest=read(gfiles['g1_manifest'])
byid={r['schedule_index']:r for r in sch['episodes']}; actual=[]
with gfiles['g1_trajectory'].open() as f:
 for line in f:
  x=json.loads(line); actual.append((x['metadata']['schedule_index'], x['task']['task_id'],x['task']['split'], x['metadata']['source_game_sha256']))
assert len(byid)==60==len(actual)==manifest['accepted_episodes']
assert len({i for i,_,_,_ in actual})==60
assert hash0['g1_schedule']==manifest['schedule_sha256'] and hash0['g1_trajectory']==manifest['trajectory_sha256']
assert all((byid[i]['task_id'],byid[i]['split'],byid[i]['source_game_sha256'])==(task,split,game) for i,task,split,game in actual)
assert all(split=='valid_unseen' for _,_,split,_ in actual)
assert {k:sha(v) for k,v in gfiles.items()}==hash0
out={'g1':{'sha256':hash0,'actual_rows':len(actual),'actual_unique_parents':len({task.split('/')[0] for _,task,_,_ in actual}),'manifest_bound_schedule_and_trajectory':True,'actual_index_id_split_game_match':True},'training':{}}
for arm in 'BC':
 manifest_path=L/(arm+'_manifest_candidate_PRIVATE.json'); m=read(manifest_path); dataset=P(m['dataset']['path']);parent=next(x for x in T.glob(arm+'_run_*') if x.is_dir()); result=parent/'training'/'training_result.json';exitf=parent/'supervisor_exit.json'; files={'manifest':manifest_path,'dataset':dataset,'result':result,'supervisor_exit':exitf}; sh={k:sha(v) for k,v in files.items()};r=read(result);e=read(exitf)
 assert sh['dataset']==m['dataset']['sha256'] and sh['manifest']==r['manifest_sha256'] and sh['result']==e['training_result_sha256']; assert r['status']=='COMPLETED' and e['authentic_returncode']==0;assert r['counts']['microbatches_completed']==1248;assert len(m['task_exposures'])==78
 assert {k:sha(v) for k,v in files.items()}==sh
 out['training'][arm]={'sha256':sh,'manifest_to_completed_result_bound':True,'supervisor_returncode':e['authentic_returncode'],'completed_microbatches':r['counts']['microbatches_completed'],'manifest_parents':len(m['task_exposures'])}
out['limits']=['Bindings verify recorded runs and manifest identities, not model internals or actual individual sample presentations independently of counters.','Scene suffix equality is not scene geometry equivalence or individual model exposure.']
print(json.dumps(out,sort_keys=True,indent=2))
