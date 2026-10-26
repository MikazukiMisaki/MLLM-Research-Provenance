from pathlib import Path
from collections import Counter
import hashlib,json,subprocess,xml.etree.ElementTree as ET
OWN=Path(__file__).resolve().parent;REPO=Path('/home/lizening/wt-si-p3-source-only-v2');BASE=Path('/home/lizening/research-notes/agent-logs/2026-10-26T111621Z__SOL__si-s01-independent-base844-suite__critic_1f34d86d');CURRENT=OWN/'comparable_rt'
def read(p):return json.loads(Path(p).read_bytes())
def binding(p):
 p=Path(p);v=p.read_bytes();return {'path':str(p),'bytes':len(v),'sha256':hashlib.sha256(v).hexdigest()}
def junit(p):
 root=ET.parse(p).getroot();counts=Counter()
 for case in root.iter('testcase'):
  kind='errors' if case.find('error') is not None else 'failed' if case.find('failure') is not None else 'skipped' if case.find('skipped') is not None else 'passed';counts[kind]+=1
 return {k:counts[k] for k in ('passed','failed','errors','skipped')}|{'collected':sum(counts.values())}
base=read(BASE/'BASELINE_ID_SETS.json');assert binding(BASE/'BASELINE_ID_SETS.json')['sha256']=='7f6c762e6c02bc144d371102cd4dd9acb5e1dddc8c1ec7898ec0124f95911499'
reports=read(CURRENT/'full.reports.json');ids=read(CURRENT/'full.collection_ids.json');baseids=read(BASE/'full.collection_ids.json');assert ids==read(CURRENT/'collect.collection_ids.json')
problems=[{'nodeid':r['nodeid'],'classification':'failure' if r['phase']=='call' else 'error','phase':r['phase'],'exception_type':r['exception_type']} for r in reports['reports'] if r['outcome']=='failed']
key=lambda r:(r['nodeid'],r['classification'],r['phase'],r['exception_type'])
assert set(map(key,problems))==set(map(key,base['comparison_keys'])),set(map(key,problems))-set(map(key,base['comparison_keys']))
assert len(problems)==80 and not reports['collection_errors']
oldset=set(baseids);newids=[i for i in ids if i not in oldset];assert [i for i in ids if i in oldset]==baseids
assert all(i.startswith('tests/test_si_s01_') for i in newids) and len(newids)==83
byid={i:[] for i in ids}
for r in reports['reports']:byid[r['nodeid']].append(r)
assert all(all(r['outcome']=='passed' for r in byid[i]) and {r['phase'] for r in byid[i]}=={'setup','call','teardown'} for i in newids)
assert all(all(r['outcome']=='passed' for r in byid[i]) for i in base['passed_ids'])
counts=junit(CURRENT/'baseline.junit.xml');assert counts=={'passed':1036,'failed':3,'errors':77,'skipped':0,'collected':1116},counts
focused=junit(OWN/'rt_focused.xml');assert focused=={'passed':83,'failed':0,'errors':0,'skipped':0,'collected':83}
additional_full=junit(OWN/'final_full.xml');assert additional_full=={'passed':1032,'failed':3,'errors':77,'skipped':0,'collected':1112}
receipt=read(CURRENT/'full.receipt.json');assert receipt['authentic_returncode']==1 and receipt['pre_status']==receipt['post_status']==''
assert read(CURRENT/'collect.receipt.json')['authentic_returncode']==0
origins={stage:read(CURRENT/('full.origins.'+stage+'.json')) for stage in ('before','after')}
for stage,v in origins.items():
 assert v['torch_cuda_initialized'] is False
 assert all(not x for x in v['environment_presence'].values())
 for name,item in v['modules'].items():
  if name!='pytest':assert Path(item['file']).is_relative_to(REPO) and hashlib.sha256(Path(item['file']).read_bytes()).hexdigest()==item['sha256']
assert origins['before']['modules']==origins['after']['modules']
assert not subprocess.check_output(['git','status','--porcelain=v1'],cwd=REPO,text=True)
value={'status':'DEVELOPER_SOFTWARE_VERIFIED_PENDING_INDEPENDENT_REVIEW','source_sha':receipt['source_sha'],'base_sha':base['target_sha'],'baseline_binding':binding(BASE/'BASELINE_ID_SETS.json'),'comparable_runner_binding':binding(OWN/'baseline_runner.py'),'same_exact_runner_as_baseline':True,'same_explicit_environment_contract':receipt['same_explicit_environment_contract'],'candidate_counts':counts,'baseline_counts':base['counts'],'focused_counts':focused,'prior_9bc_additional_full_counts':additional_full,'raw_comparable_full_returncode':receipt['authentic_returncode'],'prior_9bc_raw_additional_full_returncode':read(OWN/'receipts/final_full.json')['authentic_returncode'],'raw_focused_returncode':read(OWN/'receipts/rt_focused.json')['authentic_returncode'],'exact_historical80_ID_classification_phase_exception_types_equal':True,'all953_historical_passed_IDs_still_passed':True,'historical_collection_relative_order_preserved':True,'collection_and_full_order_equal':True,'new_test_count':len(newids),'new_problem_IDs':[],'candidate_problem_keys':sorted(problems,key=key),'new_passed_IDs':newids,'module_origins_before_after_equal':True,'all_project_origins_inside_exact_worktree':True,'CUDA_initialized_before':False,'CUDA_initialized_after':False,'whole_suite_CPU_toy_activity':'Existing small CPU PEFT/model/tokenizer software fixtures executed; this is not actual Qwen/P0/tokenizer/GPU/runtime verification.','scientific_calls':{'real_Qwen_tokenizer':0,'real_8B_weights':0,'CUDA_initializations':0,'real_ALFWorld':0,'production_preflight':0,'SSH':0,'teacher':0,'acquisition':0,'training':0,'evaluation':0},'independent_acceptance_or_launch_clearance_claimed':False}
with (OWN/'SOFTWARE_COMPARISON_FINAL.json').open('x') as f:json.dump(value,f,indent=2);f.write('\n')
print(json.dumps({k:value[k] for k in ('status','source_sha','candidate_counts','focused_counts','exact_historical80_ID_classification_phase_exception_types_equal','new_problem_IDs')}))
