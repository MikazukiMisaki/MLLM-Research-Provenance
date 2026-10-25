# R19 科学复盘与下一阶段最小可证伪设计

日期：2026-10-25 UTC。状态：**DESIGN_READY_FOR_SOL_REVIEW**，不是独立审查 PASS，不是执行方案放行。

分工：Implementation Engineer 提出机制假说、竞争解释、最小设计及停止条件；Sol reviewer 独立审视 headroom 来源、配对统计、成本、证据边界及本方案。发布由协调方负责。本文件不修改 R19 协议、代码、结果或任何 clearance。

## 1. 默认决定

**GO：仅投入有时间上限、零新增模型/环境调用的原诊断可识别性审计。NO-GO：现在启动 prospective 科学小试、扩样、学习或搜索停止策略。**

5.56 个百分点值得作为“交接时机有异质性”的探索线索保留；目前不值得据此投入一个宣称能识别该效应的效能实验。理由不只是 N 小：可用的早期信号尚未证明；K2 与 CONTINUE 都是 30/36，而 K2 平均完整分支逻辑 tokens 高 31.9%；原唯一公共停止规则只支持 7/36；oracle 的两个额外成功需要相反的时长选择。

当前新增推理、环境操作、训练、外部 API、云算力采购预算均为 **0**。本轮只读报告/协议/源文件并作纸上推导，写设计文件；没有执行下述后续审计表、数据连接、规则重算或试验。即使未来工作声称“零新增推理”，也须另获授权，不能借此重跑 G4 或创建新的离线 policy 估计。

## 2. 输入身份与已确认事实

已只读核对原件 SHA256：

| 输入 | SHA256 |
| --- | --- |
| 正式 `summary.json` | `6ff56b7e9bc31c29bc9afd0c3ceea43c4fdf53b2addb29d3ce9f2c5e99b5d3c4` |
| 正式 `R19_OPPORTUNITY_REPORT.md` | `92c066ad1c9c7f187430db82ad6285800e4f31005a1fd2933231d30d695df4bc` |
| Sol `independent_G4_acceptance.json` | `7331b865778481ab4e1b10943eac0e4090ea004e214dbdfff283cfbe042833e6` |
| 冻结 `R19_PROTOCOL.md` | `7668d7fa5422ad6ad7d3affc72b2e573ec19aae53314198fc14b46dc74c9a3d9` |
| 冻结机器协议 | `3d7d1865c807d12276a8109b06c55da4e9182df0ca05a0b5463f8128dd03e122` |

正式报告目录：`/home/lizening/research-notes/agent-logs/2026-10-23T043602Z__LUNA__r19-g4-readiness__85cbb923/future_g4_report/`。

独立验收目录：`/home/lizening/research-notes/agent-logs/2026-10-25T040304Z__SOL__r19-g4-independent-result-review__85cbb923_dffaf4/`。同时阅读其 `INDEPENDENT_G4_REVIEW.md`、`RESULT_INTERPRETATION_ZH.md` 及已有算术复核文字，不重做统计。

保持身份：analyzer `85cbb92395e5e2420c2adeb1fa0634653e742910`；executed G3 `2da980f631badc25086d12db60d128ff507d3ae6`，run `260422ac02bd42a8b2929d7ef240526b`。本轮读取时两个开发工作树均仍在相应 SHA 且干净。原 provenance main `114f6521bbe244138c556c34c8dcb8d9d76784d6` 是委托给定的截至时间记录，本轮没有网络更新或声称核验最新远端。

**CONFIRMED（引用正式结果，不是本轮新计算）：** eligible N=36：failure 6、success-control 15、random-control 15；39 attempts、127 sources、183 K arms。K1..K5 成功 29/30/28/25/24；CONTINUE 30。K2 对 K1 是 2 赢/1 输，Holm p=1；其余已登记比较 Holm p≥0.5。最佳固定正 K 的 30/36 与 oracle 32/36 差 2/36。failure 队列 7 候选耗尽，无补样，pick-two eligible n=0。

CONTINUE/K1/K2 平均完整分支逻辑 tokens 为 7470.2/9778.9/9854.25。K2 相对 CONTINUE 是 2 救回、2 伤害，总成功数相同。公共诊断仅 7 个 supported/exact mapped，7 个成功；另 29 个 coverage-only，不能填补为整组政策效果。

