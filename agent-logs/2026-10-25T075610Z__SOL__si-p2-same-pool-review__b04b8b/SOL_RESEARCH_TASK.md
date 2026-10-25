# Sol Research — SI-P2共同质量与同池对照

用户授权的实际新任务。先读本目录共同规则COMMON_AUDIT_RULES.md及固定manifest并核验SHA；P1正式review只作基点，不覆盖旧文件。

你的唯一可写目录：/home/lizening/research-notes/agent-logs/2026-10-25T075610Z__CODEX__si-p2-common-quality__b04b8b。读原171候选及必要的source/replay/CONTINUE/manifests和R19原事件引用。P1同11 case可复用其只读ref，不得执行其旧审计脚本或写旧目录。

实现纯stdlib审计，按共同规则对171行逐一给Q_hist PASS/HOLD/EXCLUDE、每项布尔/原因、证据locator/紧凑hash、CONTINUE/recover原标签、first-target actionID/command、public projection digest、physical reuse证据、模型身份/won独立轴。成功/失败路径均覆盖，不用原P0结构summary冒充实际目标核验；容许有效空suffix/first-action terminal，第一action无效/未执行明确排除。source/public完整性从原source record+原replay核对，禁止新replay或运行parser/collector。

严格执行固定dedup/anchor算法，返回精确B/C及B-minus-C的case/task ID集合和各阶段flow，各家族/来源。列原11 positive最终是否留存与原因，不能选择留存最多的hash。Q_pin只按预设算法另列。不生成任何训练样本。

交付COMMON_QUALITY_AUDIT.md、pool_quality_audit.json（紧凑，建议<1MB，不重复全metadata/全prompt）、pipeline_counts.json、完整输入bindings、stdlib脚本/原始receipts、RECORD.md、FILE_HASHES.sha256。必须区分“集合可分”“等预算对照可实现”“学习数据充分”“未知身份影响”，不得从n推学习收益或设训练N。你提供事实和设计限制，我独立验收。

先ACK再开工，45分钟进度/60分钟首轮上限；原件无法闭合要明确HOLD，不额外科学修复/补跑。
