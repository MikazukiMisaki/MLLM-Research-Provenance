import math
from math import comb

def power(n,a,b):
 q=a+b;p=a/q;total=0
 for m in range(1,n+1):
  pm=comb(n,m)*q**m*(1-q)**(n-m)
  tails=[];s=0
  for j in range(m//2+1):
   s+=comb(m,j);tails.append(min(1,2*s/(2**m)))
  for k in range(m+1):
   if tails[min(k,m-k)]<=.05+1e-14:
    total+=pm*comb(m,k)*p**k*(1-p)**(m-k)
 return total
for a,b in ((.20,.05),(.15,.05)):
 for n in (80,120,160,200):print('assumed',a,b,'n',n,'two_sided_exact_power',round(power(n,a,b),6))
for n,m,k in ((80,20,16),(120,30,24)):
 delta=.15;q=.25;se=math.sqrt((q-delta**2)/n);pv=min(1,2*sum(comb(m,j) for j in range(m-k+1))/(2**m));print('illustration',n,'discordants',m,'positive',k,'negative',m-k,'effect',delta,'wald_95',(round(delta-1.96*se,6),round(delta+1.96*se,6)),'exact_two_sided_p',round(pv,6))
for n in (2,80,120):
 print('budget_n',n,'episodes',3*n,'max_generations',150*n,'max_env_reset_step',153*n,'max_input_tokens',614400*n,'max_output_tokens',2400*n,'conditional_model_shard_equiv_gib',round(6*n*16381516776/1024**3,3))

def first_80_percent(a,b):
 q=a+b;p=a/q;rejection=[0.0]
 for m in range(1,301):
  s=0;tails=[]
  for j in range(m//2+1):
   s+=comb(m,j);tails.append(min(1,2*s/2**m))
  rejection.append(sum(comb(m,k)*p**k*(1-p)**(m-k) for k in range(m+1) if tails[min(k,m-k)]<=.05+1e-14))
 for n in range(1,301):
  value=sum(comb(n,m)*q**m*(1-q)**(n-m)*rejection[m] for m in range(1,n+1))
  if value>=.8:return n,value
for a,b in ((.20,.05),(.15,.05)):
 n,v=first_80_percent(a,b);print('assumed',a,b,'first_n_80percent',n,'power',round(v,6))
