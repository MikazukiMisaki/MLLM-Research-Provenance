"""Write SI-P0 audit/design prose from existing audit metadata only."""
import datetime
import json
from pathlib import Path


def write_deliverables(ns):
    own=ns['OWN'];inv=json.loads((own/'experience_inventory.json').read_text());st=inv['stage_summaries']
    def put(name,body):
        (own/name).write_text(body.strip()+'\n')
        print(name,(own/name).stat().st_size)
    stage_table=['| 历史证据 | 状态数 / canonical tasks | CONTINUE 成功 | 处理成功 | rescue / neutral成功 / neutral失败 / harm |','|---|---:|---:|---:|---:|']
    for k in ['SPRINT2C','R4','R10_OSR','R11_PBR','R16_OSR','R17_PAR','R18_C1','R18_C2']:
        r=st[k];c=r['labels'];stage_table.append(f"| {k} | {r['rows']} / {r['canonical_tasks']} | {r['continue_successes']} | {r['treatment_successes']} | {c.get('ACTUAL_RESCUE',0)} / {c.get('NEUTRAL_SUCCESS',0)} / {c.get('NEUTRAL_FAILURE',0)} / {c.get('HARM',0)} |")
    for k in range(1,6):
        r=st['R19_BRANCHES'];c=r['labels_vs_continue_in_eligible'][str(k)];success=c.get('ACTUAL_RESCUE',0)+c.get('NEUTRAL_SUCCESS',0)
        stage_table.append(f"| R19 K{k}，eligible | 36 / 36 | 30 | {success} | {c.get('ACTUAL_RESCUE',0)} / {c.get('NEUTRAL_SUCCESS',0)} / {c.get('NEUTRAL_FAILURE',0)} / {c.get('HARM',0)} |")
    source_table=['| Source | 已完成 episode / canonical tasks | 普通自身成功 episode | 提示与 raw output | 动作映射绑定 / decisions | 已记录 input tokens 范围 |','|---|---:|---:|---:|---:|---:|']
    for k in ['SPRINT_SOURCE','R1_SOURCE','R7_SOURCE','R14_SOURCE','R19_SOURCE']:
        r=st[k];e=r['structural_evidence'];tok=r['recorded_input_tokens'];source_table.append(f"| {k} | {r['rows']} / {r['canonical_tasks']} | {r['observed_source_successes']} | {e['prompt_present']} / {e['raw_output_present']} | {e['selected_id_maps_to_executed_command']} / {e['decisions']} | {tok['min']}–{tok['max']} |")
    rescue_table=['| 阶段 / 处理 | 实际 rescue prefix IDs（相对同前缀 CONTINUE） |','|---|---|']
    for k in ['SPRINT2C','R4','R10_OSR','R11_PBR','R16_OSR','R17_PAR','R18_C1','R18_C2']:
        rescue_table.append('| '+k+' | '+', '.join(st[k]['actual_rescue_prefix_ids'])+' |')
    source_refs=[]
    for k in ['SPRINT2C','R4','R9_CONTINUE','R10_OSR','R11_PBR','R15_CONTINUE','R16_OSR','R17_PAR','R18_C1','R18_C2','R19_BRANCHES','R19_SOURCE']:
        path=ns['STAGES'][k];binding=next(x for x in inv['input_bindings'] if x['path']==str(path));source_refs.append(f"- `{k}`: [{path.name}]({path})，{binding['bytes']} bytes，SHA256 `{binding['sha256_before']}`。")
    ownref=str(own)
    feasibility='''# SI-P0 自身经验可学习性审计

任务 SI-P0-SOL-b1c48c；只读历史证据与纸上设计。状态：提交协调方独立审阅，非 review PASS。

**DATA_FEASIBILITY = READY_FOR_PROTOCOL_DESIGN。TRAINING_DATA_READY = NOT_READY。新训练、采集及科学执行 = NO_GO / NOT_GRANTED。**

这里的 READY 只表示已能写出可被反驳的协议草案：确有可追溯的同前缀救回记录，也有普通自身成功和伤害对照。它不表示已经拥有合格训练集、足够独立任务、学习增益或统计功效。当前最有价值的交付是来源与缺口清单，不是启动一轮训练。

## 1. 证据与身份边界

OBSERVED：审阅根为 `/home/lizening/wt-codex-r18c2`、`agent/codex-r18c2`、`e537f441010077123a307e9d50ea40cf8dad8547`，开始时干净。冻结 analyzer 树为 `85cbb92395e5e2420c2adeb1fa0634653e742910`；已执行正式 G3 的 source SHA 为 `2da980f631badc25086d12db60d128ff507d3ae6`。本轮不改这些树。

Sprint 2C 的 actor 是未适配 Qwen/Qwen3-8B H4，后续 source/continuation 是冻结 SFT-P0，adapter 目录身份为 `6e403d85b150a74dfcc176f1f180ce4baf6fdacd922d2f96b3ceef0a21100f11`。恢复生成来自未加载该 adapter 的同家族模型；这是系统自身生成经验，但恢复目标不全由 SFT actor 自己生成，不能称为纯 SFT 自采样。

历史 Sprint/R4/R7/R12/R14/R16–18 manifest 记录 model ID、代码 revision、adapter 身份与部分隔离证据；**历史 base weights 的 resolved revision 仍 UNKNOWN**。代码 commit 不等于模型权重 revision。R19 才明示固定 `b968826d9c46dd6066d109eabc6255188de91218`；不能用它倒填历史。R19_PROTOCOL 也明确了这项历史差异。

原先专家 SFT 的 1074 train /126 validation tasks 是专家策略生成的监督模仿数据，另有 60 个 online identity 元数据。它们不是 self-generated 候选。本轮只读 accepted split 的身份条目，没有读取专家训练内容或未消费 reserved/held-out outcomes；其原始训练审计由协调方另行负责。

## 2. 普通自身成功与实际增量分开

OBSERVED，下表是已完成历史记录的直接计数。success 使用原记录最后一步 done 且 reward>0；不把局部 subgoal 完成当终局成功。不成功项不自动解释为环境任务失败，例如 Sprint 有 6 个 selection_failure。

SOURCE_TABLE

Source 成功为普通自身成功候选，不是 rescue。后续 CONTINUE 常复用 source suffix；不能把两份证据重复当两次经验。所有 horizon 固定为 50；前缀的剩余额度见逐条索引。

STAGE_TABLE

neutral成功/失败分列，避免把“恢复后也成功”误称“恢复造成的成功”。以上是不同 actor/处理/分层样本的描述，不能跨表求一个自然 recovery 成功率。本轮没有重新计算检验、置信区间、oracle 或新策略效果。

RESCUE_TABLE

R12 是对 R8/R9/R10/R11 的机制审计，新增 episode 为 0。R11 的 6 次相对 CONTINUE rescue，不等于相对 OSR 的 6 次增益；正式报告只记录 PBR vs OSR 的 1 win /3 losses。R17 的 5 次相对 CONTINUE rescue 同样不等于 5 次相对 OSR 的增益。

### R19 原件中两次 K2 实际救回

原始 branches 文件 SHA256 `eff9b5e74d3d5daa928cb662dcc59fc3f434f66796b673679d40b374f3c8636f`；下面两行的 CONTINUE=0，K2=1，均来自 failure 队列。row SHA256 包含原 JSONL 行末换行；完整事件引用见 `evidence_contracts.log` 和 inventory。

K2_DETAILS

R19 实际为 127 source、39 attempts、36 eligible、183 个逻辑 K arm；3 个不合资格初始 attempt 独立保留，不能静默并入 eligible。K3/K4/K5 分别有 4/4/3 个 derived alias 记录；它们不是新增独立轨迹，且每 K 自己的逻辑费用不能替换成 alias 来源整行费用。

另两例 `R19-random-control-8ec4fc037229710f8f13`（10000）和 `R19-random-control-bf448be94724da4562c0`（00001）是原正式结果的 oracle-over-K2 分解。两者 CONTINUE=1，**不是相对 CONTINUE 的新 rescue**；原 passive 诊断均为 UNSUPPORTED / 全 j UNKNOWN / COVERAGE_ONLY / selected_k=5，estimated_success/cost=null。不能把它们事后改成选择标签、把 UNKNOWN 补成策略效果或改变原 fallback。正式 oracle headroom 2/36 不能充当学习收益估计。

旧失败 G3 `3d1ccea7e97f4727abf8e216ac6ec498` 原 manifest 仍为 RUNNING 快照，唯一 source unit 为 in_progress；只有 1 次 generation、1 次 reset、0 环境 action、0 完成 source，branches 为 0 bytes。它是未完成 unit，不是任务失败，也没有训练目标。原件保持不变。

## 3. 去重与数量能说明什么

OBSERVED：Sprint 的 120 states =79 episode groups =73 canonical tasks；200 source episodes 本身只有124个 canonical tasks。R4 的24 states来自23 tasks；R8/R9/R10/R11 的48 states来自47 tasks。`R8-F22`、`R8-F23` 是同一个 Book/DeskLamp trial 的两个前缀，不是两项独立新任务。

R15、R16、R17、R18-C1、R18-C2 的60 prefix IDs及 `(canonical task, decision index)` 集合完全相同。处理变化不能把60变成240。R19 eligible为36独立 canonical trial；不能把120+36称为156独立训练样本，也不能把5个相关 K端点或 alias 当新训练任务。

在本次列出的所有处理里，已观察 rescue 的 canonical task 并集仅 **17 tasks /18 states**，跨多个基座、operator及信息处理，是审计上界，不是清洗后样本量。若仅保留 post-SFT 单动作 R4/R10-OSR/R16-OSR/R19-K1，只有 **11 rescue states /10 tasks**；11个记录中7个属于 light，另外 pick_two 2、heat 1、pick_place 1，未覆盖 clean/cool。把多步 K2 或最佳 K 合入，会改变处理定义，不能悄悄扩大这个单步池。

各 source cohort 在所读 canonical game/trial 元数据中互不重叠；已列 cohort 与 accepted expert split 的匹配重叠计数为0。这个结论仅限明确哈希绑定的这些身份清单，**不是全项目、所有旧审计或尚未消耗 reserved identity 的完整排除证明**。同场景不同 trial 也可能语义近似，exact identity 去重不保证场景泛化。新任务总量和可用于独立评估的身份全集仍 NOT_PROVEN，不能从134−60推导。

## 4. 可学习性：可追溯不等于可直接训练

OBSERVED：Sprint/R4/R10/R11/R16/R17/R18 中恢复 Stage2 的 prompt、raw output、临时 id_to_command 都可定位，已记录选择的 ID 与对应 command 在结构核对中一致。Stage1 无效仍可能留下 Stage2 生成；**生成存在不等于动作执行或可采纳**。原 fail-close 不能因训练选样而消失。

R19 有4965条 completed generation证据，其中39 Stage1、172 Stage2、2046 source actor、2708 suffix actor；4965条都含 prompt/哈希及 raw output，4926条 action generation 有当时 map与选中 command 的直接绑定；39个 Stage1 不是 Action-ID目标。5796个 K分支引用事件 ID在原事件文件中均能找到。这只是字段与来源核对，不是重跑项目完整性 validator，也不是重新签发原审查。

Sprint source/R1/R7 旧 schema 没有独立 `result_observation` 字段；不能把旁边文字未经时间语义审查就当作动作后的 transition。已有 replay/branch证据可补来源定位，但不应凭空制造最后一步反馈。R14/R19 有显式 result_observation。逐个训练输入的因果时点、末步反馈和公共输入投影仍 NOT_PROVEN。

INFERRED 的必要数据约束：

- 学生输入只准原 SFT-P0 的 task goal、当前 observation、已发生的 H4 transitions、当时动作排序/map；先输入后目标。当前动作结果、最终 reward、CONTINUE/recover label、未来位置、K结果、oracle及事后机制归因不能进输入。
- 目标必须来自实际模型 raw output并绑定同一时点 map和实际执行。相同 A003 在另一时点可能是另一命令，不能跨状态搬用数字。不得从专家计划/hidden facts改写一个看似正确的目标。
- 恢复 Stage2 看过模型生成的 diagnosis/subgoal；PAR/FACT/CARD另有输入处理。直接拿这些恢复 prompt训练 action-only actor会改变部署接口。将一个已执行恢复 action投影到原学生公共输入，是尚未验证的蒸馏步骤，非现成训练样本；不能把 Stage1 rationale一并当优质目标。
- R18-B原冻结报告标明 FACT/CARD-v2来自公共历史且无 hidden/future leakage；本轮没有重做语义验证。不能把“facts”一概误标为泄漏，也不能将 v1的已知语义缺口偷偷用v2修好后当作原模型所见。保留各自真实 treatment，单独审查，当前单动作主草案不混入这些处理。
- rescue只说明这一组合干预加后续 SFT 在该原前缀的已观察终局增量。它不证明 diagnosis真实、每个 action必要、suffix全值得模仿，或换任务后仍有增益。Sprint P033虽最终救回，正式报告明确其subgoal/action不一致，足以反驳“成功即全部推理正确”。
- incomplete、未执行/失配目标、不可追溯输入、模型可见 hiddenfacts、专家目标或未来信息进入输入均不得采纳；其他未证实项先隔离，不能默认合格。neutral成功可成为普通成功对照，不能伪标rescue；harm保留于审计和费用，不作为正样本。

只使用已记录 token统计；未加载 tokenizer。表中原 prompt长度不是未来公共输入投影后的精确长度，更不是独立任务数。大量 source success有助于普通成功基线，但没有改变 corrective任务少、light集中和未知历史权重的瓶颈。

## 5. 最大可支持主张、否决条件与待澄清项

OBSERVED 最大主张：项目确有模型自身生成、同前缀已测 continuation对照和正负终局的证据，可形成不含训练内容的候选索引；可提出一次性、可否证的经验采纳 SFT设计。

NOT_PROVEN：合格 corrective dataset、可训练 token预算、最小有意义效应、足够新任务、generalization、自改进闭环、paired标签本身的独立机制优势或创新首创性。历史专家 SFT改善不能补足这些主张。

目前对科学执行默认 NO_GO。下一次若继续，先由协调方审阅本索引和设计、决定是否值得授权公共输入/目标投影的逐条证据审查；它仍不同于训练或新采集许可。若去重/排除/时点审查后没有足够且可信的纠错多样性，结束该候选，不为凑positive补采、拼 K、训练selector或以重复episode冒充独立任务。

具体待决证据问题：历史resolved weights能否由当时原始记录证明（否则只保留UNKNOWN或隔离）；旧schema transition语义能否按原件定位；可用独立 TRAIN身份全集是否完整；单步corrective数据经严格投影后还剩多少任务/token。缺少这些答案不阻碍交付草案，但阻碍可执行协议与资源批准。

## 6. 原件、费用与复核入口

审计 inventory小于1MB，候选只含ID、来源、行哈希、既有终局和结构标记，不含训练 prompt/target。每个输入的 before/after SHA在 `experience_inventory.json.input_bindings` 和 `INPUT_HASHES.sha256`；本轮所有这些输入均未变。

R19 campaign累计仍为 **5142 generations /7949 reset-inclusive environment operations**，已包含177/342历史开销；本轮新增科学调用0。这不是全项目成本，专家SFT训练和历史其他阶段费用另计。原始大raw树、weights/adapter/cache/dataset未复制。

SOURCE_REFS
'''
    details=[]
    for r in st['R19_BRANCHES']['actual_K2_rescues']:
        details.append(f"- `{r['prefix_id']}`，原JSONL第{r['source_line']}行，`{r['canonical_task']}`；row SHA `{r['source_row_sha256']}`。K2为2次recovery action后接{r['sft_environment_actions']}次SFT action，SFT终局 environment_terminal；arm event `{r['arm_event_id']}`。")
    feasibility=feasibility.replace('SOURCE_TABLE','\n'.join(source_table)).replace('STAGE_TABLE','\n'.join(stage_table)).replace('RESCUE_TABLE','\n'.join(rescue_table)).replace('K2_DETAILS','\n'.join(details)).replace('SOURCE_REFS','\n'.join(source_refs))
    put('SELF_EXPERIENCE_FEASIBILITY.md',feasibility)
    put('MINIMAL_SELF_IMPROVEMENT_PROTOCOL_DRAFT.md',r'''
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
''')
    put('INNOVATION_COMPARISON.md',r'''
# SI-P0 创新边界：指定三项primary文献

状态：有限范围方法对照，**NOVELTY=NOT_PROVEN，EFFICACY=NOT_PROVEN**。本轮只读论文，不复现、不运行作者代码、不扩大文献范围。

| 工作 | 经验及增量信号 | 学习/写回与运行时作用 | 新任务证据边界 | 对本候选的约束 |
|---|---|---|---|---|
| [Re-ReST, EMNLP 2024](https://aclanthology.org/2024.emnlp-main.861/) | actor自采样；环境评分后保留成功，reflector修正失败后再评分；正确/错误经验也用于reflector训练 | reflector与actor均可经训练更新；主设置把成功原样本及成功修正样本写入actor权重 | 论文在多个agent任务报告实验，不等于本项目新任务证据 | “反思后成功轨迹用于SFT”已存在；不能以本候选首次提出纠错self-training |
| [Training Language Agents to Learn from Experience, v1](https://arxiv.org/abs/2605.20477) | actor历史trajectory反馈给reflector；新prompt的训练奖励来自重测历史batch | 学习reflector（GRPO）；actor权重冻结，跨任务写回system prompt，非本草案actor-SFT | 方法按task type作meta-train/meta-test；ICT loop用固定验证任务选winning prompt，不能直接视作一次冻结checkpoint的确认 | 跨任务经验写回已是明确问题；本草案不同写回通道不等于创新证明，也不采用其RL/prompt搜索 |
| [When Harnesses Lose the Signal: Causal Evaluation of Recovery in LLM Agents (CIR), v1](https://arxiv.org/abs/2610.00372) | 在同执行状态配对CONTINUE与恢复，区分rescue/harm；受控observation faults | 用paired监督训练运行时router及错误/结果模型，选择恢复；不以此训练actor动作权重 | 论文的故障/干预设定与本项目natural TRAIN执行困难不同；不能迁移数值效果 | paired增量标签并非本项目新发明；这里若有区别，是用于离线经验采纳并写回actor，而非学习runtime router |

INFERRED：本候选可检验的窄区别是：在同一固定纠错生成池中，以同前缀CONTINUE0/纠错1作为**离线数据采纳条件**，相对普通成功过滤，在等训练预算下是否改善冻结强基座的新任务表现。其两部分各有先例：Re-ReST已有成功纠错self-training，CIR已有paired recovery supervision；把二者连在一起是待验证组合，不足以宣称首创。ICT进一步表明“经验跨任务写回”本身不是新问题。

还不能声称：首个自改进ALFWorld agent、首个弱base纠正强SFT、首个增量信号、首个经验筛选、或首个因果自改进。只查三篇不能排除更直接先例；未检查所有后续版本和相关工作。尤其CIR中的rescue/harm估计依赖模型化边际概率，不能偷换为精确个体反事实概率；本项目已观测同前缀终局标签也不能证明每条纠错推理正确。

主要竞争解释及反证：

- 普通成功self-training本身就够：C若不优于B，不能归功增量采纳。
- 好处来自额外teacher、生成预算或背景样本：B必须公平可见相同生成池，B/C同训练token/steps；获取成本另列。
- 硬任务/家族或案例记忆：task级去重、新任务、受控重复；11状态/10任务的历史单步rescue不代表覆盖。
- 挑K/挑prefix/挑checkpoint：固定处理与时点、无oracle标签、单轮最终checkpoint，不能从R19最佳K倒推方法。
- teacher correction看过额外上下文：公共输入投影须诚实记录；不训练隐藏状态、事后label或rationale，未来任务表现才回答可迁移性。

已读范围与来源（2026-10-25 UTC）：

- Re-ReST：官方ACL摘要及[论文PDF](https://aclanthology.org/2024.emnlp-main.861.pdf)方法部分、自训练/reflector数据路径和部署设置；作者代码入口[PlusLabNLP/Re-ReST](https://github.com/PlusLabNLP/Re-ReST)仅核对论文官方链接，未运行或完整审阅代码。
- Training Language Agents：arXiv v1摘要、[HTML](https://arxiv.org/html/2605.20477v1)§3 ICT /§4奖励与GRPO /§5.1任务分区及§5.3验证选择限制；未复核每项附录或数值。
- CIR：arXiv v1摘要及[HTML](https://arxiv.org/html/2610.00372v1)paired干预与router方法部分；未复核全部实验/附录或运行其软件。

以上对论文内容为方法摘要，区别判断明确为INFERRED；没有论文实验的本地复现。本文不建议采用GRPO、memory、learned recovery selector或在线prompt优化，现有禁令不变。
''')
    corrections='''# SI-P0 草稿审计修正记录

这仅说明本任务纯stdlib草稿脚本的字段适配，不是科学代码bug或原证据变更。

1. 首次event schema probe查找event_type/type，原R19实际键为kind；因此schema_probe阶段的事件类别null计数没有科学含义，正确类别在r19_event_kind_probe.json及inventory_audit_final.log。
2. inventory_audit_first.log最初从payload外层找generation，因真实结构为payload.evidence.generation，把prompt/raw的存在性误记0。inventory_audit_nested_evidence和后续修正已读取真实嵌套层。
3. 后续草稿已看到actor action_map，但恢复Stage2原件使用evidence.id_to_command/action_id/command，因此先前4754的map计数仅含actor。最终按各自真实schema重数为4926/4926 action generations正确绑定，另39 Stage1不属于动作目标。
4. 两个推测的小写R18文件名检索返回工具exit=2（不存在）；随后以rg --files定位真实大写报告并成功读取。不是数据缺失、原件修复或跳过验证。

所有草稿日志保留，不覆写。experience_inventory.json最终版本与inventory_audit_final.receipt.json、inventory_summary_final.log为引用依据。未运行项目analyzer/validators/pytest，未补任何科学生成/环境调用。
'''
    put('DRAFT_AUDIT_CORRECTIONS.md',corrections)
    # Make a compact authoritative binding view without copying original data.
    selected=[]
    for x in inv['input_bindings']:
        if Path(x['path']).name in ['SOL_RESEARCH_TASK.md','summary.json','R19_OPPORTUNITY_REPORT.md','independent_G4_acceptance.json','branches.jsonl']:
            selected.append(x)
    (own/'AUTHORITATIVE_INPUT_BINDINGS.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2)+'\n')
