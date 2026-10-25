# SI-P1 — Luna：任务隔离与预算证据补齐
唯一自有目录：/home/lizening/research-notes/agent-logs/2026-10-25T065200Z__LUNA__si-p1-isolation-budget__caae4c
任务ID：SI-P1-ISOLATION-BUDGET-caae4c；接收线程01a09fcb-ab5f-7b83-9acf-91026145b764。
本任务是用户最新明确授权的SI-P1只读审计/设计：“Sol Research逐案核验11状态学习目标，Luna补齐任务隔离与预算，Sol收敛协议/统计标准并独立审查；先不启动新实验”。已有FullAccess适用于这些常规操作，不再请求Approve。禁止模型/ALFWorld/训练/tokenizer加载、source/replay/G2/G3/G4/preflight/项目analyzer/validator/pytest、新生成或新policy评估、科学代码/测试/模型/adapter/prompt/decoding/horizon/schedule/quota/exclusion修改。允许自有目录纯stdlib解析已存在历史raw/metadata、静态阅读代码，构造审计字段/摘要/hash；不导出可训练JSONL，不修复/重标原件，不调用外部模型。未消费任务只读directory身份/文件存在性，禁止打开其game/traj_data/outcomes。历史已消费raw允许按本任务核验。
开始核验review根/home/lizening/wt-codex-r18c2、branch agent/codex-r18c2、HEAD e537f441010077123a307e9d50ea40cf8dad8547，root/branch不符则停并报告。可只读冻结analyzer85cbb92395e5e2420c2adeb1fa0634653e742910及executedG3source2da980f631badc25086d12db60d128ff507d3ae6、/home/lizening/Alfworld-Self-Improvement-Project的明确原始证据。科学树不写不切branch；原G3/G4/clearance保持不变。R19累计5142generations/7949含reset环境操作（已含旧177/342），本轮科学增量0，不等于全项目SFT训练总成本。
provenance base57747744922bf7d44d0c30f1bd24cb6624f8216e已live核验；先读P0最终独立决定 /home/lizening/research-notes/agent-logs/2026-10-25T054106Z__SOL__self-improvement-phase0__b1c48c/PHASE0_DECISION_AND_NEXT_STEPS.md 与同目录phase0_independent_review.json（SHA256 c438377f5afb738b3b74c57378ba8c18b9769bb2f99bb25543aa66848d4697b7），不能引用P0的过期READY来宣称数据就绪。
唯一case清单 /home/lizening/research-notes/agent-logs/2026-10-25T065200Z__SOL__si-p1-protocol-review__caae4c/FIXED_ELEVEN_CASES.json，SHA256 e5039568d8213fa5d879ffb2aec8c44e932fa99bc4de67bd527ebcae67ccb45b；固定11/10，不加K2、不挑其他成功、不把same-task两prefix当独立任务。清单是审计索引，不是训练资料。
只写分配的自有新目录。不编辑/暂存sharedINDEX/rootinventory、旧目录或另一agent文件，不commit/push/派agent/互发线程消息。协调方统一验收和发布。不要读取另一agent未完成文件；需要对方证据时在返回中列出依赖。只用真实stdout/returncode，命令与input/file hashes留证；缺失标MISSING/UNKNOWN，不补跑、倒填或假造PASS。冻结返回后保持原字节，修正仅新addendum。原始大raw/weights/cache/dataset不复制，优先metadata≤1MB。首轮一轮有界核验、完成即交付；无法闭合原件则逐项HOLD而非无限扩查，45分钟附近报告进度，最长60分钟首轮返回已完成结果/明确缺口。该时限不代替科学判据。
完成后在本线程返回path+SHA与摘要，我会poll；不宣称独立review/launch权限。必须RECORD.md、commands.log、输入输出hash清单、真实subprocess receipts。没有pytest就不写测试PASS。

## 任务隔离
1. 使用已发布P0 inventory/metadata，把专家1074train/126offlineval、online60、已用valid_seen140/valid_unseen60、Sprint与R1/R4/R7/R12/R14/R16–R19已消费canonical身份登记整合。允许读已消费source/cohort索引身份字段，无需重新分析outcome；R12和重用prefix不重复算episode。按canonical task/trial及split保留来源category/path/hash；不同seed不算新任务。
2. 把固定11case（10task）逐项对照上述登记，明确它们是历史开发可学习性候选、不能用作新评价任务；同Book trial两prefix必须同一分区。弥补P0中R4/R16–R18从prefix到canonical task未闭合的具体映射，可引用Sol已发布P0 inventory的已消费metadata，不读取其P1未完成文件。
3. 在六family且game.tw-pddl存在的installed身份集合（只读名字/exists，不打开未来payload）上重算known-use差集，分train/seen/unseen；P0协调方1141/0/74是起点不是保证。列出是否减少、为什么、候选清单hash和全局登记仍未闭合部分。登记之外差集不得宣称clean/heldout，尤其不按255原目录计可执行N。记录exact trial disjoint与相似scene/layout泛化不是同一概念；不生成schedule/argv/gate。
4. 区分“完整盘点全部声明来源”与“证明全历史未曾查看”——后者无法穷举时明确NOT_PROVEN。不要因此停掉可完成的metadata联接，也不把所有差集一律认证干净。

## 预算证据
5. carry-forward真实R19成本证据hash：G3 4965gen/7607ops（7273非reset+334reset）；累计含177/342为5142/7949。优先引用已独立核验原成本raw/hash与正式记录，不再跑项目validator或全ledger统计。旧source不完整的1gen+1reset不归零。既有SFT训练/其他历史阶段费用另列已知/未知，不能混成R19或写0。
6. 给未来纸上方案两本账：实际共享研究physical ledger，与各方法若独立获取资料的必要费用。source、stage1/stage2、CONTINUE、恢复、suffix、reset、prefix replay、失败/未完成、验证、training、offline validation和eval分列。unknown不能填0；旧资料重用可使新增生成0，但历史获取费用和方法验证premium仍须披露。
7. 用静态代码/已有记录给出明确假设下的资源上界公式，供我收敛数值：例如未来3臂E个50-horizon任务的fresh evaluation最多150E generations/153E含reset环境ops（仅当每步1generation/step、无额外controller、每episode1reset；检查终止/invalid等不会增加上界）；若reuse来源/分支，physical调用只计一次且保留logical per-arm成本。训练T/U/有效tokens/实际inputtokens和GPU时间当前不能凭旧prompt长度估确数；提供证据缺口和可预注册上界项，不自行授予预算/选择E或新source数量。
8. 当前P1科学增量仍0；“预算方案”不是额度、旧R19上限不能挪用成新实验授权。

## 交付
TASK_ISOLATION_AND_BUDGET_EVIDENCE.md；task_isolation_audit.json（源集合/来源hash/11case对应/交集/known-use差集/未闭合项）；KNOWN_USE_IDENTITIES.json（只metadata）；budget_evidence.json（actual carry-forward、unknown项、未来formula及假设/代码位置）；BUDGET_TEMPLATE_NOT_EXECUTABLE.md；INPUT_HASHES/FILE_HASHES、RECORD、命令真实receipts。不要声称新实验READY或独立验收PASS。