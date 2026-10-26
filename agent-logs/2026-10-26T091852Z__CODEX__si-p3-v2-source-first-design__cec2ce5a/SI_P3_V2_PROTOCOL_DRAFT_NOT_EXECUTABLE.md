# SI-P3 v2 候选协议：全96固定d5、source-first、事前不可构造检查

**DRAFT_FOR_REVIEW / NOT_ADOPTED / NOT_EXECUTABLE / COLLECTION_NO_GO_NOW。** 本文件是新的文档候选，不覆盖已冻结v1，不改变工程844cc4b、科学85或已执行G3/2da。不生成任务seed表、schedule、gate、argv、run目录或clearance。当前连source96本身也不建议自动投入；无采集、训练、评价、工程探针或实现授权。

已合并阅读并核验Astra最终方案SHA `1ed3d567d534fe926ceafa7b120369905c0fb2f69ee104057b221ee24992a757`，其封存先于本稿。协调任务SHA `51143107131e15b1771882461bd77200de14c726819a909de701b9f19fe3b188`。默认结论与Astra/root一致：不采v1；v2只是另一个待审版本，工程PASS不能使其自动进入运行队列。

## 1. 改动边界与保持的科学条件

若未来独立采纳，只允许两项设计改动：(a) 每个task唯一位置统一为完成5个真实动作后的动作前状态；(b) 全96 source先完整封存，再作确定性必要数量检查，之后才可能进入branch阶段。晚位置不可达风险由(a)缓解；(a)不能创造原P0失败，也不证明C24供给。source-first是执行顺序和证据合同的实质变化，不是现有逐slot实现的开关。

保留同一已登记A96身份集合及原reservation原件SHA `6ce8a32a2345b59ecdef9c28c3a341e9c0801b8105f79895f9b2cb9545a4937e`。不重选task，不把D48/E600同family身份移入A96；48工程/600评估/395非light及2light余量保持原分区。没有打开unused task正文。五家族及必要数量如下：

| 家族 | 固定source N | 最终共同Q最低 | C最低/各臂选中C数 | neutral池最低 |
|---|---:|---:|---:|---:|
| pick-place |35|22|9|9|
| clean |26|17|6|6|
| cool |16|10|4|4|
| heat |9|6|2|2|
| pick-two |10|7|3|3|
| 总计 |96|另须≥72（家族最低之和62并不足够）|24|24|

Q、C、neutral的总门槛和家族门槛同时保留，不能转配。单K1原地交回、H50、同Qwen3 snapshot b968826…、P0 adapter6e403d85…、greedy/thinking=false、source/suffix adapter-on、teacher adapter-off、40/16/16生成帽均不变。公共输入仍为原P0 goal/当前obs/H4/完整有序map；teacher仍是冻结two_stage_v2。保留EOS/cap、标签、去重、S120、B/C配方和不重抽规则。

## 2. Source-first及计数/重放的纸上合同

1. 在任何新结果前绑定同96身份、每task seed及相应pool/RNG初始化、source与branch顺序、全部版本/输入及费用上限。这里只规定绑定要求；实际seed值/顺序映射和可执行清单尚未冻结，不能宣称协议已可执行。不能用本轮文档去选择一个“更容易失败”的seed。
2. 先完成全部96 source。每task一条P0轨迹，最多50次generation及50动作；正常terminal、horizon、完整空map、actor parser fail-closed等按原契约停止。每次真实外部调用先reserve/start落盘、再调用、再complete或failed；source封存必须引用真实原件和全部物理单位。technical/incomplete不能改成正常failure。
3. 一旦真实完成第5个动作，立即保留该transition的after公开snapshot及其hash/receipt、done/truncated、完整有序map、H4、actor公共projection。冻结时点早于第6个actor generation及未来source结局。之后得知Y0不得改这个公共输入；source终局/invalid第6次输出不得进入teacher提示或学生输入。
4. 每个source闭合独立于整个task的branch闭合；全96完整source的hash列表及source阶段seal必须在任何branch reset/replay/teacher前持久化。后续branch失败不得抹掉已认证的source/Y0。source suffix的CONTINUE结果只引用原source，不能重跑原actor或对同一物理事件再记账。
5. 经下述必要条件审查并且未来授权确实包含branch阶段时，才处理全部E中的task，按事前branch顺序、与Y0无关地各一次。不得只给Y0=0做teacher；source成功对照同样保留。若仅source阶段获授权，即使必要条件全过也不得自动进入branch。
6. source与replay分别使用新的单task环境实例；每实例只做一次初始reset，使用相同、已绑定的task-local seed/pool初始化，并验证同task初态。source全部结束后再replay，不能以全局reset次序、之前运行任务数或前一条teacher耗时决定环境初态。`receipt index=0`不是已证明的TextWorld内部counter值；内部状态的观测/绑定仍需未来工程验收，不能伪造为0。
7. 对E的task精确重放原5个动作，逐步核对task/seed、before/after obs、完整map、Action-ID→command和原source step引用；不调用模型重生prefix，不搜索seed、不再reset碰运气。任一身份/状态/命令/receipt不符整run STOP。teacher两次生成发生在replay的S5，同一个环境上执行唯一合法首动作（第6个动作），立即交回P0；suffix最多44个动作/生成，不reset、不再replay、不扩K。
8. 绑定环境seed和模型/RNG上下文需要分开审查。现wrapper reset会seed Python/numpy/torch全局状态，而单game TextWorld的pool seed又由factory设置。应在未来合同记录task、phase、local operation index、初始化/计数证据，证明另一slot提前结束或branch被省去不会改同task初态；greedy不是可以忽略所有随机状态/计数的证明。本稿不发明新解码器或随机策略。

