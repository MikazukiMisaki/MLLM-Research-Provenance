from pathlib import Path
import sys,json,hashlib,collections
blocked=[]
class NoRealRuntime:
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0] in ('torch','transformers','peft','alfworld','textworld','tokenizers','numpy'):
   blocked.append(fullname);raise AssertionError(fullname)
sys.meta_path.insert(0,NoRealRuntime());sys.path.insert(0,str(Path(sys.argv[1])/'src'))
from self_improvement.si_s01.contract import bind_plan
p=bind_plan(Path(sys.argv[2]).read_bytes(),evidence_class='live_source_only')
order=hashlib.sha256(''.join(s.task_id+'\n' for s in p.slots).encode()).hexdigest()
assert order=='40893826093d24bb111803a3532a260c2061c6c9b1c28b8d95c87000b3daa6c2'
assert len(p.slots)==96 and all((s.seed,s.pool_seed,s.cutoff)==(42,42,5) for s in p.slots)
assert list(collections.Counter(s.family for s in p.slots).values())==[35,26,16,9,10]
print(json.dumps({'status':'EXACT9BC_REAL_METADATA_PURE_BINDING_MATCH','live_plan_sha256_reference_only':p.sha256,'ordered_task_newline_sha256':order,'fixed_tasks':96,'seed_pool_cutoff':[42,42,5],'production_manifest_or_auth_written':False,'real_runtime_import_attempts':blocked,'real_scientific_calls':0}))
