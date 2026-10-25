# SI-P2 事前审计规则：同池质量、去重及可分性

用户2026-10-25明确要求继续同池成功对照核验，仍只审计既有证据，不启动新实验。科学85cbb923/执行G3 2da980f、累计5142 generations/7949含reset操作不变。P1正式决定与原件保持，P1数据NOT_READY不是新任务的阻止指令。

唯一parent范围：本目录PARENT_COHORT_MANIFEST.json，SHA256 a3e2548e89280d150cbe83cceca632f9f91275ede0a4a9d89133e53691826078，171行（R4 24/R10_OSR48/R16_OSR60/R19_K1 39）。manifest只含预存身份和locator，不含新outcome偏好。不可扩K2–5、PAR/cards、新source或suffix训练目标。

## 共同质量Q_hist（主审计口径）

对所有171行同一套规则，先审计后按成功筛选：原文件/行hash及task/prefix身份；完整动作前source public-prefix、goal/current observation/H4/有序完整action map；固定P0公共文本对原actor存储prompt的静态核对；非终局动作前时点与50−d；已有exact replay及可支持的公共state/map/history一致性；原Stage1合法、第一Stage2完整未截断、bare ID/selected/map/实际执行command与transition绑定；原CONTINUE和恢复完整分支label能够按原冻结success/stop契约追溯。无效动作/截断/未执行不得修复后纳入。

成功标签按历史冻结done&&reward>0及原stop语义核对；缺导出的won单列RAW_WON_NOT_RECORDED，不是新G3错误或目标非法。失败可由原horizon/invalid fail-closed等已记录停止支持，不要求失败也必须done=true。若缺少足够原件则HOLD，不猜测；不能以结果是否救回来定义质量。

历史weights/tokenizer版本PARTIAL不是机械FAIL；保留为历史跨策略蒸馏候选，不能伪装同一当前actor。另做预先声明的Q_pin敏感性：Q_hist且历史weights/tokenizer+loaded adapter角色都有原receipt精确绑定；按同样流程单列，不据计数挑更好口径。不得把当前cache身份反填旧历史。

学生输入仅公共动作前字段；不导入subgoal/card/facts/expert_plan、终局/未来动作/当前source动作输出及后验结果。只审计第一adapter-off恢复目标；adapter-on suffix只用于原分支证据，不作训练目标。无完整训练prompt或JSONL导出，不加载tokenizer，不把推理tokens当训练tokens。

## 固定去重顺序（事前锁定，不换规则挽救rescue）

1. 全171 parent逐行保留disposition；Q_hist共同质量过滤。
2. 对有明确shared generation-event ID/physical alias证据的重复只计一次；没有事件ID的legacy标physical reuse NOT_PROVEN，不能从语义相同推断同一物理调用。证明相同物理重复时，保留下述anchor key最小者。
3. 全池跨阶段canonical task/trial每task一个anchor，在质量合格候选上取最小anchor key，**在CONTINUE/recovery成功采纳之前**。其他prefix不再补选。key为SHA256 UTF8字节：
   `SI-P2-anchor-v1\\n{canonical_task}\\n{stage}\\n{prefix_id}\\n`
   精确定义：SHA256(("SI-P2-anchor-v1" + chr(10) + canonical_task + chr(10) + stage + chr(10) + prefix_id + chr(10)).encode("utf-8"))。实际编码使用换行字符，不是字面反斜线+n；stage仅R4/R10_OSR/R16_OSR/R19_K1。按十六进制hash升序；极罕见tie按case_id字典序。key不使用success/label/family/target ID或完整row digest；历史prefixID是opaque locator。已有历史结果并非人类盲法，但不得按观察结果重选hash/seed/anchor。
4. anchor间若exact公共projection+目标命令重复，保留同key最小者，其他slot不回填；所有相关task仍登记为已用。公共projection采用P1规范：ASCII JSON ensure_ascii=True/sort_keys=True/separators comma-colon，字段goal、observation、recent_action_result_transitions(list of action/resulting_observation)、ordered_action_map(list of ID-command pairs)。exact同输入不同目标只报告歧义，不自动判错或改目标；为保证有利结果而额外排除须停报。
5. 最后 B_pool={合格anchor且recover=1}；C={合格anchor且recover=1且CONTINUE=0}。C应为B子集；报告B\\C的neutral-success，而不是只用原11 positive池。所有171仍有去向。Q_pin按其更严格共同过滤后，独立应用同一固定dedup/anchor流程；只是预设敏感性元数据，不是第二次科学实验，也不替换主口径。

至少报告RAW、Q_hist后、physical dedup后、task anchor后、exact input-target dedup后各阶段的rows/unique tasks、B/C/neutral/harm/failure数及家族/历史来源覆盖；列原11 positive逐项去向。B!=C仅是集合可分，不代表等token/等来源训练对比已经成立。逐来源是否有B\\C、C是否只剩少数task/家族、最大共同训练去重容量、背景S/实际tokens/重复预算未定均需披露。

## 权限与封存

只能纯stdlib读既有原件、静态源码/Git对象；只写自己新任务目录。禁止模型/ALFWorld/tokenizer/训练、policy replay、任何G2/G3/G4/preflight、项目analyzer/validator/pytest、新schedule/gate/argv、科学代码/测试/旧raw/旧provenance修改。**不得执行旧脚本的硬编码ROOT**；复制既有审计逻辑仅在新脚本明确绑定OWN=__file__.parent并验证输出目录后可运行。无commit/push/sharedINDEX/rootinventory写入，无额外agent/互发任务消息。协调方统一发布。

先完成一轮有界核验，最多60分钟，45分钟时尚未完成先给进度/缺项；未知原件就HOLD，不为凑positive无限扩查。每个真实失败receipt保留；最终给RECORD、commands、实际subprocess returncodes、输入前后SHA、机器表和自己的hash清单。训练资格/独立review PASS/新执行许可不在开发或执行线程权限内。完成冻结后仅通知本线程，协调方poll；不要另行触发协调方线程消息。
