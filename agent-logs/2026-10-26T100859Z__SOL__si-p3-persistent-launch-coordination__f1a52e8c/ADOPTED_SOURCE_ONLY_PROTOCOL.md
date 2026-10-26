# SI-S01：固定A96 source-only必要条件可行性试验

**DESIGN_ADOPTED_FOR_IMPLEMENTATION / CONDITIONAL_INVESTMENT_GO / ACTUAL_LAUNCH_NOT_CLEARED。** 用户最新明确要求持续推进直到开始实验，并持续授权协调方、Sol Research、Luna分工。协调方现采纳一个比原完整采集更小的单臂阶段；这是新的、前瞻登记的设计/投入决定，不覆盖旧v1/v2原件或旧NO_GO记录。实际科学启动仍必须有新exact-SHA验收、可信执行/资源证据、正向预检、唯一argv及独立clearance；原探针/G3授权均保持已消耗。

## 科学问题与一次投入理由

唯一问题：在固定P0、既定新任务及硬预算下，这个配方是否连必要的失败来源和位置覆盖数量都无法满足？无须采集前证明C24存在。旧6/120不是新96预测；新观察可有限、可证伪地否决当前固定配方。我们接受完整负结果后结束该配方，不以补任务、换seed或扩预算挽救。正结果也仅表示必要上界未否决，不证明teacher成功、Q、C24可构造、学生学习或成功率提升。

因此同意支付**一次固定A96 source-only**的有界信息成本。完整teacher/paired采集、训练及600任务评价仍NO_GO，不为它们预建大管线。Astra的独立初步书面意见和内部独立design critic均支持该有限投入，不要求事前已知C24；Astra最终短记录交回后另绑定。

## 冻结身份与执行语义

1. 精确沿用已采纳metadata reservation SHA256 `6ce8a32a2345b59ecdef9c28c3a341e9c0801b8105f79895f9b2cb9545a4937e` 中A96身份，家族pick-place/clean/cool/heat/pick-two为35/26/16/9/10。旧R19、expert_train、S120及已登记2612 known-use与A96的task身份互斥证据已独立核对；scene/语义/未登记浏览限制保留。不读D48/E600任务正文，不替换身份，不新分区。
2. 每task唯一P0 source正常运行，H50；原Qwen3-8B snapshot、P0 adapter、普通P0 goal/current obs/H4/完整有序map、greedy/thinking=false、生成帽16、parser及正常停止语义不变。P0始终adapter-on，不运行任何teacher或独立suffix。source本身d5之后的P0动作仍是同一source的一部分，不是另起suffix。
3. 所有task固定d=5，只保存第5个真实动作after的S5及H4/map/public projection/hash与原transition引用，须在第6次生成和source终局前持久化。早终止/第5动作done或truncated/显式空map保留正常不可用去向。S5存在且第6次parser正常fail-closed仍可能E内；不能用L>5代替真实checkpoint。缺/矛盾是技术或完整性STOP，不压成0。
4. 现在冻结初始化规则而不读取新task正文：每task nominal/reset seed=42，fresh单game TextWorld pool seed=42，各只做一次初始reset。不能根据结果选择seed或重置；receipt-local index不冒充内部counter。运行计划采用原五家族顺序，家族内沿现contract.rank('SI-P3-prefix-v1', family, canonical_task_id)排序再task_id打破平局；全部cutoff=5。实际manifest/plan哈希由后续Luna准备、独立重算并在任何模型/环境副作用前封存。本阶段只需可证据化的source初始化；未来replay必须另外证明同task/seed/pool/counter等价。
5. 任何Stage1/Stage2 generation、branch/replay reset/step、teacher adapter-off、独立baseline/新suffix、训练/eval入口必须硬拒绝。不是仅靠CLI注释禁用。生成/环境边界需完整typed producer→parser→collector→journal/registry→trajectory→独立source auditor→report正向闭合。

## 正常结果、必要上界与停止

每source正常闭合Y0沿用done && reward>0；正常parser/empty-map/H50失败为0，技术/预算incomplete为NA。已认证source/Y0不可被后续汇总错误抹掉。先完成全部96正常source及每task S5去向、全部真实unit；完整source seal后才判结构性必要上界，不在95条时早停，不做teacher。

E为经过完整证据认证仍可能通过后续完整Q的S5集合，F=E∩Y0=0，S=E∩Y0=1。总量与家族条件同时检查：E≥72且各≥22/17/10/6/7；F≥24且各≥9/6/4/2/3；S≥24且各≥同配额。任何必要上界不足：`COMPLETE_SOURCE96_STRUCTURAL_NO_GO`，结束当前固定配方。全部通过：`SOURCE_UPPER_BOUNDS_NOT_FUTILE`，仅允许返回投入决定，不能继续teacher。所有YT=NA，原因`TEACHER_NOT_AUTHORIZED_SOURCE_ONLY`；上界不足另保留SOURCE_FUTILITY，不把未测YT填成0，不报告恢复率或学习提升。

身份/证据/Action-ID/map/receipt矛盾，技术异常，或预算将超限即整run STOP，不自动重试、不补任务；未满96正常闭合只能INCOMPLETE，不能解释为配方样本不足。failed/open物理单位和保守预留不抹零。原件append-only，未来汇总更正另写记录。

## 严格成本与运行边界

本阶段上限：**4800 generations /4896含reset环境操作 /76800输出tokens /16000000累计输入tokens /8192单次输入tokens /4 allocated device-hours**，各自独立生效且超限前拒绝。环境为最多4800动作+96reset；env construct/close另外记录但不重复算reset/step。所有source初始化与模型装载、等待、审计/清理占用时间计入实际GPU allocation；clock不按task归零。硬帽不是完成预测。

历史科学5142 generations/7949环境操作和旧非零工程CUDA成本单列。新工程身份/模型验证如需真实调用必须有单独新预算与清单，不能借source额度免费跑或复用旧授权。本文件不准任何此类调用。单一新科学run identity、唯一supervised launch、输出须不存在，最多一次启动、无自动重试。正式账本不得把已开始的失败调用变已知零。

## 实现前提与后续

只先实现source-only最小生产链，不实现teacher/training/full paired adoption桥接，不改旧SI-E1/E2或R19/G4冻结行为。Sol只开发测试；协调方独立review exact SHA；Luna负责只读准备/预算/原件；可信执行身份和真实P0资源验证必须先通过。随后正向真实preflight零science副作用、精确argv/env/output/review哈希和独立launch clearance闭合后，才执行本次单一source-only实验。用户已授权持续推进，无需重复常规批准；任何新实验范围或预算不由此扩张。
