# SI-P2 RECORD — 同池成功对照与数据充分性独立审查

协调方 Sol Designer / Independent Reviewer。任务 SI-P2-b04b8b。用户明确授权继续核验B_pool/C，共同质量、任务去重与数据充分性；仍不启动新实验。状态 **ACCEPT_WITH_CORRECTIONS_AND_SCOPE_LIMITS**；集合可分性支持；**当前历史池正式学习验证NO_GO、TRAINING_DATA_READY=NOT_READY、学习收益NOT_PROVEN**。这是研究投入决定，不是“十个例子不可能学习”的定理。

## 起止与精确状态

起点guard为2026-10-25 07:53:07 UTC左右，新目录时间07:56:10 UTC；实际派发和ACK在dispatch_receipts.json/agent_acknowledgments.json。本记录封存准备时间2026-10-25 08:30:24 UTC；最终发布完成UTC和commit见忽略的post-push-receipt.json。

Scientific repository MikazukiMisaki/Alfworld-Self-Improvement-Project：
- /home/lizening/wt-codex-r18c2，agent/codex-r18c2，起止e537f441010077123a307e9d50ea40cf8dad8547，干净；最先依次运行pwd/toplevel/branch/status/HEAD，根与分支符合用户要求。
- analyzer worktree /home/lizening/wt-r19-g4-consumer-contract-repair，codex/r19-g4-consumer-contract-repair，起止85cbb92395e5e2420c2adeb1fa0634653e742910，干净；live remote branch仍完全相同。
- executed G3 worktree /home/lizening/wt-r19-recovery-duration-v1，仍detached2da980f631badc25086d12db60d128ff507d3ae6，干净；对应source-contract-review-fixes远端仍2da980f。
- authoritative /home/lizening/Alfworld-Self-Improvement-Project只读原raw，未开发或变更其Git状态。
- provenance /home/lizening/research-notes main，基点34109ab3f950d321a80b6e70c5905a95c55a4034；起点及发布前ls-remote一致。本轮不stage其他历史untracked fixtures。

没有科学源码、测试、模型、adapter、prompt、decoding、horizon、schedule、quota、exclusions或原始证据修改。END_STATE_BEFORE_PUBLICATION.json和remote_refs_before_publication.json保存真实只读Git工具结果。

## 实际分工与范围

实际向Sol Research线程01a165de-c75e-7120-abc9-fa74cde1f17f、Luna线程01a09fcb-ab5f-7b83-9acf-91026145b764派发；两者host sdxsrv03。未新建agent，不虚称派发。新任务单、共同规则和171行manifest在派发前固定，SHA绑定在dispatch_receipts；manifest排除outcome字段，实际历史结果不是人类盲法。hash anchor/质量/去重规则未为positive重选。

Sol做完整source/公共输入/target/replay/终局追溯；Luna应做独立身份/标签及过滤前anchor和成本；协调方另写独立stdlib原件审计并决定最终mask。两位各写自己的新目录、不发布；协调方统一封存/上传。peer_completion_metadata.json记录真实完成状态、原用户可见结果和命令exit metadata；两线程在最终审查时均idle。

固定parent仅R4 24、R10_OSR48、R16_OSR60、R19 first-K1 39，合计171行/169不同canonical task。必要原source/CONTINUE/replay和原G3账本只读；不扩K2–5/PAR/cards，不把suffix转成teacher样本，不加载tokenizer或导出完整训练prompt/训练JSONL。

## 独立核验与明确决定

- 协调方independent_pool_audit.py不调用作者或项目代码，重读171行、source字段与原存P0公共文本、H4/full map、raw ID/parser/实际执行/原replay及冻结标签。Q_hist164通过、7排除；物理去重不删，task anchor删2，exact input-target不再删。最终162task，B95/C10/neutral85。
- 与Sol冻结表逐行匹配171行的8类字段：质量、公共projection、target ID、command、raw-output hash、anchor、labels、pin口径。B/C/neutral完整ID集合在两口径都相同，不只比总数。
- Sol95项输入after/before/当前SHA重新核对相同；协调方已读原件也before/after同。14份raw另与P1已封存binding相同。作者55项+Luna冻结清单逐项重hash；后增addenda单独绑定。没有用作者自己的PASS代替独立检查。
- 与Luna逐行匹配171行身份、family/d/标签/anchor；过滤前169个最小key选择也独立核对。169task均在既有2612 known-use并集，和已登记expert_train/expert_offline_validation/online_development task集合直接交集为0；不据此证明未训练过相似prompt或从未被看过。
- 最终C只有10task：light6/picktwo2/heat1/pickplace1，clean/cool为0；5个第一动作是go to desk 1，另5种命令各1。不同命令仅作覆盖描述，不把相同命令误称重复input-target。
- 9个C历史版本PARTIAL、1个R19精确绑定。Q_pin单独按原runtime/loaded角色绑定保留36task，B29/C1/neutral28。原runtime SHA及两个loaded commit/snapshot/tokenizer摘要均只读核对，未加载任何模型。
- 含C的来源×家族stratum均有neutral目标的组合容量，但这不是已选10对10训练集/等token预算；B不能按CONTINUE过滤以强行排除C。没有推理tokens冒充训练tokens或重放C假装新数据。

