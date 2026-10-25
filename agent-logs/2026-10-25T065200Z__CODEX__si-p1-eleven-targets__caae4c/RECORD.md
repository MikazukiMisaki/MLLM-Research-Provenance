# SI-P1 RECORD — 固定11状态只读审计封存

任务SI-P1-TARGET-caae4c。唯一自有目录 `/home/lizening/research-notes/agent-logs/2026-10-25T065200Z__CODEX__si-p1-eleven-targets__caae4c`。LOCAL_ONLY_FOR_COORDINATOR_REVIEW；不是独立review PASS或launch clearance。

## 授权、起点与实际范围

任务单SHA `adcb03193e40baf839e14f9d521e3f7a309c28ce901d6a4dcf1d044660ec579b`、固定11case清单SHA `e5039568d8213fa5d879ffb2aec8c44e932fa99bc4de67bd527ebcae67ccb45b`及P0独立审查SHA `c438377f5afb738b3b74c57378ba8c18b9769bb2f99bb25543aa66848d4697b7`均按原件核验。P0最终NOT_READY作为当前基线；provenance57747744922bf7d44d0c30f1bd24cb6624f8216e的远端核验是协调方既有收据，本线程未重新访问网络或发布。

初始只读工具已核对root/branch/HEAD为 `/home/lizening/wt-codex-r18c2` / `agent/codex-r18c2` / `e537f441010077123a307e9d50ea40cf8dad8547`。结束时同样干净。冻结analyzer `85cbb92395e5e2420c2adeb1fa0634653e742910`、executedG3 `2da980f631badc25086d12db60d128ff507d3ae6`均干净；2da保持原detached状态。本线程没有切branch或修改Git索引。

只对固定11状态（10task）读取已消费历史source/branch/replay/运行manifest，纯stdlib生成字段摘要、hash和disposition；读静态P0/map/reward契约及对应Git对象。没有模型、环境、tokenizer、训练、source生成/replay/G2/G3/G4/preflight/项目analyzer/validator/pytest或新policy评估调用，没有科学代码/测试/模型/adapter/prompt/decoding/horizon/schedule/quota/exclusions改动。没有训练JSONL/完整prompt导出，没有中和/重标/修复原件，没有commit/push/sharedINDEX/rootinventory/旧任务目录或其他agent文件写入，没有派agent/互发线程消息，也未读取另一agent未完成资料。

## 结论与全部case去向

DATA_FEASIBILITY=NOT_READY，训练合格N未建立，learning gain未证明。9行/8task INPUT_TARGET_LINEAGE_SUPPORTED；2行/2task HOLD_EVIDENCE（R4:R2-F01恢复won缺项；R19 K1恢复及CONTINUE两侧won缺项）；REINDEX_REQUIRED=0、EXCLUDE_INVALID=0。11行机械输入/目标/map/replay及原记录done/reward均匹配，但不升级为训练验收。身份另有10 PARTIAL/1 PINNED，缺resolved weights/tokenizer不伪作机械FAIL。

11个公共投影均不同，本固定集无exact同输入多目标组。R8-F22/F23是同task双prefix且suffix公共行为摘要相同；不能多计独立任务或仅据语义相同断言physical alias。所有suffix与adapter-off第一recovery目标分开，R19只使用K1的第一action。

只用这11个positive构造同池success-only与增益筛选会选同组；因此B_pool仍未就绪。本轮没有额外neutral逐案清洗、pool构建、新source或预算/N设定。Luna身份与预算工作作为依赖列出，未自行获取或指派。

## 来源、输入及代码证据

`eleven_target_audit.json`保留全部11case的原分支行SHA/逐字段来源/投影摘要/已有replay/原始目标ID与紧凑command/selection/execution/terminal/model/tokens独立轴；大小193023 bytes，小于1MB。raw source/branch/weights/adapter/cache/dataset树均未复制；schema探测只存摘要。

35个已读输入的before/after SHA全部一致，交付前再读核对见`final_input_hash_check.json`；`INPUT_HASHES.sha256`列其绝对path与hash。Git对象读取不是普通文件binding，另由`historical_contract_read.receipts.json`记录12个真实git show argv/returncode/stdout SHA；`historical_contracts.json`绑定四个原运行codeSHA、方法AST和冻结85，12/12方法匹配。没有运行这些方法。

