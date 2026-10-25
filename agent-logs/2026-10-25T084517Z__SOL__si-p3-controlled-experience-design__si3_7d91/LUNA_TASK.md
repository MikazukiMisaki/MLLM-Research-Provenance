# Luna — SI-P3任务隔离与有限预算设计任务

本任务为用户新授权设计，阅读 /home/lizening/research-notes/agent-logs/2026-10-25T084517Z__SOL__si-p3-controlled-experience-design__si3_7d91/COMMON_DESIGN_CONSTRAINTS.md。你的唯一可写目录：/home/lizening/research-notes/agent-logs/2026-10-25T084517Z__LUNA__si-p3-isolation-budget-design__si3_7d91。

只读metadata和既有原件，不打开未使用task正文/结果、不调用任何模型/环境/tokenizer/项目validator。
1. 从已有known-use2612 registry与supported候选metadata独立核对TRAIN1141/seen0/unseen74及family数；检查当前文件存在仅metadata，列出已知隔离风险。不要运行旧脚本或改旧文件。
2. 提议采集/开发/最终评估完全task-disjoint切分。以480/60/600为待审参考，给可审查hash分配规则/家族分配及交叉计数；可产生非执行metadata partition proposal（仅identity/hash/family），不能写科学schedule/gate/argv，不打开task内容。看family容量不足应直接报告，不静默转quota。74unseen不使用，不称heldout；这些是TRAIN task-disjoint评估。
3. 独立计算采集source、一次reset+精确prefix replay、teacher Stage1/2首动作、一次P0 suffix的物理calls/reset/action/output-token最坏上限，logical/physical与共享池采集成本分账。source原continue复用，不增加生成；无额外replay compare模型调用。以N=96及N=480、E=600计算，区分投产软件smoke/dev/训练预算尚未授权且不能藏在总额内。若需input/context/训练GPU硬预算，列出冻结前必须核验的量，不能虚报真实耗时。
4. 设计执行前/中/后证据、fail-closed与停止规则；不赋予执行权。R19旧账5142/7949单列，旧177/342不再重复相加。

交付 TASK_ISOLATION_AND_BUDGET_DESIGN.md、partition_proposal.json（如可行）、budget_design.json、input_bindings.json、原始metadata命令/实际receipts、RECORD.md和FILE_HASHES.sha256。不要新增局部quality mask替代共同池质量。不要INDEX/根inventory/stage/commit/push。预计20–30分钟内返回冻结交付，重大矛盾先反馈。
