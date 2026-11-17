"""Standalone fictional IPC owner; no model/task loader or production dispatch."""
import hashlib,json,os,re,socket,subprocess,sys
from pathlib import Path

CAPS={'validate_model':1,'set_train_mode':1,'zero_grad':16,'forward':64,'backward':64,'optimizer_step':16,'checkpoint_final':1}
ORDER=['validate_model','set_train_mode']+sum((['zero_grad']+['forward','backward']*4+['optimizer_step'] for _ in range(16)),[])+['checkpoint_final']
class Stop(RuntimeError):pass
class LedgerCreationUnknown(Stop):pass
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def pairs(items):
 d={}
 for key,value in items:
  if key in d:raise Stop('duplicate JSON key')
  d[key]=value
 return d
class Ledger:
 def __init__(self,path):
  self.fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW|os.O_CLOEXEC,0o600);self.prev='0'*64;self.seq=0
  try:
   os.fsync(self.fd)
   directory_fd=os.open(Path(path).parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC)
   try:os.fsync(directory_fd)
   finally:os.close(directory_fd)
  except BaseException as error:
   # Creation durability is unproved; a marker is best effort, not a guarantee.
   try:
    row={'seq':0,'previous':'0'*64,'kind':'creation_unknown','payload':{'error_type':type(error).__name__,'no_execution':True}}
    row['digest']=hashlib.sha256(canonical(row)).hexdigest();view=memoryview(canonical(row)+b'\n')
    while view:
     n=os.write(self.fd,view)
     if n<=0:raise OSError('short unknown marker')
     view=view[n:]
    os.fsync(self.fd)
   except BaseException:pass
   os.close(self.fd)
   raise LedgerCreationUnknown('ledger creation durability unknown; no child started') from error
 def append(self,kind,payload):
  row={'seq':self.seq,'previous':self.prev,'kind':kind,'payload':payload};row['digest']=hashlib.sha256(canonical(row)).hexdigest();data=canonical(row)+b'\n';view=memoryview(data)
  while view:
   n=os.write(self.fd,view)
   if n<=0:raise OSError('short ledger write')
   view=view[n:]
  os.fsync(self.fd);self.prev=row['digest'];self.seq+=1
 def close(self):os.close(self.fd)
def receipt_check(path,operation,seq,receipt,kind):
 if type(operation) is not str or operation not in CAPS or type(seq) is not int or seq<0 or kind not in ('returned','unknown') or type(receipt) is not str or re.fullmatch('[0-9a-f]{64}',receipt) is None:raise Stop('receipt argument shape')
 data=path.read_bytes()
 if not data or not data.endswith(b'\n'):raise Stop('partial child ledger')
 lines=data.splitlines(keepends=True)
 if hashlib.sha256(lines[-1]).hexdigest()!=receipt:raise Stop('receipt hash mismatch')
 prev='0'*64;rows=[];keys={'schema','seq','previous','monotonic_ns','kind','payload','digest'}
 for idx,line in enumerate(lines):
  row=json.loads(line,object_pairs_hook=pairs)
  if type(row) is not dict or set(row)!=keys or row['schema']!='SI_STAGE_WORKER_V1' or type(row['seq']) is not int or row['seq']!=idx or type(row['monotonic_ns']) is not int or row['monotonic_ns']<0 or type(row['kind']) is not str or type(row['payload']) is not dict:raise Stop('child event schema')
  if 'owner_seq' in row['payload'] and (type(row['payload']['owner_seq']) is not int or row['payload']['owner_seq']<0):raise Stop('child owner seq type')
  for op in CAPS:
   payload=row['payload']
   if row['kind']==op+'_started' and (set(payload)!={'request','owner_seq','effect_if_unreturned'} or type(payload.get('owner_seq')) is not int or type(payload.get('request')) is not dict or payload.get('effect_if_unreturned')!='UNKNOWN'):raise Stop('child started schema')
   if row['kind']==op+'_returned' and (set(payload)!={'owner_seq','evidence'} or type(payload.get('owner_seq')) is not int or type(payload.get('evidence')) is not dict):raise Stop('child return schema')
   if row['kind']==op+'_unknown' and (set(payload)!={'owner_seq','effect'} or type(payload.get('owner_seq')) is not int or payload.get('effect')!='UNKNOWN'):raise Stop('child unknown schema')
  without=dict(row);digest=without.pop('digest')
  if type(row['previous']) is not str or row['previous']!=prev or type(digest) is not str or re.fullmatch('[0-9a-f]{64}',digest) is None or hashlib.sha256(canonical(without)).hexdigest()!=digest:raise Stop('child chain mismatch')
  rows.append(row);prev=digest
 last=rows[-1];matches=[x for x in rows if x['kind']==operation+'_started' and x['payload'].get('owner_seq')==seq]
 if len(matches)!=1:raise Stop('child start mismatch')
 started=matches[0]['payload'];payload=last['payload']
 if set(started)!={'request','owner_seq','effect_if_unreturned'} or type(started['request']) is not dict or started['effect_if_unreturned']!='UNKNOWN':raise Stop('child started schema')
 if last['kind']!=operation+'_'+kind or type(payload.get('owner_seq')) is not int or payload['owner_seq']!=seq:raise Stop('child receipt operation mismatch')
 if kind=='returned' and (set(payload)!={'owner_seq','evidence'} or type(payload['evidence']) is not dict):raise Stop('child return schema')
 if kind=='unknown' and (set(payload)!={'owner_seq','effect'} or payload['effect']!='UNKNOWN'):raise Stop('child unknown schema')
 return {'receipt_sha256':receipt,'child_event':last['kind'],'child_claim_only':True}
