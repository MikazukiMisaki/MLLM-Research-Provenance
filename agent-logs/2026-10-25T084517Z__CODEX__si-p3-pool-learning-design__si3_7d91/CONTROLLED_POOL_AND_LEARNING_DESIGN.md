# SI-P3 最小受控共同池与学习协议设计

状态：DESIGN_AND_REVIEW_ONLY；科学执行NOT_GRANTED。唯一推荐是**将一次固定96-task采集可执行性研究提交下一次独立审查，且只可能单独授权这一阶段**。不接受96后自动再采384、不同时打包60 dev与600评估，也不从历史池直接训练。当前训练、采集和评估均NO_GO；这是权限与未闭合工程条件，不是断言研究不可能成功。

96=6家族×16任务=6家族×4个预定d×4重复，便于一次检查公共状态覆盖、paired label产率与可配平曝光。它不是功效样本量。以下数字均是建议冻结的资源决策guard，须Sol独立审查与用户后续授权才成为新研究协议；不提供运行schedule/gate/launch argv。

## 1. 唯一采样总体、任务与动作前anchor

总体为metadata known-use差集中的TRAIN候选，拟排除已登记2612-task union及每task所有prefix/seed/alias。1141只是已知metadata差集的文件存在数，74 unseen也不是fresh证书；本设计不读未消费game/traj_data/结果，不使用官方valid_seen/unseen。历史B95/C10与严格29/1只是动机，10/169不是新产率估计，不据它预测成功或调整N。

先由独立记录者在仅身份metadata上冻结分区：每家族预留100个TRAIN评估task、10个dev task、16个采集task，分别合计600/60/96；余385不动。60只保留身份，本最小阶段dev科学调用0。每家族需至少126个合格metadata候选，当前未核验，若不足则分区NOT_READY，不能默默少取某家族、开放74 unseen或补用已消费task。正式task清单尚未创建。本设计把原480方案的“剩1个候选”改为保留385，给隔离/metadata错误留下空间，不把余量当补正例额度。

canonical task/trial是隔离单位；同task的所有seed/prefix/alias同分区。评估与采集、开发、普通成功背景S及旧expert背景不能有task交叉。房间/场景可能跨task复用；只有metadata已支持layout/group标识时才额外核对。当前不证明scene-disjoint或所有人从未浏览，未来主张限于已登记隔离、TRAIN内部新task，不能称官方held-out或未见场景泛化。

各家族按固定salt `SI-P3-acq-v1` 的identity-only hash排序选16 task；其预定rank轮转d=5,10,15,20，各4个。d是已完成source动作数，anchor是第d+1动作之前的公共状态。任务、nominal seed（建议40000+固定schedule index）、d及成本上限在任何新source/teacher结果前一次冻结；绝不先选rescue、再选可救prefix。没有动态trigger、learned selector、第二anchor或重采任务。

冻结P0每task只生成一次完整source，按原H50与fail-closed/环境终态停止。若source在d之前终止、无法到达d、动作前已经终态或map为空，登记原source结果与不可用原因，不改d、不补task、不发teacher动作。source技术中断/未完成与行为失败分开；不把未完成unit填0。source在anchor之后的正常selection fail-closed可以按原成功/停止契约记CONTINUE=0；未来终局标签只用于最后B/C采纳，不能改变anchor。

## 2. 两条可比较路径和完整生成池

固定Qwen3-8B同一snapshot/tokenizer、source及suffix相同P0 adapter（原adapter SHA见parameters），teacher用同一base而adapter-off。collector全过程不训练；所有角色、cache隔离、公共prompt/greedy/thinking=false、H4/完整有序map、40/16/16帽不调。source与teacher不是同一policy：这是同一模型家族的跨角色自生成蒸馏，不冒称当前P0自己的on-policy正确动作。

