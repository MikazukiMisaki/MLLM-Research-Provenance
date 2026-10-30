"""Exercise the exact scene() definition without importing or executing the full audit."""
import ast,json,re
from pathlib import Path
src=Path(__file__).with_name('scene_suffix_audit.py').read_text()
tree=ast.parse(src); functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='scene']; assert len(functions)==1
module=ast.fix_missing_locations(ast.Module(body=functions,type_ignores=[])); ns={'re':re};exec(compile(module,'<exact-scene-function>','exec'),ns)
scene=ns['scene']; assert scene('synthetic-a-b-c-123')==123
bad=['synthetic-a-b-c','synthetic-a-b-c-', 'synthetic-a-b-c-12/trial', 'synthetic-a-b-c-12-tail','123','']
for b in bad:
 try:scene(b)
 except ValueError:pass
 else:raise AssertionError('invalid parent accepted')
print(json.dumps({'valid_synthetic_cases':1,'invalid_synthetic_cases_rejected':len(bad),'invalids_all_raise_ValueError':True,'environment_model_or_candidate_data_loaded':False}))
