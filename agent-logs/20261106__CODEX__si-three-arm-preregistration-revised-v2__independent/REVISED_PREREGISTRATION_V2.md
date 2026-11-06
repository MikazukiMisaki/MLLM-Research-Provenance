# 三臂 bounded-recovery 开发可行性：预登记修订草案 v2

**DRAFT / NOT FROZEN / NOT EXECUTION-READY。** 本草案明确选择下述单一候选设计供独立复核，并非已实施协议、执行入口或启动放行。模型、环境、数据来源、完整资源预算与独立任务保管均未证实。候选涉及最多 4 个自造开发组；不声称 held-out、一般 ALFWorld 泛化或成功率提高。不增加 selector、DPO、多轮反思、其他环境、SFT 训练或新科学结果。

依据和不可变来源：前一稿 `REVISED_PREREGISTRATION_DRAFT.md` SHA256 `54597050a013166b8fb872324aecaa828741960d9c6d2f89b5bd4e144b0ae79f`；其独立审查 `INDEPENDENT_REVIEW.md` SHA256 `b236590b87e64e77b414834c286c6a9516a60ed03b2eb07264a570efcbe0f8e9`；空诊断三值补充 SHA256 `649f0313cd60bb3ba92ca3166bd9702cb2baecd26a904c4cc0d90806e93f68b6`。本稿不修改这些文件。独立审查基于已有代码作静态评估，不是未来具体实现的认证。

## 1. 研究问题和 policy 身份

同一已记录来源前缀下，对比：A) SFT-P0 原始续跑；B) 冻结两阶段 recovery 后回到 SFT-P0；C) 同次数字面调用、屏蔽生成诊断/子目标文本并放入固定占位符的 recovery 信息消融，然后回到 SFT-P0。`B−A` 是完整干预与普通行动的操作性差异，调用数和可能的模型身份不相等；`B−C` 是诊断及子目标文本相对占位符的联合差异，保留 stage-1 状态信息，也不等于只识别诊断质量或精确匹配实际算力。该候选仍需生产代码实现与审查。

| 角色 | 候选明确身份/输出约束 | 解析与完整性 |
| --- | --- | --- |
| A 来源/普通续跑及 B、C 后续动作 | **SFT-P0**，指定的 Qwen 基础模型、LoRA adapter、SFT-P0 prompt/策略，历史 actor `max_new_tokens=16`，身份、适配器加载方式、decode 参数与哈希执行前精确绑定 | 历史 `SFTP0QwenPolicy` 对解码文本使用 `parse_p2_selection`，依据**最后非空行**，可接受前面文本；所查看路径没有与 recovery 相同的 EOS/completeness 拒绝闸。必须记录原始输出、token 数、EOS/cap/completeness 可观测值（无法确定则 UNKNOWN）、原 parser 与动作映射；不擅自新增截断拒绝规则。 |
| B/C stage 1 | 未适配 Qwen recovery 后端，固定 stage-1 prompt/参数，贪心，历史输出上限 **40** | 保留原诊断/子目标解析状态、raw 输出与 completeness；即使 stage-1 历史 invalid，正常控制流仍执行 stage 2。 |
| B/C stage 2 | 同一未适配 recovery 后端及固定 v2 stage-2 构造/参数，贪心，历史输出上限 **16** | 全输出严格 bare-ID、完整性检查和唯一映射；与 P0 的最后非空行规则不同。仅两阶段都按历史规则合法且 grounding 唯一时可选动作。 |

历史 H4 baseline actor 上限 **32**、其 actor policy/提示接口与 SFT-P0 actor 的 16 不是同一身份；不得以 32 调用冒称 P0。该表是拟绑定的精确契约，仍需核验实际配置、代码、input tensor、设备与模型真实路径，不能从静态审查推断当前可执行。若提出任何新的截断/拒绝规则，必须作为改变科学执行语义的版本及额外审查，而不是悄悄替换历史接口。

## 2. 分组、前缀与三臂操作

固定允许来源与可复核的自造 case 版本：在任何结果之前预登记具体祖先/相似性判等、生成器与源码、分组规则、case 哈希、配置和固定环境初始化身份，选定四个不同**具体谱系组**并锁定顺序。共同公开 domain 或抽象 family 不自动构成具体重复，也不证明真实独立或历史未暴露。四个合格组、独立保管、未知历史/预训练不重叠均尚未证实；不足时停止，不访问受保护任务补数。