CONTINUE的Y0直接引用完整source从同一anchor往后的原suffix与原成功标签：只有source身份/公共prefix/动作map/history及reset+exact replay绑定后，才能复用该已测baseline。无需第二次source生成；其物理生成/环境操作只记一次，原suffix的逻辑cost另给引用，重放/reset照实计账。若确定性/身份链闭合不了，标HOLD，不能猜Y0或追加baseline重跑来修数据。

每个可到达anchor reset到相同task/trial/seed，原动作前prefix精确重放；一次Stage1、一次初始Stage2，遵循原“invalid Stage1仍生成一次初始Stage2但不执行动作”的顺序。两阶段都合法且Stage2 bare ID、map与命令一致才执行第一teacher动作；随后相同冻结P0接管，剩余动作帽50−d−1。只收这一个adapter-off目标；SFT suffix仅佐证原终局，不作训练目标。

首动作合法且终态允许空suffix，done且reward>0为成功，truncated不作成功。cap=true不是截断：原output_complete=true且status合法时保留，包括上限EOS；仅按原complete/parse契约处理。Stage1非法、Stage2无效/未完成、未执行动作均如实保留；不修parser、不重生、不把其他动作或suffix当目标。拟议新池为这些无有效干预的行记YT=NA_NOT_EXECUTED，不伪造0或复用Y0当新恢复测量；它们先被共同质量排除。此处是新设计的缺失语义，旧R19标签与记录不改。有效动作即使无op也消耗一步；有效分支失败仍可通过机械质量。

一次完整pool含所有96个计划slot及所有失败、终止、invalid与未生成项的去向。先共同质量Q：完整source/prefix、公共P0投影/有序map、原replay、generation完整性、ID/命令/实际transition、完整原停止label、精确model/tokenizer/loaded adapter角色和未截断训练投影；不能用是否rescue定义Q。未来tokenizer审计中的2048全序列fit规则对全池对称应用，在成功采纳前完成，超长不截断动作表、不只删C。

去重固定为认证物理event复用→预定每task唯一anchor→exact公共投影+command；无事件证据不从语义相同推物理alias，slot不回填，所有task登记已消费。相同输入不同合法命令只记录多解/信息歧义，不按终局挑目标。B/C所选24行至少20种公共projection作为覆盖guard。

## 3. B/C的代数、正确对照及可识别边界

在Q且paired两个标签已闭合的行上：

- B_pool={YT=1}，包含所有满足共同质量的teacher成功；抽样绝不根据Y0排除C。
- C={YT=1且Y0=0}，是B的子集；neutral=B\C={YT=1且Y0=1}。
- harm={YT=0且Y0=1}与failure={YT=0且Y0=0}同样留在完整pool审计及成本里。

因此在B内，C恰是“baseline失败筛选”，不是独特的反事实价值估计器。若强制B与C具有完全相同Y0失败构成，B也全是Y0=0，与C成为同一采纳类，不能再声称识别增益选择机制。反之把B改成neutral-only会故意删C，已改变success-only基线，本推荐禁止。

family和实际completion长度匹配可控制已声明的组成/监督曝光；它们不能控制latent难度、所有前缀状态、私有teacher条件，也不能使单次paired rescue等于期望action advantage。共prefix控制初始公共状态，单个greedy/P0suffix结局仍只提供一次既有运行的标签；不从该0→1直接推出可学习、可泛化或新策略收益。

未来若通过数据/曝光审查，C按每家族固定hash取4（总24），不按收益大小或command挑选。B从同一完整B_pool按“家族×C所选实际监督completion长度（含EOS）”的计数构成，用独立固定hash单次抽24；所有C保持可被B抽到。报告B∩C、B中neutral数及全部cell数量。抽完若B没有任何neutral，或两臂训练新例完全相同，比较NO_GO；不重抽、不换seed、不把C从B移走。这个停止条件限制本次单次抽样的可解释性，不能包装为无条件随机success-only训练已确认有效。

## 4. 一次性可执行性/投入门槛

