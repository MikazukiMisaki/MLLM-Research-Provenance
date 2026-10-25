# SI-P2 同池共同质量与对照可分性审计

这是固定171原行的既有证据审计，科学增量0。结果：**Q_hist机械质量164 PASS、0 HOLD、7 EXCLUDE；固定去重/anchor后162任务，B_pool=95、C=10、B\C=85。集合可分已获本轮记录支持；等预算学习对照仍未建立，训练N未建立，学习收益NOT_PROVEN，数据整体NOT_READY。** PASS仅是开发侧指定质量项核对，不是独立审查通过、训练数据验收或新执行许可。

唯一任务单SHA256 1fd57bda79a38b14d96a3543d5d325fa581fd11124c5bef6901f8f0b7a88f93a；共同规则 ab5e3afe8bb1e65ae1473254810ba56dfa769cefbd0952d0b2a0bdb32368ea69；固定171行manifest a3e2548e89280d150cbe83cceca632f9f91275ede0a4a9d89133e53691826078。parent为R4 24、R10_OSR 48、R16_OSR 60、R19_K1 39，共169个canonical task/trial。没有补样、增加K2–5目标、PAR/cards或suffix目标。

## 审计方法与边界

每条原行与manifest的line/SHA/task/prefix绑定。读取原source的完整动作前公共前缀，按固定P0字段构造goal、当前observation、最近4个action/result transition和原有序完整admissible map的摘要，静态公共P0文本与原actor存储prompt逐字核对。H4第j个动作的结果取原source第j+1状态；当前source动作/输出及其后状态、teacher subgoal/card/facts、奖励/won、未来suffix不进入学生输入。这里只比较字段和公共文本，不加载tokenizer、不认证新chat渲染，也不导出训练prompt/JSONL。

R4结合完整R3原replay与R4自身当前state/map/H4 hash收据；R10直接核对原replay transitions及全部前缀map；R16核对原source/current/H4摘要、逐步7项equality收据和分支/ledger完整前缀hash绑定；R19核对initial原prefix reset/replay事件、source动作前状态/有序map/history和第一recovery事件。R16使用原逐步equality收据支持过去状态，未重新产生环境状态。所有结论都是原证据的完整性核对。

原Stage1合法、Stage2完整与bare ID/selected、teacher与P0逐ID映射、实际执行command/transition均独立核对。恢复目标只取已执行的第一adapter-off动作；adapter-on suffix仅用于原完整分支成功/停止依据。失败分支按原horizon/selection fail-closed等语义审计，未要求失败必须done=true。合法首动作终态允许空suffix。

成功按原done&&reward>0及原停止语义追溯；缺won单列RAW_WON_NOT_RECORDED，不构成新G3失败或非法动作。原成功标签全部保留。三个独立判断轴继续为机械来源链、模型身份、学习收益；终态原始佐证另列。

历史R4/R10/R16 weights/tokenizer确切revision及loaded角色绑定为PARTIAL，不据此机械FAIL、不用当前cache反填；R19依原execution/runtime receipt绑定base/tokenizer snapshot、两个loaded commit、adapter hash及开关角色。Q_pin严格按预设更强身份过滤，独立执行同一后续流程，不取代主口径。

## 固定流程

anchor规则由任务单预先固定；正式审计进程在读取parent记录前由identity-only manifest写入anchor_keys_pre_outcome.json。此前字段形状probe已读取既有结果，因此这里不声称首次接触结果之前封存hash或人类盲法。实际anchor选择函数始终只接收质量及身份/目标摘要、无结果label，并在连接结果label划分B/C之前固定选择。key使用真实LF：SHA256("SI-P2-anchor-v1"+LF+canonical_task+LF+stage+LF+prefix_id+LF)。质量后只对认证shared generation-event/physical alias去重；legacy无事件ID则physical reuse NOT_PROVEN。随后跨阶段每task取最小key（平手case_id），再对anchor的exact公共projection+command去重，slot不回填；最后才将既有label连接为B/C。selection_inputs_without_outcomes.json记录选择函数的无label输入。历史结果并非人类盲法，不把固定hash处理称作盲法。