repo wrapper只是float底层reward并保留info，不将won替换为reward；当前installed ALFWorld静态源码请求won，不证明其历史字节或填补缺失won。HOLD是新学习证据需求，不裁定旧结果错、不改变旧success/review/clearance。

原source actor公共文本与静态P0规则11/11相同，只有字段/文本hash，没有新chat template或tokenizer验证。H4只含此前action与≤d已知result，当前source动作后metadata.environment/facts/won不进入输入。teacher subgoal/card与未来suffix/终局label不移植P0。tokens仅引用历史推理计数，prospective训练tokens仍null。

## 实际命令与返回码

`commands.log`由receipt_runner追加真实subprocess.returncode，下面在finalization开始时含15项；finalization自己的exit收据随后由wrapper追加。核心最终审计及文档生成均exit0；不写测试PASS，因为没有pytest或科学测试。

| 操作 | 实际returncode | raw日志/收据 |
|---|---:|---|
| `fixed_case_probe` | 1 | `fixed_case_probe.log` + `.receipt.json` |
| `fixed_case_probe_empty_suffix` | 0 | `fixed_case_probe_empty_suffix.log` + `.receipt.json` |
| `replay_event_probe` | 0 | `replay_event_probe.log` + `.receipt.json` |
| `eleven_target_audit_draft` | 0 | `eleven_target_audit_draft.log` + `.receipt.json` |
| `historical_static_contracts` | 0 | `historical_static_contracts.log` + `.receipt.json` |
| `eleven_target_audit_final` | 0 | `eleven_target_audit_final.log` + `.receipt.json` |
| `final_evidence_summary` | 0 | `final_evidence_summary.log` + `.receipt.json` |
| `eleven_target_audit_complete` | 0 | `eleven_target_audit_complete.log` + `.receipt.json` |
| `audit_documents` | 0 | `audit_documents.log` + `.receipt.json` |
| `root_final_status` | 0 | `root_final_status.log` + `.receipt.json` |
| `root_final_head` | 0 | `root_final_head.log` + `.receipt.json` |
| `frozen85_final_status` | 0 | `frozen85_final_status.log` + `.receipt.json` |
| `frozen85_final_head` | 0 | `frozen85_final_head.log` + `.receipt.json` |
| `executed2da_final_status` | 0 | `executed2da_final_status.log` + `.receipt.json` |
| `executed2da_final_head` | 0 | `executed2da_final_head.log` + `.receipt.json` |

首次schema probe有exit1/IndexError：自有探测脚本把R10 R8-F02的合法空suffix当成有末步。修正探测为读取recovery直接终局后完成；原输入从未改动，失败日志保留。这不是科学失败或缺失suffix目标。两个辅助静态发现命令各exit2（推测文件路径不存在），一个R4构造正则检索exit1（无匹配）；均为桌面exec真实结果，不伪记0，随后使用实际文件/记录。未因发现命令失败跳过case；11个case均有去向。核心历史对象实际exit见独立receipt。

## 成本、时限与交接

R19累计仍5142generations/7949含reset环境operations，已含旧177/342；不是全项目SFT训练总成本。本轮科学增量0，无预算/操作重跑。开始约06:54UTC，本记录于2026-10-25T07:23:43.351995+00:00准备，在最长60分钟首轮内提前完成；不为用完45/60分钟扩查。45分钟进度点未到即交付。

交付 `ELEVEN_TARGET_AUDIT.md`、`eleven_target_audit.json`、`PUBLIC_INPUT_CONTRACT.md`、输入/输出hash清单、本RECORD、commands和真实receipts、纯stdlib脚本。`FROZEN_HANDOFF.json`列主要文件绝对path/SHA；最后seal在所有wrapper追加完毕后生成`FILE_HASHES.sha256`，不自哈希且不包含随后产生的`SEAL_CHECK.json`。seal是本地文件字节核对，不是项目validator或独立科研验收。

封存后保持原字节；若协调方要求修正，仅新addendum。协调方统一发布，本线程等待独立审阅/具体后续范围，不自行扩大case、构建训练pool或启动科学执行。
