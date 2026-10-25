# 一轮自身经验采纳 SFT 草案

**DRAFT_NOT_EXECUTABLE — SCIENTIFIC_PERMISSION=NOT_GRANTED**

本文件只有方法设计。当前允许资源是SI-P0首轮总2人时、0模型/环境/训练调用；不是此前36例detector审计的启动。没有批准训练集、N、科学预算、超参数搜索、可执行命令或自动后续。R19 85/2da、所有旧证据/review/clearance及5142/7949账本不变。

## 1. 唯一问题与一轮上限

候选问题：冻结强SFT-P0以后，在同一生成来源和训练预算下，额外要求“同一原前缀CONTINUE失败、纠错成功”的经验采纳条件，能否比普通绝对成功筛选更有利于新任务表现？这是待否证假设，非已命名成功方法。

仅一轮：固定经验来源 → 固定离线采纳 → 两个独立子adapter更新 → 一次预先冻结评估 → 结束。A始终是原SFT-P0；B/C从A的相同冻结状态分别初始化，绝不覆盖A或原adapter。禁止第二轮、选择器训练、memory、DPO/ORPO、PPO/GRPO、额外环境或调参搜索。下一轮若有必要仍须另授权。

## 2. A/B/C及最小可解释对照

| 组 | 权重与作用 | 训练经验采纳 |
|---|---|---|
| A | 冻结SFT-P0，不更新 | 无新增自身经验；评估强基座 |
| B | 由A初始化、一次action-only SFT | 普通成功筛选：候选的实际完整任务终局成功即可；不要求相对CONTINUE有增量 |
| C | 由A初始化、与B相同更新配方 | 相同候选池与格式；纠错部分额外要求同前缀CONTINUE=0、固定纠错处理=1且证据完整 |

为避免把“多了teacher/更多生成”误称“配对标签机制”，B/C应接触**同一个预先冻结的模型生成候选池**，包括普通A成功经验和固定operator生成的纠错候选。B对纠错候选也仅按绝对终局成功筛选；C对该纠错候选再检查paired增量。两者保留完全相同的普通自身成功背景部分，背景/纠错训练token占比在未来协议中一次冻结，不按新任务结果调节。所有目标都来自模型实际输出，专家SFT轨迹不算本轮自身经验。

这仍属于普通成功筛选self-training基线，区别是它不丢弃对B公平可见的成功纠错候选。如果协调方坚持B仅可使用actor source成功、C却额外有恢复teacher，C>B最多表明整个“来源+采纳”配方优于actor-only self-training，**不能单独归因paired采纳条件**；该较弱解释必须先明示，不能事后升级机制结论。不得默默添加第四个实验臂。

C>A是超过强基座的必要证据，C>B是超过普通成功筛选的必要证据；缺任一项均不能声称所提增量采纳有效。即使二者均好，结论也仅关于该冻结采纳配方及评估分布，不是每个纠错action的因果必要性。

## 3. 来源处理与因果时点（未来协议选择，不是现在执行）

最小处理草案只用历史共有的**一次OSR-1纠错行动后立即交回A**；同一Qwen3-8B base、无actor adapter的恢复模型，原两阶段诊断/动作接口，50总环境action horizon。选择单步是为限制处理异质性、沿用可追溯旧语义，不是按R19最佳K选择。固定一次纠错，绝不借本草案复用R19的五步例外、挑最佳K、合并PAR/FACT/CARD、优化停止规则或训练在线router。

将来若希望K2或其他输入处理，必须重新冻结一个单独处理和理由；R19 K2两例在本次inventory中是既有证据引用，不自动加入此单步训练池。历史未知weights revision保留UNKNOWN；未来生产必须有当时真实模型/adapter/tokenizer身份。历史身份不全的分区先隔离，是否接受其有限来源证据需明确审阅，不能倒填。

所有学习输入都位于本次动作**之前**：原task goal、当前公共observation、已发生的最近4条transition、当前admissible map和排序。样本ID、队列标签、最终reward、CONTINUE/recover终局、未来动作结果、oracle、环境hiddenfacts/专家计划均不进入学生输入。已观察终局可以用于离线数据采纳，不能作为部署时可用特征。

训练目标仅拟议采用已执行、合法且可追溯的**第一纠错动作**，与普通成功动作一样使用原SFT-P0 Action-ID输出接口。不训练诊断、subgoal、card或rationale；不让恢复模型重写一个新目标；不把某时点A003搬到另一时点。必须用原raw output、当时map、选中command和transition形成一条证据链。action来自看过模型生成subgoal的恢复teacher，学生投影只保留公共P0接口；这是一项需要逐条证明的蒸馏投影，不是本轮已经构建的数据。target格式化也须有原始ID映射证据，不可制造正确动作。

只允许任务终局done且positive reward作success；局部subgoal满足不代替它。Stage1 invalid时历史仍请求一次Stage2但不执行action；目标不采纳。Stage2 malformed/truncated/unmappable不修复、不重试；terminal立即结束，执行no-op照扣action，不执行的parser失败不扣环境action。CONTINUE和纠错都保留同一原剩余额度；不能用重置horizon制造正增量。中断unit隔离，不充当负例或正例。

## 4. 身份与样本选择冻结

先定已消费历史身份全集和未来合法TRAIN来源manifest；按canonical game/trial排除所有开发、SFT train/validation/online保留、旧审计和已消耗/保留确认身份。只读元数据检查不等于允许查看或使用未消费outcomes。未来评估只能在单独授权且与所有训练/生成身份无交叉的新TRAIN任务上；它不因此成为held-out正式结论。valid_seen/valid_unseen与其他held-out禁令保持，改动需新授权。

