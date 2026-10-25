"""Summarize this task's completed stdlib evidence audit; no project imports."""
from audit_io import *
from collections import Counter,defaultdict
import ast

a=readjson(OWN/'pool_quality_audit.json');counts=readjson(OWN/'pipeline_counts.json');pools=readjson(OWN/'pool_sets.json');orig=readjson(OWN/'original_eleven_dispositions.json');manifest=authority()
fileloc=a['file_locations'];xs=a['cases'];byid={x['case_id']:x for x in xs}
assert len(xs)==171 and len(byid)==171
assert len({x['canonical_task'] for x in xs})==169
assert Counter(x['Q_hist'] for x in xs)=={'PASS':164,'EXCLUDE':7}
assert all(x['checks'] and all(v is True for v in x['checks'].values()) for x in xs if x['Q_hist']=='PASS')
assert all(x.get('labels',{}).get('historical_labels_retained') for x in xs)
assert all(x['same_public_projection_as_P1'] and x['same_first_target_as_P1'] for x in orig)
assert set(pools['Q_hist']['sets']['C']['case_ids'])<=set(pools['Q_hist']['sets']['B']['case_ids'])

# Independently reconstruct the locked identity-only anchor key and task minimum.
for c in manifest['rows']:
 expected=ts('SI-P2-anchor-v1\n'+c['canonical_task']+'\n'+c['stage']+'\n'+c['prefix_id']+'\n')
 assert byid[c['case_id']]['anchor_key']==expected
for q,field in [('Q_hist','selection_hist'),('Q_pin','selection_pin')]:
 eligible=[byid[cid] for cid in a[field]['flow_case_ids']['PHYSICAL_DEDUP']]
 groups=defaultdict(list)
 for x in eligible:groups[x['canonical_task']].append(x)
 expected={min(g,key=lambda r:(r['anchor_key'],r['case_id']))['case_id'] for g in groups.values()}
 assert expected==set(a[field]['flow_case_ids']['TASK_ANCHOR'])
 assert a[field]['no_slot_refill'] is True

# Read exact historical Git objects as source text. Never import/call project functions.
source_receipts=[]
for stage,revision in [('R4','7a01a6107b4bc9c994893220aab078af39fe4fff'),('R10_OSR','8926d8fb10e634489031de3da910c572b50d8d44'),('R16_OSR','d1ef841ea9dc7423177fb7647906e2e719f0fbe7'),('R19_K1','2da980f631badc25086d12db60d128ff507d3ae6')]:
 rel='src/recovery/two_stage.py';argv=['git','-C',str(FROZEN),'show',revision+':'+rel]
 cp=subprocess.run(argv,capture_output=True,check=False)
 receipt={'stage':stage,'revision':revision,'argv':argv,'returncode':cp.returncode,'stdout_sha256':hashlib.sha256(cp.stdout).hexdigest(),'stderr':cp.stderr.decode(errors='replace'),'methods':[]}
 assert cp.returncode==0
 oldtree=ast.parse(cp.stdout.decode());currenttree=ast.parse(register(FROZEN/rel).read_text())
 for name in ['parse_stage_one_output','parse_stage_two_output']:
  old=next(n for n in ast.walk(oldtree) if isinstance(n,ast.FunctionDef) and n.name==name);current=next(n for n in ast.walk(currenttree) if isinstance(n,ast.FunctionDef) and n.name==name)
  oldhash=ts(ast.dump(old,include_attributes=False));currenthash=ts(ast.dump(current,include_attributes=False))
  receipt['methods'].append({'name':name,'historical_AST_sha256':oldhash,'current_AST_sha256':currenthash,'same_AST':oldhash==currenthash,'historical_line':old.lineno,'current_line':current.lineno})
  assert oldhash==currenthash
 source_receipts.append(receipt)
