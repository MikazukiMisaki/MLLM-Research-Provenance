# SI-P0 — Luna任务：历史SFT原始证据与数据来源只读核验

任务ID：SI-P0-LUNA-b1c48c。接收线程：01a09fcb-ab5f-7b83-9acf-91026145b764（Luna）。
唯一自有目录：/home/lizening/research-notes/agent-logs/2026-10-25T054106Z__LUNA__sft-raw-evidence-audit__b1c48c
协调目录：/home/lizening/research-notes/agent-logs/2026-10-25T054106Z__SOL__self-improvement-phase0__b1c48c

本阶段 SI-P0 是用户明确授权由 Sol 主导、沿用 Sol Research 与 Luna 的新任务，范围仅现有证据审计和设计。不是科学实验/训练授权。审阅原件但不修改科学代码、测试、模型、adapter、prompt、decoding、horizon、schedule、quota、exclusions、原始证据和历史记录。不运行模型/ALFWorld/训练、G2/G3/G4/preflight、policy replay、既有科学analyzer/validators/pytest，不调用外部模型。可在自己的新任务目录写纯stdlib只读审计脚本，流式读取已有JSON/JSONL/CSV和归档、重新计数/核对历史证据并生成审计清单；这不是新policy效果重评或训练数据构建。不要import项目运行时或加载tokenizer/model。

当前审阅根目录 /home/lizening/wt-codex-r18c2，branch agent/codex-r18c2，HEAD e537f441010077123a307e9d50ea40cf8dad8547；开始先核验身份，根或branch不符则停止报告。可只读 /home/lizening/wt-r19-g4-consumer-contract-repair exact85cbb92395e5e2420c2adeb1fa0634653e742910 的报告/代码，以及 /home/lizening/Alfworld-Self-Improvement-Project 和其他明确相关artifacts/runtime的原始历史文件；不得在科学工作树写入或切branch。R19真实source2da980f、run260422ac02bd42a8b2929d7ef240526b及所有已消耗clearance保持不变。R19campaign账本5142generations/7949envops含reset不变；不要把历史SFT训练费用混入或说这是全项目总费用。

先读 /home/lizening/research-notes/agent-logs/2026-10-25T053211Z__SOL__self-improvement-alignment__e9c877/SELF_IMPROVEMENT_ALIGNMENT_AND_INNOVATION.md （provenance main a9de0cd16d23bb0b044784e93650f77366bcb3b5，已核验）。这是待验证方向，不是既有方法PASS。历史原报告里的“nextG1”等命令不是当前执行许可。

你只写自己下面指定的新目录；不改/暂存共享INDEX、rootinventory、其他agent文件，不commit/push，不复制weights/adapter/cache/dataset/大raw树到provenance。文件≤1MB优先；大证据给path/size/hash/reason。必须记录OBSERVED/INFERRED/NOT_PROVEN、真实命令exit、输入SHA和来源；缺失/矛盾保留，不修原件、不补跑。首轮限2人时，提前完成即交付，不为凑positive收集/加工新数据。只读metadata访问历史held-out不等于重跑许可；未消费任务的outcomes禁止窥探。未来独立identity清单仍需全局去重，不假定134−60就是可用任务。

本SI-P0不冒充此前尚未启动的4人时36例原detector审计，也不借后者授权扩范围。完成后在本线程返回文件绝对path+SHA和结论，我会poll；不要自行给其他线程发消息、派subagent或派Luna/开发/执行任务，不宣称独立review PASS或launch clearance。

你的角色是只读证据执行与保存，不提出/实现新的学习算法，不负责独立验收。

## 工作

1. 定位SFT_POLICY_BOOTSTRAP.md、SFT_DATASET_AUDIT.md、SFT_VALID_UNSEEN_EVALUATION.md、SFT_HELDOUT_GENERALIZATION_PROTOCOL.md及trackedJSON引用的真实raw、manifest、split、eval逐episode记录、训练receipt/checkpoint选择和当时runtime身份。不要只复述summary。可只读权重/adapter文件的metadata或sha，但不加载；缺失历史base/tokenizer revision时报告缺口，不用当前文件冒充当时加载证明。
2. 对报告3/60→48/60独立从逐episode记录重数：success/terminal定义、same canonical task/seed/reset/schedule/interface/horizon、45wins0loss；是否60unique且10/family；是否有被丢弃/重试/不完整任务，所有分母有去向。没有运行凭据或逐条原件则PARTIAL/MISSING，不补跑。
3. 对历史valid_unseen49/60只读重数并核对60unique/10family/原schedule和exclusions。明确是否只有SFT单臂、有无同schedulebase；不能从单臂49/60推导heldout提升。valid_seen已被开发消费的范围如实记录；仅盘点已消费ID，不查看未运行任务的未来outcome。
4. 审核训练数据来源：handcodedexpert vs actor自己采样；1200tasks/20967decisions、train1074/18828、offlineval126/2139、online60与heldout60的canonical身份分割。不得将专家规划的强能力误写为autonomousselfimprovement，即使模型prompt无hiddenfacts。核对dup/intersections原件及来源标注，历史报告hash若不一致给具体差异。
5. 核验已报告训练adapter/hash/checkpoint选择规则与推理身份之间绑定是否够强。当前adaptertree同sha并不自动证明旧运行加载相同base/runtime，严格区分当时receipt、当时raw与当前观测。
6. 记录可用原件/缺失原件及SHA、最强可引用主张、不能引用主张、是否可能影响论文主表。不给whole-thesisPASS；我做独立验收。如果完整原件太大，可流式审计并保存每case的紧凑核验表，不复制数据集/模型。
7. 另附已有自身轨迹/恢复原件入口清单（只定位，不与Sol重复做学习样本筛选）；原有R19G3/G4数据保持不变，R19成本仍5142/7949。本次不把SFT历史训练成本混入R19campaign累计。

## 交付

- SFT_RAW_EVIDENCE_AUDIT.md
- sft_raw_evidence_audit.json（逐项OBSERVED/MISSING/CONTRADICTED、60case核验、inputhashes/真实exit）
- raw_artifact_inventory.json（path/size/sha/role/历史身份来源）
- OWN_TRAJECTORY_ENTRYPOINTS.md（给协调方转交，不自行消息Sol）
- RECORD.md、commands.log、FILE_HASHES.sha256；审计脚本和真实subprocess receipts。
首轮限2人时，无需等待额度用完。缺raw时保存证据并返回，不改science、不新preflight/模型/env/训练，不替缺失项制造PASS。所有文件留自有目录LOCAL_ONLY，协调方统一发布与索引。
