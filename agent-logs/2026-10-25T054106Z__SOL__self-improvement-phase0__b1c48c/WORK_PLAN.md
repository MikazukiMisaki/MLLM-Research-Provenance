# 自我改进研究流程：SI-P0工作计划
状态：SI_P0_AUTHORIZED_READ_ONLY_AUDIT_AND_DESIGN；新训练/推理/环境执行NOT_AUTHORIZED。用户授权主导整体流程、沿用Sol Research与Luna；本阶段开始审计与设计，不凭笼统授权制造未来科学clearance。
启动UTC2026-10-25T05:41:06Z；provenance base a9de0cd16d23bb0b044784e93650f77366bcb3b5，科学analyzer85/source2da不变。

| 顺序 | 工作/负责人 | 交付与验收 |
|---|---|---|
| P0-A并行 | Luna：历史SFTraw与来源/分割/运行绑定 | 独立重数60dev/60unseen，有原件引用、hash、缺失与边界；不将expertSFT说成自主改进 |
| P0-B并行 | Sol Research：自身经验清单/独立去重/可学习性 | 区分真正rescue、普通成功、harm/incomplete；有可追溯训练输入候选和足够覆盖的依据，或明确NOT_READY |
| P0-C | Sol：独立抽查原件/重数、贡献主张与近邻对照 | CLAIM_EVIDENCE_MATRIX、NOVELTY_AND_FEASIBILITY_REVIEW，不能仅用两位agent自评PASS |
| P0-D | Sol整合：最小一轮A/B/C草案、资源/统计/停止条件 | 数据不足则停止方法分支，收敛实证论文；数据支持仅进入下一份具体协议/实现审查，不自动train |
| 后续条件阶段 | 另行明确实现/测试→exactSHA独立审查→Luna只读执行准备→具体科学授权 | 不沿用已消费R19许可；不使用新heldout/teacher/memory/selector/DPO绕过当前范围 |

当前实际派发目标：Sol Research 01a165de-c75e-7120-abc9-fa74cde1f17f；Luna 01a09fcb-ab5f-7b83-9acf-91026145b764，host remote-ssh-discovered:sdxsrv03。任务单详见本目录，正文可独立复制。发出与确认分别记录，不把queued当ack。

人力首轮：Luna≤2人时、Sol Research≤2人时；提前完成即返回，未证实就报告；这是新SI-P0任务，不冒充此前未启动的4人时36诊断审计。科学调用上限0；允许纯stdlib只读解析历史记录用于审计，不运行项目科学流水线或重新估计新policy。

文件协调：各自只写指定unique目录，不改共享INDEX/rootinventory，不commit/push；Sol统一审查、保留原件、扫描、选小文件、窄提交和远端核验。原始raw、大dataset/weights/cache不复制。

停止/降级：证据矛盾先保留并报告；缺raw不修补、不补跑；没有足够独立可验证纠错经验则NOT_READY，不训练/扩采集；创新与常规selftraining未分清不称新方法；无干净可用新任务空间不承诺验证；任何模型/环境/训练或新科学调用需求必须在具体设计闭合后单独处理。
