# SI-P1 Luna 独立复核反馈：只新增V2更正
本条仍属用户已授权的任务隔离/预算补齐，不是新实验。不得写P0任何文件，不运行P0脚本，不改你已冻结P1文件/FILE_HASHES；只在你P1目录新增V2/addendum与独立清单/真实receipts。

1. 已确认P0两tracked文件被改写，另新增两JSON。我已将其全部原字节保存到 /home/lizening/research-notes/agent-logs/2026-10-25T065200Z__SOL__si-p1-protocol-review__caae4c/P0_SCOPE_INCIDENT_SNAPSHOT/，详见同目录P0_SCOPE_INCIDENT_AND_RESTORATION.json，并将两tracked文件恢复到已发布5774774原字节，将两新JSON从旧目录移入快照保留。科学raw未动。不要自己再次回滚/运行旧脚本/改共享INDEX；后续只读已恢复原件或引用快照，说明旧脚本内置ROOT导致越界。你P1 V1原收据/报告保留，input若绑定变动后的P0字节须引用对应快照，不能假装未变化。

2. 原“缺少full source file hash”不成立。P0 Sol experience_inventory.json.input_bindings有每个源path的sha256_before/after（不是sha256字段）。独立核验 /home/lizening/research-notes/agent-logs/2026-10-25T065200Z__SOL__si-p1-protocol-review__caae4c/independent_source_hash_and_identity_join.json 逐个实际全文件hash+原行hash核对全通过。R4/R10/R16/R17/R18C1/C2/R19的351条prefix-to-task原件映射均闭合，固定11全部有full-source SHA。请用该metadata结果/原P0字段修正V2，不能再将部分manifest字段缺失扩大为这些已声明cohort映射缺失。未登记全历史查看仍NOT_PROVEN，保留该准确限制。

3. budget_evidence的SFT_gpu_time_seconds=27406.3错标：training_result.json字段为wall_time_seconds=27406.28269892931，不能当GPU device-seconds。原input_tokens_seen=23860000只按原metric名报告；若要称padded需单独明确旧Trainer计数语义证据，否则UNKNOWN语义，不把completion-targettokens混进去。2354optimizer steps保留，R19实际5142/7949保持。V1文字“exact-dedup前127”应明确为去重后127、去重前148/移除21；不更动旧文，新增更正。

4. 未来本最小协议evaluation仅A/B_pool/C学生，无controller/probe/replay，故在我冻结此限定后Cextra=Rextra=0、生成≤150E、环境≤153E。额外操作若将来要加须独立预算，不默许未知extra空间。现在不选E、不执行。

请只产出有界 CORRECTED_ISOLATION_AND_BUDGET_V2.md、corrected_isolation_budget_v2.json（修正源hash/351映射、11case、known-use差集及预算字段），V2命令/真实receipt与单独hash清单；旧P1内容不覆盖。可读取原已发布P0 metadata、独立join结果和你自有已冻结证据，不扩新outcome、不调用模型/环境/训练/项目程序。若某named映射来源不符请精确反例，不靠“metadata missing”泛称。返回更正的path/SHA后冻结，不继续扩查。