来源 SFT-P0 最多跑四个 episode，各在固定 `r=1`——来源首个动作完成之后、下一个动作之前——判定可否分支；不根据动作好坏、模型信心或之后的成功与否选位置，也不替换任务/种子。保存初始版本/参数、原始动作、观测、提示上下文、历史、ordered valid actions 与 action-ID map、可公开核对的环境状态和可用哈希。B/C 各 reset 一次，重放真实已保存的首个动作，验证相同公共状态、动作映射、请求和版本后才生成；不可观测隐藏状态始终 UNKNOWN，不声称完全等价。

A 复用原 episode 在分支点的自然后续，不额外重跑。必须独立验证原记录完整且复用不改变纳入；否则先修订预算/协议，不得现场另跑。原来源可能在 branch 前已自然终止或不能产生首个动作，不产生 B/C；这属于事先定义的操作状态，不代表该任务必然失败。若来源达到分支点，不论 A 后续结局如何，都按预先计划运行两臂，除非技术 STOP。组 1/3 的 B→C，组 2/4 的 C→B；A 始终在两臂之前，因此残留时间/顺序偏差并不消失。独立审查须确认实现确能不因看到 A 结局而挑选案例。

### 单一候选：OSR 式手回规则

B/C 各运行一次原始 stage 1 与 stage 2；stage 1 即使历史 invalid 仍调用 stage 2，除非之前出现技术错误。若历史 stage 1、stage 2 与 action grounding 都合法，则最多执行一个模型选定动作并手回 P0；若任一历史规则 invalid 或选择/grounding 不合规则，不执行干预动作，从该状态按同一 P0 续跑。重复或变化的行动映射若妨碍确认实际命令，则作为无法证明的技术 UNKNOWN，停止整个研究，而不是改作普通 handback。该 OSR 规则是本版**选定的候选**，与某些旧 R4 的 invalid 即中断规则不同；尚未绑定 reviewed implementation，不能冒充历史所有运行均有此语义。不得因输出好坏修改规则、重试或额外生成。

每个重放分支从初始状态总环境步数 `r+a+c<=50`：`r=1`；`a=1` 表示实际干预动作、`c<=48`；`a=0` 表示无动作手回、`c<=49`。来源 A 从初始状态总计不超过 50 步。每条调用/动作及提前终止单独记录；不允许重放额外增加 horizon。

### 诊断信息消融候选

两臂执行同一 stage-1 prompt、recovery 后端及 40-token 上限，并各自记录输出、解析状态、实际 tokens。B stage 2 正常接收其历史 parser 解析的 diagnosis/subgoal；C stage 2 在历史 stage 1 `valid` 时以事前固定占位文本替代其内容，在历史 invalid 时与 B 一样使用冻结 invalid marker。占位符提议为 `No diagnosis provided.` / `No subgoal provided.`；确切编码、parser、构造器与置入 `stage_one_valid` 的调用方式须在候选实现中冻结并独立测试。不得将 C 生成的诊断文本或其推断的动作传入 C 的 stage 2、动作历史、环境或后续 P0；但共同的 valid/invalid 状态会影响 marker 与手回，故**status bit 仍有信息**。占位符和 prompt token 长度本身可能影响模型，不宣称移除全部 stage-1 信息或匹配 FLOPs。

两次独立实际生成即使 greedy、请求相同也可能产生不同输出或状态；预设在不违反技术契约的情况下不因此停止、不按观察值排除，保留各自完整状态及配对比较，将差异作为实现/运行变异说明。不能保证共享随机流、模型内部状态、实际 token、耗时、显存或能量一致。若输入/环境映射、物理调用或绑定不一致而不是普通模型输出差异，则 UNKNOWN/技术 STOP。

## 3. Nonempty 标记：观测而非 gate

