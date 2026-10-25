# SI-P0 — 历史 SFT 原始证据与数据来源审计

状态：`PARTIAL_RAW_EVIDENCE_AUDIT`。本记录是已保存证据的只读核验，不是新实验、训练、效果复评授权、整篇论文 PASS 或执行许可。

## 范围与方法

任务单 SHA-256：`9f93c9d1eec2fd44ef50f9528c87aaf2f2df449f35ae569a113d1943bceb1f29`。审阅树起始身份为 `/home/lizening/wt-codex-r18c2`、`agent/codex-r18c2`、`e537f441010077123a307e9d50ea40cf8dad8547`，起始 worktree clean。只用 Python 标准库流式读取已有 JSON/JSONL、配置、报告及原始源文件哈希；未 import 项目运行时代码，未加载模型/tokenizer/adapter，未访问环境实例、训练、重放、项目 analyzer/validator 或 pytest。审计脚本在本任务目录，审计输出未复制训练数据或模型权重。

## 逐 episode 重数

成功定义采用原始最终步骤的 ALFWorld `alfworld_info.won == true`；`done`、达到 horizon 或 `environment_terminal` 本身不等价于成功。逐条原始轨迹重数如下：

| Arm | 原始 episode | 唯一任务 | 每 family | terminal wins | 配对结果 |
|---|---:|---:|---:|---:|---|
| Base Qwen3-8B | 60 | 60 | 10 × 6 | 3/60 | — |
| SFT LoRA | 60 | 60 | 10 × 6 | 48/60 | 45 base-fail→SFT-success，0 base-success→SFT-fail，15 ties |

60 对逐项的 task ID、train split、family、seed 7000–7059、schedule index、reset 顺序、50 步 horizon、初始 observation hash 和 reset metadata hash 全部吻合（0 个 mismatch）。两 arm 的报告汇总数与原始 JSONL 一致。逐 case 表在 `case_level_sft_bootstrap.json`，均不复制原轨迹文本。

Base arm 有一条必须保留的失败记录：`look_at_obj_in_light-CellPhone-None-DeskLamp-320/trial_T20190908_093231_036941` 只记录 1 个 step，`termination_reason=selection_failure`、`truncated=true`，最终没有 `won` 字段。它占据唯一 episode 身份且在分母内，是原记录中的失败/协议错误，不是缺失 task；现有证据不能证明它之前/之后不存在未保存尝试。另 59 条 base 与全部 60 条 SFT trajectory 都有完整记录。原件没有独立启动 receipt，所以“60 条可配对结果”有强原始事件支持，但“只启动过一次、没有被丢弃或重试的运行”并未被运行收据证明。

历史报告与原始轨迹哈希一致：base JSONL `fe145bed8ea49350198c0c0e458df9e47252632e663dac5a2dfa3f17f3fe7759`；SFT JSONL `3509c6d45c6ce8dada1a132b5e9af2a65c898f8565ab06d9714a8a491842b3dc`。统计结果复现的是历史冻结任务上的描述性配对比较；因 base 的当时精确权重 revision/runtime receipt 缺失，模型身份绑定不能提升为完整环境可复现证明。

## valid_unseen 与 valid_seen

G1 `valid_unseen` 有真实原始 60 条 trajectory、实际 run manifest、summary 和冻结的 60 项 schedule。60 个 identity 与 schedule 一对一吻合，10/family，seeds 9000–9059、50 步 horizon，逐案 mismatch 0；原始 terminal `won=true` 为 **49/60**，与 summary 相同。trajectory SHA-256 `aaf6c90fc686eebb8efffd1ef80ef702677426dadbe127d8ca6a6013bc692f8e`；schedule SHA-256 `7ce71ad01bd03ad8a018104f3edacc4310e9a1b5fc6e015d808152f316e4e13e`。该目录是 SFT 单臂，没有同 schedule 的 base arm，因此不能从 49/60 推导 SFT 相对于 base 的 held-out 提升。这里的 49/60 是历史已完成结果，不是未来复测许可。

