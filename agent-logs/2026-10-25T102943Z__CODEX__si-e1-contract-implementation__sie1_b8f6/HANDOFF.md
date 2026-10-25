# SI-E1 frozen engineering handoff

**Developer delivery only / ENGINEERING_ONLY / NO_LIVE / NOT_RUNTIME_READY.** 请Sol独立审查精确提交；作者不签发IMPLEMENTATION_REVIEW PASS或launch clearance。当前科学执行许可仍NOT_GRANTED。

- Frozen science commit: `a995d4c3c5f7d31a2cf1fd0afc4bfa4bd72ee3a3`，直接parent为`85cbb92395e5e2420c2adeb1fa0634653e742910`。
- Worktree: `/home/lizening/wt-si-p3-engineering-contracts`；branch/remote ref: `codex/si-p3-engineering-contracts` / `refs/heads/codex/si-p3-engineering-contracts`。
- 仅17个新增文件、3315行；旧tracked文件/方法修改0。提交不含机器路径、凭证或configs/local gate。无PR/merge。
- 已非force push；本地HEAD=origin ref=live ls-remote，干净。[LIVE_REMOTE_EQUALITY.json](/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6/LIVE_REMOTE_EQUALITY.json)含真实argv/returncode/stdout/stderr与时间；85、2da旧远端ref相同。原review/evidence worktrees保持原SHA且干净，见[FROZEN_WORKTREE_STATES.json](/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6/FROZEN_WORKTREE_STATES.json)。

## 本轮待处理队列已合并

1. 读取共同合同、五份project文档、SI-P3权威protocol/review；保持原85/2da和旧R19/adapter/协议/失败原件不动。
2. 协调方DRAFT_SEMANTICS_BLOCKERS和直接差分指出的4项真实mismatch均仅在新增模块修复：teacher使用冻结`two_stage_v2.stage_two_prompt/parse_bare_stage_two_output`；裸A001选中、Action-ID标签拒绝；P0 source/suffix仍使用原`parse_p2_selection`决策，不新增EOS-complete执行门槛；teacher不完整仍拒绝。测试直接调用冻结actor方法（仅替换raw model边界），并通过真实collector source/suffix执行路径验证。
3. STATIC_CONTRACT_RISK_ADJUDICATION的在线run/task/seed/kind/index/start绑定、外来receipt/重复单元拒绝、输入token先reserve、全物理成本及未知failed call预留、原地handoff、真实collator/shift/分母、final18均纳入新增层；未修旧helper。
4. 最后一项reservation收敛要求已纳入：纯离线binder先验证原始metadata固定SHA`6ce8a32a2345b59ecdef9c28c3a341e9c0801b8105f79895f9b2cb9545a4937e`，再比对exact A96 identity/family及caller显式seed metadata。真实metadata正向96、同family A96→D48替换、修改bytes重算header及historical digest override负向均通过，[actual_reservation_binding_check.json](/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6/actual_reservation_binding_check.json)。不读取task正文，不输出真实schedule/launch argv。
5. 已收到协调方关于其独立800/3/77、parser/资源/S探针的预审结果消息；其证据不冒充作者执行或最终验收，本交付不据此再改代码或扩写测试。

## 生产实现与关键调用

