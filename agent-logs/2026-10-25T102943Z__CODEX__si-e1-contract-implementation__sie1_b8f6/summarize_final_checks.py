from pathlib import Path
import collections,hashlib,json,shutil,subprocess,xml.etree.ElementTree as ET
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
FROZEN='a995d4c3c5f7d31a2cf1fd0afc4bfa4bd72ee3a3'
def junit(name):
 root=ET.parse(OWN/(name+'.xml')).getroot();counts=collections.Counter();bad=[];toy=0
 for case in root.iter('testcase'):
  status='error' if case.find('error') is not None else 'failure' if case.find('failure') is not None else 'skipped' if case.find('skipped') is not None else 'passed'
  counts[status]+=1
  if status in ('error','failure'):bad.append(case.attrib.get('classname','')+'::'+case.attrib['name'])
  if case.attrib['name']=='test_genuine_CPU_PEFT_warmstart_fresh_optimizer_final18_and_roundtrip' and status=='passed':toy+=1
 return {'counts':dict(counts),'failure_error_ids':sorted(bad),'completed_new_CPU_toy_test_invocations':toy}
base=junit('baseline85_full');focused=junit('frozen_focused_v2');full=junit('frozen_full')
assert base['counts']=={'passed':703,'error':77,'failure':3},base
assert focused['counts']=={'passed':343},focused
assert full['counts']=={'passed':800,'error':77,'failure':3},full
assert full['failure_error_ids']==base['failure_error_ids'],'NEW/changed regression IDs'
for label,expected in [('baseline85_full',1),('frozen_focused_v2',0),('frozen_full',1),('synthetic_integration_frozen',0),('actual_reservation_binding',0),('cached_tokenizer_text_audit',0),('compile_new_sources',0),('staged_diff_check',0)]:
 assert json.loads((OWN/'receipts'/(label+'.json')).read_text())['returncode']==expected,label
runs={}
for name in ['focused_v1','focused_v2','focused_v3','focused_v4','frozen_focused_v2','frozen_full']:
 runs[name]=junit(name)
completed_toys=sum(x['completed_new_CPU_toy_test_invocations'] for x in runs.values())
assert completed_toys==6
copy_root=OWN/'cpu_toy_saved_evidence';assert not copy_root.exists();copy_root.mkdir()
raw_roots={}
for label,root in [('frozen_focused_v2',Path('/tmp/si-e1-codex-frozen_focused_v2-b8f6')),('frozen_full',Path('/tmp/si-e1-codex-frozen_full-b8f6'))]:
 cases=sorted(root.glob('test_genuine_CPU_PEFT*'))
 cases=[p for p in cases if p.is_dir() and not p.is_symlink()]
 assert len(cases)==1,(label,cases)
 case=cases[0];raw_roots[label]=str(case)
 for arm in ['B','C']:
  source=case/arm;receipt=json.loads((source/'software_receipt.json').read_text())
  assert receipt['updates']==18 and receipt['real_training_performed'] is False
  shutil.copytree(source,copy_root/label/arm)
  assert (copy_root/label/arm/'software_receipt.json').read_bytes()==(source/'software_receipt.json').read_bytes()
result={'frozen_sha':FROZEN,'scope':'DEVELOPER_SOFTWARE_CHECKS_ONLY','independent_review':'NOT_ISSUED','scientific_execution':'NOT_GRANTED',
 'fresh_base85':base,'frozen_focused':focused,'frozen_full':full,'no_NEW_failure_error_IDs':True,
 'new_software_tests':97,'all_pending_coordinator_messages_incorporated':['frozen v2 bare-ID teacher prompt/parser','P0 source/suffix incomplete-cap semantics','run/task/kind/start online receipts','fixed raw-SHA A96 identity binder and same-family D48 rejection'],
 'tokenizer_only':json.loads((OWN/'cached_tokenizer_audit.json').read_text()),'actual_reservation_metadata_only':json.loads((OWN/'actual_reservation_binding_check.json').read_text()),
 'synthetic_integration_context':json.loads((OWN/'synthetic_integration_frozen/software_invocation_context.json').read_text()),
 'synthetic_integrity':json.loads((OWN/'synthetic_integration_frozen/integrity.json').read_text()),
 'synthetic_adoption':json.loads((OWN/'synthetic_integration_frozen/adoption.json').read_text()),
 'software_activity':{'completed_new_CPU_toy_test_invocations':completed_toys,'toy_arm_continuations':2*completed_toys,'actual_toy_optimizer_updates':36*completed_toys,'actual_toy_forward_and_backward_microbatches_each':288*completed_toys,'real_Qwen_or_P0_neural_objects':0,'real_model_generations':0,'real_environment_operations':0,'actual_new_task_bodies_read':0,'GPU_activity':0,'tokenizer_text_encodings':10,'tokenizer_chat_renders':5,'tokenizer_decodes':4,'fake_boundaries_not_scientific_debits':True},
 'historical_scientific_cost_unchanged':{'generations':5142,'environment_operations_including_reset':7949,'old177_342_already_included':True},
 'raw_toy_roots':raw_roots,'copied_toy_evidence':str(copy_root),
 'limits':['no live driver','no real P0 warm-start or training verified','no actual new96 data or S120 selected','no GPU/input budget completion feasibility measured','no actual evaluation or statistical reporter','no independent acceptance or launch clearance']}
(OWN/'FINAL_DEVELOPER_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
(OWN/'HISTORICAL_FAILURE_ERROR_IDS.json').write_text(json.dumps({'base':base['failure_error_ids'],'candidate':full['failure_error_ids'],'same':True},indent=2)+'\n')
print(json.dumps({'focused':focused['counts'],'full':full['counts'],'historical80_IDs_unchanged':True,'CPU_toy_optimizer_updates':36*completed_toys,'real_science_increment':0,'independent_acceptance':'NOT_ISSUED'}))