累计真实科研支出保持 5142 generations / 7949 environment operations（含 reset），包括历史 177/342。报告中 G3 的 7273 是非 reset 操作，另有 334 resets，不能把它当作 reset-inclusive G3 7607 或累计 7949。本轮不增加这些计数。

## 3. 要证伪的假说及竞争解释

待研究的具体假说 H：**在不改变恢复动作生成、actor、prompt 或初始恢复触发的条件下，原已冻结的公共 subgoal 满足事件能在因果时点选择交还时机，相对 CONTINUE 与冻结 K2 给出有实用价值的收益。**

它比“有异质性”强，也比“oracle>最佳固定 K”强。只允许这一个规则进入以下讨论；不产生一个候选 rule 列表再择优。

| 竞争解释 / 风险 | 现有证据能说什么 | 最小反证问题；不能怎样补救 |
| --- | --- | --- |
| 同样本选择 K2 和逐样本 oracle，选择乐观 | 两者都在同一 enriched TRAIN cohort 上选择/评价；oracle 看了五个未来结果 | 冻结原 D5 后，在独立新 TRAIN identities 上是否仍出现相对 CONTINUE/K2 的净价值？不能用旧36个结果拟合规则再报旧样本成绩 |
| 两个特定 case 驱动 headroom | 已发表模式中 `10000`、`00001` 各一例，是相对 K2 的额外可救回点 | 既有 detector 在这些 case 的所需时点，是否已有合法信号？若无，原 D5 没有捕获该两例的机制证据；不得据此增加专用词法/例外 |
| satisfaction 只标记本来容易成功的状态 | 7/7 是条件性结果；不等于因果救回 | 对相同原前缀必须同时保留 CONTINUE/K1/K2，且把“同样成功但不同成本”与真正 rescue 分开 |
| control 富集、family/stratum 集中 | 30/36 为 control，failure 仅6，缺 pick-two | 不能把本队列效果推广为总体、失败恢复或六类覆盖；不得事后只报告有利 family/stratum |
| K 改变 SFT 所见状态/历史，未必是可预测停止信号 | 这是 persistence/handoff 的条件性效果，不是纯多想一步的效果 | 早期合法特征与停止动作必须先于 suffix outcome 固定；不能用未来 action success/专家路径/全任务标签决定 handoff |
| 单次 suffix 的运行非确定性或偶然分歧 | greedy 与局部 smoke 复现不等于已量化全部36例的期望效果稳定性 | 本轮无法排除；不能把未重复的 arms 当成已排除随机性。未来独立病例只能检验迁移的初步可行性，不能自动识别同一状态的随机方差；任何专门重复须另设计/授权 |
| 手工 subgoal 的支持范围太窄 | 7 supported / 29 unsupported | 低覆盖本身可以使路线不值得投入。不能事后扩 parser、让模型判 subgoal，或把 unsupported 换成对旧样本有利的 fallback |

**INFERRED（纸上逻辑）：** `10000` 需要 K1；`00001` 需要 K5。一个实现 oracle 的因果策略不只要“解释这两例”，还要保留 K2 原有的 30 个成功，避免给其余成功病例引入新损失。oracle 32/36 只在五个正 K 之间取最大，不包含一个可部署的“是否开始恢复”选择器，也不是含 CONTINUE 的全策略总体上界。

**NOT VERIFIED：** 两例是否具有原 detector 可用信号；7 个触发的具体时点及相对三个 comparator 的完整成本/救回结构；异质性是否可推广；suffix 随机变异程度。此处不补作 case-level policy replay 或新估计。

## 4. 唯一候选：原规则 D5，不能偷换 fallback

来源为冻结协议 Passive public stopping diagnostic 及 `src/recovery/r19_duration.py` 的 `parse_public_subgoal`、`evaluate_public_subgoal`、`passive_stopping_decision`、`offline_public_stopping_estimate`。本轮仅阅读定义。

在每个已执行恢复动作 j≥1 的公共转移之后：

1. 若环境已经 terminal/truncated，按原环境终止和50-action horizon语义结束，不增加新的truncation判定；截断本身不是成功。不能为了检查 detector 再执行一步。
2. 否则，仅用原始 Stage-1 subgoal 和截至 j 的已执行公共动作/观测、对应 transition IDs，检测当前 `SATISFIED / NOT_SATISFIED / UNKNOWN`。
3. `SATISFIED` 则交还 SFT；否则，包括 `UNKNOWN`，继续恢复至 common terminal/validity stop 或 cap5；到5交还。
4. 后续 Stage-2 invalid/malformed/truncated/unmapped 时原样停止恢复，若非终止则交还；无修复/重试。已执行 no-op 计动作，解析失败无环境调用不计动作。原始 50-action horizon 不重置。

