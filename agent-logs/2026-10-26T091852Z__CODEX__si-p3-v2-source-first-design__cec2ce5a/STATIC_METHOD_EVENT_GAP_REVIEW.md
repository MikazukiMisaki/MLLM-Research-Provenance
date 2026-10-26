# v2 静态方法/事件影响分析（未实现、未测试）

**STATIC_DESIGN_ONLY / NO_IMPLEMENTATION_RELEASE。** 基准是已冻结工程SHA844cc4b78df1f83e29391ffd5ab861a2d0c0a3fd。以下均是静态代码证据和未来最小审查范围；没有修改对应方法、调用函数、跑测试或创建实际run。`STATIC_METHOD_INDEX.json`仅解析AST文本，给出精确行号、method AST hash和文件SHA；不导入项目代码。

## 1. 已确认的接口差距

| 当前代码证据（均在src/self_improvement/si_p3，特别标注除外） | CONFIRMED现状 | v2未来最小影响；不是本轮授权 |
|---|---|---|
| contract.py:VERSION/DESIGN_SHA256/CONTRACT_FILE_SHA256；Slot、cut_matrix、freeze_plan、plan_hash | v1四位置矩阵、总d=1200及plan order/cutoff被强绑定 | 新版本须绑定全d5、source-first语义及新hash；原v1继续严格拒绝不符payload，不能改header伪装兼容 |
| reservations.py:bind_reservations | 精确认证原metadata SHA及A96 task/family集合，再调用v1 freeze_plan | 保留完全相同A96绑定；新v2计划构建需单独版本审查。quota一致不代替identity一致；本轮不生成seed/计划文件 |
| collector.py:Collector.__init__；contract.software_only；ProducerAdapter.__init__ | 仅synthetic evidence被允许，live默认拒绝 | 不能删除门禁把软件PASS变科学许可；未来只作被独立审查的新版本薄桥接及专用授权，旧入口保持原边界 |
| collector.py:Collector._collect、run | 每slot完整source后立即replay/teacher/suffix，逐slot关闭；并非source-first | 最少拆分source阶段、不可构造审查、branch阶段和最终slot去向。复用既有_generate/_step/_rollout的语义与原引用，不新增baseline rollout |
| collector.py:_rollout、_collect | source闭合后从source step取prefix；正常actor invalid可在L=d停下；闭合返回success=done&&reward>0 | 必须独立保存第5动作after的checkpoint，并对parser-stop、terminal、空map、缺失作不同去向；不凭L>d决定新E |
| collector.py:_partial、run异常路径 | 单slot异常摘要可将顶层Y0置None而将已完成source留partial | source-first必须以独立source seal永久保留已认证Y0；branch技术失败不能抹掉已完成的source事实。此为新编排接口要求，不重新裁定旧run |
| collector.py:_new_environment、EnvironmentAdapter.reset；env/alfworld.py:42/171；runtime_environment.py:ReadIsolatedEnvironment._get_environment | reset调用会seed全局Python/numpy/torch；新TextWorld pool另由environment.seed(pool_seed)初始化 | source/replay用task-local相同绑定及各自fresh单game实例、一次初始reset；pool RNG/counter证据与receipt index分开。不能依赖先前全局reset次数或仅传reset(seed) |
| collector.py:_step；UnitRegistry._data_contract | ID/map/命令/原generation或source step引用在线强绑定 | 两阶段之间只用原event引用，不复制或重新finish source单位；仍验证逐步before/after和map顺序，不放宽索引或source_step绑定 |
| evidence.py:Journal、validate_journal、UnitRegistry | v1 header/evidence_class/contract hash；append flush/fsync；unit identity含slot/task/phase/index/operation | 新阶段元事件及phase门槛需v2 schema，单位先start再external/complete；不得改写v1 journal或无条件接受新kind |
| audit.py:IntegrityAudit.receipt/slot/validate | 全局previous_sequence随着逐slot source→branch遍历前进；完整软件池要求96闭合和v1事件白名单 | source-first不能直接沿原逐slot顺序审核，否则先读slot1 branch再读slot2 source会逆序。未来按真实journal时间序核物理账，再用严格slot依赖图核source→seal→branch/引用；不是去掉顺序检查 |
| evidence.py:Caps.__post_init__、Budget.reserve/complete/check_time | 8496/9792/138240上限且只可收紧；累计input16M/per-call8192；clock全局 | v2需要独立版本的9216/9792/149760保守帽，不能修改旧Caps上限或把阶段clock归零；input/4h继续更紧，尚无完成性实测 |
| data.py:build_pool、adopt_once | build_pool先调v1 audit_run；未PAIRED则Q=false；共同去重后B包含C、单次按C family/长度匹配，neutral≥8 | v2消费者必须识别source-only结构STOP及partial与完整配对不同状态；source-only不得调用adoption制造数据。完整v2池仍执行同等Q/既定B/C规则，不能让旧auditor总pass |
| runtime_backend.py:LocalInference.prepare/generate；collector.py:ProducerAdapter/RawProducer | 前者接phase+PreparedTensors（含mask），后者接prompt/cap/mode；不是可直接插接接口 | 未来显式typed适配须携带slot/phase/unit、完整rendered IDs/mask和真实PEFT状态证明；operation由编排单独拥有，不重演dict/object或operation覆盖问题 |
| runtime_gate.py:PHASES/MAXIMA/validate_documents；runtime_ledger.py:reserve；runtime_diagnostic.py:run_diagnostic | SI-E2只准固定source/Stage1/Stage2/suffix各一次，工程4调用/88输出；原诊断Stage2用预声明synthetic subgoal，生成不驱动环境 | 这些工程入口/授权不能拿来收96或作真实teacher。新采集需自己范围的桥接/账本/授权审查；不能扩原MAXIMA、消费旧authorization或把独立诊断当collector已接好 |
| runtime_gate.py:inspect_gpu/validate_gpu_rows；runtime_backend.py:load/verify_cuda_uuid | UUID wire兼容已接受，仍需实际own NVML PID/UID后才加载8B；host/local映射未证明 | 保留strict ownership和原raw证据。可信入口/映射须独立能力变化与新授权；本轮不SSH、不探针、不借该问题扩修底层权限 |