只在全部96 slot完成原定义source流程并封存后审查一次；不看中期效应加样、选family、改d或改hash。以下全部满足才是“可进入下一次学习设计审查”，并不是训练GO或自动授权：

| 资源guard | 建议值 | 理由及限制 |
|---|---:|---|
| 完整计划slot登记 | 96/96 | source正常早停仍完整登记；技术missing不伪造失败 |
| Q有效paired targets | ≥72/96 | 至少75%预算转为可追溯机械经验，非置信/功效门槛 |
| 每family Q有效 | ≥10/16 | 避免整体通过掩盖某family失效 |
| C | 总≥24且每family≥4 | 支持预设4/家族、不重复的24个新监督例；不是普遍最低学习N |
| neutral | 总≥24且每family≥4 | 同pool真实success-only对照有支持，B相应≥48 |
| 错命令、泄漏、role/pin/replay不一致 | 0 | 这些是完整性问题，发生即停止、封存，不能清洗成更好pool |
| 新例公共projection覆盖 | B24、C24各≥20 | 防止名义task数掩盖几乎相同公共输入 |
| 单次B抽样存在neutral且不与C完全相同 | 是 | 无可区分对照则停止，不允许重抽改善contrast |
| 工程曝光核对 | 全闭合 | 实际token、mask、EOS、初始化、更新尚未测，当前阻断 |

门槛是预先约定的资源/主张决策，不能说23个例子不能学习。未通过则本96协议NO_GO并封存，不自动采384或凑C quota。通过也不说明有效，只说明值得提交另一个有清楚预算的学习任务。coverage不足时只能收窄描述范围；不能当场改全家族门槛继续跑。

## 5. 条件性最小A/B/C学习控制（尚未获准）

A是不更新的原P0。B、C都从同一原P0 adapter字节warm-start，相同冻结base/tokenizer；分别训练S120+B24、S120+C24。S固定为已消费的原expert_train中120个不同task、每家族20个、每task一个既有合法动作pair，经先前质量/共同token-fit审计后在新pool结果前按固定hash选anchor；不使用expert validation或新eval。S与新任务无交叉，两臂S的行、顺序/权重均同。S用于有限约束旧成功行为漂移，不保证保留能力；无S-only第四臂，所以C>A单独不能分离背景额外更新，C>B才控制共同S。最小方案不增加D臂。

每臂144个不同task例、每epoch各一次、2 epochs、effective batch16（microbatch2×accum8），恰18个optimizer updates；每个新task总曝光2次，不能将重复曝光算作新增样本。沿原数值recipe：lr1e-4、AdamW fused、cosine、warmup .03、weight_decay0、clip1、bf16、LoRA r32/alpha64/dropout.05/all-linear、seed/data_seed42、packing=false、completion-only。只取update18最终checkpoint，不按dev、validation loss或eval表现挑选，不增epoch使C看起来学会。

目标是source动作前P0公共goal/obs/H4/完整原序map → 第一teacher bare ID及正确EOS。subgoal/card、teacher输出前缀、未来suffix、奖励、Y0/YT、family标签、private facts不能进入学生输入；family仅用于data组成审计。prompt/pad不进入loss，adapter-on suffix不进入训练。

实际token必须随后由独立工程任务用精确tokenizer/chat template测量，当前没有加载tokenizer：

- B与C按同family+实际loss-bearing completion长度配额匹配，paired batch slot长度一致，使每update/epoch的真实监督token数（包含预定EOS）完全一致。不能把Axxx字符数或原推理generated_tokens当训练token。
- 相同S、相同per-task曝光/批数/更新/LR进度；逐行记录labels≠−100、prompt nonpad、padding、processed tokens及EOS边界，检查microbatch归一化。有效batch按slot一致，不将padding冒充有效曝光。
- 真实prompt非padding总token通常不同；建议新经验部分单独、以及含S的全臂总计均满足max/min≤1.05的资源对称guard（不能让共同S稀释前景差异），仍明确这不是prompt token精确相等。原始值必须披露，超限不重抽B或调loss来通过，当前设计NO_GO。teacher prompt tokens不是学生projection tokens。
- 固定训练总长2048，完整public map和target必须fit，不截断。未来Q对全pool对称应用；S若不能闭合则先阻断，不借C结果换S。当前144×2×2048=589,824/臂只是padded序列slot宽上界，不是已测真实训练tokens或计算耗时。

