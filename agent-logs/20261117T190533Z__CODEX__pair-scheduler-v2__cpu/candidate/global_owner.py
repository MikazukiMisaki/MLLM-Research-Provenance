"""Unreleased pair-owned source interface; scientific execution is hard-disabled."""
import hashlib
import json
import math
import os
from pathlib import Path
from fixed_product_dev.arm_stage import bound_paths
from process_guard import Receipt

SCHEDULE=(('eval-two-pair-a',('P0','CANDIDATE')),('eval-two-pair-b',('CANDIDATE','P0')),
          ('eval-two-pair-c',('P0','CANDIDATE')),('eval-two-pair-d',('CANDIDATE','P0')))
CAPS={'materialize':4,'env_construct':8,'env_init':8,'reset':8,'model_load':8,'generation':400,'step':400}
TOKEN_CAPS={'input':400*4096,'output':400*16}
ARM_CAPS={'env_construct':1,'env_init':1,'reset':1,'model_load':1,'generation':50,'step':50}
class Stop(RuntimeError):pass

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(x):return hashlib.sha256(x).hexdigest()

def digest_file(path):
    # This is followed by bound_paths which performs nofollow and stable-stat checks.
    return sha(Path(path).read_bytes())

def read_child_rows(path):
    """Read a chained child-claimed journal. Not authenticated physical evidence."""
    raw=Path(path).read_bytes()
    if not raw or not raw.endswith(b'\n'):raise Stop('unclosed child journal')
    rows=[];prev='0'*64
    for i,line in enumerate(raw.splitlines(keepends=True)):
        row=json.loads(line);h=row.pop('digest')
        if row['seq']!=i or row['previous']!=prev or sha(canonical(row))!=h:raise Stop('child journal chain')
        prev=h;row['digest']=h;rows.append(row)
    return raw,rows

def claimed_prepared(path):
    raw,rows=read_child_rows(path)
    last_return=max((r['seq'] for r in rows if r['kind']=='generation_returned'),default=-1)
    pending=[r for r in rows if r['kind']=='prepared' and r['seq']>last_return]
    if len(pending)!=1 or any(r['kind']=='generation_started' and r['seq']>last_return for r in rows):
        raise Stop('missing, duplicate or already started prepared claim')
    row=pending[0];data=row['payload'];ids=data.get('input_ids');mask=data.get('attention_mask');kw=data.get('kwargs');config=data.get('generation_config')
    expected_kw={'max_new_tokens':16,'do_sample':False,'num_beams':1,'num_return_sequences':1,
                 'return_dict_in_generate':True,'output_scores':True}
    if (set(data)!={'public','rendered_prompt','input_ids','attention_mask','generation_config','kwargs','eos_ids'} or
        type(ids) is not list or not 1<=len(ids)<=4096 or any(type(x) is not int or x<0 for x in ids) or
        type(mask) is not list or len(mask)!=len(ids) or any(type(x) is not int or x!=1 for x in mask) or
        type(kw) is not dict or canonical(kw)!=canonical(expected_kw) or
        type(config) is not dict or config.get('eos_token_id')!=[151645,151643] or
        type(config.get('pad_token_id')) is not int or config['pad_token_id']!=151643 or
        'forced_eos_token_id' not in config or config['forced_eos_token_id'] is not None or
        data['eos_ids']!=[151645,151643] or type(data['rendered_prompt']) is not str or not data['rendered_prompt']):
        raise Stop('prepared input or generation limit mismatch')
    public=data['public']
    if (type(public) is not dict or set(public)!={'goal','observation','recent_history','valid_actions','public_prompt','public_prompt_sha256','action_map'} or
        type(public['public_prompt']) is not str or not public['public_prompt'] or
        public['public_prompt_sha256']!=sha(public['public_prompt'].encode()) or
        type(public['valid_actions']) is not list or not public['valid_actions'] or
        any(type(x) is not str or not x for x in public['valid_actions']) or
        len(set(public['valid_actions']))!=len(public['valid_actions']) or
        public['action_map']!={'A%03d'%i:action for i,action in enumerate(public['valid_actions'])}):
        raise Stop('public prompt or action map claim mismatch')
    return {'seq':row['seq'],'digest':row['digest'],'input_ids':ids}

