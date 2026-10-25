# SI-P2 同池成功对照：独立审查与研究决定

协调方 Sol。范围仅171条既有单步记录及必要的原source/replay/CONTINUE证据，不生成或训练模型。本文的最终事实以同目录 `phase2_independent_review.json` 的冻结交付绑定为准；没有独立执行许可。

**结论：B_pool 与 C 仍可区分；当前历史池不宜直接进入以普遍成功率提升/筛选机制为目标的正式学习验证。** 集合可分性通过，不等于训练数据充分。这里的NO_GO针对当前历史池的正式验证投入，不声称十个样本在数学上绝不可能学到东西，也不否定整个self-improvement课题。

## 原件与固定流程

派发前固定171-row manifest、共同质量Q_hist、Q_pin敏感性、物理去重→每canonical task一个hash anchor→exact公共输入/目标去重→B/C采纳顺序。anchor不读success值，不为保留原11正例重选；同一任务的多个prefix始终同分区。只学第一adapter-off恢复动作；adapter-on suffix只作原终局证据。

协调方另写独立stdlib审计，重新读取171行、4类source trajectory、原replay/CONTINUE及R19原始事件：完整P0动作前公共文本、H4、动作表、bare ID/parser、命令/执行、replay及原done/reward成功判据逐项核对。没有调用项目parser、analyzer、validator、tokenizer、模型或环境。读入原件before/after SHA相同，14份raw文件还与SI-P1已封存binding逐字节hash相同。

Luna的171行身份、family、d、原标签和固定anchor key另与协调方原件逐行核对。全部匹配；169个不同task都在已登记2612-task known-use union，和已登记expert_train/expert_offline_validation/online_development列表直接task交集为0。这不是全部历史prompt未训练过或候选从未被看过的证明，也不使本池成为新评估集。

## 计数：可分性确实存在

| 流程 | 行数 | 不同task | B：恢复成功 | C：恢复成功且CONTINUE失败 | B减C |
|---|---:|---:|---:|---:|---:|
| 原始parent | 171 | 169 | 99 | 11 | 88 |
| 共同质量Q_hist | 164 | 162 | 96 | 11 | 85 |
| 已证明物理重复去重 | 164 | 162 | 96 | 11 | 85 |
| 每task一个固定anchor | 162 | 162 | 95 | 10 | 85 |
| exact公共输入/目标去重 | 162 | 162 | **95** | **10** | **85** |

7行排除均有原Stage1不合法/第一恢复动作未执行证据：R10 1、R16 3、R19 3。它们不是可以修复后纳入的第一恢复动作目标。原始分支是否成功和是否存在合格teacher动作是不同问题；其中3行原字段记success=1也不能制造已执行的teacher目标。原科学成功标签保持，不改判成任务失败，不新增G3失败。

原始99是171行全范围的字段重数，含R19原ineligible条目；此前“97个成功候选”的粗算采用R19正式eligible的29成功。二者分母不同，不能将99当G4新增结果或把97解释为所有171行的已验收target数。

原11条rescue全部通过机械共同质量；同Book任务的R8-F22/R8-F23按预设hash留下F22，不回填F23。另一个同task双prefix组不属于rescue。最后是10个不同task、每task一个第一动作。

没有已证明shared第一generation event导致进一步删除；旧legacy缺事件ID时保留physical reuse NOT_PROVEN，不能宣称已证明完全无复用。exact动作相同不等于公共输入/目标重复；本流程没有为保留样本放宽去重。

## 能否构造可比对照

最终B来源数为 R4 12 / R10 24 / R16 30 / R19 29；C为1/4/4/1。C属于B，且各含C的来源×家族stratum都有足够neutral-success，使不同且来源/家族可约束的对照在**组合容量上**存在。详见 `independent_capacity.json`。

这不表示已批准95对10训练。若要同预算比较，必须预先冻结B的success-only抽样/下采样规则和实际监督token/曝光；B可以包含C，不能为了强行使训练集不同而按CONTINUE=1筛掉C。B减C是审计指标，不是给对照偷加一项增量条件。也不能把C重放约十倍当新增经验。

