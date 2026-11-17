# 执行契约开发方案：启动失败证据包

本包保存一项未成功启动的虚构题面方案：进程在导入模型依赖前停止，**0 次模型生成、0 次环境执行**。失败记录没有被重跑或改判；后来另行设计的进度规则研究使用不同题面和契约，也未补出本批结果。

- [启动失败结果](RESULTS.md)：终止事件、后续环境检查和缺失分母。
- [运行前固定记录](PRE_RUN_FREEZE.md)：材料与代码的原始摘要及一次性停止约定。
- [运行前协议快照](PRE_RUN_PROTOCOL_SNAPSHOT.md)：原冻结协议的字节相同副本，其 SHA-256 与固定记录一致；复制该文件仅为了使审阅包自包含，不改变原方案。
- [脱敏事件](sanitized_events.jsonl)、[部分汇总](partial_results.json)、`cases.json`、`analyze.py`：均为虚构输入或停止事件；原始设备标识不在本包。

在工作树或快照根目录从脱敏事件复算，不需要模型、GPU 或额外 Python 依赖：

```sh
python3 research_packages/execution_contract_factorial_dev_v1/analyze.py \
  research_packages/execution_contract_factorial_dev_v1/sanitized_events.jsonl
```

汇总中的 32 次均标为未运行；不能从这些材料得到任何动作、进度规则或成功率结论。`run.py` 是历史运行代码，不是重试命令，方案保留一次性停止规则。
