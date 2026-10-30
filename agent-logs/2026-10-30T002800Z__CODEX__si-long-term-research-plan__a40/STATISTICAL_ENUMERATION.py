import hashlib,itertools,json,math
from pathlib import Path
O=Path(__file__).parent
src=Path('/home/lizening/research-notes/agent-logs/2026-10-30T003000Z__CODEX__si-scene-independent-recount/INDEPENDENT_SCENE_RECOUNT.json')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
x=json.loads(src.read_text());remaining=x['candidate']['union_parents']-x['union_parent_suffix_overlap']['union'];assert remaining==4
# Observational unit is a paired binary outcome per arm, per parent; ties in a given pair have no discordance.
def exact_p(w,l):
 d=w+l
 return 1.0 if not d else min(1.0,2*sum(math.comb(d,i) for i in range(min(w,l)+1))/2**d)
def holm(p,q):
 ordered=sorted([(p,0),(q,1)]); adj=[None,None]; adj[ordered[0][1]]=min(1.0,2*ordered[0][0]);adj[ordered[1][1]]=min(1.0,max(2*ordered[0][0],ordered[1][0]));return adj
rows=[]
for n in range(1,remaining+1):
 tested=0;lowest=1.;one=both=0;pairs=set()
 for units in itertools.product(itertools.product((0,1),repeat=3),repeat=n):
  ca=[0,0];cb=[0,0]
  for a,b,c in units:
   if c>a:ca[0]+=1
   if c<a:ca[1]+=1
   if c>b:cb[0]+=1
   if c<b:cb[1]+=1
  p=exact_p(*ca);q=exact_p(*cb);a,b=holm(p,q);lowest=min(lowest,p,q);one+=int(a<=.05 or b<=.05);both+=int(a<=.05 and b<=.05);tested+=1;pairs.add((tuple(ca),tuple(cb)))
 rows.append({'parents':n,'joint_binary_outcome_tables_tested':tested,'unique_joint_discordance_pairs':len(pairs),'minimum_two_sided_exact_p':lowest,'any_Holm_significant':one,'both_Holm_significant':both})
assert rows[-1]['minimum_two_sided_exact_p']==0.125 and all(r['both_Holm_significant']==0 and r['any_Holm_significant']==0 for r in rows)
res={'schema':'SCENE_FOUR_PARENT_SINGLE_SEED_EXACT_ENUMERATION_V1','scope':'conditional on scene label policy from frozen metadata; paired binary C-A and C-B; two-sided exact McNemar, Holm family of two, alpha 0.05; no minimum effect requirement; no model/environment','input_sha256':sha(src),'conditional_metadata_parent_count_upper_bound':remaining,'enumeration':rows,'N4_conditional_cost_upper_if_A_once_B_C_three_seeds_and_horizon_50':{'trajectories':28,'generations':1400,'environment_ops_including_resets':1428,'resets_if_all_start':28,'input_tokens_if_8192_per_generation':11468800,'output_tokens_if_16_per_generation':22400,'limitations':'A separate multiseed illustrative resource formula, not the single-seed decision above; exclude training, initialization/close, engineering and failures; neither availability nor protocol approved.'},'limitations':['The candidate label count is an upper bound conditional on the specific enumerated old data and screening policy; no claim of independence, eligibility, or enough viable tasks.','Proof applies only to the specified paired, single-seed, two-comparison, two-sided exact McNemar plus Holm rule, not arbitrary three-seed or alternative statistical procedures.','Power is zero for even one Holm significance at N<=4 independent of observed outcomes; this is not an effect estimate and does not prove no effect.']}
(O/'ENUMERATION.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(rows,indent=2))