- `contract.py`：版本/边界、全部96个slot、五family与balanced d矩阵、严格public projection及原producer dictionary的typed适配。工程JSON绑定最终protocol/review、S身份/hash规则、生成与输入/设备预算、共同Q/一次B/C采纳/固定学习剂量。
- `reservations.py`：真实历史reservation bytes固定hash绑定；generic freeze_plan用于synthetic，historical不能用self-report或caller digest覆盖。
- `collector.py`：完整source P0→引用既有CONTINUE终局→预分配d→逐步exact replay→冻结v2 Stage1/2→teacher一个合法动作→同环境立即P0suffix。40/16/16、H50；actor/teacher返回类型明确、operation由collector统一拥有。所有96计划/无效/不可达/终局保留；未执行teacher YT=null；技术missing不填任务失败。P0原completion行为保留。冻结P0 normalized reset的Task.family=None由canonical task ID验证派生，冲突fail-closed。
- `evidence.py`：fresh append-only/fsync journal、unique run ID、严格在线registry、跨run/kind/start/identity/命令receipt拒绝；预留精确input与完整output cap再调用；reset/replay/action各记一次。失败未知单位保留reserved成本，不retry。GPU预算按allocated devices×monotonic归属时间合同，不能以latency代替。
- `audit.py`：只做本工程软件完整性consumer，独立重建原始prompt/parser/map/action/transition/replay/终局/原source引用及physical cost；全重算hash仍不能掩盖语义tamper。receipt逻辑成本分别导出CONTINUE/K1/invalid teacher attempt，不新记physical debit；没有确认性统计reporter。
- `data.py`：全池共同Q/完整2048序列fit/去重先于B/C采纳。B包括C，按固定hash单次C24及family×实际ID+EOS长度matched B24；selected neutral7拒绝/8允许，不重抽。S固定原专家dataset及完整895个非light expert_train身份hash；选定task无合格row即NOT_READY不换task。144 paired slots、每epoch同置换与micro2/accum8边界、实际shift后token数、new/all累计prompt ratio均审计；EOS=PAD仍监督，prompt/pad不入loss。
- `continuation.py`：唯一loader为`PeftModel.from_pretrained(base, existing_adapter, is_trainable=True)`；LoRA-only/fresh optimizer/固定seed42/final18/拒绝独立shuffle/drop-last/best/额外epoch与输出覆盖。当前只允许<=1M参数CPU toy，真实8B/P0/live入口关闭；无实际训练driver。toy loss按整个update真实监督token分母归一化，不把微批mean等权累加。

完整方法/文件SHA、AST定义与行号：[NEW_METHODS_AND_FILES.json](/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6/NEW_METHODS_AND_FILES.json)（198个新增class/def节点，含测试/嵌套）；原有方法delta为空。完整patch/stat/name-status：[full_delta.patch](/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6/full_delta.patch)、[full_delta.stat](/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6/full_delta.stat)、[full_delta.name_status](/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6/full_delta.name_status)。原输入及冻结源码绑定：[INPUT_AND_FROZEN_SOURCE_BINDINGS.json](/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6/INPUT_AND_FROZEN_SOURCE_BINDINGS.json)。可读代码文档：[/home/lizening/wt-si-p3-engineering-contracts/docs/si_p3_engineering_v1.md](/home/lizening/wt-si-p3-engineering-contracts/docs/si_p3_engineering_v1.md)。

## 本人实际软件验证

| 项目 | 结果 | 真实原始证据 |
|---|---|---|
| Fresh base85 full suite |703通过/3失败/77错误，exit1|receipts/baseline85_full.*、baseline85_full.xml|
| Frozen candidate focused（246旧R19+97新） |**343通过，exit0**|receipts/frozen_focused_v2.*、frozen_focused_v2.xml|
| Frozen candidate full |**800通过/3失败/77错误，exit1**|receipts/frozen_full.*、frozen_full.xml|
| 80历史失败/错误ID |与fresh85逐ID完全相同；无NEW IDs|HISTORICAL_FAILURE_ERROR_IDS.json|
| 编译/差异 |13个新Python模块/测试编译成功；diff --cached --check exit0|receipts/compile_new_sources.*、receipts/staged_diff_check.*|
| 精确SHA新进程完整合成集成 |96slots；Q96/C24/neutral72，固定B含18neutral；144microbatches/18update审计；new/all prompt ratio1|synthetic_integration_frozen/及receipts/synthetic_integration_frozen.*|
| 真实缓存tokenizer纯文本 |4文件hash与chat template绑定一致；10编码/5chat render/4decode；4个Axxx+EOS均5个实际监督tokens，EOS=PAD保留；长map拒绝|cached_tokenizer_audit.json、receipts/cached_tokenizer_text_audit.*|
| 真实reservation纯metadata |A96正向及同family D48/改bytes/selfhash/override负向；原bytes前后hash不变|actual_reservation_binding_check.json、receipts/actual_reservation_binding.*|
| CPU tiny PEFT |每次B/C同adapter权重续载，各final18，frozen base不变，真实保存/重载相等；optimizer新建|cpu_toy_saved_evidence/、原/tmp软件树路径见FINAL_DEVELOPER_CHECKS.json|

