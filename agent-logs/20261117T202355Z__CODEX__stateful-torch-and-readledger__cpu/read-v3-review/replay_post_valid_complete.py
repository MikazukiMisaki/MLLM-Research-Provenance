from pathlib import Path
import sys,tempfile
sys.path.insert(0,'/home/lizening/research-notes/agent-logs/20261118__CODEX__si-state-selection-cpu-v7-readledger-v3__private')
from read_journal import ReadJournal,recover
with tempfile.TemporaryDirectory() as t:
 p=Path(t)/'j';j=ReadJournal(p,{'files':2,'bytes':20,'ledger_records':1})
 j.event('RESERVE',{'id':0,'bytes':10,'path':'fictional'});j.event('RETURNED',{'id':0,'known_bytes':10});j.event('READ_PHASE_COMPLETE',{'selection_status':'INSUFFICIENT'})
 assert recover(p)['read_accounting']=='COMPLETE_LOGGED_READS_ONLY'
 j.event('RESERVE',{'id':1,'bytes':1,'path':'fictional-2'});j.event('RETURNED',{'id':1,'known_bytes':1})
 r=recover(p);assert r['read_accounting']=='UNKNOWN' and r.get('journal_integrity')=='UNKNOWN'
 print('After a genuinely valid completed phase, additional hash-chained read is UNKNOWN')
