# 统计解释短稿：证据及审阅记录

状态：冻结方法的静态独立核对完成；英文补稿为候审整合文本。本次只读已完成研究的文档和源码，未读取候选池、未执行提取器或分析模块、未调用模型/环境、未设计新评估。正式分析文件只作字节哈希绑定；数值表引用既有独立复算明细，并非本次重新计算。

## 可读源码锚点

- S2 的 35–41 行：双侧 exact p 与零分歧返回 1；44–58 行：完整任务及布尔结果验证；61–70 行：胜负、效应、以 n 为分母的 CP 差区间；72–76 行：两比较 Holm；17–32 行：CP 两尾及 100 次二分；88–96 行：冻结警报优先、正信号、严格 −5pp 下界支持规则和解释限制。
- S3 的 80–95 行：82 个父任务、246 个结果、身份/顺序/seed 与完整性校验；171–173 行：构建 pairs 后载入经哈希绑定的 S2 并调用 analyze。实际提取器 SHA 与 062 审阅相符，原计划的旧提取器哈希不冒称未变；统计源码 SHA 持续与原计划一致。
- S5 原独立源码使用另一路高精度 binomial CDF inversion；其既有明细报告数值一致至 1e-12。本次只读源码与明细，不复演该独立复算。

## 文本用途与边界

STATISTICAL_METHODS_ADDENDUM_EN.md 可供论文方法或统计附录整合前再独立复核。新增的是已实施方法的公式和解释，不是新增估计量、分析家族、阈值、样本或分析结果。原阈值不在短稿重新展开，避免与冻结主方法重复；INCONCLUSIVE 原判定保持不变。

精度与人群解释特别区分：固定排程差值的描述性含义、假设条件下二项推断、跨任务依赖、两个比较/四个分量之间的依赖，以及训练 seed 的变异。Holm 和 union bound 不需要两个比较或四个分量独立；这不能代替任务层面的有效抽样模型。交换性本身不足以推出独立二项计数。

## 文件与确切字节

- **S1_plan**：[文件](/home/lizening/research-notes/agent-logs/2026-10-29T225000Z__LUNA__si-u1-extraction-publication__062a/frozen_and_review/FINAL_ANALYSIS_PLAN_PILOT82.json)；SHA-256 `7643900c2b417e9d2497d8acb195f6754ebe04f3f2c6242625948874100dc23f`。
- **S1_binding_review**：[文件](/home/lizening/research-notes/agent-logs/2026-10-29T113523Z__ASTRA__three-arm-prospective-design__a55d1af9/FINAL_ANALYSIS_BINDING_INDEPENDENT_REVIEW.json)；SHA-256 `077a0450dfb56e182f86f06a6e4e8fe5900cd0c50e4d140d324291913d9f6bfc`。
- **S2_frozen_statistics**：[文件](/home/lizening/research-notes/agent-logs/2026-10-29T114500Z__SOL__si-paired-stats-reference/paired_stats.py)；SHA-256 `dc65a06fda495517bc76357022a90a0622d1b17c11ee101e19d958aebb5e3251`。
- **S3_extractor**：[文件](/home/lizening/wt-si-u1-result-extractor/si_u1_extract.py)；SHA-256 `336d4c95c51df2bac97fac13bdc91791a64afce5c68a64cdee1c48f3b03648e9`。
- **S3_extractor_review**：[文件](/home/lizening/research-notes/agent-logs/2026-10-29T225000Z__LUNA__si-u1-extraction-publication__062a/frozen_and_review/EXTRACTOR_062_INDEPENDENT_REVIEW.json)；SHA-256 `3a7b2bd851440711773fb724df4dd1b8f9325d57db99e91a576daf849c423e20`。
- **S4_accepted_analysis**：[文件](/home/lizening/research-notes/agent-logs/2026-10-29T225000Z__LUNA__si-u1-extraction-publication__062a/frozen_and_review/FINAL_PILOT82_PAIRED_ANALYSIS_C2356.json)；SHA-256 `4a3ea016d4c06022980482ac9dbc58155a68bbe20fbc723a68ce49c7c345ea9b`。
- **S5_independent_statistics_detail**：[文件](/home/lizening/research-notes/agent-logs/2026-10-29T222200Z__SOL__si-u1-independent-recompute__c2356/INDEPENDENT_STATISTICS_DETAIL.json)；SHA-256 `47311ee5f8e3fa0022019e43da97c70ebb61b8aaa0f3e856c5a2854ef3a9f19d`。
- **S5_independent_statistics_source**：[文件](/home/lizening/research-notes/agent-logs/2026-10-29T221000Z__SOL__si-u1-independent-statistics__c2356/independent_stats.py)；SHA-256 `e7ec762a7ae6d2643d5393634c5318a63d83bbf22d1330508b0511bcef4cab06`。
- **S6_scientific_acceptance**：[文件](/home/lizening/research-notes/agent-logs/2026-10-29T230000Z__LUNA__si-u1-scientific-review-publication__c2356/astra/C2356_SCIENTIFIC_RESULT_INDEPENDENT_ACCEPTANCE.json)；SHA-256 `6530145ac3ac579d00cdb57c28f3fa9bb07b27b990cfe0fba6e93b7fcca5eacd`。
- **S7_target_thesis**：[文件](/home/lizening/research-notes/agent-logs/2026-10-30T014252Z__CODEX__si-thesis-advisor-literature__e7c1/thesis/THESIS_WITH_LITERATURE_WORKING_DRAFT_V2.md)；SHA-256 `37d7c34ff2659a194df6849fb1b27494ca181dcec182effd87dd5ec7e9943203`。

S1 为冻结计划与原绑定审查；S2 为原统计源码；S3 为实际修订提取器及审查；S4 为正式已接受结果；S5 为独立算术明细及对应源码；S6 为科学接受；S7 为当前论文目标稿。哈希绑定不证明新一轮运行，也不解决原始样本独立性、完整历史曝光或全部可复现性。
