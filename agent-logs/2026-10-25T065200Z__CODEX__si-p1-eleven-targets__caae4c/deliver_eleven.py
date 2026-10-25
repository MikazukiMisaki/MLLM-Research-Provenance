"""Write SI-P1 audit prose from already generated audit metadata only."""
import collections,datetime,json
from pathlib import Path

def documents(ns):
 own=ns['OWN'];obj=json.loads((own/'eleven_target_audit.json').read_text());history=json.loads((own/'historical_contracts.json').read_text());cases=obj['cases']
 supported=[x for x in cases if x['disposition']=='INPUT_TARGET_LINEAGE_SUPPORTED'];holds=[x for x in cases if x['disposition']=='HOLD_EVIDENCE']
 table=['| 固定case | d / H | 原始目标ID → 实际命令 | 终局won | 身份轴 | disposition |','|---|---:|---|---|---|---|']
 tokens=['| case | 原actor同一公共P0输入 tokens | Stage1 input / generated | Stage2 input / generated | 未来训练tokens |','|---|---:|---:|---:|---|']
 for x in cases:
  t=x['first_recovery_target'];tok=x['recorded_tokens'];s1=tok['first_recovery_stage1'];s2=tok['first_recovery_stage2'];model='PINNED' if x['model_identity']['axis']=='MODEL_IDENTITY_PINNED' else 'PARTIAL'
  table.append(f"| {x['case_id']} | {x['decision_index']} / {x['remaining_horizon']} | `{t['action_id']}` → `{t['mapped_command']}` | {'显式true' if x['terminal_corroboration']['axis'].startswith('EXPLICIT') else 'MISSING'} | {model} | {x['disposition']} |")
  tokens.append(f"| {x['case_id']} | {tok['source_actor_same_public_P0'].get('input_tokens','MISSING')} | {s1['input_tokens']} / {s1['generated_tokens']} | {s2['input_tokens']} / {s2['generated_tokens']} | UNKNOWN |")
 md=r'''# SI-P1 固定11状态学习目标审计

任务 `SI-P1-TARGET-caae4c`。**DATA_FEASIBILITY=NOT_READY；TRAINING_N=NOT_ESTABLISHED；LEARNING_GAIN=NOT_PROVEN。** 这是自有数据审计结论，待协调方独立审阅；不是独立数据验收PASS或科学启动许可。

## 范围与结果

唯一任务单SHA256 `adcb03193e40baf839e14f9d521e3f7a309c28ce901d6a4dcf1d044660ec579b`，固定11-case清单SHA256 `e5039568d8213fa5d879ffb2aec8c44e932fa99bc4de67bd527ebcae67ccb45b`均匹配。开始root `/home/lizening/wt-codex-r18c2`、branch `agent/codex-r18c2`、HEAD `e537f441010077123a307e9d50ea40cf8dad8547`符合任务。采用P0最终NOT_READY决定，不引用初稿READY作为训练资料就绪结论。

固定11状态/10 canonical tasks全部保留。以纯stdlib核对原JSONL行、source完整公共前缀、既有replay、原始模型输出/map/执行transition和终局；静态读代码/Git对象，未调用任何项目parser/validator或环境。

**精确审计disposition：输入—目标来源链支持9行/8个任务；HOLD_EVIDENCE 2行/2个任务；REINDEX_REQUIRED 0；EXCLUDE_INVALID 0。** 单看输入时点、map、raw ID、执行与既有replay的机械核对，11/11均匹配。另有10例MODEL_IDENTITY_PARTIAL、1例MODEL_IDENTITY_PINNED；9例显式done/won/reward终局，2例缺won。三个轴分别记录，不能将历史revision UNKNOWN伪作机械FAIL，也不能把9行来源支持写成9项合格训练N。合格训练N尚未建立，不以未知等同真实可用样本恰为0。

CASE_TABLE

## 逐字段来源与公共输入时点

`eleven_target_audit.json`每case含原分支path/line/行SHA、source episode path/line/行SHA、每字段JSON pointer和hash、完整前缀字段摘要、已有replay记录、map逐ID一致性、原selection metadata、执行transition/hash、终局及模型独立轴。原JSONL行SHA包含原换行；JSON字段摘要采用ASCII canonical JSON紧凑编码。

11例的静态P0公共文本与原source actor当时存储的公共prompt逐字节相同；这是内存中的静态对照，只输出hash，没有导出完整prompt或训练JSONL。task goal来自原source `task.text`，obs和有序actions来自 `steps[d].observation/valid_actions`；H4仅取j<d的已执行action及 `steps[j+1].observation`，j+1≤d。所有episode在该动作之前非终局，剩余horizon为50−d。

旧R1/R7未单独保存result_observation时，next-step pre-action observation与原replay的result逐项对照；没有把缺失字段假造回原记录。R4用完整R3 public replay及R4自己的exact-replay哈希收据，21条原动作/结果闭合；R10用原replay_full含每步公共状态/map；R16用完整source、当前obs/map/H4摘要与14/7/10/6条transition equality receipts。所有当前map、H4和时点核对均匹配。不同schema的summary/replay证据强度和来源在JSON中保留。

一个关键时间边界：`steps[d].metadata.environment`及当前step reward/done/result属于**原source actor执行当前动作之后**，不能拿来构成该动作前学生输入。其facts/expert_plan/won不进入投影。source当前model_output/推荐动作也不进入输入；只用原有pre-action动作表，保持原顺序。

R19仅以K1所引用的第一Stage2 generation和第一recovery transition为目标：stage_two_attempt=1、recovery_action_index=1、actions_consumed_before=31；before-history逐项等于原31步source前缀。原prefix replay31步与K1分支在恢复后的32步replay明确区分，后者不作为原prefix输入。目标是 `A002 → examine dresser 1`，不是后续SFT `look` 或K2目标。没有读取其他K目标来补该case。

## 临时ID、执行与suffix

每例P0 map都由该source时点的有序valid_actions按A000起编号；与原teacher parser的每个ID→command逐项一致，原source policy map也一致。11例原raw output均为相同合法bare ID、selection=selected、Stage1 valid、generation complete且未触cap；实际执行flag/command及transition相符。R19另有直接环境action receipt的before-state/map/command；旧collector以原command/执行flag/transition及静态调用点绑定。没有运行parser、修复ID或重索引。

所有目标属于adapter-off recovery teacher；adapter-on SFT suffix单独记录producer、步数、来源/引用及摘要，**不作为本轮额外训练目标**。原prefix 0→1不能复制成每条suffix action的因果正标签。`R10_OSR:R8-F02`第一恢复行动直接终局，suffix=0是有效已记录结构，不是缺失样本。

R8-F22/R8-F23是同一Book/DeskLamp trial的d=23与28两个前缀，不能计成两个独立task。这11个P0公共字段投影均不同，未观察到exact同输入多目标组；不表示全pool无歧义或公共输入充分。两例R8-F22/F23的后续公共行为序列摘要相同：`4c2493fa1cf07265ebc5e26a2eebc0308e8dcbd35842a5d3d6b73a4a34275843`。这说明重复行为/同task依赖，不能仅凭语义摘要相同断言physical generation被复用。固定集中不新增alias经验计数。

## 终局与reward的严格边界

R10的5例、R16的4例：原CONTINUE终局done=true、reward=0、won=false；恢复分支终局done=true、reward=1、won=true，支持该原环境记录中的0→1。won只作为终局审计证据，不进学生输入。

**R4:R2-F01：HOLD_EVIDENCE。** CONTINUE有done=true/reward=0/won=false；恢复terminal有done=true/reward=1和原success=true，但导出的恢复终局step没有won。它的输入、目标、map、执行与replay支持，新的严格终局corroboration仍缺项。不能凭“use lamp”文字、局部milestone或positive reward补写won=true。

**R19_K1:...b3ab21b8e193f6adf6ff：HOLD_EVIDENCE。** 原CONTINUE source最后done=true/reward=0，K1 suffix最后done=true/reward=1、原K1 success=1；两侧此schema都未保留won，故分别列缺项，绝不伪造won=false/true。第一恢复action本身非终局，不把后续SFT action当teacher目标。

静态历史Git对象证明四阶段的 `AlfWorldTextEnvironment.step`、`sft_p0_prompt`、`action_id_mapping`与冻结85对应方法AST相同，12/12对象读取returncode0。repo wrapper直接转发底层reward/done并把info存metadata，没有把won替换成reward。旧success helper使用done+positive reward；这说明旧标签的计算来源，**不证明任何positive reward都等价于won**，也不把这些原值武断称为塑形reward。当前installed ALFWorld源码请求won=True，但不能用当前包反填缺失历史won。两项HOLD针对本次学习证据要求，不重标旧科学结果、不撤销已完成G3/G4或旧review。

## 模型身份与记录tokens

10个历史case只有模型名Qwen/Qwen3-8B、adapter摘要、代码SHA及部分隔离manifest；weights/tokenizer实际resolved revision保留UNKNOWN。R10/R16有adapter-off恢复与adapter-on actor的隔离字段；R4manifest有双模型加载与adapter摘要，但无当时loaded commit收据，不能补造运行状态。其机械目标有效性与身份完备性分开。

R19 K1原execution/runtime有snapshot revision及loaded commit `b968826d9c46dd6066d109eabc6255188de91218`、tokenizer文件摘要/chat-template摘要、adapter目录 `6e403d85b150a74dfcc176f1f180ce4baf6fdacd922d2f96b3ceef0a21100f11`及active adapter隔离，故身份轴PINNED。此处只引用原receipt，没有加载模型/tokenizer或复验其科学gate。

TOKEN_TABLE

这些是**原已记录推理**tokens，不是新训练tokens；Stage2 generated均5也不能直接把55写成可训练监督token预算。公共文本匹配不等于已验证chat-template/tokenizer/label EOS/packing。所有prospective_projected_training_tokens为null；未加载tokenizer，teacher prompt长度不替代P0训练长度。模型revision UNKNOWN进一步限制历史长度可迁移性。

## B_pool未决条件与停止结论

**只用这11条rescue作为候选pool，success-only的B_pool与增益筛选C将采纳同一组，无法识别筛选条件的增量。** 11个正例核验不等于对照池已经就绪。本轮不扩大到neutral成功样本清洗、不构建pool或训练行。

仍需协调方决定并在未来具体任务闭合：相同生成来源与固定operator的完整候选pool及非rescue成功对照；同一student输入/目标粒度、普通成功背景和曝光分配；未知历史模型身份的可接受范围；两项终局won缺口是否有既存独立原件可佐证；独立canonical身份登记、污染缺项与新任务可用性；prospective实际训练token/重复上限/checkpoint及完整获取/验证/训练/评估费用。身份与预算登记由Luna另行负责，本线程未读取其未完成文件，也不借此造新schedule/预算。

DATA_FEASIBILITY保持NOT_READY。已有证据支持有限来源链审计，不证明学习收益、同pool机制效应或训练资料合格。首轮一次有界核验至此完成；未闭合项逐项HOLD，后续由协调方分配，不为positive扩样、不补跑、不调prompt/selector、不启动训练或新评估。科学85/2da与R19累计5142/7949（含旧177/342）保持，本轮科学增量0。
'''
 md=md.replace('CASE_TABLE','\n'.join(table)).replace('TOKEN_TABLE','\n'.join(tokens))
 (own/'ELEVEN_TARGET_AUDIT.md').write_text(md)
 contract=r'''# SI-P1 公共P0输入与学习目标证据契约

状态：STATIC_AUDIT_ONLY / DRAFT_NOT_EXECUTABLE。它定义这11例的审计字段与边界，不修改生产prompt、parser、协议或训练数据。

## 静态源码与原运行绑定

- [src/sft/protocol.py:56](/home/lizening/wt-r19-g4-consumer-contract-repair/src/sft/protocol.py:56)：sft_p0_prompt只渲染goal、当前obs、H4已完成action/result、有序indexed map；history_window固定4。
- [src/models/action_parser.py:89](/home/lizening/wt-r19-g4-consumer-contract-repair/src/models/action_parser.py:89)：按原valid_actions顺序从A000连续编号；ID是临时映射，不能跨状态搬用。
- [src/sft/policy.py:54](/home/lizening/wt-r19-g4-consumer-contract-repair/src/sft/policy.py:54)：实际policy用user chat template、add_generation_prompt=True、thinking=False，再tokenize/generate。本轮只读，未调用任何方法。
- [src/sft/r3.py:39](/home/lizening/wt-r19-g4-consumer-contract-repair/src/sft/r3.py:39)、[r3.py:71](/home/lizening/wt-r19-g4-consumer-contract-repair/src/sft/r3.py:71)：历史source前缀的action/result及history构造；[r9.py:32](/home/lizening/wt-r19-g4-consumer-contract-repair/src/sft/r9.py:32)对应完整public replay。
- [src/env/alfworld.py:58](/home/lizening/wt-r19-g4-consumer-contract-repair/src/env/alfworld.py:58)：reward=float底层reward，done=底层done，info放metadata；没有won到reward的转换。因此不把缺失won当已验证终局success。

`historical_contracts.json`列四个原运行代码SHA、上述prompt/map/env.step在Git对象中的行位置/文件SHA/方法AST SHA及冻结85对照，12个读取均exit0且对应AST相同；真实子进程receipt在 `historical_contract_read.receipts.json`。这是静态源码身份，不证明历史weights/tokenizer解析版本或当前installed ALFWorld包就是当时字节。

## 投影字段、时间与hash

投影哈希仅编码下列原字段，不带target、case id、canonical task id、d、stratum或K：

| 字段 | 原source指针 | 时间约束 |
|---|---|---|
| goal | /task/text | reset后已知 |
| observation | /steps/d/observation | 当前actor动作前 |
| recent_action_result_transitions | j=max(0,d−4)…d−1：/steps/j/action及/steps/(j+1)/observation | action已执行，result最迟在state d已知 |
| ordered_action_map | /steps/d/valid_actions按原顺序枚举为[Axxx,command] | 当前动作前完整列表；不取post-action metadata动作表 |

`projection_sha256`对上述字段的ASCII JSON（sort_keys=True、紧凑comma/colon）计算；ordered map是pair list以保留顺序。`full_public_prefix_field_sha256`另绑定0…d公共obs、0…d−1原actions、0…d动作表与goal。这些是明确命名的审计表示，不冒充原R8/R15完整prefix签名或chat-template/tokenizer序列。已有repo map/H4摘要只有在静态编码一致时核对，原件hash与新投影hash不混比。

原source actor存储的public prompt在11例均与静态P0规则在内存中产生的公共文本逐字节相同；只导出各字段及文本hash，不导出完整prompt、rendered-chat文本或训练JSONL。没有tokenizer，不能声称验证了未来训练序列、EOS、mask/packing或token预算。

明确排除：原source当前推荐动作/raw output/当前action后result/reward/done及metadata.environment、teacher诊断/subgoal/card、终局label、未来suffix/K/oracle、facts/专家计划。metadata.environment是post-action字段，即使包含won也只可作独立终局证据，不能作为pre-action输入。原始JSON可能含这些审计元数据，但投影白名单不读取它们构造学生输入。

## 目标与执行证据

本次目标仅第一adapter-off恢复Stage2原输出。核对原始raw ID、原parser selection、原id_to_command全部条目、P0有序map、原command、执行flag及transition；不调用生产parser或项目validator。若ID顺序不一致则REINDEX_REQUIRED，不自行换ID；malformed/unexecuted/失配标EXCLUDE_INVALID或HOLD并保留原行。不能把teacher原prompt移植到P0。

R19以K1 recovery_generation_event_ids中的Stage2、stage_two_attempt=1及recovery_transition_event_ids中的action index1绑定；原prefix replay31步作为投影来源，K1 checkpoint后的replay32步只用于历史suffix状态恢复证据。没有把K2目标或SFT suffix当第一恢复目标。

adapter-on SFT suffix只记独立producer/来源/步数/行为摘要；它不是adapter-off目标，也没有逐步0→1标签。空suffix可能是恢复动作直接终局，不能据空列表断言数据丢失。相同suffix行为hash不等于physical generation alias；同task多prefix仍是同一独立任务组。

## 独立轴与不可升级的结论

| 轴 | 本次结果 | 不能升级为 |
|---|---|---|
| 输入/目标/replay机械来源 | 11/11记录匹配；其中结合显式终局证据支持9，另2 HOLD | 11条合格训练行或数据验收PASS |
| 模型身份 | 历史10 PARTIAL；R19原receipt 1 PINNED | UNKNOWN机械FAIL或历史版本由R19倒填 |
| 终局corroboration | 9显式done/won/reward；R4恢复won缺失、R19两侧won缺失 | 任意正reward=环境won、塑形reward误当success |
| 公共字段投影 | 11个不同投影；无本固定集exact同输入多目标 | 全pool无歧义/输入充分或训练token已验证 |
| 学习/机制 | NOT_PROVEN；B_pool未就绪 | 被救回就能正迁移或C>B_source证明采纳机制 |

Dispositions是此线程审计分类，不是独立review权限。合格训练N仍未建立，DATA_FEASIBILITY=NOT_READY。当前只设计与审查，不改变任何科学执行行为。
'''
 (own/'PUBLIC_INPUT_CONTRACT.md').write_text(contract)
 print(json.dumps({'documents':['ELEVEN_TARGET_AUDIT.md','PUBLIC_INPUT_CONTRACT.md'],'lineage_supported_rows':len(supported),'lineage_supported_tasks':len({x['canonical_task'] for x in supported}),'hold_rows':len(holds),'training_N':'NOT_ESTABLISHED','B_pool_ready':False},ensure_ascii=False))