## 3. E是完整Q的保守上界，不能用旧L>d代替

令S5为完成5个已记录真实source动作后的公开状态。E只保留证据能认证S5存在、非done且非truncated、完整map非空的task，并要求source有已认证的正常闭合和Y0。E包含后续可能被replay、teacher有效性、2048完整序列或共同去重排除的task。因此未来完整Q必满足Q⊆E；E不是已通过Q，更不是teacher成功池。

| Source原件情况 | 位置判定与标签边界 |
|---|---|
| 第5动作后done或truncated | E外，保留NO_ELIGIBLE_STATE，不挑更早位置；Y0仍按正常source原谓词记录 |
| 正常在5动作前结束/空map/actor解析停止 | E外；是预定位置不可用，不补任务 |
| 恰有5动作，S5有效，而第6次generation解析失败未执行动作 | E内。source已正常fail-closed，Y0=0；不能因L=5排除有效S5 |
| S5有显式完整空map | E外；空与缺失不同 |
| 应有的checkpoint/map/transition/终止原因缺失、矛盾或无法认证 | INTEGRITY/TECHNICAL STOP，不将unknown当E外或Y0=0 |
| source因技术/预算中断而未正常闭合 | source阶段INCOMPLETE，Y0不填失败；不能发结构性不可构造结论 |

旧127原件恰好仅末步done，故旧描述中L>d正确；这个特性不能移植为未来collector的通用E判定。d按已执行动作计，不按生成次数计。第5动作的after是S5；teacher动作在原零基index5，suffix从index6开始，合计5+1+44=50。

缺失证据应先STOP；不能一边丢弃unknown一边以剩余E证明数量不够。必要时只能从已认证、完整保存的transition重建公共view；不能新增环境replay来填补source阶段证据，也不能偷看未用task或YT来判E。本稿没有运行这种重建或任何policy replay。

## 4. 完整source96之后的确定性futility（仅数学规范）

全部96 source正常完成、S5去向和Y0完整可核对后，设F=E中Y0=0者，S=E中Y0=1者。只有以下已经不可能达到既定配方的必要条件，才支持结构性提前终止：

* E总数少于72，或任一家族E少于表中Q最低；
* F总数少于24，或任一家族F少于9/6/4/2/3；
* S总数少于24，或任一家族S少于9/6/4/2/3。

这只使用source端已观察事实和既定数量，不使用teacher成功率预测、历史6/120外推或学习收益预测增加新判定。F是C的保守上界，S是neutral的保守上界；最终去重、合法teacher和YT仍可能使两者变小。

结构性停止单列 `COMPLETE_SOURCE96_STRUCTURAL_NO_GO`，teacher结果全部NA，未做teacher原因写 `TEACHER_NOT_RUN_SOURCE_FUTILITY`；同时保留各task原source/anchor去向，不能用这个全局原因覆盖terminal/invalid等事实。它不是96个完整paired采集，也不是teacher失败样本。所有计划source均留分母和真实费用。

必要条件全过仅表示 `SOURCE_UPPER_BOUNDS_NOT_FUTILE`，不是数据或投资GO、Q通过、C24可构造或科学release。在未来明确全采集授权下，才允许继续所有预定E；当前没有该授权，仍NO_GO。若teacher/suffix阶段中途technical/budget/integrity STOP，保留已知Y0、已执行YT或未观察NA与open reservation，不宣称完整96配对。

## 5. Y0、YT与共同质量

