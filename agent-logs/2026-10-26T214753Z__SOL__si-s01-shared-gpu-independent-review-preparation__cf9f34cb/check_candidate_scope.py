"""Static independent scope inspection. Does not import candidate/runtime modules."""
import ast, hashlib, json, subprocess, sys
from pathlib import Path

repo=Path(sys.argv[1]); base=sys.argv[2]; target=sys.argv[3]
task=Path(sys.argv[4]); task_data=json.loads(task.read_text())
allowed={(x['path'],x['method']) for x in task_data['existing_method_whitelist']}
allowed_modules={p for p,_ in allowed}
new_modules={'src/self_improvement/si_s01/shared_resource.py','src/self_improvement/si_s01/shared_resource_audit.py'}
new_config='configs/experiments/si_s01_shared_resource_v1.json'
def git(*args): return subprocess.check_output(['git',*args],cwd=repo)
def content(ref,path):
    p=subprocess.run(['git','show',ref+':'+path],cwd=repo,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return p.stdout if p.returncode==0 else None

def functions(raw):
    result={}
    def visit(nodes,prefix=''):
        for n in nodes:
            if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)):
                result[prefix+n.name]=hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest()
            elif isinstance(n,ast.ClassDef): visit(n.body,prefix+n.name+'.')
    visit(ast.parse(raw).body)
    return result
rows=[]; violations=[]
for path in git('diff','--name-only',base,target).decode().splitlines():
    before=content(base,path); after=content(target,path)
    row={'path':path,'old_sha256':hashlib.sha256(before).hexdigest() if before is not None else None,'new_sha256':hashlib.sha256(after).hexdigest() if after is not None else None}
    if path in allowed_modules and before is not None and after is not None:
        old=functions(before); new=functions(after)
        changed=[name for name in old if old[name]!=new.get(name)]
        additions=sorted(set(new)-set(old))
        row.update(changed_existing_functions=changed,new_functions=additions)
        for name in changed:
            if (path,name) not in allowed: violations.append({'path':path,'method':name,'reason':'Existing method outside authorized17'})
        row['requires_manual_review']='Imports, class/module constants, helper additions, unchanged scientific behavior and full delta still require independent review.'
    elif path in new_modules or path==new_config:
        row['category']='Authorized resource addition'
    elif path.startswith('tests/'):
        row['category']='Test delta requires meaningful test/compatibility review'
    else: violations.append({'path':path,'reason':'File outside narrow authorized scope; require separate ruling'})
    rows.append(row)
value={'schema':'ROOT_STATIC_SCOPE_INSPECTION_V1','python':sys.version,'base':base,'candidate':target,'task_sha256':hashlib.sha256(task.read_bytes()).hexdigest(),'files':rows,'violations':violations,'decision':'SCOPE_CHECK_ONLY_NOT_IMPLEMENTATION_PASS','imports_executed':False}
print(json.dumps(value,indent=2));sys.exit(bool(violations))
