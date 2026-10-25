# SI-P1 隔离与预算证据 — V2 更正

本文件是 SI-P1 V1 的**新增更正**；V1、V1 `FILE_HASHES.sha256` 与任何 P0 原件均未修改。仅基于已发布 P0 元数据、Sol 的独立只读 identity/source-hash join，以及自有冻结 V1 产物；没有重跑 P0 脚本或项目代码。

## 先前范围偏差与来源依据

V1 准备时调用的身份盘点脚本带有旧 P0 输出目录的硬编码 `ROOT/OUT`，因此曾刷新 Luna 自有 P0 目录文件，违反 SI-P1 只写新目录的边界。Sol 已保全变更/新建字节快照并恢复已发布的两个 tracked P0 文件。事故分类和原件/快照 SHA 见 [P0_SCOPE_INCIDENT_AND_RESTORATION.json](/home/lizening/research-notes/agent-logs/2026-10-25T065200Z__SOL__si-p1-protocol-review__caae4c/P0_SCOPE_INCIDENT_AND_RESTORATION.json)，SHA256 `c7947a2249f838948a07b28f6d02c21d02af2055a15e1e1205b068eed898bc35`。V1 保持原样；其中指向临时变更 P0 输出的输入 hash 应与事故快照对应，不能当成未变化的已发布原件。

本 V2 的历史 prefix 映射和全文件 hash 使用独立 join：[`independent_source_hash_and_identity_join.json`](/home/lizening/research-notes/agent-logs/2026-10-25T065200Z__SOL__si-p1-protocol-review__caae4c/independent_source_hash_and_identity_join.json)，SHA256 `462a1e723199d76a1ca732c2821832d0cdafe3d3bd01895d0e2b4a27225d942b`，绑定 P0 `experience_inventory.json` SHA256 `1b0b7766d5901894d71f635433b9055223648d07bf5bda4e648c1129403cd8c0`。该 join 报告 351 条 R4/R10/R16/R17/R18 C1/C2/R19 prefix-to-task 原件映射全部匹配，source full-file hash、原始行 hash 均核对通过；这纠正 V1 对全局历史映射不闭合及固定 case 缺少 source full-file hash 的表述。**未登记之外是否曾被查看仍 `NOT_PROVEN`**，这一限制保留。

## 固定 11 case（11 行 / 10 个 canonical task-trial）

逐 case canonical identity、prefix、完整 source path、full-file SHA256、row SHA256、split 和 disposition 在 [`corrected_isolation_budget_v2.json`](corrected_isolation_budget_v2.json) 中。11 行均通过 source mapping/hash join、均为 train split，也均属于历史开发学习候选；不能作为新评价身份，也不因此成为训练就绪数据。R10 的 R8-F22 与 R8-F23 是同一个 Book task/trial，仍只计一个底层身份。

V1 中“缺少 full source file hash”是错误结论，现撤回：固定 11 行均有经独立 join 验证的 source full-file SHA 和 row SHA。R4、R10、R16、R17、R18 C1/C2、R19 七个来源队列合计 351 条映射全部闭合；不再把部分 run manifest 自身不含 canonical ID 扩大成其 cohort 映射缺失。

Known-use 差集保留 P0 的文件存在性元数据结果及 V1 的同值记录：六 family 且 `game.tw-pddl` 存在身份中，train 3553 个、known-use 差集 1141；valid_seen 140 个、差集 0；valid_unseen 134 个、差集 74。相应 candidate identity hashes 见 JSON。由于 V1 发生过上述硬编码输出目录范围偏差，这些值不被提升为 clean/held-out 认证或可执行 N；它们只是 known-use 登记补集。exact task-trial 不相交也不能证明相似 scene/layout/prompt 无泄漏。

## 预算和计数更正

权威 R19 成本不变：G3 增量 4,965 generations、7,273 non-reset operations + 334 resets = 7,607 environment operations；含先前失败前驱的累计为 5,142 generations、7,603 non-reset + 346 resets = 7,949 operations。历史失败单元的成本没有归零。

V1 把 `training_result.json` 的 `wall_time_seconds=27406.28269892931` 错标为 GPU 时间，现撤回：这是 wall-clock 时间，GPU device-seconds 为 `UNKNOWN_NOT_PROVEN_BY_WALL_TIME`。`input_tokens_seen=23860000` 应保留原指标名；该 JSON 本身不足以证明 padding 语义，因此“padded input tokens”更正为语义未知；不与 completion-target tokens 合并。2354 optimizer steps 保留，且该历史训练成本不属于 R19 campaign 总数。

专家集重复计数更正：重复 occurrence **去重前 148、去重后保留 127、去重移除 21**；110 个 rendered-prompt groups 有不同 action targets。127 是去重后计数，不是去重前计数，亦不表示 21 个 identity/hash 错误。

用户冻结的未来最小评价限于 A / B_pool / C_student 三臂，不含 controller、probe 或 replay。因此在 E 个任务、H=50 且每步至多一次 generation/action、每 episode 一次 reset 的限定下，`C_extra=0`、`R_extra=0`，上界为 `150E` generations、`153E` environment operations（含 reset）。现在不选择 E、不执行、不授权预算；将来若增加额外操作，须单独冻结并授权预算，不能从公式留白中默认扩额。

本 V2 scientific calls 仍为 0；没有模型、环境、训练、评价、replay、项目 analyzer/validator 或 pytest 调用。保持停止状态。
