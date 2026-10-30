# R19论文证据附录独立审阅

**决定：ACCEPT_FOR_MERGE_AS_PRIVATE_WORKING_THESIS_APPENDIX_WITH_STATED_LIMITS。** 受审版本可以作为英文论文工作稿的私有证据附录；无阻塞性事实错误。接受范围不是公开发布许可、完整端到端可复现认证或新的科学执行许可。

受审文件：`/home/lizening/research-notes/agent-logs/2026-10-30T022000Z__SOL__r19-methods-appendix__8be2/R19_REPRODUCIBILITY_APPENDIX.md`。

本次实测SHA-256：`16f37e6b9ef70355b7af77e425c30c7b353ccb2fc3243453d489a5e5f808ae97`，与指定exact版本一致。全篇已只读审阅。

## 复核范围

本次读取被引历史审查、失败审计、成本更正、事件时序脚本和结果；实测附录及下列引用文件的hash；直接读取Git对象的父提交链及85cbb923统计源码。没有运行科学analyzer、原事件时序脚本、项目validator、模型、tokenizer、CUDA、环境或训练，没有修改原件，没有重新下载远端证据。

前一轮已直接核验R19 protocol、branches/events/source轨迹hash、39/36/183结构、11个alias、原始入组冻结event及两个先前报告的oracle案例字段；详细范围保持在本目录 `R19_METHODS_INDEPENDENT_REVIEW.md`，SHA-256 `59397a14dc3a6a5997db1ef920ef3b5131280084a7e5b61553894ae9773545d8`。本轮不重复把这些记录称为新统计复算。

## A. 版本链：通过

直接读取本地Git commit对象确认每个箭头都是父子关系：

`bf31f3da430ffc35bd17fc380e1752adce6d1467` → `51ec074cec6c2c2a7b1ecd64e0da33bc446a7e54` → `da7d348ffd3677d619dd31357e1e1e3cca28c9ec` → `2da980f631badc25086d12db60d128ff507d3ae6` → `85cbb92395e5e2420c2adeb1fa0634653e742910`。

失败审计确实记录bf31f3da的mapping/attribute不匹配、1 generation、1 reset、0 source completion。da7d348审查为FAIL且51ec074没有PASS；2da980f审查区分source-treatment semantics unchanged与scientific execution behavior changed。原G2仅carry-forward，不将新源码说成旧G2的执行来源。附录保留这些区别，准确。

85cbb923独立审查明确只有两个analyzer consumers/四个private helpers及测试改变，统计和运行producer保持原样；真正G3 producer仍是2da980f，G4不是重新生成数据。附录的“接受原始nested-v2/缺失run_started的authenticated evidence，而不补造event”与被引独立审查一致。实现PASS和实际G4执行/算术验收也分开引用，没有把软件测试替代科学运行。

## B. 时序与筛选：通过，范围正确

附录准确写明source outcomes用于分层而非全局盲采样，36-prefix cohort是初次介入后的eligible子集。它补上了V2需要的冻结顺序：初始attempt/eligible集合冻结后，才延长共同路径并比较更长K。

新增 `audit_event_order.py` 的静态审阅结果：读取前后分别验证原events和branches哈希；读取单调sequence；要求唯一queue/enrollment freeze；检查127个source completion均在queue freeze前、39个attempt completion均在enrollment freeze前；两freeze间generation_started必须恰为39 Stage1和39 first Stage2；每个eligible prefix要求一次path-extension completion及五次duration-arm start，前者早于全部后者。保存结果中的8566/9698与这些断言一致，enrollment9698也与本轮之前直接读取的原始event一致。

这足以支持“被检查记录中的时序”。脚本不独立证明事件链签名/完整性、全producer真实性、没有未保存调用或所有人员未看source outcomes。附录明确保留这些限制，因此没有升级为完全盲态/全量验证。

本次没有重新执行时序脚本。其本次实测SHA：