argv=['git','-C',str(FROZEN),'show','2da980f631badc25086d12db60d128ff507d3ae6:scripts/run_r19_experiment.py']
cp=subprocess.run(argv,capture_output=True,check=False);assert cp.returncode==0
oldtree=ast.parse(cp.stdout.decode());currenttext=register(FROZEN/'scripts/run_r19_experiment.py').read_text();currenttree=ast.parse(currenttext)
gen=next(n for n in ast.walk(currenttree) if isinstance(n,ast.FunctionDef) and 'eos_ids = tokenizer.eos_token_id' in (ast.get_source_segment(currenttext,n) or ''))
oldgen=next(n for n in ast.walk(oldtree) if isinstance(n,ast.FunctionDef) and n.name==gen.name)
assert ast.dump(gen,include_attributes=False)==ast.dump(oldgen,include_attributes=False)
source_receipts.append({'stage':'R19_K1','argv':argv,'returncode':cp.returncode,'stdout_sha256':hashlib.sha256(cp.stdout).hexdigest(),'stderr':cp.stderr.decode(errors='replace'),'method':gen.name,'line':gen.lineno,'AST_sha256':ts(ast.dump(gen,include_attributes=False)),'same_executed2da_AST':True,'output_complete_rule':'not token_cap_reached or final token in then-tokenizer EOS IDs; no tokenizer loading here'})
output('static_contract_receipts.json',source_receipts)

# These are actual fresh read-only Git subprocess results, not inferred state.
repo_states=[]
for path,expected,branch in [('/home/lizening/wt-codex-r18c2','e537f441010077123a307e9d50ea40cf8dad8547','agent/codex-r18c2'),('/home/lizening/wt-r19-g4-consumer-contract-repair','85cbb92395e5e2420c2adeb1fa0634653e742910','codex/r19-g4-consumer-contract-repair'),('/home/lizening/wt-r19-recovery-duration-v1','2da980f631badc25086d12db60d128ff507d3ae6','')]:
 state={'path':path,'commands':[]}
 for args in [['rev-parse','HEAD'],['branch','--show-current'],['status','--porcelain']]:
  argv=['git','--no-optional-locks','-C',path,*args];cp=subprocess.run(argv,capture_output=True,text=True,check=False)
  state['commands'].append({'argv':argv,'returncode':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr});assert cp.returncode==0
 assert state['commands'][0]['stdout'].strip()==expected and state['commands'][1]['stdout'].strip()==branch and state['commands'][2]['stdout']==''
 state.update({'HEAD':expected,'branch':branch,'clean':True});repo_states.append(state)
output('frozen_worktree_receipts.json',repo_states)

# Preserve the prior publication's manifest targets, including its appended clarification.
old_checks=[]
for name,expected in [('FILE_HASHES.sha256','14189f7752494eee84fdc6adad161957b0afe34b597f68fedce845d4d5976572'),('SUCCESS_AXES_ADDENDUM_HASHES.sha256','72fd7df05a72f487ac81bbbbe7b04cf29bc33e8157bc7a73051a2954e619485c')]:
 p=register(P1/name);assert sha(p)==expected
 for line in p.read_text().splitlines():
  wanted,path=line.split('  ',1);observed=sha(register(path));assert observed==wanted,path
  old_checks.append({'path':path,'expected_sha256':wanted,'observed_sha256':observed,'unchanged':True})
output('prior_p1_immutability_check.json',{'prior_manifest_targets':len(old_checks),'files':old_checks,'old_scripts_executed':False})

# Merge all real pre/post input records from this task, preserving earliest observations.
merged={}
for name in ['inspection_input_bindings.json','r19_inspection_input_bindings.json','draft_v1/input_bindings.json','input_bindings.json']:
 for item in json.loads((OWN/name).read_bytes()):
  path=item['path'];prior=merged.setdefault(path,item.copy());assert prior['sha256_before']==item['sha256_before']
for path,item in BINDINGS.items():
 if Path(path).is_relative_to(OWN):continue
 prior=merged.setdefault(path,item.copy());assert prior['sha256_before']==item['sha256_before']
for path,item in merged.items():
 item['sha256_after']=sha(path);item['unchanged']=item['sha256_after']==item['sha256_before'];assert item['unchanged'],path
output('complete_input_bindings.json',list(merged.values()))
output('INPUT_HASHES.sha256',''.join(x['sha256_before']+'  '+x['path']+'\n' for x in sorted(merged.values(),key=lambda x:x['path'])))

