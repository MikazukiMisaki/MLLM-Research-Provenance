"""Independent stdlib audit of an already-completed formal G4; no producer imports."""
from pathlib import Path
from collections import Counter
import json,math,hashlib,datetime
p=Path(Path('/tmp/r19-g4-result-review-path.txt').read_text().strip());report=Path('/home/lizening/research-notes/agent-logs/2026-10-23T043602Z__LUNA__r19-g4-readiness__85cbb923/future_g4_report');source=Path('/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z');doc=json.loads((report/'summary.json').read_text());s=doc['analysis'];physical=doc['physical_research_expenditure'];branches=[json.loads(x) for x in (source/'branches.jsonl').read_text().splitlines() if x.strip()];primary=[b for b in branches if b['eligible_primary'] is True];n=len(primary)
assert n==36 and len(branches)==39 and s['primary_n']==n and s['attempted_n']==39
arm=lambda b,k:b['k_results'][str(k)]
successes={f'K{k}':sum(arm(b,k)['success'] for b in primary) for k in range(1,6)};assert s['success_by_k']==successes
rates={k:v/n for k,v in successes.items()};assert s['success_rate_by_k']==rates
cont=sum(b['continue_success'] for b in primary);assert s['continue_successes_primary']==cont
patterns=dict(sorted(Counter(''.join(str(arm(b,k)['success']) for k in range(1,6)) for b in primary).items()));op=s['duration_opportunity'];assert op['outcome_pattern_frequencies']==patterns and sum(patterns.values())==n
oracle=sum(any(arm(b,k)['success'] for k in range(1,6)) for b in primary)/n;fixed=max(rates.values());assert math.isclose(op['s_oracle'],oracle) and math.isclose(op['s_fixed'],fixed) and math.isclose(op['h_success'],oracle-fixed)
assert op['successful_duration_sets']=={b['prefix_id']:[k for k in range(1,6) if arm(b,k)['success']==1] for b in primary}
helped=sum(arm(b,1)['success']==0 and any(arm(b,k)['success'] for k in range(2,6)) for b in primary);harmed=sum(arm(b,1)['success']==1 and any(arm(b,k)['success']==0 for k in range(2,6)) for b in primary);assert (op['states_helped_by_extra_recovery_vs_k1'],op['states_harmed_by_extra_recovery_vs_k1'])==(helped,harmed)
def exact_p(w,l):
 total=w+l
 if total==0:return 1.0
 observed=math.comb(total,w);return min(1.0,sum(math.comb(total,x) for x in range(total+1) if math.comb(total,x)<=observed)/(2**total))
def paired(rows,get_a,get_b):
 wins=sum(get_a(x)==1 and get_b(x)==0 for x in rows);losses=sum(get_a(x)==0 and get_b(x)==1 for x in rows);return {'n':len(rows),'wins':wins,'losses':losses,'ties':len(rows)-wins-losses,'mean_difference':(wins-losses)/len(rows) if rows else None}
def verify_pair(actual,expected):
 for key in ('n','wins','losses','ties'):assert actual[key]==expected[key],(key,actual,expected)
 # Frozen producer spells its paired difference explicitly; verify either documented key.
 for key in ('mean_difference','mean_paired_difference'):
  if key in actual:assert actual[key]==expected['mean_difference']
raw_p=[];pair_checks={}
for k in range(2,6):
 expected=paired(primary,lambda b:arm(b,k)['success'],lambda b:arm(b,1)['success']);actual=s['paired_k_gt_1_vs_k1'][f'K{k}_vs_K1'];verify_pair(actual,expected);pv=exact_p(expected['wins'],expected['losses']);assert math.isclose(actual['exact_two_sided_p'],pv,rel_tol=1e-12,abs_tol=1e-12);raw_p.append(pv);pair_checks[f'K{k}_vs_K1']={**expected,'exact_two_sided_p':pv}
