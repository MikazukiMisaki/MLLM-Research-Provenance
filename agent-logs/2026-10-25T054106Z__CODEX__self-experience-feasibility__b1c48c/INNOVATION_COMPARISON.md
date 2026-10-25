# SI-P0 创新边界：指定三项primary文献

状态：有限范围方法对照，**NOVELTY=NOT_PROVEN，EFFICACY=NOT_PROVEN**。本轮只读论文，不复现、不运行作者代码、不扩大文献范围。

| 工作 | 经验及增量信号 | 学习/写回与运行时作用 | 新任务证据边界 | 对本候选的约束 |
|---|---|---|---|---|
| [Re-ReST, EMNLP 2024](https://aclanthology.org/2024.emnlp-main.861/) | actor自采样；环境评分后保留成功，reflector修正失败后再评分；正确/错误经验也用于reflector训练 | reflector与actor均可经训练更新；主设置把成功原样本及成功修正样本写入actor权重 | 论文在多个agent任务报告实验，不等于本项目新任务证据 | “反思后成功轨迹用于SFT”已存在；不能以本候选首次提出纠错self-training |
| [Training Language Agents to Learn from Experience, v1](https://arxiv.org/abs/2605.20477) | actor历史trajectory反馈给reflector；新prompt的训练奖励来自重测历史batch | 学习reflector（GRPO）；actor权重冻结，跨任务写回system prompt，非本草案actor-SFT | 方法按task type作meta-train/meta-test；ICT loop用固定验证任务选winning prompt，不能直接视作一次冻结checkpoint的确认 | 跨任务经验写回已是明确问题；本草案不同写回通道不等于创新证明，也不采用其RL/prompt搜索 |
| [When Harnesses Lose the Signal: Causal Evaluation of Recovery in LLM Agents (CIR), v1](https://arxiv.org/abs/2610.00372) | 在同执行状态配对CONTINUE与恢复，区分rescue/harm；受控observation faults | 用paired监督训练运行时router及错误/结果模型，选择恢复；不以此训练actor动作权重 | 论文的故障/干预设定与本项目natural TRAIN执行困难不同；不能迁移数值效果 | paired增量标签并非本项目新发明；这里若有区别，是用于离线经验采纳并写回actor，而非学习runtime router |

INFERRED：本候选可检验的窄区别是：在同一固定纠错生成池中，以同前缀CONTINUE0/纠错1作为**离线数据采纳条件**，相对普通成功过滤，在等训练预算下是否改善冻结强基座的新任务表现。其两部分各有先例：Re-ReST已有成功纠错self-training，CIR已有paired recovery supervision；把二者连在一起是待验证组合，不足以宣称首创。ICT进一步表明“经验跨任务写回”本身不是新问题。

还不能声称：首个自改进ALFWorld agent、首个弱base纠正强SFT、首个增量信号、首个经验筛选、或首个因果自改进。只查三篇不能排除更直接先例；未检查所有后续版本和相关工作。尤其CIR中的rescue/harm估计依赖模型化边际概率，不能偷换为精确个体反事实概率；本项目已观测同前缀终局标签也不能证明每条纠错推理正确。

主要竞争解释及反证：

- 普通成功self-training本身就够：C若不优于B，不能归功增量采纳。
- 好处来自额外teacher、生成预算或背景样本：B必须公平可见相同生成池，B/C同训练token/steps；获取成本另列。
- 硬任务/家族或案例记忆：task级去重、新任务、受控重复；11状态/10任务的历史单步rescue不代表覆盖。
- 挑K/挑prefix/挑checkpoint：固定处理与时点、无oracle标签、单轮最终checkpoint，不能从R19最佳K倒推方法。
- teacher correction看过额外上下文：公共输入投影须诚实记录；不训练隐藏状态、事后label或rationale，未来任务表现才回答可迁移性。

已读范围与来源（2026-10-25 UTC）：

- Re-ReST：官方ACL摘要及[论文PDF](https://aclanthology.org/2024.emnlp-main.861.pdf)方法部分、自训练/reflector数据路径和部署设置；作者代码入口[PlusLabNLP/Re-ReST](https://github.com/PlusLabNLP/Re-ReST)仅核对论文官方链接，未运行或完整审阅代码。
- Training Language Agents：arXiv v1摘要、[HTML](https://arxiv.org/html/2605.20477v1)§3 ICT /§4奖励与GRPO /§5.1任务分区及§5.3验证选择限制；未复核每项附录或数值。
- CIR：arXiv v1摘要及[HTML](https://arxiv.org/html/2610.00372v1)paired干预与router方法部分；未复核全部实验/附录或运行其软件。

以上对论文内容为方法摘要，区别判断明确为INFERRED；没有论文实验的本地复现。本文不建议采用GRPO、memory、learned recovery selector或在线prompt优化，现有禁令不变。