当前可复用的是纯公共projection、冻结parser、单K1原地handoff、类型/receipt和共同Q/采纳原则；不能复用的是“当前科学采集已可执行”这个不存在的结论。未来准确method白名单/版本hash与live权限仍待另立工程任务，不由此表授权。

## 2. 最少事件合同：仅提议名称/语义，无schema或gate文件

现v1主要词汇是run_opened、slot_planned、unit_started、unit_completed/unit_failed、slot_closed、run_closed；现SI-E2另有engineering_opened/external_*、resource、adapter_state、driver_failed。二者不能串接后声称完成一个真实科学run。

以下是v2未来需明确的阶段记录概念，名称只是文档占位，未实现、未发出：

| 记录概念 | 必须绑定的内容与先后关系 |
|---|---|
| 计划冻结/run header | v2协议/metadata/全部原件/身份及范围hash；96个task和阶段顺序在任何external start前固定；不含本轮生成的实际映射 |
| anchor checkpoint | 第5动作真实after ref、公共snapshot/H4/map/projection hash、可用/不适用原因；在后续source generation/结局前落盘。未到达也有去向 |
| source_closed | 单task正常终止谓词、完整source refs/source hash/Y0、anchor去向；source单位只完成一次，不等于整个slot已配对 |
| source_phase_sealed | 全96 source及每个snapshot去向可认证、无缺失/open source单位；精确source顺序与汇总hash，不创建新的generation/reset |
| source_futility_reviewed | 引用seal和E/F/S的每家族/总数量；只支持必要上界结论，unknown不能计0；在所有branch reset/teacher前。不是runtime/science许可 |
| branch_closed/未测去向 | 每个E一次原replay/Stage1/2/合法teacher/suffix原件、YT或NA、stop原因；对应source hash必须指向seal内同task，不替换source |
| 最终slot/run关闭 | 所有96去向、真实completed和unknown/open预留、phase完成程度及费用；source-only结构NO_GO、技术/预算停止及完整配方结果不能合并成COMPLETE96_PAIRED |

