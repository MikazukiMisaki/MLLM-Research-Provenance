# SI-E2 frozen implementation handoff

仅供独立 exact-SHA 工程审查；开发者测试不能自批验收。当前 **RUNTIME_NOT_READY**，真实 probe、采集、训练、评估及科学 launch 均未由本开发交付释放。

- 科学仓库：MikazukiMisaki/Alfworld-Self-Improvement-Project。
- 精确冻结提交：`dfc00e49d1ef4d48453d2331507429f8a0c7bbc5`；直接父提交：`a995d4c3c5f7d31a2cf1fd0afc4bfa4bd72ee3a3`。
- 分支/远端 ref：`codex/si-p3-runtime-adaptation` / `refs/heads/codex/si-p3-runtime-adaptation`。
- 本地 HEAD = origin = live remote；非 force push exit0。[远端收据](/home/lizening/research-notes/agent-logs/2026-10-25T124118Z__CODEX__si-e2-runtime-adaptation__sie2_4c82/LIVE_REMOTE_EQUALITY.json)。旧 a995 ref 未变。
- 隔离 worktree：/home/lizening/wt-si-p3-runtime-adaptation。15 个新增文件、2388 行；527 个旧 tracked blob 全部相同，旧方法修改0。
- 范围绑定：ENGINEERING_SCOPE.md SHA256 `7d4f554095e96f55bf97a286dbcbdc3851f9a34b8036c5ac72d048b15564f85d`。新增读隔离 ruling、既有review和输入见 [INPUT_BINDINGS.json](/home/lizening/research-notes/agent-logs/2026-10-25T124118Z__CODEX__si-e2-runtime-adaptation__sie2_4c82/INPUT_BINDINGS.json)。

## 实现与边界

1. `runtime_gate.py` 与两个 versioned schemas：精确源码/clean gate、外部发布的 authorization 原字节 SHA、proposal 原字节 SHA、UUID、输出身份、时窗和收紧预算。拒绝 acquisition/train/eval。运行时路径只来自参数，不在科学提交中固化机器路径。schema 文件本身不签发授权；预期 authorization SHA 必须来自协调方另行冻结的 release，issuer 字符串不能自授权。
2. `runtime_backend.py`：复用冻结 Qwen loader、本地离线8B与P0加载边界。四个输入先由本地 tokenizer 预核预算；8B分配前先建立一字节CUDA context，验证实际UUID和可见自身NVML compute PID，不能证明则便宜停止。实际参数/无量化/无offload、Qwen3/config/SDPA必须被观测并记录；保留PEFT默认F32 LoRA，不为dtype一致而cast。真实loader本轮没有执行。
3. 生成前重建渲染输入，完整 IDs 和 mask 与实际送入 generate 的张量逐项相同后才 reserve。补充 proof 在严格旧 `Generation.raw` 之外。实际 PEFT `get_model_status/get_layer_status` 检查 enabled、active names、merged状态；BASE使用真实disable context。正常/异常退出都恢复原梯度标志，处理安装版PEFT退出时重新开启LoRA requires_grad的问题。P0原EOS-incomplete解析决策和v2裸ID parser不变。
4. `runtime_diagnostic.py`：独立工程入口，四个phase-specific synthetic prompts及digest预先冻结；Stage2使用预声明synthetic diagnosis/subgoal，不根据实际Stage1临时造fallback。实际invalid/incomplete是记录结果，不是质量失败或重试理由。这不是一次真实因果teacher branch。生成命令不执行到环境；完整Collector继续synthetic-only，未连接真实A96采集。
5. `runtime_environment.py`：原始G3第0条已完成source，canonical SHA `fba2a4278c4f1d9640c1c39f527fe3d5e7022ab50af4d353bc017bb31bbead89`、executed2da/run260422，不搜索成功case。after-map来自原reset/transition refs，不能从trajectory pre-map猜。源game/traj hashes交叉绑定原metadata和completion，原game物理路径绑定，拒绝复制/换目录。两个新一game实例、同pool_seed，比较全部公共字段及有序map。真实None终态map保留为证据并严格拒绝不匹配，不补成空map。
6. 新factory在ALFWorld构造之前限制effective dataset.data_path到唯一认证历史task目录，并采用no-scan subclass。旧全TRAIN扫描helper和原YAML不改；原domain/grammar内容另做hash绑定。软件sentinel测试表明不会打开sibling任务body。该限制是获裁定的工程读取隔离，不改变任务选择或环境动作语义。
7. `runtime_ledger.py`：独立fsync工程账本，actual completed成本加incomplete保守预留重算；raw query failure保留gpu/process行及checkedPID，summary置零或input/mask篡改不能仅靠重算chain通过。construct/close独立于reset/action计数。技术中断不制造任务失败、不退款已开始操作、不自动重试。
8. `runtime_supervisor.py`：外部monotonic deadline覆盖load与阻塞callbacks；-I子进程/parent identity/source/input绑定，parent-death signal，独立进程组和subreaper。按PID/start-tick/UID清理自身子孙，包括另开session的子孙，并记录authentic exit、deadline、遗留PID、实际分配时长及report缺失。既有外部graphics/compute进程不被杀；未知NVML PID不放宽。软件fixtures的实际GPU分配计数为0。

