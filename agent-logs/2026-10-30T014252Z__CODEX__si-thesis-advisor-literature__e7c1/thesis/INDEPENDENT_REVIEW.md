# 文献整合稿独立 exact-SHA 审阅

结论：`MINOR_REVISION_REQUIRED_FOR_LITERATURE_AND_METHOD_ATTRIBUTION`。新稿主体、结果和限定未被破坏；完成下述两处精确措辞修订后适合作为已审工作稿继续整合，不是最终学位提交验收。没有重跑模型、环境、统计分析或科学过程。

## 版本与完整差异

旧稿 `/home/lizening/research-notes/agent-logs/2026-10-30T011215Z__CODEX__si-thesis-r19-integration__ac83/THESIS_WORKING_DRAFT_SI_U1_R19.md` SHA `ca948da71a0b8a207c0e7f04d0072f659dc18da8cc67c53f8d262dd55777c0bd`；新稿 `/home/lizening/research-notes/agent-logs/2026-10-30T013722Z__CODEX__si-thesis-literature-revision__01bf/THESIS_WITH_LITERATURE_WORKING_DRAFT.md` SHA `0fe5f26d0df2025f9dfda3f89a7235e05b73c21fb0cc5b95e1060c338798d4d8`，均已核对。

完整差异存于 FULL_DIFF.patch。变化限于：引言新增自模仿/A³T；LoRA 引用；统计方法引用；R19 前新增 Reflexion/接口审计语境；两条旧文献更新出版信息；新增 [10]–[17]。科学数字、主比较、阈值、方法配置、先冻结入组再延长恢复路径的时序、CONTINUE 身份、183 个标签非独立执行、后见局限及四项门槛顺序均保持原文。

STRUCTURAL_CHECK.json 记录：参考文献恰为 [1]–[17]，无重复编号、未定义编号或未引用条目；全文 Markdown 表格行完全未变；唯一 Figure 1 引用文件存在。SVG/PDF/PNG 三个图文件与旧稿相应文件 SHA 逐字节一致，图题和区间限定也未改。本次核对图件身份与引用，不重新生成图或重复验算其科学数据。参考文献在正文首次出现的顺序并非连续编号（[10/11] 先于 [9]），这是样式待定事项；待学院引用格式确定后统一处理，不是事实错误。

## 新陈述与两项会刊更新