Unsupported 的原行为是 UNKNOWN→继续至 cap5/原强制停止，**不是 K2、K1 或 CONTINUE fallback**。更换 fallback、cap、正则、predicate、阈值、特征或 reward 定义都成为新假说/未来修订，本设计不把它们作为备选方案偷偷并列。若原 D5 不值得做，默认关闭这条路线，而不是在旧 outcomes 上找下一个规则。

原 estimator 有明确的 `if not supported or not branch_mapping_exact: COVERAGE_ONLY` 守卫。因此，已有记录包含 `selected_k` 也不能绕过守卫替29例填写 outcome/cost。本轮不改守卫、不调用 estimator、不生成新36例 policy 汇总。

**条件性结构证书，供 Sol 审查，不是 policy 成绩：** 若后续只读审计能证明所有29个 unsupported 的 D5 与其 K5 在终止、invalid generation debit、状态/历史及 suffix 身份/结果上完全一致（token/call/action成本可同源核对，detector CPU另加），则 D5 只可能在其余7个 supported case 改变 K5 结果。已知 K5 成功24，所以成功数必有 `S_count(D5) ≤ 24+7=31`，比正K oracle32少至少1，最多对 K2/CONTINUE 多1/36=2.78个百分点。这个宽松上界甚至允许7例全部改善，不能写成“D5=31/36”。前提尚未逐条认证，原报告仍为7 mapped/29 coverage-only；它不是总体效应上界，也不能据此给新 cohort 的效果设定先验真值。

## 5. 阶段 A：优先申请的零新增推理可识别性审计

建议只给本阶段后续授权：上限 **8 person-hours（工程4 + 独立审阅4）**，新模型/环境调用0，外部费用0。不重跑 analyzer、validator、detector、环境、策略或统计流水线，不重写正式结果。8小时耗尽而未闭合就交未闭合项并停止，不借“补证据”延长工作。

最小产物是一个引用**既有**诊断记录及原文件/事件哈希的36行证据卡清单；它不是新的 rule evaluation 表。本轮只提出字段模板，不填写新数据表：

`opaque_case_id | original_subgoal_ref | existing_supported_status | existing_selected_k/reason | detector_input_transition_ids/cutoff | existing_exact_map_ref_or_missing_reason | current_truth_support | terminal/invalid/alias/cost_binding_notes | reviewer_disposition`。

顺序应为先审因果来源和 operational predicate，再冻结人工审阅意见，最后由 Sol 对照既有 outcome/cost。先看 full outcomes 再“认出信号”不能被称为盲态验证。规则早于 outcomes 冻结不意味着本轮人类审阅者没有见过汇总结果，须诚实记录这种知情状态。

必须闭合：

- 36/36 有去向；原7个 exact mappings 的引用/当时状态证据完整率100%；29个 unsupported 的原因逐一保留，未认证 outcome/cost 继续 NA。
- 所有被用作决策证据的字段100%具有 ≤j 的时间来源；0条 source future outcome、stratum、别K suffix、未来 reward、任务ID查表或隐藏 state 进入 decision。
- 确认至少一个非 terminal、非 invalid 强制停止的 j<5 原有 `SATISFIED`；否则只观察到 cap/强制停止，没有测到自适应交接机制。
- 检查原检测器所谓“当前满足”的公共证据，而非用整任务最终成功充当 subgoal 真值。若发现因果泄漏或 predicate 语义不能支撑已记录标签，停止该路线；不就地调 parser。
- 由 Sol 审视两类 oracle 特例的早期信号，以及其余病例的潜在新增损失，不能只抽两个 winner。此步骤是对既有唯一假说的解释/反证，不生成新 classifier。
- 原29例为何没有政策映射：是支持范围限制，还是状态、alias、forced-stop、成本身份缺口？条件性31上界的等同性前提能否认证？不能认证就明确不可识别，不补跑原病例。

**A 的可接受结论：**“冻结 D5 的因果来源/映射足够明确，是否值得申请一次机制小试”；或“原 D5 缺乏可识别/可用信号，关闭”；或“证据不足，在8小时上限内不能判断，停止，不扩张规则”。这些都不是效能 PASS。只有有合法非平凡触发、没有未解决的语义/映射风险、且价值目标未被结构证据排除，才值得由 Sol 提出 B 的新授权请求；不是自动进入 B。

