# R19 G3/G4方法与分母独立审阅

日期：2026-10-30 UTC。当前线程科学顾问；不代表历史Astra线程。本次只读现存协议、原始JSON记录、冻结Git源码及已发表验收结果；没有运行正式analyzer、validator、模型、tokenizer、环境或科学统计，没有重新评估任何策略，没有修改原文件。

本次标准库JSON读取仅提取已记录的纳排/身份/分支结构字段和两个先前已经报告的案例字段；没有拟合、重新计算显著性/区间、设计新评估或选择新案例。实际对原始branches/events/source trajectories、协议、报告和受审稿求SHA-256。

**当前受审稿决定：CONDITIONAL_ACCEPT_FOR_WORKING_DRAFT，合并前须完成下述A–C纠正。** 主要数值与证据一致，问题是方法定义与表述精度，不是发现了结果造假或要求重跑。

## 受审稿与证据身份

受审稿 `/home/lizening/research-notes/agent-logs/2026-10-30T015900Z__SOL__r19-thesis-methods__8be2/R19_METHODS_RESULTS_DRAFT_EN.md`，本次实测SHA-256 `6a2a22297fe8296293e0de318468fa22fd2cc1e05048bd64afd30c46246cc985`。下文L行号针对该版本。

原始G3：run `260422ac02bd42a8b2929d7ef240526b`，代码 `2da980f631badc25086d12db60d128ff507d3ae6`。原始G4分析代码 `85cbb92395e5e2420c2adeb1fa0634653e742910`，分析身份 `r19-g4-offline-2026-10-25T040521Z-ebad1a0c`。本次没有执行这些版本。

| 证据 | 本次实测SHA-256 | 定位 |
|---|---|---|
| 冻结协议 | `3d7d1865c807d12276a8109b06c55da4e9182df0ca05a0b5463f8128dd03e122` | `/home/lizening/wt-r19-recovery-duration-v1/configs/experiments/r19_recovery_duration_v1.json` |
| 原始branches | `eff9b5e74d3d5daa928cb662dcc59fc3f434f66796b673679d40b374f3c8636f` | 下述G3目录`branches.jsonl` |
| 原始events | `05e1d443ff304eaa25d08b92a4e19d204a6c93a4f46bbe50aefef3271f211762` | 下述G3目录`execution_events.jsonl` |
| 原始execution manifest | `b00e8e4eed375532a080da6579940b44bc09089d7917540aea3ca4c227daffa0` | 下述G3目录`execution_manifest.json` |
| 原始source trajectories | `c6f37a7da28e326c70818524c79c17bbd85a286754c111f17db07cbe151a4f1c` | 下述G3目录`source_trajectories.jsonl` |
| G4 summary | `6ff56b7e9bc31c29bc9afd0c3ceea43c4fdf53b2addb29d3ce9f2c5e99b5d3c4` | 下述G4目录`summary.json` |
| G4报告 | `92c066ad1c9c7f187430db82ad6285800e4f31005a1fd2933231d30d695df4bc` | 下述G4目录`R19_OPPORTUNITY_REPORT.md` |
| 既有独立G4审查 | `e7941a530d60e97821bfa6931a2c142d31ef711c25019ba2ad502dd54066128e` | 下述独立审查目录`INDEPENDENT_G4_REVIEW.md` |

G3目录：`/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z/`。

G4目录：`/home/lizening/research-notes/agent-logs/2026-10-23T043602Z__LUNA__r19-g4-readiness__85cbb923/future_g4_report/`。

独立审查目录：`/home/lizening/research-notes/agent-logs/2026-10-25T040304Z__SOL__r19-g4-independent-result-review__85cbb923_dffaf4/`；本次另读其 `report_arithmetic_review.json`，未运行其复算脚本。

## 原始分母与记录结构核验

| 单位 | 数量 | 本次证据 | 含义与限制 |
|---|---:|---|---|
| 已完成source episodes | 127 | execution manifest的schedule_episode_count；既有G3/G4完整验证 | 产生候选轨迹的来源数，不是最终duration分析N |
| 初始attempt | 39 | 原始branches39行；原始event sequence9698的enrollment_frozen payload attempted_prefix_count=39 | 有39个不同source_schedule_index和39个canonical trial identity；不证明39个独立scene |
| Primary eligible | 36 | branches eligible_primary=true；enrollment event的failure6/success-control15/random-control15 | 第一恢复动作成功执行且仍非终止后的条件性cohort |
| Ineligible | 3 | branches eligible_primary=false，均eligibility_reason=stage_one_failure | failure层1、random-control层2；不是基础设施缺失，未从attempt层静默删除 |
| K-labelled result records | 183 | 36行的keyset为1..5，3行只有1 | 36×5+3×1；每个K1..5的primary分母都是36，K1 attempt级另有39 |
| Eligible derived/aliased K records | 11 | eligible行中derived_identity_from非null的记录数 | 进一步说明结果标签不能当独立运行次数或样本量 |

