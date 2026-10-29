import json,hashlib,sys,math
from pathlib import Path
from collections import Counter
b=Path(__file__).parent.parent;analysis=b/'FINAL_PILOT82_PAIRED_ANALYSIS_C2356.json';out=Path('/home/lizening/research-notes/agent-logs/2026-10-29T145200Z__LUNA__si-u1-production-preflight-proposal__853/run_parent/evaluation_c2356bbda2b44159a333e7c9d24fc2d4');procdir=Path('/home/lizening/research-notes/agent-logs/2026-10-29T224100Z__LUNA__si-u1-approved-extraction__062a')
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for block in iter(lambda:f.read(1048576),b''):h.update(block)
 return h.hexdigest()
assert sha(analysis)=='4a3ea016d4c06022980482ac9dbc58155a68bbe20fbc723a68ce49c7c345ea9b';assert sha(procdir/'PROCESS_RECEIPT.json')=='b3121522e37551451b30bc5611dc744b0dc85f39604dbdf8c6ba65220961c7ee'
a=json.loads(analysis.read_text());process=json.loads((procdir/'PROCESS_RECEIPT.json').read_text());assert type(process['authentic_returncode']) is int and process['authentic_returncode']==0
for p,h in process['input_hashes'].items():assert sha(p)==h
for p,h in a['evidence_hashes'].items():assert sha(p)==h
assert json.loads((procdir/'original_before.json').read_text())==json.loads((procdir/'original_after.json').read_text())
spec=json.loads((b/'EXTRACTION_SPEC_C2356_CANDIDATE_V1.json').read_text());manifest=json.loads(Path(spec['manifest']['path']).read_text());lookup={r['task_id']:r for r in manifest['tasks']}
apppath=Path(process['argv'][process['argv'].index('--approval')+1]);approval=json.loads(apppath.read_text());assert sha(apppath)==a['analysis_approval_sha256'] and approval['extractor_sha256']==process['input_hashes']['/home/lizening/wt-si-u1-result-extractor/si_u1_extract.py']
sys.path.insert(0,'/home/lizening/wt-si-self-imitation-evaluator/src')
from models.protocol_stability import parse_p2_selection
states={};steps=Counter();pending={};outcomes=[];terminations=Counter();selection_failures=0;last=None
for line in (out/'evaluation/events.jsonl').open('rb'):
 r=json.loads(line);kind=r['kind'];p=r['payload'];last=r
 if kind=='unit_completed':
  ident=p['identity'];key=(ident['arm'],ident.get('task_id'));op=ident['op'];data=p['data']
  if op=='reset':states[key]=data;pending[key]=None
  elif op=='generation':pending[key]=parse_p2_selection(data['raw_output'],states[key]['valid_actions'],reflection_required=False)
  elif op=='step':assert pending[key].selection_status=='selected';states[key]=data;steps[key]+=1;pending[key]=None
 elif kind=='episode_closed':
  key=(p['arm'],p['task_id']);st=states[key];invalid=pending[key] is not None and pending[key].selection_status!='selected';ended=st['done'] or st['truncated'];assert ended or steps[key]==50 or invalid
  termination='selection_failure' if invalid else ('terminal' if st['done'] else 'truncated') if ended else 'horizon';value=int(st['done'] and st['reward']>0) if st['done'] else (0 if termination in ('horizon','selection_failure') else None)
  assert type(value) is int and p['outcome']==value and p['end_state']==st and p['steps']==steps[key] and p['termination']==termination and p['seed']==lookup[key[1]]['seed'] and p['family']==lookup[key[1]]['family'];outcomes.append((key,value));terminations[termination]+=1;selection_failures+=int(invalid)
report=json.loads((out/'evaluation/report.json').read_text());assert last['kind']=='run_closed' and last['payload']==report and len(outcomes)==246 and report['pending_na']==[]
assert [k for k,v in outcomes]==[(arm,t['task_id']) for arm in ('A','B','C') for t in manifest['tasks']]
values=dict(outcomes);pairs=[{'task_id':t['task_id'],'family':t['family'],**{arm:bool(values[(arm,t['task_id'])]) for arm in ('A','B','C')}} for t in manifest['tasks']];assert pairs==a['paired_records']
counts={arm:sum(p[arm] for p in pairs) for arm in ('A','B','C')};assert counts==a['overall_successes']
contrasts={}
for label,other in [('C-A','A'),('C-B','B')]:
 w=sum(p['C'] and not p[other] for p in pairs);loss=sum(p[other] and not p['C'] for p in pairs);m=w+loss;pv=min(1.0,2*sum(math.comb(m,i) for i in range(min(w,loss)+1))/2**m) if m else 1.0
 c=a['statistics']['contrasts'][label];assert (c['wins'],c['losses'],c['ties'])==(w,loss,82-m) and c['mcnemar_two_sided_p']==pv;contrasts[label]={'wins':w,'losses':loss,'delta':(w-loss)/82,'p':pv}
sortedp=sorted(contrasts,key=lambda k:contrasts[k]['p']);running=0
for i,k in enumerate(sortedp):running=max(running,min(1,(2-i)*contrasts[k]['p']));assert running==a['statistics']['contrasts'][k]['holm_adjusted_p']
families={}
for family in sorted({p['family'] for p in pairs}):
 rows=[p for p in pairs if p['family']==family];d={'n':len(rows),'A_success':sum(p['A'] for p in rows),'B_success':sum(p['B'] for p in rows),'C_success':sum(p['C'] for p in rows)};d['C_minus_A']=(d['C_success']-d['A_success'])/d['n'];assert d==a['statistics']['families'][family];families[family]=d
warning=any(10*(c['wins']-c['losses'])<=-82 for c in contrasts.values()) or any(10*(d['C_success']-d['A_success'])<=-d['n'] for d in families.values());large=all(a['statistics']['contrasts'][k]['holm_adjusted_p']<=.05 and 10*(c['wins']-c['losses'])>=82 for k,c in contrasts.items());decision='UNFAVORABLE_WARNING' if warning else 'LARGE_EFFECT_SIGNAL' if large else 'INCONCLUSIVE';assert decision==a['statistics']['decision']
assert not a['statistics']['five_pp_nonharm_supported_under_inference_assumptions']
r={'status':'INDEPENDENT_RECONSTRUCTION_PASS','analysis_sha256':sha(analysis),'process_sha256':sha(procdir/'PROCESS_RECEIPT.json'),'paired_rows':82,'episodes':246,'successes':counts,'rates':{k:v/82 for k,v in counts.items()},'contrasts':contrasts,'families':families,'termination_counts':dict(terminations),'selection_failures':selection_failures,'decision':decision,'five_pp_nonharm_established':False,'evidence_hashes_verified':len(a['evidence_hashes']),'all_actual_approval_and_process_input_hashes_verified':True,'method':'Independent stream last-state/selection/termination reconstruction and integer exact-binomial/Holm/threshold recomputation; no extractor rerun, model or environment.'}
Path(__file__).with_name('RESULT_V2.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r))
