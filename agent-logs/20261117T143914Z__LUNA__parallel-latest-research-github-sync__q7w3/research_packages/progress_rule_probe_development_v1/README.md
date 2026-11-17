# 进度规则单步探针：开发记录与 CPU 复算

本包记录 16 次虚构题面生成、事前方案及失败边界。**所有输出都因方括号而不符合裸编号格式：有效动作数为 0。** 另附结果已知后对方括号内编号的描述，它不修复正式解析，也不是执行环境或任务成功结果。

- [固定方案](PROTOCOL.md)：四个情境、两种契约与两个子目标，目标和停止规则。
- [结果及成本](RESULTS.md)：正式无效结果、事后字符串观察、资源和适用范围。
- [题面语义审阅](SEMANTIC_REVIEW_V1.md)：V1、V2 的独立意见及 V3 的最后修改。
- [接口边界澄清](INTERFACE_SCOPE.md)：本探针去空白的裸编号规则与冻结 H4、当前两阶段 parser 的差异。
- [脱敏事件](sanitized_events.jsonl)、[正式汇总](results.json)、[事后字符串汇总](bracketed_exploratory.json)：可复核数据；题面均为虚构文本，仍不应把其当作真实任务轨迹。
- `cases.v1.reviewed.json` 和 `cases.v2.reviewed.json` 保留先前版本；`cases.json` 是实际使用的 V3 输入。模型权重、真实设备身份和原始模型缓存均不在此包内。

在工作树根目录运行，无需模型、GPU 或额外 Python 依赖：

```sh
python3 research_packages/progress_rule_probe_development_v1/analyze.py \
  research_packages/progress_rule_probe_development_v1/sanitized_events.jsonl
python3 research_packages/progress_rule_probe_development_v1/analyze_bracketed_exploratory.py
```

复算检查保存记录的关联和算术，不认证权重、物理执行或没有记录的模型输出。有关此前一次独立研究未加载模型即停止的事件，见相邻的 `execution_contract_factorial_dev_v1/RESULTS.md`；本包不是那次方案的补跑。
