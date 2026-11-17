from pathlib import Path
import sys,tempfile,json,hashlib
sys.path.insert(0,'/home/lizening/research-notes/agent-logs/20261118__CODEX__si-state-selection-cpu-v7-readledger-v3__private')
from read_journal import ReadJournal,recover,canonical
with tempfile.TemporaryDirectory() as t:
    root=Path(t);limits={'files':1,'bytes':10,'ledger_records':1}
    path=root/'dup';j=ReadJournal(path,limits);j.event('HEADER',limits)
    r=recover(path);assert r['read_accounting']=='UNKNOWN' and r.get('journal_integrity')=='UNKNOWN'
    print('duplicate_HEADER UNKNOWN')
    for case,seq in [('bool_false',False),('float_zero',0.0),('bool_true',True),('float_one',1.0)]:
        path=root/case;rows=[];prev='0'*64
        events=[('HEADER',limits)] if case in ('bool_false','float_zero') else [('HEADER',limits),('RESERVE',{'id':0,'bytes':1,'path':'fictional'})]
        for i,(kind,payload) in enumerate(events):
            value=seq if i==len(events)-1 else i
            row={'seq':value,'previous':prev,'kind':kind,'payload':payload};h=hashlib.sha256(canonical(row)).hexdigest();rows.append(canonical(dict(row,digest=h))+b'\n');prev=h
        path.write_bytes(b''.join(rows));r=recover(path)
        assert r['read_accounting']=='UNKNOWN' and r.get('journal_integrity')=='UNKNOWN'
        print(case,'UNKNOWN')
print('Only fully fictional hash-chained journals; no actual read')
