# R19 最小离线阶段：可执行性与证据覆盖审计

版本：V4，2026-10-25 UTC。状态：**DESIGN_FROZEN_FOR_SOL_REVIEW**；不是审查PASS或执行授权。V4是当前提交，V1–V3保留为历史草案。

## 1. 决定与问题边界

**默认NO_GO新live、live feasibility、扩样、learned selector、停止规则训练/搜索/调参。仅建议另授权一轮固定36例、最多4人时、0模型推理/0环境调用的可执行性与证据覆盖审计。** 本轮只设计和读审，没有实施该36例审计或启动任何流水线。

审计问题是：原唯一公共停止规则的决定是否能由当时可见信息按冻结合同产生；已接受证据覆盖了什么、遗漏了什么；全队列的损失风险和相对CONTINUE的价值主张有哪些已证与未证依据。它不是一次能够识别总体因果效应、验证新policy或确认5.56pp的回顾性实验。

固定36、4人时及0调用是**资源/范围上限，不是效能样本量**。原V1/V2中的小试N、非零资源包和trigger投资线不再作为当前建议，不因本审计完整而恢复。没有自动通向live的下一闸门。

## 2. 冻结身份与输入归属

原analyzer `85cbb92395e5e2420c2adeb1fa0634653e742910`；executedG3 `2da980f631badc25086d12db60d128ff507d3ae6`，run `260422ac02bd42a8b2929d7ef240526b`。本轮未改两者、原数据、旧review/clearance或共享索引。

前文已只读核验的正式输入：

| 输入 | SHA256 |
| --- | --- |
| summary.json | `6ff56b7e9bc31c29bc9afd0c3ceea43c4fdf53b2addb29d3ce9f2c5e99b5d3c4` |
| R19_OPPORTUNITY_REPORT.md | `92c066ad1c9c7f187430db82ad6285800e4f31005a1fd2933231d30d695df4bc` |
| independent_G4_acceptance.json | `7331b865778481ab4e1b10943eac0e4090ea004e214dbdfff283cfbe042833e6` |
| R19_PROTOCOL.md | `7668d7fa5422ad6ad7d3affc72b2e573ec19aae53314198fc14b46dc74c9a3d9` |
| machine protocol | `3d7d1865c807d12276a8109b06c55da4e9182df0ca05a0b5463f8128dd03e122` |

正式报告目录：`/home/lizening/research-notes/agent-logs/2026-10-23T043602Z__LUNA__r19-g4-readiness__85cbb923/future_g4_report/`。

独立验收目录：`/home/lizening/research-notes/agent-logs/2026-10-25T040304Z__SOL__r19-g4-independent-result-review__85cbb923_dffaf4/`。

Sol提供的原branch复核来源：`/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z/branches.jsonl`，指定SHA `eff9b5e74d3d5daa928cb662dcc59fc3f434f66796b673679d40b374f3c8636f`。本文归属为**Sol已核验的原字段**，不冒充开发方重新执行raw校验/统计。

另只读参考了尚在整合的Sol复盘草稿 `/home/lizening/research-notes/agent-logs/2026-10-25T043056Z__SOL__r19-scientific-retrospective-design__96b57f/SCIENTIFIC_RETROSPECTIVE.md`，读取时SHA `2e4451e5152bc0eb92db2455098be7b090653c264e70895e62d6f4e94ffd23a9`。这是所读草稿快照，不宣称它已经冻结或赋予本设计独立验收。

## 3. 科学复盘：不把oracle当policy

**OBSERVED，引用既有结果：** N36=6 failure+15 success-control+15 random-control；39attempts/127sources/183K arms。K1..5成功29/30/28/25/24，CONTINUE30。K2对K1为2赢1输，Holm p=1；其他注册比较Holm p≥0.5。CONTINUE/K2平均full-branch logical tokens为7470.2/9854.25，K2高31.9%。没有固定更长恢复的可靠净优势；不显著也不等于等效。

正K oracle32相对最佳固定正K30多出的两例全部在random-control：failure oracle=K2=2/6，success-control=15/15，random-control oracle15/K2 13。failure上未观察到oracle-over-K2 headroom，**n6不能证明不存在**。control富集、缺pick-two和队列耗尽均保留，不补样或外推部署总体。

| 原prefix后缀 | 正K成功模式 | CONTINUE | K2 | 既有public诊断 |
| --- | --- | ---: | ---: | --- |
| 8ec4fc037229710f8f13 | 10000，仅K1 | 1 | 0 | UNSUPPORTED；全j UNKNOWN；selected_k5/cap5 |
| bf448be94724da4562c0 | 00001，仅K5 | 1 | 0 | UNSUPPORTED；全j UNKNOWN；selected_k5/cap5 |

两例均为 `COVERAGE_ONLY`，reason为 `unsupported_or_ambiguous_subgoal`，estimated_success/cost为null，虽有branch_mapping_exact=true也不能绕过unsupported守卫。它们是可避免的K2干预损失，不是相对CONTINUE的新增rescue。

