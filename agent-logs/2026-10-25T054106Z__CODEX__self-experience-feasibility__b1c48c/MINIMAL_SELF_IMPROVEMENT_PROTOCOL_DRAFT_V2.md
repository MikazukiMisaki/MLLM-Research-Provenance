# 一轮自身经验采纳 SFT 草案 V2 — 最终设计审查限定

**DRAFT_NOT_EXECUTABLE — SCIENTIFIC_PERMISSION=NOT_GRANTED**

**最终 DATA_FEASIBILITY=NOT_READY；QUALIFIED_TRAINING_N=NOT_ESTABLISHED；LEARNING_GAIN=NOT_PROVEN。** V1的READY_FOR_PROTOCOL_DESIGN仅表示能够写出草案，不是学习数据已就绪。本V2限制当前可读主张；原V1、inventory、所有旧收据/封存文件原字节保留。配套最终决定见 `SI_P0_FINAL_FEASIBILITY_DECISION.md`。本轮至此完成，不扩大调查或自动后续。

本文件只有方法设计。当前允许资源是SI-P0首轮总2人时、0模型/环境/训练调用；不是此前36例detector审计的启动。没有批准训练集、N、科学预算、超参数搜索、可执行命令或自动后续。R19 85/2da、所有旧证据/review/clearance及5142/7949账本不变。

## 1. 唯一问题与一轮上限

候选问题：冻结强SFT-P0以后，在同一生成来源和训练预算下，额外要求“同一原前缀CONTINUE失败、纠错成功”的经验采纳条件，能否比普通绝对成功筛选更有利于新任务表现？这是待否证假设，非已命名成功方法。

仅一轮：固定经验来源 → 固定离线采纳 → 两个独立子adapter更新 → 一次预先冻结评估 → 结束。A始终是原SFT-P0；B/C从A的相同冻结状态分别初始化，绝不覆盖A或原adapter。禁止第二轮、选择器训练、memory、DPO/ORPO、PPO/GRPO、额外环境或调参搜索。下一轮若有必要仍须另授权。

## 2. 竞争配方与机制归因的必要对照

原始配方含义需先分清：A冻结强SFT-P0；B_source只对actor普通成功自身经验做SFT；C采纳增益验证的纠错经验。**C>B_source即使出现，也不能单独证明筛选机制**，因为训练生成来源、teacher、任务难度、纠错/普通数据比例及曝光分布同时可能不同。C>A也不自动分解出这些因素。它们至多比较整个数据/更新配方。

若未来希望把问题限定为采纳条件，最小纸上主对照应将B_source**替换为B_pool**，保持三臂数量；本文其余B/C训练预算条款里的B均指B_pool。这是设计上的必要条件，当前没有构建pool、训练B_pool或获准执行任何训练臂。

| 组 | 权重/候选来源 | 采纳条件及能回答的问题 |
|---|---|---|
| A | 冻结原SFT-P0 | 不更新；回答是否超过强基座 |
| B_pool（success-only） | 与C相同的预先冻结生成候选池，恢复teacher/固定operator/学生目标格式相同 | 对候选纠错仅要求完整任务终局成功，不看相对CONTINUE增量；普通自身成功背景与C相同 |
| C | 与B_pool同池、相同初始化/格式/背景比例/更新预算 | 纠错部分另要求同前缀CONTINUE=0且纠错=1，并通过相同证据条件 |

同池指**相同采纳前候选来源及生成机会**，不表示把两组采纳后的训练行强行做成相同。来源、处理、目标粒度、student输入、背景比例、token/steps、重复上限和checkpoint须一致冻结；不能让B_pool看不到C的teacher候选，再把来源差异归因给paired筛选。处理带来的难度/家族组成变化仍须透明报告；同池success-only是必要对照，并非自动排除所有难度重加权解释。若要更强地宣称“增益标签本身优于单纯难度重采样”，尚需独立预注册且可实现的设计，当前不作该主张或扩充方案。

若协调方未来必须保留B_source，则只能将同池success-only列为**条件性D_pool的审查依赖**；缺少D_pool时禁止采纳机制归因。D_pool不是当前最小执行计划，不是已接受第四臂，亦不产生新增训练/生成额度。替换B或条件性D两种选择都须未来明确冻结，不能事后择优解释。

C>A是学习超过强基座的必要证据；C>B_source仅比较配方。只有在上述同池及更新约束成立、独立新任务评估等条件满足时，C>B_pool（或C>D_pool）才可能支持这一**冻结采纳配方**相对success-only的增量，仍不证明每条目标正确/必要、所有竞争解释排除或方法首创。当前没有任何这些已训练比较结果。

