"""One-arm budget adaptation; counts every actual reservation separately.

Copied from the existing StageBudgetChannel with only EVAL limits and its
minimum completed generation count changed for a single H50 episode.
"""
import json
import re
import time

PROFILES={
 'UPDATE':{'model_load':1,'zero_grad':1,'forward':4,'backward':4,'optimizer_step':1,'checkpoint_save':1,'checkpoint_readback':1,'model_reload':1},
 'EVAL':{'env_construct':1,'env_init':1,'reset':1,'model_load':1,'generation':50,'step':50},
}
MANDATORY={'UPDATE':dict(PROFILES['UPDATE']),'EVAL':{'env_construct':1,'env_init':1,'reset':1,'model_load':1}}
UPDATE_ORDER=('model_load','zero_grad')+('forward','backward')*4+('optimizer_step','checkpoint_save','checkpoint_readback','model_reload')
class Stop(Exception):pass

def pairs(items):
 out={}
 for k,v in items:
  if k in out:raise Stop('duplicate_key')
  out[k]=v
 return out

def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False).encode()

class StageBudgetChannel:
 def __init__(self,stage,sock,journal,*,global_owner,case,arm):
  if type(stage) is not str or stage not in PROFILES:raise Stop('unreviewed_stage')
  self.stage=stage;self.caps=dict(PROFILES[stage]);self.mandatory=dict(MANDATORY[stage]);self.sock=sock;self.journal=journal
  self.global_owner=global_owner;self.case=case;self.arm=arm
  self.buffer=b'';self.pending_ack=b'';self.ack_deadline=None;self.counts={k:0 for k in self.caps}
  self.next_seq=0;self.outstanding=None;self.finished=None;self.unknown=False;self.returned_count=0
 def receive(self,data):
  try:return self._receive(data)
  except BaseException as error:
   self.global_owner.abort(type(error).__name__+': '+str(error))
   raise
 def _receive(self,data):
  if self.pending_ack:raise Stop('frame_before_ack')
  self.buffer+=data
  if len(self.buffer)>4096:raise Stop('frame_too_large')
  if b'\n' not in self.buffer:return
  line,rest=self.buffer.split(b'\n',1);self.buffer=rest
  if rest or not line:raise Stop('multiple_or_empty_frame')
  msg=json.loads(line.decode('utf8','strict'),object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(Stop('nonfinite')))
  if type(msg) is not dict or type(msg.get('seq')) is not int:raise Stop('shape')
  kind=msg.get('kind');seq=msg['seq']
  if kind=='reserve':
   if set(msg)!={'kind','seq','operation'} or seq!=self.next_seq or self.outstanding is not None or self.finished is not None or self.unknown:raise Stop('reserve_order')
   op=msg['operation']
   if type(op) is not str or op not in self.caps or self.counts[op]>=self.caps[op]:raise Stop('cap')
   if self.stage=='UPDATE' and (self.returned_count>=len(UPDATE_ORDER) or op!=UPDATE_ORDER[self.returned_count]):raise Stop('update_order')
   self.global_owner.reserve(self.case,self.arm,op,seq)
   self.counts[op]+=1;self.outstanding={'seq':seq,'operation':op};self.next_seq+=1
   self.journal.emit('operation_reserved',{'stage':self.stage,'seq':seq,'operation':op,'count':self.counts[op],'cost':'STARTED_OR_UNKNOWN_UNTIL_CHILD_PROOF'})
  elif kind in ('returned','unknown'):
   if set(msg)!={'kind','seq','operation','receipt_sha256'} or self.outstanding!={'seq':seq,'operation':msg.get('operation')} or type(msg.get('receipt_sha256')) is not str or re.fullmatch('[0-9a-f]{64}',msg['receipt_sha256']) is None:raise Stop('return_order')
   if kind=='unknown':raise Stop('unknown_effect_fail_stop')
   self.global_owner.returned(self.case,self.arm,msg['operation'],seq,msg['receipt_sha256'])
   self.journal.emit('operation_'+kind,{'stage':self.stage,'seq':seq,'operation':msg['operation'],'receipt_sha256':msg['receipt_sha256'],'child_claim_only':True})
   self.outstanding=None
   if kind=='unknown':self.unknown=True
   else:self.returned_count+=1
  elif kind=='finished':
   if set(msg)!={'kind','seq','status'} or seq!=self.next_seq or self.outstanding is not None or self.finished is not None or msg['status'] not in ('COMPLETED','STOPPED'):raise Stop('finish_order')
   if msg['status']!='COMPLETED':raise Stop('worker_stopped_fail_stop')
   if msg['status']=='COMPLETED' and (self.unknown or any(self.counts[k]!=v for k,v in self.mandatory.items()) or (self.stage=='EVAL' and self.counts['generation']<1)):raise Stop('finish_unproved')
   self.journal.emit('worker_budget_finished',{'stage':self.stage,'seq':seq,'status':msg['status'],'counts':dict(self.counts),'child_claim_only':True});self.finished=msg['status']
  else:raise Stop('kind')
  self.pending_ack=canonical({'kind':'ack','seq':seq,'allowed':True})+b'\n';self.ack_deadline=time.monotonic()+2.0
 def write_ack(self):
  try:return self._write_ack()
  except BaseException as error:
   self.global_owner.abort(type(error).__name__+': '+str(error))
   raise
 def _write_ack(self):
  if not self.pending_ack:raise Stop('unexpected_ack_write')
  try:n=self.sock.send(self.pending_ack)
  except BlockingIOError:return
  if n<=0:raise Stop('ack_write')
  self.pending_ack=self.pending_ack[n:]
  if not self.pending_ack:self.ack_deadline=None
 def eof(self):
  try:
   if self.buffer or self.pending_ack or self.outstanding is not None or self.finished is None:raise Stop('incomplete_eof')
  except BaseException as error:
   self.global_owner.abort(type(error).__name__+': '+str(error))
   raise
