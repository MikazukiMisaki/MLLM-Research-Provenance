# SI-P1 固定11状态学习目标审计

任务 `SI-P1-TARGET-caae4c`。**DATA_FEASIBILITY=NOT_READY；TRAINING_N=NOT_ESTABLISHED；LEARNING_GAIN=NOT_PROVEN。** 这是自有数据审计结论，待协调方独立审阅；不是独立数据验收PASS或科学启动许可。

## 范围与结果

唯一任务单SHA256 `adcb03193e40baf839e14f9d521e3f7a309c28ce901d6a4dcf1d044660ec579b`，固定11-case清单SHA256 `e5039568d8213fa5d879ffb2aec8c44e932fa99bc4de67bd527ebcae67ccb45b`均匹配。开始root `/home/lizening/wt-codex-r18c2`、branch `agent/codex-r18c2`、HEAD `e537f441010077123a307e9d50ea40cf8dad8547`符合任务。采用P0最终NOT_READY决定，不引用初稿READY作为训练资料就绪结论。

固定11状态/10 canonical tasks全部保留。以纯stdlib核对原JSONL行、source完整公共前缀、既有replay、原始模型输出/map/执行transition和终局；静态读代码/Git对象，未调用任何项目parser/validator或环境。

**精确审计disposition：输入—目标来源链支持9行/8个任务；HOLD_EVIDENCE 2行/2个任务；REINDEX_REQUIRED 0；EXCLUDE_INVALID 0。** 单看输入时点、map、raw ID、执行与既有replay的机械核对，11/11均匹配。另有10例MODEL_IDENTITY_PARTIAL、1例MODEL_IDENTITY_PINNED；9例显式done/won/reward终局，2例缺won。三个轴分别记录，不能将历史revision UNKNOWN伪作机械FAIL，也不能把9行来源支持写成9项合格训练N。合格训练N尚未建立，不以未知等同真实可用样本恰为0。

| 固定case | d / H | 原始目标ID → 实际命令 | 终局won | 身份轴 | disposition |
|---|---:|---|---|---|---|
| R4:R2-F01 | 21 / 29 | `A003` → `go to desk 1` | MISSING | PARTIAL | HOLD_EVIDENCE |
| R10_OSR:R8-F02 | 12 / 38 | `A013` → `move book 2 to bed 1` | 显式true | PARTIAL | INPUT_TARGET_LINEAGE_SUPPORTED |
| R10_OSR:R8-F20 | 42 / 8 | `A005` → `go to desk 1` | 显式true | PARTIAL | INPUT_TARGET_LINEAGE_SUPPORTED |
| R10_OSR:R8-F21 | 35 / 15 | `A002` → `go to desk 1` | 显式true | PARTIAL | INPUT_TARGET_LINEAGE_SUPPORTED |
| R10_OSR:R8-F22 | 23 / 27 | `A004` → `go to desk 1` | 显式true | PARTIAL | INPUT_TARGET_LINEAGE_SUPPORTED |
| R10_OSR:R8-F23 | 28 / 22 | `A004` → `go to desk 1` | 显式true | PARTIAL | INPUT_TARGET_LINEAGE_SUPPORTED |
| R16_OSR:R15-F01 | 14 / 36 | `A001` → `go to cabinet 1` | 显式true | PARTIAL | INPUT_TARGET_LINEAGE_SUPPORTED |
| R16_OSR:R15-F22 | 7 / 43 | `A001` → `examine stoveburner 2` | 显式true | PARTIAL | INPUT_TARGET_LINEAGE_SUPPORTED |
| R16_OSR:R15-F23 | 10 / 40 | `A001` → `examine shelf 6` | 显式true | PARTIAL | INPUT_TARGET_LINEAGE_SUPPORTED |
| R16_OSR:R15-F25 | 6 / 44 | `A003` → `go to desk 1` | 显式true | PARTIAL | INPUT_TARGET_LINEAGE_SUPPORTED |
| R19_K1:R19-failure-b3ab21b8e193f6adf6ff | 31 / 19 | `A002` → `examine dresser 1` | MISSING | PINNED | HOLD_EVIDENCE |

## 逐字段来源与公共输入时点

`eleven_target_audit.json`每case含原分支path/line/行SHA、source episode path/line/行SHA、每字段JSON pointer和hash、完整前缀字段摘要、已有replay记录、map逐ID一致性、原selection metadata、执行transition/hash、终局及模型独立轴。原JSONL行SHA包含原换行；JSON字段摘要采用ASCII canonical JSON紧凑编码。