在二值标签下，给定B里的恢复成功，C的正增量条件就是CONTINUE失败。因此即使将来C优于B，也首先支持**基线失败感知的成功经验采纳配方**；它不能单独证明独特价值估计算法，或排除难度选择/数据组成解释。此前“固定同池预算的采纳差异”主张边界保持。

## 为什么当前数据仍不足以支撑正式方法验证

1. **监督极少**：C是10个task上的10个第一动作，不是10条完整优质teacher轨迹或大量独立纠错技能。第一动作之后的成功不使每个suffix都获得相同增量标签。
2. **覆盖集中**：C的家族为light 6、pick-two 2、heat 1、pick-place 1；clean/cool为0。五个目标命令是“go to desk 1”，其余五个各一个；共6种不同命令。这只是覆盖集中，不把相同命令误称重复训练行或据此证明无学习能力。
3. **来源限制**：主口径10个task中9个历史weights/tokenizer身份PARTIAL、1个R19有完整版本绑定。四个来源可做透明历史蒸馏比较，但不是同一个精确当前actor的自采样闭环。
4. **严格绑定更小**：Q_pin敏感性保留36个R19合格候选，B=29、C=1、neutral=28。没有通过换口径使C变大；仅一个完全绑定rescue不能承载广泛学习主张。
5. **训练/评估条件未建立**：真实supervised completion tokens、序列/EOS/曝光/T/U/recipe尚未冻结；未来评估E、来源空间、任务隔离风险和成本没有由这些计数自动确定。训练task数不是评估统计样本量；旧oracle 5.56pp和“95比10”不能证明功效。

这些是对研究投入和目标主张的审慎判断，不是发明“少于某个N绝不可能学习”的硬门槛。当前池足以作为来源可追溯的少样本候选和论文case material，**不足以据此宣布正式self-improvement方法实验就绪**。本轮没有验证学生能否拟合或泛化，也没有批准以试跑代替缺失设计。

## 两处审计口径更正

- 一条R19 neutral-success的Stage1 output_complete=true、token_cap_reached=true；原最后token是151645，原生成器允许EOS恰好在cap处，原parser以complete=false判截断。不能仅凭cap=true排除。Sol保留初稿并按冻结契约更正；这没有改规则保留C，也没有改原科学代码。原件和静态AST证据在 `cap_completion_static_evidence.json`。
- Luna原任务是身份/标签及**过滤前**anchor审计。其额外局部locator mask曾报81 PASS/90 HOLD，主要因为没有把另存的source/replay原件接入。该mask不接受为最终Q_hist或底层数据缺陷证据。原字节保留，scope addendum已明确；协调方完整原件检查与Sol的完整审计决定最终mask，再接合Luna的独立身份表。不能把三份不同scope的计数描述为原先就一致。

## 决定和停止范围

**POOL_DISTINGUISHABLE=YES；LINEAGE_REVIEW=PASS_WITH_DISCLOSED_LIMITS；CONFIRMATORY_LEARNING_FROM_THIS_POOL=NO_GO；TRAINING_EXECUTION=NOT_AUTHORIZED。**

本轮同池审计可以结案；不再为增加可用正例换anchor、把K2/PAR/cards并入、重标历史、无上限过采样或补生成至positive。保留这10个目标及85个neutral对照作审计与论文素材。

若继续以“提升agent成功率的自改进”为下一阶段核心，需要先设计**受控新经验的数据协议**：同一精确teacher/actor与task边界、第一动作粒度、包含非rescue的完整池、预设获取/验证成本和停止规则，再审查是否值得采集。当前不预设新正例配额、不自动收集，也不追加实验。论文整理可并行推进既有SFT成功率结果和恢复收益/伤害/成本的实证链。

R19累计仍5,142 generations / 7,949 reset-inclusive操作（已含177/342），本轮科学增量0。旧G2不重跑、旧incomplete source不改、G3/G4不重启。下一阶段的任何新数据/训练设计都不复用已消费clearance。