| 口径/阶段 | 行 | task | B | C | B\C | harm | failure |
|---|---:|---:|---:|---:|---:|---:|---:|
| Q_hist/RAW | 171 | 169 | 99 | 11 | 88 | 6 | 66 |
| Q_hist/QUALITY | 164 | 162 | 96 | 11 | 85 | 6 | 62 |
| Q_hist/PHYSICAL_DEDUP | 164 | 162 | 96 | 11 | 85 | 6 | 62 |
| Q_hist/TASK_ANCHOR | 162 | 162 | 95 | 10 | 85 | 6 | 61 |
| Q_hist/EXACT_INPUT_TARGET_DEDUP | 162 | 162 | 95 | 10 | 85 | 6 | 61 |
| Q_pin/RAW | 171 | 169 | 99 | 11 | 88 | 6 | 66 |
| Q_pin/QUALITY | 36 | 36 | 29 | 1 | 28 | 2 | 5 |
| Q_pin/PHYSICAL_DEDUP | 36 | 36 | 29 | 1 | 28 | 2 | 5 |
| Q_pin/TASK_ANCHOR | 36 | 36 | 29 | 1 | 28 | 2 | 5 |
| Q_pin/EXACT_INPUT_TARGET_DEDUP | 36 | 36 | 29 | 1 | 28 | 2 | 5 |

Q_hist无有证据的跨候选共享物理generation重复被删除；Q_hist通过的legacy128行无认证共享event ID（原parent legacy合计132行），不把语义相同suffix当物理复用证明。两个重复task由固定hash删去一条failure前缀和一条rescue前缀；exact输入-目标去重再删除0条，Q_hist内same public input群组0个。全部171行有最终去向，非anchor仍保留质量结论，不补选更有利prefix。

## 来源与家族

下表为最终Q_hist anchors；所有中间阶段、Q_pin来源/家族分解见pipeline_counts.json。

| 来源 | 行/task | B | C | B\C | harm | failure |
|---|---:|---:|---:|---:|---:|---:|
| R4 | 23/23 | 12 | 1 | 11 | 0 | 11 |
| R10_OSR | 46/46 | 24 | 4 | 20 | 2 | 20 |
| R16_OSR | 57/57 | 30 | 4 | 26 | 2 | 25 |
| R19_K1 | 36/36 | 29 | 1 | 28 | 2 | 5 |

| 家族 | 行/task | B | C | B\C | harm | failure |
|---|---:|---:|---:|---:|---:|---:|
| look_at_obj_in_light | 22/22 | 20 | 6 | 14 | 0 | 2 |
| pick_and_place_simple | 23/23 | 17 | 1 | 16 | 2 | 4 |
| pick_clean_then_place_in_recep | 20/20 | 16 | 0 | 16 | 1 | 3 |
| pick_cool_then_place_in_recep | 24/24 | 19 | 0 | 19 | 1 | 4 |
| pick_heat_then_place_in_recep | 24/24 | 18 | 1 | 17 | 2 | 4 |
| pick_two_obj_and_place | 49/49 | 5 | 2 | 3 | 0 | 44 |

## 全部排除与原11项去向

以下7行均有无效Stage1和第一动作未执行证据；原分支结果仍保留，排除训练候选不改变原科学结果。

| case | 原CONTINUE→recover | 理由 |
|---|---|---|
| R10_OSR:R8-F10 | 0→0 | STAGE1_INVALID:diagnosis_too_long; FIRST_ACTION_NOT_EXECUTED |
| R16_OSR:R15-F24 | 0→0 | STAGE1_INVALID:subgoal_too_long; FIRST_ACTION_NOT_EXECUTED |
| R16_OSR:R15-F28 | 0→0 | STAGE1_INVALID:diagnosis_too_long; FIRST_ACTION_NOT_EXECUTED |
| R16_OSR:R15-S04 | 1→1 | STAGE1_INVALID:truncated_stage_one; STAGE1_TRUNCATED; FIRST_ACTION_NOT_EXECUTED |
| R19_K1:R19-failure-22984d06767be55e8b1a | 0→0 | STAGE1_INVALID:subgoal_too_long; FIRST_ACTION_NOT_EXECUTED |
| R19_K1:R19-random-control-892da8a85142c10ddc4e | 1→1 | STAGE1_INVALID:diagnosis_too_long; FIRST_ACTION_NOT_EXECUTED |
| R19_K1:R19-random-control-6baa1b9cd932f23ba51d | 1→1 | STAGE1_INVALID:diagnosis_too_long; FIRST_ACTION_NOT_EXECUTED |

| 原P1 case | Q_hist | 固定去向 | 最终C | Q_pin |
|---|---|---|---|---|
| R4:R2-F01 | PASS | FINAL_ANCHOR | True | HOLD |
| R10_OSR:R8-F02 | PASS | FINAL_ANCHOR | True | HOLD |
| R10_OSR:R8-F20 | PASS | FINAL_ANCHOR | True | HOLD |
| R10_OSR:R8-F21 | PASS | FINAL_ANCHOR | True | HOLD |
| R10_OSR:R8-F22 | PASS | FINAL_ANCHOR | True | HOLD |
| R10_OSR:R8-F23 | PASS | NONMINIMUM_TASK_ANCHOR | False | HOLD |
| R16_OSR:R15-F01 | PASS | FINAL_ANCHOR | True | HOLD |
| R16_OSR:R15-F22 | PASS | FINAL_ANCHOR | True | HOLD |
| R16_OSR:R15-F23 | PASS | FINAL_ANCHOR | True | HOLD |
| R16_OSR:R15-F25 | PASS | FINAL_ANCHOR | True | HOLD |
| R19_K1:R19-failure-b3ab21b8e193f6adf6ff | PASS | FINAL_ANCHOR | True | PASS |

