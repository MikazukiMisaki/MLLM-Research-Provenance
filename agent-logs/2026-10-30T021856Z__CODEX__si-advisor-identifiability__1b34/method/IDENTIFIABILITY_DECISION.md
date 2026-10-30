# Self-generated 经验研究的概念可识别性：独立决策

**结论：已有记录足以报告指定 checkpoint 在固定 82 任务上的配对差异；没有建立“自生成来源本身”的净因果效果、完整续训算法在目标总体上的平均增益，或跨训练 seed 的稳定改进。** 这三项未知不是同一个“样本太小”问题，不能只靠扩大同类记录数同时解决。当前四项前置条件不变；本记录不设计新实验。

本次只阅读已核证的方法、接受记录及既有统计/诊断材料，核对文件摘要，没有重算科学统计、访问候选内容/结果或调用模型/环境。英文可整合段落见 `IDENTIFIABILITY_DISCUSSION_EN.md`；它是候审文本，不回写原协议或既有研究问题。

## 一、研究问题有不同的可回答层次

| 问题层次 | 当前证据能回答什么 | 使更强主张成立所需的证据类型；非实施方案 |
|---|---|---|
| 指定 checkpoint 在固定任务上的表现 | 已接受 246 个结果形成 82 个配对任务记录：A/B/C 为 65/68/67；C−A +2.44pp，C−B −1.22pp。原规则结论为 INCONCLUSIVE。[E1–E3] | 可追溯的结果身份、统一指标、完整配对、方法与实际记录的一致性。既有审查已在记录范围提供，不等于重新运行。 |
| 指定两种数据构建/续训流程的比较 | 本轮是共同 P0 下两个已实现流程的实例，控制家族父数和监督剂量，记录各一训练 seed。[E4] | 若主张流程的平均效果，需要明确流程包含哪些采集/筛选/优化环节、其随机机制及哪些条件固定，并有足以支撑该平均量及不确定度的证据。单次训练实例不能估计未观察的训练变异。 |
| self-generated“来源本身”的效果 | 来源与训练任务、状态、行为内容、筛选和输入计算量共同变化；现有对比不能把净差分解给某一项。[E4,E5] | 必须先把“来源”定义为可区分且可追溯的操作性因素，并有能够区分来源作用与这些共同变化的识别依据。只使用 source 标签、相同监督 token 或相同家族数不是该依据。这里不提出操纵或分组方式。 |
| 对未见任务/场景总体的改进 | 目前只有固定 TRAIN 排程和不完整历史隔离，未建立代表性目标总体。[E6,E7] | 目标总体的来源/单位/版本、项目历史接触及场景或语义依赖的可证明边界，以及任务记录对该总体有何代表性的依据。parent 数或官方 unseen 名称不替代这些证据。 |
| 覆盖或循环造成失败的机制 | 已观察八个双物体任务全部失败、B/C 各两个该类训练父/八例，部分失败轨迹有重复块；都是事后描述。[E5] | 能排除或区分任务难度、关键状态覆盖、动作质量、共同起点和交互约束等替代解释的证据。当前没有这种区分，不把候选解释升级为原注册假说。 |
| 自主、反复自我改进 | C 由专家监督 P0 的成功轨迹形成监督续训，依赖外部成功反馈；R19 未训练 SI-U1 策略。[E4,E8] | 对“自主”所覆盖的外部知识/反馈及多轮过程有明确范围和对应结果证据。现有一轮续训和后见恢复选择不支持这种更强概括。 |

**可识别性与精度不同。** 在已有结果上，固定排程的差值定义清楚、可计算；它是否代表新总体是外推问题，是否代表平均训练流程是重复与随机性问题，是否归因于 source 单因素是识别问题。较窄的置信区间本身不会把未识别的 source 因果量识别出来；同样，改写研究问题也不会产生缺失的任务或训练随机性证据。

**任务/状态差异的含义取决于主张。** 若对象是完整的两条数据生成与训练流程，那么不同采样状态和成功筛选可以是流程本身的一部分；不应笼统把它们都称为必须去除的统计混杂。若对象是排除这些差异之后的“纯来源效果”，现有数据却没有支持这种分离。必须先明确要解释的处理是什么，才能判断哪些变化是其组成/机制，哪些是需要另行识别的竞争因素。P0 共同起点和监督剂量匹配是有用控制，但没有单独解决这个问题。

## 二、研究问题—目标总体—seed 不确定度的依赖

需要先明确主张针对**哪个过程的哪种结果**，以及是在固定任务/固定 checkpoint 上报告，还是对某个任务总体、训练过程分布作推广；随后才有可辩护的不确定度来源。这里列的是概念依赖，不是新协议步骤或已选研究总体。

- 对当前固定 checkpoint，任务配对使同任务上的差异可描述；不能把三臂轨迹、动作数或多个记录副本当新任务。
- 对任务总体，需要适用的抽样/模型依据。共享 scene 或模板可能带来任务间相关；目录互异、无精确文本交集、Holm 校正和 union bound 都不自动建立独立二项计数。[E6,E7]
- 对训练算法总体，还涉及训练随机性和可能的数据构建随机性；当前每臂一 seed 无法识别这些方差。不同 seed 标签不是独立性的证据，epoch 顺序 seed 也不是独立的完整训练重复。
- 如果声称“对不同任务训练出来的策略也有效”，还多了一层训练数据来源变异，不能由当前同一已选数据集上的任何历史单次结果代替。
- 这些依赖决定精度主张需要解释的量，也影响完整资源范围。现有历史耗时和候选名称上界不是对这种精度/预算的通过证明。[E9]

