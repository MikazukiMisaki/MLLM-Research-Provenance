# 文献整合稿 V2 独立验收

结论：`ACCEPT_AS_REVIEWED_WORKING_DRAFT`。被审文件 `/home/lizening/research-notes/agent-logs/2026-10-30T013722Z__CODEX__si-thesis-literature-revision__01bf/THESIS_WITH_LITERATURE_WORKING_DRAFT_V2.md` 的 SHA-256 已确认为 `37d7c34ff2659a194df6849fb1b27494ca181dcec182effd87dd5ec7e9943203`。

前稿 SHA `0fe5f26d0df2025f9dfda3f89a7235e05b73c21fb0cc5b95e1060c338798d4d8` 同时匹配。完整 diff 已阅读并保存 V2_DIFF.patch；从前稿应用三个约定的唯一文本替换后，所得字节与 V2 完全一致，没有其他改变。

1. A³T 现明确同样使用 ALFWorld，区别在 contrastive objective 及多轮采集/训练，而本项目为一轮监督续训。这解除领域不重叠的歧义，也未将“一轮”误写为仅一次 optimizer step。
2. McNemar 原论文现作相关二元结果比较框架的出处，随后单独说明实际采用对 discordant pairs、零假设下胜负概率 0.5 的双侧精确条件二项检验，再对两个 p 值作 Holm 校正。此措辞符合已审原方法的层级，不冒称 1947 原文直接规定本项目全部计算。
3. Clopper–Pearson 单个比例区间与冻结分析的四分量 union-bound 同时覆盖构造分开。相邻句继续保留 task-level sampling/exchangeability 限制；没有用这种构造证明固定 TRAIN 样本具有总体代表性，也没有要求四个分量彼此独立。

结构复核见 V2_STRUCTURAL_CHECK.json：参考文献内容未变，[1]–[17] 全部唯一、全被引用、无悬空编号；所有 Markdown 表格未变；Figure 1 引用未变且有效，SVG/PDF/PNG 三个文件哈希仍与旧稿一致。两项会刊更正、LoRA 引用、所有科学结果、R19 分母/时序/后见限定、事后诊断和四项前置门槛均未改。

原 INDEPENDENT_REVIEW.md 的两项措辞问题已关闭，非阻塞 CP 建议也已落实。该验收允许作为经过限定审阅的论文工作稿继续使用；文献搜索覆盖不等于系统综述，部分原文访问限制、完整方法附录和学院格式仍遵循原审阅记录。本次没有重新联网、重算统计或运行模型/环境/科学分析器，没有修改原稿、图件或科学证据。
