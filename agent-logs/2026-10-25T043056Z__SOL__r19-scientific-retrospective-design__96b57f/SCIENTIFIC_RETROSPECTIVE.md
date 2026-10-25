# R19 正式结果科学复盘

状态：DESIGN_AND_REVIEW_ONLY。本文解释已经独立验收的正式 G4；不授权任何新分析执行、模型/环境调用、重跑或训练。

## 独立判断

现有证据值得一次有时间上限、零新增推理的可执行性与证据覆盖审计；不值得仅凭 5.56 个百分点启动自适应控制器开发、扩大 live 样本或训练 selector。这个决定针对当前候选与投入依据，不是否定所有自适应停止研究。

R19 已经完成了有价值的负向边界测量：恢复持续时间会改变结果，持续更久并不单调改善任务，额外恢复也会破坏原本可成功的轨迹。但目前缺少“能在决定时观察到什么，足以选择更好的停止点”的证据。

## OBSERVED：正式样本、效果与成本

已验收的 G3 是 source SHA `2da980f631badc25086d12db60d128ff507d3ae6`、run `260422ac02bd42a8b2929d7ef240526b`；G4 analyzer SHA `85cbb92395e5e2420c2adeb1fa0634653e742910`。本轮没有执行它们。

127 个 source episodes、39 次 attempts，36 个 eligible 状态（failure 6、success-control 15、random-control 15）。失败队列耗尽，没有补样或跨层填额；不能把这个组成当作实际部署失败分布。无 held-out 证据。

| 策略 | 成功数 /36 | 成功率 | 平均 full-branch logical tokens |
|---|---:|---:|---:|
| CONTINUE | 30 | 83.33% | 7470.22 |
| K1 | 29 | 80.56% | 9778.89 |
| K2 | 30 | 83.33% | 9854.25 |
| K3 | 28 | 77.78% | 11749.67 |
| K4 | 25 | 69.44% | 13514.00 |
| K5 | 24 | 66.67% | 13482.36 |
| K1..5 事后 oracle | 32 | 88.89% | 不能当作可部署策略成本 |

K2 相对 K1 是 2 wins、1 loss、33 ties，净多 1 例；预注册四项比较 Holm 校正 p 均不小于 0.5。没有得到固定时长增益的统计支持，也不能据此声称策略等效。K2 相对 CONTINUE 是 2 wins、2 losses、32 ties，成功率相同而平均逻辑 tokens 高 31.9%。在本样本的成功率和平均成本两个汇总指标上，CONTINUE 是更强的基准；并非逐状态都优于 K2。

36 个状态中，10 个在不同 K 下成败不同；相对 K1，存在某个更长 K 可以帮助的状态为 3 个，也存在被某个更长 K 伤害的状态为 7 个。两者不是一次已验证策略的净收益。

## OBSERVED：5.56 个百分点具体来自哪里

H = 32/36 − 30/36 = 2/36，只是已测共同恢复路径上的经验性事后 envelope。oracle 在看到所有后续结果后选 K；真实停止策略必须在 checkpoint 当时决定，不能使用之后的结果。

| 分层 | N | K2 成功 | 至少一个 positive K 成功 | oracle 相对 K2 新增 |
|---|---:|---:|---:|---:|
| failure | 6 | 2 | 2 | 0 |
| success-control | 15 | 15 | 15 | 0 |
| random-control | 15 | 13 | 15 | 2 |

这两例的现有原始记录如下；是读取已经产生的字段，不是执行新策略评估。

| prefix 后缀 | 家族 | K1..5 成败 | CONTINUE | 原公共检测器 |
|---|---|---|---|---|
| 8ec4fc037229710f8f13 | look_at_obj_in_light | 10000 | 成功 | 各 checkpoint UNKNOWN / UNSUPPORTED |
| bf448be94724da4562c0 | pick_cool_then_place_in_recep | 00001 | 成功 | 各 checkpoint UNKNOWN / UNSUPPORTED |

两例均属于 random-control。它们支持“部分恢复损失可以通过不同 handoff 时机避免”，不构成相对 CONTINUE 的两例新 rescue。failure 层没有观察到 oracle 超过 K2，不代表总体不存在这种 headroom：只有 6 例，且采样不代表部署总体。

