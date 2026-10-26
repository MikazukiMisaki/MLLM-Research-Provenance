# SI-P3 v2 C01/C02最小文档澄清附录（作者待审）

**AUTHOR_CLARIFICATION_ONLY / CHANGES_REQUIRED_BEFORE_ADOPTION / COLLECTION_NO_GO_NOW。** 本附录仅限定原三文的两处歧义并纠正当前任务hash的叙述引用；不覆盖任何已封存字节，不改变其他协议条件，不采纳v2，不授权实现或运行。Astra静态审查SHA为 `2e91dd8e348562821e5d94e0ade33d5306a7ee862480cb93d142ca15e6eaaafe`。root的READINESS_DECISION仍是协调中的文件，本附录不冒称其最终封存或附录已通过独立审查。

## 原件与任务字节绑定

原包：`/home/lizening/research-notes/agent-logs/2026-10-26T091852Z__CODEX__si-p3-v2-source-first-design__cec2ce5a/`。

| 原文（保持原字节） | SHA256 |
|---|---|
| SI_P3_V2_PROTOCOL_DRAFT_NOT_EXECUTABLE.md |39abd66958553722d63e70c20b40e342a1c5329fd20995163b41b8d2298fe3a8|
| STATIC_METHOD_EVENT_GAP_REVIEW.md |4394443e5a2187ff9a932b671418f104486a6d3474828c89fb38683c74c27003|
| BUDGET_STOP_AND_ATTRIBUTION.md |ec98ed09acbc085bb0a5f20685fc81dce8251df48ecb0e13b215fa22530d5a8f|

当前NEXT_STAGE_DESIGN_TASKS.md真实字节SHA256为 **`12e312be741343e9998f331bad5a9a3b5ddb09df4444a0e47fd0cf869214fdd5`**。原主文/RECORD等叙述中的旧值 `51143107131e15b1771882461bd77200de14c726819a909de701b9f19fe3b188` 不认证当前字节，应与当前版本分开。原INPUT_BINDINGS_BEFORE.json和INPUT_BINDINGS_AFTER_AND_SOURCE_STATES.json实际已经正确保存同一当前12e312…，本次已核对；没有改写这些JSON或原文。证据条目及原包整套hash未变记录见EVIDENCE_BINDINGS.json。

## C01：替代原静态差距文档负向验收第14项的歧义解释

* **学生边界：** 输入仅S5冻结的普通P0公共投影；监督目标仅合法首动作ID+EOS。Stage1 diagnosis/subgoal、未来source或branch终局、完整未来suffix及隐藏状态均不得进入学生特征。
* **teacher边界：** Stage1使用S5因果公共请求；Stage2保留同一S5请求，并按冻结two_stage_v2接收该S5上Stage1产生的 `diagnosis`、`subgoal` 及既有 `stage_one_valid` 参数。这一合法Stage1→Stage2内部传递不属于泄漏，不能删掉或误列为拒绝条件。teacher同样不得获得未来source/branch终局、完整未来suffix或隐藏状态。
* **无效路径不变：** Stage1 invalid仍固定做一次Stage2诊断性生成，保留既有validity语义；不因此取消该调用或增加重试。Stage1无效时不执行teacher动作，YT=NA；不能用Stage2恰有合法ID来绕开该条件。

因此，学生的“仅公共P0投影+动作目标”不能套成teacher Stage2也禁止合法诊断/子目标。这里只澄清负向验收文字，未修改prompt/parser/teacher方法或运行结果。

## C02：配额表的C臂与B臂含义

原配额表“C最低/各臂选中C数”的歧义，限定义为：C臂选中C的配额；B臂匹配的同family新例**总数**，不表示B臂每个例子都来自C。

| 家族 | C臂选中C配额 | B臂匹配family新例总量 |
|---|---:|---:|
| pick-place |9|9|
| clean |6|6|
| cool |4|4|
| heat |2|2|
| pick-two |3|3|
| 合计 |24|24|

B_pool包含C_pool是**候选池**关系；B24从整个B_pool按原family×实际监督长度一次匹配抽样，允许选C候选但不要求包含全部选中C24。B24必须至少8neutral，所以其中C类最多16，且与选中C24的交集最多16，不可能包含全部C24。应如实报告实际B∩C，不重抽以改变交集。

原C/neutral候选池总量及家族最低、Q、一次hash抽样、长度/token/曝光、S120及禁止top-up等条件均不变；不新增B每family必须含多少neutral的条件，也不改B为neutral-only。

## 仍未解除的阻塞

附录交付或通过文档审查均不采纳v2。C24供给、source96本身投入理由、source-first真实驱动/审计、host/local PID映射与真实资源证据仍未闭合。工程844/科学85/已执行2da及旧证据保持不变；当前没有实现、测试、探针、采集、训练、评价或其他runtime/science许可。
