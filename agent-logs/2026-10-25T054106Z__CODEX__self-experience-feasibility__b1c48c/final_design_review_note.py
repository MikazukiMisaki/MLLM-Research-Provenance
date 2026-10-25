"""Same SI-P0 final review clarification: read reports and version prose only.
No raw branch/training data are opened; no project code imported or executed.
"""
import datetime
import hashlib
import json
from pathlib import Path

OWN=Path(__file__).resolve().parent
COORD=Path('/home/lizening/research-notes/agent-logs/2026-10-25T054106Z__SOL__self-improvement-phase0__b1c48c')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
paths=[COORD/'independent_historical_rescue_verification.json',COORD/'independent_r19_experience_recount.json']
expected=['bf3503774a81abfeb1dc11343f677dafccefabcae78fe38607b815b82f5f437a','fa7e2ee6acf5b34f7c7229e203bd7e384c51a05c6c201494b1ce0772e950a0b9']
for p,h in zip(paths,expected):
 if sha(p)!=h:raise RuntimeError('Independent report changed '+str(p))
historical=json.loads(paths[0].read_text());r19=json.loads(paths[1].read_text())
if historical['historical_rescue_rows']!=31 or historical['historical_unique_tasks']!=15 or historical['errors']:raise RuntimeError('Historical report needs clarification')
hist_ids={r['canonical_task'] for r in historical['verified_refs']}
r19_ids={r['canonical_trial_id'] for items in r19['rescue_candidates_by_k'].values() for r in items}
if len(hist_ids)!=15 or len(r19_ids)!=2 or hist_ids&r19_ids:raise RuntimeError('Report-level identity counts need clarification')
# Check both previous seals without updating their files or receipt logs.
old_count=0
for name,manifest_hash in [('FILE_HASHES.sha256','d7f60e2bfc293a88f6131c3f91af20980bae28caf3211f9f64b8ddd21b3cb0cb'),('ADDENDUM_FILE_HASHES.sha256','7e0039ae5eddb81ee730f7b9da0759d2d3399f81ed82b1c4339a5e05cfa3c00e')]:
 p=OWN/name
 if sha(p)!=manifest_hash:raise RuntimeError('Prior seal changed')
 for line in p.read_text().splitlines():
  h,filename=line.split('  ',1);f=Path(filename)
  if f.parent!=OWN or sha(f)!=h:raise RuntimeError('Prior frozen file changed '+filename)
  old_count+=1