研究决定：B/C结构可分已闭合，当前池不足以据此安排以广泛成功率提升/筛选机制为目标的正式学习验证。保留10个第一动作及85neutral作审计/论文材料；当前历史池审计结案，不再换anchor/扩K/重标/无上限oversample凑positive。若继续self-improvement方法线，下一步应另设计受控新经验的数据协议并先审查成本/停止规则，而非直接训练这十条；本轮未派发新采集/实验任务。

## 两项解释更正与真实失败

Sol初稿把cap=true一律当截断，误排R19 random-control-47bcdcad9c56a38ac146。原Stage1 complete=true/status=valid、末token151645，冻结生成器容许EOS在cap处，parser只因complete=false判truncated。独立原始event及两处executed2da/85 AST/Git对象对照支持，真实git show返回0；未运行parser。Sol保留draft_v1后纠正V2，该neutral归回但C不增加；队列收到协调方解释后又只新增addendum，旧55项文件未变。

Luna超出指定身份任务额外做的局部branch-locator mask报81PASS/90HOLD，因未接入另存source/replay，不能作最终Q_hist或底层数据缺陷。Luna保留原字节并追加CAP_ROLE_SCOPE_CLARIFICATION_ADDENDUM；最终mask来自完整原件核验后接入其独立171行身份表。只接受其身份/label/preQ证据；不声称三份不同scope的原报告一开始就一致。此轮没有P0/P1旧ROOT写入范围事件。

原99 raw success字段包含R19 ineligible无teacher动作的条目，旧粗算97采用eligible29不同分母；原分支success标签不改。7个无合法执行teacher动作条目中有3个raw success=1，也不能作为该teacher的训练目标。这不是新G3失败、成功重标或G4重算。notes/HISTORICAL_CORRECTIONS.md追加上述解释，原稿和失败/初稿收据保留。

Sol辅助只读工具曾rg exit2/临时打印SyntaxError exit1，原receipt保留；正式6次stdlib审计真实exit0。协调方independent_pool_audit与verify_phase2_deliveries实际subprocess.returncode均0。Luna原执行收据与桌面工具metadata保存，不以自写统计值充当科学runner退出状态。没有运行科学pytest/validator，故没有新科学测试PASS/FAIL主张。

## 成本与边界

本轮模型、ALFWorld、tokenizer、训练、source/policy replay、G2/G3/G4、preflight、项目analyzer/validator/pytest和新heldout policy评价全部0。没有新科学output/run identity/gate/argv，也没切换科学branch。

R19累计仍5142 generations/7949环境操作（7603非reset+346reset），已含177/342；external incomplete operations=0是前期真实审计的carry-forward，不是本轮重跑validator。旧failed source unit仍保持原incomplete证据，不重标/重跑。

历史SFT单列2354 updates、27406.28269892931秒wall time、23860000 input_tokens_seen；GPU device-time/padding语义UNKNOWN。历史R4/R10/R16独立采集与配对验证成本本轮未完整重建，不能写0或把R19总成本全分摊给十个target；原G3本来是恢复时长实验，不能冒充新学习方法的采集效率实验。未来150E/153E三臂公式不是预算拨付，E仍未选。

## 输出与发布

主交付INDEPENDENT_REVIEW_AND_DECISION.md、phase2_independent_review.json、ADEQUACY_CRITERIA.md；原独立审计与逐case交叉比对、95输入/原始日志/真实receipts、两位冻结交付及scope/cap addenda全部保留。只有本轮三个新目录、自己的INDEX行、append-only更正与root hash inventory进入窄提交。超过1MB的两份Sol逐案metadata检查其仅含既有locator/hash/短target及布尔证据，1–10MB范围内保留审查价值；不导入raw数据集/模型权重/adapter/cache。

按provenance协议扫描目标凭据、刷新清单、精确stage集合核对、commit/push且不force，逐文件比较live-remote同commit的Git对象bytes。最终commit、实际推送/远端核验结果放在忽略的post-push-receipt.json并回报用户；正文不伪造包含自身的commit。

发布准备的严格git diff --cached --check实际exit2，仅为已封存Sol parent_inspection.log第15/33行原始stdout尾部空格；没有代码/数据错误。第一次prepare_publication.py因此真实exit1，停在窄stage后、commit前。publication_whitespace_exception.json保存实际完整诊断/returncode；不修改作者日志或其冻结hash，以明确的单raw-log路径例外复核其他所有staged内容，并记录其真实结果。该保留原件的发布处理不改变数据/科学验收，也不把严格检查伪记为0。
