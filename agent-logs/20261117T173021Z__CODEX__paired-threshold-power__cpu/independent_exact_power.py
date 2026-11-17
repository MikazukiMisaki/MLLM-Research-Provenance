"""Exact integer arithmetic for a single paired binary contrast; no input data."""
from fractions import Fraction
from math import comb
from decimal import Decimal, localcontext

def power(n, win, lose, common=40):
    agree = common - win - lose
    threshold = (n + 9) // 10  # exact ceil(0.10*n), in integer wins-minus-losses
    numerator = 0
    for k in range(n + 1):
        # P_two-sided = 2 * P(Bin(k,.5) >= w) for w > k/2.
        # Two-sided p <= 1/40 iff 80 * integer upper tail <= 2**k.
        tail = 0
        accepted_weight = 0
        for w in range(k, -1, -1):
            coefficient = comb(k, w)
            tail += coefficient
            if 2*w-k >= threshold and 80*tail <= 2**k:
                accepted_weight += coefficient * win**w * lose**(k-w)
        numerator += comb(n,k) * agree**(n-k) * accepted_weight
    return Fraction(numerator, common**n)

if __name__ == '__main__':
    with localcontext() as ctx:
        ctx.prec=20
        for win,lose,delta in [(8,4,'0.10'),(9,3,'0.15')]:
            for n in (82,200,400):
                x=power(n,win,lose)
                print(f'q=0.30 delta={delta} n={n} power={Decimal(x.numerator)/Decimal(x.denominator):.12f}')
