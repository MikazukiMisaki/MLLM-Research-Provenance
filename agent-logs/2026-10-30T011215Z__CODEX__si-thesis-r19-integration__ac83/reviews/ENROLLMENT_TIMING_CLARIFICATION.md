# R19入组冻结时序限定

V2 exact SHA `60a679691403be15c308d68f496b6b1a8c7a628ad37cfe7f9a79e808b942d277` 没有写出与证据相反的时序，因此仍可并入工作稿；这不改变 `R19_V2_ACCEPTANCE.md` 的用途。为完整表达方法，定稿前应明确入组在共同恢复路径延长和替代suffix结局评估之前冻结，避免“事后按K2–K5结局选36例”的误读。

建议放在primary eligibility定义之后：

> Enrollment was frozen after these initial recovery attempts and before the common recovery paths were extended or their alternative SFT suffixes were evaluated.

证据：冻结G3代码 `2da980f631badc25086d12db60d128ff507d3ae6:src/recovery/r19_duration.py` L1423–1429发出enrollment_frozen；其后函数 `execute_frozen_r19_enrollment` L1440起、L1465–1491扩展path，L1504调用suffix评估。原始ledger event sequence9698、event ID `f14635272a407ddf96a0a83e172d3a033ad5ecfb45a7a1941aa41b744f5fd9f4` 记录39 attempts、eligible分层6/15/15和 `additional_stage_two_generations_before_freeze=0`。原始ledger SHA `05e1d443ff304eaa25d08b92a4e19d204a6c93a4f46bbe50aefef3271f211762` 已在本次审阅实测。

关键边界：freeze发生在Stage1及初次恢复动作的纳排之后，不能写成“before any intervention or outcome observation”。source轨迹结果用于分层，初始intervention成败用于eligibility；这些处理后条件化限制仍存在。正确的冻结时序排除了以更长K分支的后续结果选样这一流程，不消除初始eligibility选择本身。

本说明依据已只读核验材料，不新增运行或更改原件。