def claimed_receipt(path,operation,seq,receipt):
    """Verify format/chain and operation-start/return; child claims are not physical proof."""
    raw,rows=read_child_rows(path);last=rows[-1]
    if (sha(raw.splitlines(keepends=True)[-1])!=receipt or last['kind']!=operation+'_returned' or
        last['payload'].get('owner_seq')!=seq):raise Stop('child return binding')
    found=[r for r in rows if r['kind']==operation+'_started' and r['payload'].get('owner_seq')==seq]
    if len(found)!=1:raise Stop('child start missing/duplicate')
    return last['payload'].get('evidence'),rows

class GlobalOwner:
    def __init__(self,root):
        self.root=Path(root)
        self.root.mkdir(mode=0o700,parents=True,exist_ok=False)
        fd=os.open(self.root/'claim',os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW,0o600)
        try:os.write(fd,b'RESEARCH HOLD; NO RESUME\n');os.fsync(fd)
        finally:os.close(fd)
        self.path=self.root/'global.jsonl'
        fd=os.open(self.path,os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW,0o600)
        try:os.fsync(fd)
        finally:os.close(fd)
        self.counts={k:0 for k in CAPS};self.local={};self.returned_ops={};self.seq=0;self.prev='0'*64
        self.pair_index=0;self.arm_index=0;self.binding=None;self.active=None;self.failed=False
        self.initial=None;self.initial_case=None;self.reset_checked=set();self.worker_log=None;self.current=None;self.setup_used=set()
        self.closed=set();self.completed=False;self.tokens={'input':0,'output':0};self.pending_prepared=None;self.used_prepared=set()
    def record(self,event,payload):
        if self.completed:raise Stop('owner closed')
        row={'seq':self.seq,'previous':self.prev,'event':event,'payload':payload}
        h=sha(canonical(row));line=canonical(dict(row,digest=h))+b'\n'
        fd=os.open(self.path,os.O_APPEND|os.O_WRONLY|os.O_NOFOLLOW)
        try:
            view=memoryview(line)
            while view:
                n=os.write(fd,view)
                if n<=0:raise OSError('short write')
                view=view[n:]
            os.fsync(fd)
        finally:os.close(fd)
        dfd=os.open(self.root,os.O_RDONLY|os.O_DIRECTORY)
        try:os.fsync(dfd)
        finally:os.close(dfd)
        self.seq+=1;self.prev=h
    def abort(self,reason):
        if self.failed:return
        try:self.record('aborted',{'reason':str(reason),'active':self.active})
        except BaseException:pass
        finally:self.failed=True
    def expected(self):
        if self.failed or self.completed or self.pair_index>=len(SCHEDULE):raise Stop('not runnable')
        return SCHEDULE[self.pair_index]
    def materialize_pair(self,case,inputs,materialize,verify):
        try:
            if case!=self.expected()[0] or self.active or self.binding or case in self.setup_used or self.counts['materialize']>=4:
                raise Stop('out-of-order setup')
            self.initial=None;self.initial_case=case
            output=self.root/('pair-'+str(self.pair_index));output.mkdir(mode=0o700)
            ticket={'case':case,'operation':'materialize'}
            self.record('reserve',ticket);self.counts['materialize']+=1;self.setup_used.add(case);self.active=ticket
            def journal(event,payload):self.record('setup_detail',{'event':event,'payload':payload})
            game,config,data_root=materialize(output,inputs,journal,family='two')
            verify(game,config,data_root,inputs,journal,'pre')
            binding={'root':str(output),'game':str(game),'config':str(config),'data_root':str(data_root),
                     'sha256':{'game':digest_file(game),'routing':digest_file(Path(game).parent/'traj_data.json'),'config':digest_file(config)}}
            bound_paths(binding)
            self.record('returned',dict(ticket,binding=binding));self.active=None;self.binding=binding
            return binding
        except BaseException as error:
            self.abort(type(error).__name__+': '+str(error));raise
    def begin_arm(self,case,arm,worker_journal,inputs,verify):
        try:
            expected,order=self.expected()
            if case!=expected or self.binding is None or self.active or arm!=order[self.arm_index] or self.current is not None:
                raise Stop('out-of-order arm')
            def journal(event,payload):self.record('verification_detail',{'event':event,'payload':payload})
            paths=bound_paths(self.binding);verify(*paths,inputs,journal,'pre');bound_paths(self.binding)
            self.current=(case,arm);self.worker_log=Path(worker_journal);self.local[self.current]={k:0 for k in ARM_CAPS};self.returned_ops[self.current]={k:0 for k in ARM_CAPS}
            self.record('arm_started',{'case':case,'arm':arm,'binding':self.binding})
        except BaseException as error:
            self.abort(type(error).__name__+': '+str(error));raise
    def reserve(self,case,arm,operation,seq):
        try:
            if self.failed or self.current!=(case,arm) or self.active or operation not in ARM_CAPS:raise Stop('invalid operation')
            if self.counts[operation]>=CAPS[operation] or self.local[self.current][operation]>=ARM_CAPS[operation]:raise Stop('budget exceeded')
            prerequisite={'env_init':'env_construct','reset':'env_init','model_load':'reset','generation':'model_load','step':'generation'}
            if operation in prerequisite and self.returned_ops[self.current][prerequisite[operation]]<1:raise Stop('operation order')
            if operation=='model_load' and self.current not in self.reset_checked:raise Stop('reset comparison not passed')
            ticket={'case':case,'arm':arm,'operation':operation,'seq':seq}
            if operation=='generation':
                prepared=claimed_prepared(self.worker_log)
                key=(case,arm,prepared['seq'],prepared['digest'])
                if key in self.used_prepared:raise Stop('prepared claim reused')
                # Conservative upper bound: never refund even for smaller child claims.
                if self.tokens['input']+4096>TOKEN_CAPS['input'] or self.tokens['output']+16>TOKEN_CAPS['output']:
                    raise Stop('global token reservation exceeded')
                ticket.update({'prepared_seq':prepared['seq'],'prepared_digest':prepared['digest'],
                               'input_tokens_reserved':4096,'output_tokens_reserved':16})
            self.record('reserve',ticket);self.counts[operation]+=1;self.local[self.current][operation]+=1;self.active=ticket
            if operation=='generation':
                self.tokens['input']+=4096;self.tokens['output']+=16
                self.pending_prepared=prepared;self.used_prepared.add(key)
        except BaseException as error:
            self.abort(type(error).__name__+': '+str(error));raise
    def returned(self,case,arm,operation,seq,receipt):
        try:
            ticket={'case':case,'arm':arm,'operation':operation,'seq':seq}
            if self.failed or self.active is None or any(self.active.get(k)!=v for k,v in ticket.items()):raise Stop('unmatched return')
            evidence,rows=claimed_receipt(self.worker_log,operation,seq,receipt)
            if operation=='generation':
                p=self.pending_prepared
                if p is None or rows[p['seq']]['digest']!=p['digest'] or rows[p['seq']]['kind']!='prepared':raise Stop('prepared claim changed')
                if type(evidence) is not dict:raise Stop('generation claim shape')
                sequence=evidence.get('sequence');out=evidence.get('output_ids');shape=evidence.get('shape')
                if (type(sequence) is not list or type(out) is not list or not 1<=len(out)<=16 or
                    any(type(x) is not int or x<0 for x in sequence+out) or
                    sequence!=p['input_ids']+out or type(shape) is not list or len(shape)!=2 or
                    any(type(v) is not int for v in shape) or shape!=[1,len(sequence)]):raise Stop('generation claim mismatch')
            self.record('returned',dict(self.active,receipt_sha256=receipt,child_claim_only=True));self.active=None
            self.returned_ops[self.current][operation]+=1
            if operation=='generation':self.pending_prepared=None
            if operation=='reset':
                if type(evidence) is not dict or set(evidence)!={'arm','state','gamefile','candidate_native_reset'} or evidence['arm']!=arm or evidence['gamefile']!=self.binding['game']:
                    raise Stop('reset evidence binding')
                native=evidence['candidate_native_reset'];state=evidence['state']
                if (type(native) is not dict or set(native)!={'won_batch','won_batch_type'} or
                    type(native['won_batch']) is not list or len(native['won_batch'])!=1 or native['won_batch'][0] is not False or
                    native['won_batch_type'] not in ('list','tuple') or type(state) is not dict):raise Stop('reset claim malformed')
                if (set(state)!={'task_id','family','goal','observation','valid_actions','done','reward','truncated'} or
                    any(type(state[k]) is not str or not state[k] for k in ('task_id','family','goal','observation')) or
                    type(state['valid_actions']) is not list or not state['valid_actions'] or
                    any(type(x) is not str or not x for x in state['valid_actions']) or
                    len(set(state['valid_actions']))!=len(state['valid_actions']) or
                    state['done'] is not False or state['truncated'] is not False or type(state['reward']) not in (int,float) or not math.isfinite(state['reward'])):
                    raise Stop('public reset shape')
                if self.initial_case!=case:raise Stop('reset case binding')
                if self.initial is None:self.initial=state
                elif canonical(state)!=canonical(self.initial):raise Stop('initial mismatch')
                self.record('reset_claim_accepted',{'case':case,'arm':arm,'child_claim_only':True});self.reset_checked.add((case,arm))
        except BaseException as error:
            self.abort(type(error).__name__+': '+str(error));raise
    def close_arm_after_cleanup(self,case,arm,receipt,inputs,verify):
        try:
            if (self.failed or self.current!=(case,arm) or self.active or
                type(receipt) is not Receipt or receipt.returncode!=0 or receipt.visible_group_members):
                raise Stop('cleanup observation missing or incomplete')
            expected,order=self.expected()
            if case!=expected or arm!=order[self.arm_index] or (case,arm) not in self.reset_checked:
                raise Stop('close order or reset not checked')
            def journal(event,payload):self.record('verification_detail',{'event':event,'payload':payload})
            paths=bound_paths(self.binding);verify(*paths,inputs,journal,'post');bound_paths(self.binding)
            raw,rows=read_child_rows(self.worker_log)
            outcomes=[r['payload'] for r in rows if r['kind']=='fixed_product_arm_result']
            if len(outcomes)!=1:raise Stop('child result missing or duplicate')
            result=outcomes[0]
            if (type(result) is not dict or result.get('arm')!=arm or type(result.get('won')) is not bool or
                type(result.get('steps')) is not int or not 0<=result['steps']<=50 or
                canonical(result.get('initial_public'))!=canonical(self.initial)):
                raise Stop('child result shape or reset mismatch')
            self.record('arm_closed',{'case':case,'arm':arm,'cleanup':receipt.__dict__,
                                      'child_result_claim':result,'physical_proof':False})
            self.closed.add((case,arm));self.current=None;self.worker_log=None;self.arm_index+=1
            if self.arm_index==2:
                self.record('pair_closed',{'case':case,'scope':'child claims only'})
                self.pair_index+=1;self.arm_index=0;self.binding=None;self.initial=None;self.initial_case=None
        except BaseException as error:
            self.abort(type(error).__name__+': '+str(error));raise

    def complete(self):
        try:
            expected={(case,arm) for case,order in SCHEDULE for arm in order}
            if (self.failed or self.active or self.current or self.pair_index!=4 or self.closed!=expected or
                self.setup_used!={case for case,_ in SCHEDULE} or self.counts['materialize']!=4):
                raise Stop('incomplete or unknown batch')
            self.record('synthetic_batch_complete',{'counts':self.counts,'tokens_reserved':self.tokens,
                        'scope':'child claims only; not scientific acceptance'})
            self.completed=True
        except BaseException as error:
            self.abort(type(error).__name__+': '+str(error));raise