但这**不否定任何自适应组合的价值**：K2在别处已有2个rescue并在这两例有2个harm；若未来事前可执行的规则能保留救回而避免伤害，可能优于CONTINUE。现在缺的是可用时点信息、全队列可靠比较和成本依据，不是“必须达到oracle32”的理论要求。

原detector对两例没有区分信号：它不能为第一例产生所需K1决定；第二例cap5只是fallback对齐。由此不能声称原detector已经利用了这2例headroom。其他公共信息能否区分仍**NOT_PROVEN**，本轮不搜索或拟合。

竞争解释包括同样本选择K2/oracle、少数特定case、control富集、subgoal支持只覆盖容易病例、handoff状态/历史改变后actor行为差异，以及未量化的单次suffix变异。不能把其中任何一个未经证据地宣布为已识别机制或随机噪声。

## 4. 审计对象只允许原D5

每个已执行恢复动作j≥1后，仅以原subgoal及≤j公共动作/观测判断当前SATISFIED；SATISFIED交还，否则UNKNOWN/NOT_SATISFIED继续至cap5或原强制停止。unsupported不改fallback。terminal无SFT交还；非terminal invalid可按原语义交还，无repair/retry。no-op、invalid generation debit、50-action horizon和剩余SFT预算均沿用原定义。

时点证据包含transition IDs和可见边界；不能用source未来成败、stratum、任务ID查表、未来reward、别K suffix或oracle K。当前j之前的撤销转移可改变current truth；已冻结的早期handoff不受后来comparator路径动作回写。

“信息可在j获得”不等于“原运行曾在j在线执行停止”。原记录是passive/offline诊断，即使其输入切片只含≤j，也不能把该记录升级为在线decision的墙钟时点凭据或实际部署过的handoff。审计只能核对接口和信息边界。

本审计不调用detector重新生成decisions，不执行policy replay，不重跑analyzer/validator或统计流水线；只审阅已经产生的记录、字段来源、原定义和已有比较。发现需要新运算、额外记录、predicate或fallback才能回答，就登记缺口，不现场补做。

7个supported/exact-mapped的原条件性结果与29个coverage-only分开。`branch_mapping_exact=true`说明的一种身份匹配不能代替predicate支持，两道条件不可合并。unsupported可以是重要的研究发现，不必被伪装成应修复的数据错误。

## 5. 最小离线阶段及交付物

**范围固定为原36个eligible，覆盖全部10个非恒定模式与29个unsupported；不只看两例winner，也不丢弃26个恒定模式。** 39attempts/127sources仅作既有分母和取样限制的引用，不重新入组或重建source轨迹。没有新增N、替换、补样、规则选择或data实验。

本轮只冻结以下产物的设计；不是声称表已填写或审计已执行：

| 拟议产物 | 最小内容 | 明确不做 |
| --- | --- | --- |
| 输入与范围清单 | 已接受报告/原branch/原诊断及协议的身份、SHA、36个canonical case引用、分母限制、来源归属 | 不创建新队列、改原清单或重新验证运行 |
| 36例证据登记册 | 每例原记录引用、原subgoal/predicate/support状态、原selected_k/reason、可见时点/transition引用、原exact-map或coverage-only状态、缺口说明 | 不生成新D5 outcome/cost；不为29例补K5结果 |
| 可执行性注记 | 原决定用到了什么公共信息、何时可见、terminal/invalid/horizon/alias语义、当前真值证据 | 不根据后续结果修改早期决定，不新增parser或rule |
| 覆盖/损失与比较注记 | 全队列中已有证据支持什么；10个非恒定模式、29个unsupported的去向；CONTINUE/K1/冻结K2比较是否有可引用的原结果/成本 | 不把原正K损失直接当成未估计D5的损失；不把7/7当完整policy优势 |
| 收尾与资源决定备忘录 | 哪些原合同可追溯，哪些证据不足；相对CONTINUE的价值主张有哪些依据/缺口；保持NO_GO或要求完整新提案的具体理由 | 不发live许可，不把审计完整性当效能证明 |

证据登记册字段模板：

`case_ref | original_diagnostic_ref | subgoal/predicate/support | existing_selected_k/reason | cutoff_j/public_transition_refs | existing_mapping_status | original_comparator_refs_CONTINUE_K1_K2 | original_cost_refs | gap_or_risk | attribution`。

其中comparator/cost字段是**引用原已产生的值或比较**，不是给新策略拼装成绩表；缺失就NA。对已有7个映射病例也须问：是否只是CONTINUE本来成功，是否只相对弱基准省成本，是否有完整branch成本；不据7个有利终点排除其他损失风险。未估计的队列部分使完整价值主张不能成立时，应明确承认，而不是填补它。

全队列harms审视不意味着能够给29个未知policy结果贴上harm/no-harm标签；未知风险必须保留，不能以“未估计”报告“没有伤害”。

两例已知病例用于检查解释是否忠实，**不要求新规则找回2/2，也不要求任何规则达到oracle32**。它们必须出现在固定36例覆盖中只是文档完整性要求。一个只实现部分headroom、或以成功保持换取成本降低的候选也可能有价值，但必须有相对CONTINUE的真实可证依据；本轮没有这种新候选或新效能证明。

