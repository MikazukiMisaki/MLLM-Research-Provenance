# Luna — SI-P2独立身份、去重容量与预算证据

用户授权的实际新任务。先读共同规则COMMON_AUDIT_RULES.md及固定manifest，核验SHA。唯一可写目录：/home/lizening/research-notes/agent-logs/2026-10-25T075610Z__LUNA__si-p2-pool-independence__b04b8b。必须使用新脚本OWN=Path(__file__).resolve().parent并assert精确新目录；**不得执行或改动任何P0/P1旧脚本/旧输出**。本轮不读取Sol Research进行中的文件。

独立从171个原branch行核对fullfile/row SHA、canonical task/trial、d/H、原CONTINUE/recover标签及已有source index；R19只看K1。身份元数据与上一轮已封存known-use 2612集合、expert_train/validation/online与各split登记做交叉，不读取未消费task payload。报告跨阶段同task、same-task multi-prefix、known split/teacher来源、原11去向的metadata。可以读原branch完整性字段，但不运行项目validator。

冻结算法自己实现并交叉核对：先在全部171有效身份记录上给**过滤前**hash-anchor计划（此不是质量后结果），含每task所有候选key、选择行和labels、B/C原始可分性；不是替Sol确认Q_hist，也不得把preQ数量当最终。协调方收到两份冻结交付后会把独立Q mask接入你的原始索引，复算Q后anchor和最终容量。无需等待Sol或读取其临时表。

物理alias只接受明确event ID等原receipt；legacy无事件ID未知，不因语义相同就宣称物理复用。逐来源统计candidate、success、rescue、neutral-success及task数量。量化同task跨来源和旧expert task overlap，但没有原训练prompt全hash时不声称输入从未训练。推理raw输出token只能列为已有计数，prospective supervisedtokens仍UNKNOWN。

成本仅携带已审R19累计5142/7949（旧177/342已含）、历史SFT不同单位，不重建模型或环境；写独立获取成本/共享实物成本/未来训练和150E/153E评估公式的缺项，不能将历史获取未知写0或生成预算授权。重点回答最多有多少独立task/first-target、来源和family偏斜，以及什么信息仍使“够不够”无法成立。不要为数据充分自行设最低n或新schedule。

交付POOL_IDENTITY_AND_CAPACITY.md、pool_identity_audit.json、parent_anchor_plan.json、COST_LIMITS_NOT_EXECUTABLE.md、原始commands/实际receipts/前后hash、RECORD.md和FILE_HASHES.sha256。只读软件核验、无训练/模型/环境/新实验；无commit/push/sharedINDEX或其他agent字节写入。先ACK，45分钟进度/60分钟首轮上限，完成冻结等独立审查。