def run_fake(root,mode):
 if mode not in ('normal','interrupt_after_first_step'):raise Stop('fiction only')
 root=Path(root);root.mkdir(mode=0o700,parents=True,exist_ok=False);ledger=Ledger(root/'parent.jsonl')
 parent,child=socket.socketpair();parent.settimeout(10);proc=None;stream=None;active=None;seq=0;counts={k:0 for k in CAPS};finished=False;outcome='UNKNOWN';reason=None
 try:
  ledger.append('scope',{'classification':'FICTIONAL_ONLY','authorization':False,'physical_proof':False})
  env=dict(os.environ,CUDA_VISIBLE_DEVICES='',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
  with (root/'child.stderr').open('wb') as stderr:
   proc=subprocess.Popen([sys.executable,'-I','-B',str(Path(__file__).with_name('fake_child.py')),str(child.fileno()),str(root),mode],pass_fds=(child.fileno(),),stdout=subprocess.DEVNULL,stderr=stderr,env=env)
   child.close();stream=parent.makefile('rb')
   while True:
    line=stream.readline(4098)
    if not line:
     if not finished:raise Stop('EOF before completed finish')
     break
    if len(line)>4097 or not line.endswith(b'\n'):raise Stop('invalid frame length')
    msg=json.loads(line,object_pairs_hook=pairs,parse_constant=lambda _ : (_ for _ in ()).throw(Stop('nonfinite')))
    if type(msg) is not dict or type(msg.get('seq')) is not int:raise Stop('frame shape')
    kind=msg.get('kind');n=msg['seq']
    if kind=='reserve':
     if set(msg)!={'kind','seq','operation'} or active is not None or n!=seq or seq>=len(ORDER) or type(msg['operation']) is not str or msg['operation']!=ORDER[seq]:raise Stop('reserve sequence')
     op=msg['operation']
     if counts[op]>=CAPS[op]:raise Stop('cap')
     # Durable reservation before ACK; no refund on later EOF/ACK failure.
     ledger.append('reserve',{'seq':seq,'operation':op,'cost':'STARTED_OR_UNKNOWN'});counts[op]+=1;active=(seq,op)
    elif kind in ('returned','unknown'):
     if set(msg)!={'kind','seq','operation','receipt_sha256'} or active!=(n,msg.get('operation')) or type(msg.get('operation')) is not str or type(msg.get('receipt_sha256')) is not str or re.fullmatch('[0-9a-f]{64}',msg['receipt_sha256']) is None:raise Stop('receipt sequence')
     bound=receipt_check(root/'worker_events.jsonl',active[1],n,msg['receipt_sha256'],kind)
     ledger.append(kind,{'seq':n,'operation':active[1],**bound});active=None;seq+=1
    elif kind=='finished':
     if set(msg)!={'kind','seq','status'} or active is not None or n!=seq or seq!=len(ORDER) or counts!=CAPS or type(msg['status']) is not str or msg['status']!='COMPLETED':raise Stop('incomplete finish')
     ledger.append('finished',{'seq':seq,'scope':'CHILD_CLAIMS_ONLY'});finished=True
    else:raise Stop('unknown frame kind')
    # sendall handles partial writes. ACK errors leave prior reservations charged.
    parent.sendall(canonical({'kind':'ack','seq':n,'allowed':True})+b'\n')
    if kind=='unknown':raise Stop('child reported unknown')
    if finished:break
   proc.wait(timeout=10)
   if proc.returncode!=0:raise Stop('child exited nonzero')
   outcome='FICTIONAL_COMPLETE'
 except BaseException as error:
  reason=type(error).__name__+': '+str(error)
  try:ledger.append('stopped_unknown',{'active':active,'reason':reason,'counts':counts,'no_refund':True})
  except BaseException:pass
  outcome='UNKNOWN'
 finally:
  if stream is not None:stream.close()
  parent.close();child.close()
  if proc is not None:
   try:proc.wait(timeout=5)
   except subprocess.TimeoutExpired:reason=(reason or '')+'; direct child not reaped'
  try:ledger.append('process_observation',{'direct_child_returncode':None if proc is None else proc.returncode,'scope':'direct child only; descendants and GPU unknown'})
  finally:ledger.close()
 result={'outcome':outcome,'reason':reason,'returncode':None if proc is None else proc.returncode,'counts':counts,'active':active,'scientific_use':'HOLD'}
 (root/'result.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');return result

def dispatch_real(*_args,**_kwargs):raise RuntimeError('RESEARCH_HOLD')