一个canonical task的所有episode/prefix/treatment/K alias必须同属一个数据分区。不能用seed、时间戳或不同prefix绕过身份隔离。拟议最小主池每task最多一个anchor，按不看终局的冻结hash/时点规则选择；actor/ref/corrector身份分别记录，不能全池混成同一个policy。相同physical suffix、复用source、报告再导出和alias只计一次经验来源。

固定source名单和完成/中断处理，不按positive数量追加采集或转移quota。不存在“采到足够救回为止”。若既有记录不足以支撑严格来源/多样性预算，停止该候选或返回NOT_READY，不能临时收集新positive。本轮不为这一草案构建任何训练JSONL、选anchor或执行新predicate。

## 5. B/C训练预算与checkpoint

未来需共同冻结非padding supervised completion tokens T、普通/纠错token比例、optimizer updates U、每次batch的loss token配额、学习率/LoRA/损失/随机种子、序列上限和checkpoint规则。当前这些科学数值**UNSET，不能执行**；不把专家SFT原来的2epochs/LR等当作已批准新配方。

B/C相同T、相同U、相同初始化和更新超参数；目标只计算action completion loss。使用相同长度/批次处理预算，报告实际input/completion/padding/processed tokens及FLOPs代理，避免“相同tokens”只算便宜的输出。序列溢出不能截掉目标或引入未来信息。若要完全匹配processed token预算，未来固定padding/packing规则也必须同一版本冻结；当前已记录token长度不能证明投影后长度。

较大池只能按预先规则下采样到共同可支持预算；不得反复过采样稀有C任务来装成数据充分。每task曝光与重复上限一次冻结，若C无法满足共同T/U和该上限，就停止或由未来审阅重新设计，不能偷偷加epoch/生成/selector。唯一checkpoint提案为两组都取预定最后一次update；不按新任务结果、训练源任务reward或多个checkpoint挑胜者。若未来另选离线validation checkpoint，需先冻结且与最终评估严格隔离，不能本轮默许搜索。

## 6. 生成、配对与总费用公平

训练token匹配不足以证明成本公平。需要两本账：

1. **实际研究账**：common source、两阶段恢复生成、所有失败/neutral/harm、paired comparator、reset、prefix/branch replay、未完成操作、训练与评估全部逐项计费；physical调用不因alias或复用而再算。common pool获取成本只发生一次，不在合计账重复，但各组来源暴露与分摊规则需一致写清。
2. **方法获取成本账**：普通成功过滤本不必支付paired验证，C需要这一额外证据。即使研究中两组共用同池，也不能隐藏C的必要验证premium，再宣称端到端预算效率优于B。报告每方法若独立获取经验所需成本和共享研究成本，分别呈现。

未来generation/environment/training/evaluation硬上限和耗尽停规须由新任务授权冻结，当前额度均未批准。没有3k/5k之类默认预算，没有把历史5142/7949当可支取余额。若要回答“同总获取预算是否优于B”，还需让B有公平的预算使用方式并另行审查；本三臂同候选池草案只隔离**给定生成池、相同训练预算下的采纳差异**，不预先声称端到端成本最优。

## 7. 评估、验收和反证

未来A/B/C都只运行同一学生接口、同一50-action horizon/greedy配置，无运行时恢复/记忆/router。评估单位为独立canonical task；多个prefix或K不是独立N。相同任务上的A/B/C形成paired终局结果，必须同时报告成功、paired wins/losses、harm、覆盖、消耗和中断；不得只报C的训练case成功。

若未来进入效能确认，预注册C−A和C−B两项paired比较、多重比较处理、效应区间、最小有意义改善及总成本/伤害容忍度；数值应由用途、预算与独立任务可用性共同论证，**本轮不编一个小N或任意效应门槛**。不能把R19 oracle 2/36、某历史rescue率或多个相关treatment当新训练增益的效应先验来承诺显著。p>0.05不是等效证明，小样本不确定也不是肯定收益。

验收分层：

- **协议可设计**：现有审计可写清来源、离线采纳、对照与反证。SI-P0达到的是这一层的候选交付，尚待协调方审阅。
- **数据/工程feasibility**：未来授权后才可证明100%纳入项有真实公共时点、map/target/transition/terminal证据；0专家/hidden/future泄漏、0跨分区canonical重叠；训练预算与checkpoint等量，C多样性和重复约束可行。任一关键缺口阻断训练。它不代表效能通过。
- **效能确认**：须在预先固定新任务与足以回答问题的样本设计上，按预注册标准同时支持C>A、C>B并满足伤害/总成本约束；否则不能声称有用的自改进采纳。此处尚无已批准样本、统计计划或通过阈值。

实质反证/停止条件：去重后纠错经验不足或只靠light个例；严格投影造成不可追溯目标；未知模型来源无法接受；新任务身份不足；C依赖过采样/更多生成或训练步数；C只赢弱对照而不赢A/B；改善只在已见源任务、训练loss下降或oracle挑选；伤害/获取费用抵消价值；或一轮结果无法区分选择配方与更强teacher。出现这些情况结束本轮候选，不自动扩大样本、换operator或开始第二轮。

## 8. 需要的新授权

协调方独立审阅这份设计之后，仍需人类明确批准：任何训练数据构建/公共输入投影或tokenizer运行；任何科学代码实现/测试；新source/paired验证/环境调用；B/C adapter训练、预算与冻结清单；任何独立任务科学评估。旧G2/G3/G4/review/clearance均不可复用为这些许可。当前learnedselector/memory/DPO/额外环境禁令维持。没有自动下一阶段。
