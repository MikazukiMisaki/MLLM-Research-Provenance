# SI-U1修订方法稿：exact-byte合并审阅

**决定：ACCEPT_FOR_MERGE_INTO_WORKING_THESIS_WITH_STATED_LIMITS。** 接受下列确切版本并入论文工作稿；不是最终论文/完整可复现包验收，不是新实验、预检或评估设计许可。

受审文件：`/home/lizening/research-notes/agent-logs/2026-10-30T034000Z__CODEX__si-methods-amendment__e170/METHODS_REVISED.md`。

本次独立读取并实测SHA-256：`aad007a30db6ea17dcd1298af37f2a8f9fd83ecadd73a04abec9b0ea75b706a3`，与协调方指定值一致。此结论只绑定该版本。

## 纠错复核

此前 `SOL_METHODS_CLAIM_REVIEW.md` 要求的关键修改均已落实：

- P0专家来源区分文件身份核验与同期报告对expert流程的归类；历史base/tokenizer/launch未知保留，没有恢复已撤回的canonical hash冲突。
- 全候选ranking/eligible/conflicting-target机制写成specified规则，保留selected-row审计没有全量重排的限制。
- LoRA rank/alpha/dropout字段与实际B/C保存配置一致，未把alpha64误写成实测scaler64。
- optimizer配置使用“specified”，实际microbatch、updates、order、LR与token计数单独以日志验收支撑。
- success具体写为done=true且positive reward；selection failure是协议处理规则，本次实际为零，未混入P0旧评估的失败案例。
- 5pp科学兴趣、10pp观测signal、warning优先边界、inconclusive与一次训练seed的解释区分清楚。
- extractor修订只宣称通过冻结symlink检查所指bytes，没有宣称约束了目标位置；结果可见性只限已检查调用，不宣称全历史盲态。
- 新增5001条decoder metadata明确是记录检查，并保留未重现模型执行与未记录调用的边界。

## 与853冻结源码的独立静态对照

本次直接读取本地Git对象 `8532275932dabddc498c23a2b6d9a045647542f0` 下述路径，未导入、运行或修改源码。以下行号对应该Git对象，而非默认工作树。

1. `src/self_improvement/si_transfer_eval/evaluator.py`：实测SHA-256 `d399ffa95c109b5b83195d3639f24261b7a63a62c1b3fe7c18d59ae695ae037a`，与decoder审计报告一致。L21–22固定HORIZON=50、OUTPUT_CAP=16；L78–90校验raw输出schema、token计数、adapter身份及 `do_sample is False / thinking is False`。L214–225调用public projection及当前valid_actions解析，选中ID须与action-map吻合。L232–240区分terminal、truncated、horizon与selection_failure，truncated中止比较，done且reward>0才是成功。
2. `src/self_improvement/si_transfer_eval/live_runtime.py`：实测SHA-256 `c247df8e1ac8985dc569b67c4ab3f3e2efceef1b837973e861a085a95fd3b2bc`，与decoder报告一致。L96配置thinking=false及do_sample=false；L118模板render禁用thinking；L140实际generate参数为max_new_tokens=OUTPUT_CAP及do_sample=False；L149–150从返回序列形成计数并记录同样的metadata。这支持设置与记录字段的实现对应，不是GPU计算重新验真。
3. `src/self_improvement/si_p3/contract.py`：实测SHA-256 `2d7b05d5c230cb45c2ad90c7507c11a5c76ce52f7335548c46a48d78e8842239`，与decoder报告一致。L163–173的projection使用 `sft_p0_prompt`、当前action map与history[-4:]。
4. `src/sft/protocol.py`：实测SHA-256 `cb9a8ee23d1208064348810ef3580773ba14403bfaac6a4e7f4a43c5540178a8`。L21设history window=4；L56–87的renderer提供goal、当前observation、至多4条action/result transitions和indexed admissible actions，并要求bare action ID。`src/models/action_parser.py` L89–93保留环境动作列表顺序，enumerate为A000…，没有另行语义排序。

因此修订稿关于四条history、indexed map、ID解析、H50、解码设置及terminal success的表述，与固定853实现和新增记录聚合桥一致。该静态对照补充了前一份报告末段“未逐函数核查”的状态；不能据此升级为完整代码审计或runtime再执行。

## 新metadata审计实现的边界

已在前一报告记录：对新增脚本、JSON、RECORD三文件的hash检查均通过；脚本按completed generation事件筛选，类型和值同时核查decoder字段，并对整个ledger bytes求hash。保存的总数/分臂数/5-token范围与既有独立验收一致，输入ledger SHA直接匹配已接受分析。

本次没有重跑该metadata脚本或原ledger。它不独立检查整条事件链、start/completion配对、模型实际身份、依赖闭包或已删除/未保存调用；修订稿没有提出这些超范围主张，因此可合并。

## 可复现性清单的新证据与剩余问题

另只读查看 `/home/lizening/research-notes/agent-logs/2026-10-30T033500Z__CODEX__si-repro-independent-review__b18f/INDEPENDENT_REVIEW.md`。该独立复算记录报告当前runtime/authorization/launch绑定、82+82任务源文件、base/adapter树及部分package/import收据匹配，并明确当前字节存在不等于重新训练/评估可重跑、未证明历史独立或远端完整custody。这是新的可复现性附录证据，可在其适当范围引用；本次仅阅读其报告，没有再次复算上述文件。

对合并的限制：仍应在工作稿附件补齐可定位的科学代码/配置及证据索引、数据受控获取方式、完整依赖与历史未知说明、R19单独方法；两个具体checkpoint的比较不得升级为训练算法平均效应或data source净因果效应。正文仅新增方法说明，不回写旧科学协议，不改变冻结baseline或joint operator。第一份报告要求四项前置门槛先成立并独立复核、之后才设计新评估的修订继续适用。
