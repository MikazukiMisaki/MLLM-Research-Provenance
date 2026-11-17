import copy,json,unittest
from pathlib import Path
import static_adapter as s
ROOT='/home/lizening/research-notes/agent-logs/20261118__CODEX__pair-owned-scheduler-v4__private'
def example():
 product={'base_path':'/fiction/base','base_tree_sha256':'1'*64,'products':{arm:{'adapter_path':'/fiction/'+arm,'adapter_tree_sha256':str(i)*64} for arm,i in [('P0',2),('CANDIDATE',3)]}}
 raw=s.canonical(product);h=s.digest(raw)
 inputs={k:{'path':'/fiction/'+k,'sha256':'4'*64} for k in ('game','routing','config')}
 cases=[{'case':str(i),'public_goal':'fictional','order':['P0','CANDIDATE'] if i%2==0 else ['CANDIDATE','P0'],'input_sha256':{k:v['sha256'] for k,v in inputs.items()}} for i in range(4)]
 budget={'historical_ledger_sha256':'5'*64,'historical_used':{'generation':1,'environment_operations':2,'materialize':1},'prospective_ceiling':{'generation':500,'environment_operations':1000,'materialize':5},'proposed_additional':{'generation':400,'environment_operations':800,'materialize':4}}
 plan={'schema':'STATIC_PAIR_ADAPTER_V1','products':product,'limits':s.LIMITS,'cases':cases,'env_seed':42,'budget':budget}
 binding={'root':'/fiction/pair','game':'/fiction/pair/data/authored-eprime-only/game.tw-pddl','config':'/fiction/pair/config.json','data_root':'/fiction/pair/data','sha256':{k:'6'*64 for k in ('game','routing','config')}}
 manifest=s.canonical({'schema':'FIXED_PRODUCT_FOUR_PAIR_DEV_V1','cases':cases,'env_seed':42,'horizon':50,'limits':s.LIMITS})
 kw={'case':'0','arm':'P0','previous_initial':None,'output':'/fiction/output','manifest_path':'/fiction/manifest','manifest_sha256':s.digest(manifest),'manifest_bytes':manifest,'inputs':inputs,'pair_binding':binding,'source_root':'/fiction/source','legacy_dir':'/fiction/legacy','candidate_root':ROOT,'code_files':[{'path':str(Path(ROOT)/k),'sha256':v} for k,v in s.SOURCE_HASHES.items()],'runtime_extra':{'gpu_uuid':'FICTIONAL','packages':{},'runtime_identity':{}}}
 return plan,raw,h,kw
class TestStatic(unittest.TestCase):
 def test_frozen_candidate_code_and_hold(self):
  self.assertFalse(s.check_source_contract(ROOT)['physical_runtime_verified'])
  with self.assertRaises(RuntimeError):s.launch()
 def test_empty_and_bindings_refused(self):
  with self.assertRaises(s.ContractError):s.validate_plan({},b'','0'*64)
  p,r,h,k=example();self.assertTrue(s.draft_arm_config(p,r,h,**k)['draft_only'])
  bad=copy.deepcopy(p);bad['products']['products']['P0']['adapter_tree_sha256']='9'*64
  with self.assertRaises(s.ContractError):s.validate_plan(bad,r,h)
  bad=copy.deepcopy(p);bad['budget']['historical_used']={x:0 for x in s.METRICS}
  with self.assertRaises(s.ContractError):s.validate_plan(bad,r,h)
  bad=copy.deepcopy(p);bad['budget']['proposed_additional']['materialize']=5
  with self.assertRaises(s.ContractError):s.validate_plan(bad,r,h)
  badkw=copy.deepcopy(k);badkw['code_files'][0]['sha256']='9'*64
  with self.assertRaises(s.ContractError):s.draft_arm_config(p,r,h,**badkw)
  badkw=copy.deepcopy(k);badkw['manifest_sha256']='9'*64
  with self.assertRaises(s.ContractError):s.draft_arm_config(p,r,h,**badkw)
  badkw=copy.deepcopy(k);badkw['inputs']['game']['sha256']='9'*64
  with self.assertRaises(s.ContractError):s.draft_arm_config(p,r,h,**badkw)
  badkw=copy.deepcopy(k);badkw['arm']='CANDIDATE'
  with self.assertRaises(s.ContractError):s.draft_arm_config(p,r,h,**badkw)
if __name__=='__main__':unittest.main(verbosity=2)