quality_note={'Q_hist':dict(Counter(x['Q_hist'] for x in xs)),'Q_pin':dict(Counter(x['Q_pin'] for x in xs)),
 'model_identity_all_rows':dict(Counter(x['model_identity_axis'] for x in xs)),
 'recover_raw_won_all_rows':dict(Counter(x['terminal_corroboration']['recover']['raw_won_status'] for x in xs)),
 'recover_raw_won_Qhist_pass':dict(Counter(x['terminal_corroboration']['recover']['raw_won_status'] for x in xs if x['Q_hist']=='PASS')),
 'shared_physical_generation_receipts_removed':len(a['selection_hist']['flow_case_ids']['QUALITY'])-len(a['selection_hist']['flow_case_ids']['PHYSICAL_DEDUP']),
 'legacy_physical_reuse_not_proven_rows':sum(x['stage']!='R19_K1' for x in xs),
 'unexecuted_first_action_rows':sum(not x.get('first_target',{}).get('executed') for x in xs),
 'valid_first_action_terminal_empty_suffix_cases':[x['case_id'] for x in xs if x['Q_hist']=='PASS' and x['suffix_evidence_only']['actions_recorded']==0],
 'all_original_eleven_projection_target_bindings_match':True,
 'training_data_ready':False,'learning_gain':'NOT_PROVEN','scientific_calls_added':0,'prior_files_unchanged':True,'input_paths_checked_unchanged':len(merged)}
output('audit_completion_summary.json',quality_note)

md='''# SI-P2 同池共同质量与对照可分性审计

这是固定171原行的既有证据审计，科学增量0。结果：**Q_hist机械质量164 PASS、0 HOLD、7 EXCLUDE；固定去重/anchor后162任务，B_pool=95、C=10、B\\C=85。集合可分已获本轮记录支持；等预算学习对照仍未建立，训练N未建立，学习收益NOT_PROVEN，数据整体NOT_READY。** PASS仅是开发侧指定质量项核对，不是独立审查通过、训练数据验收或新执行许可。

唯一任务单SHA256 1fd57bda79a38b14d96a3543d5d325fa581fd11124c5bef6901f8f0b7a88f93a；共同规则 ab5e3afe8bb1e65ae1473254810ba56dfa769cefbd0952d0b2a0bdb32368ea69；固定171行manifest a3e2548e89280d150cbe83cceca632f9f91275ede0a4a9d89133e53691826078。parent为R4 24、R10_OSR 48、R16_OSR 60、R19_K1 39，共169个canonical task/trial。没有补样、增加K2–5目标、PAR/cards或suffix目标。

## 审计方法与边界

每条原行与manifest的line/SHA/task/prefix绑定。读取原source的完整动作前公共前缀，按固定P0字段构造goal、当前observation、最近4个action/result transition和原有序完整admissible map的摘要，静态公共P0文本与原actor存储prompt逐字核对。H4第j个动作的结果取原source第j+1状态；当前source动作/输出及其后状态、teacher subgoal/card/facts、奖励/won、未来suffix不进入学生输入。这里只比较字段和公共文本，不加载tokenizer、不认证新chat渲染，也不导出训练prompt/JSONL。

R4结合完整R3原replay与R4自身当前state/map/H4 hash收据；R10直接核对原replay transitions及全部前缀map；R16核对原source/current/H4摘要、逐步7项equality收据和分支/ledger完整前缀hash绑定；R19核对initial原prefix reset/replay事件、source动作前状态/有序map/history和第一recovery事件。R16使用原逐步equality收据支持过去状态，未重新产生环境状态。所有结论都是原证据的完整性核对。

原Stage1合法、Stage2完整与bare ID/selected、teacher与P0逐ID映射、实际执行command/transition均独立核对。恢复目标只取已执行的第一adapter-off动作；adapter-on suffix仅用于原完整分支成功/停止依据。失败分支按原horizon/selection fail-closed等语义审计，未要求失败必须done=true。合法首动作终态允许空suffix。

成功按原done&&reward>0及原停止语义追溯；缺won单列RAW_WON_NOT_RECORDED，不构成新G3失败或非法动作。原成功标签全部保留。三个独立判断轴继续为机械来源链、模型身份、学习收益；终态原始佐证另列。

历史R4/R10/R16 weights/tokenizer确切revision及loaded角色绑定为PARTIAL，不据此机械FAIL、不用当前cache反填；R19依原execution/runtime receipt绑定base/tokenizer snapshot、两个loaded commit、adapter hash及开关角色。Q_pin严格按预设更强身份过滤，独立执行同一后续流程，不取代主口径。

## 固定流程

anchor key在打开parent结果前从无outcome的manifest写入anchor_keys_pre_outcome.json，使用真实LF：SHA256("SI-P2-anchor-v1"+LF+canonical_task+LF+stage+LF+prefix_id+LF)。质量后只对认证shared generation-event/physical alias去重；legacy无事件ID则physical reuse NOT_PROVEN。随后跨阶段每task取最小key（平手case_id），再对anchor的exact公共projection+command去重，slot不回填；最后才将既有label连接为B/C。selection_inputs_without_outcomes.json记录选择函数的无label输入。历史结果并非人类盲法，不把固定hash处理称作盲法。

| 口径/阶段 | 行 | task | B | C | B\\C | harm | failure |
|---|---:|---:|---:|---:|---:|---:|---:|
'''
for q in ['Q_hist','Q_pin']:
 for stage,v in counts[q].items():md+=f"| {q}/{stage} | {v['rows']} | {v['unique_tasks']} | {v['B']} | {v['C']} | {v['B_minus_C']} | {v['harm']} | {v['failure']} |\n"