- **[10] 自模仿**：官方 EACL 摘要支持使用有价值的历史轨迹适配动作候选生成模型；稿件未误称 ALFWorld 结果，也未引入其 pruning 方法。[官方记录](https://aclanthology.org/2023.eacl-main.50/)
- **[11] A³T**：作者 arXiv 摘要支持成功与失败轨迹、contrastive self-training，也明确实验包括 ALFWorld。COLM 2024 PDF 的官方搜索结果支持新稿标题、作者首字母及会名；本次直接打开 OpenReview 被浏览器验证页阻断，因此不声称本次已全文读到该最终 PDF。作者预印本标题不同，不能以其标题否定已查到的会议标题。[作者预印本](https://arxiv.org/abs/2403.14589)，[会议 PDF](https://openreview.net/pdf?id=0VLBwQGWpA)
- **[12] Reflexion**：官方摘要明确不更新权重，反思反馈保存于 episodic memory 并用于后续 trials；新稿的短述准确，没有将其改为 R19 同一轨迹内干预。[官方记录](https://proceedings.neurips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html)
- **[13] Grounding First**：官方摘要明确四类接口/触发/处理/结果合约及 recovery prompt 与 counter resets、termination changes 的合成处理；新稿保留不可直接比较的限定。跨 trial wrapper 的进一步依据来自所审本地文献报告，本次官方摘要的直接核对不能冒称全文复核。[官方 REALM 记录](https://aclanthology.org/2026.realm-1.52/)
- **[6] 更新为 NeurIPS 2025**：已直接核对官方主会记录，作者和标题一致。正文 fine-tuning 的细节是未变的既有陈述；其依据为本地审阅对会议 PDF §6.4/App.F 的核查，本次没有重读这些章节。[官方记录](https://papers.nips.cc/paper_files/paper/2025/hash/5d1f02132ef51602adf07000ca5b6138-Abstract-Conference.html)
- **[8] 更新为 ICML 2026, PMLR 306:154443–154475**：官方 PMLR 页直接确认标题、作者、会议、卷页。正文 matched updates/epochs 的限定保持未变，依赖本地报告对最终 PDF p.6/App.B 的既有核查；没有升级为等总成本或纯成功数据比较。[官方记录](https://proceedings.mlr.press/v306/zhang26m.html)

这两项是从有效预印本引用更新为已发表版本，不是旧引用“伪造”的更正。没有用跨论文分数比较证明本项目优越性，也没有出现 first/unique 算法主张。

## 两处需要精确修订

**1. 引言第 11 行的领域限定。** “These methods, objectives, and domains are distinct from the present continuation comparison” 容易误称 A³T 的领域也不同；A³T 实际包含 ALFWorld。建议替换这句及紧接的重复概括句为：

> A³T also evaluates on ALFWorld, but its contrastive objective and multiple rounds of trajectory collection and training differ from the one-round supervised continuation procedure studied here. Across these studies, the models, data-construction procedures, objectives, and evaluation settings vary.

**2. 统计第 62 行的 McNemar 引用。** [15] 适合作相关比例检验的历史出处；仅挂在 “two-sided exact McNemar test” 后，未落实本地文献审查要求的精确条件二项计算说明。建议用下句取代当前第二句：

> For each paired contrast, we used the McNemar framework for correlated binary outcomes [15] and computed a two-sided exact conditional binomial test on the discordant pairs, under an equal win/loss probability of 0.5; the two resulting p-values were adjusted using Holm's procedure [16] at family-wise α=0.05.

这是说明已采用方法，不是新的检验或重分析。若最终附录给公式，应绑定冻结统计实现及零分歧分支，不应只凭历史论文推定具体实现。本次没有重新定位或执行冻结统计代码，故不把拟补公式写成新的源码核验结论。

## LoRA / Holm / Clopper–Pearson 与原方法的适配

[14] 用于 LoRA 名称和冻结基座、训练低秩参数的背景适合；本项目 rank/alpha/dropout、是否续训已有 adapter 和实际载入字节仍应来自本地证据。原文没有将 alpha 写为有效 scaler，也没有把普通 LoRA 改称 QLoRA，正确。作者预印本摘要本次可读；会议 OpenReview 页面被验证拦截。[LoRA 作者原文](https://arxiv.org/abs/2106.09685)

[16] 对两项 SI-U1 p 值使用 Holm，及 R19 四项比较的另一检验族，保持各自范围，不能把它扩写为总体代表性证明。[Holm 原论文入口](https://www.jstor.org/stable/4615733)本次仅返回空壳页面；引用信息与本地文献审查一致，不声称全文重新核对。

[17] 位于四个 marginal Clopper–Pearson 区间之后，适合作单个二项比例区间的出处；新稿明确四个 98.75% 区间组合为 nominal conservative simultaneous 95%，没有直接写成 1934 论文发明了本项目的四分量差区间。但为彻底避免归属混淆，建议（非阻塞）补：

> The simultaneous coverage follows from the four-component union-bound construction specified in the frozen analysis, rather than from a single Clopper–Pearson interval.

这不需四个分量彼此独立，但每个区间及总体解释仍需各自适用的抽样/模型假设；原稿已保留该限制。[Biometrika 1934 卷期原始目录](https://www.jstor.org/stable/i315388)可核对作者、标题和页码；本次 OUP 原文入口无法读取正文，不声称重新推导或核实原论文全文。

## 审阅范围与剩余工作

本地主要依据为 `/home/lizening/research-notes/agent-logs/2026-10-30T060000Z__CODEX__si-r19-independent-literature__a183/INDEPENDENT_LITERATURE_AND_NOVELTY_REVIEW.md` 及 PRIMARY_SOURCE_RECEIPTS.json；其覆盖是针对性检索，不是系统综述。DARC、AgentDebug、Last Step Matters 未在新稿纳入，不妨碍这次有限修订，但不能宣称相关工作已穷尽。旧 [1]–[5]/[7]/[9] 的内容未改，本次依据已审旧稿和本地原文审阅，不宣称全部再次原文复验。

新稿和旧稿未经本审者修改。此结论只针对所列 exact SHA；后续修订应再核对 diff 与新 SHA。科学结论仍为 SI-U1 inconclusive、R19 hindsight-only，四项前提尚未通过。