old_path=OWN/'MINIMAL_SELF_IMPROVEMENT_PROTOCOL_DRAFT.md'
if sha(old_path)!='11d3d6577dcefb2afc31f63334b6351b14f55303e46c5904019090617b8b2bbd':raise RuntimeError('Original draft changed')
v2=old_path.read_text().replace('# 一轮自身经验采纳 SFT 草案','# 一轮自身经验采纳 SFT 草案 V2 — 最终设计审查限定',1)
v2=v2.replace('**DRAFT_NOT_EXECUTABLE — SCIENTIFIC_PERMISSION=NOT_GRANTED**','''**DRAFT_NOT_EXECUTABLE — SCIENTIFIC_PERMISSION=NOT_GRANTED**

**最终 DATA_FEASIBILITY=NOT_READY；QUALIFIED_TRAINING_N=NOT_ESTABLISHED；LEARNING_GAIN=NOT_PROVEN。** V1的READY_FOR_PROTOCOL_DESIGN仅表示能够写出草案，不是学习数据已就绪。本V2限制当前可读主张；原V1、inventory、所有旧收据/封存文件原字节保留。配套最终决定见 `SI_P0_FINAL_FEASIBILITY_DECISION.md`。本轮至此完成，不扩大调查或自动后续。''',1)
a=v2.index('## 2. A/B/C及最小可解释对照');b=v2.index('## 3. 来源处理与因果时点',a)
v2=v2[:a]+'''## 2. 竞争配方与机制归因的必要对照

原始配方含义需先分清：A冻结强SFT-P0；B_source只对actor普通成功自身经验做SFT；C采纳增益验证的纠错经验。**C>B_source即使出现，也不能单独证明筛选机制**，因为训练生成来源、teacher、任务难度、纠错/普通数据比例及曝光分布同时可能不同。C>A也不自动分解出这些因素。它们至多比较整个数据/更新配方。

若未来希望把问题限定为采纳条件，最小纸上主对照应将B_source**替换为B_pool**，保持三臂数量；本文其余B/C训练预算条款里的B均指B_pool。这是设计上的必要条件，当前没有构建pool、训练B_pool或获准执行任何训练臂。

| 组 | 权重/候选来源 | 采纳条件及能回答的问题 |
|---|---|---|
| A | 冻结原SFT-P0 | 不更新；回答是否超过强基座 |
| B_pool（success-only） | 与C相同的预先冻结生成候选池，恢复teacher/固定operator/学生目标格式相同 | 对候选纠错仅要求完整任务终局成功，不看相对CONTINUE增量；普通自身成功背景与C相同 |
| C | 与B_pool同池、相同初始化/格式/背景比例/更新预算 | 纠错部分另要求同前缀CONTINUE=0且纠错=1，并通过相同证据条件 |

同池指**相同采纳前候选来源及生成机会**，不表示把两组采纳后的训练行强行做成相同。来源、处理、目标粒度、student输入、背景比例、token/steps、重复上限和checkpoint须一致冻结；不能让B_pool看不到C的teacher候选，再把来源差异归因给paired筛选。处理带来的难度/家族组成变化仍须透明报告；同池success-only是必要对照，并非自动排除所有难度重加权解释。若要更强地宣称“增益标签本身优于单纯难度重采样”，尚需独立预注册且可实现的设计，当前不作该主张或扩充方案。

若协调方未来必须保留B_source，则只能将同池success-only列为**条件性D_pool的审查依赖**；缺少D_pool时禁止采纳机制归因。D_pool不是当前最小执行计划，不是已接受第四臂，亦不产生新增训练/生成额度。替换B或条件性D两种选择都须未来明确冻结，不能事后择优解释。

C>A是学习超过强基座的必要证据；C>B_source仅比较配方。只有在上述同池及更新约束成立、独立新任务评估等条件满足时，C>B_pool（或C>D_pool）才可能支持这一**冻结采纳配方**相对success-only的增量，仍不证明每条目标正确/必要、所有竞争解释排除或方法首创。当前没有任何这些已训练比较结果。

'''+v2[b:]
needle='训练目标仅拟议采用已执行、合法且可追溯的**第一纠错动作**'
pos=v2.index(needle);end=v2.index('\n\n',pos)
v2=v2[:pos]+'''训练目标仅拟议采用已执行、合法且可追溯的**第一纠错动作**，使用原SFT-P0 Action-ID输出接口。恢复teacher是adapter-off base；它看过原时点的diagnosis/subgoal，某些历史处理还看过card。**这些原始恢复prompt及subgoal/card不能直接移植给P0**。P0只能使用动作前的原公共goal/observation/H4/map；对目标的投影是否可追溯、是否丢失了必要区分信息尚未证明，不能当已经合格的训练行。不训练rationale，不让teacher重写新目标，不跨时点搬用Axxx；需原raw ID、当时map、选中command及transition绑定。

必须分别记来源：①adapter-off恢复action目标；②恢复后由adapter-on冻结SFT-P0生成的suffix动作。后者发生在改变后的checkpoint，有自己的输入/map/时间，不是adapter-off标签，不是新增独立task，也不能把原prefix的0→1沿时间复制成每个suffix action的“已验证正增益”。本最小草案没有自动采纳suffix作为额外C监督；未来若要使用，需要另行固定其来源比例与同池对照，当前仍只是分开的候选证据索引。主草案不混入PAR/FACT/CARD处理。'''+v2[end:]
v2=v2.replace('预注册C−A和C−B两项paired比较','预注册C−A和C−B_pool两项paired比较')
v2=v2.replace('同时支持C>A、C>B并满足伤害/总成本约束','同时支持C>A、C>B_pool并满足伤害/总成本约束')
(OWN/'MINIMAL_SELF_IMPROVEMENT_PROTOCOL_DRAFT_V2.md').write_text(v2)
md=r'''# SI-P0 最终学习可行性决定与设计审查限定

同一任务 `SI-P0-SOL-b1c48c`；仅只读审计与DRAFT设计。**最终 DATA_FEASIBILITY=NOT_READY；QUALIFIED_TRAINING_N=NOT_ESTABLISHED；LEARNING_GAIN/MECHANISM=NOT_PROVEN。新科学执行NO_GO/NOT_GRANTED。**

原V1的READY_FOR_PROTOCOL_DESIGN仅表示已有事实足以写出可否证草案，不是学习闭环数据就绪。为避免READY歧义，本最终决定使用NOT_READY；原文、inventory、第一补充及封存清单均不覆写。当前阅读草案以 `MINIMAL_SELF_IMPROVEMENT_PROTOCOL_DRAFT_V2.md` 的限定为准。没有新增数据处理/生成计划，也不为用完2人时继续扩查。

## OBSERVED：候选来源核对，不是训练N

协调方独立原件核对 [independent_historical_rescue_verification.json](/home/lizening/research-notes/agent-logs/2026-10-25T054106Z__SOL__self-improvement-phase0__b1c48c/independent_historical_rescue_verification.json)，SHA256 `bf3503774a81abfeb1dc11343f677dafccefabcae78fe38607b815b82f5f437a`，确认原inventory的31条历史rescue ref/hash/CONTINUE0→recovery1均匹配、errors为空，折叠为15 canonical tasks。它明确不是training-row approval。本线程仅阅读该核对结果，没有重跑原件审计。

协调方 [independent_r19_experience_recount.json](/home/lizening/research-notes/agent-logs/2026-10-25T054106Z__SOL__self-improvement-phase0__b1c48c/independent_r19_experience_recount.json)，SHA256 `fa7e2ee6acf5b34f7c7229e203bd7e384c51a05c6c201494b1ce0772e950a0b9`，显示R19虽有多个K rescue记录，被任何K救回的unique task仅2个：

- `R19-failure-a33d7ca26ecbe46dc4b6`：Ladle/Drawer clean trial。
- `R19-failure-b3ab21b8e193f6adf6ff`：Vase/DeskLamp light trial。

两份报告中的task标识无交叉，合计17个canonical task仅是**这些异质处理下已观察救回的候选覆盖上限**；不是合格训练N、不是可用新评估N，也不是17项同一teacher/同一处理/同一学生输入的独立学习样本。原单步限定下11states/10tasks的稀少与家族偏斜也没有因此消失。

0→1及行哈希核对解决了“原件是否确有这个终局与引用”，没有解决：逐目标的学生公共时点投影、恢复teacher身份/额外上下文、历史weights UNKNOWN、足够的多样性/训练token、独立新任务全集或更新后收益。合格N未建立；不把17写成训练N，也不把尚未审批误写成真实可用样本数恰为0。

## INFERRED：对照能支持的主张

A冻结SFT-P0、B_source普通actor成功、C增益纠错三种配方即使C>B_source，也混有生成来源/teacher/难度与数据组成，不能单独证明筛选机制。V2选择的最小纸上机制对照是**以B_pool同池success-only替换B_source**；共同候选来源/处理/学生格式/背景比例/训练预算冻结，仅离线纠错采纳条件不同。

如果未来保留B_source，则同池success-only只能作为条件性D_pool的必要依赖；没有该对照时仅比较整体配方。**当前不添加实际训练臂、不授权D、不构建数据或运行对照。** 同池仍不是“所有机制已隔离”的保证，尤其不能自动排除难度重加权解释；更强的标签机制主张当前不成立。

干预差值 `R_i(恢复→A)−R_i(A)` 与学习后的新任务差值、C相对B_pool的差值是不同量。前者正值不能保证某条action的监督梯度具有正迁移，也不能保证suffix每一步都值得模仿。必要的新任务、预算、伤害和获取成本条件保留，不从2个R19case或oracle 2/36承诺学习效应。

## 目标来源与P0边界

adapter-off恢复目标与adapter-on SFT suffix分开索引。恢复原prompt中的subgoal/card不能直接移植到P0；只保留P0原公共动作前接口的投影仍待证明。SFT suffix在恢复改变后的状态生成，自己的map/时点和actor身份必须保留，不能当另一份恢复teacher目标或独立rescue，不把原prefix的增量标签沿suffix逐步复制。

第一补充关于专家110个多目标prompt组的限定继续有效：机械自洽不证明输入充分，多目标不等于错误，148−21=127计数相容。专家数据仍不是自身经验，不能补足这里的corrective N。

## 停止结论

本阶段现有证据足以完成候选审计和限定草案，**不足以释放数据构建、训练或新采集**。不补positive、不挑K、不改停止规则/输入接口、不训练selector、不修历史数据、不扩大文献或反复复盘。当前首轮交付结束，交由协调方独立整合；新任务和科学授权若有，另行明确。

科学SHA85/2da、原始证据/旧review/clearance、共享INDEX/rootinventory均保持；R19累计5142 generations/7949 reset-inclusive ops不变。本补充科学调用0、无commit/push/派agent。
'''
(OWN/'SI_P0_FINAL_FEASIBILITY_DECISION.md').write_text(md)
for p,h in zip(paths,expected):
 if sha(p)!=h:raise RuntimeError('Independent report changed during supplement')
