"""CPU protocol-fragment candidate. Never a production launcher."""
import hashlib
import json
import os
from pathlib import Path
import re
import select
import socket

SHA_RE=re.compile(r'^[0-9a-f]{64}$')
class Stop(RuntimeError): pass

def canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def digest(x): return hashlib.sha256(x).hexdigest()
def pairs(seq):
    out={}
    for k,v in seq:
        if k in out: raise ValueError('duplicate key')
        out[k]=v
    return out

def valid_receipt(path,kind,op,seq,expected):
    """Check child journal chain and exact last-row bytes. No physical proof."""
    raw=Path(path).read_bytes()
    if not raw or not raw.endswith(b'\n'): raise Stop('journal incomplete')
    lines=raw.splitlines(keepends=True); prev='0'*64
    for index,line in enumerate(lines):
        row=json.loads(line,object_pairs_hook=pairs)
        saved=row.pop('digest')
        if row['seq']!=index or row['previous']!=prev or digest(canon(row))!=saved:
            raise Stop('journal hash chain')
        prev=saved
    if (digest(lines[-1])!=expected or row['kind']!=op+'_'+kind or
        row['payload'].get('owner_seq')!=seq): raise Stop('receipt mismatch')

class Budget:
    def __init__(self,root,caps):
        self.root=Path(root);self.root.mkdir(mode=0o700,parents=True,exist_ok=True)
        fd=os.open(self.root/'claim',os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW,0o600)
        try: os.write(fd,b'SYNTHETIC ONLY; NO RESUME\n');os.fsync(fd)
        finally: os.close(fd)
        dfd=os.open(self.root,os.O_RDONLY|os.O_DIRECTORY)
        try:os.fsync(dfd)
        finally:os.close(dfd)
        self.path=self.root/'parent-ledger.jsonl';self.caps=dict(caps);self.counts={k:0 for k in caps}
        self.previous='0'*64;self.seq=0;self.active=None;self.failed=False;self.finished=[]

    def record(self,event,payload):
        row={'seq':self.seq,'previous':self.previous,'event':event,'payload':payload}
        h=digest(canon(row));data=canon(dict(row,digest=h))+b'\n'
        fd=os.open(self.path,os.O_CREAT|os.O_APPEND|os.O_WRONLY|os.O_NOFOLLOW,0o600)
        try:
            view=memoryview(data)
            while view:
                n=os.write(fd,view)
                if n<=0:raise OSError('short write')
                view=view[n:]
            os.fsync(fd)
        finally:os.close(fd)
        dfd=os.open(self.root,os.O_RDONLY|os.O_DIRECTORY)
        try:os.fsync(dfd)
        finally:os.close(dfd)
        self.seq+=1;self.previous=h

    def abort(self,reason):
        try:self.record('aborted',{'reason':reason,'active':self.active})
        except Exception:pass
        self.failed=True

    def serve(self,sock,arm,journal):
        if self.failed or self.active is not None or arm not in ('A','B') or arm in self.finished or (arm=='B' and self.finished!=['A']):
            if not self.failed: self.abort('invalid arm order or active effect')
            sock.close()
            raise Stop('cannot enter arm')
        next_seq=0
        arm_returned={k:0 for k in self.caps}
        sock.settimeout(5)
        try:
            with sock.makefile('rwb',buffering=0) as stream:
                while True:
                    line=stream.readline(4097)
                    if not line or len(line)>4096 or not line.endswith(b'\n'): raise Stop('EOF or oversized request')
                    try:msg=json.loads(line,object_pairs_hook=pairs,parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite')))
                    except (ValueError,TypeError) as e:raise Stop('malformed message') from e
                    if type(msg) is not dict or type(msg.get('seq')) is not int:raise Stop('sequence shape')
                    kind=msg.get('kind')
                    expected = (self.active['seq'] if kind in ('returned','unknown') and self.active is not None else next_seq)
                    if msg['seq']!=expected:raise Stop('sequence mismatch')
                    if kind=='reserve':
                        if set(msg)!={'kind','seq','operation'}:raise Stop('reserve schema')
                        op=msg['operation']
                        if not isinstance(op,str) or op not in self.caps or self.active is not None or self.counts[op]>=self.caps[op]:raise Stop('budget or duplicate reserve')
                        ticket={'arm':arm,'seq':expected,'operation':op}
                        self.record('reserved',ticket) # durable before ACK and count
                        self.counts[op]+=1;self.active=ticket;next_seq+=1
                    elif kind in ('returned','unknown'):
                        if set(msg)!={'kind','seq','operation','receipt_sha256'}:raise Stop('return schema')
                        op=msg['operation'];receipt=msg['receipt_sha256']
                        if (type(receipt) is not str or not SHA_RE.fullmatch(receipt) or self.active!={'arm':arm,'seq':expected,'operation':op}):raise Stop('unexpected receipt')
                        valid_receipt(journal,kind,op,expected,receipt)
                        self.record(kind,dict(self.active,receipt_sha256=receipt));self.active=None
                        if kind=='returned': arm_returned[op]+=1
                    elif kind=='finished':
                        if (set(msg)!={'kind','seq','status'} or self.active is not None or msg['status']!='COMPLETED' or
                            any(arm_returned.get(op,0)<1 for op in ('model_load','generation'))): raise Stop('invalid or incomplete finish')
                        self.record('finished',{'arm':arm,'seq':expected,'status':'COMPLETED'})
                    else:raise Stop('unknown request')
                    # Reject frames already queued before their prior ACK. This is not
                    # a proof against a concurrent same-UID peer or all timing races.
                    queued=sock.recv(1,socket.MSG_PEEK) if select.select([sock],[],[],0)[0] else b''
                    if queued: raise Stop('pipelined frame before ACK')
                    sock.sendall(canon({'kind':'ack','seq':expected,'allowed':True})+b'\n')
                    if kind=='unknown':raise Stop('unknown effect; batch must stop')
                    if kind=='finished':self.finished.append(arm);return
        except (Exception,KeyboardInterrupt) as error:
            self.abort(type(error).__name__+': '+str(error))
            raise Stop('fail stop: '+str(error)) from error
        finally:sock.close()