order=sorted(range(4),key=lambda i:raw_p[i]);adjusted=[None]*4;carry=0.0
for rank,index in enumerate(order):carry=max(carry,min(1.0,(4-rank)*raw_p[index]));adjusted[index]=carry
for i,k in enumerate(range(2,6)):
 assert math.isclose(s['paired_k_gt_1_vs_k1'][f'K{k}_vs_K1']['holm_adjusted_p'],adjusted[i]);pair_checks[f'K{k}_vs_K1']['holm_adjusted_p']=adjusted[i]
for k in range(1,6):verify_pair(s['paired_positive_k_vs_continue_primary'][f'K{k}_vs_CONTINUE'],paired(primary,lambda b:arm(b,k)['success'],lambda b:b['continue_success']))
verify_pair(s['paired_k1_vs_continue_attempted'],paired(branches,lambda b:arm(b,1)['success'],lambda b:b['continue_success']))
for k in range(1,5):verify_pair(op['adjacent_contrasts'][f'K{k+1}_minus_K{k}'],paired(primary,lambda b:arm(b,k+1)['success'],lambda b:arm(b,k)['success']))
fields=('input_tokens','generated_tokens','total_tokens','model_calls','environment_actions');costs={}
for k in range(1,6):
 value=s['logical_cost_by_policy'][f'K{k}'];assert value['n']==n and value['success_rate']==rates[f'K{k}']
 means={}
 for scope in ('full_branch','recovery_only'):
  m={field:sum(arm(b,k)['logical_cost'][scope][field] for b in primary)/n for field in fields};means[scope]=m
  for field,expected in m.items():assert math.isclose(value[f'mean_{scope}_cost'][field],expected,rel_tol=1e-12,abs_tol=1e-8)
  assert math.isclose(value[f'mean_{scope}_total_tokens'],m['total_tokens'])
 costs[f'K{k}']={'successes':successes[f'K{k}'],'success_rate':rates[f'K{k}'],**means}
cc=s['logical_cost_by_policy']['CONTINUE'];assert cc['n']==n and cc['success_rate']==cont/n
cm={f:sum(b['continue_logical_cost']['full_branch'][f] for b in primary)/n for f in fields};assert all(math.isclose(cc['mean_full_branch_cost'][f],cm[f],rel_tol=1e-12) for f in fields);costs['CONTINUE']={'successes':cont,'success_rate':cont/n,'full_branch':cm}
for k in range(2,6):
 key=f'K{k}_vs_K1';gain=successes[f'K{k}']-successes['K1'];diff=sum(arm(b,k)['logical_cost']['full_branch']['total_tokens']-arm(b,1)['logical_cost']['full_branch']['total_tokens'] for b in primary);v=s['cost_per_additional_net_success'][key];assert v['net_additional_successes']==gain and v['total_full_branch_token_difference']==diff;expected=diff/gain if gain>0 else None;assert v['tokens_per_net_additional_success']==expected
 same=[b for b in primary if arm(b,k)['success']==arm(b,1)['success']];mv=s['matched_success_cost_vs_k1'][key];md=sum(arm(b,k)['logical_cost']['full_branch']['total_tokens']-arm(b,1)['logical_cost']['full_branch']['total_tokens'] for b in same)/len(same) if same else None;assert mv['n']==len(same) and mv['mean_full_branch_token_difference']==md;assert mv['matched_success']==sum(arm(b,1)['success']==1 for b in same) and mv['matched_failure']==sum(arm(b,1)['success']==0 for b in same)
success_ties=[k for k in range(1,6) if rates[f'K{k}']==fixed];mincost=min(costs[f'K{k}']['full_branch']['total_tokens'] for k in success_ties);cost_ties=[k for k in success_ties if costs[f'K{k}']['full_branch']['total_tokens']==mincost];assert op['fixed_k_candidates_tied_on_success']==success_ties and op['fixed_k_candidates_tied_after_cost']==cost_ties and op['development_selected_fixed_k']==min(cost_ties)
for name,table in [('stratum',s['stratum_summaries']),('task_family',s['family_summaries'])]:
 for group,v in table.items():
  rows=[b for b in primary if b[name]==group];assert v['n']==len(rows)
  for k in range(1,6):assert v[f'K{k}_successes']==sum(arm(b,k)['success'] for b in rows)
