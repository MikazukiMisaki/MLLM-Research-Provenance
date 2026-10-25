# R19 最小后续设计与停止结论 — V3

日期：2026-10-25 UTC。状态：**DESIGN_READY_FOR_SOL_REVIEW；IMMEDIATE_LIVE_FEASIBILITY=NO_GO**。不是独立review PASS，不发放运行许可。

本版为当前建议，取代V1/V2中“条件性小试”作为潜在下一阶段的安排。两版旧文件及哈希原样保留；它们的12-source与3000/5000资源包从未获批，本版不再把它作为当前研究申请。当前仅保留零新增推理的因果可识别性收尾审计之设计与审查。

分工不变：Implementation Engineer负责竞争解释、可证伪设计和停止门槛；Sol负责原始证据、配对统计、成本边界及本文件的独立审视/整合。没有新增线程或派遣Luna。

## 1. 明确决定

**默认 NO_GO 新live、前瞻feasibility、扩样、learned selector和任何rule训练/搜索/调参。先把原唯一规则的可识别性审计收尾；即使审计材料完整，也不自动进入live。**

5.56pp是五个正K中事后选择的包络。新增原始证据表明，构成全部+2的两个random-control病例，在CONTINUE下本来都成功，在K2下失败。不同正K能避免这些已测的K2损失，但并未在这两例上提供相对CONTINUE的新rescue。冻结public detector对两例均无可用的SATISFIED区分信号。因此，“已有5.56pp，所以该detector值得立即live验证”这条动机链现在不成立。

这不证明任何未来的公共信息停止策略都不可能有效，也不证明failure人群没有headroom。它只要求本轮按实际证据停止，而非强行承诺一个live试验。

## 2. 证据身份与来源层级

原analyzer SHA保持 `85cbb92395e5e2420c2adeb1fa0634653e742910`；executedG3保持 `2da980f631badc25086d12db60d128ff507d3ae6` / run `260422ac02bd42a8b2929d7ef240526b`。旧review、raw evidence、clearance和shared INDEX/root inventories均不改。

本轮前文已只读核验：

| 输入 | SHA256 |
| --- | --- |
| 正式summary | `6ff56b7e9bc31c29bc9afd0c3ceea43c4fdf53b2addb29d3ce9f2c5e99b5d3c4` |
| 正式opportunity report | `92c066ad1c9c7f187430db82ad6285800e4f31005a1fd2933231d30d695df4bc` |
| Sol independent G4 acceptance | `7331b865778481ab4e1b10943eac0e4090ea004e214dbdfff283cfbe042833e6` |
| 冻结protocol document | `7668d7fa5422ad6ad7d3affc72b2e573ec19aae53314198fc14b46dc74c9a3d9` |
| 冻结machine protocol | `3d7d1865c807d12276a8109b06c55da4e9182df0ca05a0b5463f8128dd03e122` |

正式report位于 `/home/lizening/research-notes/agent-logs/2026-10-23T043602Z__LUNA__r19-g4-readiness__85cbb923/future_g4_report/`；独立验收/解释位于 `/home/lizening/research-notes/agent-logs/2026-10-25T040304Z__SOL__r19-g4-independent-result-review__85cbb923_dffaf4/`。

本次新增branch字段由Sol直接只读核验并在委托中提供，原件为 `/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z/branches.jsonl`，指定SHA256 `eff9b5e74d3d5daa928cb662dcc59fc3f434f66796b673679d40b374f3c8636f`。**本修订引用其已核验证据，不声称开发方又运行了一次独立raw校验、分组统计或policy evaluation。**

## 3. CONFIRMED：5.56pp来自哪里

既有36个eligible为failure6、success-control15、random-control15。CONTINUE30成功，K1..K5为29/30/28/25/24。K2与CONTINUE同为30/36，平均完整分支逻辑tokens却为9854.25对7470.2，增加31.9%。注册比较未建立更长固定恢复的显著优势。

Sol提供的既有结果分解：

| stratum | N | K2成功 | 正K oracle成功 | oracle-over-K2 |
| --- | ---: | ---: | ---: | ---: |
| failure | 6 | 2 | 2 | 0 |
| success-control | 15 | 15 | 15 | 0 |
| random-control | 15 | 13 | 15 | +2 |

对两个精确病例，新增只读证据为：

| 原branch ID | CONTINUE | K2 | 成功正K集合 | 既有passive诊断 |
| --- | ---: | ---: | --- | --- |
| `R19-random-control-8ec4fc037229710f8f13` | 1 | 0 | 仅K1；10000 | UNSUPPORTED；全j UNKNOWN；selected_k=5，cap5 |
| `R19-random-control-bf448be94724da4562c0` | 1 | 0 | 仅K5；00001 | UNSUPPORTED；全j UNKNOWN；selected_k=5，cap5 |

两例诊断的reason均为 `unsupported_or_ambiguous_subgoal`，status均为 `COVERAGE_ONLY`，`estimated_success`和`estimated_logical_cost`均为null。虽然 `branch_mapping_exact=true`，仍受“不支持或不精确则coverage-only”的原守卫限制。

