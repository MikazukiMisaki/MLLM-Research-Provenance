import subprocess,sys,tempfile
from pathlib import Path
candidate='/home/lizening/research-notes/agent-logs/20261118__CODEX__si-state-selection-cpu-v7-readledger-v2__private'
sys.path.insert(0,candidate)
from read_journal import recover
with tempfile.TemporaryDirectory() as t:
    path=Path(t)/'reads.jsonl'
    script='import sys,os;sys.path.insert(0,sys.argv[1]);from read_journal import ReadJournal;j=ReadJournal(sys.argv[2],{"files":1,"bytes":64,"ledger_records":1});j.event("RESERVE",{"id":0,"bytes":64,"path":"fictional"});os._exit(23)'
    p=subprocess.run([sys.executable,'-I','-B','-c',script,candidate,str(path)],capture_output=True)
    result=recover(path)
    assert p.returncode==23 and result['read_accounting']=='UNKNOWN' and result['reserved_bytes']==64 and result['unclosed']==[0]
    print('Actual review-owned child _exit=23 after fsync; reservation 64 retained; unclosed [0]; read_accounting UNKNOWN')
    print('No file content read, no task/model/environment and no scan resume')
