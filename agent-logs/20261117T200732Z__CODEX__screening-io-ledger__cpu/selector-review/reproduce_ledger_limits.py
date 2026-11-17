import json,subprocess,sys,tempfile
from pathlib import Path
sys.path.insert(0,'/home/lizening/research-notes/agent-logs/20261118__CODEX__si-state-selection-cpu-v7__private')
import test_selector as f
source=Path(f.HERE)/'select_pairs.py'
with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp)/'in';m=f.build_fixture(root,count=20);raw=f.encode(m);mp=root/'manifest.json';mp.write_bytes(raw)
    for cap in (19,20):
        out=Path(tmp)/('out'+str(cap))
        argv=[sys.executable,'-I','-B',str(source),'--input-root',str(root),'--manifest',str(mp),'--manifest-sha256',f.sha(raw),'--output',str(out),'--max-files','10000','--max-bytes','20000000','--max-ledger-records',str(cap)]
        p=subprocess.run(argv,capture_output=True,text=True);status=json.loads((out/'status.json').read_text())
        assert p.returncode==1 and status['status']=='UNKNOWN' and 'ledger record ceiling' in status['reason']
        if cap==19:
            assert status['parent_roster_ledger_complete'] is False and not (out/'ledger.jsonl').exists()
            print('cap19: UNKNOWN; complete parent ledger false; ledger absent')
        else:
            rows=[json.loads(x) for x in (out/'ledger.jsonl').read_text().splitlines()]
            assert status['parent_roster_ledger_complete'] and len(rows)==20 and rows[0]['disposition']=='UNKNOWN' and all(r['disposition']=='NOT_SCANNED_AFTER_STOP' for r in rows[1:])
            print('cap20: UNKNOWN; 20 parent rows incl UNKNOWN then 19 NOT_SCANNED_AFTER_STOP')
