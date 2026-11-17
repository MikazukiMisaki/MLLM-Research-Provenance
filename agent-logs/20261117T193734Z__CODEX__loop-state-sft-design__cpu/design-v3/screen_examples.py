"""Purely fictional arithmetic of proposed screen; no scientific outcomes."""
from fractions import Fraction
def screening(p0,target,control):
    assert len(p0)==len(target)==len(control)==16
    if any(type(v) is not int or v not in (0,1) for v in p0):return 'INCOMPLETE'
    if any(len(t)!=3 or len(c)!=3 or any(type(v) is not int or v not in (0,1) for v in t+c)
           for t,c in zip(target,control)):return 'INCOMPLETE'
    delta_control=sum((Fraction(sum(t)-sum(c),3) for t,c in zip(target,control)),Fraction())/16
    delta_p0=sum((Fraction(sum(t),3)-p for t,p in zip(target,p0)),Fraction())/16
    harms=sum(sum(a<b for a,b in zip(t,c))>=2 for t,c in zip(target,control))
    return 'CONSIDER_FOLLOWUP' if delta_control>=Fraction(1,16) and delta_p0>=Fraction(1,16) and harms<=2 else 'STOP'
def rows(n):return [[1 if i<n else 0]*3 for i in range(16)]
assert screening([1]*16,rows(9),rows(8))=='STOP'
assert screening([1]*8+[0]*8,rows(10),rows(9))=='CONSIDER_FOLLOWUP'
unknown=rows(10);unknown[0][0]=None
assert screening([1]*8+[0]*8,unknown,rows(9))=='INCOMPLETE'
print('fictional checks passed: saturated P0 stops; defined improvement screens; UNKNOWN incomplete')
