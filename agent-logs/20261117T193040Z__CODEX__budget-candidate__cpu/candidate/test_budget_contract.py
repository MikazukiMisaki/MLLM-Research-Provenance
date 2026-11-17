import copy
import unittest
import static_adapter
from budget_contract import BudgetError,NEW_MAX,UNMODELED,validate_budget

def values():return {k:0 for k in NEW_MAX}
def example():
 known=values();known.update(generation=3,reset=1,step=2,environment_operations=3,materialize=1,input_tokens=10,output_tokens=4)
 unknown=values();unknown.update(generation=1,input_tokens=4096,output_tokens=16,reset=1,environment_operations=1)
 ceiling={k:known[k]+unknown[k]+NEW_MAX[k] for k in NEW_MAX}
 return {'known_completed':{'ledger_sha256':'a'*64,'amounts':known},
         'unknown_reserved':{'ledger_sha256':'b'*64,'amounts':unknown},'new_limits':dict(NEW_MAX),
         'combined_ceiling':ceiling,'unmodeled':{k:'NOT_MODELED' for k in UNMODELED}}
class TestBudget(unittest.TestCase):
 def test_consistent_claims_still_incomplete(self):
  b=example();r=validate_budget(b);self.assertEqual(r['status'],'BUDGET_INCOMPLETE')
  self.assertEqual(r['required_ceiling'],b['combined_ceiling']);self.assertFalse(r['authorization']);self.assertFalse(r['history_authenticated'])
 def test_zero_and_every_single_resource_shortage_fail(self):
  b=example();b['new_limits']=values()
  with self.assertRaises(BudgetError):validate_budget(b)
  for k in NEW_MAX:
   with self.subTest(resource=k):
    b=example();b['new_limits'][k]-=1
    with self.assertRaises(BudgetError):validate_budget(b)
 def test_unknown_must_be_explicit_and_include_tokens(self):
  b=example();del b['unknown_reserved']
  with self.assertRaises(BudgetError):validate_budget(b)
  b=example();del b['unknown_reserved']['amounts']['step']
  with self.assertRaises(BudgetError):validate_budget(b)
  b=example();b['unknown_reserved']['amounts']['input_tokens']=0
  with self.assertRaises(BudgetError):validate_budget(b)
 def test_any_combined_ceiling_shortage_is_rejected(self):
  for k in NEW_MAX:
   with self.subTest(resource=k):
    b=example();b['combined_ceiling'][k]-=1
    with self.assertRaises(BudgetError):validate_budget(b)
 def test_unmodeled_cannot_be_declared_complete(self):
  b=example();b['unmodeled']['device']='COMPLETE'
  with self.assertRaises(BudgetError):validate_budget(b)
class TestAdapterIntegration(unittest.TestCase):
 def test_adapter_enforces_budget_before_claiming_consistency(self):
  product={'base_path':'/fiction/base','base_tree_sha256':'1'*64,'products':{a:{'adapter_path':'/fiction/'+a,'adapter_tree_sha256':str(i)*64} for a,i in [('P0',2),('CANDIDATE',3)]}}
  raw=static_adapter.canonical(product)
  cases=[{'case':str(i),'public_goal':'fictional','order':['P0','CANDIDATE'] if i%2==0 else ['CANDIDATE','P0'],'input_sha256':{x:'4'*64 for x in ('game','routing','config')}} for i in range(4)]
  plan={'schema':'STATIC_PAIR_ADAPTER_V1','products':product,'limits':static_adapter.LIMITS,'cases':cases,'env_seed':42,'budget':example()}
  result=static_adapter.validate_plan(plan,raw,static_adapter.digest(raw))
  self.assertEqual(result['budget']['status'],'BUDGET_INCOMPLETE');self.assertFalse(result['execution_authorized'])
  plan['budget']['new_limits']=values()
  with self.assertRaises(static_adapter.ContractError):static_adapter.validate_plan(plan,raw,static_adapter.digest(raw))
if __name__=='__main__':unittest.main(verbosity=2)
