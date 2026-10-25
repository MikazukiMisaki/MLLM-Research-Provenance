# SI-P0 独立审查决定与后续顺序
协调方Sol；本轮是用户授权的审计与设计。审查了两位实际线程的交付，另写独立stdlib脚本读取历史原件，不以agent自评代替验收。本文件不签发新实验clearance。

## 决定
**SI-P0交付：ACCEPT_WITH_CORRECTIONS。设计可继续；训练资料尚NOT_READY。**
**DATA_FEASIBILITY=NOT_READY；PROTOCOL_DESIGN_FEASIBILITY=READY；TRAINING_DATA_READY=NOT_READY；自主self-improvement效能=NOT_DEMONSTRATED。**
保留“能力建立→执行纠错→纠错经验能否可学习”的主线；不再把微调恢复时长当唯一成功率提升路线。本轮没有证明必须放弃该研究，也没有足够依据直接开启训练。

## 独立核验
- 原件重数SFT开发配对3/60→48/60、45胜0负、60身份和记录字段一致；旧unseen49/60单臂与60冻结日程逐项匹配。base仅1/2817格式违规，不足以把45任务提升全部解释为格式修复；未隔离各学到技能的因果贡献。
- 最终专家集20,967行/1,200task，字段hash/map一致；原protocol三项canonical SHA精确匹配。明确撤回Luna草稿的raw/canonical误比，不改原稿，后续引用必须连同更正。
- 110同输入不同目标组是局部歧义/多解线索，不是已证实数据错误；148→127是exact去重前后计数。未改数据或输入。
- 对Sol历史31条rescue ref逐行原件hash/identity/0→1全部匹配，涉及15task；R19各K rescue union另2task。跨所有处理为17task/18state审计上界；post-SFT单动作仅11state/10task、4family。它们不自动成为合格训练样本。
- R19 36eligible的K1..5成功29/30/28/25/24、K2 rescue2/harm2均和旧正式结果一致。两个oracle额外病例不是CONTINUE rescue；旧incomplete source保持原样。
- Luna目录盘点只是文件名差集。协调方另做六family+game文件存在性元数据核对：supported文件3553train/140seen/134unseen；known-use差集在其中为1141/0/74。仍非完整历史污染证明、运行资格或新heldout许可；没有打开未消费内容。
- 原科学树85/2da、所有已读输入与原件hash不变；本轮新模型/环境/训练调用0，R19账本5142/7949不变。

## 对一轮草案的审查
最终审查采用Sol的SI_P0_FINAL_FEASIBILITY_DECISION.md和不可执行V2（原V1保留历史）。Sol V2草案固定A强SFT-P0，B/C共享生成池、格式和普通成功背景，B仅按成功、C对纠错部分加paired增量，等训练预算并单列配对验证费用。该设计有可证伪性，优于将不同来源差异直接称筛选机制。仅接受为DRAFT_NOT_EXECUTABLE，不是效能/训练/工程PASS。
method主张限定为“给定固定生成池与训练预算的采纳差异”。不声称相同端到端获取成本最优；也不以连接Re-ReST与CIR两种已有机制就宣称算法首创。额外DITS近邻提醒：当次干预价值不等于学习价值。

以下条件由协调方审查补充，优先于草案中的宽泛表述：
1. 正式新协议必须将success绑定到原环境的终局success/won与done，说明reward字段语义；不能泛用任意positive reward代替任务成功。这里是未来谓词澄清，没有发现或裁定原结果错误。
2. 逐项public-P0输入投影、目标原始ID/命令/执行、完整反馈与模型来源尚未验收。不同controller上下文可以用于离线目标生成，但必须明确是跨策略蒸馏，不能把额外subgoal/card/未来反馈带入学生输入。
3. 单步纠错对clean/cool没有正例、light集中。不能据10task/11state或相关K外推学习收益/power；实际targettoken、重复上限、预算、checkpoint、预设效应/伤害标准与任务空间都需闭合。DESIGN_PRECISION_NOTE仅作假想表说明，不是新样本量承诺。
4. 任务污染登记仍需整合已消费canonical来源；剩余74只作identity候选。未来若仅用独立TRAIN评估，诚实称跨训练任务测试，不冒称heldout。
5. 人类已有FullAccess和继续工作的授权适用于常规只读整理、文稿修正和已授权可逆工作；不因Sol草案第8节而反复索要Approve。当前仍按“先设计与审查、不启动新实验”边界工作；未定义预算/协议的模型、环境、训练或新评估不会自动开始。旧许可已消费，不能复用。
6. 不改变冻结模型/prompt/decoding/horizon/schedule/quota/exclusions；不开发selector/memory/DPO/RL/新环境，不为凑positive采集或自动多轮。

## 后续工作顺序与验收
1. **Sol Research：协议与可学习性**。以已经列明的单步11state候选为审查对象，先闭合动作前公共输入/目标来源和反例去向，决定是可设计小型学习feasibility、还需新数据协议，还是结束该方法分支。不把索引导出当已批准训练集。把同池success-only对照、来源边界和一轮停规写入正式协议候选；不启动训练。
2. **Luna：证据/身份与资源准备**。沿用已消费的canonical元数据和独立file-presence核对，闭合已知使用登记、缺项与未来资源账的结构；不消费未运行结果、不造schedule或launch gate，不调用模型/环境。
3. **Sol：独立设计冻结审查**。决定目标主张是机制还是整体配方、可接受预算/精度和停止条件；有可执行协议后才进入明确实现任务、exact-SHA独立审查、Luna准备及科学执行边界。设计未闭合就不以“先跑看看”绕过。
4. 同步整理论文证据链：专家SFT主结果、恢复机制/成本与反例、self-improvement未证实的缺口。若经验数量/来源/独立评价无法支持有意义比较，收敛为实证论文，不继续调恢复prompt或累计重复版本。

上述为阶段路线，不是假报下一阶段已经执行。当前首轮任务、独立审查与发布完成后保留所有原件和草案；进一步工作仍只在明确分配范围内进行。此前4人时36例detector设计仍NOT_STARTED，本轮不冒名完成它。
