# SI-P0 — Sol Research任务：自身经验可学习性与最小闭环草案

任务ID：SI-P0-SOL-b1c48c。接收线程：01a165de-c75e-7120-abc9-fa74cde1f17f（Sol Research）。
唯一自有目录：/home/lizening/research-notes/agent-logs/2026-10-25T054106Z__CODEX__self-experience-feasibility__b1c48c
协调目录：/home/lizening/research-notes/agent-logs/2026-10-25T054106Z__SOL__self-improvement-phase0__b1c48c

本阶段 SI-P0 是用户明确授权由 Sol 主导、沿用 Sol Research 与 Luna 的新任务，范围仅现有证据审计和设计。不是科学实验/训练授权。审阅原件但不修改科学代码、测试、模型、adapter、prompt、decoding、horizon、schedule、quota、exclusions、原始证据和历史记录。不运行模型/ALFWorld/训练、G2/G3/G4/preflight、policy replay、既有科学analyzer/validators/pytest，不调用外部模型。可在自己的新任务目录写纯stdlib只读审计脚本，流式读取已有JSON/JSONL/CSV和归档、重新计数/核对历史证据并生成审计清单；这不是新policy效果重评或训练数据构建。不要import项目运行时或加载tokenizer/model。

当前审阅根目录 /home/lizening/wt-codex-r18c2，branch agent/codex-r18c2，HEAD e537f441010077123a307e9d50ea40cf8dad8547；开始先核验身份，根或branch不符则停止报告。可只读 /home/lizening/wt-r19-g4-consumer-contract-repair exact85cbb92395e5e2420c2adeb1fa0634653e742910 的报告/代码，以及 /home/lizening/Alfworld-Self-Improvement-Project 和其他明确相关artifacts/runtime的原始历史文件；不得在科学工作树写入或切branch。R19真实source2da980f、run260422ac02bd42a8b2929d7ef240526b及所有已消耗clearance保持不变。R19campaign账本5142generations/7949envops含reset不变；不要把历史SFT训练费用混入或说这是全项目总费用。

先读 /home/lizening/research-notes/agent-logs/2026-10-25T053211Z__SOL__self-improvement-alignment__e9c877/SELF_IMPROVEMENT_ALIGNMENT_AND_INNOVATION.md （provenance main a9de0cd16d23bb0b044784e93650f77366bcb3b5，已核验）。这是待验证方向，不是既有方法PASS。历史原报告里的“nextG1”等命令不是当前执行许可。

你只写自己下面指定的新目录；不改/暂存共享INDEX、rootinventory、其他agent文件，不commit/push，不复制weights/adapter/cache/dataset/大raw树到provenance。文件≤1MB优先；大证据给path/size/hash/reason。必须记录OBSERVED/INFERRED/NOT_PROVEN、真实命令exit、输入SHA和来源；缺失/矛盾保留，不修原件、不补跑。首轮限2人时，提前完成即交付，不为凑positive收集/加工新数据。只读metadata访问历史held-out不等于重跑许可；未消费任务的outcomes禁止窥探。未来独立identity清单仍需全局去重，不假定134−60就是可用任务。

本SI-P0不冒充此前尚未启动的4人时36例原detector审计，也不借后者授权扩范围。完成后在本线程返回文件绝对path+SHA和结论，我会poll；不要自行给其他线程发消息、派subagent或派Luna/开发/执行任务，不宣称独立review PASS或launch clearance。

你的角色是技术/方法可行性分析，不拥有独立验收权。本轮不开发学习方法或选择器。

## 工作

1. 建立已有自身经验清单。分阶段查找现有source/continue/recover/共同路径数据：Sprint2C120配对，SFT后的R4、R12、R16–R18、正式R19；用已有manifest/JSON/原件引用，清点阶段、policy/adapter身份、canonical task/trial、prefix/horizon、模型生成来源、实际成功/失败、可用prompt/raw output/action-map/transition/termination以及hash。不要把专家SFT数据标为self-generated。若历史base model身份缺失，保留UNKNOWN，不能用现在R19runtime倒填。
2. 分开普通self-success、实际rescue（同原前缀CONTINUE0/recover1）、neutral、harm、incomplete和仅oracle-over另一个K。R19两个额外oracle病例CONTINUE本来成功，不是新增rescue标签；已有R19K2两次rescue要按真实原件列明。失败G3未完成source unit不算任务失败、不进入正样本。
3. 全局/分层去重：同task的多prefix、同prefix多treatment、同K alias、跨R16–R18反复使用的60prefix不能当独立新样本。区分独立episode数与state/branch数，保持不同actor/base/处理分别计数，不把历史120与新36拼成156训练独立样本。
4. 评估可学习性，仅产生审计候选索引，不生成训练JSONL或挑选新规则。看是否有完整公共输入、正确临时Action-ID映射、可追溯模型目标、独立终局增量、足够的多任务覆盖；token长度只用已记录值，不能加载tokenizer。局部subgoal成功不代替任务成功；残缺、数据泄漏、专家标签、模型可见hiddenfacts、同任务重复、动作后未来信息进入输入等明确排除或标未证实。
5. 给出DATA_FEASIBILITY结论：READY_FOR_PROTOCOL_DESIGN / NOT_READY / INDETERMINATE，分别说明数据瓶颈、能证明的最大主张、缺口。不要为了达到某个任意小N而授意新采集。列出足够支撑设计的事实，以及仍不能估样本量/学习增益的事实。
6. 最小闭环草案仅一轮：A冻结SFT-P0；B普通成功筛选自身经验SFT；C拟议“增益验证纠错经验采纳”SFT。明确B/C训练tokens/steps/checkpoint规则、数据生成/配对验证成本、公平比较和新数据防泄漏；C>A说明超过强基座、C>B才说明采纳机制增量。不制定虚假的已授权N、科学预算或argv，不承诺显著；声明自身经验稀少可能使此候选不值得继续。当前 learnedselector/memory/DPO/额外环境禁令不变。
7. 创新对照表：Re-ReST(https://aclanthology.org/2024.emnlp-main.861/)、TrainingLanguageAgentstoLearnfromExperience(https://arxiv.org/abs/2605.20477)、CIR(https://arxiv.org/abs/2610.00372)，必要时查原论文/作者代码。比较经验来源、干预增量标签、运行时router vs训练资料采纳、是否学习/写回、新任务验证。只有primarysources；候选区别不是首创或有效性证明。不要无限扩展literature。

## 交付

- SELF_EXPERIENCE_FEASIBILITY.md
- experience_inventory.json（候选ID+阶段+count/source/hash与明确缺口，≤1MB）
- MINIMAL_SELF_IMPROVEMENT_PROTOCOL_DRAFT.md（DRAFT_NOT_EXECUTABLE）
- INNOVATION_COMPARISON.md（primarylinks和已读范围）
- RECORD.md、commands.log、FILE_HASHES.sha256；纯审计脚本与真实exit receipts。
原始大数据不复制。返回自己的冻结文件SHA和是否需要澄清的具体证据问题。Luna另行做SFT历史raw核验，两项并行；不读取其未完成文件或自行互发任务，协调由我负责。