11例的静态P0公共文本与原source actor当时存储的公共prompt逐字节相同；这是内存中的静态对照，只输出hash，没有导出完整prompt或训练JSONL。task goal来自原source `task.text`，obs和有序actions来自 `steps[d].observation/valid_actions`；H4仅取j<d的已执行action及 `steps[j+1].observation`，j+1≤d。所有episode在该动作之前非终局，剩余horizon为50−d。

旧R1/R7未单独保存result_observation时，next-step pre-action observation与原replay的result逐项对照；没有把缺失字段假造回原记录。R4用完整R3 public replay及R4自己的exact-replay哈希收据，21条原动作/结果闭合；R10用原replay_full含每步公共状态/map；R16用完整source、当前obs/map/H4摘要与14/7/10/6条transition equality receipts。所有当前map、H4和时点核对均匹配。不同schema的summary/replay证据强度和来源在JSON中保留。

一个关键时间边界：`steps[d].metadata.environment`及当前step reward/done/result属于**原source actor执行当前动作之后**，不能拿来构成该动作前学生输入。其facts/expert_plan/won不进入投影。source当前model_output/推荐动作也不进入输入；只用原有pre-action动作表，保持原顺序。

R19仅以K1所引用的第一Stage2 generation和第一recovery transition为目标：stage_two_attempt=1、recovery_action_index=1、actions_consumed_before=31；before-history逐项等于原31步source前缀。原prefix replay31步与K1分支在恢复后的32步replay明确区分，后者不作为原prefix输入。目标是 `A002 → examine dresser 1`，不是后续SFT `look` 或K2目标。没有读取其他K目标来补该case。

## 临时ID、执行与suffix

每例P0 map都由该source时点的有序valid_actions按A000起编号；与原teacher parser的每个ID→command逐项一致，原source policy map也一致。11例原raw output均为相同合法bare ID、selection=selected、Stage1 valid、generation complete且未触cap；实际执行flag/command及transition相符。R19另有直接环境action receipt的before-state/map/command；旧collector以原command/执行flag/transition及静态调用点绑定。没有运行parser、修复ID或重索引。

所有目标属于adapter-off recovery teacher；adapter-on SFT suffix单独记录producer、步数、来源/引用及摘要，**不作为本轮额外训练目标**。原prefix 0→1不能复制成每条suffix action的因果正标签。`R10_OSR:R8-F02`第一恢复行动直接终局，suffix=0是有效已记录结构，不是缺失样本。

R8-F22/R8-F23是同一Book/DeskLamp trial的d=23与28两个前缀，不能计成两个独立task。这11个P0公共字段投影均不同，未观察到exact同输入多目标组；不表示全pool无歧义或公共输入充分。两例R8-F22/F23的后续公共行为序列摘要相同：`4c2493fa1cf07265ebc5e26a2eebc0308e8dcbd35842a5d3d6b73a4a34275843`。这说明重复行为/同task依赖，不能仅凭语义摘要相同断言physical generation被复用。固定集中不新增alias经验计数。

## 终局与reward的严格边界

R10的5例、R16的4例：原CONTINUE终局done=true、reward=0、won=false；恢复分支终局done=true、reward=1、won=true，支持该原环境记录中的0→1。won只作为终局审计证据，不进学生输入。

**R4:R2-F01：HOLD_EVIDENCE。** CONTINUE有done=true/reward=0/won=false；恢复terminal有done=true/reward=1和原success=true，但导出的恢复终局step没有won。它的输入、目标、map、执行与replay支持，新的严格终局corroboration仍缺项。不能凭“use lamp”文字、局部milestone或positive reward补写won=true。

**R19_K1:...b3ab21b8e193f6adf6ff：HOLD_EVIDENCE。** 原CONTINUE source最后done=true/reward=0，K1 suffix最后done=true/reward=1、原K1 success=1；两侧此schema都未保留won，故分别列缺项，绝不伪造won=false/true。第一恢复action本身非终局，不把后续SFT action当teacher目标。