11项机械来源链全部继续成立，公共projection和第一目标与P1逐项一致。R8-F22是同task最小anchor，F23不再计独立样本；保留10个unique rescue task。Q_pin只保留R19那一项C，其余历史身份不足保持PARTIAL/HOLD，不伪造机械FAIL。

## 源码边界纠正与真实回执

初稿把token_cap_reached=true直接当截断，误排R19-random-control-47bcdcad9c56a38ac146。原事件Stage1.status=valid、output_complete=true，原生成器允许EOS恰在cap处；原两阶段parser只以output_complete判截断。已静态核对四个真实历史Git对象中的两个parser方法及R19 executed2da生成器，真实读取rc均0；本轮没有运行parser或tokenizer。初稿程序、输出8项、日志和rc=0回执完整保留于draft_v1与common_quality_audit.*；最终v2回执为common_quality_final.receipt.json，rc=0。变化仅使该neutral-success归回Q_hist/Q_pin，C仍10/1，没有为了rescue更换质量/anchor规则。

两个辅助只读候选路径不存在导致一次rg exit2，另一次临时只读打印表达式有SyntaxError exit1；均在RECORD中保留真实工具收据指针，不冒充科学失败。正式新stdlib审计及固定记录检查回执与这些辅助错误分开。

## 可以证明与仍未建立

1. **集合可分：SUPPORTED。** Q_hist B=95、C=10、neutral=85；Q_pin B=29、C=1、neutral=28。两口径每个来源中有C时也有同来源neutral，具体家族分解已列。C仍很少且集中，9/10 C依赖历史PARTIAL身份；严格pin口径只剩单个look_at_obj_in_light任务，不能据此判断学习效果。
2. **等预算对照可实现：NOT_ESTABLISHED。** count层面B/C每臂不同task容量宽上界10（Q_pin为1）；若只用互不重叠neutral/C，按同source+family的count匹配上界也为10/1。它们是容量上界，不是已选训练N、效能样本量或token配平证明。B包含C，若未来独立采样可能重叠，不能把两个集合误称独立数据。即便同source/family，C与neutral仍可能有prefix难度、失败类型、teacher条件差异。
3. **学习数据充分：NOT_READY。** 背景成功数据S、任务/所有历史暴露隔离、实际P0训练tokens、重复次数/采样权重、相同更新预算和独立评估均未在本任务建立。原推理tokens只保留为成本元数据，不替代训练tokens；不得因C=10承诺可学习或统计效能。
4. **学习收益/筛选机制：NOT_PROVEN。** 被恢复成功与学习收益不同；如果未来比较C增益筛选纠错与B同pool success-only，仍需冻结共同来源/生成角色、背景S及更新/token预算、任务隔离和目标可用字段时点。当前不训练、不选择最佳rule，不将adapter-off teacher称作当前actor自采样。除这些条件设计外，本轮不建立新实验或给启动许可。

## 交付与冻结

pool_quality_audit.json含171行布尔项/理由、原label、第一动作ID/command、public摘要、终态won属性、模型轴及两口径去向；绝对文件路径通过file_locations表解析file_id，保留原line、raw_line_sha256和pointer。pool_sets.json给B/C/neutral的完整case/task ID集合；pipeline_counts.json给每阶段来源/家族flow；complete_input_bindings.json与INPUT_HASHES.sha256给原件前后hash。所有输入保持原字节；旧P1两份manifest覆盖的59目标均核对未变。

科学树仍为analyzer85cbb92395e5e2420c2adeb1fa0634653e742910、executedG3 2da980f631badc25086d12db60d128ff507d3ae6，review根e537f441010077123a307e9d50ea40cf8dad8547；均干净。R19累计5142 generations/7949含reset操作（含旧177/342）不变，不是全项目SFT总成本。仅在本轮OWN新增文件，无commit/push/sharedINDEX/rootinventory/旧raw或旧provenance修改，无额外agent/线程消息。未执行任何旧脚本、项目analyzer/validator/pytest、模型/ALFWorld/tokenizer/训练、source/replay/G2/G3/G4/preflight。后续由协调方独立审查与统一发布。
