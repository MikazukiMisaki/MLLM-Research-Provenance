# SI-U1：从观察到候选解释的科学批判与导师说明

状态：`EVIDENCE_SYNTHESIS_ONLY; NO_NEW_EVALUATION_DESIGN`。本次只阅读已有方法、冻结计划、接受记录与脱敏诊断，核对文档字节；没有重新计算科学结果，没有选择新任务、样本、臂、seed 或阈值，没有模型或环境调用。以下数字来自既有已审结果，不冒称本次重跑或新的独立统计复算。

## 导师可读说明

目前最可靠的成果是一项范围明确、结果无法判定的比较：从同一个专家监督起点 P0 出发，专家数据续训 B 和自身成功经验续训 C，在同一组 82 个 TRAIN 任务上分别完成 68 和 67 个，原始 P0 完成 65 个。C 相对 P0 的净差为 +2.44 个百分点，相对 B 为 −1.22 个百分点。原来冻结的两个主要比较均未通过预先规定的判定规则。不能因此说自生成训练有效，也不能说没有效果或与专家数据等效。

“自身经验”的含义需要具体说明。C 的动作来自 P0 先前执行并成功的轨迹，再经过已有选择规则形成监督样本。P0 已经接受专家监督，成功标签依赖环境反馈，数据选择与训练管线是人为指定的。因此这是专家起点上的成功轨迹自训练步骤，并不等于不依赖专家或外部反馈的自主改进，也不是多轮自我改进已获验证。

两种续训的任务家族父数和监督 token 数一致，这是有效控制；但专家样本与自身样本来自不同任务和状态，而且 B 重访原始专家训练样本、C 使用选中的 P0 成功经历。来源、熟悉程度、状态分布、行为内容与选择机制一起改变，输入 token 总量也不同。比较可以说明这两条已实现管线在此样本上的表现，不能把差异单独归因于“self-generated”这种来源属性。

两个物体任务的共同失败值得记录，但不是已解释的失败：八个评估任务上 A/B/C 都没有成功，而 B/C 各只包含两个该类训练父任务、八个唯一示例。覆盖不足是看过结果后提出的候选解释。既有记录也兼容任务难度、状态覆盖不合适、所选动作教学价值不足、共同起点或固定交互配置的限制；尚不能在这些解释之间做因果裁决。四遍展示不会把八个唯一示例变成三十二个独立示例。

R19 研究的是另一个问题：在已选的状态上干预恢复时长，而不是评价 C 的续训效果。CONTINUE 与最佳固定时长都成功 30/36；后见选择得到 32/36，依赖行动当时不可获得的未来结果。它超过最佳固定时长的两例本来就被 CONTINUE 完成，不能当成相对原策略的两个新救回，也不能用来补强 SI-U1 的自我改进主张。

## 观察—候选假说—替代解释

| 已观察且来源明确的事实 | 可讨论的候选解释；均非本次新增预注册 | 同样兼容的解释与当前无法识别之处 |
|---|---|---|
| C−A 为 3 胜/1 负，C−B 为 3 胜/4 负；两项 Holm p 均为 1.00。[E1–E3] | 该自训练管线也许改变了少数任务的行为，净收益可能较小。 | 有益或有害变化均未被精确排除；只有一个续训 seed，不能估计训练随机性。固定任务与历史曝光未知，也不支持总体效果或跨场景泛化。不能将“不显著”写为“无效”。 |
| B/C 各 78 父、312 唯一样本、6,240 训练监督 token；输入 token 分别 661,620/695,872，任务与精确输入不重合。[E4–E6] | 自身经历可能提供与当前策略相关的状态经验。 | 状态相关性本身未被单独量化或操纵；成功筛选也可能偏向易任务或遗漏失败状态。家族数匹配不等于具体状态、难度、轨迹质量或总计算量匹配。不能认定这些替代机制已经发生。 |
| A/B/C 在八个双物体任务均为 0/8；B/C 各两个训练父、八个唯一示例。[E5–E6] | 有限的任务/状态覆盖可能限制这一类别的完成能力。 | A 未接受这两次续训也失败，不能将共同失败归因于某一续训来源；“类别有数据”不等于关键状态覆盖，“数据少”也不等于已证明增加数据有用。任务困难、动作质量与共同配置限制尚未排除。 |
| 结果后选定的 17 任务、51 轨迹中，37 条失败都在第 50 动作记录 done=true/reward=0。[E5–E6] | 现有行为未在记录的执行期限内完成任务。 | 不能仅凭步数认定评估器 horizon 截断、环境缺陷或某种策略机制；既有复审明确称 terminal-at-step50。不能外推全体失败的机制或总体发生率。 |
| 这 51 条轨迹的 2,206 次输出按冻结映射可对应实际执行请求；失败轨迹中出现重复命令块。[E5–E6] | 某些失败可能涉及持续无进展行为。 | 格式合法不等于行动合适；重复可能合法，失败轨迹更长、检测机会更多。字面模式不是语义循环；不能称“循环导致失败”或由此发明纠错规则。 |
| 11 个分歧配对在第一次不同执行命令前，记录的模型输入、观察和动作映射哈希一致。[E6] | 已训练策略可在相同记录输入下产生不同动作。 | 不能说明隐藏状态完全相同，也不能说明第一次分歧就是最终成败的关键原因；11 个比较只涉及九个任务，不是 11 个独立任务。 |
| R19 的 CONTINUE/K2 为 30/36，oracle 为 32/36；K2 相对 CONTINUE 有两救回、两损失。[E7] | 不同已观察状态可能对应不同的有利交接时长。 | 后见最优不等于在线可识别；同一样本选择最佳固定 K，且按干预开始后的资格规则条件化。失败层仅六例、无 eligible 双物体前缀，也没有 SI-U1 续训效应。 |

