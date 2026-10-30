# 历史参与审计独立复核

结论：`ACCEPT_BOUNDED_IDENTITY_LINKAGE_WITH_SCOPE_LIMITS`。Sol 审计确切 SHA-256 `6746ee1d5d8379842d8eea65467e8c52d577460e6374b676883a346e9841f295` 已匹配。主要身份链、账本重复和曝光限制表述可接受；不构成完整历史曝光证明、独立任务证明或新评估许可。本记录不披露候选身份、内容或任务结果。

## 本次直接复核

使用独立编写的 `check_metadata.py` 读取保存的 JSON/JSONL 元数据，输出 `METADATA_VERIFICATION.json`；每个读取的科学输入均核对 Sol 报告配套 JSON 中的 SHA，并在读取结束后复核字节未变。

1. R14 `run_manifest.json` 记录 completed、accepted_episodes=180，其 raw_trajectory_sha256 与实际 raw_trajectories.jsonl 相符。实际文件含 180 行、180 个唯一 schedule index、180 个唯一 task identity、170 个 parent-name 字符串；与已保护登记表 R14_completed_schedule_positions 的身份集合完全一致。这支持“已保存完成记录绑定源轨迹字节”，不是仅有待执行计划。它不能独立认证所有历史执行过程或模型算术。
2. R15、R16、R17、R18-C1、R18-C2 的已保存 manifest 均报告 completed；每组 replay 和对应 branch 各 60 行、60 个唯一身份三元组；两类账本三元组相同，并经 schedule index 和 task identity 完整映射到 R14。五组的 60 个三元组集合完全相同，保存的 replay-pass/replay-match 值均为 true。这证明保留记录之间的身份连接与记录状态。
3. R15/R16/R17 replay 文件逐字节相同；R18-C1/C2 replay 文件逐字节相同，SHA 分组与审计一致。不能将这些复制或继承的记录计为五次独立物理回放，也不能计为 300 个新增独立任务。相同字节也不反向证明物理上只执行过一次：本次不能确定实际执行次数。
4. 后续阶段 completed manifest 与现存账本的当前哈希，不能自动等价于“每份账本由其 manifest 当时认证”。本次明确核实的原始文件哈希绑定是 R14 manifest→raw trajectory；后续是已保存记录的身份连接。Sol 正文对后续 supervisor receipt 未认证的限定是必要且恰当的。
5. trainer_state.json 的 log_history 实际有 237 项；除吞吐率字段 eval_samples_per_second 外，没有包含 task/sample 的标识字段。这些汇总日志不支持逐任务优化器参与收据；没有标识字段不意味着任务未参与训练。报告已保持此边界。

## 未在本次独立复算的来源主张

本次未重算 ZIP 的 1,207 个旧版路径及其 0/16、0/5 交集，未重算 P0 的 1,200/1,074/126 分割与 2,354 updates/选定 checkpoint，也未重算最初 SFT 候选的五个 parent overlap。这些段落有先前报告出处，本次仅审查其推论边界；不能把本记录引用为这些数值的新独立复算。未进行全盘历史搜索，故“未定位完整 receipt”不应写为“receipt 不存在”。

## 一个非阻塞文字修正

首段称 input paths and fingerprints 均记录于 HISTORY_LINKAGE.json；实际该 JSON 保存符号键和哈希，完整输入路径位于 audit_history_identity.py。建议精确替换为：

> SHA-256 hashes of all inputs were compared before and after the audit; input paths are specified in `audit_history_identity.py`, and their fingerprints are recorded in `HISTORY_LINKAGE.json`.

此问题不影响已独立重算的身份链。本复核自己的 METADATA_VERIFICATION.json 同时记录输入路径与 SHA，便于追溯。

## 可允许用途与限制

可用于论文证据附录中关于“已保存历史记录身份连接”的窄结论，并保留 manifest、现存文件、物理执行三者的区分。parent-name 相同不证明相应旧版 trial 执行过；精确身份零交集、缺少记录或模型日志无 ID 也不证明未曝光。所有 R14 身份已在保护登记表中，连接增强来源说明，不扩大可用任务池。

四项前提仍需各自有证据并经独立复核后，才开始设计新评估。当前记录不证明独立任务、预先规定的可检验假设、统计精度或完整预算已经满足。没有运行模型、CUDA、ALFWorld、训练、实验或科学分析器；只运行元数据/哈希核验；未更改任何历史输入。