静态历史Git对象证明四阶段的 `AlfWorldTextEnvironment.step`、`sft_p0_prompt`、`action_id_mapping`与冻结85对应方法AST相同，12/12对象读取returncode0。repo wrapper直接转发底层reward/done并把info存metadata，没有把won替换成reward。旧success helper使用done+positive reward；这说明旧标签的计算来源，**不证明任何positive reward都等价于won**，也不把这些原值武断称为塑形reward。当前installed ALFWorld源码请求won=True，但不能用当前包反填缺失历史won。两项HOLD针对本次学习证据要求，不重标旧科学结果、不撤销已完成G3/G4或旧review。

## 模型身份与记录tokens

10个历史case只有模型名Qwen/Qwen3-8B、adapter摘要、代码SHA及部分隔离manifest；weights/tokenizer实际resolved revision保留UNKNOWN。R10/R16有adapter-off恢复与adapter-on actor的隔离字段；R4manifest有双模型加载与adapter摘要，但无当时loaded commit收据，不能补造运行状态。其机械目标有效性与身份完备性分开。

R19 K1原execution/runtime有snapshot revision及loaded commit `b968826d9c46dd6066d109eabc6255188de91218`、tokenizer文件摘要/chat-template摘要、adapter目录 `6e403d85b150a74dfcc176f1f180ce4baf6fdacd922d2f96b3ceef0a21100f11`及active adapter隔离，故身份轴PINNED。此处只引用原receipt，没有加载模型/tokenizer或复验其科学gate。

| case | 原actor同一公共P0输入 tokens | Stage1 input / generated | Stage2 input / generated | 未来训练tokens |
|---|---:|---:|---:|---|
| R4:R2-F01 | 562 | 526 / 32 | 651 / 5 | UNKNOWN |
| R10_OSR:R8-F02 | 378 | 394 / 26 | 461 / 5 | UNKNOWN |
| R10_OSR:R8-F20 | 512 | 468 / 39 | 608 / 5 | UNKNOWN |
| R10_OSR:R8-F21 | 536 | 488 / 32 | 625 / 5 | UNKNOWN |
| R10_OSR:R8-F22 | 563 | 507 / 30 | 650 / 5 | UNKNOWN |
| R10_OSR:R8-F23 | 578 | 522 / 28 | 663 / 5 | UNKNOWN |
| R16_OSR:R15-F01 | 665 | 569 / 25 | 745 / 5 | UNKNOWN |
| R16_OSR:R15-F22 | 702 | 610 / 31 | 788 / 5 | UNKNOWN |
| R16_OSR:R15-F23 | 379 | 379 / 22 | 458 / 5 | UNKNOWN |
| R16_OSR:R15-F25 | 516 | 468 / 39 | 610 / 5 | UNKNOWN |
| R19_K1:R19-failure-b3ab21b8e193f6adf6ff | 488 | 452 / 26 | 571 / 5 | UNKNOWN |

这些是**原已记录推理**tokens，不是新训练tokens；Stage2 generated均5也不能直接把55写成可训练监督token预算。公共文本匹配不等于已验证chat-template/tokenizer/label EOS/packing。所有prospective_projected_training_tokens为null；未加载tokenizer，teacher prompt长度不替代P0训练长度。模型revision UNKNOWN进一步限制历史长度可迁移性。

## B_pool未决条件与停止结论

**只用这11条rescue作为候选pool，success-only的B_pool与增益筛选C将采纳同一组，无法识别筛选条件的增量。** 11个正例核验不等于对照池已经就绪。本轮不扩大到neutral成功样本清洗、不构建pool或训练行。

仍需协调方决定并在未来具体任务闭合：相同生成来源与固定operator的完整候选pool及非rescue成功对照；同一student输入/目标粒度、普通成功背景和曝光分配；未知历史模型身份的可接受范围；两项终局won缺口是否有既存独立原件可佐证；独立canonical身份登记、污染缺项与新任务可用性；prospective实际训练token/重复上限/checkpoint及完整获取/验证/训练/评估费用。身份与预算登记由Luna另行负责，本线程未读取其未完成文件，也不借此造新schedule/预算。

DATA_FEASIBILITY保持NOT_READY。已有证据支持有限来源链审计，不证明学习收益、同pool机制效应或训练资料合格。首轮一次有界核验至此完成；未闭合项逐项HOLD，后续由协调方分配，不为positive扩样、不补跑、不调prompt/selector、不启动训练或新评估。科学85/2da与R19累计5142/7949（含旧177/342）保持，本轮科学增量0。
