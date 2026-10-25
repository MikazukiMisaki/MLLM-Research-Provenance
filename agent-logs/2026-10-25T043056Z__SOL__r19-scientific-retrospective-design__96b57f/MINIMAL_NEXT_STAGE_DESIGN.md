# 下一阶段最小方案：冻结停止规则的可执行性与证据覆盖审计

状态：DESIGN_ONLY / NOT_STARTED。当前只完成方案与独立审查；本文件没有为离线审计、新 G4、live pilot 或训练发放执行许可。R19 的一次性 G3/G4 许可均已消耗。

## 决定与研究问题

只建议考虑一轮零新增推理的离线审计。暂不推进新的自适应控制器实现或效能实验。

唯一问题：**R19 已冻结的公共状态规则能否在当时可见的信息上作出可追溯的 handoff 决定，以及现有 measured suffix 到底支持多少这样的决定？** 这是可执行性和证据覆盖问题，不能识别总体因果效应，也不搜索最优停止规则。

本阶段既不选择“何时介入”，也不训练“何时停止”。不把 CONTINUE 优势转化为未经授权的 entry selector 研究。

## 固定输入、样本与规则

- 数据仅来自 authentic G3 run `260422ac02bd42a8b2929d7ef240526b` 和已正式验收的 G4；source2da / analyzer85 保持原样。
- 固定全部 36 eligible 状态；保留 6/15/15 原始分层、39 attempts 的分母说明和全部 exclusion。不得只挑 2 个 oracle case 或 7 个 supported case，不补样、不改 quota，不重跑127 source。
- 唯一规则就是原规则：每个已实际执行的 recovery checkpoint j>=1，原检测器 SATISFIED 则交回；NOT_SATISFIED/UNKNOWN 则继续，受到原 terminal、invalid 和 K<=5 的停止约束；到 cap5 交回。
- UNKNOWN 不能改成 K1/K2 fallback，不能人工改写 subgoal、扩展谓词、调用模型判断、改 prompt/decoding/recovery/suffix/horizon。
- 当前已知两例 oracle-over-K2 均 UNKNOWN；不能把“研究想解释这两例”变成针对它们修改的规则。
- 原R19诊断是passive/offline记录；≤j指可用信息边界，不代表原运行在墙钟j在线部署过停止器。本审计也不能将它升级为已执行的live控制决定。

版本、原始文件路径和哈希以 [observed_existing_results.json](evidence/observed_existing_results.json) 为准；包含正式 summary SHA6ff56b7... 和原 branches SHAeff9b5e...。未来授权时须重新核验，任何漂移先停止。

## 一轮审计应做什么

1. 在查看进一步 outcome 详情前，固定本文件、唯一规则的 source/协议哈希、表格字段和比较目标。现有团队已经看过 R19 结果，必须诚实称作 retrospective audit；输入遮蔽不能把它变成新的 held-out 验证。
2. 整理 36/36 状态的既有 detector decision/coverage 表。仅在 checkpoint j 当时可用的 original subgoal、public observations/actions、合法动作映射和已执行 transition 上验证决定；任务 ID、family/stratum、source 最终成败、未来观察、reward、oracle K 和未来 suffix 不得进入决定。ID 只用于审计联结，不是决策特征。
3. 列出每次停止的 checkpoint、typed predicate、supporting transition IDs、时点边界、selected K/reason 和 suffix mapping 依据。没有实际到达的 checkpoint 不补造记录；保留 terminal、invalid、alias 和未执行动作的原语义。
4. 检查全部 10 个结局随 K 变化的状态（8 种非恒定模式）、两例 oracle-over-K2、K2 相对 CONTINUE 的 rescue/harm，以及已有 7 supported /29 unsupported 的理由。不能仅解释赢家，也不能将“没有观察到进展”当作无效导航的证据。
5. 优先引用已有生产记录和既有测试证据。若因果时点/映射性质没有证据，标 NOT_PROVEN。不可为了完成表格启动环境、调用模型、重跑 analyzer/validators/G4、做新的策略 replay 或生成 missing suffix。
6. 只有满足原 exact mapping 和 supported 语义的记录才能报告对应的既有条件性 outcome/cost。29 个 coverage-only 保持 coverage-only；不填0、不填1、不当 dropout，不能把7/7换成全队列成功率。任何新的完整 fallback outcome 评估都需要另行写明分析修订与授权，不得覆盖原 G4。
7. 分开报告成功、伤害、logical full-branch tokens/model calls/actions、detector CPU 开销，以及已支付的物理研究成本。不用 recovery-only tokens 代替完整策略成本。

