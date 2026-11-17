"""Illustrative joint two-comparison Holm power under explicit task coupling.

Only simulated IID task outcomes; no research tasks, model, GPU or environment.
"""
import json, math, random

def p_table(n):
    table=[]
    for m in range(n+1):
        # Index k is C-only successes, m-k is other-arm-only successes.
        vals=[]
        for k in range(m+1):
            tail=sum(math.comb(m,j) for j in range(max(k,m-k),m+1))
            vals.append(min(1.0, math.ldexp(float(tail),1-m)))
        table.append(vals)
    return table

def simulate(n, dependence, runs, seed):
    rng=random.Random(seed); p=p_table(n)
    both=single_a=single_b=0
    for _ in range(runs):
        wa=la=wb=lb=0
        for _ in range(n):
            c=rng.random()<.5
            # True joint is an explicitly selected construction, not observed.
            pa=.45 if c else .15
            a=rng.random()<pa
            b=a if dependence=='same_given_c' else rng.random()<pa
            if c:
                wa+=a; wb+=b
            else:
                la+=a; lb+=b
        p1,p2=p[wa+la][wa],p[wb+lb][wb]
        min1=(wa-la)*10>=n
        min2=(wb-lb)*10>=n
        single_a+=min1 and p1<=.025+1e-15
        single_b+=min2 and p2<=.025+1e-15
        both+=min1 and min2 and min(p1,p2)<=.025+1e-15 and max(p1,p2)<=.05+1e-15
    return {'n':n,'dependence':dependence,'runs':runs,'seed':seed,'joint_success_count':both,'joint_power':both/runs,'mc_standard_error':math.sqrt((both/runs)*(1-both/runs)/runs),'single_A_conservative':single_a/runs,'single_B_conservative':single_b/runs}

if __name__=='__main__':
    print(json.dumps({'q_per_comparison':.3,'delta_per_comparison':.15,'p_C':.5,'required_observed_delta':.10,'p_method':'two-sided exact McNemar; Holm both','scenario_note':'conditional on C, each comparison has disagreement .45 when C=1 and .15 when C=0. Dependence independent or identical conditional on C.', 'results':[simulate(n,dep,20000,20261117+n+(0 if dep=='independent_given_c' else 10000)) for n in (82,200) for dep in ('independent_given_c','same_given_c')]},indent=2))
