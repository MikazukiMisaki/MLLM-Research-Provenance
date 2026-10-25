# SI-P1 最小学习协议：设计冻结，执行附件未就绪

状态：**DRAFT_NOT_EXECUTABLE / DESIGN_REVIEWED_WITH_CONDITIONS**。协调方 Sol；本轮授权仅为既有证据审计和设计。本文不是训练配置、预算拨付、日程、preflight 或 launch clearance。

## 研究问题和当前决定

问题收敛为：**给定同一个历史单步恢复候选池、同一学生输入和受控训练曝光，按配对增量采纳经验，是否比仅按恢复成功采纳经验，更能提高冻结 SFT-P0 在独立任务上的成功率？**

继续这一研究问题的设计与证据整理；**暂不启动学习实验**。11 状态/10 canonical task 的动作来源可核对，不等于已经有足够、可学习且有可区分对照的数据。R19 的 5.56pp 是已有 36 状态上的事后 oracle 差额，不是新学生的预期增益、训练标签或功效先验。

本协议保留“能力建立 → 执行纠错 → 纠错经验的学习价值”的论文主线。现有结果支持前两部分的实证分析；第三部分仍是待证假设。没有在线自主循环，不声称算法首创或已经实现 autonomous self-improvement。

## 唯一最小比较

| arm | 起点与数据 | 用途 |
|---|---|---|
| A | 已冻结的原 SFT-P0，不更新 | 强基线；判断是否实际提高成功率 |
| B_pool | 从同一个 A 起点更新；普通成功背景 S 与 C 完全相同；同池单步恢复记录仅按恢复成功采纳 | 隔离“多了一批成功演示” |
| C | 同起点、S、格式、训练预算；同池纠错部分另要求原 CONTINUE=0、恢复后=1 | 检验配对增量采纳配方 |

不增加 B_source、oracle、K2 目标、detector、selector、memory、DPO/RL、多轮反思或新环境。B_pool 与 C 都只学习第一恢复动作，不把 adapter-on SFT suffix 当成另一份 adapter-off teacher 目标。两者训练后评估均为 actor-only：原公共 P0 输入、原 greedy decoding、horizon 50，无 recovery、额外模型 probe 或环境 replay。

主张限定为**固定历史生成池和训练预算下的采纳配方差异**。C>A 且 C>B_pool 才支持这个有限主张；仍不能证明某条动作本身具有因果学习增益、同等端到端获取成本最优、跨随机种子稳健或每个家族有效。

## 候选池和共同质量规则

原始候选清单 11 行保持不变，不把审核后导出的索引当作已验收训练集。Sol 的终局证据分层保持：9 行有显式 done/won/reward，2 行缺显式 won；协调方另核对 11 行均符合原冻结 done+positive-reward 成功判据。缺 won 不改判旧 G3，也不补写历史字段。未来若要合并两类终局证据，必须在数据附件中明确采用何种既存证据标准，对 B/C 一视同仁；当前训练 N 未建立。

10 行历史 weights/tokenizer revision 不完备，不能回填成当前 R19 的精确版本。可保留为**来源部分可追溯的历史跨策略蒸馏候选**；不能据此称同一当前 actor 自采样。只有通过同一质量规则、且来源混合被预先分层约束的池才可能用于比较。若必须靠追认历史版本、重写动作或补跑成功才能形成对照，则停止该池的使用。

公共学生输入固定为动作前 goal、current observation、最近 4 条已发生的 action/result transitions 和完整有序 admissible action map。目标固定为原 teacher 的合法 bare ID；必须与公共 map、实际命令和执行 transition 一致。诊断/subgoal/card、facts/expert_plan、原当前动作输出、当前动作之后的 observation/reward/done、终局标签、K/oracle 等都不能进入学生输入。无效/截断/未执行目标排除；map 不同先停，不能静默重索引。

共同质量筛选必须在 B/C 的采纳条件之前完成。适用于同池所有记录的公共输入、目标粒度、完整性、来源和身份规则完全相同。后续数据附件还须证明有真实的成功但非 rescue 候选。**若只有这 11 条正例，B_pool=C，实验没有识别能力，直接停止。** 不为得到不同集合而反复改种子或过滤规则。

## 独立性和去重

canonical task/trial 是分区和统计单位；不同 prefix/seed/处理/alias 不能绕过隔离。11 行实际仅 10 个 task；两条 Book/DeskLamp 同 trial 的 d=23/28 不能算两个独立 task。