不能由 A 得到：新的29例政策成功率、基于现有 outcomes 拟合的最佳停止器、改 fallback 后的 retrospectively best 结果、对旧36例的确认性显著性。

## 6. 阶段 B：若 A 提供理由，再申请一次独立 TRAIN 机制小试

**当前 NO-GO，以下仅是条件性资源封顶草案。** 目的为时点/状态恢复/合同和初步成本可行性，不是确认5.56pp，也不是在少数例上比较候选规则。

### 6.1 样本与比较

- 最大12个新 canonical TRAIN game/trial identities：六个原有 family 各最多2个，来源/排除/身份/seed/顺序在 source generation 前冻结并哈希。不存在足够新任务则相应更少；不得跨 family 借位。
- 每任务最多1个前缀；来源不得与 R19、历史已消费开发身份、已知 SFT训练身份或保留确认身份重叠。若 SFT训练身份不可完整建立，沿用诚实的“TRAIN-development，训练不重叠未证实”，不能改称 unseen 或 held-out。保留确认身份仍禁止使用。
- source 最多12条，initial attempts最多12，eligible最多12；12只是研究支出上限，不是 power 计算或承诺取得12个 eligible。沿用原选择器和 H_i≥5、原 eligibility 语义，禁止按 subgoal 支持/收益选入。
- 建议预先固定 failure/success-control/random-control eligible cap 各4，source后冻结 disjoint queues，排队/随机控制定义沿用原方法；队列耗尽、预算触顶或固定 sources 结束即停止，无补样、quota转移、换seed伪装新任务或追加 source。这个新队列混合是新小试设计，不能冒充复现R19原30/15/15目标或当前6/15/15总体。
- primary 比较必须包含 `D5 vs CONTINUE`，并同时保留 `D5 vs K1`、`D5 vs frozen K2`。K2 在新 cohort 前就固定为2，不能重选最佳固定K。若仅赢K1而不优于 CONTINUE/K2，不构成路线进展。
- CONTINUE 只能认证复用同一新 source suffix 的 actor/prompt/public history/action-map/horizon；认证不成立则 blocker，不允许偷偷重跑一个 comparator。原R19 source/branch一个也不重跑。
- 主效应限于共同第一步后预先冻结 eligible cohort，同时保留全部 attempted cohort 的 K1/CONTINUE及初始无效/terminal和成本，避免把初始干预损失隐藏掉。不得把这个条件性 estimand 写成全体TRAIN任务效果。

### 6.2 唯一规则和因果时点

唯一规则仍 D5，不训练、不校准、不选阈值，不使用 stratum/source未来结果、不加入“no progress”、confidence或其他停止器。Stage1只生成一次，Stage2/SFT prompts、greedy、thinking-off、adapter隔离、token caps不变；不把assignedK或detector状态写入模型prompt。

在 checkpoint j、生成 j+1 或任何替代 SFT outcome 之前，先持久化规则的输入引用、状态和 handoff/continue decision，包含 exact transition IDs。只有原 subgoal 和 ≤j 的公共动作/观测可见；当前环境终止标志仅用于原强制终止语义，未来 reward 不得作 stopping feature。若截至当前j已有放下/拾取/离开等撤销转移，按原检测器的 current-truth语义处理，不能只找历史一次命中。一旦D5在j交还的决定已冻结，后来为K2等comparator延伸的路径动作不得撤销、改写该早期决定。

把公共诊断变成前瞻治疗的时点记录/执行，是对原“仅passive offline”例外的未来协议变更；需新范围、新协议及精确实现SHA独立审查。它仍不许可 learned recovery selector、初始恢复触发选择、memory、额外reflection/model、DPO/ORPO、PPO/GRPO或held-out。若有人提议这些，必须另立研究修订，不能算本设计已批准。原85/2da两个引用永久不动，不能直接拿旧pilot/clearance启动此试验。

### 6.3 共同路径与最少 suffix

正K比较共享 Stage1 和第一步；对每个 case，按原规则因果地确定 J_D5。只需保留 K1、K2、D5 三个逻辑政策，无需再跑K3/K4/K5的五个固定suffix。可在冻结各时点决定后，把 canonical path 延伸到比较所需最大 checkpoint `max(2,J_D5)`，遇原terminal/invalid停；所有替代 SFT outcomes 均在路径与选择记录冻结之后获取。