阶段元事件不收费为模型或环境操作，但承载它们的真实GPU占用时间仍在4h内。实际env construct/close可另列资源/清理receipt；不把它们重复算成reset/step，也不掩盖这段allocated时间。新auditor必须验证新增kind/字段/前后关系；不能全局放宽白名单。

## 3. Future负向验收矩阵（本轮全部NOT_RUN）

1. 同family用D48/E600替换A96、带未来标签的计划字段、错cutoff/错版本hash：在runtime构造前拒绝，v1/v2互不冒充。
2. 第5动作terminal/truncated，显式空map，5动作前合法停止：位置不可用；与“5动作后S5有效、第6 generation解析失败”的E内情况分开。不要把生成数当动作数。
3. 缺snapshot/map/step receipt、source技术中断或预算中断：不能伪造完整source96或结构性NO_GO；保留NA及open units。
4. 任何branch reset/replay/teacher unit在完整source seal与已认证必要数量审查前开始：拒绝；source仅95完整也不能提前以已知失败数量结束。
5. 总E达到72但某family不足，F/S总量达到24但某family不足：分别识别；unknown出现不能压0后判结构失败。上界通过不得宣称完整Q或学习GO。
6. source正常parser fail-closed与技术异常分开；缺raw won不抹掉合法done&&reward>0标签；后续branch异常不得改source seal中的Y0或原完成event。
7. source/replay fresh实例、pool seed或初始化counter漂移、全局reset顺序依赖、checkpoint public state/map不同：拒绝，不seed-search或额外reset。另一slot提前停止不应改此task的初态绑定。
8. Action-ID错配、map顺序改变、错误source_step/generation_event、同一物理source再finish/debit、孤儿或跨run引用：拒绝；CONTINUE只作原refs。
9. 真实时间顺序为全部source后branch的非空fixture必须能审核；跨phase source seal伪造、时间逆序、漏start/complete、unknown开销即使重算hash chain也拒绝。不能通过取消previous_sequence约束完成适配。
10. source或suffix合法bare ID但EOS incomplete仍保持原P0选择；teacher incomplete不执行；complete=true/cap=true的EOS正常接受。Stage1无效仍只固定一次Stage2，YT=NA不填0。
11. 合法teacher直接terminal时零suffix调用；suffix与teacher同env且不reset。terminal map缺失不得伪造empty以通过，不扩K或额外复放。
12. 预留8192/input16M/9216与149760/4h的边界及source→branch累计：超限前停止，阶段不清零timer或预算；失败调用预留不能释放成已知零。source-only数据未完整不能转进配方。
13. B_pool包含C，按原一次hash/family×实际loss长度抽样；neutral<8、projection<20或prompt比>1.05即该draw NO_GO，不redraw、不排C或改hash。共同Q/去重不按rescue保留而改规则。
14. teacher/source终局、诊断、source完整suffix、隐藏控制字段混入学生/teacher因果公共输入：拒绝；只允许S5冻结P0 view与合法ID+EOS。
15. 捕获host PID与local PID未认证映射、外来UID/进程、旧consumed授权、已有输出重用：继续fail-closed。不得因为UUID匹配、仅一个GPU进程或软件PASS而接受。

未来正向软件验收最少要有非空、多family、全96去向的两阶段production-path fixture：真实编排/parser/journal/registry/独立完整性audit/Q/一次B/C链路，只替换模型/环境外部边界；还须独立source-only结构STOP、正常不可达、预定invalid和技术/budget partial路径。另跑的actual-data integrity/运行或原轨迹测量各自需新具体授权；本轮没有调用或预备可执行配置。

## 4. 风险分类与决定

CONFIRMED：逐slot编排、v1顺序审计、版本/cap、4调用独立工程probe及seed/reset界面的以上差距均有代码证据。

SUSPECTED：若未经版本化拆分就套source-first，容易产生false futility、source标签覆盖或二次debit；这里只报告风险，不声称这些新流程已经实际运行失败。

NOT_VERIFIED：真实GPU身份/8B装载/资源完成性、source96可达及C产率、运行中terminal map行为、严格source-first live driver与未来B/C token/collator实际新经验覆盖和学习效果。已认证软件953/3/77是旧证据引用，本轮没有测试。

默认NO_GO保持不变。此表只是将未来最小工程任务变得可审查，不是实现任务单、clearance或额外架构提案。