因此：

- 在本次已测配对分支内，这两例是K2相对CONTINUE的损失，可以由不同正K避免；不是相对CONTINUE新增的救回。不把这种观察升级成已证明的总体期望因果效应。
- 对真实失败恢复，目前未观察到oracle-over-K2 headroom；failure n6很小，不能写成“已证明不存在”。
- random-control的身份是描述性抽样标签，不是handoff前合法feature；两个task ID、最终成功集合、source未来outcome也不能成为策略查表或训练标签。不能事后改为“只对random-control自适应”。
- 7/7仅是另7个supported/exact-mapped病例的条件性诊断结果，不能覆盖这两个unsupported病例或其余29例，更不能推出有效完整策略。

## 4. 因果可识别性裁决：哪些已被反证，哪些仍未知

冻结规则D5只有一种：每个已执行恢复动作j≥1后，若当前公共证据判SATISFIED则交还；UNKNOWN/NOT_SATISFIED继续到cap5，或遇原terminal/validity stop。unsupported原样UNKNOWN。没有K1/K2/CONTINUE fallback，没有增加predicate、正则、阈值、模型判断或“no progress”规则。

在 `src/recovery/r19_duration.py` 的已读定义中：不识别的subgoal直接返回UNKNOWN；原 `offline_public_stopping_estimate` 在 `not supported or not branch_mapping_exact` 时返回COVERAGE_ONLY及null outcome/cost。源码与Sol提供的两例原记录形成以下纸上反证链，不需重跑任何函数：

1. 第一例理想正K时点必须是K1；原detector在j1仍UNKNOWN，没有提前handoff，既有记录选择cap5。**原冻结detector没有产生捕获该例所需的K1决定。**
2. 第二例唯一成功正K为K5；原记录选择5仅因unsupported兜底，而非识别到了一个支持“应等到5”的公共predicate。选择恰好一致不等于预测能力。
3. 两例的诊断状态完全不给出所需的相反时机区分。因而“冻结detector已经具备实现这两例oracle增益的信号”不能成立。
4. 不把第一例的K5 outcome、第二例的K5 outcome，或29个unsupported的K5结果填入新D5 policy成绩。这里裁决的是**已有决定与理想决定的机制不匹配**；原policy估计仍null。

| 假说/命题 | 当前裁决 |
| --- | --- |
| 已测正K时长存在非单调、病例相关的异质性 | 有既有探索性证据；不改原标签 |
| 冻结D5能利用构成全部+2的两个case实现完整oracle headroom | 原记录不支持；第一例所需K1决定缺失，第二例仅cap5对齐 |
| 7/7证明冻结D5优于CONTINUE/K2的完整政策 | 不成立，29个coverage-only未估计，且不是完整配对效果 |
| 任何handoff前公共信息都不可能区分两例 | **NOT_PROVEN**；本轮没有也不进行feature搜索来回答 |
| failure人群不存在headroom | **NOT_PROVEN**，n6不能支持不存在结论 |
| D5在整个36cohort的政策成功率/成本 | **NOT_ESTIMATED**；不补29例，不由决定记录冒充新policy evaluation |
| 新predicate或新fallback可改善结果 | 新假说；需要独立提案，不是本轮审计通过后的实施细节 |

V1/V2的条件性 `24+7≤31` 上界仍只是带等同性前提的纸上界，不是测得成绩；当前不需要先补全这个界的逐病例前提才能决定不做live。两例原诊断已足够收紧当前动机，不能为了“证明31”再发起一次隐藏的政策重算。

## 5. 下一阶段最小工作：零推理收尾审计，不是live门票

建议只保留一轮有上限的因果可识别性审计之设计/审查及收尾文件；任何超出当前design-only范围的资料审计实施仍须明确授权。最多沿用先前8person-hours上限，不再增加研究预算。新generations=0、环境操作=0、外部费用=0；不跑analyzer/validator/detector/replay/统计流水线。

收尾文件需要：

1. **来源卡：** 为上述2/2病例引用原branch ID、原件SHA、CONTINUE与各K的既有字段、完整passive诊断字段；区分Sol原始复核与开发方纸上裁决。不生成新policy outcome或分层汇总。
2. **时点卡：** 只引用原始subgoal和既有诊断的≤j公共转移ID/状态证据，核对其确为UNSUPPORTED→UNKNOWN→cap5的原逻辑。来源缺口保留未闭合，不调用模型补语义，不重新执行规则。
3. **比较卡：** 保留CONTINUE/K1/冻结K2；明确这两例是避免恢复引入损失，而不是新rescue。不得只拿弱K1 baseline支持未来adaptive效能。
4. **范围卡：** 既有36/7/29的分母、failure6的限制、缺pick-two、control富集、同样本K2与oracle选择以及单次suffix变异未量化，全部保留；不能把“不显著”当等效。
5. **停止备忘录：** 独立review确认材料/逻辑是否闭合，给出“保持NO_GO”或具体证据争议。材料审计通过最多表示收尾解释完整，**不自动触发live授权**。

