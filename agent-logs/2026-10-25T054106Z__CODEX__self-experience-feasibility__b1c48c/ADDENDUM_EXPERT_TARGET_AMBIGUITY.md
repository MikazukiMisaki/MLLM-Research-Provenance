# SI-P0 只读补充：专家多目标与学习收益边界

同一任务 `SI-P0-SOL-b1c48c` 的协调补充；不替换已冻结V1。原 `SELF_EXPERIENCE_FEASIBILITY.md` SHA256 `59982056769090f6aa62ee22761bcc076cf17525a7d6a4a06d039b8589e848f5`、原 `FILE_HASHES.sha256` SHA256 `d7f60e2bfc293a88f6131c3f91af20980bae28caf3211f9f64b8ddd21b3cb0cb` 保持不变。本次只读协调方结果/脚本/收据、旧summary与计数代码，不再解析专家JSONL、不重建/修复数据、不拟合或重评策略。

## OBSERVED：独立检查的具体含义

协调方结果 [independent_expert_dataset_check.json](/home/lizening/research-notes/agent-logs/2026-10-25T054106Z__SOL__self-improvement-phase0__b1c48c/independent_expert_dataset_check.json)，本次读取SHA256 `8c2b381d7ae6e0b30c66911683531a71a450271a0dddd5f39629c8ab25a1650b`。配套真实returncode为0。本线程阅读了其stdlib脚本，未执行它，也未读取其SOURCE JSONL。

该检查报告最终专家数据20,967条、1,200 tasks，其中train18,828条/1,074 tasks，validation2,139条/126 tasks；被检查的rendered-prompt SHA、target ID→command map、completion→target ID及declared terminal-success字段未发现错误，train/val prompt hash交叉为0。数据文件SHA前后均为 `c547e8f0c5988b29288f2a097169c7859741b7d4f53f222af31f5e2889d516cf`；这是协调方对该原件的直接检查，本补充引用其结果，不冒充独立重复解析。

同一报告记录110个重复rendered-prompt组，全部110组具有不同的 `(action_id, command)` 目标；最终保留的额外重复occurrence为127。**110是组数，127是超出每组首条后的occurrence数，二者均不是错误样本数。** 这些条目仍为expert-origin监督数据，不能纳入本项目自身经验数量。

检查范围是字段自洽与记录一致性；它没有重tokenize、重放专家trajectory、检查所有hidden-state语义或测量policy效果。0字段错误/0交叉不等于公共状态充分、标签唯一正确或全局无污染。

## OBSERVED：148与127符合既有计数约定

[src/sft/dataset.py:274](/home/lizening/wt-r19-g4-consumer-contract-repair/src/sft/dataset.py:274) 先对 `prompt_counts` 及task-step计数，再于276–286行以 `(prompt, completion, target_command)` 的exact hash跳过重复并保留accepted项；291行的重复prompt统计仍使用去exact前的计数。代码仅被阅读，函数未被调用。

旧 [sft_dataset_summary.json](/home/lizening/wt-r19-g4-consumer-contract-repair/reports/sft_dataset_summary.json) 记录重复prompt occurrence148、exact重复移除21；最终JSONL上的127满足纸上关系 **148−21=127**。这两个统计口径不同且相容，**不应报作数据不一致，也无理由据此修复或重建原件**。exact去重不以“同prompt只能保留一个目标”为条件；不同completion/command的多目标保留符合现有定义。

## INFERRED / NOT_PROVEN：三种情况不能混称错误

| 解释 | 现有证据允许的判断 | 仍未证明 |
|---|---|---|
| 动作多解 | 同一可见输入可容许不同的可行搜索/操作顺序；专家选择某一条成功路径不表示其他可见合法动作错误 | 110组中哪些动作在同一真实状态都能成功；原记录各自成功不证明可跨状态互换 |
| 有界输入歧义/状态别名 | 同一task/observation/H4/map文本可能对应不同的更早历史或潜在环境状态；因此目标不同不必是格式或标注错误 | 每组是否确有状态别名、哪些历史被截断、是否存在两种状态都有效的共同动作，以及是否影响新任务收益 |
| 真正数据错误 | 需要ID/command失配、completion不符、hash破坏、时点/trajectory绑定错误等具体证据；本检查覆盖的机械项为0错误 | 未核验的语义或来源错误不能仅凭多目标宣布不存在，也不能仅凭多目标宣布存在 |

这里只是在区分竞争解释，没有把110组逐条分类、选择多数目标、生成soft targets、删除条目或增添新训练规则。没有新回放或数据实验，因此上述多解与状态别名仍为候选解释，**NOT_PROVEN_PER_GROUP**。

纸上损失解释：同一个学生输入x有不同目标y时，交叉熵累计的是 `−Σ_y n_y log p(y|x)`。多目标会影响单一确定性输出的exact-label匹配及梯度分配；它不自动构成逻辑错误。必须区分“匹配某条专家next-action”与“任务终局成功”：观察到多目标不能给出ALFWorld成功率上界，更不能用127/20,967当错误率、损失率或可修复headroom。此处未估计任何数值学习上限，也不提出修改输入窗口/提示接口。

## INFERRED：被救回的干预价值不等于学习收益

历史同前缀差值 `V_i = R_i(固定恢复→冻结A) − R_i(A)` 是已测分支的终局增量；`V_i=1` 能作为纠错候选的来源事实。待证明的学习收益却是新任务上的 `E[R(由候选更新后的C)] − E[R(冻结A)]`，以及相同训练预算下C−B。它们涉及更新后的权重、新任务分布及采纳造成的梯度，不能由前一个差值推出。

原因包括：恢复teacher看过模型生成的subgoal，学生公共输入投影未必保留可区分信息；一次干预改变整个后续suffix，不能把终局增量全归给一条目标；成功可能容许多个动作；少量重复任务可能只导致记忆；采纳可能以损害原本成功的任务换取训练case拟合。即使一个干预在原case上确有正值，也不保证模仿该action能改善强基座在新任务上的期望回报。反过来，neutral成功的动作也可能具有一般学习价值，不能仅因其增量0就先验宣告无用。

因此保留原A/B/C对照及证据边界：C>A才有超过强基座的证据，C>B才可能支持该增量采纳配方相对普通成功过滤的优势，且还须满足新任务隔离、共同训练预算、伤害与完整获取成本要求。这是未来验证需求，不是本轮已获科学授权或已得到的收益。

## 当前决定不变

DATA_FEASIBILITY仍仅为 **READY_FOR_PROTOCOL_DESIGN**；TRAINING_DATA_READY仍 **NOT_READY**；新采集/模型/环境/训练/统计/selector均 **NO_GO / NOT_GRANTED**。新增检查增强的是既有专家数据机械自洽证据，不增加自身救回样本、不证明学生输入充分，也不解除单步纠错11states/10tasks的稀少与家族偏斜。

不改原专家数据、科学树、旧报告/receipt、原封存清单或共享INDEX；不commit/push、不派agent。科学85/2da保持，R19累计5142 generations/7949 reset-inclusive ops不变，本次科学调用0。所有新增内容仅为本目录加法补充，交由协调方独立审阅与发布。
