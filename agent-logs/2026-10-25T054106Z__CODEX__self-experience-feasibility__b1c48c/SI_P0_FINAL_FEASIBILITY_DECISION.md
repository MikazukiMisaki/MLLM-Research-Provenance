# SI-P0 最终学习可行性决定与设计审查限定

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
