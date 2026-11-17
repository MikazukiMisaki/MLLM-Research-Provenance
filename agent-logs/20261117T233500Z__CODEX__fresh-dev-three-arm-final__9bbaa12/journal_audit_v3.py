"""Candidate offline evidence consistency checker; no model or environment execution."""
import collections,hashlib,json,sys
from pathlib import Path
ARMS=('P0','C-old','C-quarter')
CAPS={'environment_construct':36,'cuda_guard':36,'environment_reset':36,'model_load':36,'tokenizer_preview':1800,'model_generation':1800,'environment_step':1800,'environment_close':36,'model_close':36}
VALID={'SUCCESS','POLICY_FAILURE','NATIVE_FAILURE','HORIZON_FAILURE'}
def require(ok,msg):
 if not ok:raise ValueError(msg)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def file_sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def tree_sha(root):
 root=Path(root);require(not root.is_symlink() and root.is_dir(),'tree root');entries=[]
 for p in sorted(root.rglob('*')):
  if p.is_symlink() and not p.is_file():raise ValueError('bad link')
  if p.is_file():entries.append([p.relative_to(root).as_posix(),p.stat().st_size,file_sha(p)])
  elif not p.is_dir():raise ValueError('bad tree node')
 require(bool(entries),'empty tree')
 return sha(json.dumps(entries,ensure_ascii=False,separators=(',',':')).encode())
