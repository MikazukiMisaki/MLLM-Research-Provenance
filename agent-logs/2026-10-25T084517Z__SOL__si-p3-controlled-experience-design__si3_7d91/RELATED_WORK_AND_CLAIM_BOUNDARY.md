# SI-P3 研究主张边界（设计阶段）

2026-10-25仅查阅原始论文页面；没有对既有实验重新统计或执行新学习。本文不是系统综述，也不保证排除了所有近期近邻。

- [Re-ReST, EMNLP 2024](https://aclanthology.org/2024.emnlp-main.861/) 已研究由环境反馈改善模型自生成样本，再训练agent；其摘要亦包含ALFWorld。因此“环境反馈+纠错经验+微调”本身不能成为本项目首创声明。这里拟检验的更窄问题是：在同一完整生成池、同一学生输入与受控更新预算内，失败感知的成功采纳是否胜过success-only采纳。
- [Agent-R, arXiv v3, 2025](https://arxiv.org/abs/2501.11425v3) 已研究从错误轨迹构造纠错训练路径并迭代自训练，使用MCTS和模型引导批评。本协议不引入树搜索、反思训练、多轮自训练或额外模型，也不能将“从失败学习”独占为创新。
- [Fagerland, Lydersen & Laake, 2013](https://link.springer.com/article/10.1186/1471-2288-13-91) 指出exact conditional McNemar的保守与功效代价，并更推荐mid-p等替代。本项目继续此前预设的exact检验，是明确接受的设计取舍；并不是该论文推荐exact最优，也不在看到结果后换检验。

最强可争取贡献是：在固定小模型与推理接口下，以可审计的共同生成池/终局配对反馈控制训练数据采纳，展示或否证独立任务上的真实成功率改善，并呈现收益、伤害与数据获取成本。C={teacher成功且原actor失败}，B={teacher成功}，故C在B中只是原actor失败感知的成功采纳；不能单凭C>B断言新颖价值估计、因果信用分配或排除了hard-case mining。

teacher是同一base checkpoint的adapter-off两阶段控制器，student从已受专家监督的P0出发。应称“专家SFT初始化后的、同基座纠错经验学习/受控self-improvement验证”；不是从零、纯学生自举、无专家或已实现自主持续改进。只有新冻结学生C在独立actor-only任务上超过A，才得到新的self-improvement成功率证据。仅有可采正例、训练loss下降、oracle或C>B均不能替代。

任务隔离主要保证canonical task/trial不重叠；相同物体/房间模板、scene/layout和人工未登记查看的剩余风险必须披露。若无法形成独立评估，不通过改名held-out解决。当前仅设计，不改变旧论文proposal和冻结科学文件；将来论文应明确记录研究问题迁移及其证据原因。
