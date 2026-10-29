import copy,importlib.util,math,unittest
from decimal import Decimal
from fractions import Fraction
import independent_stats as independent
spec=importlib.util.spec_from_file_location('frozen_reference','/home/lizening/research-notes/agent-logs/2026-10-29T114500Z__SOL__si-paired-stats-reference/paired_stats.py');reference=importlib.util.module_from_spec(spec);spec.loader.exec_module(reference)
def fixture(salt=0):
 tasks=[{'task_id':f'synthetic-{i}/trial','family':f'f{i%4}'} for i in range(82)]
 rows=[{'task_id':t['task_id'],'family':t['family'],'A':(i+salt)%4<2,'B':(i*3+salt)%5<3,'C':(i*7+salt)%11<6} for i,t in enumerate(tasks)]
 return rows,tasks
class IndependentSyntheticTests(unittest.TestCase):
 def test_cp_edge_closed_forms(self):
  alpha=Decimal(1)/Decimal(160);low,high=independent.cp(0,82)
  self.assertEqual(low,0);self.assertAlmostEqual(float(high),1-float(alpha)**(1/82),places=13)
  low,high=independent.cp(82,82);self.assertEqual(high,1);self.assertAlmostEqual(float(low),float(alpha)**(1/82),places=13)
 def test_exact_p_special_cases(self):
  self.assertEqual(independent.paired_test(0,0),Fraction(1));self.assertEqual(independent.paired_test(82,0),Fraction(1,2**81));self.assertEqual(independent.paired_test(3,3),Fraction(1))
 def test_independent_calculation_against_reference_on_synthetic_cases(self):
  for seed in range(4):
   rows,tasks=fixture(seed);a=independent.calculate(rows,tasks);b=reference.analyze(rows,expected_tasks={t['task_id']:t['family'] for t in tasks})
   self.assertEqual(a['decision'],b['decision']);self.assertEqual(a['nonharm'],b['five_pp_nonharm_supported_under_inference_assumptions'])
   for name,x in a['contrasts'].items():
    y=b['contrasts'][name]
    for k in ('n','wins','losses','ties'):self.assertEqual(x[k],y[k])
    for k,v in [('delta','delta'),('p','mcnemar_two_sided_p'),('holm','holm_adjusted_p')]:self.assertAlmostEqual(float(x[k]),y[v],places=12)
    for x0,y0 in zip(x['ci'],y['simultaneous_95pct_conservative_ci']):self.assertAlmostEqual(float(x0),y0,places=12)
   for family,v in a['families'].items():
    self.assertEqual({k:v[k] for k in ('n','A_success','B_success','C_success')},{k:b['families'][family][k] for k in ('n','A_success','B_success','C_success')})
    self.assertAlmostEqual(float(v['C_minus_A']),b['families'][family]['C_minus_A'],places=12)
 def test_reject_partial_duplicates_out_of_order_and_invalid(self):
  rows,tasks=fixture()
  for case in ('missing','duplicate','wrong_order','wrong_family','none','integer','unexpected_field','duplicate_parent'):
   x,y=copy.deepcopy(rows),copy.deepcopy(tasks)
   if case=='missing':x.pop()
   if case=='duplicate':x[1]=copy.deepcopy(x[0])
   if case=='wrong_order':x[0],x[1]=x[1],x[0]
   if case=='wrong_family':x[0]['family']='bad'
   if case=='none':x[0]['A']=None
   if case=='integer':x[0]['A']=1
   if case=='unexpected_field':x[0]['extra']=False
   if case=='duplicate_parent':y[1]['task_id']=y[0]['task_id'].split('/')[0]+'/other'
   with self.subTest(case=case),self.assertRaises(ValueError):independent.calculate(x,y)
 def test_family_warning_precedes_large_signal(self):
  rows,tasks=fixture()
  for r in rows:r['A']=False;r['B']=False;r['C']=True
  for i in range(0,82,4):rows[i]['A']=True;rows[i]['C']=False
  self.assertEqual(independent.calculate(rows,tasks)['decision'],'UNFAVORABLE_WARNING')
 def test_complete_comparison_and_tampered_outputs(self):
  rows,tasks=fixture();manifest={'tasks':[dict(t,seed=2000000+i) for i,t in enumerate(tasks)]}
  schedule={'rows':[{'task_id':t['task_id'],'family':t['family'],'schedule_index':i,'parent':t['task_id'].split('/')[0]} for i,t in enumerate(tasks)]}
  result={'schema':'SI_U1_PAIRED_ANALYSIS_V1','run_id':independent.RUN,'manifest_sha256':independent.MANIFEST,'production_audit':{'status':'AUDIT_PASS_LIVE','report_status':'COMPLETE','episode_count':246,'pending_na_count':0},'paired_records':rows,'overall_successes':{a:sum(r[a] for r in rows) for a in 'ABC'},'statistics':reference.analyze(rows,expected_tasks={t['task_id']:t['family'] for t in tasks})}
  independent.compare(result,manifest,schedule)
  for bad in ('wrong_run','partial','wrong_audit','wrong_p','wrong_ci','wrong_success','wrong_family_stat','wrong_schedule'):
   x=copy.deepcopy(result);s=copy.deepcopy(schedule)
   if bad=='wrong_run':x['run_id']='bad'
   if bad=='partial':x['paired_records'].pop()
   if bad=='wrong_audit':x['production_audit']['status']='PARTIAL'
   if bad=='wrong_p':x['statistics']['contrasts']['C-A']['holm_adjusted_p']+=.01
   if bad=='wrong_ci':x['statistics']['contrasts']['C-A']['simultaneous_95pct_conservative_ci'][0]+=.01
   if bad=='wrong_success':x['overall_successes']['A']+=1
   if bad=='wrong_family_stat':x['statistics']['families']['f0']['C_success']+=1
   if bad=='wrong_schedule':s['rows'][0]['schedule_index']=1
   with self.subTest(bad=bad),self.assertRaises(ValueError):independent.compare(x,manifest,s)
if __name__=='__main__':unittest.main(verbosity=2)
