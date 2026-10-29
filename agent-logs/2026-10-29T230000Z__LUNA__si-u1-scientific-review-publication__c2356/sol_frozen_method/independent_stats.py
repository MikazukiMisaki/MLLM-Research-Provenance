"""Independent offline paired-statistics recalculation. No model/environment calls.

Scientific input is only permitted after independently authenticated completed-run
extraction; no invalid or partial input is eligible. Uses exact integer binomial
and high-precision decimal CDF inversion, not the preregistered implementation.
"""
import argparse,hashlib,json,math,pathlib
from decimal import Decimal,localcontext
from fractions import Fraction

MANIFEST='7d1b61a9054f99a40fe895c7bb292a81e7a578bbd5fc6bf0777157676213e338'
SCHEDULE='c352a0d708b910bb3703c63009aed3a800b5ba4d40f95021f3bd30db0e4823cd'
RUN='c2356bbda2b44159a333e7c9d24fc2d4'

def reject(msg):raise ValueError(msg)
def exact_json(path,expected):
 p=pathlib.Path(path)
 if not p.is_absolute() or not p.is_file() or p.is_symlink():reject('missing/untrusted bound input')
 raw=p.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=expected:reject('input hash drift')
 def pairs(items):
  out={}
  for k,v in items:
   if k in out:reject('duplicate JSON key')
   out[k]=v
  return out
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:reject('nonfinite JSON'))

def cp(k,n):
 if type(k) is not int or type(n) is not int or not 0<=k<=n or n<1:reject('invalid binomial count')
 with localcontext() as ctx:
  ctx.prec=70
  tail=Decimal(1)/Decimal(160)
  def cdf(j,p):
   return sum((Decimal(math.comb(n,x))*(p**x)*((Decimal(1)-p)**(n-x)) for x in range(j+1)),Decimal(0))
  def inverse(j,target):
   lo,hi=Decimal(0),Decimal(1)
   for _ in range(240):
    mid=(lo+hi)/2
    if cdf(j,mid)>target:lo=mid
    else:hi=mid
   return (lo+hi)/2
  lo=Decimal(0) if k==0 else inverse(k-1,1-tail)
  hi=Decimal(1) if k==n else inverse(k,tail)
  return lo,hi

def paired_test(wins,losses):
 if any(type(x) is not int or x<0 for x in (wins,losses)):reject('invalid discordances')
 n=wins+losses
 if n==0:return Fraction(1)
 lower=min(wins,losses);coefficient=1;total=1
 for k in range(1,lower+1):
  coefficient=coefficient*(n-k+1)//k;total+=coefficient
 return min(Fraction(1),Fraction(2*total,2**n))

def calculate(rows, tasks):
 if type(tasks) is not list or len(tasks)!=82 or type(rows) is not list or len(rows)!=82:reject('complete 82 pairs required')
 if len({t['task_id'] for t in tasks})!=82 or len({t['task_id'].split('/')[0] for t in tasks})!=82:reject('task/parent duplicate')
 for row,task in zip(rows,tasks):
  if type(row) is not dict or set(row)!={'task_id','family','A','B','C'} or row['task_id']!=task['task_id'] or row['family']!=task['family'] or any(type(row[a]) is not bool for a in 'ABC'):reject('row identity/order/outcome mismatch')
 stats={};raw={};families={}
 for row in rows:
  f=families.setdefault(row['family'],{'n':0,'A_success':0,'B_success':0,'C_success':0});f['n']+=1
  for a in 'ABC':f[a+'_success']+=int(row[a])
 for f in families.values():f['C_minus_A']=Fraction(f['C_success']-f['A_success'],f['n'])
 for a in 'AB':
  w=sum(r['C'] and not r[a] for r in rows);l=sum(not r['C'] and r[a] for r in rows)
  wl,wu=cp(w,82);ll,lu=cp(l,82);raw['C-'+a]=paired_test(w,l)
  stats['C-'+a]={'n':82,'wins':w,'losses':l,'ties':82-w-l,'delta':Fraction(w-l,82),'ci':[wl-lu,wu-ll],'p':raw['C-'+a]}
 order=sorted(raw,key=raw.get);first=min(Fraction(1),2*raw[order[0]]);second=min(Fraction(1),max(first,raw[order[1]]))
 stats[order[0]]['holm']=first;stats[order[1]]['holm']=second
 warning=any(10*(s['wins']-s['losses'])<=-82 for s in stats.values()) or any(10*(f['C_success']-f['A_success'])<=-f['n'] for f in families.values())
 positive=all(s['holm']<=Fraction(1,20) and 10*(s['wins']-s['losses'])>=82 for s in stats.values())
 decision='UNFAVORABLE_WARNING' if warning else ('LARGE_EFFECT_SIGNAL' if positive else 'INCONCLUSIVE')
 return {'contrasts':stats,'families':families,'decision':decision,'nonharm':stats['C-A']['ci'][0]>Decimal('-.05'),'successes':{a:sum(int(r[a]) for r in rows) for a in 'ABC'}}

