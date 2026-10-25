from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,subprocess
ROOT=Path(__file__).resolve().parent
repo=Path('/tmp/si-e2-uuid-independent-review-844cc4b7');base='dfc00e49d1ef4d48453d2331507429f8a0c7bbc5';sha='844cc4b78df1f83e29391ffd5ab861a2d0c0a3fd'
def git(*a):return subprocess.check_output(['git',*a],cwd=repo)
def files(ref):
 return {row.split()[3].decode():row.split()[2].decode() for row in git('ls-tree','-r',ref).splitlines()}
def methods(text):
 tree=ast.parse(text);out={}
 def visit(nodes,prefix=''):
  for node in nodes:
   if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):
    out[prefix+node.name]=hashlib.sha256(ast.dump(node,include_attributes=False).encode()).hexdigest()
   elif isinstance(node,ast.ClassDef):visit(node.body,prefix+node.name+'.')
 visit(tree.body);return out
old,new=files(base),files(sha);changed=[p for p in old if old[p]!=new.get(p)];added=sorted(set(new)-set(old));assert changed==['src/self_improvement/si_p3/runtime_backend.py'] and added==['tests/test_si_e2_cuda_uuid_compat.py']
path=changed[0];before=methods(git('show',base+':'+path).decode());after=methods((repo/path).read_text())
changed_methods=[p for p in before if before[p]!=after.get(p)];new_methods=sorted(set(after)-set(before));assert changed_methods==['LocalInference.load'] and new_methods==['cuda_uuid_matches','verify_cuda_uuid']
unchanged=['src/self_improvement/si_p3/'+x+'.py' for x in ('runtime_gate','runtime_ledger','runtime_environment','runtime_supervisor','runtime_diagnostic','collector','contract')]
assert all(old[p]==new[p] for p in unchanged)
result={'UTC':datetime.now(timezone.utc).isoformat(),'source_SHA':sha,'base_SHA':base,'changed_old_files':changed,'new_files':added,'old_tracked_files_unchanged':len(old)-len(changed),'methods_changed':changed_methods,'methods_added':new_methods,'before_method_hashes':before,'after_method_hashes':after,'critical_unchanged_blobs':{p:old[p] for p in unchanged},'inspect_gpu_PID_UID_and_foreign_compute_policy':'BYTE_IDENTICAL','no_sci_treatment_budget_prompt_parser_or_old_evidence_change':True,'source_treatment_semantics_changed':False,'scientific_execution_behavior_changed':False,'new_scientific_authorization':False,'critical_remaining_condition':'Trusted host/local PID map or verified same-namespace execution context before8B'}
with (ROOT/'independent_exact_source_scope.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({k:result[k] for k in ('changed_old_files','new_files','old_tracked_files_unchanged','methods_changed','methods_added','inspect_gpu_PID_UID_and_foreign_compute_policy')}))
