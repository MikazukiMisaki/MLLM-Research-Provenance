"""Static Git-object and installed-source reading only; never executes source."""
import ast,datetime,hashlib,json,subprocess
from pathlib import Path

def method_tree(text,needle):
 tree=ast.parse(text)
 if '.' in needle:
  cls,name=needle.split('.',1);parent=next((n for n in tree.body if isinstance(n,ast.ClassDef) and n.name==cls),None)
  node=next((n for n in parent.body if isinstance(n,ast.FunctionDef) and n.name==name),None) if parent else None
 else:node=next((n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==needle),None)
 if node is None:return None
 return {'line':node.lineno,'end_line':node.end_lineno,'AST_sha256':hashlib.sha256(ast.dump(node,include_attributes=False).encode()).hexdigest()}

def run(ns):
 own,frozen=ns['OWN'],ns['FROZEN'];register=ns['register'];sha=ns['sha'];out=[];receipts=[]
 revisions={'R4':'7a01a6107b4bc9c994893220aab078af39fe4fff','R10_OSR':'8926d8fb10e634489031de3da910c572b50d8d44','R16_OSR':'d1ef841ea9dc7423177fb7647906e2e719f0fbe7','R19_K1':'2da980f631badc25086d12db60d128ff507d3ae6'}
 targets=[('src/env/alfworld.py','AlfWorldTextEnvironment.step'),('src/sft/protocol.py','sft_p0_prompt'),('src/models/action_parser.py','action_id_mapping')]
 for stage,rev in revisions.items():
  for file,method in targets:
   argv=['git','show',rev+':'+file];started=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run(argv,cwd=frozen,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   receipt={'argv':argv,'cwd':str(frozen),'actual_returncode':r.returncode,'returncode_source':'subprocess.returncode','started_utc':started,'stdout_sha256':hashlib.sha256(r.stdout.encode()).hexdigest(),'stdout_chars':len(r.stdout),'stderr':r.stderr}
   receipts.append(receipt)
   current=register(frozen/file);current_text=current.read_text();hist=method_tree(r.stdout,method) if r.returncode==0 else None;now=method_tree(current_text,method)
   out.append({'stage':stage,'executed_implementation_sha':rev,'source_path':file,'method':method,'historical_git_object_read_returncode':r.returncode,'historical_file_sha256':receipt['stdout_sha256'] if r.returncode==0 else None,'frozen85_file_sha256':sha(current),'historical_method':hist,'frozen85_method':now,'method_AST_equal':hist is not None and now is not None and hist['AST_sha256']==now['AST_sha256'],'status':'STATIC_METHOD_BOUND' if hist is not None and now is not None and hist['AST_sha256']==now['AST_sha256'] else 'HOLD_HISTORY_UNRESOLVED'})
 installed=register(Path('/home/lizening/miniconda3/envs/alfworld-self-improve/lib/python3.10/site-packages/alfworld/agents/environment/alfred_tw_env.py'))
 (own/'historical_contract_read.receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
 result={'contracts':out,'installed_alfworld_source':{'path':str(installed),'sha256':sha(installed),'scope':'Current installed code only; historical package-byte pin not retrospectively assumed','observation':'AlfredTWEnv.init_env requests won=True and creates TextWorld gym. AlfredExpert.step forwards super reward; repository wrapper returns float(rewards), records won in metadata without replacing reward by won. Thus absence of won is retained as separate terminal corroboration gap.'},'no_project_import_or_runtime_call':True}
 (own/'historical_contracts.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 ns['savebindings']();print(json.dumps({'historical_reads':len(out),'all_method_AST_equal':all(x['method_AST_equal'] for x in out),'read_returncodes':[x['actual_returncode'] for x in receipts]},indent=2))
