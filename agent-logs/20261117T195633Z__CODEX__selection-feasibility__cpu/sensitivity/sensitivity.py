from decimal import Decimal, localcontext
from math import comb

with localcontext() as ctx:
    ctx.prec=120
    def pmf(n,k,q):return Decimal(comb(n,k)) * q**k * (1-q)**(n-k)
    def cdf_lt16(n,q):return sum((pmf(n,k,q) for k in range(min(n,15)+1)),Decimal(0))
    print('q,all16_probability,predeclared128_probability,predeclared128_failure_probability,expected_number_parents_screened')
    for s in ('0.05','0.10','0.20','0.50','0.80','0.90'):
        q=Decimal(s);fail=cdf_lt16(128,q); success=1-fail
        scanned=sum((cdf_lt16(n,q) for n in range(128)),Decimal(0))
        print(f'{s},{q**16:.12E},{success:.12E},{fail:.12E},{scanned:.4f}')