## 3. 来源处理与因果时点（未来协议选择，不是现在执行）

最小处理草案只用历史共有的**一次OSR-1纠错行动后立即交回A**；同一Qwen3-8B base、无actor adapter的恢复模型，原两阶段诊断/动作接口，50总环境action horizon。选择单步是为限制处理异质性、沿用可追溯旧语义，不是按R19最佳K选择。固定一次纠错，绝不借本草案复用R19的五步例外、挑最佳K、合并PAR/FACT/CARD、优化停止规则或训练在线router。

将来若希望K2或其他输入处理，必须重新冻结一个单独处理和理由；R19 K2两例在本次inventory中是既有证据引用，不自动加入此单步训练池。历史未知weights revision保留UNKNOWN；未来生产必须有当时真实模型/adapter/tokenizer身份。历史身份不全的分区先隔离，是否接受其有限来源证据需明确审阅，不能倒填。

所有学习输入都位于本次动作**之前**：原task goal、当前公共observation、已发生的最近4条transition、当前admissible map和排序。样本ID、队列标签、最终reward、CONTINUE/recover终局、未来动作结果、oracle、环境hiddenfacts/专家计划均不进入学生输入。已观察终局可以用于离线数据采纳，不能作为部署时可用特征。

训练目标仅拟议采用已执行、合法且可追溯的**第一纠错动作**，使用原SFT-P0 Action-ID输出接口。恢复teacher是adapter-off base；它看过原时点的diagnosis/subgoal，某些历史处理还看过card。**这些原始恢复prompt及subgoal/card不能直接移植给P0**。P0只能使用动作前的原公共goal/observation/H4/map；对目标的投影是否可追溯、是否丢失了必要区分信息尚未证明，不能当已经合格的训练行。不训练rationale，不让teacher重写新目标，不跨时点搬用Axxx；需原raw ID、当时map、选中command及transition绑定。

必须分别记来源：①adapter-off恢复action目标；②恢复后由adapter-on冻结SFT-P0生成的suffix动作。后者发生在改变后的checkpoint，有自己的输入/map/时间，不是adapter-off标签，不是新增独立task，也不能把原prefix的0→1沿时间复制成每个suffix action的“已验证正增益”。本最小草案没有自动采纳suffix作为额外C监督；未来若要使用，需要另行固定其来源比例与同池对照，当前仍只是分开的候选证据索引。主草案不混入PAR/FACT/CARD处理。

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

若未来进入效能确认，预注册C−A和C−B_pool两项paired比较、多重比较处理、效应区间、最小有意义改善及总成本/伤害容忍度；数值应由用途、预算与独立任务可用性共同论证，**本轮不编一个小N或任意效应门槛**。不能把R19 oracle 2/36、某历史rescue率或多个相关treatment当新训练增益的效应先验来承诺显著。p>0.05不是等效证明，小样本不确定也不是肯定收益。

验收分层：

- **协议可设计**：现有审计可写清来源、离线采纳、对照与反证。SI-P0达到的是这一层的候选交付，尚待协调方审阅。
- **数据/工程feasibility**：未来授权后才可证明100%纳入项有真实公共时点、map/target/transition/terminal证据；0专家/hidden/future泄漏、0跨分区canonical重叠；训练预算与checkpoint等量，C多样性和重复约束可行。任一关键缺口阻断训练。它不代表效能通过。
- **效能确认**：须在预先固定新任务与足以回答问题的样本设计上，按预注册标准同时支持C>A、C>B_pool并满足伤害/总成本约束；否则不能声称有用的自改进采纳。此处尚无已批准样本、统计计划或通过阈值。

实质反证/停止条件：去重后纠错经验不足或只靠light个例；严格投影造成不可追溯目标；未知模型来源无法接受；新任务身份不足；C依赖过采样/更多生成或训练步数；C只赢弱对照而不赢A/B；改善只在已见源任务、训练loss下降或oracle挑选；伤害/获取费用抵消价值；或一轮结果无法区分选择配方与更强teacher。出现这些情况结束本轮候选，不自动扩大样本、换operator或开始第二轮。

## 8. 需要的新授权

协调方独立审阅这份设计之后，仍需人类明确批准：任何训练数据构建/公共输入投影或tokenizer运行；任何科学代码实现/测试；新source/paired验证/环境调用；B/C adapter训练、预算与冻结清单；任何独立任务科学评估。旧G2/G3/G4/review/clearance均不可复用为这些许可。当前learnedselector/memory/DPO/额外环境禁令维持。没有自动下一阶段。
