# 动作编号呈现及输出格式：开发研究包

本包保存 8 个虚构状态 × 4 个条件的 32 次单步生成。固定裸编号输出要求时，裸候选行 8/8、方括号候选行 6/8 符合条件格式；后者的两例无效是同一结构的词汇变体。要求方括号时两类候选行各 8/8 符合其各自的要求，但这些输出不符合统一裸编号参考。该实验没有执行环境，不代表项目生产 parser 或真实任务成功率。

- [方案](PROTOCOL.md)：预先固定的条件、解析规则、分母、资源和停止条件。
- [结果](RESULTS.md)：各条件、配对、成本、可复算范围和结论限制。
- [设计审阅](DESIGN_REVIEW.md)：Astra 对 V1 的只读审核及作者对 V2 的修改。
- [独立记录复算](independent_recompute/REVIEW.md)：从固定题面和保存的解码字符串独立重算计数与配对，不是独立 token 解码或模型复现。
- [接口边界澄清](INTERFACE_SCOPE.md)：本研究去空白的裸编号参考与冻结 H4、当前两阶段 parser 的差异。
- [脱敏事件](sanitized_events.jsonl)及[汇总](results.json)：不包含设备身份；人工题面、模型输入 token、输出和映射均保留。
- `cases.v1.reviewed.json` 和 `build_cases.v1.reviewed.py` 是审阅过的旧题面版本，`cases.json` 是实际运行的 V2。

在工作树根目录使用标准库复算，无需模型或 GPU：

```sh
python3 research_packages/action_id_format_factorial_dev_v1/analyze.py \
  research_packages/action_id_format_factorial_dev_v1/sanitized_events.jsonl
```

复算核对保存记录的关联和计算，不证明模型权重、物理执行或从未记录的输出。先前 16 个进度规则题面的格式失败保持原判，本研究不补出其有效动作或证明其失败原因。
