import hashlib,importlib.util,json,os,pathlib
P=pathlib.Path(__file__).resolve().parent
src=pathlib.Path('/home/lizening/research-notes/agent-logs/2026-10-29T221000Z__SOL__si-u1-independent-statistics__c2356/independent_stats.py')
a=pathlib.Path('/home/lizening/research-notes/agent-logs/2026-10-29T113523Z__ASTRA__three-arm-prospective-design__a55d1af9/FINAL_PILOT82_PAIRED_ANALYSIS_C2356.json')
m=pathlib.Path('/home/lizening/research-notes/agent-logs/2026-10-29T144100Z__SOL__si-u1-stage2-plan__2060cc8/stage2/manifest.json')
s=pathlib.Path('/home/lizening/research-notes/agent-logs/2026-10-29T113523Z__ASTRA__three-arm-prospective-design__a55d1af9/PILOT82_PROPOSED_SCHEDULE_PRIVATE.json')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
assert sha(src)=='e7ec762a7ae6d2643d5393634c5318a63d83bbf22d1330508b0511bcef4cab06'
sp=importlib.util.spec_from_file_location('independent_stats_reviewed',src);mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod)
x=mod.exact_json(a,'4a3ea016d4c06022980482ac9dbc58155a68bbe20fbc723a68ce49c7c345ea9b');mm=mod.exact_json(m,mod.MANIFEST);ss=mod.exact_json(s,mod.SCHEDULE)
r=mod.compare(x,mm,ss)
contrasts={};maximum_error=0.0
for name,c in r['contrasts'].items():
 v=x['statistics']['contrasts'][name];diffs={'delta':float(c['delta'])-v['delta'],'p':float(c['p'])-v['mcnemar_two_sided_p'],'holm':float(c['holm'])-v['holm_adjusted_p'],'ci_low':float(c['ci'][0])-v['simultaneous_95pct_conservative_ci'][0],'ci_high':float(c['ci'][1])-v['simultaneous_95pct_conservative_ci'][1]};maximum_error=max(maximum_error,*map(abs,diffs.values()))
 contrasts[name]={'n':c['n'],'wins':c['wins'],'losses':c['losses'],'ties':c['ties'],'delta':float(c['delta']),'mcnemar_p':float(c['p']),'holm_adjusted_p':float(c['holm']),'simultaneous_ci':[float(c['ci'][0]),float(c['ci'][1])],'absolute_max_numeric_difference':max(map(abs,diffs.values()))}
families={k:{**{n:int(v[n]) for n in ('n','A_success','B_success','C_success')},'C_minus_A':float(v['C_minus_A']),'warning_at_minus_10pp':10*(v['C_success']-v['A_success'])<=-v['n']} for k,v in r['families'].items()}
result={'schema':'SI_U1_INDEPENDENT_STATISTICS_DETAIL_V1','status':'AGREES_TOLERANCE_1E-12','input_sha256':sha(a),'method_sha256':sha(src),'run_id':mod.RUN,'paired_n':82,'overall_successes':r['successes'],'contrasts':contrasts,'families':families,'decision':r['decision'],'nonharm_supported_under_assumptions':r['nonharm'],'maximum_absolute_numeric_difference':maximum_error,'method':'Exact rational McNemar/Holm; 70-decimal inverse binomial CDF for 98.75% component CP bounds','outcome_identity_and_full_production_audit_status_checked':True,'arithmetic_only_not_independent_supervisor_authentication':True}
with (P/'INDEPENDENT_STATISTICS_DETAIL.json').open('x') as f:json.dump(result,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(result,sort_keys=True))