模块public `__version__` 与协调方pinned bindings采用同一wire约定（缺失为空）；distribution metadata另记，不能混同或编造版本。模型/环境实际运行package路径、hash、public版本必须与proposal相同。

## 实际软件与只读证据

固定解释器：`/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python`；软件检查CUDA不可见、HF offline、禁止pytest cache。

| 检查 | 真实结果 | 原始收据 |
|---|---|---|
| 原有a995 tracked代码基线 |800 pass /3 fail /77 errors，exit1|`receipts/baseline_a995.*`、`baseline_a995.xml`|
| 干净冻结candidate focused |**83 pass，exit0**|`receipts/frozen_focused.*`、`frozen_focused.xml`|
| 干净冻结candidate full |**883 pass /3 fail /77 errors，exit1**|`receipts/frozen_full.*`、`frozen_full.xml`|
| 编译/JSON解析 |12 Python、2 JSON，exit0|`receipts/frozen_compile.*`|
| 冻结diff check |exit0|`receipts/frozen_diff_check.*`|
| 原始source wire纯读取 |6命令、7状态、8原refs；输入前后hash一致，exit0|`actual_original_source_wire_check.json`、`receipts/actual_source_wire.*`|

[REGRESSION_COMPARISON.json](/home/lizening/research-notes/agent-logs/2026-10-25T124118Z__CODEX__si-e2-runtime-adaptation__sie2_4c82/REGRESSION_COMPARISON.json) 按ID及failure/error类型核对80项完全相同；无新增/丢失、无skip/xfail，新增83项恰为focused集。开发者结果不是独立PASS。

基线收集在实现前开始，期间写入了新的untracked工程文件，原527 tracked字节未变、新测试尚未创建/收集；不宣称它是全程pristine工作树。独立pristine a995基线800/3/77另由既有Sol review绑定；详见 [BASELINE_CONTEXT.json](/home/lizening/research-notes/agent-logs/2026-10-25T124118Z__CODEX__si-e2-runtime-adaptation__sie2_4c82/BASELINE_CONTEXT.json)。冻结candidate的focused/full前后均clean。

非空生产fixture走实际prepare/parser/PEFT状态/ledger/reconstruct/report及规范环境adapter，仅替换模型generate与TextWorld I/O：4 synthetic generations、8输出tokens、521输入tokens；2reset/2step、2construct/2close，13started全部completed。该fixture不是实际六步历史env replay；真实六步wire仅作原件读取验证。[compact evidence](/home/lizening/research-notes/agent-logs/2026-10-25T124118Z__CODEX__si-e2-runtime-adaptation__sie2_4c82/NONEMPTY_INTEGRATION_EVIDENCE.json)。完整token/tensor fixture树保留在/tmp，不发布。4条真实negative CLI child returncode1覆盖draft dirty拒绝及frozen clean下坏snapshot/输出复用；[收据](/home/lizening/research-notes/agent-logs/2026-10-25T124118Z__CODEX__si-e2-runtime-adaptation__sie2_4c82/NEGATIVE_CLI_SUMMARY.json)。4条真实subprocess exit覆盖exit0、exit7、普通/另开session超时均-9，子孙清理可核对；[收据](/home/lizening/research-notes/agent-logs/2026-10-25T124118Z__CODEX__si-e2-runtime-adaptation__sie2_4c82/SUBPROCESS_DEADLINE_EVIDENCE.json)。

保留draft v1的53pass/13fail（tiny tokenizer默认token_type_ids导致；只修fixture为Qwen keys，未放宽生产校验），v2的66pass、v3的76pass、v4的83pass以及全部stdout/stderr/returncode。早期通过不代替exactSHA结果。

## 行为变化与保存

