# SI-P1 RECORD — 11目标、隔离预算与最小协议独立审查

任务 SI-P1-REVIEW-caae4c；协调方 Sol Designer / Technical Lead / Independent Reviewer。状态 **ACCEPT_WITH_CORRECTIONS__AUDIT_AND_DESIGN_ONLY**。DATA_FEASIBILITY、TRAINING_DATA_READY、EXECUTION_READY 均 NOT_READY；无新实验许可或 launch clearance。

## 时间、授权与分工

任务目录时间 2026-10-25T06:52:00Z；此前已做起点只读 guard。本记录封存准备时间 2026-10-25 07:37:25 UTC，实际发布/远端验证完成时间在忽略的 post-push-receipt.json。用户明确要求 Sol Research 逐案核验11状态、Luna补隔离和预算、协调方收敛最小协议/统计标准并独立审查，先不启动新实验；沿用 Full Access 对已授权可逆审计/文稿/发布的权限，没有新增科学授权推断。

实际队列派发、ACK、完成状态和工具实际exit信息见 dispatch_receipts.json、agent_acknowledgments.json、sol_completion_and_receipt_metadata.json、luna_completion_and_receipt_metadata.json。Sol Research 实际线程 01a165de-c75e-7120-abc9-fa74cde1f17f；Luna实际线程 01a09fcb-ab5f-7b83-9acf-91026145b764，均在 sdxsrv03。没有新建 agent 或虚称已派发；两位已完成并冻结，协调方统一发布。

## 仓库与漂移

Scientific repository MikazukiMisaki/Alfworld-Self-Improvement-Project：
- review-root /home/lizening/wt-codex-r18c2，agent/codex-r18c2，起止 e537f441010077123a307e9d50ea40cf8dad8547，干净。
- frozen analyzer /home/lizening/wt-r19-g4-consumer-contract-repair，codex/r19-g4-consumer-contract-repair，起止85cbb92395e5e2420c2adeb1fa0634653e742910，干净。
- executed G3 /home/lizening/wt-r19-recovery-duration-v1，保持 detached2da980f631badc25086d12db60d128ff507d3ae6，干净。
- /home/lizening/Alfworld-Self-Improvement-Project仅读取原始历史证据，没有开发/分支切换/源码或测试修改。
- provenance /home/lizening/research-notes main，本轮基点57747744922bf7d44d0c30f1bd24cb6624f8216e；起点及发布前 live ls-remote 一致。不动其他历史 untracked fixtures。

START_STATE.json、END_STATE_BEFORE_PUBLICATION.json保存实际命令输出/返回码。原G3/source/branch和35个Sol输入、协调方独立读入文件重新hash未变；Luna V1指向transient P0元数据的例外另列，不假称所有这些旧路径字节相同。

## 独立检查与结果

1. 独立stdlib读取原JSONL行和full-file SHA，11/11动作前P0公共文本、H4、完整动作表、原raw ID/parser、实际执行及已有replay匹配。11state仅10canonical task；同Book双prefix不增加独立N。原done/reward成功标签保留；9显式won、2 RAW_WON_NOT_RECORDED分轴。10历史模型/tokenizer identity PARTIAL、1 R19 PINNED；训练N未建立。
2. 独立351条prefix-to-task/row hash和7个stage整文件hash全部匹配，跨阶段169task都在2,612已登记known-use union内。supported差集1141TRAIN/0seen/74unseen，新增映射不改变集合；不构成全历史clean证书。
3. 原success helper、wrapper、run_sft_suffix、record_step做静态AST和executed2da Git对象比对，4/4相同、4次真实git show exit0；原导出不含won。没有执行这些方法或认证历史安装binary。
4. 对作者4份冻结hash清单逐项核对75条，35个source输入再次相同；终局澄清和Luna V2与独立原件相符。
5. 纯数学112场景枚举exact conditional McNemar规划，6项算术条件含独立小n三项枚举对照通过。只是假想δ/q/N，未读新task结果、未训练/评估policy；不叫完整验收功效，不拨付样本量。
6. 最小设计A/B_pool/C、同池共同质量、每task一个事前anchor、无未来信息学生输入；双侧exact McNemar+Holm两主比较，另设观测净增益≥5pp、gross harm≤5%的前瞻项目护栏。未冻结执行T/U/token/recipe/N/预算，设计可审查而执行不可用。

