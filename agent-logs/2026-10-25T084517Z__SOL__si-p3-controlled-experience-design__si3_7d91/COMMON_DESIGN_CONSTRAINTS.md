# SI-P3 共同边界：受控新经验协议设计（不可执行）

用户新授权设计，覆盖上一轮任务结案；不是新采集/训练/验证/launch授权。以提升冻结SFT-P0 actor独立任务成功率为主线，不再发展adaptive stopping或扩K。历史池B95/C10，严格29/1，作为动机与案例而非新训练/评估池。

研究问题：同一精确actor/teacher、同一个完整新经验池，success-only B_pool与baseline-failure-aware success C是否产生不同的学生成功率；C>A且C>B才支持有限采纳配方主张。C在B内等价于baseline失败筛选，不能包装为独特价值算法。A冻结P0，B/C相同初始化、公共输入、普通成功背景、优化recipe/真实监督曝光。仅第一恢复动作标签，adapter-on suffix只作终局证据。B不能故意排除C。

共同池必须在CONTINUE/恢复结果前一次固定task schedule、每task一个anchor和预算；包括失败、非rescue、无效生成，无正例quota、无采到成功为止、无看结果换anchor/补task。源轨迹只生成一次；原continue若经完整确定性/replay绑定可直接复用，不重复当物理成本；重放/reset/恢复/actor suffix各自真实记账。建议只用K=1（stage1一次+stage2一次），原Qwen3-8B、P0公共H4/有序map/greedy/H50、stage1 40/stage2 16/actor16 token上限不变；不调prompt/decoding/teacher，不把私有诊断/终局结果输入学生。

仅可读取既有科学/provenance代码和元数据。允许自己新目录里的stdlib数学/metadata脚本；禁止模型、环境、tokenizer、训练、policy replay、项目validator/pytest/preflight/G2/G3/G4及创建可执行schedule/gate/launch argv。不要执行旧脚本：其硬编码ROOT曾覆盖旧记录。新脚本以自身目录为OWN并断言当前新任务路径。科学代码/旧证据/旧hash文件均不得修改。

任务隔离按canonical task/trial及同task所有prefix/seed/alias；已登记2612 known-use union全部排除。支持metadata known-use差集TRAIN1141/seen0/unseen74不是从未查看证书；不把74自动当fresh heldout，不开未消耗task正文/结果。评估需独立于采集/开发/旧expert背景。讨论场景重叠风险与可审查边界，不要求证明所有人的完整历史浏览。

协调方供讨论的有限上界方案（尚未冻结）：从1141里预留evaluation600、development60、acquisition480（余1）；采集分96-task feasibility和最多384-task后续，两阶段都不在本轮执行，后续不是自动授权；固定总上限，不能补到rescue quota。若预算/任务空间不可接受，请明确更小feasibility的结论边界或NO_GO，不承诺5pp功效。请挑战此方案，给唯一推荐及充分理由；不要只留下所有关键量UNKNOWN。

两项共同主比较、exact McNemar+Holm(.025/.05)、完整paired W/L/net/gross harm、边际Newcombe10 CI、观测净增益至少5pp及观测gross harm≤5%作为既有价值标准。单训练seed不支持跨seed；样本量/完整验收功效不能由R19 oracle估计。数据充分阈值是资源决策guard，不能宣称存在普遍最低N定理。

仅写自己新目录，保留原始log/实际subprocess receipt、输入/输出SHA和RECORD.md，最终返回冻结交付清单。不要写INDEX/根inventory/其他agent目录，不stage/commit/push。Coordinator统一独立审查和发布。R19累计5142/7949保持，本轮新增科学计数全部0。
