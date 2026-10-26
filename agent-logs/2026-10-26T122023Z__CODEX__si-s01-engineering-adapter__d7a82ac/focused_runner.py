from pathlib import Path
import json,sys
TREE=Path(sys.argv[1]).resolve();OUT=Path(sys.argv[2]).resolve();sys.path[:0]=[str(TREE/'src'),str(TREE/'tests'),str(TREE)]
import pytest
args=['-q','-p','no:cacheprovider','--basetemp=/tmp/si-s01-engineering-final-focused','--junitxml='+str(OUT/'focused.junit.xml'),*[str(p.relative_to(TREE)) for p in sorted((TREE/'tests').glob('test_si_s01*.py'))]]
(OUT/'focused.arguments.json').write_text(json.dumps(args,indent=2)+'\n');raise SystemExit(int(pytest.main(args)))
