# SI-P1 独立审查决定

协调方 Sol。实际向 Sol Research、Luna 两个既有线程派发任务并收到交付；另写独立 stdlib 脚本读取原件、复算字段和身份映射，没有用作者的自评代替验收。本文审查既有证据；协议和统计准则由协调方提出，未声称又经第三方独立统计审查。

**本阶段交付：ACCEPT_WITH_CORRECTIONS。11-case 机械来源链核验完成；已登记隔离映射/成本语义可接受；最小科学结构和统计决策标准形成。DATA_FEASIBILITY / TRAINING_DATA_READY / EXECUTION_READY 仍为 NOT_READY。新实验未启动。**

## 11 状态的独立原件检查

`independent_target_and_isolation_review.py` 未导入项目代码；peer JSON 仅作 locator，再读原 JSONL、逐行/整文件 SHA、source episode、动作前公共字段、原 teacher/parser/实际命令和既有 replay。11/11 的公共 P0 文本与原 source actor 当时保存文本逐字节一致；完整有序 map、raw bare ID、selection、执行命令、非终局时点和剩余 horizon 全匹配。R19 另外从原 188MB 账本核对 initial prefix replay 和第一 K1 recovery before-state，不借用恢复后 replay 或后续 SFT/K2 目标。

11 行仅 10 canonical task；两条 Book/DeskLamp 是同 task 的 d=23/28。11 个公共字段投影彼此不同；这不证明全池输入充分或目标唯一最优。原推理 token 数也不等于未来训练 token。

作者初稿把 R4/R19 缺显式 won 的两行标 HOLD_EVIDENCE，而 9 行为 INPUT_TARGET_LINEAGE_SUPPORTED。保留这些原字节和后续澄清：**机械来源链支持 11 行；终局信息完整度是另一个轴。** 9 行有显式 done/won/reward，2 行为 RAW_WON_NOT_RECORDED；原 frozen success helper 使用 done 且 reward>0，R19 transition 序列化本来未保留 won。本轮独立核对原 CONTINUE done/reward=0 与恢复终局 done/reward>0 及原成功标签一致。不伪造 won、不武断称奖励是 shaping、不以字段未导出追认新 G3 失败，也不把机械支持升级为完整训练验收。

10 个历史目标的实际 weights/tokenizer revision 仍不完整；R19 一例有原 runtime 的精确绑定。历史版本不完整不意味着动作非法，但限制“同一当前 actor 自采样”的主张；若将来采纳，应作为明确披露的历史跨策略蒸馏数据，并对 B/C 使用共同质量规则。不能从当前 cache 反填历史 loaded revision。

## 隔离与预算

协调方独立读取七个阶段原文件和已封存 P0 索引，闭合 351 个 prefix-to-task 与 row hash，跨阶段 169 unique task；完整 source hashes 全匹配。它们都已包含在现有 2,612-task known-use union。固定 11 行的全文件 SHA、行 SHA、task 身份也全匹配。原先“整批 R4/R16–18 映射缺失”与“全 source hash 缺失”的说法不成立。

known-use 差集计数为 TRAIN 1,141 / seen 0 / unseen 74，新增映射不改变这些集合。这里只核对已登记来源与支持 game 文件的元数据，未读取未消费的任务内容或运行新 policy。没有全历史从未查看证明，也未闭合场景/layout 相似性；因此不能宣称这些是 clean held-out 或立刻可执行的新日程。

R19 成本不变：原 G3 增量 4,965 generations / 7,607 含 reset 环境操作，累计 5,142/7,949，已含旧 177/342，0 incomplete external operations。本轮新科学成本 0。

历史 SFT 的 27,406.28269892931 秒是训练 wall time，不能写成 GPU device-time；23,860,000 保留原名 input_tokens_seen，padding 语义未证实；2,354 optimizer steps 单列，不并入 R19 推理账。专家重复计数为去重前148、删除21、去重后127；110同输入不同目标组不是已证实错误。未来三臂 actor-only 预算公式 150E/153E 是协调方设计限制，**不是“用户已冻结”或已批准执行的预算**。

## 文档写入越界与更正

Luna V1 的脚本含旧 P0 硬编码 ROOT，实际改写了两份已封存 P0 元数据，并在旧目录产生两份新文件。协调方先保存全部变动字节和 hashes，再恢复两份 tracked P0 文件至已发布 commit `57747744922bf7d44d0c30f1bd24cb6624f8216e`，将两份新 metadata 保存在本轮 incident snapshot 中。旧 P0 最终字节已恢复；科学源码和原始实验文件未改。

这属于真实的 provenance scope incident，不能用“科学树干净”掩盖。`P0_SCOPE_INCIDENT_AND_RESTORATION.json`保存逐项实际前后 hash；V1 仍保留，V2 另增更正，没有静默覆盖。V1 指向 transient P0 元数据的 input hash 只对应已保存 snapshot，不再谎称对应恢复后的原路径字节。Luna V2 的关键 source/mapping/成本结论由协调方另读原件支持。

## 设计取舍和阻断项

1. 最小比较是 A、B_pool、C；来源池、公共输入、目标粒度、背景 S 和训练曝光共同约束。只有 rescue 正例时 B=C，不能开始机制比较。
2. 每 task 最多一个事前 anchor；11 状态不能都当独立训练 task。共同池质量/anchor 后的真实 N、B_pool 非 rescue 成功对照、来源分层仍未验收，不能将本次 11-case 审核冒充全池通过。
3. 实际 supervised-token、曝光上限、T/U、单一训练 seed/recipe、独立评估任务空间/N 和实物成本未闭合。没有可执行训练配置、schedule、gate 或 argv。设计标准已明确，但执行附件仍阻断；不虚填参数来制造 READY。
4. 两项共同主比较用双侧 exact McNemar + Holm，并分别披露净增益和 gross harm；观测价值门槛为两项至少5pp、gross harm各≤5%。它们是前瞻项目取舍，不是旧 oracle 给出的效应先验或总体无伤害证明。
5. 纯数学规划表明，小 E 下无法承诺检出5pp；表只是 p-value 组件和假设场景，不是完整验收功效或新科学拨付。当前不以“跑完不显著再加样本”收尾。

**下一项必要证据是同池对照可分性及共同质量审计，不是训练。** 若共同规则后 B=C、可用数据过小、无法隔离任务或实际预算不支持有意义比较，停止该学习配方的实验推进，转向既有强 SFT 主结果与恢复/副作用/成本的论文实证。无需为维持 self-improvement 名称而继续调 recovery。

## 边界与原始收据

三份科学 worktree 在结束检查中保持原 SHA/branch 状态且干净：review-root e537f441、analyzer85cbb923、executedG3 detached2da980f。原始 source/branch/账本和全部独立读入输入 before/after SHA 相同。只做静态源代码/Git 对象、stdlib 元数据/字段审计、假想统计数学和文稿；没有模型、ALFWorld、tokenizer、训练、policy replay、预检、G2/G3/G4、项目 analyzer/validator 或 pytest 调用。

Sol 首次 schema probe exit1 是自有探测把合法空 suffix 当成非空，修正仅在新审计脚本，失败收据保留；后续真实 audit exit0。独立目标/隔离检查、351映射检查和假想数学均有实际 subprocess.returncode=0 的原始日志/收据。未执行的科学测试不写 PASS。

最终文件绑定、真实 peer 交付与 seal 验证见 `phase1_independent_review.json` 和 `RECORD.md`。本审查不签发任何新实验 clearance。
