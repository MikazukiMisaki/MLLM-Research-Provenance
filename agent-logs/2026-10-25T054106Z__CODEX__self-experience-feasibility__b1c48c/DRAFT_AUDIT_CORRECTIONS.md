# SI-P0 草稿审计修正记录

这仅说明本任务纯stdlib草稿脚本的字段适配，不是科学代码bug或原证据变更。

1. 首次event schema probe查找event_type/type，原R19实际键为kind；因此schema_probe阶段的事件类别null计数没有科学含义，正确类别在r19_event_kind_probe.json及inventory_audit_final.log。
2. inventory_audit_first.log最初从payload外层找generation，因真实结构为payload.evidence.generation，把prompt/raw的存在性误记0。inventory_audit_nested_evidence和后续修正已读取真实嵌套层。
3. 后续草稿已看到actor action_map，但恢复Stage2原件使用evidence.id_to_command/action_id/command，因此先前4754的map计数仅含actor。最终按各自真实schema重数为4926/4926 action generations正确绑定，另39 Stage1不属于动作目标。
4. 两个推测的小写R18文件名检索返回工具exit=2（不存在）；随后以rg --files定位真实大写报告并成功读取。不是数据缺失、原件修复或跳过验证。

所有草稿日志保留，不覆写。experience_inventory.json最终版本与inventory_audit_final.receipt.json、inventory_summary_final.log为引用依据。未运行项目analyzer/validators/pytest，未补任何科学生成/环境调用。