## 原冻结主张与事后窗口必须分开

原分析计划 [E1] 明确冻结 C−A/C−B、精确双侧 McNemar、两比较 Holm、完整配对要求和原判定规则。正式结果 [E2] 与科学接受记录 [E3] 对应这套规则，结论仍是 INCONCLUSIVE。修订方法 [E4] 区分五个百分点的科学兴趣与十个百分点的原操作性信号阈值；不得混称或事后交换。这里是在记述历史规则，不建议新阈值。

两物体覆盖解释、重复行为解释，以及从分歧任务观察得到的机制讨论，来自结果之后的诊断窗口 [E5–E6]。完整纳入所有九个分歧任务和八个双物体任务，避免了在这两个类别内部只挑好讲的个案；但结果依赖的类别选择仍然存在，不能变成独立验证。新命名、重写段落或引用原冻结计划，都不能让这些解释获得事前注册身份。

技术提取器在评估后修订、原失败收据保留、统计规则未改的情况，也应按 [E4] 明示。该受限记录不证明所有人和进程此前都未见结果。今后若要将探索得到的解释用于确认性论证，必须明确其探索来源；本次不编写该研究方案。

## 可读证据路径

以下入口按导师阅读便利排序。旧来源中出现的未来实验建议不在本记录中采用；当前以长期计划 [E8] 的四项前置门槛为准。

- **E1 原冻结统计计划**：[FINAL_ANALYSIS_PLAN_PILOT82.json](/home/lizening/research-notes/agent-logs/2026-10-29T225000Z__LUNA__si-u1-extraction-publication__062a/frozen_and_review/FINAL_ANALYSIS_PLAN_PILOT82.json)。区分原主比较与后来的机制解释。
- **E2 已完成正式结果**：[FINAL_PILOT82_PAIRED_ANALYSIS_C2356.json](/home/lizening/research-notes/agent-logs/2026-10-29T225000Z__LUNA__si-u1-extraction-publication__062a/frozen_and_review/FINAL_PILOT82_PAIRED_ANALYSIS_C2356.json)。本次不重新运行提取或统计。
- **E3 科学独立接受记录**：[C2356_SCIENTIFIC_RESULT_INDEPENDENT_ACCEPTANCE.json](/home/lizening/research-notes/agent-logs/2026-10-29T230000Z__LUNA__si-u1-scientific-review-publication__c2356/astra/C2356_SCIENTIFIC_RESULT_INDEPENDENT_ACCEPTANCE.json)。数字的既有独立复核出处。
- **E4 当前已审方法稿**：[METHODS_REVISED.md](/home/lizening/research-notes/agent-logs/2026-10-30T034000Z__CODEX__si-methods-amendment__e170/METHODS_REVISED.md)。说明专家起点、C 的成功动作来源、匹配范围、选择规则与事后提取修订。
- **E5 脱敏诊断摘要**：[SHAREABLE_DESCRIPTIVE_SUMMARY.md](/home/lizening/research-notes/agent-logs/2026-10-29T222600Z__SOL__si-u1-disagreement-diagnostic__c2356/SHAREABLE_DESCRIPTIVE_SUMMARY.md)。最易读的两物体、重复行为和数据覆盖说明；其“待复核”历史状态由 E6 补充，不改原稿。
- **E6 诊断独立复核**：[POSTRESULT_DIAGNOSTIC_INDEPENDENT_REVIEW.json](/home/lizening/research-notes/agent-logs/2026-10-29T113523Z__ASTRA__three-arm-prospective-design__a55d1af9/POSTRESULT_DIAGNOSTIC_INDEPENDENT_REVIEW.json)。接受描述性数字，同时保留非因果边界。
- **E7 已审 R19 说明**：[R19_METHODS_RESULTS_DRAFT_EN_V2.md](/home/lizening/research-notes/agent-logs/2026-10-30T020500Z__SOL__r19-thesis-methods-v2__8be2/R19_METHODS_RESULTS_DRAFT_EN_V2.md)；时间顺序补充：[ENROLLMENT_TIMING_CLARIFICATION.md](/home/lizening/research-notes/agent-logs/2026-10-30T010928Z__CODEX__r19-methods-independent-review/ENROLLMENT_TIMING_CLARIFICATION.md)。资格队列在延长共同恢复路径前冻结，不能误写在所有恢复结果之后筛出；资格仍依赖初始干预后的条件。
- **E8 当前长期计划**：[LONG_TERM_PLAN.md](/home/lizening/research-notes/agent-logs/2026-10-30T002800Z__CODEX__si-long-term-research-plan__a40/LONG_TERM_PLAN.md)。独立任务、可检验假说、统计精度和完整预算全部先有证据并独立复核，之后才开始设计新评估。

各文档实际字节 SHA 见同目录 EVIDENCE_HASHES.json。本记录只提供可追溯解释，不重新认证原始轨迹，不披露私人任务内容，也不扩大既有结果适用总体。