原始日志与真实subprocess.returncode：independent_source_hash_and_identity_join.log/.receipt.json exit0；independent_target_and_isolation_review.log/.receipt.json exit0；hypothetical_power_enumeration_v2.log/.receipt.json exit0；verify_phase1_deliveries.log/.receipt.json exit0。静态Git对象真实exit另在independent_frozen_success_contract.json；科学pytest/项目validator未执行，不能记为PASS。

Sol首次自有schema probe exit1是合法空suffix的探测错误，后续修正仅在新审计脚本；失败原日志保留。Luna多次文稿builder的真实工具metadata包含一次exit1和后续exit0；一个只读发现命令工具exit=-1，未冒记为科学失败或0。协调方少量推测路径发现命令exit1/2随后定位到实际文件；不改变科学结果。关键结论均由真实最终原件检查支持。

## provenance范围事件与更正

Luna V1运行旧脚本，硬编码P0 ROOT导致2个已发布metadata被写、2个新metadata写进旧目录。协调方先保存全部4项变动字节和实际hash到新P0_SCOPE_INCIDENT_SNAPSHOT，再恢复两个tracked P0文件至5774774精确字节，并将新增旧目录项保存在snapshot。科学源码/原始运行证据未改。这是实际provenance ownership/immutability偏差，不能仅说科学树干净就掩盖。

Luna V1/原hash清单和Sol最初9/2综合disposition都保留；纠正分别新增V2和success-axes addendum。V1的sourcehash/整批映射缺失、walltime当GPUtime、input_tokens_seen擅称padding、重复计数等解释撤回；详见notes/HISTORICAL_CORRECTIONS.md及INDEPENDENT_REVIEW.md。不要求作者改旧字节来取得PASS。

## 成本、执行和结论边界

本轮模型、ALFWorld、tokenizer、训练、source/replay/G2/G3/G4、preflight、项目analyzer/validator、pytest、新heldout policy评价全部0；没有新的argv/gate/schedule。R19实际累计5,142 generations/7,949环境操作（7603非reset+346reset），已含旧177/342；0 incomplete external operations，旧incomplete source不改判。

这不是全项目训练/推理成本。历史SFT单列2,354updates、27,406.28269892931秒walltime、23,860,000 input_tokens_seen；GPU device-time/padding语义UNKNOWN。R4/R10/R16历史获取与配对验证的全成本尚未在此重建，不能用R19总数或零替代。共享原件实物花费与未来独立方法获取/训练/评估费用分别记账。

输出主要文件：INDEPENDENT_REVIEW.md、phase1_independent_review.json、MINIMAL_PROTOCOL_DESIGN.md、STATISTICAL_ACCEPTANCE_CRITERIA.md、NEXT_EVIDENCE_SCOPE_DRAFT.md以及两位作者冻结交付/原始receipts。NEXT scope仅草案未派发，不隐式授权扩大11case工作。

当前继续设计具有明确可证伪问题，但11行/10task并不足以宣称学习数据或方法就绪。下一项必要证据是同池成功对照的共同质量/anchor后是否仍与C可分；若数据、独立任务或预算不足，结束此学习配方，保留强SFT和恢复/副作用/成本的论文实证，不自动增样/调prompt或训练至positive。

## 发布

仅新增本轮三个独有目录、自己的INDEX行、上述更正及当前root hash inventory；不stage其他agent历史untracked files。不改旧作者字节。扫描、清单、窄暂存、commit/push、Git对象远端逐字节核对由协调方完成；最终自指commit和实际远端验证结果在本目录忽略的post-push-receipt.json及面向用户最终回执，不伪造包含自身commit的正文。
