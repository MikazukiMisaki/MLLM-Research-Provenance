import os,sys,tempfile,json
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,'/home/lizening/research-notes/agent-logs/20261118__CODEX__si-state-selection-cpu-v7__private')
import select_pairs as s,test_selector as f
with tempfile.TemporaryDirectory() as t:
    root=Path(t)/'inputs';m=f.build_fixture(root);raw=f.encode(m);mp=root/'manifest.json';mp.write_bytes(raw);out=Path(t)/'out'
    real=os.fdopen;calls=[0];observed=[0]
    class FailingRead:
        def __init__(self,wrapped):self.wrapped=wrapped
        def __enter__(self):self.wrapped.__enter__();return self
        def __exit__(self,*args):return self.wrapped.__exit__(*args)
        def read(self,n):
            chunk=self.wrapped.read(min(5,n));observed[0]+=len(chunk)
            raise OSError('fictional mid-read failure after partial bytes')
    def injected(fd,*args,**kwargs):
        calls[0]+=1;wrapped=real(fd,*args,**kwargs)
        return FailingRead(wrapped) if calls[0]==2 else wrapped
    argv=['select_pairs.py','--input-root',str(root),'--manifest',str(mp),'--manifest-sha256',f.sha(raw),'--output',str(out),'--max-files','10000','--max-bytes','20000000','--max-ledger-records','128']
    with patch.object(sys,'argv',argv),patch.object(s.os,'fdopen',side_effect=injected):rc=s.main()
    status=json.loads((out/'status.json').read_text());ledger=[json.loads(x) for x in (out/'ledger.jsonl').read_text().splitlines()]
    assert rc==1 and status['status']=='UNKNOWN' and observed[0]>0
    assert status['counters']['bytes_read']==len(raw) and ledger[0]['disposition']=='UNKNOWN'
    print('PARTIAL READ: status UNKNOWN and parent UNKNOWN; measured earlier returned partial bytes excluded from bytes_read counter')
    print('partial_bytes=',observed[0],'reported_bytes=',status['counters']['bytes_read'],'manifest_bytes=',len(raw))
    print('No physical I/O-total claim; entirely fictional file content')
