# v2 预算、STOP与归因合同：默认NO_GO

本文件只有纸上算术/研究设计。`PAPER_BUDGET_ARITHMETIC.json`及receipts/paper_arithmetic.*保存独立stdlib计算和真实exit0；没有项目模块、tokenizer、测试、analyzer/validator、policy replay或科学流水线调用。数值是保守完整上界，不是运行结果、收益预测、功效或执行额度。

## 1. 独立复算的预算

固定N96、H50、每task一source/唯一teacher首动作/同env suffix。d按动作数计。v2总d=96×5=480；v1总d=1200。suffix上界为96×49−总d。teacher每task两次生成，40+16输出帽；所有P0 source/suffix生成帽16。

| 费用组成 | v1均衡5/10/15/20 | v2全5 | v2 source-only |
|---|---:|---:|---:|
| source生成 |4,800|4,800|4,800|
| teacher生成 |192|192|0|
| suffix生成 |3,504|4,224|0|
| 生成总数 |8,496|**9,216**|**4,800**|
| source动作 |4,800|4,800|4,800|
| replay动作 |1,200|480|0|
| teacher动作 |96|96|0|
| suffix动作 |3,504|4,224|0|
| reset |192|192|96|
| 含reset环境操作 |**9,792**|**9,792**|**4,896**|
| 输出token |**138,240**|**149,760**|**76,800**|

v2完整生成=4800+192+4224=9216；环境=4800+480+96+4224+192=9792；输出=(4800+4224)×16+96×56=149760。它比v1少720 replay动作，多720 suffix生成/11,520输出token，不能说全面省钱。futility恰在完整source96之后停止时，可省去的后续保守上界为4416生成/4896含reset操作/72960输出token；已经完成的source费用不退回，未做的费用不当作实际“收益”。

保留累计input≤16,000,000、单次input≤8192、allocated GPU×monotonic≤4 device-hours的投资硬帽，不增额。逐调用8192推出的宽input包络为75,497,472，大于16M；因此16M必须独立逐调用实际预留/累计执行，不承诺完整9216可达。source-only的逐调用宽包络39,321,600也不保证能落在16M内。

4h包含真正占用GPU的装载、等待、token处理、环境/审计/清理与各阶段；不等于kernel latency，也不能在source→branch切换归零。如果实际资源被释放重获，未来需记录各真实allocation区间及累计，不能凭新进程清账。这里只规定账本要求，不建立跨run续跑或新资源owner。

没有8B/P0成功装载/新driver实测，不能以平均tokens或现有软件PASS预测4h足够。source-only最多4800调用本身是独立投资；当前没有支付它的充分新理由，不因完整预算上界存在就自动批准“先跑source看看”。代码里的旧Caps8496/138240及SI-E2工程4调用/88输出不能冒充本表新v2帽。

## 2. 账本分离

* 历史科学累计5142 generations/7949 reset-inclusive operations，已含177/342。本轮科学新增0，不重跑G2/G3/G4。
* 既有SI-E2完整工程probe的supervisor真实记录allocated_device_hours=0.006624203831630034、child exit1；另一次identity诊断记录device_hours_upper_bound=0.0005721175856888294。这是不同收据/定义，保留非零原件，不把一个精确记录加一个上界称为新的精确总成本；不归入科学样本，也不归零。
* 本任务新工程CUDA/模型/环境/SSH/tokenizer/测试调用均0。无unused task-body读取；只写自己的新文档目录。
* 未来v2采集是新账本/范围：完整物理debit与prefix比较的logical cost分开。CONTINUE引用source已记录suffix，物理收费一次；replay reset/动作只计环境，不计新baseline推理。failed/open保留保守reservation；不能填成已知零或任务失败。
* 未来训练/工程测量/600×3评价均不在9216/9792内。三臂600-task actor-only评价本身上界90,000生成/91,800含reset操作，是独立重大投入；没有任何当前授权。600是TRAIN任务隔离集合，非新heldout/layout外泛化证据。

## 3. STOP分类及不得混淆的结论

| 状态/条件 | 所支持的结论与保留字段 |
|---|---|
| 当前设计未采纳、live driver缺失、host/local PID未认证 | 当前COLLECTION_NO_GO_NOW/RUNTIME_BLOCKED；没有科学run可供标成失败 |
| future技术异常、单位返回不完整 | TECHNICAL_STOP，已知Y0/完成单位保留，未知YT/单位状态NA或open，不作科学失败 |
| identity/hash/public输入泄漏/Action-ID/receipt/replay矛盾 | INTEGRITY_STOP；整run停，原件不改、不以丢该task后补样解决 |
| 任一预留将超token/call/操作/allocated-time硬帽 | BUDGET_STOP/INCOMPLETE；不能加额度或把缺失source/teacher补成0 |
| 正常早终止、empty map、actor parser停止造成d5不可达 | source正常去向/NO_ELIGIBLE_STATE；Y0按原谓词，YT未执行则NA；不替换prefix/task |
| 96 source完整而E/F/S必要总量或family已不足 | COMPLETE_SOURCE96_STRUCTURAL_NO_GO；全部未测YT=NA及TEACHER_NOT_RUN_SOURCE_FUTILITY；不是完整paired pool |
| source必要上界全部够 | SOURCE_UPPER_BOUNDS_NOT_FUTILE，仅未被这些必要条件否决；不是Q、RECIPE或运行GO |
| source完整但只授权了source | SOURCE_PHASE_COMPLETE_BRANCH_NOT_RELEASED（概念状态）；即使上界够也不得进teacher |
| 全部预定E已按固定规则尝试后，实际共同Q/配额/固定draw/token等任一不满足 | COMPLETE96_RECIPE_NO_GO；保留全部96来源/invalid/harm/NA；不追加384、不重抽或放宽门槛 |
| 全部实际配方/曝光/成本合同闭合 | 最多RECIPE_CONSTRUCTIBLE；是否值得训练及评价仍另作投入判断 |
| 将来正式效能未同时达到两主比较/收益/伤害标准 | 不支持该固定小剂量配方的预定效能主张；不追调seed/d/epoch/teacher至positive |