- `audit_event_order.py`：`004a403f65a61714a93a3359e2c5844cbf4dc18b7c14726989df684b8af4d565`
- `EVENT_ORDER_RECOUNT.json`：`68433c9c154552e88c9ecd12454c8378cd2ceb0395a7fef317a6a8b33416ef97`

措辞上的非阻塞建议：B节“A candidate requires…”可改为“A prefix is primary-eligible only if…”，因第一动作已执行/非终止是介入后的eligibility，不是生成candidate前的条件。后句已解释post-intervention条件，当前不会构成实质相反主张。

## C–D. Treatment、alias及成本：通过

本目录上一报告已按2da980f `src/recovery/r19_duration.py` L710–729及L780–905核验：Stage1计一次，Stage2截至该K端点的请求包括无效输出，未来更长K才请求的generation不计入早K；full logical branch增加实际SFT suffix。reset/replay归物理研究支出，不算单次政策逻辑成本。alias共享endpoint/suffix证据仍保留每K自己的计费规则。附录准确区分183标签、180 eligible标签、36个paired分析prefix以及独立物理调用。

4,965/7,607与历史177/342相加得到campaign5,142/7,949的口径，与独立G4验收及更正附录一致。7,273是非reset字段；169个wrapper重复计数被更正而不是删除真实支出。原始旧summary未改，新addendum说明权威口径，版本史没有被抹掉。

非阻塞建议：D节“one use from a prefix”已暗示不计干预前source前缀，可再明说“Full-branch logical cost starts at the intervention prefix and excludes the already incurred source-prefix cost.” 这利于避免将full-branch误解成从episode reset开始的总费用。

## E. 统计与推广边界：通过，建议补一句区间范围

直接静态查看 `85cbb92395e5e2420c2adeb1fa0634653e742910:src/recovery/r19_duration.py`：

- L1628–1629精确two-sided discordant-pair binomial尾概率；零discordance的p=1来自其前置分支。
- L1655的CP默认confidence=.975；L1724–1730对win/loss分别求.975区间，再组合 `[Lwin−Uloss, Uwin−Lloss]` 并clip到[-1,1]。
- L1788–1800只对K2..5对K1四个p值做Holm。
- L1802起CONTINUE比较另建，不暗中纳入上项Holm。

因此附录四primary contrasts及其他descriptive analyses的划分正确，未错误宣称后者得到同样multiplicity保护。附录目前没有宣称四个差值区间同时95%覆盖，所以没有事实错误；为避免与SI-U1的同时区间混淆，建议加入：

> These are per-contrast model-based intervals; they do not provide simultaneous 95% coverage across the four primary contrasts.

不需要重新计算统计来完成该文字澄清。固定富集样本、scene依赖、single-sample K选择、hindsight oracle及7/7支持子集的解释限制均适当保留。

## 引用字节复核

除前轮已核验machine-readable protocol与原始G3/G4外，本次对附录新引用的12个本地文件逐个执行原始字节SHA-256检查，均与附录值匹配：human protocol、predecessor failure_audit、da7d348 REVIEW、2da980f REVIEW与independent_review、genuine execution_manifest副本、launch_clearance、85cbb923 INDEPENDENT_REVIEW与independent_review、independent_G4_acceptance、G3_EXECUTION_SUMMARY、POST_RUN_AUDIT_ADDENDUM。具体路径和值都已列于受审附录，不在此重复内部目录。

这核实当前文件身份和引用位置；不把当前bytes存在等同历史运行加载证明、未来可取得性或远端full-content认证。附录对原历史R18 revision等价未知、lifetime exposure未知、已记录控制条件与实际总体之间的差距没有过度承诺。

## 使用结论

指定exact版本可作为私有工作稿证据附录合并。上述三条文字建议属于增强精确度，不阻止合并；如修改文件，应保留本审阅绑定的旧版本和新的hash。公开稿还需去除内部绝对路径并以可发布的资料编号/访问方式替代，不发布私人task文本或轨迹。本次审查不授权任何新模型、环境、评估、selector或科学运行。
