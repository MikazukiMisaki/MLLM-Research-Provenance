from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,subprocess
OWN=Path(__file__).resolve().parent;REPO=Path('/home/lizening/wt-si-p3-source-only-v2');BASE='844cc4b78df1f83e29391ffd5ab861a2d0c0a3fd'
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def write(name,value):
 with (OWN/name).open('x') as f:json.dump(value,f,indent=2);f.write('\n')
def binding(path):
 p=Path(path);b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def tree(ref):
 result={}
 for item in git('ls-tree','-r','-z',ref).split(b'\0'):
  if item:
   info,name=item.split(b'\t',1);result[name.decode()]=info.decode()
 return result
head=git('rev-parse','HEAD').decode().strip();status=git('status','--porcelain=v1').decode();assert not status
before=tree(BASE);after=tree(head);changed=[p for p,v in before.items() if after.get(p)!=v];added=sorted(set(after)-set(before));assert not changed and len(added)==15
for name,args in [('source_delta.patch',('diff','--binary',BASE,head)),('source_delta.stat',('diff','--stat',BASE,head))]:
 with (OWN/name).open('xb') as f:f.write(git(*args))
write('SOURCE_SCOPE.json',{'base_sha':BASE,'candidate_sha':head,'branch':git('branch','--show-current').decode().strip(),'worktree':str(REPO),'clean_status':status,'original_tracked_entries':len(before),'all_original_tree_entries_equal':not changed,'changed_or_deleted_original_paths':changed,'added_paths':added,'old_worktree':{'path':'/home/lizening/wt-si-e2-cuda-uuid-compat','head':subprocess.check_output(['git','rev-parse','HEAD'],cwd='/home/lizening/wt-si-e2-cuda-uuid-compat',text=True).strip(),'status':subprocess.check_output(['git','status','--porcelain=v1'],cwd='/home/lizening/wt-si-e2-cuda-uuid-compat',text=True)},'scope':'Only added SI-S01 namespace, CLI, docs and software tests; no old shared methods changed.'})
modules=[]
for name in added:
 path=REPO/name;raw=path.read_bytes();row={'path':name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'definitions':[]}
 if path.suffix=='.py':
  module=ast.parse(raw,filename=name)
  class Visitor(ast.NodeVisitor):
   def __init__(self):self.prefix=[]
   def collect(self,node):
    row['definitions'].append({'name':'.'.join(self.prefix+[node.name]),'kind':type(node).__name__,'line':node.lineno,'end_line':node.end_lineno,'ast_sha256':hashlib.sha256(ast.dump(node,include_attributes=False).encode()).hexdigest()})
    self.prefix.append(node.name);self.generic_visit(node);self.prefix.pop()
   visit_FunctionDef=collect;visit_AsyncFunctionDef=collect;visit_ClassDef=collect
  Visitor().visit(module)
 modules.append(row)
write('METHOD_HASHES.json',{'source_sha':head,'hash_algorithm':'SHA256(ast.dump(node, include_attributes=False)); source hash separately exact bytes','modules':modules})
root=Path('/home/lizening/research-notes/agent-logs')
paths=[root/'2026-10-26T100859Z__SOL__si-p3-persistent-launch-coordination__f1a52e8c'/x for x in ('SOURCE_ONLY_IMPLEMENTATION_TASK.md','ADOPTED_SOURCE_ONLY_PROTOCOL.md')]
paths += [root/'2026-10-25T084517Z__SOL__si-p3-controlled-experience-design__si3_7d91/ADOPTED_METADATA_RESERVATIONS.json']
paths += [root/'2026-10-26T091852Z__CODEX__si-p3-v2-source-first-design__cec2ce5a'/x for x in ('SI_P3_V2_PROTOCOL_DRAFT_NOT_EXECUTABLE.md','PAPER_BUDGET_ARITHMETIC.json','STATIC_METHOD_EVENT_GAP_REVIEW.md')]
paths += [root/'2026-10-26T095405Z__CODEX__si-p3-v2-C01-C02-clarification__ed7dbe04/C01_C02_CLARIFICATION_ADDENDUM.md',root/'2026-10-25T142922Z__SOL__si-e2-uuid-compat-review__cudafix_3a14/independent_review.json',root/'2026-10-26T111621Z__SOL__si-s01-independent-base844-suite__critic_1f34d86d/BASELINE_ID_SETS.json']
paths += [REPO/x for x in ('AGENTS.md','PROJECT.md','PAPER_PROPOSAL.md','EXPERIMENT_PLAN.md','IMPLEMENTATION_PHASES.md','reports/SPRINT_1_5_FINAL.md')]
write('INPUT_BINDINGS_FINALIZATION_INITIAL.json',{'captured_utc':datetime.now(timezone.utc).isoformat(),'timing':'After committed focused tests; before final handoff seal. Not a claim of pre-development measurement. Original scientific source equality is independently checked from immutable base Git objects.','files':[binding(p) for p in paths],'payloads_opened':'Hash bytes only for metadata; no fresh task body or production launch plan constructed.'})
print(json.dumps({'source_sha':head,'unchanged_original_entries':len(before),'new_files':len(added),'definition_count':sum(len(r['definitions']) for r in modules)}))
