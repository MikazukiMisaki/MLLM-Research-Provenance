# 自身经验学习：独立创新与可行性审查
状态：INDEPENDENT_DESIGN_REVIEW_COMPLETE_WITH_CONDITIONS；非方法效能PASS，不可执行。协调方Sol，2026-10-25。已审查两位冻结交付及原件；条件见PHASE0_DECISION_AND_NEXT_STEPS.md。

## 现有证据能承受的主张
专家模仿SFT在已开发60任务上3/60→48/60（75个百分点）；原始身份和记录接口匹配。已有valid_unseen49/60是单臂迁移结果，不能说同批heldout提升。两者都不证明从自身经验发生了持续学习。
R19最佳固定K2与CONTINUE均30/36；oracle32/36只比bestfixed多2例，是已观测回顾空间，非任何在线停止器实现的增益，亦非学习上限。R19不能成为一个已成功self-improvement方法。
已有严谨反例和边界可组成研究贡献；工程修复、哈希和严格审计保证可信度，但不能单独当算法创新。

## 最近工作的重叠与候选区别
| primary source | 已存在的机制/本轮读取范围 | 对本项目的限制 |
|---|---|---|
| [Re-ReST, EMNLP2024](https://aclanthology.org/2024.emnlp-main.861/) / [方法原文](https://aclanthology.org/2024.emnlp-main.861.pdf) | agent采样、反思修正、环境验证成功、再训练，含ALFWorld；已读abstract与method | “把纠错成功轨迹拿去SFT”不足以单独形成新方法。 |
| [CIR, 2026 preprint v1](https://arxiv.org/html/2610.00372v1) | 同状态比较refresh/continue，分rescue/harm并学运行时router；已读setting与decisionobjective | paired救回标签不新；本项目若研究训练资料采纳，需要与运行时router区别，不能称其首创。其受控观测扰动场景不自动等同自然失败。 |
| [Training Language Agents to Learn from Experience, 2026 preprint v1](https://arxiv.org/html/2605.20477v1) | 经历反馈训练reflector形成跨任务systemprompt；已读method | “利用经历提升后续任务”已有；本轮不扩到GRPO、memory或反复反思。 |
| [DITS, ACL2026](https://aclanthology.org/2026.acl-long.296/) | abstract明确区分轨迹return和数据学习效用，采用influence导向MAS数据选择；本轮只据abstract，未完整复现 | 高干预回报不必带来高学习收益；不能把rescue标签直接当训练效用或泛称首个value过滤。 |

候选问题：在同一个小模型、公开输入和等预算下，同前缀验证得到的纠错增量能否预测后续训练的迁移收益？这比“恢复是否有时成功”多一个可检验环节，目前没有答案。与DITS的场景/信号不同并不能单独确立方法新颖性；须同时和同池success-only及普通自训练比较。

## 对最小闭环的要求
一轮A/B/C可评估整个纠错资料方案，但C>B可能同时改变样本来源、难度和筛选。若论文主张“增益筛选”机制，需同池D消融，或把B明确定义为同一pool只按成功采纳；不得在三个比较里承诺已隔离所有因素。
必须报告独立task/episode数、重复权重、有效targettokens、训练steps、选择规则、采集和验证成本。仅匹配训练token而漏算多分支生成不公平。先给预算与最小有意义效果，再用独立task簇计划精度，不能从2/36或重复prefix推造有power的N。
学习结果评估必须与训练资料和调参task隔离。已用过的valid_seen和已看过的valid_unseen不能重新命名成新heldout。可用未来任务数需要只读identity/全局污染盘点，不能按总数减60猜测。

## 当前限制
独立解析最终专家集得到20,967条、1,200task、237行属于110个相同prompt不同目标组（107组同task/同轨迹）。这些目标均可通过原动作map字段一致性检查，229行属于pick-two；只构成局部多解/观测歧义线索，不证明因果来源，不据此改输入或扩memory。
历史protocol的split/exclusion/schema声明与当前文件canonical JSON SHA全部相符；原始bytes SHA不同不能当绑定矛盾。开发评估当时完整base/tokenizer/runtime加载receipt仍需如实标缺，不拿现在R19文件倒填。
最终DATA_FEASIBILITY=NOT_READY；PROTOCOL_DESIGN_FEASIBILITY=READY；TRAINING_DATA_READY=NOT_READY。接受设计方向及反证结构，尚无可执行协议；当前不训练、不采新轨迹、不开发selector。