统一汇总[FINAL_DEVELOPER_CHECKS.json](/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6/FINAL_DEVELOPER_CHECKS.json)。所有raw stdout/stderr/returncode均真实subprocess capture。343/800是开发软件检查，不是独立review PASS。PEFT警告（toy无原base config路径）保留；没有skip/xfail、没有新增expected regression ID。

合成集成中的2527 raw fake generations/3823 fake reset-inclusive operations只是fixture调用，不计入科研物理开销。source、replay、parser、journal、registry、Q、抽样、collator、controller均未mock；仅原始model与env I/O边界synthetic。CPU软件测试累计6次完成test invocation×两臂=12个toy continuation，共216个真实toy optimizer updates、1728个forward及1728个backward微批；不称actual P0/8B训练。最终focused/full两轮toy保存原件字节副本在own目录，其余历史toy raw trees按receipt保留。没有使用这些toy loss选择recipe或效果。

## 未证与阻断（不得解释为runtime ready）

1. **NOT VERIFIED**：真实8B/P0神经对象未构造；adapter on/off实际硬件/模型状态与P0权重续训未验证。Producer ports验证receipt合同，未来真实driver仍需独立认证模型、active adapter、模块/input origins。CPU tiny loaded adapter不是actual P0证明。
2. **NOT IMPLEMENTED/NOT AUTHORIZED**：没有real model/env/live/train driver、真实科学gate或launch manifest，没有确认性统计reporter。registry是per-run软件约束，不是跨run科学执行许可。
3. **NOT VERIFIED**：真实新96 pool/yield/质量/采纳未产生，实际新数据配平、完整S120训练使用与GPU完成可行性未由本作者执行。缓存tokenizer synthetic字符串不替代真实新pool审计。协调方独立历史S审计属于其独立证据，不计入本人的执行。
4. **NOT VERIFIED**：真实终态是否报告完整map；empty terminal map已测，None仍严格拒绝。未做全局missing-map/Action-ID掩盖。
5. **NOT VERIFIED**：4 device-hours/16Minput投资帽能否完成；CPU软件allocated-device计数0不代表实测GPU预算。fp32/non-fused CPU toy例外不宣称BF16/fused/checkpointing真实路径ready。
6. JSON schema为可核查versioned形状；pinned环境无额外jsonschema包，未安装依赖或声称外部metaschema验证。生产强语义validator/负向检查实际执行。
7. 本人未做确认性统计、policy replay、项目actual-data analyzer/validator、G2/G3/G4/preflight、实际模型/ALFWorld、训练/采集/eval、selector/调参。没有效能/因果/学习改善结论。

## 授权与封存

等待Sol对精确SHA独立审查；后续真实driver/runtime/resource/实际P0工程闭合和任何科学采集、训练、评估仍需相应独立审查与新的明确用户科学授权。当前没有自动384、没有因guard通过自动训练/eval。

R19历史**5142 generations/7949含reset env operations**原样保留，包含177/342；本轮真实科学新增0，old evidence/review/clearance未变。provenance仅本own目录LOCAL_ONLY创建，未commit/push/sharedINDEX或rootinventory；由协调方统一发布。`PUBLICATION_MANIFEST.json`提供选定紧凑文件/原字节hash，raw fixture trees留local，`FILE_HASHES.sha256`绑定整个own交付（不含自身）。源branch已按用户授权单独发布，不代表provenance发布或科学许可。