md+='''
Q_hist无有证据的跨候选共享物理generation重复被删除；legacy128行原件无认证共享event ID，不把语义相同suffix当物理复用证明。两个重复task由固定hash删去一条failure前缀和一条rescue前缀；exact输入-目标去重再删除0条，Q_hist内same public input群组0个。全部171行有最终去向，非anchor仍保留质量结论，不补选更有利prefix。

## 来源与家族

下表为最终Q_hist anchors；所有中间阶段、Q_pin来源/家族分解见pipeline_counts.json。

| 来源 | 行/task | B | C | B\\C | harm | failure |
|---|---:|---:|---:|---:|---:|---:|
'''
for st,v in counts['Q_hist']['EXACT_INPUT_TARGET_DEDUP']['by_source'].items():md+=f"| {st} | {v['rows']}/{v['unique_tasks']} | {v['B']} | {v['C']} | {v['B_minus_C']} | {v['harm']} | {v['failure']} |\n"
md+='\n| 家族 | 行/task | B | C | B\\C | harm | failure |\n|---|---:|---:|---:|---:|---:|---:|\n'
for fam,v in counts['Q_hist']['EXACT_INPUT_TARGET_DEDUP']['by_family'].items():md+=f"| {fam} | {v['rows']}/{v['unique_tasks']} | {v['B']} | {v['C']} | {v['B_minus_C']} | {v['harm']} | {v['failure']} |\n"
md+='''
## 全部排除与原11项去向

以下7行均有无效Stage1和第一动作未执行证据；原分支结果仍保留，排除训练候选不改变原科学结果。

| case | 原CONTINUE→recover | 理由 |
|---|---|---|
'''
for x in xs:
 if x['Q_hist']!='PASS':md+=f"| {x['case_id']} | {x['labels']['CONTINUE']}→{x['labels']['recover']} | {'; '.join(x['Q_hist_reasons'])} |\n"
