from pathlib import Path
import json,sys,hashlib
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
ROOT=Path('/home/lizening/wt-si-p3-engineering-contracts')
f=ROOT/'tests/si_p3_support.py'
s=f.read_text();s=s.replace('f"Complete synthetic task {self.slot.task_id.rsplit(\'/\', 1)[-1]}."','f"Complete {self.slot.family} synthetic task {self.slot.task_id.rsplit(\'/\', 1)[-1]}."');f.write_text(s)
f=ROOT/'src/self_improvement/si_p3/collector.py';s=f.read_text();s=s.replace('self.state: PublicState | None = None','self.state: PublicState | None = None\n        self.closed = False');s=s.replace('if closer is not None:\n            closer()','if not self.closed:\n            self.closed = True\n            if closer is not None:\n                closer()');s=s.replace('session = digest([slot.key, phase])\n        env =','self.budget.check_time()\n        session = digest([slot.key, phase])\n        env =');f.write_text(s)
sys.path.insert(0,str(ROOT/'src'))
from self_improvement.si_p3.contract import *
from self_improvement.si_p3.continuation import RECIPE
contract={
'schema_version':VERSION,'status':STATUS,'execution':False,
'authority':{'base_sha':BASE_SHA,'SI_P3_design_sha256':DESIGN_SHA256,'SI_P3_review_sha256':REVIEW_SHA256,'old_bootstrap_unchanged':True,'recovery_target_exception':'future conditional SI-P3 only; not current execution permission'},
'population':{'families':list(FAMILIES),'source_quotas':SOURCE_QUOTAS,'cut_matrix':{k:{str(d):n for d,n in v.items()} for k,v in cut_matrix().items()},'source_count':96,'engineering_reserved':48,'eval_reserved':600,'nonlight_unrun':395,'light_unrun':2,'official_unseen_used':False,'automatic_384':False},
'model':{'base':'Qwen/Qwen3-8B','snapshot':SNAPSHOT,'P0_directory_sha256':P0_SHA256,'actor_adapter':'P0','teacher_adapter':'BASE','history':4,'thinking':False,'do_sample':False,'caps':CAPS,'horizon':50,'single_K':1,'suffix':'in_place_same_environment'},
'budgets':{'generations':8496,'environment_operations_with_resets':9792,'generated_tokens':138240,'input_tokens':16000000,'per_call_input':8192,'allocated_device_hours':4,'retries':0,'replacement':0,'baseline_reruns':0},
'guards':{'all_slots':96,'Q_min':72,'Q_family':Q_MIN,'C_and_neutral_min':24,'C_and_neutral_family':ADOPTION_QUOTAS,'selected_B_neutral_min':8,'distinct_public_projection_min_each':20,'draws':1,'new_prompt_ratio_max':1.05,'whole_arm_prompt_ratio_max':1.05},
'background':{'count':120,'family':BACKGROUND_QUOTAS,'dataset_sha256':BACKGROUND_DATA_SHA256,'task_hash':'SHA256 UTF8(SI-P3-S-v1\\n+family+\\n+canonical_task+\\n)','row_hash':'SHA256 UTF8(SI-P3-S-row-v1\\n+task+\\n+str(step_index)+\\n+prompt_sha256+\\n+completion+\\n)','selected_task_without_qualified_row':'NOT_READY_NO_REPLACEMENT'},
'adoption':{'C_hash_domain':'SI-P3-C-v1','B_hash_domain':'SI-P3-B-v1','hash_parts':['family','canonical_task'],'B_pool_includes_C':True,'matching':['family','actual_shifted_ID_plus_EOS_length'],'background_same_both_arms':True,'same_paired_slots_permutation_and_batch_boundaries':True},
'continuation':RECIPE,'future_acceptance_spec_only':{'confirmatory_reporter_implemented':False,'comparisons':['C>A','C>B'],'eval_tasks':600,'new_science_authorization_required':True},
'not_implemented_or_proven':['live model/environment driver','actual 8B/P0 warm-start','actual new96 pool','GPU resource completion feasibility','real training driver','confirmatory statistical reporter','independent exact-SHA acceptance','scientific launch']}
path=ROOT/'configs/self_improvement/si_p3_engineering_v1.json';path.parent.mkdir(parents=True,exist_ok=True);assert not path.exists();path.write_text(json.dumps(contract,indent=2,sort_keys=True)+'\n')
sha=hashlib.sha256(path.read_bytes()).hexdigest()
f=ROOT/'src/self_improvement/si_p3/contract.py';f.write_text(f.read_text()+f'\n\n# Byte binding of the versioned, tracked ENGINEERING_ONLY contract.\nCONTRACT_FILE_SHA256 = "{sha}"\n')
for name in ['evidence.py','collector.py','audit.py']:
 f=ROOT/'src/self_improvement/si_p3'/name;s=f.read_text()
 if name=='evidence.py':
  s=s.replace('from .contract import VERSION,','from .contract import CONTRACT_FILE_SHA256, VERSION,')
  s=s.replace('"plan_sha256": plan_sha256, "execution_authorized": False','"plan_sha256": plan_sha256, "contract_sha256": CONTRACT_FILE_SHA256, "execution_authorized": False')
  s=s.replace('header["payload"]["execution_authorized"] is False','header["payload"]["execution_authorized"] is False and header["payload"]["contract_sha256"] == CONTRACT_FILE_SHA256')
 elif name=='collector.py':
  s=s.replace('from .contract import (CAPS,','from .contract import (CONTRACT_FILE_SHA256, CAPS,')
  s=s.replace('"plan_sha256": self.plan_sha256,\n                   "status"','"plan_sha256": self.plan_sha256, "contract_sha256": CONTRACT_FILE_SHA256,\n                   "status"')
 else:
  s=s.replace('from .contract import (CAPS,','from .contract import (CONTRACT_FILE_SHA256, CAPS,')
  s=s.replace('run["execution_authorized"] is False and run["status"]','run["execution_authorized"] is False and run["contract_sha256"] == CONTRACT_FILE_SHA256 and run["status"]')
 f.write_text(s)
# Static wire schema is descriptive; production strict validators remain authoritative.
schema={'$schema':'https://json-schema.org/draft/2020-12/schema','title':'SI-P3 engineering runtime boundaries v1','type':'object','additionalProperties':False,'required':['schema_version','status','execution','authority','population','model','budgets','guards','background','adoption','continuation','future_acceptance_spec_only','not_implemented_or_proven'],'properties':{k:({'const':v} if k in ['schema_version','status','execution'] else {'type': 'object' if isinstance(v,dict) else 'array'}) for k,v in contract.items()},'$defs':{'slot':{'type':'object','additionalProperties':False,'required':['task_id','family','seed','cutoff'],'properties':{'task_id':{'type':'string'},'family':{'enum':list(FAMILIES)},'seed':{'type':'integer','minimum':0},'cutoff':{'enum':list(CUTS)}}},'labels':{'description':'Unexecuted teacher is NA/null, never failed zero. Terminal success is done && reward>0.','type':['integer','null'],'enum':[0,1,None]},'public_state':{'type':'object','additionalProperties':False,'required':list(PublicState.__dataclass_fields__),'properties':{k:{'type': 'array' if k=='valid_actions' else 'boolean' if k in ['done','truncated'] else 'number' if k=='reward' else 'string'} for k in PublicState.__dataclass_fields__}}}}
(ROOT/'configs/self_improvement/si_p3_engineering_schema_v1.json').write_text(json.dumps(schema,indent=2,sort_keys=True)+'\n')
print('contract_sha256',sha)
print('only new files changed')
