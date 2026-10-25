from pathlib import Path
import json,math,hashlib,datetime,subprocess,collections
S=json.loads(Path('/tmp/si_p3_paths.json').read_text());OWN=Path(S['directories']['root']);assert 'si-p3-controlled-experience-design' in str(OWN)
known=Path('/home/lizening/research-notes/agent-logs/2026-10-25T065200Z__LUNA__si-p1-isolation-budget__caae4c/KNOWN_USE_IDENTITIES.json'); cand=Path('/home/lizening/research-notes/agent-logs/2026-10-25T065200Z__SOL__si-p1-protocol-review__caae4c/P0_SCOPE_INCIDENT_SNAPSHOT/SUPPORTED_IDENTITY_CANDIDATES.json');p=json.loads(cand.read_text());a=json.loads(known.read_text())
sets={k:set(v) for k,v in a['registered_identity_members'].items() if isinstance(v,list)};used=set().union(*sets.values());families=['pick_and_place_simple','pick_two_obj_and_place','pick_clean_then_place_in_recep','pick_cool_then_place_in_recep','pick_heat_then_place_in_recep','look_at_obj_in_light']
def fam(x):
 out=[f for f in families if x.startswith(f+'-')];assert len(out)==1;return out[0]
checks={}
for split,rows in p.items():
 ids=[x['identity'] for x in rows];assert len(ids)==len(set(ids));assert not set(ids)&used; assert all(hashlib.sha256(x['identity'].encode()).hexdigest()==x['identity_sha256'] for x in rows)
 checks[split]={'count':len(ids),'family_counts':dict(collections.Counter(fam(x) for x in ids)),'known_use_intersection':0}
inputs=[known,cand];out={'scope':'metadata only; no new task contents read; not a never-viewed certificate','known_use_union':len(used),'group_counts':{k:len(v) for k,v in sets.items()},'complement':checks,'bindings':[{'path':str(x),'bytes':x.stat().st_size,'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in inputs]}
(OWN/'independent_capacity_metadata.json').write_text(json.dumps(out,indent=2)+'\n')
def logbin(n,k,p):
 if p==0:return 1.0 if k==0 else 0.0
 if p==1:return 1.0 if k==n else 0.0
 return math.exp(math.lgamma(n+1)-math.lgamma(k+1)-math.lgamma(n-k+1)+k*math.log(p)+(n-k)*math.log1p(-p))
def mcnum(d,k):return min(2**d,2*sum(math.comb(d,j) for j in range(k+1)))
def power(n,q,delta,alpha,full):
 pwin=(q+delta)/2;ploss=(q-delta)/2;assert 0<=ploss<=pwin<=1
 ans=0.0
 for d in range(n+1):
  pd=logbin(n,d,q)
  if not pd:continue
  den=2**d
  for w in range(d//2+1,d+1):
   l=d-w
   if mcnum(d,l)*int(round(1/alpha))>den:continue
   if full and (100*(w-l)<5*n or 100*l>5*n):continue
   ans+=pd*logbin(d,w,pwin/q)
 return ans
# integer cumulative McNemar table avoids recomputing every binomial sum
M={}
for d in range(601):
 c=0;M[d]=[]
 for j in range(d+1):c+=math.comb(d,j);M[d].append(min(2**d,2*c))
def pwr(n,q,delta,alpha,full):
 s=0.0;factor=int(round(1/alpha))
 for d in range(n+1):
  pd=logbin(n,d,q)
  if pd==0:continue
  for w in range(d//2+1,d+1):
   l=d-w
   if M[d][l]*factor>2**d:continue
   if full and (100*(w-l)<5*n or 100*l>5*n):continue
   s+=pd*logbin(d,w,(q+delta)/(2*q))
 return s
rows=[]
for n in [200,600]:
 for delta,q in [(.05,.05),(.05,.1),(.05,.15),(.05,.2),(.1,.1),(.1,.2),(.1,.3)]:
  v={f'{mode}_alpha{alpha}':pwr(n,q,delta,alpha,mode=='full_value_harm') for mode in ['p_only','full_value_harm'] for alpha in [.025,.05]}
  rows.append({'E':n,'delta_assumed':delta,'discordance_assumed':q,'true_win':(q+delta)/2,'true_loss':(q-delta)/2,**v,'two_comparison_full_event_bounds_if_equal_marginals':[max(0,2*v['full_value_harm_alpha0.025']-1),v['full_value_harm_alpha0.05']]})
# independent small-n exhaustive trinomial crosscheck; net/harm guards exactly same decision
cross=[]
for n,q,delta in [(6,.2,.1),(20,.15,.05)]:
 s=0.0
 for w in range(n+1):
  for l in range(n-w+1):
   d=w+l;rest=n-d
   if w<=l or mcnum(d,l)*40>2**d or 100*(w-l)<5*n or 100*l>5*n:continue
   pw=(q+delta)/2;pl=(q-delta)/2
   prob=math.factorial(n)/(math.factorial(w)*math.factorial(l)*math.factorial(rest))*(pw**w)*(pl**l)*((1-q)**rest)
   s+=prob
 v=pwr(n,q,delta,.025,True);assert abs(s-v)<1e-12;cross.append({'n':n,'q':q,'delta':delta,'trinomial':s,'conditional':v,'abs_difference':abs(s-v)})
(OWN/'independent_acceptance_planning.json').write_text(json.dumps({'scope':'hypothetical homogeneous independent task planning, not estimated from R19; no joint independence assumed; no software/data gate included','full_gate':'positive two-sided exact conditional McNemar at alpha, observed net >=5pp, observed harm<=5%; integer guards','joint_bound':'Frechet sufficient both alpha025 vs necessary each alpha05; equal marginal scenarios; training seed fixed','scenarios':rows,'small_n_independent_crosschecks':cross},indent=2)+'\n')
bud=[]
for n in [96,384,480]:
 bud.append({'acquisition_tasks':n,'source_generations_max':50*n,'teacher_generations_max':2*n,'suffix_generations_max':49*n,'total_generations_max':101*n,'source_resets':n,'replay_resets':n,'source_actions_max':50*n,'replay_plus_teacher_plus_suffix_actions_max':50*n,'environment_operations_including_resets_max':102*n,'generated_token_upper_bound':1640*n,'dependence':'generations = 101-d per task if both full H50 and teacher valid; conservative d>=0; env bound has replay d cancelling remaining suffix; no extra baseline/replay model invocation'})
budget={'acquisition':bud,'evaluation_E600_three_arms':{'episodes':1800,'generations_max':90000,'resets':1800,'actions_max':90000,'environment_operations_with_resets_max':91800,'generated_tokens_max':1440000},'full_acquisition_plus_evaluation_excludes_software_runtime_checks_and_training':{'new_generations_max':138480,'new_operations_with_resets_max':140760,'new_generated_tokens_max':2227200,'historical_R19_plus_these_planned_components_generations':143622,'historical_R19_plus_these_planned_components_environment_operations':148709},'prior_cost_actual':S['actual_cost_carry'],'no_actual_new_science':True}
(OWN/'independent_budget_math.json').write_text(json.dumps(budget,indent=2)+'\n')
print(json.dumps({'capacity':out['complement'],'scenarios':rows,'budget':budget},indent=2))