原始enrollment_frozen event ID为 `f14635272a407ddf96a0a83e172d3a033ad5ecfb45a7a1941aa41b744f5fd9f4`，enrollment hash `9ae916666d895989345c5104671e59e3366a0d87a1a17e4a3e4cf75693459ac1`，记录 `additional_stage_two_generations_before_freeze=0`。这支持初始入组先于延长恢复路径的边界；本次没有重做事件链全量完整性验证，继续依赖原G3/G4验收。

失败候选队列仅7个、6个eligible，低于原failure目标30；两个control各达15。计划60 eligible是上限/目标，不是缺失24个结局。没有补齐quota或跨层移额是原完整验收结论。不能称“随机抽样36个状态”，也不能把7/39或6/36推成部署失败率。

## 合并前修订A–C与精确替换

### A. L9必须给出eligible操作定义及条件化范围

当前“met the primary eligibility rules”让关键的处理后筛选不可见。建议在36计数后加入：

> Primary eligibility required an exact replay check, execution of the first recovery action without reaching a terminal state, and at least five actions remaining at the original intervention prefix. Enrollment was frozen before extending the common recovery paths. The duration analysis therefore conditions on passing this initial intervention stage; it does not estimate the unconditional effect of attempting recovery on all 39 prefixes.

依据：冻结G3 `src/recovery/r19_duration.py` L1344–1363，拒绝非exact replay；要求len(path.actions)==1、stopping_reason=awaiting_path_extension、terminal_checkpoint=None及原prefix remaining horizon≥5。L1423–1429记录入组freeze。基础设施replay失败会中止，不是普通ineligible。3个stage_one_failure保留在attempt级K1记录。

### B. L11“五个duration comparisons”改为“五个条件”

建议直接替换为：

> The primary denominator for the five duration conditions was 36 eligible prefixes, with four prespecified paired contrasts comparing K2–K5 against K1.

原L15准确列出四项primary contrasts，L11不应引入第五项。CONTINUE比较为另行描述，不纳入这四项Holm家族。

### C. L17“no mapped result for29”需区分支持性与映射

建议替换诊断句为：

> The offline public-state stopping diagnostic supported an exact measured-suffix estimate for seven prefixes, all seven successful. The other 29 were unsupported or ambiguous and were reported as coverage-only, without imputing a policy-success outcome; 7/7 is therefore not a full-cohort controller estimate.

理由：已报告两个oracle案例的 `branch_mapping_exact=true`，同时 `coverage=UNSUPPORTED`、`status=COVERAGE_ONLY`、`estimated_success=null`。它们不能贡献正式policy success，也不能说根本没有对应的测量分支。缺乏语义支持与缺少几何/分支映射是两种不同缺口。

非阻塞但建议一并修正：L7 “the task actor then continues”改为 “if the state remains nonterminal, the task actor continues within the remaining original 50-action horizon”。已经终止的恢复路径不会继续调用task actor。

## 控制条件、路径和成本的核验

冻结协议 `policies`区分带P0 adapter的task actor与不带该adapter的Qwen3-8B recovery controller；`model_objects_distinct=true`、`kv_cache_shared=false`。不应把它写成SI-U1的C checkpoint，也不应说两策略是同一adapter状态。

`common_path`规定每prefix一次Stage1；其diagnosis/subgoal冻结，后续Stage2使用同一上下文目标，K不进入生成prompt；每prefix只有一条canonical recovery path，先完成/冻结该path再看alternate suffix结局，不从另一个K的SFT suffix继续构造恢复。后续无效Stage2输出停止恢复、非终止则handoff；没有repair/retry/replacement。K数的是环境动作，不是模型调用；Stage1额外调用不可漏计。初始Stage1失效时协议仍记录一次初始Stage2生成但不执行动作，成本照记。

