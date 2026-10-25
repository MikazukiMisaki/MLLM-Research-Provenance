# R19 最终设计与交叉审查 addendum

状态：**DESIGN_FROZEN_FOR_SOL_INTEGRATION**。本文件收尾本轮设计与交叉读审，不是科学执行PASS、审计实施许可或live release。旧V1/V2/V3及已冻结V4原样保留。

## 1. 交叉读审对象与结论

已只读审看整合草案：

`/home/lizening/research-notes/agent-logs/2026-10-25T043056Z__SOL__r19-scientific-retrospective-design__96b57f/MINIMAL_NEXT_STAGE_DESIGN.md`

读取时SHA256：`d5408fa5f2543481bd6f4e25ed78d98da3933a1a1d9372f58f8bd84db5ff3741`。该hash标识本次读审的草稿快照；协调方最终整合冻结可产生不同hash，本文件不替其宣告最终验收。

**未发现会改变“仅阶段A、live NO_GO”决定的实质性事实或统计错误。** 草案正确保留了原唯一规则、完整36例、7/29覆盖边界、CONTINUE/K1/冻结K2及4人时总上限；没有把小样本或oracle选优包装为效能确认。

记录一条影响执行范围的解释约束：验收表“全部36例分母、成功和伤害、对照与成本齐全”，必须按以下含义理解，而不能要求补齐未估计的D5政策结果：

> 36/36证据去向完整；已测正K/CONTINUE以及原7个supported映射记录的既有outcome/cost有完整引用；29个coverage-only的D5结果与成本保持NA/null。未覆盖的harms/价值明确为未知，不新增完整D5汇总或统计。

这与草案步骤6的守卫一致，不是发现原数据错误，也不要求另开一轮设计。其“不确定性分析/整体收益”在阶段A只能指已有证据范围、未知风险与价值主张的缺口说明，不能升级为新policy evaluation、统计流水线或总体因果效应证明。可将这条限定直接并入最终整合文字或与本addendum一起发布。

## 2. 最终保留的最小方案：阶段A

名称统一为 **可执行性与证据覆盖审计**。问题是原冻结D5能否以checkpoint时点可用公共信息产生可追溯决定，以及已接受的measured suffix证据支持哪些比较；不研究初始“何时介入”，不寻找最优停止规则。

资源提议仅为：**一轮、原固定36个eligible、总计最多4人时（工程与审阅合计）、0新model generations、0environment operations、0外部费用。** 这是范围/资源上限，不是power或效能样本量。当前只是设计，尚未实施该36例审计。

输入只限原run260422ac02bd42a8b2929d7ef240526b及已正式验收的G4；analyzer85cbb92395e5e2420c2adeb1fa0634653e742910、executedG3 2da980f631badc25086d12db60d128ff507d3ae6保持冻结。保留6/15/15、39attempts、127source的既有说明；不得换任务、补样、改quota或重跑source。

唯一规则仍为：每次已执行恢复动作j≥1之后，原subgoal与≤j公共动作/观测判SATISFIED则交还，否则NOT_SATISFIED/UNKNOWN继续至cap5或原terminal/invalid stop。不改fallback为K1/K2、不改predicate/prompt/decoder/horizon。terminal没有SFT handoff；invalid/no-op/generation debit与alias各政策成本沿原语义。原offline诊断的≤j输入不等于已经在墙钟j在线执行过停止。

最小产物与验收：

| 产物 | 可验收要求 | 停止线 |
| --- | --- | --- |
| 固定范围/输入清单 | 原身份、路径、hash及来源归属明确；36/36有去向，含全部10非恒定模式和29unsupported | 漂移/来源争议则停止，不修原件 |
| 原诊断证据登记 | 原predicate/support、selectedK/reason、时点/transition引用、mapping/缺口；已用字段100%有既有来源 | 缺失标NOT_PROVEN/NA，不重新执行detector或生成missing suffix |
| 时点/语义说明 | 0未来观察、reward、source结果、stratum/task-ID查表、oracle K进入decision；current truth和强制停止语义不变 | 发现泄漏或需调rule才能通过则停止候选升级 |
| 覆盖、harms与对照说明 | CONTINUE为首要实用基准，保留K1/冻结K2；原7例只作条件性结果，29例保持未估计；未知风险不当作无伤害 | 不得仅解释赢家、只赢弱基线或插补全队列政策效果 |
| 收尾备忘录 | 明确已有/缺失证据及相对CONTINUE的可证价值边界；可以完整记录“不能判断” | 4人时到即交未闭合项；不扩样、重试或换rule |

