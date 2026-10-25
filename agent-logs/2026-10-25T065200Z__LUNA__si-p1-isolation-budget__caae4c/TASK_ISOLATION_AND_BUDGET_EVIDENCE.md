# SI-P1 任务隔离与预算证据（只读）

状态：`PREPARATION_ONLY / NOT_READY_FOR_TRAINING_OR_NEW_EVALUATION`。本轮模型、环境、训练、policy replay、新评价调用均为 0；没有生成 schedule、argv 或 gate。

## 固定 11 case

固定索引为 11 行、10 个 canonical task/trial。逐行身份、prefix、历史来源路径、source-row hash、已安装 split 与已知使用登记见 [`task_isolation_audit.json`](task_isolation_audit.json)。11 行均在 train split，且都命中已记录的历史使用/排除登记，因此只能视为历史开发学习候选；不能再当新评价身份，也不等于训练数据已就绪。`R10_OSR:R8-F22` 和 `R10_OSR:R8-F23` 是同一 Book task/trial 的两个 prefix，按一个底层身份计数，二者同属 train。固定行有 source-row SHA，但冻结 P0 原始盘点没有为这些 case 的每个历史源文件绑定完整文件 SHA（字段为 null）；不可把 row hash冒充文件 hash。

## 身份盘点和隔离

| Split | task/trial 目录 | 六 family 且 `game.tw-pddl` 存在 | known-use 差集 | candidate ID SHA256 |
|---|---:|---:|---:|---|
| train | 6374 | 3553 | 1141 | `13e403d27a59f25e6ed8ce5677a8d3da2cfd8760360a5c557c2fe297b13174dc` |
| valid_seen | 251 | 140 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| valid_unseen | 255 | 134 | 74 | `7b7b9a4f2987f1780d73199506d447bf13f878500cbfa228d2d69ed20a1c6ad0` |

本次元数据重算与 P0 file-presence 支持数/known-use 差集完全一致（train 1141、seen 0、unseen 74）；因此**没有减少** P0 差集，也没有证明这些身份干净。差集只是已登记身份的补集，来源登记可能不完整，不能标为 clean/held-out/可执行 N。目录身份交集 train/seen/unseen 两两为 0；这是 exact task-trial 分区结果，不排除近似场景、布局、物体或 prompt 泄漏。

全局来源登记已纳入专家 train 1074、offline validation 126、online development 60、已知 exclusion union 1406、valid_unseen G1 已用 60、历史 architecture/recovery/Sprint/R14/R19 登记（详见机器文件）。R19 registry 的 127 个 source episode 单独计数；39 个 replay/initial-attempt 与 36 个 extension 是分支/子单元，不再加成新 source episode。R12 的重复示例和重用 prefix 不重复算 episode。

固定 11 case 从 prefix 到 canonical task/trial 的映射已由固定索引补齐；但 R4 及 R16–R18 的**所有**历史 prefix/cohort 并未普遍闭合：部分 manifest 只提供 prefix/position 数量，缺少完整 canonical 映射。这里只报告可证实的固定身份，不从 outcome 表反推。完整登记覆盖不等于证明历史从未查看其他任务（`NOT_PROVEN`）。

P0 专家集核对：20,967 rows / 1,200 tasks；exact-dedup 前保留的重复 occurrence 为 127，110 个 rendered-prompt group 有不同 action target。该数符合生成器计数阶段约定，不构成 identity/hash mismatch；本报告没有重建数据集。

## 真实成本与边界

经独立已存成本审计，G3 增量为 4,965 generations、7,273 non-reset operations + 334 resets = 7,607 environment operations，0 incomplete；含前驱累计 5,142 generations、7,603 non-reset + 346 resets = 7,949 operations。前驱已知失败单元的 1 generation + 1 reset 保留在累计数中，不清零。曾出现的 8,118 是将 169 个 wrapper transition 与底层物理操作重复计数的监控显示值，已由独立链接证据修正；权威值为 7,949。

历史 SFT 训练单独列账：已记录 2,354 optimizer steps、27,406.3 秒、约 23.86M padded input tokens；完整项目其他阶段物理成本、未来训练 T/U、有效 token、实际输入 token 和 GPU 时间均为 `UNKNOWN_NOT_ZERO`。不把这些混入 R19，也不按旧 prompt 长度估算。

纸面上，未来 E 个任务、3 个独立 arms、H=50 的动作生成上界为 `150E + C`，其中 C 是任何额外 controller generation；若每 episode 一个 reset、每动作至多一个环境操作，环境上界为 `153E + R_extra`。额外 prefix replay、probe、validation、失败/未完成单元必须单列。来源/分支复用时 physical acquisition 只计一次，但各 policy 的 logical cost 仍分别报告。该公式不是额度，也不选择 E；本轮新增预算授权为 0。

完整双账模板见 [`BUDGET_TEMPLATE_NOT_EXECUTABLE.md`](BUDGET_TEMPLATE_NOT_EXECUTABLE.md)。静态 horizon 依据 R19 source 的 `R19_MAX_STEPS=50`、`remaining_horizon` 与 suffix cap；未运行项目代码。

## 范围偏差与证据边界

准备阶段曾有一次宽泛文本搜索短暂输出两条已消费 R16/R17 结果行（包含 outcome 列）。没有读取任何未消费结果；该输出没有用于身份或候选结论。此偏差在早先 Luna P0 自有收据中已有记录，本轮不改写旧收据。所有其余任务仍限于身份/元数据和已消费登记。

独立审查、实验 READY 或执行许可均未由本报告宣称。历史 P0 的 `DATA_FEASIBILITY=NOT_READY` 继续有效。
