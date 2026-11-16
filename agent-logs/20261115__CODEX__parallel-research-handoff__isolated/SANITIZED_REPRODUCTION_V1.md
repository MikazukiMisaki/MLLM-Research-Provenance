# 合成题面：脱敏日志的 CPU 复算

在本目录运行 `python3 scripts/recompute_sanitized_handoff_v1.py`。只依赖 Python 3 标准库，无需模型或环境；结果打印为 JSON。保存在 `evidence/sanitized_synthetic_logs/recomputed_handoff_v1.json` 的结果是一次运行的输出。

输入是四份白名单导出的虚构题面日志：`second-object-visible-acquisition-v1.jsonl`（基线生成）、`incorrect-subgoal-handoff-v1.jsonl`、`incorrect-diagnosis-handoff-v1.jsonl`、`diagnosis-subgoal-candidate-scores-v1.jsonl`。程序核对这四份脱敏文件的固定 SHA-256，并按情境编号关联：原诊断／原子目标对应基线 `NN-generated`，原诊断／错误子目标对应错误子目标日志的 `NN`，注入诊断下两种子目标分别对应诊断日志 `NN-original_goal` 和 `NN-injected_goal`。评分日志使用 `NN-old_correct`、`NN-old_wrong`、`NN-false_correct`、`NN-false_wrong`。

入口重建四条件动作表，检查四个生成提示除指定诊断与子目标外一致、编号映射和提示 token 数一致、生成 token 与保存的原始输出后缀及规范候选后缀一致，并比较每个得分最高编号与保存的贪心编号。它重算四候选权重、两候选差、条件配对和交互，逐项比较本快照中的两份既有汇总。32 条提示和 128 条评分来自同一组八个人工情境，不是 32 或 128 个独立情境。该版本使用输入中已保存的浮点数和 Python 浮点运算，差异极小时不能推断不同计算精度下方向稳定。

程序还重计三批生成的已记载 token 数和评分输入 token 数。四候选权重只是指定序列的条件归一化，不是完整动作概率或任务成功概率。

**绑定边界：**评分导出的 prepared 行没有完整提示、提示 token IDs 或逐提示摘要，因此上述检查不能证明每组分数确由相应完整提示计算，只验证情境键、编号映射、长度、保存的生成记录和分数之间的一致性。关联原始输入仍依赖未上传的执行记录及代码；SHA 只是固定导出文件，不认证设备、模型权重、来源身份或实际执行。没有重跑模型或环境；三个生成批次分开执行，不能据此估计真实任务错误频率或后续成功率。