def canonical(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
def audit(root,manifest_path,expected_sha):
 root=Path(root);manifest_path=Path(manifest_path);mb=manifest_path.read_bytes();require(sha(mb)==expected_sha,'manifest hash');m=json.loads(mb)
 sb=(root/'results/summary.json').read_bytes();eb=(root/'supervisor_exit.json').read_bytes();jb=(root/'results/events.jsonl').read_bytes();s=json.loads(sb);e=json.loads(eb)
 require(m.get('schema')=='THREE_ARM_DEV_V1' and m.get('evidence_class')=='EXPOSED_DEV' and m.get('draft_only') is False and m.get('horizon')==50,'manifest scope')
 require(s.get('status')=='COMPLETE' and s.get('scope')=='EXPOSED_DEV' and s.get('retry') is False and s.get('open_effect') is None and s.get('error') is None,'summary incomplete')
 require(e.get('status')=='EXIT_ZERO_REQUIRES_RESULT_AUDIT' and type(e.get('direct_child_returncode')) is int and e['direct_child_returncode']==0 and 'stop' in e and e['stop'] is None and e.get('spawn_status')=='RETURNED' and e.get('retry') is False,'exit incomplete')
 tasks=m['tasks'];products=m['products'];require(len(tasks)==12 and set(products)==set(ARMS),'manifest roster')
 require(len({t['task_id'] for t in tasks})==12 and len({t['parent_id'] for t in tasks})==12,'manifest duplicate')
 for i,t in enumerate(tasks):
  require(type(t['index']) is int and t['index']==i and type(t['seed']) is int and len(t['arm_order'])==3 and set(t['arm_order'])==set(ARMS),'manifest task')
  require(file_sha(t['game_path'])==t['game_sha256'],'game file hash')
 for a in ARMS:require(tree_sha(products[a]['adapter_path'])==products[a]['adapter_tree_sha256'],'adapter tree hash')
 require(tree_sha(m['runtime']['base_path'])==m['runtime']['base_tree_sha256'],'base tree hash')
 rows=s['rows'];require(len(rows)==12,'summary rows');expected=[]
 for t,r in zip(tasks,rows):
  require(type(r['index']) is int and r['index']==t['index'] and r['arm_order']==t['arm_order'] and set(r['arms'])==set(ARMS) and all(v in VALID for v in r['arms'].values()),'summary roster')
  expected.extend((t['index'],a,pos) for pos,a in enumerate(t['arm_order']))
 lines=jb.splitlines();require(len(lines)>=3,'empty journal');events=[json.loads(l) for l in lines]
 require(all(type(x.get('seq')) is int and x['seq']==i and isinstance(x.get('payload'),dict) for i,x in enumerate(events)),'journal sequence')
 require(events[0]['kind']=='run_started' and events[0]['payload']=={'scope':'EXPOSED_DEV','retry':False,'status':'RUNNING'},'start envelope')
 require(events[1]['kind']=='manifest_binding' and events[1]['payload']=={'canonical_sha256':sha(canonical(m)),'scope':'EXPOSED_DEV'},'manifest binding')
 require(events[-1]['kind']=='run_summary' and events[-1]['payload']==s,'summary journal mismatch')
 counters=collections.Counter();per=collections.Counter();states={};inflight=None;cur=None;started=[];completed=[];had_state=False;terminal=None;decision=None;progress=0;stage='READY';terminal_ended=False;reserved={'input_tokens':0,'output_tokens':0};measured={'input_tokens':0,'output_tokens':0};reservation=None;generation=None
 for ev in events[2:-1]:
  k,p=ev['kind'],ev['payload']
  if k=='episode_started':
   require(cur is None and inflight is None and len(started)<36,'episode overlap');require(type(p.get('index')) is int and type(p.get('order_position')) is int,'episode index type');cur=(p['index'],p['arm'],p['order_position']);require(cur==expected[len(started)],'episode order');i,a,pos=cur;t=tasks[i]
   require(all(p.get(n)==v for n,v in {'task_id':t['task_id'],'parent_id':t['parent_id'],'seed':t['seed'],'game_sha256':t['game_sha256'],'adapter_tree_sha256':products[a]['adapter_tree_sha256']}.items()),'episode binding');started.append(cur);per=collections.Counter();had_state=False;terminal=None;decision=None;progress=0;stage='READY';terminal_ended=False;reservation=None;generation=None
  elif k in ('external_started','external_returned'):
   require(cur is not None,'effect outside episode');op=p.get('operation');ident=p.get('identity');require(op in CAPS and isinstance(ident,dict) and type(ident.get('index')) is int and type(ident.get('order_position')) is int and (ident.get('index'),ident.get('arm'),ident.get('order_position'))==cur,'effect identity')
   if k=='external_started':
    if op in ('tokenizer_preview','model_generation','environment_step'):
     require(type(ident.get('step')) is int and ident['step']==progress and progress<50,'effect step index')
     expected_stage={'tokenizer_preview':'READY','model_generation':'RESERVED','environment_step':'DECIDED'}[op]
     require(stage==expected_stage and (op!='tokenizer_preview' or not terminal_ended),'effect step ordering');stage={'tokenizer_preview':'PREVIEW_STARTED','model_generation':'GENERATION_STARTED','environment_step':'STEP_STARTED'}[op]
    require(inflight is None and p.get('cost')=='STARTED_OR_UNKNOWN','effect overlap');inflight=(op,ident);counters[op]+=1;per[op]+=1;require(counters[op]<=CAPS[op],'effect cap')
   else:
    require(inflight==(op,ident),'unmatched effect');inflight=None
    if op in ('tokenizer_preview','model_generation','environment_step'):
     require(stage=={'tokenizer_preview':'PREVIEW_STARTED','model_generation':'GENERATION_STARTED','environment_step':'STEP_STARTED'}[op],'effect return ordering');stage={'tokenizer_preview':'PREVIEW_RETURNED','model_generation':'GENERATION_RETURNED','environment_step':'STEP_RETURNED'}[op]
  elif k=='initial_state':
   require(cur is not None and inflight is None and not had_state and p.get('identity')=={'index':cur[0],'arm':cur[1],'order_position':cur[2]} and per['environment_reset']==1 and per['model_load']==0,'initial state timing')
   h=p.get('public_state_sha256');require(isinstance(h,str) and len(h)==64 and all(c in '0123456789abcdef' for c in h),'initial state hash');require(cur[0] not in states or states[cur[0]]==h,'paired state mismatch');states[cur[0]]=h;had_state=True
  elif k in ('token_reservation','generation_receipt','decision','transition_raw','transition_classified'):
   require(cur is not None and inflight is None and p.get('identity')=={'index':cur[0],'arm':cur[1],'order_position':cur[2]} and type(p.get('step')) is int and p['step']==progress,'step event identity/index')
   require(stage=={'token_reservation':'PREVIEW_RETURNED','generation_receipt':'GENERATION_RETURNED','decision':'RECEIPT','transition_raw':'STEP_RETURNED','transition_classified':'TRANSITION'}[k],'step event ordering')
   if k=='token_reservation':
    require(p.get('status')=='STARTED_OR_UNKNOWN' and type(p.get('input_tokens')) is int and 1<=p['input_tokens']<=4080 and type(p.get('output_tokens')) is int and p['output_tokens']==16,'token reservation');reservation=p;reserved['input_tokens']+=p['input_tokens'];reserved['output_tokens']+=p['output_tokens'];stage='RESERVED'
   elif k=='generation_receipt':
    require(type(p.get('claimed_input_tokens')) is int and p['claimed_input_tokens']==reservation['input_tokens'] and type(p.get('claimed_output_tokens')) is int and 1<=p['claimed_output_tokens']<16,'generation receipt tokens');generation=p;measured['input_tokens']+=p['claimed_input_tokens'];measured['output_tokens']+=p['claimed_output_tokens'];stage='RECEIPT'
   elif k=='decision':
    require(type(p.get('input_tokens')) is int and p['input_tokens']==generation['claimed_input_tokens'] and type(p.get('output_tokens')) is int and p['output_tokens']==generation['claimed_output_tokens'] and p.get('reserved_output_tokens')==16 and all(p.get(k)==generation.get(k) for k in ('raw_output','parser_status','action','selection')),'decision receipt mismatch');decision=p;stage='DECIDED'
   elif k=='transition_raw':
    actions=decision.get('valid_actions');selection=decision.get('selection');action=decision.get('action')
    require(decision.get('parser_status')=='grounded' and isinstance(actions,list) and actions and all(isinstance(x,str) for x in actions) and isinstance(action,str) and action in actions and p.get('action')==action,'transition action mismatch')
    mapping={f'A{i:03d}':v for i,v in enumerate(actions)}
    require(isinstance(selection,dict) and selection.get('id_to_command')==mapping and selection.get('selection_status')=='selected' and mapping.get(selection.get('parsed_action_id'))==action and selection.get('mapped_environment_command')==action,'selection action-map mismatch')
    terminal=p;stage='TRANSITION'
   else:
    info=terminal.get('native_metadata',{}).get('alfworld_info',{});w=info.get('won');w=w[0] if isinstance(w,list) and len(w)==1 else w
    require(type(w) is bool and type(p.get('native_won')) is bool and p['native_won']==w,'transition classification');terminal_ended=terminal.get('done') is True or progress==49;progress+=1;stage='READY'
  elif k=='episode_completed':
   require(cur is not None and inflight is None and had_state,'completion state');ident={'index':cur[0],'arm':cur[1],'order_position':cur[2]};require(all(p.get(x)==v for x,v in ident.items()),'completion identity')
   require(all(per[x]==1 for x in ('environment_construct','cuda_guard','environment_reset','model_load','environment_close','model_close')) and per['tokenizer_preview']==per['model_generation'] and per['model_generation']>=1 and per['environment_step']<=per['model_generation'],'episode effects')
   outcome=p.get('outcome');require(outcome in VALID and outcome==rows[cur[0]]['arms'][cur[1]],'outcome mismatch')
   if outcome=='POLICY_FAILURE':require(stage=='DECIDED' and per['environment_step']==progress and per['model_generation']==progress+1 and decision is not None and decision.get('parser_status') in ('action_format_violation','action_out_of_range'),'policy failure evidence')
   else:
    require(stage=='READY' and 1<=progress<=50 and per['environment_step']==per['model_generation']==progress and terminal is not None and terminal.get('step')==progress-1 and type(terminal.get('done')) is bool and terminal.get('truncated') is False,'terminal transition and step count')
    info=terminal.get('native_metadata',{}).get('alfworld_info',{});won=info.get('won');won=won[0] if isinstance(won,list) and len(won)==1 else won
    require(type(won) is bool,'won evidence');step=terminal.get('step');require(type(step) is int and 0<=step<50,'terminal step')
    if outcome=='SUCCESS':require(won and terminal['done'],'success evidence')
    elif outcome=='HORIZON_FAILURE':require(not won and step==49 and progress==50,'horizon evidence')
    else:
     lost=info.get('lost');lost=lost[0] if isinstance(lost,list) and len(lost)==1 else lost
     require(not won and terminal['done'] and step<49 and lost is True,'native loss evidence')
   completed.append(cur);cur=None
  else:raise ValueError('unknown or unexpected event kind')
 require(cur is None and inflight is None and len(started)==len(completed)==36 and started==completed and len(states)==12,'incomplete episode ledger')
 require(s.get('token_measurement_complete') is True and s.get('reserved_tokens')==reserved and s.get('known_completed_generation_tokens')==measured,'token totals')
 require(set(s['operation_starts'])==set(CAPS) and all(type(s['operation_starts'][k]) is int and s['operation_starts'][k]==counters[k] for k in CAPS),'operation counts')
 return {'schema':'FRESH_DEV_JOURNAL_AUDIT_V1','status':'PASS','summary_sha256':sha(sb),'supervisor_exit_sha256':sha(eb),'raw_journal_sha256':sha(jb),'manifest_sha256':sha(mb),'episode_starts':len(started),'episode_completions':len(completed),'scope':'integrity and basic outcome evidence only; not proof of process ownership, semantic independence, statistical validity or source authenticity','physical_product_and_task_hashes_rechecked':True}
def main():
 require(len(sys.argv)==5,'usage: audit.py RUN MANIFEST EXPECTED_MANIFEST_SHA OUTPUT')
 out=Path(sys.argv[4]);r=audit(sys.argv[1],sys.argv[2],sys.argv[3])
 with out.open('x') as f:json.dump(r,f,sort_keys=True,indent=2);f.write('\n')
 print(json.dumps(r,sort_keys=True))
if __name__=='__main__':main()