最小主设计继续采用 P0 的**每 task 最多一个 anchor**。在共同候选池上按不看结果的固定规则选 anchor，再做成功/配对增量采纳；不能先挑 rescue 再为它选最有利前缀。具体规则、全池去重和各阶段可用数须随数据附件一次冻结。故最终 C 的独立 task 数上界为 10，实际合格 N 仍 UNKNOWN；不会为了维持 11 而豁免同-task 规则。

同一物理生成、source 复用、suffix alias 或重复报告只记一次来源；语义相同序列不自动证明物理复用。B/C 从同池获得按来源阶段约束的曝光，必须披露剩余难度/任务组成变化。共享 S 不带入任何新评估 task；所有源 task、teacher 生成 task、背景 S 和开发 task 均排除出最终评估。

## 训练和预算附件必须补齐什么

两组从相同 A 权重/adapter 哈希开始，使用相同损失、LoRA、学习率、batch 规则、单一训练随机种子和最终预定 update 的 checkpoint。无 checkpoint/seed 搜索，无根据评估结果加 epoch 或补样本。

**目前不虚填 T、U 或 GPU 时间。** 共同非 padding supervised completion-token 预算 T、背景/纠错比例、optimizer updates U、每 task 曝光上限、序列/截断与 EOS 规则须依据实际合格数据与固定 tokenizer 的独立核对一次选定。原推理 generated_tokens、历史 SFT 的 input_tokens_seen、2 epochs 或约 7.6h wall time都不能直接替代这些数值。本轮未加载 tokenizer，也没有为“预算匹配”复制稀有样本。

若 C 在共同训练预算与预设重复上限下无法形成有意义的更新，应判数据不足；不能用无上限重放十个 task 掩盖不足。没有共同池和实际 token 长度之前，给一个漂亮的 update 数反而不可审查。因此本文冻结科学结构和验收，训练参数保持阻断项，而不是声称可执行。

## 评估和资源

未来同一个独立 task 清单对 A/B_pool/C 各执行一次，输出成对 2×2 表；成功需绑定环境的终局 success/won 与 done，并保存 reward 字段语义。无效动作按原 fail-closed 规则处理，不替换任务、不给额外 horizon。

已登记集合并集 2,612 task；本轮补闭合的 351 prefix 映射对应 169 个跨阶段 unique task，均已在此并集中。支持文件的 known-use 差集是 TRAIN 1,141 / seen 0 / unseen 74。它们**不是从未被看过的证明**，无新 held-out 许可。场景/layout 相似性及未登记历史查看仍未闭合。未来若使用 task-disjoint TRAIN，应如实称跨 TRAIN 任务评估，不能改名 held-out。后续应冻结可审查的身份规则、覆盖来源和剩余风险，不要求逻辑上证明所有人的完整浏览史，也不以此开展无限审计。

评估 E 个 task、三臂、H=50 时，actor-only 静态最坏上限为 150E generations、153E 环境操作（含每 episode 一次 reset）；这是设计公式，不是本轮拨付。若额外 probe/replay/controller 操作出现，必须先停，不得藏入此上限。训练、历史演示获取、配对验证、共享实物成本与独立方法获取成本分账。

R19 原累计账本保持 **5,142 generations / 7,949 reset-inclusive operations**；旧 177/342 包含在内，不能再加一次。历史 SFT 的 optimizer_steps=2,354、wall_time_seconds=27,406.28269892931、input_tokens_seen=23,860,000 单列；GPU device-time 和 padding 语义保留 UNKNOWN。

## 当前放行与停止点

1. 本轮 11-case 审计、已登记隔离证据和预算语义整理可验收，附更正；训练/执行不放行。
2. 下一个最小证据工作是**同池 B_pool 对照可分性与共同质量规则审计**：仅复用已经存在的索引和原件，不生成新成功、不做训练、不补跑 G3。该任务需单独明确行范围，不能把本轮 11-case 验收冒充全池验收。
3. 若同池质量筛选/anchor 后 B=C、C来源不可用、无法满足独立任务或合理训练预算，停止此学习配方；不扩到多步 K、换 prompt、调 selector 或持续收集至出现 positive。
4. 若以后形成可执行附件，仍须 exact-SHA 实现审查 → Luna 只读准备 → 独立执行核验 → 明确范围的科学执行。当前没有准备 gate、preflight、训练、模型或环境启动。

统计准则见同目录 `STATISTICAL_ACCEPTANCE_CRITERIA.md`。当前最诚实的下一步是先闭合对照，而不是把 11 个来源可核对的动作宣称为已可训练的自改进方法。
