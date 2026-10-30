# R19方法稿V2独立验收

**决定：ACCEPT_FOR_MERGE_INTO_WORKING_THESIS_WITH_STATED_LIMITS。** 本结论允许将指定文字并入英文论文工作稿的独立R19探索章节，不是完整可复现包验收、最终学位论文认证或新评估许可。

本次逐段只读审查并重新计算文件SHA-256：

- 路径：`/home/lizening/research-notes/agent-logs/2026-10-30T020500Z__SOL__r19-thesis-methods-v2__8be2/R19_METHODS_RESULTS_DRAFT_EN_V2.md`
- 实测SHA-256：`60a679691403be15c308d68f496b6b1a8c7a628ad37cfe7f9a79e808b942d277`
- 与协调方指定版本一致。

前版`6a2a2229…`的合并前问题已纠正：明确eligible需要exact replay、原prefix剩余预算≥5、第1恢复动作已执行且仍非终止，指出这是intervention开始后的条件化cohort；区分五个K条件与四项预注册contrast；29例写为unsupported/ambiguous coverage-only，而不再等同无分支映射；terminal恢复路径不再描述为继续执行task actor。

39 attempt/36 eligible/183 result-label、11 alias、CONTINUE复用source suffix、各K成功数、2胜2负、逻辑token差异、oracle及两例非新增rescue、7/7有条件诊断、G3及campaign成本边界均与本次直接读取的原始结构/个案字段和既有独立验收一致。没有发现阻止其进入工作稿的新增主张。详细证据、实测hash、源码行号及本次读取范围见同目录`R19_METHODS_INDEPENDENT_REVIEW.md`，SHA-256 `59397a14dc3a6a5997db1ef920ef3b5131280084a7e5b61553894ae9773545d8`。

剩余非阻塞限制应在附录继续补齐：

1. 协议、G3 run/source SHA、G4 analyzer SHA与修订链的可定位来源；G4consumer曾经契约不兼容后修复，不能伪装成从无失败。
2. 入组在延长共同路径前冻结、K不进入生成prompt、共享Stage1/subgoal、相同端点alias及逻辑cost范围（不含干预前source前缀与实验reset/replay）的定义。现稿概括基本准确，附录应足以重建。
3. 若呈现R19区间，另说明97.5% CP component构造及推断假设，不能沿用SI-U1跨primary对比simultaneous95%措辞。四项Holm属于K2..5对K1，不自动扩至CONTINUE及事后oracle。
4. 不把不同source episode/parent等同独立scene；样本包含处理后选择与control富集，原有39-attempt失败记录须保留。
5. 既有数值与历史独立验收支持文稿，本次没有重新计算科学统计、重放环境、验证所有隐藏状态或重新下载远端原件。

本次未更改V1/V2或任何原科学文件；未执行模型、CUDA、环境、analyzer、训练或新评估。
