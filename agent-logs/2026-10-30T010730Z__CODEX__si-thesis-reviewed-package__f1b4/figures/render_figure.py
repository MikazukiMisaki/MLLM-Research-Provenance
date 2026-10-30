#!/usr/bin/env python3
"""Render SI-U1 aggregate plot from hash-bound local reports; no science runtime."""
import hashlib
import json
import math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE=Path('/home/lizening/research-notes/agent-logs')
PRIMARY=BASE/'2026-10-29T225000Z__LUNA__si-u1-extraction-publication__062a/frozen_and_review/FINAL_PILOT82_PAIRED_ANALYSIS_C2356.json'
SECOND=BASE/'2026-10-29T222200Z__SOL__si-u1-independent-recompute__c2356/INDEPENDENT_STATISTICS_DETAIL.json'
EXPECTED={PRIMARY:'4a3ea016d4c06022980482ac9dbc58155a68bbe20fbc723a68ce49c7c345ea9b',SECOND:'47311ee5f8e3fa0022019e43da97c70ebb61b8aaa0f3e856c5a2854ef3a9f19d'}
for p,want in EXPECTED.items():
    got=hashlib.sha256(p.read_bytes()).hexdigest()
    if got != want: raise ValueError(f'source digest mismatch: {p.name}')
a=json.loads(PRIMARY.read_bytes()); b=json.loads(SECOND.read_bytes())
n=a['statistics']['n']; totals=a['overall_successes']; c=a['statistics']['contrasts']
assert n==b['paired_n']==82 and totals==b['overall_successes']=={'A':65,'B':68,'C':67}
for key in ('C-A','C-B'):
    x,y=c[key],b['contrasts'][key]
    assert x['n']==y['n']==n
    for k in ('wins','losses','ties','holm_adjusted_p'):
        assert x[k]==y[k]
    assert math.isclose(x['delta'],y['delta'],rel_tol=0.0,abs_tol=1e-12)
    for v,w in zip(x['simultaneous_95pct_conservative_ci'],y['simultaneous_ci']):
        assert math.isclose(v,w,rel_tol=0.0,abs_tol=1e-12)
assert a['statistics']['decision']==b['decision']=='INCONCLUSIVE'

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.titlesize':11,
                     'axes.labelsize':10,'svg.fonttype':'none','pdf.fonttype':42,
                     'axes.spines.top':False,'axes.spines.right':False})
fig,(left,right)=plt.subplots(1,2,figsize=(11.8,5.6),gridspec_kw={'width_ratios':[1.05,1]})
fig.subplots_adjust(left=.145,right=.98,top=.78,bottom=.36,wspace=.43)
fig.suptitle('SI-U1: paired success on the fixed development schedule',fontsize=15,fontweight='bold',x=.145,ha='left',y=.94)
fig.text(.145,.875,'Exploratory ALFWorld TRAIN sample  |  82 paired tasks  |  one B and one C training seed',fontsize=9.5,color='#414a52')
colors=['#6f7b86','#4b7899','#b0633d']; labels=['A  P0','B  Expert','C  Self-success']
y=[2,1,0]
for i,key in enumerate(('A','B','C')):
    val=100*totals[key]/n
    left.barh(y[i],val,height=.52,color=colors[i],edgecolor='none')
    left.text(val+1,y[i],f'{totals[key]}/{n}  ({val:.2f}%)',va='center',fontsize=10)
left.set_yticks(y,labels);left.set_xlim(0,115);left.set_xticks([0,25,50,75,100]);left.set_xlabel('Success rate on the same 82 tasks (%)')
left.set_title('A  Observed success',loc='left',fontweight='bold',pad=13)
left.xaxis.grid(True,color='#d7dce0',linewidth=.6);left.set_axisbelow(True);left.tick_params(axis='y',length=0)
right.axvline(0,color='#727c82',linewidth=1,linestyle='--',zorder=1)
for i,key in enumerate(('C-A','C-B')):
    item=c[key]; yy=1-i; delta=100*item['delta']; lo,hi=[100*v for v in item['simultaneous_95pct_conservative_ci']]
    right.plot([lo,hi],[yy,yy],color='#234e66',linewidth=2.6,zorder=2)
    right.scatter([delta],[yy],color='#b0633d',s=50,zorder=3)
    right.text(0,yy-.24,f'{delta:+.2f} pp  [{lo:+.2f}, {hi:+.2f}]',ha='center',va='center',fontsize=9)
right.set_ylim(-.55,1.45);right.set_xlim(-20,20);right.set_yticks([1,0],['C − A','C − B']);right.set_xticks([-20,-10,0,10,20]);right.set_xlabel('Paired difference in success (percentage points)')
right.set_title('B  Paired differences (95% intervals)',loc='left',fontweight='bold',pad=13)
right.xaxis.grid(True,color='#d7dce0',linewidth=.6);right.set_axisbelow(True);right.tick_params(axis='y',length=0)
fig.text(.145,.245,'Points are observed differences; bars are conservative simultaneous 95% intervals.',fontsize=9)
fig.text(.145,.202,'Population interpretation of these intervals requires task sampling/exchangeability assumptions.',fontsize=9)
fig.text(.145,.159,'The fixed TRAIN schedule is not a certified held-out sample. Each continuation has one training seed.',fontsize=9)
fig.text(.145,.116,'Exact McNemar tests with Holm correction: both adjusted p = 1.00. Decision: INCONCLUSIVE.',fontsize=9)
fig.text(.145,.073,'A = original P0; B = expert-data continuation; C = self-success continuation.',fontsize=9)
out=Path(__file__).parent
fig.savefig(out/'si_u1_paired_results.svg',format='svg',metadata={'Date':None})
fig.savefig(out/'si_u1_paired_results.pdf',format='pdf',metadata={'CreationDate':None,'ModDate':None})
fig.savefig(out/'si_u1_paired_results_preview.png',dpi=150,metadata={'Software':'matplotlib'})
(out/'figure_data.json').write_text(json.dumps({'source_sha256':{p.name:v for p,v in EXPECTED.items()},'n':n,'overall_successes':totals,'contrasts':{k:{'delta_pp':100*c[k]['delta'],'simultaneous_ci_pp':[100*x for x in c[k]['simultaneous_95pct_conservative_ci']],'wins':c[k]['wins'],'losses':c[k]['losses'],'ties':c[k]['ties'],'holm_adjusted_p':c[k]['holm_adjusted_p']} for k in c},'decision':a['statistics']['decision'],'matplotlib_version':matplotlib.__version__},indent=2,sort_keys=True)+'\n')
print('Figure rendered from two verified, concordant inputs; no task identities emitted.')