[全delta](/home/lizening/research-notes/agent-logs/2026-10-25T124118Z__CODEX__si-e2-runtime-adaptation__sie2_4c82/full_delta.patch)、[stat](/home/lizening/research-notes/agent-logs/2026-10-25T124118Z__CODEX__si-e2-runtime-adaptation__sie2_4c82/full_delta_stat.txt)、[新增文件和全部AST方法hash](/home/lizening/research-notes/agent-logs/2026-10-25T124118Z__CODEX__si-e2-runtime-adaptation__sie2_4c82/NEW_METHODS_AND_FILES.json)、[全部旧blob相同](/home/lizening/research-notes/agent-logs/2026-10-25T124118Z__CODEX__si-e2-runtime-adaptation__sie2_4c82/OLD_TRACKED_BLOB_EQUALITY.json)、[行为flags](/home/lizening/research-notes/agent-logs/2026-10-25T124118Z__CODEX__si-e2-runtime-adaptation__sie2_4c82/BEHAVIOR_CHANGE_FLAGS.json)、[worktree状态](/home/lizening/research-notes/agent-logs/2026-10-25T124118Z__CODEX__si-e2-runtime-adaptation__sie2_4c82/FROZEN_WORKTREE_STATES.json)、[原输入最终hash](/home/lizening/research-notes/agent-logs/2026-10-25T124118Z__CODEX__si-e2-runtime-adaptation__sie2_4c82/ORIGINAL_INPUTS_FINAL_CHECK.json)。旧R19/analyzer/scientific settings/预算/科学统计/训练recipe/Collector gate修改均false；新增工程bridge、诊断、deadline、工程账本consumer和读隔离为true。未新增实际采集或训练driver、confirmatory reporter。

科学85/执行G3的2da、旧a995和旧失败证据均保留。科学历史仍5142 generations /7949 reset-inclusive envops，包含原177/342。本任务实际8B/P0加载/生成、CUDA context、ALFWorld构造/reset/step、采集/训练/eval、新task正文读取全部0。**真实CPU软件活动存在**：新测试5次tiny CPU generate；基线及full各跑既有E1双臂toy continuation，共4 toy臂/72 optimizer updates/576forward+576backward microbatches。它们不是actual8B/P0训练，权重留/tmp且不发布。[活动边界](/home/lizening/research-notes/agent-logs/2026-10-25T124118Z__CODEX__si-e2-runtime-adaptation__sie2_4c82/SOFTWARE_ACTIVITY_AND_COST_BOUNDARY.json)。

## Luna准备依赖与未证项

- **NOT VERIFIED**：实际8B/P0字节加载/adapter切换、GPU UUID/PID namespace可证明性、SDPA/device/dtype实际状态及显存/时延。代码检查存在不等于观测通过；无法识别自身NVML PID必须停止，不能改成忽略其他进程。
- **NOT VERIFIED**：实际ALFWorld两fresh replay及终态map暴露；目前只有真实wire读取与fake TextWorld I/O。完整Collector-to-auditor仍仅synthetic，无实际A96 runtime readiness。
- **NOT IMPLEMENTED/NOT OBSERVED**：实际collection/training/evaluation driver、未来B/C新pool/exposure、actualP0续训、学习/效能、confirmatory reporter。未证明4device-hours或训练显存可完成，不从静态参数推算运行PASS。
- 所有SCIENCE/PREFLIGHT/LAUNCH仍NOT_GRANTED。源码exactSHA工程审查仅由Sol独立完成；通过后还需Luna冻结具体immutable proposal与协调方另行工程release。

后续命令接口已实现，但下面仅是**不可直接执行的待审模板**，没有有效authorization文件或GPU值：

```text
CUDA_VISIBLE_DEVICES=<approved UUID> HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 \
  /home/lizening/miniconda3/envs/alfworld-self-improve/bin/python -I \
  /home/lizening/wt-si-p3-runtime-adaptation/scripts/run_si_p3_engineering_probe.py \
  --authorization <root-released-authorization.json> \
  --authorization-sha256 <externally released exact bytes SHA256> \
  --proposal <immutable proposal.json>
```

[授权schema](/home/lizening/wt-si-p3-runtime-adaptation/configs/self_improvement/si_e2_authorization_schema_v1.json)、[proposal schema](/home/lizening/wt-si-p3-runtime-adaptation/configs/self_improvement/si_e2_proposal_schema_v1.json)、[运行合同](/home/lizening/wt-si-p3-runtime-adaptation/docs/si_p3_runtime_engineering_v1.md)。Proposal需绑定实际snapshot/P0路径、原JSONL+ledger/YAML/game/traj_data+logic文件、interpreter/package origins、固定synthetic prompts digest；授权另绑本提交、proposal原字节SHA、UUID、唯一output、UTC窗口与ceilings。建议后续只提议4calls/88output/32768input/8192percall/2reset/**12step**/1800s/0.5device-hour，仍待具体审查与release。本开发者不发起这个probe。

provenance仅写本目录；不commit/push provenance、不改共享INDEX/inventory、协调方或Luna文件。Publication manifest供协调方统一发布，raw software trees/weights/token数组留本地。
