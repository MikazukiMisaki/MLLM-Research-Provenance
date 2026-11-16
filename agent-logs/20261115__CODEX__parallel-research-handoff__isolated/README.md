# 并行研究进度与论文：Sol Pro 审阅入口

本目录是 2026-11-15 的私有研究记录快照，面向本课题后续分析。原本的本地工作树包含其他未审阅文件，本目录不是完整工作树或对历史科学执行的独立认证。

- [完整中文论文工作稿 V2](reports/parallel_research_round5/RECOVERY_MAINLINE_MANUSCRIPT_ZH_DRAFT_V2.md)：真实开发汇总、虚构题面模型观察、动作编号与第二件机会、文献定位、成本及局限。为避免携带未核准逐案内容，涉及两份历史报告的链接指向明确标注的聚合转述，原始本地论文不变。
- [三方向证据范围](reports/parallel_research_round5/THREE_DIRECTIONS_REPRODUCIBILITY_EVIDENCE_MATRIX_V2.md)与[已有量化汇总](reports/parallel_research_round5/CROSS_DIRECTION_QUANTITATIVE_EVIDENCE_SUPPLEMENT_V6.md)：动作编号和排列、双物体机会、恢复链；历史 TV 精度、数据来源和执行未因本快照获得认证。
- [第二件可见观察](reports/parallel_research_round5/SECOND_OBJECT_VISIBLE_ACQUISITION_RESULTS_V1.md)、[错误子目标](reports/parallel_research_round5/INCORRECT_SUBGOAL_HANDOFF_RESULTS_V1.md)、[矛盾诊断](reports/parallel_research_round5/INCORRECT_DIAGNOSIS_HANDOFF_RESULTS_V1.md)、[候选得分](reports/parallel_research_round5/DIAGNOSIS_SUBGOAL_CANDIDATE_SCORES_RESULTS_V1.md)、[得分交互](reports/parallel_research_round5/HANDOFF_GOAL_DIAGNOSIS_INTERACTION_V1.md)。每项均明确人造题面、实验批次、限制及成本。
- [7/8 配对的 CPU 审阅包](research_packages/recovery_handoff_counterfactual_v1/README.md)：包含虚构题面和保存的模型输出，可以按包内说明重算。
- `evidence/sanitized_synthetic_logs/` 是八份人工题面日志的白名单字段导出。它们保留提示、编号映射、已存 token 和分数等，不包含 GPU 身份或本机配置；导出文件不是原日志，摘要不同，固定原始摘要的脚本不能直接将其当原日志使用。对应原日志及各研究的可信边界见报告；没有全量 logits，不认证设备、权重或物理执行。
- `scripts/` 和 `src/` 是与这些观察有关的代码摘录，仅供审阅，不包含模型、机器配置、完整依赖或环境；并非可直接重跑的完整软件分发。

## 必须保留的研究边界

错误子目标实验使用八个虚构情境，7/8 只是给定条件下的动作选择；没有环境执行、真实轨迹后果、自然错误率、总体因果结论或留出验证。历史两阶段 V2 的 1/10 和 60 任务恢复汇总是旧报告转述，未在本轮核验底层记录；所见 0 个有害配对来自原继续全失败的十状态，不证明一般无害。候选内归一化得分不是任务成功概率或校准信心。

本快照不包含受保护任务、未核准逐案报告、第二件受限窗口包及其三份输入、服务器配置、凭据、模型权重和所有未审查的历史文件。原始日志及其他本地材料未全部上传；部分旧报告保留指向不在本快照的历史来源链接，主论文核心链接及本页入口优先使用本目录内内容。项目过去的访问范围偏差记录单独保留，不因公开聚合转述而解除数据限制。

仅向有权限的 GitHub 用户／连接开放；是否能被具体 ChatGPT 对话读取，取决于该对话所使用的 GitHub 连接和权限。

## 本次审阅补充

- [脱敏日志 CPU 复算入口及限制](SANITIZED_REPRODUCTION_V1.md)：四份固定摘要的虚构题面日志可在 Python 标准库下复算；不认证模型输入、设备或实际执行。
- [各方向稿件在本快照中的全文覆盖范围](SNAPSHOT_SCOPE_V1.md)。
- V2 论文将冲突交接问题置于摘要中心，并写明唯一归一化权重下降约为 1.32×10⁻⁹、对精度敏感。
