# SI-P1 — Sol Research：固定11状态逐案学习目标核验
唯一自有目录：/home/lizening/research-notes/agent-logs/2026-10-25T065200Z__CODEX__si-p1-eleven-targets__caae4c
任务ID：SI-P1-TARGET-caae4c；接收线程01a165de-c75e-7120-abc9-fa74cde1f17f。
本任务是用户最新明确授权的SI-P1只读审计/设计：“Sol Research逐案核验11状态学习目标，Luna补齐任务隔离与预算，Sol收敛协议/统计标准并独立审查；先不启动新实验”。已有FullAccess适用于这些常规操作，不再请求Approve。禁止模型/ALFWorld/训练/tokenizer加载、source/replay/G2/G3/G4/preflight/项目analyzer/validator/pytest、新生成或新policy评估、科学代码/测试/模型/adapter/prompt/decoding/horizon/schedule/quota/exclusion修改。允许自有目录纯stdlib解析已存在历史raw/metadata、静态阅读代码，构造审计字段/摘要/hash；不导出可训练JSONL，不修复/重标原件，不调用外部模型。未消费任务只读directory身份/文件存在性，禁止打开其game/traj_data/outcomes。历史已消费raw允许按本任务核验。
开始核验review根/home/lizening/wt-codex-r18c2、branch agent/codex-r18c2、HEAD e537f441010077123a307e9d50ea40cf8dad8547，root/branch不符则停并报告。可只读冻结analyzer85cbb92395e5e2420c2adeb1fa0634653e742910及executedG3source2da980f631badc25086d12db60d128ff507d3ae6、/home/lizening/Alfworld-Self-Improvement-Project的明确原始证据。科学树不写不切branch；原G3/G4/clearance保持不变。R19累计5142generations/7949含reset环境操作（已含旧177/342），本轮科学增量0，不等于全项目SFT训练总成本。
provenance base57747744922bf7d44d0c30f1bd24cb6624f8216e已live核验；先读P0最终独立决定 /home/lizening/research-notes/agent-logs/2026-10-25T054106Z__SOL__self-improvement-phase0__b1c48c/PHASE0_DECISION_AND_NEXT_STEPS.md 与同目录phase0_independent_review.json（SHA256 c438377f5afb738b3b74c57378ba8c18b9769bb2f99bb25543aa66848d4697b7），不能引用P0的过期READY来宣称数据就绪。
唯一case清单 /home/lizening/research-notes/agent-logs/2026-10-25T065200Z__SOL__si-p1-protocol-review__caae4c/FIXED_ELEVEN_CASES.json，SHA256 e5039568d8213fa5d879ffb2aec8c44e932fa99bc4de67bd527ebcae67ccb45b；固定11/10，不加K2、不挑其他成功、不把same-task两prefix当独立任务。清单是审计索引，不是训练资料。
只写分配的自有新目录。不编辑/暂存sharedINDEX/rootinventory、旧目录或另一agent文件，不commit/push/派agent/互发线程消息。协调方统一验收和发布。不要读取另一agent未完成文件；需要对方证据时在返回中列出依赖。只用真实stdout/returncode，命令与input/file hashes留证；缺失标MISSING/UNKNOWN，不补跑、倒填或假造PASS。冻结返回后保持原字节，修正仅新addendum。原始大raw/weights/cache/dataset不复制，优先metadata≤1MB。首轮一轮有界核验、完成即交付；无法闭合原件则逐项HOLD而非无限扩查，45分钟附近报告进度，最长60分钟首轮返回已完成结果/明确缺口。该时限不代替科学判据。
完成后在本线程返回path+SHA与摘要，我会poll；不宣称独立review/launch权限。必须RECORD.md、commands.log、输入输出hash清单、真实subprocess receipts。没有pytest就不写测试PASS。

## 核验内容
对清单全部11case逐项填写，任何排除仍保留一行，不以合格样本恰为0代替未知：
1. 原件source line/hash、canonical task、prefix、decision index/剩余horizon、CONTINUE0/recover1依据；区分done/环境won/成功reward字段，静态核对该旧wrapper reward语义。若缺won，仅写实际可证的结果，不把塑形reward当成功。R19K1只验已执行第一recovery action，不能偷用K2或SFT suffix目标。
2. 找到对应原source完整公共前缀及精确replay记录；恢复前原goal/observation、已发生H4 transition、当时完整且有序admissible map。信息须来自动作之前；原recovery teacher的subgoal/card/后续action/终局标签不能进入P0输入。可以用stdlib按静态P0契约形成public-field摘要/hash、审计每字段来源/时点；不要导出完整可训练prompt/JSONL或加载tokenizer。字段投影hash不是已验证chat template/tokenizer序列，明确范围。
3. 第一recovery模型原始输出、原parser/selection metadata、当时ID→command、实际执行command/transition/hash逐项匹配；不重跑生产parser或项目validator，可按已记录字段和静态定义核对。P0 map与teacher map必须逐项比较；若顺序/ID不同标REINDEX_REQUIRED，禁止自行改目标或跨状态搬Axxx。malformed、unexecuted、缺replay、缺转移等逐项HOLD/EXCLUDE并给原件证据。
4. 分开adapter-off恢复teacher与adapter-on SFT suffix，记录模型名称、当时weights/tokenizer revision有无、adapter身份/代码/运行receipt。历史UNKNOWN保持UNKNOWN；机械目标有效性、历史身份完备性和学习收益是三个轴，不能仅因UNKNOWN伪造机械FAIL或直接称当前actor自采样。
5. 在这11case的P0字段投影上查 exact相同public输入但不同目标command的冲突，及同task两prefix/复用suffix。冲突是多解/歧义线索而非自动坏标签；不修复、不选最优目标。每case记录原已有tokens及缺失，不能把恢复prompt长度当投影后训练tokens。
6. 每case给reasoned disposition：INPUT_TARGET_LINEAGE_SUPPORTED / HOLD_EVIDENCE / REINDEX_REQUIRED / EXCLUDE_INVALID等，另列MODEL_IDENTITY_PINNED/PARTIAL、TERMINAL_CORROBORATION和PUBLIC_PROJECTION范围。这些是数据审计结论，不是独立数据验收/学习增益PASS。汇总rows/tasks/families（任务重复不能计新N）。
7. 给B_pool同候选来源success-only对照的未决条件清单；本轮不扩大到额外neutral样本逐案清洗、不建立训练pool。明确11个正例核验不等于对照池已就绪。

## 交付
ELEVEN_TARGET_AUDIT.md；eleven_target_audit.json（11case逐字段来源与hash、时点、map/target、独立轴/disposition，可附紧凑ID/command但不附训练prompt）；PUBLIC_INPUT_CONTRACT.md（静态源位置/定义/hash及投影边界）；INPUT_HASHES.sha256、FILE_HASHES.sha256、RECORD.md、commands/真实receipts和审计脚本。返回精确合格/待定数，不夸大成训练集就绪。