这也不等于“自适应组合绝无价值”：K2 相对 CONTINUE 已有 2 个 rescue，同时损失 2 个原本成功的状态；上述两例正是那两个损失。一个可执行规则若保住前者并避免后者，在本数据上有超过 CONTINUE 的可能。R19 展示的是这种事后组合的可能性，尚未展示事前可用的信息或可部署策略；不能从两例原本成功就推出所有自适应停止无价值。

原检测器对两例的记录都是 cap5、COVERAGE_ONLY、estimated_success/cost=null。即使记录中 branch_mapping_exact=true，也不能越过 unsupported 语义把它们补成正式策略效果，更不能挑选其中有利的一例填报。

## OBSERVED 与 NOT PROVEN：停止信号

正式公共停止诊断仅 7/36 支持且可精确映射，7 例成功；其余 29 例 unsupported/ambiguous、只报告 coverage。7/7 是有条件子集，不是全体策略成功率；未证明较 K2 或 CONTINUE 的成功或成本优势。

尚未证明：

- 原始 subgoal、截至 j 的公共观察和动作能区分应该早停与应该继续的状态。
- 在不读取 future observations、reward、任务最终结果、source 成败/分层或 oracle K 的情况下可以获得上述 headroom。
- 扩展谓词、改变 UNKNOWN fallback 或新增 learned selector 会泛化到新任务。
- K 间差异是哪些具体机制所致。环境状态改变、handoff 后 actor 行为差异和数值/执行变化只能作为待审计解释，不能未经证据宣称是随机噪声。单次共同路径不能估计重复运行方差。

即使设想一个事先冻结的策略只有 2 个 paired wins、0 losses，双侧精确符号/二项检验也仅为 0.5；这只是数学示例，不是对 oracle 的新显著性检验。不能把一个任意小的 pilot 包装成对 5.56pp 的效能确认。

## 投入与停止决定

建议下一步仅设计一次固定 36 例的只读可执行性与证据覆盖审计，覆盖全部 10 个结局随 K 变化的状态（8 种非恒定模式）和 29 个 unsupported，不搜索规则，不补样，不更改冻结 fallback。预算建议为 0 model generations、0 environment operations、最多 4 人时、一轮固定审计；此预算是未来授权提案，本轮未执行该审计。

如果解释 headroom 需要看未来、扩写针对两个样例的谓词、改用更弱基准、丢弃 UNKNOWN 或改变 fallback，则本候选停止。若只有有条件子集结果、无整体可靠比较，结论仍为不足以支持 live 试验。后续真正的新规则必须先有独立的协议修订与新数据设计，不得把已暴露的 R19 数据称作 held-out。

成功提高和降低成本是两个不同研究主张，必须在看新数据之前选定。比较中必须保留 CONTINUE（主实用基准）、K2（R19 开发集选择、在新阶段固定）和 K1（原时长语义基准）。只相对 K5 节省、或只赢 K1，都不足以回答相对冻结原 actor 是否值得介入。

## 证据边界与来源

本轮 scientific generations / environment operations 均为 0。累计仍为 5142 /7949（含 reset）；这是物理实验成本，不与上表的策略逻辑 tokens 混用。

- 正式 summary：`6ff56b7e9bc31c29bc9afd0c3ceea43c4fdf53b2addb29d3ce9f2c5e99b5d3c4`。
- 原 branches：`eff9b5e74d3d5daa928cb662dcc59fc3f434f66796b673679d40b374f3c8636f`。
- 独立 G4 acceptance：`7331b865778481ab4e1b10943eac0e4090ea004e214dbdfff283cfbe042833e6`。
- 逐字段摘录、路径与原始值见 [observed_existing_results.json](evidence/observed_existing_results.json)。

方法参考：[Cawley & Talbot, JMLR 2010](https://www.jmlr.org/beta/papers/v11/cawley10a.html) 讨论有限样本上选择规则会造成的评估偏差；本项目据此不能在同一批已暴露结果上挑规则后再声称独立验证。[SciPy binomtest 官方文档](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binomtest.html) 给出精确二项检验定义；本文只作纸上概率解释，没有执行新的检验。