成功/成本字段只能引用已有记录和原比较，不能为填表拼装新的完整policy成绩。审计的完整性可被验收，**效果不因此得到确认**。没有trigger数量、成功率、净赢、p值、达到oracle32或找回两例的验收门槛。

## 3. 反证边界与价值判断

Sol已哈希核对的原branch（SHA256 `eff9b5e74d3d5daa928cb662dcc59fc3f434f66796b673679d40b374f3c8636f`）显示：两个oracle-over-K2病例8ec4fc037229710f8f13与bf448be94724da4562c0均CONTINUE成功、K2失败；正K成功集合分别仅K1、仅K5。两者原诊断均UNSUPPORTED、全j UNKNOWN、cap5、COVERAGE_ONLY，estimated_success/cost=null。branch_mapping_exact=true不解除unsupported守卫。

这些是**Sol给定并核验的原字段**，本文不宣称开发方重跑了raw校验、统计或策略。两例说明部分K2损失可由不同handoff避免，不是这两例相对CONTINUE的新rescue。全部+2来自random-control；failure oracle=K2=2/6，不能由n6推出总体不存在headroom。

原detector没有为两例提供相反时机的区分信号，其他公共信息是否足以区分仍NOT_PROVEN。不能把task ID、random-control标签或未来结果变成选择标签，也不能从另外7个mapped成功推断完整策略有效。

同时不否定所有自适应组合：保留其他病例的K2 rescue并避免其harms，或以可证成功保持换取成本降低，都可能有实用价值。关键是事前可用信息、完整coverage/损失风险与CONTINUE比较，而非必须取得全部oracle headroom。低于oracle的策略不自动无价值。

如果引用24+7=31，只可作为**带明示前提的纸上宽上界**：29unsupported上的D5必须严格等同对应K5的原强制停止、状态/历史、suffix结果身份及请求debit，且最多在7supported上改变结果；detector CPU另计。该前提不能仅由mapping flag代替。31不是运行过的policy成绩或总体上界，达不到32也不是否决策略的充分条件；本阶段不为证明它而重算29例。

## 4. 明确不纳入当前方案

阶段B、12sources、3000generations/5000operations、12GPU小时、10%cost premium，以及旧trigger/family投资门槛，**均为未接受备选草案，不纳入当前最小方案，永不因阶段A完整而自动恢复**。不再扩写更大试验，不承诺任意小N确认5.56pp。

新predicate/fallback、live controller或任何learned selector是新提案，不是原审计的修补。未来若另议，须先选定成功提升还是保成功省成本、明确伤害/成本容忍、独立可用TRAIN身份与统计精度、固定规则/实现/预算并取得新授权；本轮不替它填N或放行。held-out、训练/搜索/调参及已消费clearance的边界不变。

**当前状态：阶段A设计可供独立整合；阶段A实施尚未授权/未开始；新推理与live保持NO_GO。** 审计可能给出解释性负结果或NOT_PROVEN，不承诺带来下一轮live。

## 5. 冻结交付与实际操作

本addendum与配套RECORD保存在既有/tmp目录供Sol统一复制原字节发布。已冻结V4完整设计仍可作详细附件，SHA256 `d8cf5966d17051a02ec6ecafd0d4f462ae354ccbc79c2f75ee023c1b5ed314e4`；其4人时、固定36和无自动live的范围与此一致。旧V1/V2不改；它们的未接受试验数字不能作为当前建议引用。

本次只读整合草案并写addendum/RECORD/校验元数据；没有实施审计、运行分析/策略/analyzer/validator/model/environment/G3/G4、训练搜索或派agent。无科学代码、原证据、旧review/clearance、共享INDEX/rootinventory或其他agent文件修改。累计科学成本保持5142/7949（含历史177/342）。

交叉读审意见到此收尾；不请求循环修订，不宣称独立PASS或新执行许可。后续由Sol完成整合、冻结和发布收据。
