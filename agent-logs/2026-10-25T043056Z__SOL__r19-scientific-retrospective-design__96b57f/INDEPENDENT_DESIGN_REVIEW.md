# 独立方案审查

审查身份：Sol Technical Lead / Independent Reviewer。状态：DESIGN_REVIEW_ACCEPTED_WITH_SCOPE_REDUCTION；EXECUTION_AUTHORIZATION=NOT_GRANTED。本文件不是 launch clearance，也不是新策略效能 PASS。

## 实际分工和审查对象

用户直接指定与现有 Sol Research 协作。任务已实际派发至 thread `01a165de-c75e-7120-abc9-fa74cde1f17f`，并从该线程读到确认、完整草案与 V2 交接；不是只产出未发送的任务文件。Sol Research 负责竞争解释、可证伪最小设计与停止条件；Sol reviewer 独立核验正式结果、原分支字段、统计和成本，并决定保留范围。另有只作纸上推理的独立统计 critic，意见见本目录 evidence/independent_statistical_critique.json。

审查的 Sol Research V1 原字节 SHA256：
`b204ed7a59b9f450b758170314798486793077ccd57325cb18127bc138243668`，
原文件 /tmp/r19-design-review-20261025T043034Z-codex/R19_MINIMAL_FALSIFIABLE_FOLLOWUP_DESIGN.md；本目录 sol_research_submission 有原字节副本。

其 V2 修订 SHA256：
`eba6a25907d3fa9f818eff347696f0d554b91166652e025590b29deea68f1515`，
增加两例都来自 random-control、failure 层没有观察到额外 headroom 等限制。保留原版，不能把后来的完整事实倒写成开发方最初已经独立核验的结论。

## 关键独立核验

正式 summary SHA6ff56b7...、原 branches SHAeff9b5e...均匹配。逐字段读取两个 oracle-over-K2 状态，确认：

- 分别只有K1、只有K5成功；均 random-control。
- CONTINUE 在二者均成功，所以不能将其写成相对原 actor 的新 rescue。
- 原公共检测器在各实际 checkpoint 均 UNKNOWN/UNSUPPORTED，selected K5，COVERAGE_ONLY，estimated success/cost 为 null。
- 原 supported guard 不能因有 selected_k 或 branch_mapping_exact=true 被绕过。
- failure6 的 K2=oracle2，样本不足以断言总体无 headroom。
- K2 与 CONTINUE 都30/36，前者平均 logical tokens 高31.9%；固定时长比较均无显著优势，不等于等效。

这些是既有字段和纸上解释，没有运行 analyzer、validator、detector、policy replay、统计检验或新的结果流水线。

## 对开发方设计的独立裁定

| 项目 | 裁定与理由 |
|---|---|
| 仅审原D5、固定36、不搜索规则 | 接受；明确保留UNKNOWN/NOT_SATISFIED继续至cap5，以及原terminal/invalid/horizon。 |
| 比较CONTINUE、固定K2、K1 | 接受；不能只赢弱基准，不把同样本选择K2写成新阶段独立发现。 |
| 7/7和29缺口 | 接受其不补填原则；全部缺口继续公开，审计完成不等于全队列策略效果。 |
| 原文“因果可识别性” | 收紧为“可执行性与证据覆盖”；只读回顾可检查时点合法性，不能识别总体因果效应。 |
| 原阶段A 8人时 | 收紧为总计4人时、一轮固定审计。这是资金/注意力上限，不是统计阈值。 |
| 条件性24+7=31 | 只可保留作注明前提的宽松纸上上界，不是执行成绩；且未达到oracle32本身不是否决任何策略的充分理由。整合最小方案无需依赖这项额外证书。 |
| 阶段B 12sources /3000gen /5000ops /12GPU小时 | 本轮不采纳。原文诚实标为条件性草案，但当前没有公共信号与整体价值证据支撑投入；保留历史提案，不成为执行或自动下一阶段。 |
| 3触发/2family、110%CONTINUE成本门槛 | 不纳入当前决议。它们是开发方明确标出的投资偏好，不是R19推出的科学阈值；应在真正的新候选/目标/资源论证后另审。 |
| 小N效能确认 | 拒绝此类解读；未来固定规则2赢0输的精确p=.5只作数学例示，不能检验事后oracle。未来N不能由2/36净值直接决定。 |

