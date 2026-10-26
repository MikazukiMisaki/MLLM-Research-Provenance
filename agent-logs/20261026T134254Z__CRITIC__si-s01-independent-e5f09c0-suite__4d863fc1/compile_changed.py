from pathlib import Path
import json,py_compile,sys
TREE=Path(sys.argv[1]);OUT=Path(sys.argv[2]);FILES=json.loads(Path(sys.argv[3]).read_text())['paths']
for i,relative in enumerate(FILES):
 target=OUT/('changed_'+str(i)+'.pyc');target.parent.mkdir(parents=True,exist_ok=True);py_compile.compile(str(TREE/relative),cfile=str(target),doraise=True)
print(json.dumps({'compiled_python_count':len(FILES),'external_compile_root':str(OUT),'paths':FILES}))
