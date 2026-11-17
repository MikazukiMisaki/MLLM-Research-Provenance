import json,sys,tempfile
from pathlib import Path
sys.path.insert(0,'/home/lizening/research-notes/agent-logs/20261118__CODEX__si-state-selection-cpu__private')
import test_selector,select_pairs
with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp)/'input';manifest=test_selector.build_fixture(root)
    a,b=[row['episode_ref'] for row in manifest['train'][:2]]
    e0=json.loads((root/a).read_bytes());e1=json.loads((root/b).read_bytes())
    for key in ('episode_id','terminal_ref','decisions'):e1[key]=e0[key]
    raw=test_selector.encode(e1);(root/b).write_bytes(raw);manifest['files'][b]=test_selector.sha(raw)
    result=select_pairs.build(manifest,root.resolve())
    assert len(result)==16 and result[0]['parent']!=result[1]['parent']
    assert result[0]['episode_id']==result[1]['episode_id']
    assert result[0]['target']['refs']==result[1]['target']['refs']
    assert result[0]['control']['refs']==result[1]['control']['refs']
    assert result[0]['terminal_ref']==result[1]['terminal_ref']
    print('ACCEPTED: two declared parents share the exact episode ID, decision refs, target/control refs and terminal ref')
    print('Synthetic fixture only; input authenticity was never established')