assert {k:v['n'] for k,v in s['stratum_summaries'].items()}=={'failure':6,'success_control':15,'random_control':15}
diags=[b['passive_stopping_estimate'] for b in primary if isinstance(b.get('passive_stopping_estimate'),dict)];mapped=[d for d in diags if d.get('status')=='MAPPED_TO_MEASURED_SUFFIX'];satisfied=[d for d in mapped if d.get('selected_reason')=='public_subgoal_satisfied'];pd=s['public_stopping_diagnostic'];assert pd['diagnostic_records']==len(diags) and pd['exact_suffix_mapped_count']==len(mapped) and pd['satisfied_handoff_count']==len(satisfied) and pd['satisfied_handoff_successes']==sum(d.get('estimated_success',0) for d in satisfied);assert pd['new_model_calls']==pd['new_environment_operations']==0
expected_label='ADAPTIVE STOPPING OPPORTUNITY' if oracle-fixed>0 else ('FIXED DURATION CANDIDATE' if any(rates[f'K{k}']>rates['K1'] for k in range(2,6)) else 'NO OBSERVED SUCCESS HEADROOM');assert s['scientific_conclusion']==expected_label
assert physical['evidence_class']=='live' and physical['completed_physical_model_generations']==4965 and physical['physical_environment_operations']==7273 and physical['physical_environment_resets']==334 and physical['incomplete_operations']==0
assert physical['live_scope_validation']['completed_source_episodes']==127 and physical['live_scope_validation']['heldout_tasks']==physical['live_scope_validation']['training_runs']==physical['live_scope_validation']['external_paid_model_calls']==0
assert physical['live_execution_validation']['implementation_sha']=='2da980f631badc25086d12db60d128ff507d3ae6';assert physical['supervised_exit_validation']['exit_code']==0 and physical['supervised_exit_validation']['start_proof']=='supervisor_launch_context'
sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest();hashdoc=json.loads((report/'report_hashes.json').read_text());assert sha(report/'summary.json')==hashdoc['summary_json_sha256'] and sha(report/'R19_OPPORTUNITY_REPORT.md')==hashdoc['opportunity_report_sha256'];assert physical['events_sha256']==sha(source/'execution_events.jsonl') and physical['branches_sha256']==sha(source/'branches.jsonl')
result={'status':'PASS_INDEPENDENT_RAW_REPORT_ARITHMETIC_AND_FROZEN_INPUT_REVIEW','reviewed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'formal_analyzer_invocations_by_reviewer':0,'independent_stdlib_reconciliation_only':True,'primary_n':n,'attempted_n':len(branches),'continue_successes_primary':cont,'success_by_k':successes,'success_rate_by_k':rates,'patterns':patterns,'fixed_rate':fixed,'oracle_rate':oracle,'h_success':oracle-fixed,'helped_by_extra_recovery':helped,'harmed_by_extra_recovery':harmed,'development_selected_fixed_k':min(cost_ties),'paired_K_vs_K1':pair_checks,'logical_costs':costs,'stratum_summaries':s['stratum_summaries'],'family_summaries':s['family_summaries'],'passive_stopping_diagnostic':pd,'report_scientific_classification':s['scientific_conclusion'],'output_sha256':{name:sha(report/name) for name in ['summary.json','R19_OPPORTUNITY_REPORT.md','report_hashes.json']},'physical_cost_G3':{'model_generations':4965,'nonreset_environment_operations':7273,'resets':334,'total_environment_operations':7607},'physical_cost_cumulative_retained':{'model_generations':5142,'environment_operations_including_resets':7949},'limitations':['enrichedTRAINdevelopment36eligible; only6failure states; no general or heldout accuracy inference','fixedK selected on this same development cohort, not independently validated','oracle headroom is empirical hindsight; not an implemented or prospectively tested adaptive controller','logical deployment cost differs from physical research expenditure; all historical failed costs retained','automatic classification label does not imply statistically established adaptive-policy benefit']}
(p/'report_arithmetic_review.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['logical_costs','family_summaries','stratum_summaries','limitations']},indent=2))