Y0引用原source正常闭合结果，维持 `done && reward>0` 成功谓词。合法正常的actor解析停止、empty-map或H50未成功为0；技术missing/incomplete为NA而非失败。不能新增“必须有raw won”来改写旧成功。截断/terminal等原stop字段完整保留，不用它们替代成功谓词。

YT只在真实执行合法teacher首动作后、按同一P0 suffix的原正常停止合同记录。teacher动作直接成功可有YT=1和零suffix生成；合法teacher后suffix正常失败/解析停止可为YT=0。未做teacher、Stage1或Stage2不合格未执行动作，YT均NA；不得复制Y0、填0或创造终局。source/suffix沿用P0原parse选择语义，不因EOS incomplete额外取消其合法选择。teacher完整性保持严格；complete=true且cap=true（帽处EOS）不得误排除。Stage1不合法仍按原固定协议记录一次Stage2诊断性生成，但不执行该teacher动作。

共同Q及其去重对完整池对称适用：全部原件/版本/身份/精确source与replay/公共map/合法首teacher目标/实际branch闭合/完整2048训练序列，不截map或label。physical unit去重→每task一个anchor→按既定与结局无关的顺序去重exact public input+command；不同command的相同public input不能按未来结果随意修理。harms、双失败、invalid、不可达和NA均保留于完整池/去向。

B_pool={Q且YT=1}，C_pool={Q且YT=1且Y0=0}，neutral={Q且YT=1且Y0=1}。B_pool必须包含C；B不是neutral-only。C按原fixed hash和9/6/4/2/3选24，再在整个B_pool按family×实际supervised ID+EOS长度匹配一次原fixed B hash。保留至少8/24 neutral、B/C multiset不同、每臂≥20种公共projection、无exact input-command重复；任一不满足停止该固定draw，不换C、length cell、B seed或hash域，不重抽、不top-up。

## 6. 学习与研究归因边界

保持A=冻结P0，B=S120+B24，C=S120+C24；同P0字节warm start、只更新预定LoRA、fresh optimizer、2epoch、每新task最多2曝光、18update/唯一final18、同paired slot置换及microbatch/accum边界。保留真实causal-shift ID+EOS监督token逐microbatch/更新相等、两臂累计新例prompt与全臂prompt比各≤1.05、完整2048无截断。此前S120/mask软件证据不等于未来B/C token已测；本轮无tokenizer或训练调用。

C−A是S120复训、teacher动作目标及24新例/更新共同组成的追加训练包；不能独归于纠错经验。C−B仅是同池、共同S/剂量/长度匹配配方下，原actor失败筛选相对C分布匹配success-only采纳的差异，B的分布由所选C构造，且可能与C重叠；不是独立随机的普通成功分布，也不是teacher因果机制的唯一证明。报告B∩C、neutral、任务/公共输入/长度和真实token差异，不据这些结果重抽。

teacher看过的diagnosis/subgoal不能传给学生；学生只见S5冻结普通P0公共输入，目标仅首动作ID+EOS。source终局仅用于离线标签/采纳。完整后缀成功不认证该单动作处处最优，也不保证公共输入足以无歧义学习。固定d5可能发生在错误之前，因此这是固定早期干预动作蒸馏，不是error-triggered recovery、adaptive stopping、learned recovery selector或自主自举。

门槛全过最多得到 `RECIPE_CONSTRUCTIBLE`，不是learning efficacy或投资通过。完整效能仍需未来独立决定，保持C−A/C−B双主比较及原净收益/伤害/统计准则、单seed和TRAIN任务隔离但非scene外泛化局限；不追加第四臂来扩大本轮，只收窄主张。

## 7. 当前决定与尚待闭合

旧四家族非light source120中仅6失败、pick-place0失败，以及d5可达111只是已用旧队列的描述；我没有重数原source/teacher结果，也不将它们推成新96的产率或功效。它们提示C供给是独立风险，pick-two没有旧source证据。必要条件是新96至少24个可达source失败且符合各家族门槛；全d5本身不能论证这笔投入值得。

默认仍NO_GO新source/live/学习/评价；不降低C、不加N/384、不改teacher或加selector来修复产率。若未来缺少独立的source96投入理由，可以结束当前小剂量路线而不把NOT_PROVEN写为“不能学习”。

本稿不是启动申请。未来唯一顺序：设计版本/投入理由审查→另行最小实现及exact-SHA独立验收→真实可信执行能力/单独有界工程证据→独立科学采集授权→完整实际数据后的学习/评价投入决定。PID映射仍BLOCKED；当前source-first驱动、phase事件/独立auditor和真实成本闭合未实现或未测。不得沿用已消费工程/G3授权。
