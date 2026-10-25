# SI-P0 自身经验可学习性审计

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

| Source | 已完成 episode / canonical tasks | 普通自身成功 episode | 提示与 raw output | 动作映射绑定 / decisions | 已记录 input tokens 范围 |
|---|---:|---:|---:|---:|---:|
| SPRINT_SOURCE | 200 / 124 | 21 | 8926 / 8926 | 8920 / 8926 | 364–1685 |
| R1_SOURCE | 60 / 60 | 47 | 1431 / 1431 | 1431 / 1431 | 231–1456 |
| R7_SOURCE | 120 / 120 | 94 | 2935 / 2935 | 2935 / 2935 | 230–1344 |
| R14_SOURCE | 180 / 180 | 136 | 4313 / 4313 | 4313 / 4313 | 230–1310 |
| R19_SOURCE | 127 / 127 | 120 | 2046 / 2046 | 2046 / 2046 | 228–1274 |

Source 成功为普通自身成功候选，不是 rescue。后续 CONTINUE 常复用 source suffix；不能把两份证据重复当两次经验。所有 horizon 固定为 50；前缀的剩余额度见逐条索引。

| 历史证据 | 状态数 / canonical tasks | CONTINUE 成功 | 处理成功 | rescue / neutral成功 / neutral失败 / harm |
|---|---:|---:|---:|---:|
| SPRINT2C | 120 / 73 | 20 | 19 | 2 / 17 / 98 / 3 |
| R4 | 24 / 23 | 11 | 12 | 1 / 11 / 12 / 0 |
| R10_OSR | 48 / 47 | 22 | 25 | 5 / 20 / 21 / 2 |
| R11_PBR | 48 / 47 | 22 | 23 | 6 / 17 / 20 / 5 |
| R16_OSR | 60 / 60 | 29 | 31 | 4 / 27 / 27 / 2 |
| R17_PAR | 60 / 60 | 29 | 33 | 5 / 28 / 26 / 1 |
| R18_C1 | 60 / 60 | 29 | 32 | 5 / 27 / 26 / 2 |
| R18_C2 | 60 / 60 | 29 | 30 | 3 / 27 / 28 / 2 |
| R19 K1，eligible | 36 / 36 | 30 | 29 | 1 / 28 / 5 / 2 |
| R19 K2，eligible | 36 / 36 | 30 | 30 | 2 / 28 / 4 / 2 |
| R19 K3，eligible | 36 / 36 | 30 | 28 | 2 / 26 / 4 / 4 |
| R19 K4，eligible | 36 / 36 | 30 | 25 | 1 / 24 / 5 / 6 |
| R19 K5，eligible | 36 / 36 | 30 | 24 | 0 / 24 / 6 / 6 |

neutral成功/失败分列，避免把“恢复后也成功”误称“恢复造成的成功”。以上是不同 actor/处理/分层样本的描述，不能跨表求一个自然 recovery 成功率。本轮没有重新计算检验、置信区间、oracle 或新策略效果。

| 阶段 / 处理 | 实际 rescue prefix IDs（相对同前缀 CONTINUE） |
|---|---|
| SPRINT2C | P033, P050 |
| R4 | R2-F01 |
| R10_OSR | R8-F02, R8-F20, R8-F21, R8-F22, R8-F23 |
| R11_PBR | R8-F02, R8-F16, R8-F20, R8-F21, R8-F22, R8-F23 |
| R16_OSR | R15-F01, R15-F22, R15-F23, R15-F25 |
| R17_PAR | R15-F01, R15-F22, R15-F23, R15-F24, R15-F29 |
| R18_C1 | R15-F01, R15-F22, R15-F23, R15-F24, R15-F27 |
| R18_C2 | R15-F01, R15-F22, R15-F23 |

R12 是对 R8/R9/R10/R11 的机制审计，新增 episode 为 0。R11 的 6 次相对 CONTINUE rescue，不等于相对 OSR 的 6 次增益；正式报告只记录 PBR vs OSR 的 1 win /3 losses。R17 的 5 次相对 CONTINUE rescue 同样不等于 5 次相对 OSR 的增益。

### R19 原件中两次 K2 实际救回

原始 branches 文件 SHA256 `eff9b5e74d3d5daa928cb662dcc59fc3f434f66796b673679d40b374f3c8636f`；下面两行的 CONTINUE=0，K2=1，均来自 failure 队列。row SHA256 包含原 JSONL 行末换行；完整事件引用见 `evidence_contracts.log` 和 inventory。