现有代码不能直接当作新训练路径：`configs/sft/sft_training_protocol.json` 原prohibited含recovery/selector，旧协议未授权这些新目标；`src/sft/training.py:85+` 从base重新构建而非证明从P0 adapter warm-start，`108+`/配置按validation loss取checkpoint。未来须单独新协议/实现任务，证明初始P0参数相等、只更新预定adapter、最终18步及正确mask。当前不写trainer、不改旧config、不启动任何训练。任一不闭合、OOM/NaN/更新不符均停止且不自动重训或挑另一个checkpoint；不存在当前“token检查通过”或训练就绪声明。

## 6. 资源上限与对480/60/600的挑战

预算按“每task source最多50；teacher两次；suffix最多49−d；prefix replay d；source+teacher各一次reset”做纸上上界，不是运行计划。d均值12.5。若前述source/replay复用条件不成立，不能临时加第二baseline；应停止并另审协议。

| 范围 | model generations上限 | reset-inclusive env ops上限 | generated tokens上限 |
|---|---:|---:|---:|
| 唯一推荐96-task可执行性候选 | 8,496 | 9,792 | 138,240 |
| 不接受的480-task整体采集上界 | 42,480 | 48,960 | 691,200 |
| 后续600-task、A/B/C各一次（未授权） | 90,000 | 91,800 | 1,440,000 |

该2N-reset上界要求未来新K1单分支collector在第一动作后原地handoff给P0，无多K公共路径或额外checkpoint reset/replay；并正确更新history/动作计数。它不是现有R19多K运行器的成本或可用性证明，不能把旧G3程序直接执行后套此预算。新collector及receipt/计账须另派工程任务、冻结代码并独立审查；做不到则当前方案NO_GO，不自动加操作额度。

96预算细分为source4,800、teacher192、P0suffix3,504次generation；source动作4,800、prefix replay1,200、teacher动作96、suffix3,504，加192 reset共9,792操作。建议另设aggregate input token≤16,000,000及4 GPU-hour资源上限，均是投入ceiling而非已有耗时/费用估计；没有输入token化或GPU计时就不承诺金钱/墙钟成本。任何上限将到即先停止，保留incomplete，不填0、不补样、不自动加预算。未来所有真实科学check若耗模型/环境，也须入这96及上限，不能作为“免费preflight”。当前上限没有获准消耗。

480+60dev（仅一个actor）+600三臂评估的纸上上界已达135,480 generations、143,820环境操作；若dev也跑三臂更高，训练forward/backward、input tokens另计。削减采集后仍是600评估主导成本。因此拒绝把480/60/600作为一次打包投入，也不预留“达到C quota就自动继续”的通道。96已需最多8,496次generation，不称作廉价或效能pilot；若资源预算不接受这个上限，默认NO_GO采集，保留设计成果即可。

## 7. 未来效能验收与600的功效边界（不在本次release）

若以后另获授权，评估只运行学生自身：A/B/C各自从同一600独立TRAIN-task初态开始，H50/greedy/actor16，不使用teacher或recovery。按完整task配对报告两项co-primary C>A、C>B的W/L/net/gross harm；双侧exact McNemar、Holm排序阈值.025/.05；各比较观测net≥5pp、gross harm≤5%，并报告边际Newcombe10 CI。600时对应net≥30个task、loss≤30个task。CI不是paired检验替代，也不自动是多重比较同时CI。全部600预定完成，不看中期p延长、换任务或改checkpoint；技术missing使确认性报告不闭合，不能填失败或事后删除；正常actor fail-closed按原规则失败。

