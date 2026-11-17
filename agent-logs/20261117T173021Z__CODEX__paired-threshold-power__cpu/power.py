"""Single planned binary-pair screen under IID tasks; standard library only.

P(rescue)=(q+d)/2, P(harm)=(q-d)/2; remaining ties. Require observed
(rescue-harm)/n >= 0.10 and exact two-sided McNemar p <= .025. This is
not the joint power of a two-comparison Holm decision or a data analysis.
"""
import json, math

def binomial_pmf(k,n,p):
    if not 0 <= k <= n:return 0.0
    if p == 0:return float(k==0)
    if p == 1:return float(k==n)
    return math.exp(math.lgamma(n+1)-math.lgamma(k+1)-math.lgamma(n-k+1)+k*math.log(p)+(n-k)*math.log1p(-p))

def critical_win_count(m, alpha=0.025):
    # For the symmetric conditional null, the two-sided exact p is twice the
    # upper tail at or above observed wins when wins exceed half discordances.
    tail=0.0
    critical=m+1
    for k in range(m,m//2,-1):
        tail+=binomial_pmf(k,m,0.5)
        if 2*tail <= alpha+1e-14:critical=k
        else:break
    return critical

def power(n, q, delta):
    if not (0<q<1 and -q <= delta <= q):raise ValueError('scenario')
    a=(q+delta)/(2*q)
    result=0.0
    for m in range(n+1):
        bound=math.ceil((10*m+n)/20)  # exact integer threshold 2*k-m >= n/10
        kmin=max(critical_win_count(m),bound)
        prob=sum(binomial_pmf(k,m,a) for k in range(kmin,m+1))
        result+=binomial_pmf(m,n,q)*prob
    return result

if __name__=='__main__':
    print(json.dumps({'assumptions':{'q':0.30,'delta':[0.10,0.15],'samples':[82,200,400,800],'minimum_observed_delta':0.10,'single_comparison_alpha':0.025,'task_independence':'IID assumption only; unverified for project tasks'},'power':{str(d):{str(n):power(n,0.30,d) for n in (82,200,400,800)} for d in (0.10,0.15)}},indent=2))