## 对照、验收和推进门槛

CONTINUE 是首要实用基准，K2 是在 R19 开发结果上选择、在新阶段提前冻结的固定时长基准，K1 保留原 duration 基准。只赢 K1 或只相对 K5 省成本，不够支持实用价值。不能把本轮 K2 数据选择写成独立预注册优势。

| 检查层 | 明确验收标准 | 不满足时 |
|---|---|---|
| 证据完整性 | 输入哈希全部匹配；36/36 有账；原始结果与证据零修改；0 新模型/环境操作 | STOP，保存证据，不修补旧数据 |
| 时点与语义 | 决定引用未来信息为0；未证明的判断全部标明；原 UNKNOWN/terminal/invalid/fallback 语义完整保留 | STOP，不调整规则取得通过 |
| 覆盖与映射 | 7 supported 和29 unsupported 均说明；无不具证明的 suffix outcome/cost 声明 | 只能交 coverage/NOT_PROVEN，不能给策略效果 PASS |
| 科学报告 | 36/36有去向；原已测结果和成本有完整引用；D5未估计部分保持NA，未知伤害不当作无伤害；两例及其他异质状态均解释或明确未解释 | 补文档仅限时间预算内，不增样本/策略 |
| 是否值得另写下一阶段方案 | 存在预先固定、公共可用、与固定 K 不同的可执行时点机制，且有包含 UNKNOWN、伤害及成本的不确定性分析支持相对 CONTINUE 的合理价值主张 | 关闭当前候选或 INCONCLUSIVE；不给 live GO |

“审计完成”不等于“自适应停止有效”。不要求达到 oracle32/36；任何低于 oracle 的策略也可能有价值，但价值必须有独立可执行机制和适当对照支撑，不能由事后赢家替代。

目前原 detector 在两例 headroom 上都是 UNKNOWN，29例没有整体策略估计；K2 与 CONTINUE 成功率相同且成本更高。故**新推理/新控制器的当前状态是 NO_GO**。只读审计可形成有价值的解释性负结果，不能承诺它一定带来下一轮 live。

## 最小资源与停止条件

提议未来单独授权的资源上限：一次固定审计、最多 4 人时、36 个既有 eligible 状态、0 新 generations、0 environment operations、0 G2/G3/G4/训练。最多一轮事实核对与独立复审，无自动重试或“再找一种规则”。

出现下列任一情形立即停止并交回：

- 原始哈希/来源不符、时点泄漏、无法证明所声称的 suffix mapping。
- 为解释 headroom 必须看未来、使用 task/stratum/outcome 选择 K、改 detector/fallback、加模型评判，或排除不利案例。
- 需要额外模型/环境操作、缺失 suffix 重跑、新 source、扩大 N/K 或改变 frozen inputs。
- 达到 4 人时仍无法完成证据表，或可用信号/整体收益仍无从证明。

若完成后仍仅有 7 个有条件成功、UNKNOWN 无整体估计，或可证明的策略仍被 CONTINUE 在成功与完整逻辑成本上支配，则停止推进当前候选。不得为挽救主张在同数据上搜索替代谓词。

## 若未来确有新候选，仍需哪些前置条件

本方案**不安排 live pilot**。只在审计后另行评审：明确的新协议修订、唯一规则/fallback/可用信息/实现冻结、独立可用且未用于规则设计的 TRAIN 身份清单、实际 source/attempt/cost 上限及新用户授权。不能把已看过的36例、原127 source的另一前缀或重新划分后的同一批数据称作新验证；不能动 held-out 来补额。

未来目标要先选成功优效还是保成功省成本，并提前确定最小有价值收益、可容忍伤害/非劣界限、paired win/loss 假设、任务依赖和多重比较处理，再计算样本量。净 oracle2/36 不能直接决定 N；一个资源上限很小的 mechanism pilot 只能检验可执行性，不能宣布确认5.56pp。

Sol Research 负责独立提出反证和最小设计；Sol reviewer 负责原始结果核对、统计/成本审查和最终设计整合。未来 Luna 的任何执行必须等单独任务、独立审查及明确授权；本轮不派执行任务。
