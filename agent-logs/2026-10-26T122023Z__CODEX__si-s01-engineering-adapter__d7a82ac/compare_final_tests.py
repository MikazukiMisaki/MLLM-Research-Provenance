from pathlib import Path
from collections import Counter
import hashlib,json,subprocess,xml.etree.ElementTree as ET
OWN=Path(__file__).resolve().parent;REPO=Path('/home/lizening/wt-si-s01-engineering-adapter');CUR=OWN/'final_tests';BASE=Path('/home/lizening/research-notes/agent-logs/2026-10-26T111621Z__SOL__si-s01-independent-base844-suite__critic_1f34d86d');D7=Path('/home/lizening/research-notes/agent-logs/2026-10-26T102514Z__CODEX__si-s01-source-only-implementation__f1a52e8c/comparable_rt')
def read(p):return json.loads(Path(p).read_bytes())
def bind(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def keys(reports):return sorted((r['nodeid'],'failure' if r['phase']=='call' else 'error',r['phase'],r['exception_type']) for r in reports if r['outcome']=='failed')
def junit(p):
 c=Counter()
 for node in ET.parse(p).getroot().iter('testcase'):c['errors' if node.find('error') is not None else 'failed' if node.find('failure') is not None else 'skipped' if node.find('skipped') is not None else 'passed']+=1
 return {k:c[k] for k in ('passed','failed','errors','skipped')}|{'collected':sum(c.values())}
base=read(BASE/'BASELINE_ID_SETS.json');assert bind(BASE/'BASELINE_ID_SETS.json')['sha256']=='7f6c762e6c02bc144d371102cd4dd9acb5e1dddc8c1ec7898ec0124f95911499'
reports=read(CUR/'full.reports.json');old=read(D7/'full.reports.json');ids=read(CUR/'full.collection_ids.json');d7ids=read(D7/'full.collection_ids.json');bids=read(BASE/'full.collection_ids.json')
assert ids==read(CUR/'collect.collection_ids.json') and not reports['collection_errors']
expected=sorted((r['nodeid'],r['classification'],r['phase'],r['exception_type']) for r in base['comparison_keys'])
assert keys(reports['reports'])==keys(old['reports'])==expected
new=[x for x in ids if x not in set(d7ids)];assert len(new)==71 and all(x.startswith('tests/test_si_s01_engineering_') for x in new)
assert [x for x in ids if x in set(d7ids)]==d7ids and [x for x in ids if x in set(bids)]==bids
byid={x:[] for x in ids}
for r in reports['reports']:byid[r['nodeid']].append(r)
oldpass={x for x in d7ids if all(r['outcome']=='passed' for r in old['reports'] if r['nodeid']==x)};assert len(oldpass)==1036
assert all(all(r['outcome']=='passed' for r in byid[x]) for x in oldpass|set(new))
counts=junit(CUR/'baseline.junit.xml');focus=junit(CUR/'focused.junit.xml')
assert counts=={'passed':1107,'failed':3,'errors':77,'skipped':0,'collected':1187},counts
assert focus=={'passed':154,'failed':0,'errors':0,'skipped':0,'collected':154},focus
receipts={k:read(CUR/(k+'.receipt.json')) for k in ('focused','collect','full')}
assert receipts['focused']['authentic_returncode']==receipts['collect']['authentic_returncode']==0 and receipts['full']['authentic_returncode']==1
assert len({r['source_sha'] for r in receipts.values()})==1 and all(r['pre_status']==r['post_status']=='' for r in receipts.values())
orig={k:read(CUR/('full.origins.'+k+'.json')) for k in ('before','after')}
assert orig['before']['modules']==orig['after']['modules'] and not orig['before']['torch_cuda_initialized'] and not orig['after']['torch_cuda_initialized']
for name,v in orig['after']['modules'].items():
 if name!='pytest':assert Path(v['file']).is_relative_to(REPO) and hashlib.sha256(Path(v['file']).read_bytes()).hexdigest()==v['sha256']
assert not subprocess.check_output(['git','status','--porcelain=v1'],cwd=REPO,text=True)
value={'status':'DEVELOPER_SOFTWARE_VERIFIED_PENDING_INDEPENDENT_EXACT_SHA_REVIEW','source_sha':receipts['full']['source_sha'],'base_d7_sha':'d7a82acb510157ab7ba5439d790816c5c948439f','base844_problem_binding':bind(BASE/'BASELINE_ID_SETS.json'),'sealed_d7_reports_binding':bind(D7/'full.reports.json'),'counts':counts,'focused_counts':focus,'new_engineering_tests':len(new),'new_problem_IDs':[],'all80_ID_classification_phase_exception_types_match_both_bases':True,'all1036_d7_prior_passing_IDs_preserved':True,'all953_base844_passing_IDs_preserved':True,'all83_source_only_tests_preserved':True,'no_dropped_collected_IDs':True,'relative_prior_collection_order_preserved':True,'candidate_problem_keys':keys(reports['reports']),'new_passed_IDs':new,'full_authentic_returncode':1,'focused_authentic_returncode':0,'collect_authentic_returncode':0,'same_baseline_runner_sha256':bind(OWN/'baseline_runner.py')['sha256'],'module_origins_unchanged_and_inside_worktree':True,'CUDA_initialized_before_after':False,'CPU_fixture_activity':'Tiny existing CPU PEFT/tokenizer/model software tests and explicit fake model/CUDA/NVML/TextWorld I/O only; no actual Qwen/ALFWorld/hostSSH/preflight/science.','actual_reader_evidence':bind(OWN/'ACTUAL_READER_CARRY_FORWARD.json'),'independent_review_or_runtime_launch_claim':False}
with (OWN/'SOFTWARE_COMPARISON.json').open('x') as f:json.dump(value,f,indent=2);f.write('\n')
print(json.dumps({k:value[k] for k in ('status','source_sha','counts','focused_counts','new_problem_IDs','all80_ID_classification_phase_exception_types_match_both_bases')}))