源码2da980f `r19_duration.py` L780起随机固定suffix次序（seed19022），不同K共享恢复动作；L809–829允许相同端点的已测suffix或终止端点以derived identity记录。因此“183 records”准确，“183独立实验”错误。exact replay支持public observation、history、动作顺序和map的记录一致性，不自动证明所有未记录隐藏状态完全相等。

CONTINUE明确复用exact source suffix，原协议 `population.continue`要求identity/prompt/horizon/replay checks；不是同期另跑的新K0。原127 source rollout不因CONTINUE引用而重复计为新执行。

`r19_duration.py` L710–729的logical_policy_cost：recovery-only包括Stage1加截至端点已计费Stage2；full-branch再加恢复后的SFT suffix。它不包含干预前公共source前缀，也不包括为了实验分支恢复状态所做的reset/replay。每个正K逻辑政策各计一次Stage1，而实际物理运行共享调用；不得把五个逻辑cost简单相加当真实支出。

现有31.9%是均值之比 `9854.25/7470.2222−1` 的描述，不是逐prefix token比值的均值，不是延迟/费用实测优势。工作稿L15的“higher on this measure”适当。

## 已发表结果与oracle解释

本次对照原G4 summary、原report及独立arithmetical review：CONTINUE/K1/K2/K3/K4/K5分别30/29/30/28/25/24成功，分母均36；K2对K1为2胜1负33平、Holm p=1；K2对CONTINUE为2救回2损失。没有在本次重新计算检验、区间或重新评价分支。

S_fixed=max_K平均success，S_oracle=平均每prefix的max_K success，K范围仅1..5。32/36−30/36=2/36=5.56pp的定义与记录相符。原稿正确限制为同样本选定的hindsight envelope，不是训练出的selector或总体策略上界。

本次从原branches直接读取两个旧审查已经指明的案例，确认：一例K1..5为10000、另一例00001，两例CONTINUE均成功；这只核实已有个案陈述，不是重新搜寻有利案例。故它们相对K2的oracle新增属于避免已观察恢复损失，不是相对CONTINUE新增的两次rescue。

但不能从这点反推“oracle相对CONTINUE没有任何经验性差值”：两个边际率确为32与30；oracle仍包括原有的K2 rescue。准确结论是没有展示现实中可选择这些分支的规则，而非事后组合在此样本上数学上无优势。

四项Holm调整仅属于K2..5对K1。R19协议的差值区间由每对比两组97.5% CP边际区间组成，不能把它写成SI-U1那种跨两primary contrasts的simultaneous95%构造，更不能宣称对R19四对比自动同时覆盖95%。如稿件不呈现区间，可留在方法附录；若呈现，必须说明其模型假设和多重区间范围。固定富集开发样本与scene依赖未建立时，p值不能证明总体效应。

## 执行与分析历史应如何保留

原G3完成后G4曾存在两个consumer契约阻塞：nested runtime manifest版本及缺失run_started envelope。后续在85cbb923修复离线consumer契约再执行G4，未重跑G3、未改原ledger。不要把早期“G4 blocked”审查当最终状态，也不要抹去这条修订链。

既有独立G4审查报告真实offline invocation exit0、56个输入前后hash一致，并独立核对原报告与远端bytes。本次实测本地主要hash相符，但未重新下载远端，也未重复56输入全部验证；“本次独立远端验证”不成立。

成本口径与原验收一致：本次G3 successor 4,965 generations、7,273非reset环境操作+334 reset=7,607；加历史已计177 generations/342 reset-inclusive operations后campaign累计5,142/7,949。原G4主报告的7,273只是非reset字段，不能作为全环境调用数。G4为离线分析且新增模型/环境调用为0。原G3审查出现的source-bound和branch-bound事件集可有共享引用，不能将其计数直接相加推断独立外部调用。

## 非阻塞限制与下一份论文交付

- 36为共享路径与初始intervention条件下的分析单位；不保证scene或task-parent独立。现有39个不同canonical trial仅支持身份层分离。
- 失败层仅6、两个control共30且two-object为0；0个样本时不能报告该family成功率0%。
- 配额与source结局富集使之不代表一般agent遇到失败时的分布；入组条件使之不代表全pipeline可靠性。应同时给出39-attempt层K1与CONTINUE的已发布描述，若不呈现数值也至少明确保留该分母及3次失效。
- R19与SI-U1没有可合并分母；不能把恢复机会当作self-improvement提升、训练机制证据或许可。
- 上述A–C修正后可并入工作稿，仍需在证据附录补上协议/执行/analyzer版本及cost定义；不需要任何新模型或环境运行。