只一个训练seed42，最多支持该初始化/数据抽样/训练seed/协议的有限结论；不能推出跨seed稳健性。C>A与C>B都过才支持“这个受控同pool、failure-aware采纳配方在该设置改善学生”的有限主张；只C>A可能只是额外SFT，只有C>B可能是B退化，均不够。即便都通过，也不是unique advantage算法、第一动作期望价值估计或通用self-improvement机制证明。

下表仅为单个比较的假设trinomial纸上精确枚举。δ为真净差、q为discordance，win=(q+δ)/2、loss=(q−δ)/2；它们不是从R19/历史池估计的效应或新产率。将D~Bin(600,q)、W|D~Bin(D,win/q)与双侧conditional exact null逐项求和，没有运行任何真实结果统计或policy。

| 假设δ | q | 真loss | α=.025正向拒绝概率 | 同时满足观测5pp/5%及该检验 |
|---|---|---|---|---|
| 0.05 | 0.05 | 0.000 | 1.000 | 0.526 |
| 0.05 | 0.10 | 0.025 | 0.950 | 0.523 |
| 0.05 | 0.15 | 0.050 | 0.806 | 0.393 |
| 0.05 | 0.20 | 0.075 | 0.665 | 0.009 |
| 0.05 | 0.30 | 0.125 | 0.471 | 0.000 |
| 0.08 | 0.14 | 0.030 | 0.999 | 0.980 |
| 0.10 | 0.16 | 0.030 | 1.000 | 0.997 |

600并非天然没功效，也不保证完整验收80%。例如真δ=.05/q=.10时单pair检验约.950，但含观测效应门槛只约.523；δ=.05/q=.15时约.806降为.393。真loss>.05的情景本身不满足价值要求。两项Holm的联合通过还依赖A/B/C联合outcome分布，表中没有该模型，不能把两个概率相乘或称联合power。真实改善恰在5pp门槛时，有限观测过门槛概率接近一半本就不能靠任意小N承诺。若未来资金要求“5pp真实效应且完整标准80%联合通过”，目前不满足设计论证，默认不释放600评估。不能用旧oracle5.56pp补这个论证。

## 8. 负向结论、停规和近邻定位

默认只完成设计。未来采集只有独立关闭metadata/pin/receipt/成本条件并取得新授权才能开始；96完成后一次yield/coverage/contrast/exposure审查，失败则封存NO_GO，不追洗、不扩K、不重复C伪造N、不改baseline/teacher/prompt/decoding、不训练selector。即便机械可执行性通过，训练仍需独立授权；训练完成不自动解锁评估。任何泄漏、错误命令、身份/重放不一致立即停止并保留现场；行为失败与技术缺失分开。学习失败或效能未过不说明self-improvement普遍不可行，只否定本预算/采纳配方的当前投入主张。

近邻仅查两项原文，避免首创主张：[ReST^EM（Singh等，v4）](https://arxiv.org/html/2312.06585v4) 讨论用二元反馈筛生成样本再SFT，本设计不是新发明success-only过滤；其数学/代码任务结果不证明ALFWorld第一动作蒸馏会改善。[DAgger（Ross等，2011）](https://proceedings.mlr.press/v15/ross11a/ross11a.pdf) 说明序列决策中训练/部署状态分布偏移及迭代标注问题；这里单轮、少量base-teacher目标不具备其expert假设或迭代保证。只作定位，不照搬经验效果或理论承诺。

输入SHA与具体源码位置见source_bindings.json；纸上数学及真实rc见paper_math.json/.log/.receipt.json。没有运行旧脚本、tokenizer、项目analyzer/validator/pytest/preflight/G2/G3/G4或模型/环境/训练，没有读取未消费task正文/结果、创建实际schedule/gate/launch argv、派agent或写共享INDEX；只有OWN新设计文件。科学85/2da及原R19累计5142 generations/7949操作（含177/342）不变，本轮新科学调用0，研究审查与最终发布由协调方负责。