## 三、基座预训练未知与项目内独立性

项目内独立性关注采集、开发、训练、验证、结果访问和研究选择的具体记录；基座预训练/外部后训练曝光关注模型进入本项目之前的来源。它们需要不同的证据，不能由一个 registry 包办。已有本地哈希可确定某些保留文件身份，却不能证明模型供应方语料排除了某个任务或语义等价物；没有找到外部包含证据也不是排除证据。[E6]

三臂共享 P0 并不使未知历史曝光自动“相消”：本项目没有证明先前熟悉程度不会影响不同续训流程的收益。另一方面，预训练未知也不意味着已证明数据污染或所有本地观察无效；它约束“未见任务”“从自身经验新学会”等更强解释。可继续报告限定范围的实际比较，不能利用该区分降低既有独立任务前提。即使供应方资料将来补强一层，项目内开发/选择暴露仍需单独审查；反过来也一样。

## 四、当前可继续的证据工作及边界

可以继续核对已保存 source→选中行→训练→checkpoint→配对结果的身份链，注明专家起点、成功条件和哪些排序只见规则没有全量重算；对既有决策版本标明原冻结主张与事后解释；整理已核证 scene/版本/历史账本覆盖与成本遗漏。每一项只陈述找到了什么和仍缺什么，不从未找到记录推断未使用。

不会从这些证据选择新任务/分组/seed/阈值，也不拟定采集或训练安排。现有“覆盖不足”“成功筛选偏向容易状态”“重复行为无进展”“input compute 差异影响学习”均是可讨论的候选解释，并未被此材料验证。R19 的 oracle 32/36 相对固定 K 30/36 是不同研究的后见窗口，不能填补上述识别或总体证据缺口。[E5,E8]

**阶段决策：概念问题可以更精确地表述，但新研究的可检验性/独立总体/精度/完整预算仍未建立。只有四项全部先有证据并独立复核，才开始设计新评估。** 当前工作直接支持完成已有实证比较与局限的论文，而不是为扩大运行提供许可。

## 证据索引

- E1：[原冻结统计计划](/home/lizening/research-notes/agent-logs/2026-10-29T225000Z__LUNA__si-u1-extraction-publication__062a/frozen_and_review/FINAL_ANALYSIS_PLAN_PILOT82.json)。
- E2：[独立统计明细](/home/lizening/research-notes/agent-logs/2026-10-29T222200Z__SOL__si-u1-independent-recompute__c2356/INDEPENDENT_STATISTICS_DETAIL.json)。
- E3：[科学结果接受记录](/home/lizening/research-notes/agent-logs/2026-10-29T230000Z__LUNA__si-u1-scientific-review-publication__c2356/astra/C2356_SCIENTIFIC_RESULT_INDEPENDENT_ACCEPTANCE.json)。
- E4：[已审方法](/home/lizening/research-notes/agent-logs/2026-10-30T034000Z__CODEX__si-methods-amendment__e170/METHODS_REVISED.md)；[该版本独立接受](/home/lizening/research-notes/agent-logs/2026-10-30T005557Z__CODEX__si-methods-independent-review/REVISED_METHODS_ACCEPTANCE.md)。
- E5：[事后诊断独立复核](/home/lizening/research-notes/agent-logs/2026-10-29T113523Z__ASTRA__three-arm-prospective-design__a55d1af9/POSTRESULT_DIAGNOSTIC_INDEPENDENT_REVIEW.json)。
- E6：[隔离与曝光层级决策](/home/lizening/research-notes/agent-logs/2026-10-30T015944Z__CODEX__si-isolation-provability/ISOLATION_AND_EXPOSURE_DECISION.md)及所引历史/场景审计。
- E7：[原分析绑定审查](/home/lizening/research-notes/agent-logs/2026-10-29T113523Z__ASTRA__three-arm-prospective-design__a55d1af9/FINAL_ANALYSIS_BINDING_INDEPENDENT_REVIEW.json)。固定排程、seed、推断假设与原判定范围。
- E8：[R19 已审方法](/home/lizening/research-notes/agent-logs/2026-10-30T020500Z__SOL__r19-thesis-methods-v2__8be2/R19_METHODS_RESULTS_DRAFT_EN_V2.md)；[独立接受](/home/lizening/research-notes/agent-logs/2026-10-30T010928Z__CODEX__r19-methods-independent-review/R19_V2_ACCEPTANCE.md)。
- E9：[四前提独立决策](/home/lizening/research-notes/agent-logs/2026-10-30T012341Z__CODEX__si-four-prerequisite-methods-review/FOUR_PREREQUISITE_DECISION.md)；[长期计划](/home/lizening/research-notes/agent-logs/2026-10-30T002800Z__CODEX__si-long-term-research-plan__a40/LONG_TERM_PLAN.md)。

各文档当前 SHA-256 见 EVIDENCE_HASHES.json；它不代替原审计，亦不表示本次已重新执行历史过程。
