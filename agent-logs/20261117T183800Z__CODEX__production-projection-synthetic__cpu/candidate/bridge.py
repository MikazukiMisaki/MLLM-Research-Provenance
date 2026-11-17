"""CPU protocol-fragment candidate. Never a production launcher."""
import hashlib
import json
import os
from pathlib import Path
import re
import select
import socket

SHA_RE=re.compile(r'^[0-9a-f]{64}$')
OPS=('env_construct','env_init','reset','model_load','generation','step')
ARM_CAPS={arm:{op:(2 if op in ('generation','step') else 1) for op in OPS} for arm in ('A','B')}
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
    """Validate claimed child lifecycle, not process ownership or actual effects."""
    raw=Path(path).read_bytes()
    if not raw or not raw.endswith(b'\n'): raise Stop('journal incomplete')
    lines=raw.splitlines(keepends=True); prev='0'*64; effect_events=[]
    for index,line in enumerate(lines):
        row=json.loads(line,object_pairs_hook=pairs)
        saved=row.pop('digest')
        if row['seq']!=index or row['previous']!=prev or digest(canon(row))!=saved:
            raise Stop('journal hash chain')
        prev=saved
        for operation in OPS:
            for suffix in ('started','returned','unknown'):
                if row['kind']==operation+'_'+suffix:
                    owner_seq=row['payload'].get('owner_seq')
                    if type(owner_seq) is not int: raise Stop('bad owner seq in claim')
                    effect_events.append((owner_seq,operation,suffix))
    if (digest(lines[-1])!=expected or row['kind']!=op+'_'+kind or
        row['payload'].get('owner_seq')!=seq): raise Stop('receipt mismatch')
    if len(effect_events)!=2*(seq+1): raise Stop('child claimed lifecycle length mismatch')
    for effect_seq in range(seq+1):
        start,terminal=effect_events[2*effect_seq:2*effect_seq+2]
        terminal_kind=kind if effect_seq==seq else 'returned'
        if (start[0]!=effect_seq or terminal[0]!=effect_seq or start[1]!=terminal[1] or
            start[2]!='started' or terminal[2]!=terminal_kind or (effect_seq==seq and start[1]!=op)):
            raise Stop('child claimed lifecycle mismatch')
    return row['payload'].get('evidence')


def send_all(sock,data,send=None):
    """Loop on short writes; injected send hook exists solely for deterministic tests."""
    send = sock.send if send is None else send
    view=memoryview(data)
    while view:
        n=send(view)
        if type(n) is not int or n<=0 or n>len(view): raise Stop('short/invalid ACK write')
        view=view[n:]

