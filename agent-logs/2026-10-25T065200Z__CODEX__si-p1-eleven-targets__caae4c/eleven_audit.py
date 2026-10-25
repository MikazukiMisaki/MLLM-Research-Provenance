"""Pure stdlib fixed-eleven evidence audit; no project imports/execution/tokenizer.
Outputs hashes/lineage only; never exports full public prompts or training JSONL.
"""
import collections,datetime,hashlib,json,re,sys
from pathlib import Path
sys.dont_write_bytecode=True
OWN=Path(__file__).resolve().parent
COORD=Path('/home/lizening/research-notes/agent-logs/2026-10-25T065200Z__SOL__si-p1-protocol-review__caae4c')
FROZEN=Path('/home/lizening/wt-r19-g4-consumer-contract-repair')
PROJECT=Path('/home/lizening/Alfworld-Self-Improvement-Project')
RUNTIME=PROJECT/'artifacts/runtime'
R19=Path('/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z')
BINDINGS_PATH=OWN/'input_bindings.json'
BINDINGS=json.loads(BINDINGS_PATH.read_text()) if BINDINGS_PATH.exists() else {}
def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as stream:
  for b in iter(lambda:stream.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def value_sha(value):return hashlib.sha256(json.dumps(value,ensure_ascii=True,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def text_sha(s):return hashlib.sha256(s.encode()).hexdigest()
def register(path):
 p=Path(path);k=str(p)
 if k not in BINDINGS:BINDINGS[k]={'path':k,'bytes':p.stat().st_size,'sha256_before':sha(p)}
 return p
def readjson(p):return json.loads(register(p).read_text())
def streamrows(p):
 with register(p).open('rb') as stream:
  for n,l in enumerate(stream,1):
   if l.strip():yield n,hashlib.sha256(l).hexdigest(),json.loads(l)
def savebindings():
 for k,v in BINDINGS.items():
  v['sha256_after']=sha(k);v['unchanged']=v['sha256_before']==v['sha256_after']
  if not v['unchanged']:raise RuntimeError('Original input changed '+k)
 BINDINGS_PATH.write_text(json.dumps(BINDINGS,indent=2)+'\n')
def cases():
 p=register(COORD/'FIXED_ELEVEN_CASES.json')
 if sha(p)!='e5039568d8213fa5d879ffb2aec8c44e932fa99bc4de67bd527ebcae67ccb45b':raise RuntimeError('fixed list mismatch')
 return json.loads(p.read_text())['cases']
def rawcases():
 out={}
 for c in cases():
  for n,h,r in streamrows(c['source_path']):
   if n==c['source_line']:
    if h!=c['source_row_sha256'] or r['prefix_id']!=c['prefix_id']:raise RuntimeError('Raw index mismatch '+c['case_id'])
    out[c['case_id']]=(c,r);break
  else:raise RuntimeError('Missing fixed line')
 return out
SOURCES={
 'R4':RUNTIME/'validation/sft-recovery-source-pool-r1-20260908T042933Z/trajectories.jsonl',
 'R10_OSR':RUNTIME/'validation/persistent-recovery-source-pool-r7-20260909T000000Z/trajectories.jsonl',
 'R16_OSR':RUNTIME/'validation/progress-aware-recovery-r14-20260910T000000Z/raw_trajectories.jsonl',
 'R19_K1':R19/'source_trajectories.jsonl'}
def canonical(t):
 parts=str(t).rstrip('/').split('/')
 for j in range(len(parts)-1,0,-1):
  if parts[j].startswith('trial_'):return parts[j-1]+'/'+parts[j]
 return str(t)
def sourcecases():
 wanted=collections.defaultdict(set)
 for c in cases():wanted[c['stage']].add(c['canonical_task'])
 out={}
 for stage,p in SOURCES.items():
  for n,h,r in streamrows(p):
   t=canonical(r['task']['task_id'])
   if t in wanted[stage]:out[(stage,t)]=(n,h,r)
 return out
def outline(v,depth=0):
 if isinstance(v,dict):return {k:outline(x,depth+1) for k,x in v.items()} if depth<3 else {'keys':list(v)}
 if isinstance(v,list):return {'length':len(v),'first':outline(v[0],depth+1) if v else None}
 if isinstance(v,str):return {'chars':len(v),'value':v if depth<2 and len(v)<120 else None}
 return v
def probe():
 src=sourcecases();out={}
 for cid,(c,r) in rawcases().items():
  n,h,s=src[(c['stage'],c['canonical_task'])];d=c['decision_index'];step=s['steps'][d]
  result={'case':c,'source_line':n,'source_row_sha256':h,'task':s['task'],'metadata_schema':outline(s['metadata']),'step_schema':outline(step),'row_schema':outline(r)}
  out[cid]=result
  print(cid,'source',n,'d',d,'stepkeys',list(step),'metadata',list(step.get('metadata',{})))
  if c['stage']=='R4':rf=r['raw_generations']['recovery'];print('R4stage2',json.dumps(outline(rf['stage_two'])));print('R4recover',json.dumps(outline(r['recover'])))
  elif c['stage'] in ('R10_OSR','R16_OSR'):
   print('replaykeys',list(r.get('replay_full',r.get('replay',{}))));print('terminal',json.dumps(outline(r['continuation_full']['steps'][-1] if r['continuation_full']['steps'] else None)));print('stage2keys',list(r['recovery_full']['stage_two']));print('sourcemeta',json.dumps(outline(step['metadata'])))
  else:print('K1',json.dumps(outline(r['k_results']['1'])));print('source step meta',json.dumps(outline(step['metadata'])))
 (OWN/'probe.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 savebindings()
def evidence_probe():
 for label,p in [('R3_REPLAY',RUNTIME/'validation/sft-recovery-replay-continue-r3-20260908T055308Z/replay_validation.jsonl'),('R16_REPLAY',RUNTIME/'validation/progress-aware-recovery-r16-osr-20260910T000000Z/replay_ledger.jsonl')]:
  n,h,r=next(streamrows(p));print(label,'keys',list(r));print(label,'schema',json.dumps(outline(r)))
 rows=rawcases();c,r=next((c,r) for c,r in rows.values() if c['stage']=='R19_K1');arm=r['k_results']['1'];ids={r['evidence_refs']['prefix_attempt_event_id']}
 for val in arm['evidence_refs'].values():ids.update(val if isinstance(val,list) else [])
 ids.update(arm['replay_evidence']['replay_transition_event_ids'][:1]);seen=set()
 for n,h,e in streamrows(R19/'execution_events.jsonl'):
  if e['event_id'] not in ids:continue
  label=(e['kind'],e.get('identity',{}).get('component'))
  if label in seen:continue
  seen.add(label);print('R19EVENT',label,'line',n,'payload_schema',json.dumps(outline(e['payload'])))
 for st in ['R4','R10_OSR','R16_OSR']:
  c,r=next((c,r) for c,r in rows.values() if c['stage']==st)
  m=readjson(Path(c['source_path']).parent/'run_manifest.json')
  print('MANIFEST',st,json.dumps({k:v for k,v in m.items() if any(x in k for x in ['revision','model','adapter','isolation','operator','generation','horizon'])}))
 savebindings()

def review_summary():
 obj=json.loads((OWN/'eleven_target_audit.json').read_text())
 for x in obj['cases']:
  t=x['terminal_corroboration'];c=t['CONTINUE_terminal'];r=t['recovery_branch_terminal']
  print(x['case_id'],'CONTINUE',c['done'],c['reward'],c['won_entries'],'RECOVER',r['done'],r['reward'],r['won_entries'],'tokens',json.dumps(x['recorded_tokens']))
 print('SAME_PUBLIC_INPUT',json.dumps(obj['same_public_input_groups']))
 print('SAME_SUFFIX',json.dumps(obj['same_semantic_suffix_groups']))
 print('SUMMARY',json.dumps(obj['summary']))
 print('INPUT_FILES',len(BINDINGS),'OUTPUT_BYTES',(OWN/'eleven_target_audit.json').stat().st_size)

if __name__=='__main__':
 if sys.argv[1:]==['probe']:probe()
 elif sys.argv[1:]==['evidence_probe']:evidence_probe()
 elif sys.argv[1:]==['review_summary']:review_summary()
 elif sys.argv[1:]==['documents']:
  from deliver_eleven import documents
  documents(globals())
 elif sys.argv[1:]==['finalize']:
  from freeze_eleven import finalize
  finalize(globals())
 elif sys.argv[1:]==['seal']:
  from freeze_eleven import seal
  seal(globals())
 elif sys.argv[1:]==['history']:
  from history_contracts import run
  run(globals())
 elif sys.argv[1:]==['audit']:
  from target_audit_impl import audit
  audit(globals())
 else:raise SystemExit('mode not supported')
