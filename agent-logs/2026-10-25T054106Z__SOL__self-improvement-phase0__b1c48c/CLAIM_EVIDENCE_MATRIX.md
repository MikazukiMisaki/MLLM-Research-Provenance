# SI-P0 主张—证据矩阵（独立审查）
协调方Sol；截至本目录的原件核对。OBSERVED为历史原始记录事实，不是新实验。新调用0，R19campaign仍5142 generations/7949 environment operations（含reset；不含历史SFT训练的全项目预算）。

| 论文主张 | 独立证据及状态 | 可写结论/不可外推 |
|---|---|---|
| 专家SFT提高该agent任务能力 | independent_raw_recount.json：60同task/seed/reset/schedule/horizon/pipeline的记录；base3、SFT48、45胜0负；任意won与终局won相同 | 支持已开发任务的专家模仿效果，75个百分点；历史启动/runtime完整receipt缺失，写清局限。不是自身经历学习。 |
| 提升只是学会输出Action-ID格式 | independent_action_contract_recount.json：base2816/2817 grounded，SFT1355/1355 | 仅1个base格式违例不能解释45个配对任务增益。该反驳不隔离规划/导航/其他技能的因果贡献。 |
| 新任务上也改善75个百分点 | independent_unseen_recount.json：60/60冻结日程匹配，SFT49/60，开发ID交叉0 | 只有SFT单臂，支持已记录迁移表现；没有同批base臂，不能给heldout提升。不得重新把已看过的结果称新heldout。 |
| 训练数据是agent自采样 | expertJSONL及Luna来源审计：1200任务20967行，18828train/2139val、1074/126任务；来源标handcoded expert | 专家模仿，不是自主self-improvement；当时rejected候选逐案缺失、base/tokenizer完整revision未证实。 |
| 冻结训练split/exclusion绑定矛盾 | independent_raw_recount.json的canonical_bindings三项精确匹配；Luna更正addendum | 撤回raw-vs-canonical混比的误报；不能据此说数据漂移。匹配文件对象也不能倒证历史实际加载。 |
| 最终专家数据内部完全无输入歧义 | independent_raw_recount.json：110同prompt不同目标组，237行，107组同task/trajectory；field错误0 | 可报告局部多解/有界观测歧义；不等于标签错误，不证明失败机制。148去重前−21exact=127去重后重复occurrences，计数阶段解释一致。 |
| R19固定恢复已提高强基座成功率 | 原正式G4与independent_r19_experience_recount.json：CONTINUE30/36；K1..5=29/30/28/25/24 | K2与CONTINUE均30（2rescue/2harm），不能称总体提升；K2平均logicaltokens高31.9%。registered非显著不当等效证明。 |
| 自适应停止已有5.56pp增益 | bestfixed30 vs hindsightoracle32，两个额外病例CONTINUE本来成功；7supported/29coverageonly | 只有回顾oracle空间，未实现在线策略/新任务提升；不是self-learning的上限。 |
| 有183个独立纠错经验 | R19 39branches/183K记录、36eligible独立trial；各K引用共同路径/alias。独立所有K rescue union只有2task | K与别名不是独立样本。不得合并120旧prefix与36新prefix成为156独立训练N。 |
| 已有候选可立即组成新训练集 | Sol Research索引及independent_historical_rescue_verification.json：31旧处理rescue行涉及15canonical task；R19另2task独立重数，prompt/map/结果refs存在 | 候选索引，不是逐行合格训练集；不同actor/context/处理要分开，public输入投射及终局信息隔离未逐行通过。不能复制少量样本制造N。 |
| 从自身经历训练后已超越SFT-P0 | 尚无新权重、等预算普通selftraining对照或新任务结果 | NOT_DEMONSTRATED；这是拟议研究问题。 |
| “恢复成功后再SFT”本身是新方法 | Re-ReST及其他primarysources见NOVELTY_AND_FEASIBILITY_REVIEW.md | overlap明确；新颖性需要同poolsuccess-only对照和新任务学习收益，不能凭流程新命名。 |
| 未来还有干净测试空间 | Luna目录差集及independent_identity_file_presence.json：六family且有game文件的已知登记差集为train1141/seen0/unseen74；污染全表仍未闭合 | 只允许候选identity层面的审计，不生成schedule、不读取未消费outcome，不把134−60直接当授权/干净样本。 |

本矩阵优先采用独立原件重数及Luna最终更正，旧报告/JSON的raw-vs-canonical误报原字节保留作审计历史，不能脱离更正单独引用。最终可行性结论与后续设计以PHASE0_DECISION_AND_NEXT_STEPS.md为准。
