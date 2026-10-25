# Sol Research — SI-P3共同池与学习协议设计任务

本任务由用户新请求正式派发，阅读 /home/lizening/research-notes/agent-logs/2026-10-25T084517Z__SOL__si-p3-controlled-experience-design__si3_7d91/COMMON_DESIGN_CONSTRAINTS.md。你的唯一可写目录：/home/lizening/research-notes/agent-logs/2026-10-25T084517Z__CODEX__si-p3-pool-learning-design__si3_7d91。

请独立提出最小受控新经验协议，重点：
1. task/source/prefix预定选择（不使用未来终局标签，不选rescue再挑anchor）；可比较的原source CONTINUE标签与一次teacher首动作+P0suffix；采样总体、可用prefix边界、无效/终局/空map处理、complete=true且cap=true不误排除。固定40/16/16生成帽，不改旧R19。
2. 同一个完整生成池与对称共同质量；B_pool success-only抽样绝不按CONTINUE排除C，C按paired rescue。明确按family或composition匹配能/不能识别什么，标签代数限制。
3. 建议有限采集N与预先冻结yield/coverage/可用训练曝光GO/NO_GO阈值；挑战96+384/480采集+60dev+600eval方案，给唯一推荐和成本/功效限制。非看效应补样，不把历史10/169当新池产率估计。
4. 最小学习控制：A/B/C、公共输入防泄漏、第一动作目标、共同成功背景S是否必要且固定、每task曝光/真实token/更新如何匹配并避免C重复伪数据；没有实际tokenizer数据时明确后续独立工程检查阻断，不虚报训练就绪。
5. 验收、负向与停止条件，claim边界。必要时只查主要近邻原文，不能宣称首创或预期改善已存在。

交付 CONTROLLED_POOL_AND_LEARNING_DESIGN.md、design_parameters.json（推荐值/理由/待闭合条件）、可核查源绑定、RECORD.md、FILE_HASHES.sha256。仅设计/stdlib数学，原始log及实际returncode。请专注设计，不无限追查或写代码实现。预计20–30分钟内返回可冻结成果；遇关键冲突及时汇报。原有SI-P2文件完全冻结，不新增其ACK。
