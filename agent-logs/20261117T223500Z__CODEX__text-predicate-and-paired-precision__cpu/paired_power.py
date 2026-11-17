import json, math, platform
from pathlib import Path

def logpmf(n,k,p):
    return math.lgamma(n+1)-math.lgamma(k+1)-math.lgamma(n-k+1)+k*math.log(p)+(n-k)*math.log1p(-p)

def prob(n,k,p):
    return math.exp(logpmf(n,k,p))

def critical(d,alpha):
    if d == 0: return -1
    c=0.0; threshold=-1
    for k in range(d//2+1):
        c+=prob(d,k,0.5)
        if min(1.0,2*c)<=alpha+1e-14: threshold=k
        else: break
    return threshold

def power(n,q,delta,alpha):
    pp=(1+delta/q)/2
    total=0.0
    for d in range(1,n+1):
        crit=critical(d,alpha)
        if crit<0: continue
        low=sum(prob(d,k,pp) for k in range(crit+1))
        high=sum(prob(d,k,pp) for k in range(d-crit,d+1))
        total+=prob(n,d,q)*(low+high)
    return total

rows=[]
for n in (100,200,400,800):
    for q in (0.2,0.3):
        for delta in (0.05,0.1):
            rows.append({'parents':n,'discordant_fraction_assumed':q,'success_difference_assumed':delta,'power':power(n,q,delta,0.025)})
assert all(0<=x['power']<=1+1e-10 for x in rows)
result={'schema':'paired_power_hypothetical_v1','method':'unconditional exact two-sided McNemar with binomial discordants and binomial direction','alpha_per_comparison':0.025,'assumptions':'independent parent pairs, constant discordance and directional effect; illustrative, not estimated from study','python':platform.python_version(),'rows':rows}
Path(__file__).with_name('result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
