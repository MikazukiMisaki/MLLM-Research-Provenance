"""Deterministic hypothetical design mathematics only: no data outcomes/project imports."""
import datetime, functools, hashlib, json, math
from fractions import Fraction
from pathlib import Path
OWN=Path(__file__).resolve().parent
ALPHA=Fraction(1,40)  # .025 is sufficient for each of two Holm comparisons.
N_GRID=(60,74,100,200,400,600,1000,1141)
DELTA_GRID=(0.03,0.05,0.10)
Q_GRID=(0.05,0.10,0.20,0.30,0.50)

@functools.lru_cache(None)
def lower_critical(d):
    if d==0:return -1
    den=1<<d;coef=1;cum=0;last=-1
    for k in range(d//2+1):
        if k:coef=coef*(d-k+1)//k
        cum+=coef
        # exact rational 2*cumulative_probability <= alpha
        if 2*cum*ALPHA.denominator<=den*ALPHA.numerator:last=k
        else:break
    return last

def pmf(n,p):
    if p<=0:return [1.0]+[0.0]*n
    if p>=1:return [0.0]*n+[1.0]
    mode=min(n,int((n+1)*p));v=[0.0]*(n+1);v[mode]=1.0
    for k in range(mode,0,-1):v[k-1]=v[k]*k/(n-k+1)*(1-p)/p
    for k in range(mode,n):v[k+1]=v[k]*(n-k)/(k+1)*p/(1-p)
    s=math.fsum(v);return [x/s for x in v]

@functools.lru_cache(None)
def positive_rejection_given_d(d,prob_win_given_discordance):
    cut=lower_critical(d)
    if cut<0:return 0.0
    return math.fsum(pmf(d,prob_win_given_discordance)[d-cut:])

def planned_power(n,q,delta):
    if not abs(delta)<=q<=1:raise ValueError("invalid paired probabilities")
    if q==0:return 0.0
    cond=(q+delta)/(2*q)
    return math.fsum(prob*positive_rejection_given_d(d,cond) for d,prob in enumerate(pmf(n,q)))

def direct_small_n(n,pw,pl):
    ans=0.0
    for w in range(n+1):
        for loss in range(n-w+1):
            discord=w+loss
            if w<=loss or lower_critical(discord)<loss:continue
            coefficient=math.comb(n,w)*math.comb(n-w,loss)
            ans+=coefficient*pw**w*pl**loss*(1-pw-pl)**(n-w-loss)
    return ans

# Meaningful independent arithmetic verification, not tests of project/software policies.
checks={}
checks["all_wins_6_not_at_025"]=lower_critical(6)==-1
checks["all_wins_7_reject_at_025"]=lower_critical(7)==0
checks["certain_wins_7_power_one"]=abs(planned_power(7,1,1)-1)<1e-14
checks["certain_wins_6_power_zero"]=planned_power(6,1,1)==0
a=planned_power(12,.15,.05);b=direct_small_n(12,.10,.05)
checks["conditional_mixture_equals_direct_trinomial"]=abs(a-b)<1e-13
checks["null_positive_tail_at_most_alpha_half"]=all(planned_power(n,q,0)<=float(ALPHA)/2+1e-12 for n in (10,60,74,200) for q in (.05,.2,.5,1))
assert all(checks.values()),checks

rows=[]
for delta in DELTA_GRID:
    for q in Q_GRID:
        if delta>q:continue
        pw=(q+delta)/2;pl=(q-delta)/2
        for n in N_GRID:
            power=planned_power(n,q,delta)
            rows.append({"n":n,"true_delta":delta,"true_discordance_q":q,"p_win":pw,"p_loss":pl,"compatible_reference_success_range":[pl,1-pw],"positive_significant_power_each_comparison":power,"lower_bound_both_statistical_comparisons":max(0,2*power-1),"evaluation_model_generation_cap_if_three_arms_h50":150*n,"evaluation_environment_operation_cap_including_resets":153*n})
out={"schema":"SI_P1_HYPOTHETICAL_EXACT_DESIGN_ENUMERATION_V1","created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"not_a_scientific_policy_experiment":True,"inputs":"hypothetical n/delta/q, no task outcome files read","alpha_each_for_planning":float(ALPHA),"analysis_plan":"final two-sided exact McNemar + Holm for two comparisons at family alpha.05; requiring p<=.025 for each is a conservative sufficient planning event","model_assumptions":["independent paired task draws with homogeneous joint probabilities or explicitly declared reference task model; fixed frozen training snapshots","D~Binomial(n,q), wins|D~Binomial(D,(q+delta)/(2q))","Compatible reference success must lie in [p_loss,1-p_win]; high-q scenarios are not necessarily compatible with an80% baseline"],"limits":["Power is for positive-direction p-value criterion only, not practical-effect/harms/data-integrity/full acceptance gates","Union-bound lower bound uses only two marginal powers; no independence between model comparisons assumed","No q is estimated from old R19, oracle2/36 or target training cases","N values are mathematical scenarios, not certified available identities, approved sample counts or budget","No claim about training-seed variability; exact conditional test is conservative"],"arithmetic_checks":checks,"small_n_crosscheck":{"mixture":a,"direct_trinomial":b},"rows":rows,"new_model_environment_training_calls":0}
(OWN/"hypothetical_power_enumeration.json").write_text(json.dumps(out,indent=2)+"\n")
summary=[r for r in rows if r["true_delta"]==.05 and r["true_discordance_q"] in (.1,.2,.3) and r["n"] in (74,200,600,1000,1141)]
print(json.dumps({"arithmetic_checks":checks,"scenarios":len(rows),"selected_5pp_scenarios":summary},indent=2))
