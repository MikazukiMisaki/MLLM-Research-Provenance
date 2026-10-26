# Astra：三份 SI-P3 v2 文档的独立静态复审

**DOCUMENT_REVISION_REQUIRED；核心设计逻辑可继续审议；COLLECTION_NO_GO_NOW / NOT_ADOPTED / NOT_IMPLEMENTED / NOT_EXECUTED。**

仅审查指定的协议草稿、静态方法/事件差距分析、预算与归因文档。没有重新计数旧source，没有读取新任务、源码或其他科学数据，没有运行项目模块、模型、CUDA、tokenizer、环境、SSH、测试或preflight。文档中的源码位置、历史运行数值和历史测试结果在本次只作为其引用的既有证据，没有重新核验。两名内部子审阅者也限制为这三份文档的只读复核。

## 唯一需要修正的问题

### [P2] 将 teacher 合法诊断输入与学生特征泄漏混为一个拒绝条件

位置：`STATIC_METHOD_EVENT_GAP_REVIEW.md:60`（Future负向验收矩阵第14项）。该项把“诊断”进入“学生/teacher因果公共输入”统一列为拒绝，并限定“只允许S5冻结P0 view与合法ID+EOS”。

这与协议草稿第22行保留冻结 `two_stage_v2`、第82行只禁止teacher诊断/subgoal传给学生的规定冲突。冻结teacher的Stage2需要同一S5上Stage1产生的diagnosis/subgoal；该内部计算不是未来结局或隐藏状态泄漏。若按第60行的字面范围编写负向验收，会拒绝合法Stage2请求，或促使实现删除诊断而改变干预方法。本次发现的是**文档合同冲突**，不是已发生的运行故障。

最小修正：将学生和teacher边界拆开，明确以下三点；不改原teacher或其他设计：

1. 学生输入仅为S5冻结普通P0公共投影，监督目标仅为首动作ID+EOS。禁止Stage1诊断/subgoal、未来source/branch终局、完整未来suffix及隐藏状态进入学生特征。
2. teacher Stage1使用S5的因果公共请求；Stage2还允许按冻结协议使用同一S5产生的Stage1诊断/子目标及既有有效性参数。禁止未来结局、完整未来source suffix和隐藏状态进入teacher输入。
3. 保留原Stage1无效时仍做一次Stage2诊断性生成、但不执行teacher动作且YT=NA的既有路径；不能将“只允许合法Stage1输出”另增为取消该固定调用的条件。

请通过新修订或补充说明修正封存文档，不覆盖已封存原字节。这项修正是文档作为实施验收依据前的必要步骤；它不解除既有执行能力、实现和投入阻塞。

## 未发现其他实质性逻辑或数字不一致

- **E/F/S上界与完整性。** 协议第37–64行以运行时S5状态、terminal/truncated、完整map及正常source闭合定义E；unknown先STOP，不按零计数。第6次解析失败但已有有效S5仍纳入E，避免移植旧L>d计数器造成false NO_GO。Q⊆E、C⊆F、neutral⊆S，因此总量和家族必要条件不足时可确定配方不成立；通过不能证明Q/C或投资通过。
- **source-first边界。** 全部96 source封存和必要数量审核先于任何branch reset/replay/teacher；随后对全部预定E尝试一次，包含Y0=1对照。仅source授权不能自动进入branch。独立source seal、真实物理时间序与slot依赖、task-local seed/pool/counter绑定均被列为未来须实现/审核，未冒充现成能力。
- **停止类型。** source-only结构性NO_GO、正常不可达/invalid、技术或预算INCOMPLETE、完整性STOP及完整配方NO_GO被区分；未调用teacher保留YT=NA，不能作为teacher失败。禁止补样、重抽、改变位置或追加384。
- **预算。** 完整v2上界为9,216 generations、9,792含reset环境操作、149,760输出token；source-only为4,800 / 4,896 / 76,800；完整source后的后续上界为4,416 / 4,896 / 72,960。相对v1多720次suffix推理和11,520输出token的说明正确。16M输入和4 device-hours为独立累计硬帽，不保证完成；训练、工程与600×3评价不在采集预算内。评价上界90,000 / 91,800正确。
- **归因。** C−A归于整个追加训练包；C−B只归于共同S与剂量、C分布匹配成功对照下的失败筛选配方差异。B_pool包含C_pool，实际抽取B24不必包含全部C24。24新例和最多136/144共享例的限制被保留；固定d5不被误称错误触发恢复、自适应停止或学习收益。
- **投入。** 新96至少需要24个可达source失败及家族配额只是代数必要条件。旧6/120、旧d5可达率均未被当作新96预测。source-only并非免费预检；文档明确没有新的充分投入理由，不能据工程PASS自动采集。

以上仅表明文档所陈述的逻辑和算术相互一致。尤其不独立认证其引用源码位置、seed/reset真实行为、旧原件数值、GPU身份或未来资源完成性。

## 处置与边界

建议协调方要求上述单处文档修订，然后继续独立审议该候选；无需为解决此文档冲突启动任何科学运行。没有发现其他应阻止候选继续讨论的实质问题。

**对“现在能否做下一轮实验”的回答仍是否。** 真实可信宿主/PID映射、source-first live driver/独立auditor、真实8B与资源证据、以及支付source96本身成本的投入理由都没有由这三份文档证明。本文既不采纳v2，也不授权实施、探针、采集、训练或评价。

本轮报告交Sol Designer统一整合；不修改共享INDEX/根清单，不独立commit/push，不更改上一轮封存文件。

## 审查输入

共同目录：`/home/lizening/research-notes/agent-logs/2026-10-26T091852Z__CODEX__si-p3-v2-source-first-design__cec2ce5a/`

| 文件 | SHA256 |
|---|---|
| SI_P3_V2_PROTOCOL_DRAFT_NOT_EXECUTABLE.md |39abd66958553722d63e70c20b40e342a1c5329fd20995163b41b8d2298fe3a8|
| STATIC_METHOD_EVENT_GAP_REVIEW.md |4394443e5a2187ff9a932b671418f104486a6d3474828c89fb38683c74c27003|
| BUDGET_STOP_AND_ATTRIBUTION.md |ec98ed09acbc085bb0a5f20685fc81dce8251df48ecb0e13b215fa22530d5a8f|

文档行号由本轮带行号读取所得；输入SHA与请求给出的三个前缀一致。
