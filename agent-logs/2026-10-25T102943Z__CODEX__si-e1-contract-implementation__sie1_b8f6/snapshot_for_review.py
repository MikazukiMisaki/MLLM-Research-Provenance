from pathlib import Path
import ast,hashlib,json,subprocess
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
ROOT=Path('/home/lizening/wt-si-p3-engineering-contracts');BASE='85cbb92395e5e2420c2adeb1fa0634653e742910';FROZEN='a995d4c3c5f7d31a2cf1fd0afc4bfa4bd72ee3a3'
def git(*args,cwd=ROOT):
 p=subprocess.run(['git',*args],cwd=cwd,capture_output=True);assert p.returncode==0,p.stderr;return p.stdout
assert git('rev-parse','HEAD').decode().strip()==FROZEN
assert not git('status','--porcelain')
assert git('rev-parse','HEAD^').decode().strip()==BASE
names=git('diff','--name-status',BASE,FROZEN).decode().splitlines();assert len(names)==17 and all(x.startswith('A\t') for x in names)
for name,args in [('full_delta.patch',['diff','--binary',BASE,FROZEN]),('full_delta.stat',['diff','--stat',BASE,FROZEN]),('full_delta.name_status',['diff','--name-status',BASE,FROZEN])]:
 (OWN/name).write_bytes(git(*args))
methods=[]
files={}
for entry in names:
 p=ROOT/entry.split('\t')[1];b=p.read_bytes();files[str(p.relative_to(ROOT))]={'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
 if p.suffix!='.py':continue
 tree=ast.parse(b)
 def visit(node,prefix=''):
  for child in ast.iter_child_nodes(node):
   if isinstance(child,(ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef)):
    qual=prefix+child.name
    methods.append({'file':str(p.relative_to(ROOT)),'name':qual,'kind':type(child).__name__,'line':child.lineno,'AST_sha256':hashlib.sha256(ast.dump(child,include_attributes=False).encode()).hexdigest()})
    visit(child,qual+'.')
   else:visit(child,prefix)
 visit(tree)
(OWN/'NEW_METHODS_AND_FILES.json').write_text(json.dumps({'frozen_sha':FROZEN,'base_sha':BASE,'all_old_methods_changed':[],'only_added_files':files,'definitions':methods},indent=2)+'\n')
oldnames=['AGENTS.md','PROJECT.md','PAPER_PROPOSAL.md','EXPERIMENT_PLAN.md','IMPLEMENTATION_PHASES.md','reports/SPRINT_1_5_FINAL.md','configs/sft/sft_run_config.json','configs/sft/sft_training_protocol.json','configs/sft/sft_accepted_task_splits.json','configs/experiments/r19_recovery_duration_v1.json','src/sft/protocol.py','src/sft/policy.py','src/sft/masking.py','src/sft/training.py','src/sft/environment.py','src/models/protocol_stability.py','src/recovery/two_stage.py','src/recovery/two_stage_v2.py','src/recovery/r19_duration.py','scripts/run_r19_experiment.py','scripts/analyze_r19_recovery_duration.py','scripts/launch_r19_supervised.py']
bindings=[]
for name in oldnames:
 original=git('show',BASE+':'+name);current=(ROOT/name).read_bytes();assert current==original,name
 bindings.append({'path':str(ROOT/name),'frozen_git_object_sha256':hashlib.sha256(original).hexdigest(),'current_sha256':hashlib.sha256(current).hexdigest(),'unchanged':True})
phase3=Path('/home/lizening/research-notes/agent-logs/2026-10-25T084517Z__SOL__si-p3-controlled-experience-design__si3_7d91')
coordinator=Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__SOL__si-e1-engineering-review__sie1_b8f6')
for p in [phase3/'MINIMAL_CONTROLLED_EXPERIENCE_PROTOCOL.md',phase3/'phase3_independent_review.json',phase3/'ADOPTED_METADATA_RESERVATIONS.json',coordinator/'COMMON_ENGINEERING_CONTRACT.md',coordinator/'DRAFT_SEMANTICS_BLOCKERS.md',coordinator/'STATIC_CONTRACT_RISK_ADJUDICATION.md',coordinator/'draft_semantics_differential.json']:
 b=p.read_bytes();bindings.append({'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'read_only':True})
(OWN/'INPUT_AND_FROZEN_SOURCE_BINDINGS.json').write_text(json.dumps({'frozen_sha':FROZEN,'base_sha':BASE,'complete_Git_delta_only_additions':True,'bindings':bindings},indent=2)+'\n')
states=[]
for p,expected in [(ROOT,FROZEN),(Path('/home/lizening/wt-codex-r18c2'),'e537f441010077123a307e9d50ea40cf8dad8547'),(Path('/home/lizening/wt-r19-g4-consumer-contract-repair'),BASE),(Path('/home/lizening/wt-r19-recovery-duration-v1'),'2da980f631badc25086d12db60d128ff507d3ae6')]:
 head=git('rev-parse','HEAD',cwd=p).decode().strip();status=git('status','--porcelain=v1',cwd=p).decode();assert head==expected and not status,(p,head,status)
 states.append({'path':str(p),'HEAD':head,'porcelain':status})
(OWN/'FROZEN_WORKTREE_STATES.json').write_text(json.dumps(states,indent=2)+'\n')
print(json.dumps({'frozen_sha':FROZEN,'new_files':len(files),'new_AST_definitions':len(methods),'old_file_changes':0,'old_method_changes':0,'all_four_worktrees_match_and_clean':True,'pending_coordinator_semantics_and_metadata_requests_merged':True,'independent_acceptance':'NOT_ISSUED'}))
