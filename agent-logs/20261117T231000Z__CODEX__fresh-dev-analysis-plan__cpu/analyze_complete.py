"""Predeclared descriptive analysis; accepts only a fully completed 36-row run."""
import hashlib,json,math,sys
from pathlib import Path

def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def p_exact(gain,loss):
    n=gain+loss
    if n==0:return 1.0
    return min(1.0,2*sum(math.comb(n,k) for k in range(min(gain,loss)+1))/(2**n))

def main():
    if len(sys.argv)!=3:raise ValueError('expected run directory and new output path')
    root=Path(sys.argv[1]);out=Path(sys.argv[2]);summary_path=root/'results/summary.json';exit_path=root/'supervisor_exit.json';journal=root/'results/events.jsonl'
    summary=json.loads(summary_path.read_bytes());ex=json.loads(exit_path.read_bytes())
    if summary.get('status')!='COMPLETE' or summary.get('open_effect') is not None or ex.get('direct_child_returncode')!=0 or ex.get('stop') is not None:raise ValueError('run is not complete; no statistics')
    rows=summary['rows'];arms=('P0','C-old','C-quarter');valid={'SUCCESS','POLICY_FAILURE','NATIVE_FAILURE','HORIZON_FAILURE'}
    if len(rows)!=12 or [r['index'] for r in rows]!=list(range(12)):raise ValueError('roster differs')
    if any(set(r['arms'])!=set(arms) or any(r['arms'][a] not in valid for a in arms) for r in rows):raise ValueError('incomplete or invalid outcomes')
    values={a:[r['arms'][a]=='SUCCESS' for r in rows] for a in arms};totals={a:sum(v) for a,v in values.items()};comparisons={}
    for base in ('P0','C-old'):
        gain=sum(x and not y for x,y in zip(values['C-quarter'],values[base]));loss=sum(y and not x for x,y in zip(values['C-quarter'],values[base]))
        both_success=sum(x and y for x,y in zip(values['C-quarter'],values[base]));both_failure=sum(not x and not y for x,y in zip(values['C-quarter'],values[base]))
        comparisons[base]={'gain':gain,'loss':loss,'both_success':both_success,'both_failure':both_failure,'difference_count':gain-loss,'difference_percentage_points':100*(gain-loss)/12,'exact_mcnemar_p_exploratory':p_exact(gain,loss)}
    ordered=sorted(comparisons,key=lambda a:comparisons[a]['exact_mcnemar_p_exploratory']);p1=comparisons[ordered[0]]['exact_mcnemar_p_exploratory'];p2=comparisons[ordered[1]]['exact_mcnemar_p_exploratory'];comparisons[ordered[0]]['holm_adjusted_p_exploratory']=min(1.,2*p1);comparisons[ordered[1]]['holm_adjusted_p_exploratory']=min(1.,max(2*p1,p2))
    result={'schema':'adaptive_exposed_dev_descriptive_v1','scope':'previously exposed adaptive DEV, not independent confirmation','parents':12,'episodes':36,'success_counts':totals,'comparisons':comparisons,'exploratory_resource_screen_pass':comparisons['P0']['difference_count']>=2 and comparisons['C-old']['difference_count']>=1,'results_sha256':digest(summary_path),'supervisor_exit_sha256':digest(exit_path),'raw_journal_sha256':digest(journal),'limitations':['single trained seed','ordered previously exposed development parents','protocol adapted after earlier technical stop','no population or stable generalization inference','device sharing and unobserved cleanup tails not fully measured'],'operation_starts':summary.get('operation_starts'),'conservative_allocation_seconds':ex.get('conservative_device_allocated_seconds')}
    with out.open('x',encoding='utf8') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