不改历史 parser，不修补历史或本次 raw 输出。对 B/C 自己的 stage-1 结果对称计算 `diagnosis_nonempty`、`subgoal_nonempty` 与 `semantic_nonempty`。前两者仅当原生成完整、历史解析正常返回且对应字段为 Python `str` 时，以固定 Python 版本 `len(value.strip())>0` 记录 TRUE/FALSE；不完整、无返回、异常、字段缺失或非字符串记 UNKNOWN。联合字段有任一 FALSE 为 FALSE、两者均 TRUE 为 TRUE、其他 UNKNOWN。该名称仅指字符串非空，不代表语义有意义、与动作一致或正确；Unicode 不可见但非 whitespace 字符可能仍判 TRUE。

历史 `stage_one.status` 原样记录并控制既有行为；例如原 parser 将空白 diagnosis 判 valid 时，B 仍照原样传输并可能选动作，C 仍按历史 valid 置占位符；不由 nonempty 改变提示、拒绝或排除任何一臂。记录 raw output、completeness、parser status、两个字段、词数与各三值指标；持久化失败是技术 UNKNOWN。按每臂与配对报告 valid+FALSE、invalid 和 UNKNOWN；任何仅限 both-TRUE 的事后子集是描述性敏感性展示而非主估计。

## 4. 分类、先错停和验收

固定各来源状态互斥区分：`SOURCE_TERMINAL_BEFORE_FIRST_ACTION`、`SOURCE_NO_LEGAL_ACTION`、`SOURCE_P0_ACTION_WITHHELD`（原 P0 parser 无有效唯一动作或无法落地，但外部操作/记录可靠）、`SOURCE_TERMINAL_AFTER_FIRST_ACTION`、`REACHED_FIXED_PREFIX`。无可判状态、部分调用或无法区分以上状态为 `TECHNICAL_UNKNOWN`。候选明确：P0 parser 无动作时该 episode 以 withheld 结束，不擅自执行动作、不生成重试，不自动写成任务成功或任务失败；此 episode 包装语义与历史运行的等价性尚待核查。后续 P0 无动作亦按同样的 `P0_ACTION_WITHHELD` 终止该臂。自然达到明确环境成功、明确终止未成功、耗尽 50 步未成功、invalid/withheld 各自保留；UNKNOWN 不填 0 或 1。

stage invalid 是在收到真实返回、完成解析和证据持久化后依 OSR rule 无动作手回的**操作结果**；进程异常、超时、回执丢失、解析器崩溃、状态/map 无法核实、持久化失败或可能仍运行的外部操作是技术 UNKNOWN，立即停止整个研究的后续科学调用，不 retry、不补案；必要安全清理仍须进行并留证。每次实际/可能外部开始、返回、失败、open 未决和清理单列。

报告四个已分配组的状态、三臂配对是否完整、每个可判单元的原始结局和 B−A、B−C，以及成功/失败/withheld/UNKNOWN/未执行分母，不以三臂完整子集冒称总体。候选工程可行性门槛：四组均到达固定前缀、三臂均按规则完成且证据账本通过；自然不合格造成不足记 `FEASIBILITY_INSUFFICIENT`，技术 UNKNOWN 则 `TECHNICAL_STOP`，均不替补。即使通过也仅说明这一开发路径可执行；四组不支撑统计显著性、精度或 Phase 2 科学有效性。

## 5. 候选计数上界与未知完整预算

条件：四个来源 episode ≤50 步；每个 B/C 各重放 1 步，再按 `a+c<=49`；无额外 P0 生成、模型重载、重试或回合。生成数在无效手回且有全部续跑时取上界，绝非预测均会发生。`PRECALL` 已持久化而实际调用未证实的操作按保守预算消耗/OPEN_UNKNOWN，不伪称物理执行或零成本。

| 部分 | reset starts | 物理 step starts | P0 生成 starts | stage 1 | stage 2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 4 来源（含 A） | 4 | 200 | 200 | 0 | 0 |
| 4 B 分支 | 4 | 200 | 196 | 4 | 4 |
| 4 C 分支 | 4 | 200 | 196 | 4 | 4 |
| 合计 | **12** | **600** | **592** | **8** | **8** |

