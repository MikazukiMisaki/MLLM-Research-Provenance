"""Editorial/source-binding closure of a design artifact, not an execution gate."""
from pathlib import Path
import json,hashlib,shutil,datetime,subprocess
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T084517Z__CODEX__si-p3-pool-learning-design__si3_7d91')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
draft=OWN/'draft_v1';draft.mkdir(exist_ok=False)
for name in ['CONTROLLED_POOL_AND_LEARNING_DESIGN.md','design_parameters.json','source_bindings.json','INPUT_HASHES.sha256','RECORD.md']:shutil.copy2(OWN/name,draft/name)
report=OWN/'CONTROLLED_POOL_AND_LEARNING_DESIGN.md';text=report.read_text()
text=text.replace('真实prompt非padding总token通常不同；建议max/min≤1.05的资源对称guard','真实prompt非padding总token通常不同；建议新经验部分单独、以及含S的全臂总计均满足max/min≤1.05的资源对称guard（不能让共同S稀释前景差异）')
needle='96预算细分为source4,800、teacher192、P0suffix3,504次generation；'
replacement='该2N-reset上界要求未来新K1单分支collector在第一动作后原地handoff给P0，无多K公共路径或额外checkpoint reset/replay；并正确更新history/动作计数。它不是现有R19多K运行器的成本或可用性证明，不能把旧G3程序直接执行后套此预算。新collector及receipt/计账须另派工程任务、冻结代码并独立审查；做不到则当前方案NO_GO，不自动加操作额度。\n\n'+needle
assert needle in text;text=text.replace(needle,replacement);report.write_text(text)
p=OWN/'design_parameters.json';obj=json.loads(p.read_bytes())
obj['learning_candidate_not_authorized']['input_token_cost_parity_guard']='Actual nonpadding prompt-token ratio max(B,C)/min(B,C) <=1.05 BOTH for new examples separately and for whole arm including S; not exact equality and no redraw to pass'
obj['budgets_if_future_feasibility_authorized']['collector_assumption']='New independently reviewed single-K1 collector with in-place P0 handoff after first action, correct history/counter; no extra checkpoint reset/replay. Existing R19 multik runner not approved or budgeted for this.'
obj['blocking_conditions'].insert(3,'New single-K1 collector/receipt/cost implementation independently reviewed; original R19 multik execution cannot instantiate this budget')
p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
p=OWN/'source_bindings.json';bindings=json.loads(p.read_bytes());script=Path('/home/lizening/wt-r19-g4-consumer-contract-repair/scripts/run_r19_experiment.py');h=sha(script)
assert h=='06bb8e11c3cc9e9484b8d5731c86690b97a4c445a0e5aa16b72b912c6c14dd5c'
bindings['input_bindings'].append({'path':str(script),'sha256_before':h,'sha256_after':sha(script),'bytes':script.stat().st_size,'unchanged':True})
for x in bindings['input_bindings']:assert sha(Path(x['path']))==x['sha256_before']==x['sha256_after']
p.write_text(json.dumps(bindings,ensure_ascii=False,indent=2)+'\n')
(OWN/'INPUT_HASHES.sha256').write_text(''.join(x['sha256_before']+'  '+x['path']+'\n' for x in bindings['input_bindings']))
with (OWN/'RECORD.md').open('a') as f:f.write('\n封存前独立自检收敛三项：将非padding输入token5%对称guard明确同时适用于新经验部分与全臂，防止共同S稀释差异；将2N-reset预算明确限定于未来新审查的单K1原地handoff collector，不套用现有多K/G3程序；补齐所引用run_r19_experiment.py的实际输入SHA。仅设计/绑定澄清，不运行或实现collector。初稿5文件原字节留draft_v1，初稿writer/真实回执不改。\n')
repo_receipts=[]
for path,expected in [('/home/lizening/wt-codex-r18c2','e537f441010077123a307e9d50ea40cf8dad8547'),('/home/lizening/wt-r19-g4-consumer-contract-repair','85cbb92395e5e2420c2adeb1fa0634653e742910'),('/home/lizening/wt-r19-recovery-duration-v1','2da980f631badc25086d12db60d128ff507d3ae6')]:
 rec={'path':path,'calls':[]}
 for args in [['rev-parse','HEAD'],['status','--porcelain']]:
  argv=['git','--no-optional-locks','-C',path,*args];cp=subprocess.run(argv,capture_output=True,text=True,check=False)
  rec['calls'].append({'argv':argv,'returncode':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr});assert cp.returncode==0
 assert rec['calls'][0]['stdout'].strip()==expected and rec['calls'][1]['stdout']==''
 rec['HEAD']=expected;rec['clean']=True;repo_receipts.append(rec)
(OWN/'frozen_source_state_receipts.json').write_text(json.dumps(repo_receipts,indent=2)+'\n')
items=[]
for name in ['CONTROLLED_POOL_AND_LEARNING_DESIGN.md','design_parameters.json','source_bindings.json','INPUT_HASHES.sha256','paper_math.json','paper_math.receipt.json','primary_reference_bindings.json','frozen_source_state_receipts.json','RECORD.md']:
 p=OWN/name;items.append({'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size})
hand={'task':'SI-P3','status':'DESIGN_COMPLETE_AWAITING_INDEPENDENT_REVIEW','directory':str(OWN),'recommendation':'Only96-task future feasibility candidate after partition/engineering/new authorization, no automatic384/train/dev/eval','proposed_candidate_acquisition_N':96,'current_acquisition_training_eval_calls_authorized':0,'science_calls_this_task':0,'tokenizer_loaded':False,'actual_training_exposure_verified':False,'trained_models_or_policy_results':False,'historical_cost_unchanged':'5142 generations /7949 reset-inclusive operations, includes177/342','source_SHA85_and2da_unchanged':True,'all_metadata_input_hashes_unchanged':len(bindings['input_bindings']),'artifacts':items,'math_scope':'Hypothetical single-pair binomial paper arithmetic only, not real-data analysis or joint Holm power','source_citation_scope':'2 primary papers, URLs/versions recorded, no byte-authentication claim for raw papers','software_or_protocol_implementation':'None; current trainer/collector require separate future assignment and independent review','publication':'Coordinator owned, no sharedINDEX/commit/push'}
(OWN/'FROZEN_HANDOFF.json').write_text(json.dumps(hand,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'report_sha256':sha(OWN/'CONTROLLED_POOL_AND_LEARNING_DESIGN.md'),'parameters_sha256':sha(OWN/'design_parameters.json'),'handoff_sha256':sha(OWN/'FROZEN_HANDOFF.json'),'inputs_unchanged':len(bindings['input_bindings']),'source_worktrees_clean':True,'science_calls':0},indent=2))