- `R19-failure-a33d7ca26ecbe46dc4b6`，原JSONL第5行，`pick_clean_then_place_in_recep-Ladle-None-Drawer-30/trial_T20190907_194033_752745`；row SHA `716d5b71579334b9cee91cc12f738c0bd0f0747d8a4ed008adb1277822e60042`。K2为2次recovery action后接7次SFT action，SFT终局 environment_terminal；arm event `d98b32e28ebf0285b1c348c29f5db110b900ec73c8665cd1d411f89dc6483a09`。
- `R19-failure-b3ab21b8e193f6adf6ff`，原JSONL第6行，`look_at_obj_in_light-Vase-None-DeskLamp-303/trial_T20190907_150403_049073`；row SHA `15049449b94f7d5bfa85c62fbe626a0705fe04cdcebc3719d345bce5bab434f6`。K2为2次recovery action后接15次SFT action，SFT终局 environment_terminal；arm event `611dfb57ea1d891d9dfacda4a26f398ad5c6d20bf274e2cdaf1e93310c589d25`。

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

- `SPRINT2C`: [pairs.jsonl](/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/corpus/sprint2c-paired-20260820T143604Z/pairs.jsonl)，31310814 bytes，SHA256 `785ffc5712b97fafc4ee9965e52eacef4bc390f7dfe4e8e227cc3cf38761f831`。
- `R4`: [pairs.jsonl](/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/validation/sft-recovery-feasibility-r4-20260908T080000Z/pairs.jsonl)，3790580 bytes，SHA256 `6f53ac7434bfb84f68de88d31730ad2206194d77f4aac7c134ce562cd81d2415`。
- `R9_CONTINUE`: [continue_branches.jsonl](/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/validation/persistent-recovery-replay-continue-r9-20260909T033000Z/continue_branches.jsonl)，34703287 bytes，SHA256 `b04ea7cbea1ddd5818a2875e6a806b468e6db03afed09cfeaa792f8a05af2e99`。
- `R10_OSR`: [osr_branches.jsonl](/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/validation/persistent-recovery-osr-control-r10-20260909T000000Z/osr_branches.jsonl)，35436058 bytes，SHA256 `ef953743d95fea93fb48b43a68b4b1b470aaee910becedfbfe4fd2c10008a76e`。
- `R11_PBR`: [pbr_branches.jsonl](/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/validation/persistent-recovery-pbr-comparison-r11-20260909T000000Z/pbr_branches.jsonl)，45877925 bytes，SHA256 `61b2c3c8250ce3f07a97ebf5f9dd2ce5fad63c5b53a76bb93e9bdad646c6af8f`。
- `R15_CONTINUE`: [continue_ledger.jsonl](/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/validation/progress-aware-recovery-r15-b-20260910T000000Z/continue_ledger.jsonl)，45868962 bytes，SHA256 `30acd05a5ef7d0a0a2f71967fecff643374c844e8ee21a7914c188c23e7c91ce`。
- `R16_OSR`: [osr_ledger.jsonl](/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/validation/progress-aware-recovery-r16-osr-20260910T000000Z/osr_ledger.jsonl)，48207142 bytes，SHA256 `548d06f7479e33306780d2c3434d1888957f0d4b42da6e4f510d949db310bacf`。
- `R17_PAR`: [par_ledger.jsonl](/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/validation/progress-aware-recovery-r17-par-20260911T000000Z/par_ledger.jsonl)，48867616 bytes，SHA256 `ce79cb9f0509d0cb51732fcc482891d7290ee93aa1d81a78ae81a6c071c6ec56`。
- `R18_C1`: [fact_text_branches.jsonl](/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/validation/progress-aware-r18-c1-20260911T000000Z/fact_text_branches.jsonl)，8191574 bytes，SHA256 `1f4d5da2e58636afb728aac86a24a484fddc830c46704eedb5a44d7d23f1cfc2`。
- `R18_C2`: [card_v2_branches.jsonl](/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/validation/progress-aware-r18-c2-formal-aa9fa3c34520941e/card_v2_branches.jsonl)，8339863 bytes，SHA256 `b44c6e8fb4173f0be06e2f1d94af7bba40e030325f0cecd8f2f56ebc32b7d3e5`。
- `R19_BRANCHES`: [branches.jsonl](/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z/branches.jsonl)，1482426 bytes，SHA256 `eff9b5e74d3d5daa928cb662dcc59fc3f434f66796b673679d40b374f3c8636f`。
- `R19_SOURCE`: [source_trajectories.jsonl](/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z/source_trajectories.jsonl)，19726633 bytes，SHA256 `c6f37a7da28e326c70818524c79c17bbd85a286754c111f17db07cbe151a4f1c`。
