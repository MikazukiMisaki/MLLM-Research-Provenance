from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
base=Path('/home/lizening/research-notes/agent-logs')
worktree=Path('/home/lizening/wt-si-p3-runtime-adaptation')
torch=Path('/home/lizening/miniconda3/envs/alfworld-self-improve/lib/python3.10/site-packages/torch')
run=base/'2026-10-25T133918Z__LUNA__si-e2-engineering-probe__dfc00e49_7a61/engineering_run'
identity=base/'2026-10-25T141400Z__LUNA__si-e2-cuda-identity__dfc00e49_2e79/identity_run'
paths=[worktree/'src/self_improvement/si_p3/runtime_backend.py',worktree/'src/self_improvement/si_p3/runtime_gate.py',torch/'__init__.py',torch/'cuda/__init__.py',torch/'_C/__init__.pyi',torch/'version.py',run/'engineering_events.jsonl',run/'engineering_report.json',run/'worker_gate.json',run/'supervisor_exit.json',identity/'pre_allocation_identity.json',identity/'identity_observation.json',base/'2026-10-25T124118Z__SOL__si-e2-runtime-resource-review__sie2_4c82/independent_runtime_recount.json']
bindings=[{'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]
(root/'SOURCE_BINDINGS.json').write_text(json.dumps({'schema':'SI_E2_STATIC_UUID_BINDINGS_V1','files':bindings},indent=2)+'\n')
excerpts=[]
for p,intervals in [(paths[0],[(111,148)]),(torch/'cuda/__init__.py',[(275,319),(511,527),(781,840)]),(torch/'_C/__init__.pyi',[(10784,10796)]),(torch/'version.py',[(1,9)])]:
 lines=p.read_text().splitlines()
 excerpts.append({'path':str(p),'sections':[{'start':a,'end':b,'lines':[f'{i+1}: {lines[i]}' for i in range(a-1,min(b,len(lines)))]} for a,b in intervals]})
(root/'STATIC_SOURCE_EXCERPTS.json').write_text(json.dumps(excerpts,indent=2)+'\n')
print(json.dumps({'static_files_bound':len(bindings),'torch_imports':0,'CUDA_NVML_model_env_test_calls':0,'return':'READ_ONLY_CAPTURE_COMPLETE'}))
