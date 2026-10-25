from pathlib import Path
import ast,json,subprocess
ROOT=Path("/home/lizening/wt-si-p3-runtime-adaptation")
paths=subprocess.check_output(["git","ls-files","--others","--exclude-standard"],cwd=ROOT,text=True).splitlines()
if not paths:
 paths=subprocess.check_output(["git","diff","--name-only","a995d4c3c5f7d31a2cf1fd0afc4bfa4bd72ee3a3","HEAD"],cwd=ROOT,text=True).splitlines()
compiled=[];wire=[]
for name in paths:
 p=ROOT/name
 if p.suffix==".py":compile(p.read_bytes(),str(p),"exec");ast.parse(p.read_text());compiled.append(name)
 elif p.suffix==".json":json.loads(p.read_bytes());wire.append(name)
assert len(compiled)==12 and len(wire)==2,(compiled,wire)
print(json.dumps({"compiled":compiled,"json_parsed":wire,"no_imports_or_bytecode_writes":True}))