def compare(extracted,manifest,schedule):
 audit=extracted.get('production_audit',{})
 if extracted.get('schema')!='SI_U1_PAIRED_ANALYSIS_V1' or extracted.get('run_id')!=RUN or extracted.get('manifest_sha256')!=MANIFEST or audit.get('status')!='AUDIT_PASS_LIVE' or audit.get('report_status')!='COMPLETE' or type(audit.get('episode_count')) is not int or audit['episode_count']!=246 or type(audit.get('pending_na_count')) is not int or audit['pending_na_count']!=0:reject('untrusted/incorrect extraction')
 tasks=manifest['tasks'];sched=schedule['rows']
 if len(sched)!=82 or any((t['task_id'],t['family'],t['seed'])!=(s['task_id'],s['family'],2000000+i) or s['schedule_index']!=i or s['parent']!=t['task_id'].split('/')[0] for i,(t,s) in enumerate(zip(tasks,sched))):reject('frozen manifest/schedule mismatch')
 mine=calculate(extracted['paired_records'],tasks);other=extracted['statistics'];tol=1e-12
 def near(x,y):return type(y) in (int,float) and math.isfinite(y) and abs(float(x)-y)<=tol
 if extracted['overall_successes']!=mine['successes'] or other['decision']!=mine['decision'] or other['n']!=82 or other['five_pp_nonharm_supported_under_inference_assumptions']!=mine['nonharm']:reject('decision or overall discrepancy')
 if set(other['contrasts'])!=set(mine['contrasts']) or set(other['families'])!=set(mine['families']):reject('contrast/family keys discrepancy')
 for name,c in mine['contrasts'].items():
  o=other['contrasts'][name]
  if any(o[k]!=c[k] for k in ('n','wins','losses','ties')) or not all(near(c[k],o[v]) for k,v in [('delta','delta'),('p','mcnemar_two_sided_p'),('holm','holm_adjusted_p')]) or len(o['simultaneous_95pct_conservative_ci'])!=2 or any(not near(x,y) for x,y in zip(c['ci'],o['simultaneous_95pct_conservative_ci'])):reject('contrast discrepancy')
 for name,f in mine['families'].items():
  o=other['families'][name]
  if any(o[k]!=f[k] for k in ('n','A_success','B_success','C_success')) or not near(f['C_minus_A'],o['C_minus_A']):reject('family discrepancy')
 return mine

def main():
 a=argparse.ArgumentParser();a.add_argument('--analysis',required=True);a.add_argument('--analysis-sha256',required=True);a.add_argument('--manifest',required=True);a.add_argument('--schedule',required=True);a.add_argument('--output',required=True);args=a.parse_args()
 extracted=exact_json(args.analysis,args.analysis_sha256);m=exact_json(args.manifest,MANIFEST);s=exact_json(args.schedule,SCHEDULE)
 result=compare(extracted,m,s)
 out={'schema':'SI_U1_INDEPENDENT_STATISTICAL_COMPARISON_V1','status':'AGREES_WITH_INDEPENDENT_RECOMPUTATION','analysis_sha256':args.analysis_sha256,'manifest_sha256':MANIFEST,'schedule_sha256':SCHEDULE,'run_id':RUN,'tolerance_absolute':1e-12,'decimal_precision':70,'paired_records':82,'overall_successes':result['successes'],'decision':result['decision'],'nonharm_supported_under_assumptions':result['nonharm'],'interpretation':'Agreement is arithmetic only; audit of authentic run and sampling assumptions is separate.'}
 p=pathlib.Path(args.output)
 if not p.is_absolute() or p.exists() or p.is_symlink() or not p.parent.is_dir():reject('fresh output required')
 with p.open('x') as f:json.dump(out,f,sort_keys=True,indent=2);f.write('\n')
 p.chmod(0o600);print('INDEPENDENT_STATISTICS_AGREE',hashlib.sha256(p.read_bytes()).hexdigest())
if __name__=='__main__':main()
