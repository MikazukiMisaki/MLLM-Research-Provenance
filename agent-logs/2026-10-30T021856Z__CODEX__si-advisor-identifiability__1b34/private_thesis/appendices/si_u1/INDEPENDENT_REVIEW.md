# SI-U1 可复现性附录独立审阅

结论：`ACCEPT_APPENDIX_CONTENT_WITH_BOUNDED_EVIDENCE_SCOPE; FIX_COMPANION_HASH_BEFORE_BUNDLE_ACCEPTANCE`。

已核验附录 `/home/lizening/research-notes/agent-logs/2026-10-30T064500Z__SOL__si-u1-repro-appendix__8be2/SI_U1_REPRODUCIBILITY_APPENDIX.md` exact SHA-256 `7fd0db41d8223e70dfca0f9e45f68d4214e97458edc457b7c60c3e7470aab592`。正文可作为限定范围的论文工作附录；配套证据索引一处错误 SHA 需先修正。本次不重跑科学过程、不执行原 checker、不触及候选任务，也未重新遍历模型权重、164 个输入或归档正文。

## 唯一阻塞配套索引验收的问题

`EVIDENCE_MAP.md` 的 decoder RECORD 摘要哈希抄漏字符。该地图本次 SHA 为 `9b0614b8824c44dcce93cb0667c840eea6552d665dbc9a2097ecd24638e88476`。对应源文件是：

`/home/lizening/research-notes/agent-logs/2026-10-30T032000Z__CODEX__si-runtime-decode-audit__1f3b/RECORD.md`

实际完整 SHA-256 应为：

`2b4c6567a247af53f35eacd78fef6d0ef6cc8615fb5de1b4aec6a0954f19149c`

地图当前写为 `2b4c6567a247af53f35eacd78fef6cc8615fb5de1b4aec6a0954f19149c`。建议另存更正版地图并刷新相应文件清单，保留原稿。不影响附录正文对 5,001 次 recorded generation 的描述；不能把错误短串当完整 SHA 引用。

独立核对地图中可直接识别的 15 个“绝对路径＋摘要”对，14 项匹配，仅此一项不匹配；没有假装自动复核所有“同目录/旁边文件”省略路径的引用。结果与被审包当前摘要见 DOCUMENT_HASH_REVIEW.json。

## 内容逐项判断