例如 D5 在j1交还，K2还需第二个恢复动作。这是为 comparator 产生的物理开销，不能回写 D5 决策或给其逻辑成本加上未来调用。若D5与K1/K2有相同 checkpoint/状态/suffix，可认证alias，物理只执行一次，逻辑各自计费；detector CPU耗时归D5，不归固定K。invalid造成相同suffix但不同generation debit时，保留每个政策自己请求过的调用。不得把 K2 没请求的第三次 invalid generation 计给 K2。

恢复/replay必须保持同一 trial、seed、counter、完整公共历史、obs、ordered actions及Action-ID。原 horizon=50，SFT剩余 H_i-已执行恢复动作；no-op/terminal/truncation/invalid与原协议完全同义。任何 replay mismatch、actor污染、未来泄漏或缺失外部操作完成凭据，立即停止；不替换样本。INDETERMINATE不是任务失败，保留已花成本和分母缺口。

## 7. 数值验收与停止条件

以下是**拟议资源/决策门槛**，不是由R19估出的真值，须在任何未来数据产生前由 Sol 和用户接受；不能看新结果后改线。

| 层次 | 拟议验收 | 停止/反证及允许的结论 |
| --- | --- | --- |
| A 身份与因果可识别性 | 36/36有去向；7/7既有exact证据引用完备；所有used fields100%≤j；未来泄漏/语义矛盾0；至少1个非强制j<5触发 | 任一未闭合不启动B；若只有新规则才能利用信号，关闭原D5路线，不调rule |
| B 执行合同 | 所有已消费unit/成本留痕100%；detector新增model calls=0；未来泄漏、horizon/invalid/terminal/Action-ID/状态恢复偏离=0；不得重试外部不确定操作 | 一次合同破坏即停止；不称策略失效，也不替换或把未完成unit算任务失败 |
| B 最低机制可行性 | 至少1个非强制j<5的真实causal触发，并至少出现2种实际SFT handoff时点；预定cap及非terminal invalid交还可计入但单列，terminal没有handoff不能凑数 | 未达即“本上限内机制证据不足”，不加sources凑trigger |
| B 值得另议更大研究的投资筛选 | 合同完备；至少3个此类非强制触发，来自至少2个family；相对CONTINUE与K2各至少1个净赢；完整分支逻辑平均tokens≤1.10×CONTINUE且≤1.00×K2；K1比较同时公开 | 任一不达，默认不追加推理、停止此路线。3/2与成本百分比是避免单case和弱基线驱动的资助偏好，不是显著性或总体效果保证 |
| 效能确认 | B无论出现什么 nominal p，都不作为本轮效能确认；必须另行设计独立新TRAIN cohort、固定样本/错误率/精度及资金；保留三比较 | B的mechanism/feasibility通过不能叫 adaptive controller superiority，不自动扩样或转heldout |

投资筛选对低覆盖可能很严格；这是有意接受的“资源上限内不值得继续”判断，不是声称理论上不存在其他停止策略。若没有预算在12 sources上观察3个触发，不能以“至少需要再几例”无限继续。

未来若申请确认性研究，我建议事前把实用目标定为：相对 CONTINUE 和 frozen K2 有正的 paired success advantage，目标幅度至少约5个百分点，且tokens不超过CONTINUE的110%。这些5%/10%是待批准的价值选择，不是当前oracle对新cohort的预测。三个正式paired比较须一起登记并控制多重性（例如Holm）；CONTINUE和K2都必须通过相应确认要求，不能只拿K1结果作结论。若还要声称成本非劣/节省，须另预登记其margin、配对区间和错误率；`p>0.05`与样本均值较小都不能替代非劣/总体成本推断。该确认研究的精度和资源方案未闭合前仍NO-GO。

**为何不承诺任意小N确认5.56pp：** 对一个在未来资料前就固定的策略，即便观察到2赢0输，双侧discordant-pair exact p也为0.5；5赢0输为0.0625，6赢0输才为0.03125。若三项正式比较用Holm，最强首项要跨0.05/3，理想全赢无输也至少7个discordances才可能过线；这不保证其余比较通过。这里只是纸上exact-test例示，不能给当前事后oracle计算有效的policy显著性。

效能样本量取决于 discordant-pair概率q、真实差d、校正与所需power，不能只从2/36抄一个N。配对差取{-1,0,1}时方差为q-d²；常规近似的N数量级随 `(q-d²)/d²` 增长。在d约5.56pp、q约0.1–0.2的纯假设情景，通常已是几百pair的量级而不是12/36；不是R19拟合的q或正式样本量。q若很低、效应更小或成本要求更严，设计可能根本不值得资助。不得用本小试不断查看p后增样本。

