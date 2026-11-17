from pathlib import Path
import sys,tempfile
sys.path.insert(0,'/home/lizening/research-notes/agent-logs/20261118__CODEX__si-state-selection-cpu-v7-readledger__private')
from read_journal import ReadJournal,recover
with tempfile.TemporaryDirectory() as t:
    root=Path(t)
    for case in ('short_return','after_complete','over_limit'):
        path=root/(case+'.jsonl');j=ReadJournal(path,{'files':1,'bytes':5 if case=='over_limit' else 10,'ledger_records':1})
        if case=='after_complete':j.event('READ_PHASE_COMPLETE',{'selection_status':'INSUFFICIENT'})
        j.event('RESERVE',{'id':0,'bytes':10,'path':'fictional'})
        j.event('RETURNED',{'id':0,'known_bytes':5 if case=='short_return' else 10})
        if case!='after_complete':j.event('READ_PHASE_COMPLETE',{'selection_status':'INSUFFICIENT'})
        state=recover(path)
        assert state['read_accounting']=='COMPLETE_LOGGED_READS_ONLY'
        print(case,'ACCEPTED AS COMPLETE_LOGGED_READS_ONLY',state)
print('Fictional synthetically constructed, hash-chained records; no claim current selector generates these sequences')