class Budget:
    def __init__(self,root,caps,ack_sender=send_all):
        self.root=Path(root);self.root.mkdir(mode=0o700,parents=True,exist_ok=True)
        self.path=self.root/'parent-ledger.jsonl'
        if os.path.lexists(self.path): raise Stop('existing ledger: no reuse')
        fd=os.open(self.root/'claim',os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW,0o600)
        try: os.write(fd,b'SYNTHETIC ONLY; NO RESUME\n');os.fsync(fd)
        finally: os.close(fd)
        dfd=os.open(self.root,os.O_RDONLY|os.O_DIRECTORY)
        try:os.fsync(dfd)
        finally:os.close(dfd)
        # Exclusive creation also rejects an unexpected existing ledger after claim.
        ledger_fd=os.open(self.path,os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW,0o600)
        try: os.fsync(ledger_fd)
        finally: os.close(ledger_fd)
        self.caps=dict(caps);self.counts={k:0 for k in caps}
        self.arm_counts={a:{op:0 for op in ARM_CAPS[a]} for a in ARM_CAPS}
        self.ack_sender=ack_sender
        self.previous='0'*64;self.seq=0;self.active=None;self.failed=False;self.finished=[]
        self.setup_returned=False;self.prepared=set();self.closed=set()
        self.public_claim=None;self.public_checked=set();self.bound_files=None

    def record(self,event,payload):
        row={'seq':self.seq,'previous':self.previous,'event':event,'payload':payload}
        h=digest(canon(row));data=canon(dict(row,digest=h))+b'\n'
        fd=os.open(self.path,os.O_APPEND|os.O_WRONLY|os.O_NOFOLLOW,0o600)
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
        except BaseException:pass
        finally:self.failed=True

    def serve(self,sock,arm,journal):
        if (self.failed or not self.setup_returned or arm not in self.prepared or self.active is not None or
            arm not in ('A','B') or arm in self.finished or (arm=='B' and (self.finished!=['A'] or 'A' not in self.closed))):
            if not self.failed: self.abort('invalid arm order or active effect')
            sock.close()
            raise Stop('cannot enter arm')
        next_seq=0
        arm_returned={k:0 for k in self.caps}
        try:
            sock.settimeout(5)
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
                        if (not isinstance(op,str) or op not in self.caps or op not in ARM_CAPS[arm] or self.active is not None or
                            self.counts[op]>=self.caps[op] or self.arm_counts[arm][op]>=ARM_CAPS[arm][op]):
                            raise Stop('global/arm budget or duplicate reserve')
                        required={'env_init':'env_construct','reset':'env_init','model_load':'reset','generation':'model_load','step':'generation'}
                        if op in required and arm_returned[required[op]]<1: raise Stop('fake operation order')
                        if op=='model_load' and arm not in self.public_checked: raise Stop('reset claim not checked')
                        ticket={'arm':arm,'seq':expected,'operation':op}
                        self.record('reserved',ticket) # durable before ACK and count
                        self.counts[op]+=1;self.arm_counts[arm][op]+=1;self.active=ticket;next_seq+=1
                    elif kind in ('returned','unknown'):
                        if set(msg)!={'kind','seq','operation','receipt_sha256'}:raise Stop('return schema')
                        op=msg['operation'];receipt=msg['receipt_sha256']
                        if (type(receipt) is not str or not SHA_RE.fullmatch(receipt) or self.active!={'arm':arm,'seq':expected,'operation':op}):raise Stop('unexpected receipt')
                        evidence=valid_receipt(journal,kind,op,expected,receipt)
                        self.record(kind,dict(self.active,receipt_sha256=receipt));self.active=None
                        if kind=='returned':
                            arm_returned[op]+=1
                            if op=='reset':
                                if (not isinstance(evidence,dict) or set(evidence)!={'arm','state','gamefile','candidate_native_reset'} or
                                    evidence.get('arm')!=arm or not isinstance(evidence.get('state'),dict) or
                                    evidence.get('gamefile')!=self.bound_files[0]['path']):
                                    raise Stop('fake reset claim invalid')
                                native=evidence.get('candidate_native_reset')
                                if (type(native) is not dict or set(native)!={'won_batch','won_batch_type'} or
                                    type(native['won_batch']) is not list or len(native['won_batch'])!=1 or
                                    native['won_batch'][0] is not False or type(native['won_batch_type']) is not str or
                                    native['won_batch_type'] not in ('list','tuple')):
                                    raise Stop('fake native reset claim malformed')
                                claim=evidence['state']
                                if set(claim)!={'task_id','family','goal','observation','valid_actions','done','reward','truncated'}:
                                    raise Stop('fake public state shape')
                                if self.public_claim is None: self.public_claim=claim
                                elif canon(claim)!=canon(self.public_claim): raise Stop('fake reset claim mismatch')
                                self.record('public_claim_matched',{'arm':arm,'state':claim,'bound_files':self.bound_files})
                                self.public_checked.add(arm)
                    elif kind=='finished':
                        if (set(msg)!={'kind','seq','status'} or self.active is not None or msg['status']!='COMPLETED' or
                            any(arm_returned.get(op,0)<1 for op in ('env_construct','env_init','reset','model_load','generation'))): raise Stop('invalid or incomplete finish')
                        self.record('finished',{'arm':arm,'seq':expected,'status':'COMPLETED'})
                    else:raise Stop('unknown request')
                    # Reject frames already queued before their prior ACK. This is not
                    # a proof against a concurrent same-UID peer or all timing races.
                    queued=sock.recv(1,socket.MSG_PEEK) if select.select([sock],[],[],0)[0] else b''
                    if queued: raise Stop('pipelined frame before ACK')
                    self.ack_sender(sock,canon({'kind':'ack','seq':expected,'allowed':True})+b'\n')
                    if kind=='unknown':raise Stop('unknown effect; batch must stop')
                    if kind=='finished':self.finished.append(arm);return
        except BaseException as error:
            self.abort(type(error).__name__+': '+str(error))
            raise Stop('fail stop: '+str(error)) from error
        finally:sock.close()