冻结排除文件记载 valid_seen 的 140/140 个 task identity 已被先前开发/恢复使用，协议将其判为不可用。审计只盘点了这 140 个已消费 ID，没有打开未运行任务 outcome。valid_unseen 60 个 identity 与 SFT 接受数据 1200 个任务及 bootstrap 开发 60 个任务均无交集。身份隔离是本次从保存的 ID 清单核对；不据此声称整个项目/所有未来任务完全无泄漏。

## 数据来源、分母与 checkpoint

版本化报告称语料来自 hand-coded ALFWorld expert 成功轨迹，而非 actor 自己采样；prompt/target 是 public SFT-P0 状态与 expert `Axxx` 动作。这个归类与 JSONL 记录的 `source_split=train`、`source_traj_data_sha256`、`trajectory_sha256` 和 completion/action ID 一致。更强的源文件核验中，初始和 pick-two extension 共 1,273 个 accepted-candidate task identity 的 `traj_data.json` 与 `game.tw-pddl` 都存在于本地原始 train 文件树，2,546 个源 SHA 全部与行记录相符。该直接核验确认行引用的源文件身份，不单独证明专家规划为何成功；hand-coded expert 的作者/流程结论仍依赖 contemporaneous 报告标注。

| 数据层 | 观察到的计数 | 说明 |
|---|---:|---|
| candidate replay / accepted / rejected | 1,869 / 1,273 / 596 | 596 在汇总中均归因 `trajectory_not_successful`；未找到逐 rejected-case 原始记录 |
| initial expert JSONL | 1,140 task / 17,588 rows | `train` 15,720 rows、offline validation 1,868 rows |
| pick-two extension JSONL | 133 task / 4,339 rows | 初始集无 identity overlap |
| accepted candidate union | 1,273 task | 初始与 extension union 正好重数到 summary 的 1,273 |
| 未进入 final balanced set | 73 task | 原始初始/extension 中存在，但不在最终 1,200-task accepted split |
| final balanced SFT 数据 | 1,200 task / 20,967 decisions | train 1,074 / 18,828；offline validation 126 / 2,139；每 family 总计 200 task |
| 额外 online development | 60 task | 与最终训练/验证数据 identity 不相交；不是 1,200 训练语料的一部分 |

Balanced JSONL 逐行检查得 1,200 个 task、20,967 个 action labels；所有 `terminal_task_success=true`，1,200 个 source traj hash 与 expert trajectory hash 均非空且唯一，task-step key 无重复。最终数据报告额外记录 exact-row removal 21、prompt-hash duplicate occurrences 148（保留）、accepted split SHA `9c374fafdcc7d7db77e878d23e852a0ec55eedcc3886cb0cebe7491d67e564e5`。专家方案可能比仅凭公开文本的策略更强；这属于监督专家模仿/能力初始化，不是 agent 自己从交互经验中改进。

训练结果原件 SHA-256 `e6a47124200cacba4d1f3eaf97fdf79657d7df04f072a4d5446c2bec677c399e`；记载 2 epochs、2,354 optimizer steps、27,406.3 秒、最低 offline validation completion loss 0.06381698、选 checkpoint-2354。checkpoint-2354 `trainer_state.json` 独立记录同一步数、best metric 与 best checkpoint；训练配置明定只能按 offline validation loss 选 checkpoint，禁止用 online outcome。当前 adapter directory hash 逐文件按项目记录格式只读复算为 `6e403d85b150a74dfcc176f1f180ce4baf6fdacd922d2f96b3ceef0a21100f11`，与 training result、online evaluation、G1 报告声明相符；未加载任何权重。训练成本可描述为此训练 receipt 报告的约 7.61 小时及 23.86M padded input tokens，不与 R19 campaign 成本相加。

## 具体 provenance 缺口 / 矛盾