md+='\n| 原P1 case | Q_hist | 固定去向 | 最终C | Q_pin |\n|---|---|---|---|---|\n'
for x in orig:md+=f"| {x['case_id']} | {x['Q_hist']} | {x['Q_hist_destination']} | {x['in_C_hist']} | {x['Q_pin']} |\n"
md+='''
11项机械来源链全部继续成立，公共projection和第一目标与P1逐项一致。R8-F22是同task最小anchor，F23不再计独立样本；保留10个unique rescue task。Q_pin只保留R19那一项C，其余历史身份不足保持PARTIAL/HOLD，不伪造机械FAIL。

## 源码边界纠正与真实回执

初稿把token_cap_reached=true直接当截断，误排R19-random-control-47bcdcad9c56a38ac146。原事件Stage1.status=valid、output_complete=true，原生成器允许EOS恰在cap处；原两阶段parser只以output_complete判截断。已静态核对四个真实历史Git对象中的两个parser方法及R19 executed2da生成器，真实读取rc均0；本轮没有运行parser或tokenizer。初稿程序、输出8项、日志和rc=0回执完整保留于draft_v1与common_quality_audit.*；最终v2回执为common_quality_final.receipt.json，rc=0。变化仅使该neutral-success归回Q_hist/Q_pin，C仍10/1，没有为了rescue更换质量/anchor规则。

两个辅助只读候选路径不存在导致一次rg exit2，另一次临时只读打印表达式有SyntaxError exit1；均在RECORD中保留真实工具收据指针，不冒充科学失败。正式新stdlib审计及固定记录检查回执与这些辅助错误分开。

## 可以证明与仍未建立

1. **集合可分：SUPPORTED。** Q_hist B=95、C=10、neutral=85；Q_pin B=29、C=1、neutral=28。两口径每个来源中有C时也有同来源neutral，具体家族分解已列。C仍很少且集中，9/10 C依赖历史PARTIAL身份；严格pin口径只剩单个look_at_obj_in_light任务，不能据此判断学习效果。
2. **等预算对照可实现：NOT_ESTABLISHED。** count层面B/C每臂不同task容量宽上界10（Q_pin为1）；若只用互不重叠neutral/C，按同source+family的count匹配上界也为10/1。它们是容量上界，不是已选训练N、效能样本量或token配平证明。B包含C，若未来独立采样可能重叠，不能把两个集合误称独立数据。即便同source/family，C与neutral仍可能有prefix难度、失败类型、teacher条件差异。
3. **学习数据充分：NOT_READY。** 背景成功数据S、任务/所有历史暴露隔离、实际P0训练tokens、重复次数/采样权重、相同更新预算和独立评估均未在本任务建立。原推理tokens只保留为成本元数据，不替代训练tokens；不得因C=10承诺可学习或统计效能。
4. **学习收益/筛选机制：NOT_PROVEN。** 被恢复成功与学习收益不同；如果未来比较C增益筛选纠错与B同pool success-only，仍需冻结共同来源/生成角色、背景S及更新/token预算、任务隔离和目标可用字段时点。当前不训练、不选择最佳rule，不将adapter-off teacher称作当前actor自采样。除这些条件设计外，本轮不建立新实验或给启动许可。

## 交付与冻结

pool_quality_audit.json含171行布尔项/理由、原label、第一动作ID/command、public摘要、终态won属性、模型轴及两口径去向；绝对文件路径通过file_locations表解析file_id，保留原line、raw_line_sha256和pointer。pool_sets.json给B/C/neutral的完整case/task ID集合；pipeline_counts.json给每阶段来源/家族flow；complete_input_bindings.json与INPUT_HASHES.sha256给原件前后hash。所有输入保持原字节；旧P1两份manifest覆盖的59目标均核对未变。

科学树仍为analyzer85cbb92395e5e2420c2adeb1fa0634653e742910、executedG3 2da980f631badc25086d12db60d128ff507d3ae6，review根e537f441010077123a307e9d50ea40cf8dad8547；均干净。R19累计5142 generations/7949含reset操作（含旧177/342）不变，不是全项目SFT总成本。仅在本轮OWN新增文件，无commit/push/sharedINDEX/rootinventory/旧raw或旧provenance修改，无额外agent/线程消息。未执行任何旧脚本、项目analyzer/validator/pytest、模型/ALFWorld/tokenizer/训练、source/replay/G2/G3/G4/preflight。后续由协调方独立审查与统一发布。
'''
output('COMMON_QUALITY_AUDIT.md',md)
record='''# SI-P2 RECORD

任务SI-P2，接收后仅在OWN（本文件父目录）写入新程序/证据摘要，OWN由__file__.resolve().parent并assert精确分配路径。未执行前轮脚本，未导入项目模块。所有parent171原行/4文件hash由唯一manifest认证；源source/replay/CONTINUE和R19 initial+K1事件静态读取，其他K不做目标/结果审计。一次早期字段形状辅助打印展开了分支原evidence_refs中的其他K引用locator；没有据此选择目标、计数其他K结局或新增评估，正式审计只使用初始与K1引用。大raw、权重、完整prompt不复制，无可训练JSONL导出。

真实过程收据：parent_inspection.receipt.json、r19_event_inspection.receipt.json、common_quality_audit.receipt.json（初稿）、common_quality_final.receipt.json（最终v2）、document_completion.receipt.json（由外层进程在本程序退出后写入）。这些stdlib子进程使用真实stdout/stderr与returncode，commands.log逐条记录。静态Git对象读取和工作树命令各自有argv/真实rc/stdout hash或原输出，见static_contract_receipts.json、frozen_worktree_receipts.json。没有pytest或科学执行，不能称独立review PASS。

初稿误把cap标志当截断，造成一项EOS-at-cap valid Stage1误排；初稿8份输出及hash保存draft_v1，程序70fa20ca5fd4b19e2b1c200db3b0eadfd31b67986c462d6ccfb2b9dbb3239832保持不变。最终v2 d680091dd733282cfbe5053b1b0d752be417801795429e519fc4363763b45aa5 按原output_complete契约纠正；没有重选anchor/调整成功标签或挽救rescue。原11项projection和第一目标与P1一致；Q_hist164 PASS/7 EXCLUDE、final162anchors，B95/C10/neutral85；Q_pin36 PASS、final36anchors，B29/C1/neutral28。质量通过不是训练数据充分或学习增益证明。

保留的辅助工具错误（均只读，未造成输入变动）：工具chunk f31718 的rg读取两个猜测路径 src/sft/r15.py 与 scripts/run_progress_aware_recovery.py 返回exit2（文件不存在）；其后用rg定位实际源码。chunk 3c9eba 的临时Python打印表达式多一括号返回exit1 SyntaxError，chunk 3fddab 修正后返回0。真实工具回执指针见auxiliary_tool_receipts.json。没有倒填成项目测试失败或科学失败。

完整输入hash前后核对表complete_input_bindings.json、INPUT_HASHES.sha256；旧P1主manifest51项和成功谓词追加manifest8项保持原字节。冻结review根e537f、analyzer85、executed2da的HEAD/branch/clean由真实只读Git命令核对。自己的FILE_HASHES.sha256在所有子进程日志/receipts写完后生成，含本轮初稿及最终产物，不含自身。文件冻结后不再改；协调方统一独立审查/发布。没有对remote做新声称，没有commit/push或共享索引改动。

权限/成本：无模型/环境/tokenizer/训练/项目analyzer/validator/pytest/source/replay/G2/G3/G4/preflight/policy评估；无额外agent或线程消息；新增科学调用0，累计R19 5142/7949（含177/342）保持。DATA_FEASIBILITY=NOT_READY，qualified training N=NOT_ESTABLISHED，learning gain=NOT_PROVEN。后续任何科学执行仍NOT_GRANTED。
'''
output('RECORD.md',record)
output('auxiliary_tool_receipts.json',[{'source':'actual tool result in this conversation','chunk_id':'f31718','exit_code':2,'operation':'read-only rg for complete_public_prefix_sha256 in two absent candidate paths and one existing source','reason':'candidate paths absent; no code executed'}, {'source':'actual tool result in this conversation','chunk_id':'3c9eba','exit_code':1,'operation':'temporary read-only Python metadata printing expression','reason':'SyntaxError extra closing parenthesis; failed before execution'}, {'source':'actual tool result in this conversation','chunk_id':'3fddab','exit_code':0,'operation':'corrected read-only metadata print and static source read'}])
print(json.dumps(quality_note,ensure_ascii=False,indent=2));print('static_source_read_returncodes',[x['returncode'] for x in source_receipts]);print('worktrees_all_clean',all(x['clean'] for x in repo_states));print('old_p1_targets_unchanged',len(old_checks));print('report_bytes',(OWN/'COMMON_QUALITY_AUDIT.md').stat().st_size)