| 主题 | 证据与判断 |
|---|---|
| 数学复算、字节核验与完整重跑 | A 节分成三种活动正确；没有把 arithmetic agreement 升格为模型实验重复或总体有效性。 |
| P0 来源与训练参与 | B 节把 hand-coded 来源追溯到同时期报告/文件绑定，并承认未逐任务重建生成器执行、无逐任务优化器收据、旧模型/tokenizer revision 与 launcher 缺失，符合已有历史审计。1,200/1,074/126、20,967、两遍/2,354 属于既有来源记录；本次未重新计算这些历史数据。 |
| canonical hash 更正 | 正确撤销旧“文件哈希冲突”解释，同时不把 canonical 匹配升级为历史实际加载字节证明。 |
| B/C 续训与来源差异 | 同 P0、78 父/四示例、1,248 microbatches/78 更新/6,240 targets 与已审方法及实际接受记录一致。明确不同任务/状态、输入计算不等、全候选 ranking 未独立重做；没有宣称来源单因素效果。三种 adapter digest 是树序列化身份，不是每个父任务都优化过的逐任务证明。 |
| 已记录运行与版本 | C 节对 completed/246、5,001 decoder flags 及 Python/库版本使用 recorded 范围；ALFWorld 空 version string 但文件绑定、不等于完整依赖树/lockfile 的表述正确。共享 GPU 区间不证明独占。 |
| 当前本地文件 | 正确区分旧独立 inventory 的 base/adapter 全树匹配与本次只复核 164 inputs、12 lineage、8 package entries。旧独立审查明确 12 base symlink 的目标在当时可解析；原目录存在不保证搬迁后的目标可用。当前字节相同不能证明历史曝光、场景独立或全部历史执行状态。 |
| 新本地 checker 的能力 | 静态阅读 check_appendix_inputs.py 与 APPENDIX_LOCAL_CHECK.json：脚本只用标准库，断言绑定与计数，按清单哈希 12 片、在内存组装，再流式读取 32 个 regular members 的尺寸/摘要；没有模型、环境或原分析调用。输出报告的检查范围与源码相符。本次不执行该脚本，不声称新计数经第二次独立复算。非原子逐文件检查，且一些上游来源真实性需依赖先前审查，不能作为完整发布/运行闸门。 |
| 修复时点与盲态 | 直接读取两次 PROCESS_RECEIPT：首次 returncode=1、analysis_exists=false；第二次 returncode=0 且分析摘要匹配 4a3ea0…。首次记录旧 extractor c0827b…，第二次记录 336d4c…，第二次输入绑定技术补充 526cc7…；二次调用起止时间有明确先后。D 节写明 post-evaluation、首轮已读结果字节做哈希、此前运行结构检查、不能证明所有人或进程盲态，正确。 |
| 修订范围 | 与已审 EXTRACTOR_062_INDEPENDENT_REVIEW.json 及此前方法审查一致：只改变 tokenizer 文件绑定接口，统计代码/原规则/结果输入保持；不表述为评估前修复或事前无结果接触。expected targets 在这里按 production byte-binding contract 理解，不应扩写为新验证了 target 绝对路径位置约束。 |
| 本地归档与远端 | E 节把 12 片、46,536,262 bytes、32 members 的本地 inventory 检查与远端 Git object metadata 分开；11 大片无正文、第 12 小片在该次未比正文的边界与先前 inventory 独立审阅一致。没有把本地＋同机 Git object 当独立灾备。source96 独立归档明确另述，与其 CUSTODY_REVIEW.md 一致；本次没有重新发起远端请求或全文下载。 |
| 对外分享 | 原始身份、prompt/轨迹、权重及数据有访问和再分发条件；哈希不能代替权限或历史隔离。附录没有承诺完整复现或授权新研究。 |

## 成本口径与非阻塞补充

当前附录只提设备分配区间和共享 GPU，没有新增总成本数，也没有把 logical token 当物理开销，故未发现成本数值冲突。若其承担完整可复现性/资源记录入口的职责，建议补入下述历史口径说明，或明确引用主文成本段：

> The recorded B/C continuation runs and the completed SI-U1 evaluation together used 6,063.34 allocated device-seconds; separate engineering probes accounted for another 455.86 device-seconds. The evaluation recorded 5,001 model generations and 5,247 environment operations including resets. These measurements cover those named activities, not the full historical project cost, exclusive GPU utilization, deployment latency or the budget of a future study.

这只是重述主文已接受的项目，不能暗示包含 P0 原始训练、全部 source 采集和所有先前研究成本。推荐增加便于理解，但不是当前正文的事实错误。正文关于首轮未完成完整解析可更明确，但当前“read bytes for hashes / no final analysis / no universal blinding”已经满足边界要求。

## 依据与范围

直接阅读了被审附录、配套地图/checker/JSON、两次提取收据、先前 REPRODUCIBILITY_AND_ACCESS_MATRIX.md 与 INDEPENDENT_REVIEW.md、decoder RECORD.md 和 source96 CUSTODY_REVIEW.md；结合本线程已完成方法/历史参与审阅。原统计源码及实际 extractor 的字节绑定刚在 `2026-10-30T014730Z__CODEX__si-statistical-interpretation/` 静态核对。未独立重算新归档清单、模型树或私有逐任务数据，未验证新远端状态。报告目录时间仅作命名空间，不将其当原始执行时间证明。

修正配套地图后，需再核对更正版 exact SHA/diff；附录正文接受范围不因省略的新审查自动扩张为完整可复现性通过。