只有source完整才有上述结构性不可构造结论；不能把source96尚未完整的技术/预算停止换成结构失败。也不在95条后以另一个未登记的早停算法结束source。对单task已执行teacher后的正常suffix失败可记录YT=0；未执行teacher或未完成的technical分支永远不是同一种0。

## 4. C24与contrast的未证明风险

引用协调方已独立核对的旧source描述，而非本报告新跑统计：旧127 source=120成功/7失败；去light后四家族120=114成功/6失败，pick-place0/30失败，其余三个各2/30。pick-two无旧source观测。旧d5可达111/120是另一个维度；它不增加那6个原source失败，也不能估计新五家族96的失败率或teacher成功率。我没有重数127原source/读取teacher结果来挑规则。

不依赖概率假设的新配方必要条件是新96中至少24个Y0=0且可达d5的task，并达到9/6/4/2/3；即至少25%的全96 source须落入可达失败上界F，之后还需teacher成功、Q及去重。这是代数必要条件，不是由旧6/120推出的新96预测或“绝不可能”的定理。task隔离与历史使用交集的具体可比性由Luna本次独立审计闭合；本稿不把metadata reservation自动升级为所有历史使用的clean证明。

三个纯逻辑反例说明不能把门槛通过互相替代，均非生成过的fixture或未来数据评估：

* 即使96个S5都可达，只要Y0全成功，C供给仍为0；d5可达提升不推出纠错供给。
* 即使E/F/S必要数量与family全够，teacher无足够成功或2048/共同去重损失仍可使Q/C不足。
* 即使C24和neutral24全够，neutral的实际监督长度未落入所选C需要的匹配cells，B的一次抽样仍可能neutral<8；不能为contrast重抽。

这些门槛是投资guard，不是最小可学习N定理。24新首动作×2曝光可能有用也可能没用；即使表面B≠C，在允许最大重叠时两臂可共享S120+16新例，即136/144例。数据剂量可构造不等于可辨学习差异，更不足以自动正当化后续90,000-generation评价。

## 5. 研究归因和允许主张

| 比较/证据 | 能支持什么（须未来真实效能证据） | 不能单独支持什么 |
|---|---|---|
| C−A | 同P0起点接受S120+24筛选teacher首动作及固定更新的整个追加训练包效果 | 不能分离S120复训、teacher标签、新经验或相互作用；没有S-only第四臂，本轮收窄主张 |
| C−B | 同一完整成功pool、共同S、曝光/token/配方条件下failure筛选相对family×长度匹配success-only采纳的差异 | 不代表一般未匹配success-only效果；不独立隔离状态难度/目标语义等筛选渠道；不是唯一机制证明 |
| paired Y0=0→YT=1 | 已执行、可追溯单次早期干预在该source/teacher+suffix合同下的局部结果差异 | 不证明该首动作普遍最优、可由公共输入唯一学习或训练后能迁移 |
| E、Q、mask、loss降低、配方可构造 | 可执行性/证据/剂量或优化层事实 | 不能替代任务成功率、C>A/C>B、成本/伤害或自适应停止效果 |
| 旧R19 oracle32/36相对K2的+2 | 旧开发前缀的事后上界和有限机会；不是新学习试验 | 不作为未来提升5.56pp的先验承诺、效能样本量或selector训练标签 |

B仍从包含C的整个B_pool单次抽取；匹配分布由所选C的family和实际监督长度确定，不是完全独立的普通success-only臂。相同teacher来源/生成池使C−B避免“换生成来源”的旧混杂，但其结论仍限于这个具体采纳配方。报告B∩C和实际neutral等，不按重叠大小重抽。

部署学生的输入只为冻结公共S5 P0 projection；label仅首动作ID+EOS，teacher诊断/subgoal及未来source/teacher终局不是学生特征。研究名称应是固定早期单次干预经验的动作蒸馏。d5不是错误触发点，不训练selector、不搜索停止规则、不声称adaptive stopping或同一实验覆盖全部恢复阶段。

将来效能如获独立投入，保留原C−A与C−B共同主比较、配对wins/losses、exact McNemar+Holm、Newcombe10边际CI、每项观测net≥5pp且gross harm≤5%等冻结标准与单训练seed限制；本轮不跑统计、不作新功效计算、不生成reporter或600task schedule。既有S120 tokenizer/mask证明也没有认证未来B/C实际token或新数据学习价值。

## 6. 同意、剩余风险与最小后续

同意Astra/root的NO_GO优先、唯一待审全d5/source-first候选、严格E/NA/STOP区分、同池B包含C和不扩大范围。没有需要新科学执行才能解决的本轮分歧；我补充的重点是旧auditor物理顺序、独立source seal、parser-stop checkpoint及四调用工程桥接不能复用为live driver。

仍未闭合：可信执行入口/PID映射；真实模型和资源证据；新phase/seed/counter驱动与auditor；新96的C供给及semantic dose；实际新B/C token/对照；是否值得付source96本身费用。缺少新的投入理由时默认不花这笔钱。若未来继续，只能先独立审查这个文档版本及明确工程任务，再讨论不同范围的能力测量与科学release；不得以本报告或旧工程PASS自动采集。