## 6. 可验收标准：资料完整性不是效果确认

| 项目 | 数值/判定标准 | 达不到时 |
| --- | --- | --- |
| 固定对象 | 36/36登记去向；已有10个非恒定模式和29个unsupported均纳入；不选择性删行 | 报AUDIT_INCOMPLETE，时间到即停止 |
| 既有字段与缺口 | 已用字段100%有原记录引用/来源归属；缺失明确NA；0个未经支持的新policy值 | 记录缺口，不现场计算或补跑 |
| 时点合同 | 已用decision证据100%≤j；0条future reward/outcome/stratum/task-ID查表用于decision | 报可执行性问题，停止候选升级，不调rule |
| unsupported守卫 | 29/29保留coverage-only的未估计语义；7/7仅原条件性解释 | 不接受该审计说明，禁止插补 |
| 比较完整性 | CONTINUE作为主实用基准；K1与冻结K2均保留原证据引用或缺口；0次只用有利子集/弱baseline替代 | 价值证据不足，保持NO_GO |
| 资源/范围 | ≤4 person-hours，固定36，0 generation、0 env operation、0新策略重评/训练/搜索/统计流水线 | 到上限交未闭合项并结束，不扩张 |

建议4人时由工程2小时、Sol独立审阅2小时组成；这是未执行的资源上限，不保证所有证据在4小时内可闭合。允许交付“完整记录了不可判断”的审计，不以得到正面候选为成功标准。

审计可验收的意思是引用、时点、coverage、限制和停止决定可被独立读审。**不要求任意数量trigger、净赢、特定成功率、2/2 oracle救回、p值或N达到power。** V1/V2中的3trigger/2family、净赢与成本百分比不再用作本阶段验收线。

允许的阶段结果是：

- `AUDIT_DOCUMENTATION_COMPLETE / LIVE_NO_GO`：原证据及缺口解释完整，仍没有新live授权。
- `AUDIT_INCOMPLETE / LIVE_NO_GO`：时间或证据不足，不补样、不延时凑完整。
- `CURRENT_CANDIDATE_STOP`：需要未来信息、针对旧样本扩predicate、改变fallback、删UNKNOWN或换弱基准才能声称价值；关闭当前候选的升级请求。

若既有证据出现部分真实价值线索，只能写明其来源、范围与缺口，请求独立新提案；不通过本阶段自动放行live。审计不会识别总体因果效应，也不会把未评估策略变成已验证策略。

## 7. 纸上上界与统计解释的使用限制

若保留 `24+7=31`，必须同时列条件：29个unsupported上的原D5须在原terminal/invalid debit、公共状态/历史及suffix结果身份上严格等同其K5，且最多只在7个supported病例改变K5结果。detector CPU另计，mapping flag本身不证明所有前提。在这些假设下成功数至多31；**不是测得D5=31/36，也不是全体policy评估或总体上界**。

达不到oracle32本身不足以否决策略。一个低于oracle但能在实际可用信息下改善CONTINUE或以可证非劣成功降低成本的策略仍可能值得研究。当前NO_GO依据是早期可用信号与全队列增量价值尚无可靠证据、coverage严重不足和当前成本基准强，而不是要求捕获完整oracle。审计也无须为证明这个宽上界重算29例。

2个paired wins、0 losses对一个事前固定的假想策略，双侧exact p为0.5，只作纸上例示，不给事后oracle计算有效policy p。固定36与4人时更不是为确认5.56pp设置的效能样本量；不承诺一个任意小live N，不用不显著声称等效/非劣。

## 8. 后续约束与明确停止

新predicate、新fallback、cap、特征或live controller都属于新处理策略。当前不列候选rule、不开发选择器，也不把已暴露R19数据称作held-out。任何新提案必须在新资料之前选择研究主张（提高成功或降低成本）、因果可用特征和唯一冻结规则，保留CONTINUE/K1/冻结K2，并独立设计source、完整配对风险/成本、统计精度和硬预算。不能把本审计验收当作这些要件已具备。

learned recovery selector、训练、DPO/ORPO、memory、额外环境/模型、held-out等禁令不变。原“passive offline”例外不能自动扩展为live treatment；旧G2/G3/G4和clearance不能复用或重跑。任何未来science仍需新的具体提案、精确实现/协议审查及明确人类授权。

**当前资金与科学预算：0新generations、0环境操作、0外部API/云算力支出。** 累计5142/7949（含reset，包含历史177/342）不变；逻辑policy tokens与物理科研开销不混用。4人时只是拟议离线审计人力上限。

本轮只读正式文件/协议/相关源码及Sol复盘草稿、作纸上论证、写新的/tmp文档；没有实施36例审计、重算policy、调用analyzer/validators/统计流水线/模型/环境、训练搜索或新线程派遣。共享INDEX/rootinventory、原数据/代码/review/clearance未改；最终发布由Sol统一协调。

**交付决定：冻结这个最小离线设计供Sol读审。保持LIVE_NO_GO；不强行承诺live pilot或效能样本量，不要求达到oracle或救回2/2。**