## 8. 资金与硬预算提议

**现在批准/使用额度：0新增科学generation，0环境操作，0外部费用。** A仅建议8person-hours静态审计，不增加科学计算。当前阶段不启动A的新数据审计表或任何流水线。

只有A给出理由、Sol独立审查方案、用户再授权时，B才可考虑以下**最大资源包**：最多12 sources/12 attempts/12 eligible；整个未来活动（含任何另外明确批准的必要机制sanity）总计不超过 **3000 generations / 5000 environment operations（含所有reset/replay）/ 12 existing-GPU-hours / 外部付费0**。这只是封顶提议，不是许可，也不是要把余额用完。若需要额外付费、原模型/环境以外资源或不能在该包内完成，默认NO-GO，不能自动上调。机构计费如需货币预算，应在授权前填入批准的单价和总额；未批准金额视为0。

保守纸上分项上界如下，不运行任何资源估计程序。对原前缀p≤45、H≥5；这里把restore重复多计以保持保守：

| B主体分项 | generations上界 | environment operations上界（含reset） |
| --- | ---: | ---: |
| 12 source episodes，每个≤50actor calls/actions+1reset | 600 | 612 |
| 最多12次纯replay身份门，每次≤45actions+1reset | 0 | 552 |
| 最多12个初始Stage1/Stage2和restore+第一action | 24 | 564 |
| 最多12条额外4步path及保守重新restore | 48 | 612 |
| 至多3×12个suffix，各modelcalls≤50，含完整restore+suffix≤50actions+1reset | 1800 | 1836 |
| 主体总上界 | **2472** | **4176** |

3000/5000包的余量最多528/824，不能自动花在复跑、额外病例或新比较上。若新实现独立审查要求独立有限sanity，必须先精确列出其新身份/范围/成本且在该总包内单独获批；不能把旧G2/G3清零重跑，也不能以“先做smoke”为未授权例外。主体上限不是实测费用，shared aliases可使实际更少。

计费同时保留两个账本：物理research ledger每次实际source/recovery/restore/suffix/reset只计一次；每个logical policy从原前缀独立计Stage1、它请求的所有valid/invalid generation、执行action和自己的SFT suffix，D5另计detector CPU。input/generated/total tokens、calls、actions分开，reset/replay不挪入部署逻辑cost。成功代价与matched-outcome cost都公开，不事后选utility权重，不声称deployment latency speedup。

预执行操作/新unit前应确认剩余预算容纳其保守上界；超时在安全边界停止，不把硬预算当作杀进程后可随意重试的理由。若中断无完成receipt，保留INDETERMINATE、停止且不补样。规则或预算一旦冻结，观察到任何收益/损失都不能改cap。

## 9. Sol 的独立评审问题

请独立接受或推翻以下设计判断，而不是替开发方背书：

1. 原 D5 的 causal接口能否在不加新规则下区分所需交接，或结构性证书已说明它只能覆盖很小的目标？
2. 两个oracle特例与K2原有成功病例是否支持未来研究动机，而非仅同样本选择、易例或suffix偶然性？已登记headroom仍只作探索线索。
3. A是否足以作下一笔投入的门槛，还是现有证据已应直接关闭？能否接受29例保留NA且不要求补跑？
4. CONTINUE/K1/冻结K2是否都被公平保留，logical/physical和invalid/alias成本是否正确且没有弱基线替代？
5. B的12source资源上限、trigger条件及1.10×成本投资门槛是否值得批准？若不同意，先修改纸上方案并重新审查，不能运行后改线。
6. 未来把passive detector变为治疗所需的新协议/实现/授权是否闭合？任何learned selector、rule搜索或训练例外均未批准，也不在本方案请求内。

**本轮完成的工作只限于文件核对、源码阅读、纸上竞争解释与设计。没有运行analyzer/validators/统计流水线、任何policy replay、模型/环境/G3/G4，没有修改科学代码、旧引用或原始证据，没有派遣Luna或发放PASS/launch clearance。** 新文件位于/tmp，未写共享INDEX/root inventory或其他agent目录；协调发布仍由Sol负责。

最终建议保留：**先用0新增推理检验原唯一假说是否可识别、是否值得投入；默认不启动B，更不承诺确认5.56pp。若原规则被反证或仅换rule才有希望，就停止这条路线，保留R19作为有限的handoff异质性结果。**