files=['SI_P0_FINAL_FEASIBILITY_DECISION.md','MINIMAL_SELF_IMPROVEMENT_PROTOCOL_DRAFT_V2.md']
record={'task_id':'SI-P0-SOL-b1c48c','continuation_not_new_task':True,'status':'LOCAL_FROZEN_FOR_COORDINATOR_REVIEW','data_feasibility_final':'NOT_READY','qualified_training_N':None,'qualified_training_N_status':'NOT_ESTABLISHED; candidate identity counts are not training N','historical_candidate_refs':31,'historical_candidate_tasks':15,'R19_any_K_rescued_unique_tasks':2,'combined_candidate_tasks':17,'not_recounted_from_raw_here':True,'old_frozen_files_unchanged':old_count,'source_bindings':[{'path':str(p),'sha256_before':h,'sha256_after':sha(p),'unchanged':True} for p,h in zip(paths,expected)],'mechanism_control':'B_pool success-only same pre-admission candidate pool replaces B_source in V2; D_pool only conditional dependency if B_source retained, not accepted execution arm','teacher_and_suffix_separate':True,'recovery_subgoal_card_not_transplanted_to_P0':True,'new_scientific_calls':0,'training_data_or_scientific_code_modified':False,'shared_index_or_git_publication':False,'not_independent_review_PASS':True,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[{'path':str(OWN/n),'sha256':sha(OWN/n),'bytes':(OWN/n).stat().st_size} for n in files],'next_action':'Task complete; wait for coordinator. No automatic data construction/training/collection.'}
(OWN/'FINAL_REVIEW_RECORD.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(record,ensure_ascii=False,indent=2))
