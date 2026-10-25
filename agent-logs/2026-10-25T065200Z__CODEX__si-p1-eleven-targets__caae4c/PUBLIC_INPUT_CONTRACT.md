# SI-P1 公共P0输入与学习目标证据契约

状态：STATIC_AUDIT_ONLY / DRAFT_NOT_EXECUTABLE。它定义这11例的审计字段与边界，不修改生产prompt、parser、协议或训练数据。

## 静态源码与原运行绑定

- [src/sft/protocol.py:56](/home/lizening/wt-r19-g4-consumer-contract-repair/src/sft/protocol.py:56)：sft_p0_prompt只渲染goal、当前obs、H4已完成action/result、有序indexed map；history_window固定4。
- [src/models/action_parser.py:89](/home/lizening/wt-r19-g4-consumer-contract-repair/src/models/action_parser.py:89)：按原valid_actions顺序从A000连续编号；ID是临时映射，不能跨状态搬用。
- [src/sft/policy.py:54](/home/lizening/wt-r19-g4-consumer-contract-repair/src/sft/policy.py:54)：实际policy用user chat template、add_generation_prompt=True、thinking=False，再tokenize/generate。本轮只读，未调用任何方法。
- [src/sft/r3.py:39](/home/lizening/wt-r19-g4-consumer-contract-repair/src/sft/r3.py:39)、[r3.py:71](/home/lizening/wt-r19-g4-consumer-contract-repair/src/sft/r3.py:71)：历史source前缀的action/result及history构造；[r9.py:32](/home/lizening/wt-r19-g4-consumer-contract-repair/src/sft/r9.py:32)对应完整public replay。
- [src/env/alfworld.py:58](/home/lizening/wt-r19-g4-consumer-contract-repair/src/env/alfworld.py:58)：reward=float底层reward，done=底层done，info放metadata；没有won到reward的转换。因此不把缺失won当已验证终局success。

`historical_contracts.json`列四个原运行代码SHA、上述prompt/map/env.step在Git对象中的行位置/文件SHA/方法AST SHA及冻结85对照，12个读取均exit0且对应AST相同；真实子进程receipt在 `historical_contract_read.receipts.json`。这是静态源码身份，不证明历史weights/tokenizer解析版本或当前installed ALFWorld包就是当时字节。

## 投影字段、时间与hash

投影哈希仅编码下列原字段，不带target、case id、canonical task id、d、stratum或K：

| 字段 | 原source指针 | 时间约束 |
|---|---|---|
| goal | /task/text | reset后已知 |
| observation | /steps/d/observation | 当前actor动作前 |
| recent_action_result_transitions | j=max(0,d−4)…d−1：/steps/j/action及/steps/(j+1)/observation | action已执行，result最迟在state d已知 |
| ordered_action_map | /steps/d/valid_actions按原顺序枚举为[Axxx,command] | 当前动作前完整列表；不取post-action metadata动作表 |

`projection_sha256`对上述字段的ASCII JSON（sort_keys=True、紧凑comma/colon）计算；ordered map是pair list以保留顺序。`full_public_prefix_field_sha256`另绑定0…d公共obs、0…d−1原actions、0…d动作表与goal。这些是明确命名的审计表示，不冒充原R8/R15完整prefix签名或chat-template/tokenizer序列。已有repo map/H4摘要只有在静态编码一致时核对，原件hash与新投影hash不混比。

原source actor存储的public prompt在11例均与静态P0规则在内存中产生的公共文本逐字节相同；只导出各字段及文本hash，不导出完整prompt、rendered-chat文本或训练JSONL。没有tokenizer，不能声称验证了未来训练序列、EOS、mask/packing或token预算。

明确排除：原source当前推荐动作/raw output/当前action后result/reward/done及metadata.environment、teacher诊断/subgoal/card、终局label、未来suffix/K/oracle、facts/专家计划。metadata.environment是post-action字段，即使包含won也只可作独立终局证据，不能作为pre-action输入。原始JSON可能含这些审计元数据，但投影白名单不读取它们构造学生输入。

## 目标与执行证据

本次目标仅第一adapter-off恢复Stage2原输出。核对原始raw ID、原parser selection、原id_to_command全部条目、P0有序map、原command、执行flag及transition；不调用生产parser或项目validator。若ID顺序不一致则REINDEX_REQUIRED，不自行换ID；malformed/unexecuted/失配标EXCLUDE_INVALID或HOLD并保留原行。不能把teacher原prompt移植到P0。

R19以K1 recovery_generation_event_ids中的Stage2、stage_two_attempt=1及recovery_transition_event_ids中的action index1绑定；原prefix replay31步作为投影来源，K1 checkpoint后的replay32步只用于历史suffix状态恢复证据。没有把K2目标或SFT suffix当第一恢复目标。

adapter-on SFT suffix只记独立producer/来源/步数/行为摘要；它不是adapter-off目标，也没有逐步0→1标签。空suffix可能是恢复动作直接终局，不能据空列表断言数据丢失。相同suffix行为hash不等于physical generation alias；同task多prefix仍是同一独立任务组。

## 独立轴与不可升级的结论

| 轴 | 本次结果 | 不能升级为 |
|---|---|---|
| 输入/目标/replay机械来源 | 11/11记录匹配；其中结合显式终局证据支持9，另2 HOLD | 11条合格训练行或数据验收PASS |
| 模型身份 | 历史10 PARTIAL；R19原receipt 1 PINNED | UNKNOWN机械FAIL或历史版本由R19倒填 |
| 终局corroboration | 9显式done/won/reward；R4恢复won缺失、R19两侧won缺失 | 任意正reward=环境won、塑形reward误当success |
| 公共字段投影 | 11个不同投影；无本固定集exact同输入多目标 | 全pool无歧义/输入充分或训练token已验证 |
| 学习/机制 | NOT_PROVEN；B_pool未就绪 | 被救回就能正迁移或C>B_source证明采纳机制 |

Dispositions是此线程审计分类，不是独立review权限。合格训练N仍未建立，DATA_FEASIBILITY=NOT_READY。当前只设计与审查，不改变任何科学执行行为。