`reset+step<=612`；总生成 starts `592+8+8=608`。在真实执行版证实 SFT-P0 输出实际上限为 16，stage 1/2 分别为 40/16 的条件下，输出上界 **`592×16 + 8×40 + 8×16 = 9,920` tokens**。此前以 actor 32 得到的 19,392 是更宽的保守数，不是 SFT-P0 的真实配置。若每次实际送入 generate 的 tensor 均经验证不超过候选 4096（无任何截断/改 prompt），输入上界 `608×4096=2,490,368` tokens；这些不是已观测值。CPU 预分词不能单独证明 GPU 所用输入 tensor 一致；无法实时核验则不得把该上限声明为已实现。实际 tokens、stage 状态与输出可在异常时 UNKNOWN，不因上限得出实际费用。

另需独立记录并限制：最多 12 次环境 construct/load/reset/常规 close 的候选 start；replay；P0 底模加载、adapter 加载/attach、未适配 recovery 后端加载（分开且失败留账），tokenizer/template；翻译/编译及后代进程；CPU/GPU/显存/时间/磁盘、监控、输出/日志、异常清理和既有累计成本。两种模型/适配器是否可常驻、实际是否只需两次底模加载以及 GPU fit **UNKNOWN**；若实际要更多加载，修订协议和预算，不可现场加额。需要有可测 admission 阈值、截止、异常清理和资源 UNKNOWN 规则，不能把本表称为完整物理预算。共享 GPU 利用率、他人资源及不可见子进程须据观察诚实记录；有限采样不是进程树硬上限。

## 6. 与 SI-U1 self-improvement 主线的关系

本方案没有训练或测试更新后的 policy，不能声称 self-improvement、训练效果或成功率提升。最多产生需进一步核实的**候选**学习样本：允许来源的公共 pre-decision 状态/历史、唯一环境 grounding 的实际选中动作和观测后继，及模型/干预、原始 parser、token、事件链。单步有返回、后缀成功、相对 C 的差异都不能单独证明动作有益；后续 P0 行为构成归因混淆。无效/withheld/UNKNOWN、失败或不可验证的内容不可默认为正监督标签。

在任何训练之前，必须另行冻结可独立复核的动作/状态/后果学习目标、质量规则、选择机制、标签不确定性、任务谱系及重复检查；规定无需依赖未来 outcome 或明确登记允许的后验来源，提供相同质量和接触预算的恰当对照，说明实际可获得的合格条数。不足时停止而非把脚本或无关成功路径改名为自生成改进。训练、隔离评估与统计精度是独立方案，不含于本预算；不能假定上述四组可以支持它们。

## 7. 未决与非运行下一步

1. 独立审查 exact-SHA 的 P0/recovery 两后端、adapter、提示、parser、generation/grounding、OSR 语义和占位接口；为 historical valid+空诊断、truncated-but-nonempty、stage1 invalid 仍生成 stage2、状态信息泄露、重复映射、掉电与账本缺口提供 synthetic 测试。当前 matched arm 尚未经过真实生产实现审查，入口必须保持禁用。
2. 证实四个允许来源的开发组、语义可达性、生成规则、具体谱系和冻结顺序；未知独立性与 custody 保留 UNKNOWN。不得打开受保护内容或将 schema 校验当作真实独立性证明。
3. 明确模型及 adapter 真实加载策略、完整预算、共享 GPU admission、实际 tensor token 测量、环境 wrapper/翻译工作、完整累计成本及真实 receipt/恢复边界，复核先错停/no-retry 与善后。
4. 独立审查修订和恰当的数据目标；只有全部证据与 exact-code 达到条件后，协调者才能作事实性的工程 release。用户已有授权不需被重复索取，但本稿不等于这些先决条件已满足。

## 相对 v1 的具体修订

不改动 v1 字节：本稿将 SFT-P0 actor 从模糊的 H4/P0 区分为历史 16-token/最后非空行接口，将 H4 32 仅列为不同基线；将 recovery stage 1/2 分别固定为候选 40/16；明确 stage-1 status 信息仍存在于信息消融、无效仍做 stage 2 与单一候选 OSR handback；补充不改变历史 parser 的 tri-state nonempty 观察；分开来源无动作、自然终止与技术 UNKNOWN；将输出上界从宽松 19,392 修正为条件性 9,920，并把 adapter 和底模载入独立记账；增加 SI-U1 学习目标和训练效果的边界。原始组数、先定 r=1、先错停/不重试、不补案和非 held-out 限制均保留。