现有信息已支持第3、4项的文字结论和第2项的源码层反证。剩余工作应由Sol整合既有raw引用，而非重新构造36例策略表。若需新字段计算、规则重评或修改null结果才能继续，应记录需求并停止，不能以零LLM调用为理由默认放行。

### 数值验收与停止线

| 收尾要求 | 门槛 | 不满足时 |
| --- | --- | --- |
| 两个headroom病例的身份及证据引用 | 2/2；原SHA、字段来源、Sol复核归属明确 | 标明争议，停止升级结论，不补跑 |
| causal来源 | 使用的证据100%≤相应checkpoint；0未来outcome/stratum/task-ID查表用于decision | 停止，报告可识别性缺口，不调rule |
| null与分母完整性 | 29/29 coverage-only保持未估计；7/7只保留原条件性解释；0新增policy成绩 | 不能交付为合格收尾说明 |
| 科研新增成本和行为变更 | 0 generations、0 env ops、0规则/代码修改、0新训练/搜索/实验 | 越界则立即停止，不以结果好坏辩护 |
| 工作上限 | 最多原建议8person-hours，不追加source或计算 | 交未闭合项并结束 |
| 审计后live状态 | 始终维持NO_GO，除非未来完整新提案另获审查和人类授权 | 不存在自动进入B的闸门 |

这不是用“未证明有效”断言无效，而是要求资金与执行门槛跟随当前证据；目前没有需要新科学调用才能合理完成的下一步。

## 6. 如果将来提出新predicate/fallback，必须另立提案

本轮不设计、列举、实现或挑选候选新rule。若冻结规则不能完成研究目标，不能通过把UNKNOWN改为K1/K2、扩语言支持或更换cap，直接满足本轮门槛。这些变化定义新的处理策略。

未来新提案至少要独立说明以下条件，不能把它们视为本轮已批准：

- 新机制动机与因果可用特征必须先于新资料结果冻结；不能针对两个已知ID或random-control标签制作规则。旧36例只能是已知development证据。
- 必须保留CONTINUE、K1与冻结K2。收益目标需相对CONTINUE/K2成立；若只减少某种正K造成的损伤，应如实称避免干预损伤，不能称超越原actor的rescue。
- 任务source/排除清单、family/stratum与顺序、no-backfill/no-quota-transfer及硬预算都要事先冻结；身份新鲜不能靠换seed伪造。不增加held-out、不训练selector，不沿用已消费clearance。
- 单次recovery、原50-action horizon、共同path、checkpoint前决策、terminal/invalid/no-op和alias独立成本语义必须明确。后续比较路径不得回写已冻结的早期handoff。
- 真实research支出与logical deployment成本分开；CONTINUE与正K比较不能漏Stage1、invalid generation、reset/replay，也不能让K1承担未来path成本。detector零LLM调用不等于整套恢复策略零成本。
- 原R19例外仅passive诊断。把新停止器变成实际治疗，需要新的范围、协议与实现精确SHA独立审查；learned recovery selector禁令仍在，任何例外另行请求，本提案没有申请。

**当前不为这些未来工作承诺N、live feasibility或非零资金。** V1/V2的小试数字不应被复用为待启动计划。仅有真实新提案和新的明确授权，才重新讨论是否值得做。

## 7. 为什么停止不等于放弃科研结论

可以写实保留的贡献是：在冻结agent/共同恢复路径下，固定恢复时长结果非单调；总体固定K2未净胜CONTINUE且逻辑tokens更高；正K oracle的全部额外2例来源已明确，是两个本来CONTINUE成功的random-control病例；原detector对其均unsupported，不能把oracle headroom等同于可用控制器。

效能仍不由小N或oracle选优确认。对一个事前固定的未来策略，即使2赢0输，双侧exact p也为0.5；这个纸上例示不是给当前oracle计算policy p。未来若另立研究，power仍取决于discordance、目标效应、错误率与成本约束；不能为了实现5.56pp而任意选小N、不断增样或调规则。

单次suffix的非确定性、control富集、failure n6与缺失family都限制外推；新增记录并未消除这些限制。它们也不要求现在用更多推理“修复”一个科学负结果。

## 8. 本版交付边界

当前实际新增科学预算为0；累计5142 generations / 7949 environment operations（含历史177/342）保持不变。未执行任何新replay/analyzer/validator、统计流水线、policy评估、模型/环境/G3/G4、训练/搜索/调参；未改科学代码、原报告/null字段、原始branch、旧review/clearance或冻结引用。

本修订仅写新的/tmp设计文件，保留V1/V2字节，没有派其他线程或Luna，没有修改共享INDEX/rootinventory或其他agent文件。Sol继续独立审查和最终整合；开发方不宣称review PASS。

**最终结论：停止把5.56pp作为立即live可行性动机。完成原唯一诊断的零新增推理可识别性收尾设计/审查，保持NO_GO。若需要新predicate/fallback才能前进，另立新提案，而不是让本轮审计成为进入实验的自动门票。**
