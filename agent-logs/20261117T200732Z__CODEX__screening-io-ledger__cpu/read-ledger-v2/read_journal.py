"""Synthetic read-reservation journal; not physical-disk I/O accounting."""
import hashlib
import json
import os
from pathlib import Path

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
class ReadJournal:
    def __init__(self,path,limits):
        self.path=Path(path);self.seq=0;self.prev='0'*64;self.broken=False
        fd=os.open(self.path,os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW,0o600)
        try:os.fsync(fd)
        finally:os.close(fd)
        fd=os.open(self.path.parent,os.O_RDONLY|os.O_DIRECTORY)
        try:os.fsync(fd)
        finally:os.close(fd)
        self.event('HEADER',limits)
    def event(self,kind,payload):
        if self.broken:raise OSError('journal already failed')
        row={'seq':self.seq,'previous':self.prev,'kind':kind,'payload':payload}
        h=hashlib.sha256(canonical(row)).hexdigest();line=canonical(dict(row,digest=h))+b'\n'
        try:
            fd=os.open(self.path,os.O_WRONLY|os.O_APPEND|os.O_NOFOLLOW)
            try:
                view=memoryview(line)
                while view:
                    n=os.write(fd,view)
                    if n<=0:raise OSError('short journal write')
                    view=view[n:]
                os.fsync(fd)
            finally:os.close(fd)
        except BaseException:
            self.broken=True;raise
        self.seq+=1;self.prev=h

def recover(path):
    """Conservatively reconstruct reservations; malformed/incomplete means UNKNOWN."""
    result={'read_accounting':'UNKNOWN','reserved_files':0,'reserved_bytes':0,
            'returned_bytes_lower_bound':0,'unclosed':[],'unknown_reads':[]}
    try:
        raw=Path(path).read_bytes()
        if not raw or not raw.endswith(b'\n'):raise ValueError('incomplete journal')
        prev='0'*64;pending={};seen=set();ended=False;scan_unknown=False;limits=None
        for i,line in enumerate(raw.splitlines()):
            if ended:raise ValueError('event after read phase complete')
            row=json.loads(line);h=row.pop('digest')
            if row['seq']!=i or row['previous']!=prev or hashlib.sha256(canonical(row)).hexdigest()!=h:raise ValueError('chain')
            prev=h;kind=row['kind'];payload=row['payload']
            if i==0 and kind!='HEADER':raise ValueError('missing header')
            if i==0:
                limits=payload
                if (type(limits) is not dict or any(type(limits.get(k)) is not int or limits[k]<=0 for k in ('files','bytes'))):
                    raise ValueError('invalid header limits')
            if kind=='RESERVE':
                rid=payload['id'];n=payload['bytes']
                if type(rid) is not int or rid in seen or type(n) is not int or n<0:raise ValueError('reservation')
                seen.add(rid);pending[rid]=n;result['reserved_files']+=1;result['reserved_bytes']+=n
                if result['reserved_files']>limits['files'] or result['reserved_bytes']>limits['bytes']:
                    raise ValueError('reservation exceeds header limits')
            elif kind in ('RETURNED','UNKNOWN'):
                rid=payload['id'];n=payload['known_bytes']
                if rid not in pending or type(n) is not int or n<0 or n>pending[rid]:raise ValueError('return')
                if kind=='RETURNED' and n!=pending[rid]:raise ValueError('short completed read')
                result['returned_bytes_lower_bound']+=n
                if kind=='UNKNOWN':result['unknown_reads'].append(rid)
                del pending[rid]
            elif kind=='READ_PHASE_COMPLETE':ended=True
            elif kind=='SCAN_UNKNOWN':scan_unknown=True
            elif kind!='HEADER':raise ValueError('event')
        result['unclosed']=sorted(pending)
        if ended and not scan_unknown and not pending and not result['unknown_reads']:result['read_accounting']='COMPLETE_LOGGED_READS_ONLY'
    except (OSError,ValueError,KeyError,TypeError,json.JSONDecodeError):result['journal_integrity']='UNKNOWN'
    return result