独立统计 critic 与上述范围一致：本次是有限的规则/证据审计设计；无权据此训练控制器、扩样、调谓词或启动效能实验。

## 最终可审查版本与停止决定

协调方整合版以 [MINIMAL_NEXT_STAGE_DESIGN.md](MINIMAL_NEXT_STAGE_DESIGN.md) 为唯一当前最小方案，以 [SCIENTIFIC_RETROSPECTIVE.md](SCIENTIFIC_RETROSPECTIVE.md) 为科学判断依据。Sol Research 的原方案和后续 addendum 原字节保留，主张分歧公开，不用开发者自己的结论代替独立审查。

当前决定：

- DESIGN_ONLY：完成复盘、最小方案和独立审查。
- 可考虑另行授权：固定36例、最多4人时、0新增科学调用的可执行性/覆盖审计；不是已经运行或通过的预检。
- NEW_INFERENCE / ADAPTIVE_CONTROLLER / LEARNED_SELECTOR / LIVE_PILOT：NO_GO。
- 任何未来修改规则、补 suffix、新TRAIN数据或把passive变为治疗，均须新的协议与精确实现审查；旧G3/G4许可已消耗。
- 保持累计5142 generations /7949 environment operations（含reset），本轮新增0/0。

本设计没有追求必须达到32/36。推进应取决于可执行的公共信息机制、完整分母/伤害/成本和公平基准；若需要看未来、按旧结果选择规则、排除UNKNOWN或无限补样，则关闭当前候选。

## 冻结 V4 追加审查

Sol Research 已提交冻结 V4，SHA256 d8cf5966d17051a02ec6ecafd0d4f462ae354ccbc79c2f75ee023c1b5ed314e4；RECORD SHA25640b68f350017947facf13b479c53bb741dfe6e09763cc81f65ec2524d99eff53。Sol 已全文读审 V4，确认其采纳4人时、零调用、可执行性/覆盖术语、无oracle完全捕获门槛及live NO_GO。V4 原字节副本保持不变。

一项文字精确性由协调方纠正：36例中是10个结局随K变化的状态，分属8种非恒定五位模式；不是10种不同的非恒定模式。正式频数表未变。整合版已使用“10个状态（8种模式）”；原提交中的简写按此解释，不构成数据或处理改动。

V4 关于在线时点的限制被接受：passive诊断具有≤j的信息边界，也不代表原运行在j实际部署了停止器。审计只能核验可执行接口及证据覆盖。

## 最终交叉审查闭合

Sol Research 的最终 addendum SHA2569630ecd85b0927ed46b1c8e4808d33527ab85bf4d8c461341ff670cd296f5b99，配套RECORD SHA256de6b591099c7982c40a67148848909a94cf199a5175c105d6a47a65f014e9da4；已全文独立读审。其未发现改变stage-A-only/LIVE_NO_GO决定的实质事实/统计错误，提出一条执行范围限定，被协调方采纳：36例完整指证据去向及原已测结果完整引用，不要求补齐未估计D5成绩，29例结果/成本保持NA，未知伤害继续未知。整合版同时明确passive≤j信息边界不等于曾在线部署停止。

原被读审草稿SHA及最终整合SHA分别记录于evidence/cross_review_result.json；最后改动仅为以上限定和“10状态/8模式”的文字精确性，不改唯一规则、预算、研究主张、原结果或执行权限。所有交接原件保持原字节。交叉审查到此收尾，不再发起方案循环或执行任务。
