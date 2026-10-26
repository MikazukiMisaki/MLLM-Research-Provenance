# SI-S01 已采纳设计与最小实现任务：独立静态复审

**STATIC_SCOPE_REVIEW_ACCEPTED / NO_BLOCKING_DOCUMENT_DEFECT_FOUND / ACTUAL_LAUNCH_NOT_CLEARED。** 本复审追加于同一尚未最终交接的投资评审任务。协调方已另立source-only设计采纳与条件投入决定；该状态不追溯修改原v1/v2或前几轮NO_GO原件。

仅阅读以下两份新文件并核对SHA，没有读新任务、源码、设备、SSH配置或运行任何测试/模型/环境：

| 文件 | SHA256 |
|---|---|
| ADOPTED_SOURCE_ONLY_PROTOCOL.md |daa1d787f9ef13f5927dcf696a2be4c6328dc159b3eb39b5f0f5f520582ebb72|
| SOURCE_ONLY_IMPLEMENTATION_TASK.md |5fd913a8d980f8e3eba551e3d377221c691033c090bb5a3a9af3b3ce7845263c|

目录：`/home/lizening/research-notes/agent-logs/2026-10-26T100859Z__SOL__si-p3-persistent-launch-coordination__f1a52e8c/`。

## 复审结论

1. **seed、顺序与counter边界明确。** 协议第16行在新结果前固定每task nominal/reset seed42、fresh单game pool seed42及一次reset；按既定五家族顺序，再用冻结rank域及canonical task ID排序，平局由task ID打破。这是前瞻的单seed设计选择，不依结果改seed。实际manifest在副作用前封存，并要求独立复算。receipt-local index不能冒充内部counter；本阶段只要求source初始化可认证，未来replay等价另证，未把同一个数字seed当成已有replay证明。
2. **零teacher范围是实现要求。** 协议第14–17行、实现任务第13–18及24行明确禁止Stage1/Stage2、adapter-off、branch reset/replay、独立suffix、训练与评价。source在d5后的正常P0延续仍属于原source，并未被误禁。需要在真实外部边界前拒绝这些阶段，不能仅依靠CLI约定；文档已经提出这项验收要求。
3. **source-only报告没有越界。** 协议第21–25行要求全部96正常source及S5去向可认证后才计算E/F/S；有效S5后的第6次parser fail-closed仍可E内。unknown不能当0；所有YT=NA。必要数量失败只否决固定配方，足够仅NOT_FUTILE，不报告恢复率或学习提升。后续Q/token/teacher去重尚未观测，E仍是其保守上界，不能实现为猜测完整Q后任意剔除task。
4. **原件与独立核算要求充分且仍待实现。** 实现任务第15–17、22–26行覆盖及时S5、已认证Y0不丢、source seal、跨run/身份/动作映射与物理调用绑定、failed/open保留、独立auditor逐原始receipt重构及真实production路径fixture。它没有允许collector汇总或report为自己背书，也没有把软件fixture称为真实运行。
5. **预算与阶段隔离保持一致。** 协议第29–31行为4800/4896/76800/16M/8192/4device-hours，真实source初始化和GPU占用计入；新工程调用另定有限范围，不借source额度。只一次科学启动、输出不得存在、无自动重试。实现任务本身只允许代码和软件测试，不允许真实模型、tokenizer、CUDA、ALFWorld、SSH或生产preflight。
6. **可以据此推进实现，但不能据此宣布启动。** 旧synthetic gate、Caps/MAXIMA、R19/G4及所有旧原件保持严格；隔离worktree、exact基线和科学commit不得含机器路径的边界明确。最小source-only生产链必须真正接好再独立审核，不能拿旧4调用diagnostic替代。未来可信身份、真实P0资源、零science副作用的生产预检和单次launch具体绑定仍需实际证据。

未发现需在代码开发前阻断的精确合同缺陷，无需再为source-only增加teacher/training/full-paired实现任务。种子和顺序的文档明确不等于真实TextWorld行为已验证；以上是静态合同接受，所有相应测试和live条件仍为NOT_VERIFIED。

本复审与同目录 `INVESTMENT_AND_ADDENDUM_REVIEW.md` 一起支持协调方继续推进到真实启动条件闭合，不要求事前知道C24。当前没有发出任何运行许可，没有修改共享INDEX或旧封存文件。