- `sft_training_protocol.json` 自身被 run config 的 protocol SHA `dd06d087...` 引用；但其中声明的 split SHA `e6695359...`、exclusion SHA `8e0d04d3...` 与当前相应原件 `sft_task_splits.json` SHA `53471633...`、`sft_task_exclusions.json` SHA `fdbe3b1c...` 不同。本地找到的 report/dataset summary 又明确引用当前 534/9c/fd 三个 manifest 版本。原先 e669/8e 的文件版本未定位。此处是保存文件之间可复核的字节级绑定冲突，标为 `CONTRADICTED`；不能据此倒推实际训练进程一定加载了错误 split，也不能悄悄把旧 protocol 改写成一致。
- Adapter 当前 bytes、训练结果与 checkpoint 选择记录相互吻合；但 adapter config 的 `revision` 为 null，未找到 contemporaneous base-model/tokenizer commit 或 full loaded runtime receipt。`Qwen/Qwen3-8B` 只是模型名，不是精确权重 revision。当前 Hugging Face cache/model snapshot 不作为过去加载证明。
- SFT bootstrap online trajectory/report 原件存在，但其目录未找到配套 online `run_manifest.json` 或独立 launcher/supervisor receipt；因此历史基础模型精确 snapshot、环境版本与被丢弃/重试运行数仍 `NOT_PROVEN`。
- 找到 aggregate 所称 596 rejected 次数/原因，但没有逐 candidate rejected 原始记录。接受候选到 final balanced 中另有 73 task 未被选用；可从 identity 列表确认为未纳入，不能把它们算成被拒绝或失败。

## 可引用主张与论文影响

最强可支持表述：**在固定的 60 个已消费 train-development task identity 上，保存的 Base/SFT 原始轨迹逐项匹配；记录到 base 3/60、SFT 48/60、45 个 fail-to-success、0 个 success-to-fail。SFT 标签来自 ALFWorld train split 的成功 hand-coded expert 轨迹，是 supervised expert-policy imitation 的能力 bootstrap。**同时披露一个 base selection-failure episode，以及历史精确 base/tokenizer/runtime revision 和 bootstrap 启动 receipt 缺失。

不能据此称为自主 self-improvement、在线自训练闭环、一般性最优方法，或精确 base revision 已独立验证。valid_unseen 的 49/60 是唯一 SFT arm 的已完成结果；没有同 schedule base control，不能称为 causal held-out gain。不能将 valid_seen 已消费身份重标成 held out。

48/60 vs 3/60 是论文主表潜在的重要能力基座证据，但“专家模仿”与 provenance 限制必须同表披露；valid_unseen 应独立作为单臂描述性泛化结果，禁止写成配对提升。该审计不是 whole-thesis pass，也未做系统新颖性检索。

## 自身轨迹原件入口与成本边界

可供协调方后续单独审阅的入口列于 `OWN_TRAJECTORY_ENTRYPOINTS.md`。本轮只定位 R1/R7/R3/R9 与既有 R19 原件，不筛选学习样本、不将任何 outcome 转成训练数据；R19 G3/G4 原件、2da980f source、run `260422ac02bd42a8b2929d7ef240526b` 和已消耗 clearance 保持不变。

R19 campaign 成本仍为 **5,142 generations / 7,949 environment operations（含 resets）**；其历史前驱为 177 / 342。历史 SFT 训练成本不包含在这两个 R19 campaign 数字内，也不宣称这两个数字是全项目总成本。本轮新科学调用为 0。

## 本地证据文件

机器可读逐项审计与 input SHA/size 在 `sft_raw_evidence_audit.json`；case-level 表在 `case_level_sft_bootstrap.json` 和 `case_level_valid_unseen.json`；全量路径清单在 `raw_artifact_inventory.json`。所有文件为本任务私有目录的 `LOCAL_ONLY` 产物，等待协调方独立验收；未改科学树、共享 INDEX 或原始证据，未 commit/push。
