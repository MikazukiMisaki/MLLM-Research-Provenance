# Astra：source-only 有界投入与 C01/C02 附录独立审查

**支持新的 SOURCE_ONLY_INVESTMENT 决定；C01/C02 文档问题关闭。** 本次只评审投资逻辑和文档，不是启动许可；实际运行仍取决于最小source-only实现、独立验收和可信执行/资源条件。本评审不再把“采集前已知能形成C24”列为投入前置条件。

已通过 `codex_app.read_thread` 核实协调线程 Sol Designer 中用户最新直接要求：“行，你来持续进行这个任务，直到开始实验”。用户授权持续推进；这不要求把旧已消费探针/G3授权复用，也不允许放宽执行身份或伪造数据。本轮按协调方指派只做静态审查，未运行模型、CUDA、环境、SSH、tokenizer、测试或preflight，未修改科学源码或已封存记录。

## 1. 为什么接受这次投入转变

这不是要求原完整配方一定成功，而是明确购买一个更窄的可证伪结果：**同一已登记A96、冻结P0、固定d5规则下，source端数量是否已经排除了构造原Q/C/neutral配方的可能。** 它是前瞻性、单臂的source可行性研究；第5步只记录状态，不进行恢复干预。

完整96正常闭合后，若E/F/S总量或家族必要上界不足，就可以终止这套固定任务、位置、剂量与门槛的配方，免去后续teacher和效能投入。若必要上界全够，得到的只是“尚未被这些条件否决”，仍不知道teacher成功率、完整Q、实际C24、可学习性或学生收益。

因此不需要在新数据前已经知道C24可构造；那正是试验需要消除的部分不确定性。旧6/120不能预测新96，更不能用来代替这个测量。此前NO_GO针对缺少明确阶段性投入决定及运行准备；现在协调方提出并愿意承担一次有硬帽的必要条件否证研究，投资问题已具体化。我支持这一新的理由，而非继续以未知yield循环阻止测量。

接受的范围是**一次source-only研究**，不是全paired采集、teacher投资、训练或600-task评价。一次失败也只能否决该固定配方，不能宣称整个自我改进方向无效。请将新的投入决定单独版本化，使其取代此前“source96投入理由未闭合”的当前状态；原记录保留为历史事实，不追溯成早已获准。

## 2. 预算与入口必须同时收窄

| 项目 | source-only硬上限/规则 |
|---|---:|
| 已登记A96任务 |96，不换身份、不补任务|
| P0 source generations |4,800|
| source动作 |4,800|
| source初始reset |96|
| 含reset环境操作 |4,896|
| 输出token |76,800|
| 累计输入token |16,000,000|
| 每次输入token |保留既有8,192帽，不截断prompt|
| GPU占用 |≤4 device-hours，真实allocation累计|
| teacher Stage1/Stage2 |**均为0**|
| branch reset/replay/teacher后suffix |**均为0**|
| 训练、学生评价、额外任务/重试 |**均为0**|

第5步只保存S5 checkpoint；source仍按原P0合同继续到正常停止或H50，以得到真实Y0。source在d5之后的动作继续计入source，不等同于teacher之后的branch suffix。不能在d5截断source后把未知终局填失败。

这些是分别生效的上限，不是完整96一定能完成的承诺。16M输入或4 device-hours先触及时，应保留BUDGET_STOP/INCOMPLETE；不补额度、不释放未知成本为零、不填造失败。GPU占用包括资源仍分配时的装载、等待、环境处理、记录和清理；不能跨阶段或进程清账。模型工程测量若另行进行，其固定范围与成本另记，不能伪装成免费的source预检。

实现应只有source允许路径，所有teacher/branch/学习阶段在真实外部调用之前被拒绝。不是在完整teacher驱动的文档上仅写一句“不调用”。支持协调方先安排最小source-only实现；**完整teacher、训练、评价桥接不应成为本阶段启动的前置工作**。

## 3. 实验结果与停止边界

- 全部96 source正常闭合、Y0和S5去向可认证后，再计算E/F/S；保留原Q≥72、C≥24、neutral≥24与家族必要条件，不降门槛。
- E仍必须是完整Q的保守上界，基于真实d5后的snapshot、done/truncated、完整map和停止原因。第6次解析失败但已有有效S5的task不能因L=5被漏掉；unknown不能当0。
- 必要上界不足记 `COMPLETE_SOURCE96_STRUCTURAL_NO_GO`，保存全部96 source及费用；所有YT=NA，没有teacher失败样本。结论仅为当前固定配方被source必要条件否决。
- 全部上界足够仅记 `SOURCE_UPPER_BOUNDS_NOT_FUTILE`，source-only入口随即结束。不能自动创建branch/reset/replay/teacher单位，也不能把已取得Y0当作teacher/训练授权。
- 技术、身份、完整性或预算失败各按对应STOP保留原件/open状态；不能把不完整96称为完整结构性否证。没有新source重跑、任务替补或第二种d试赛。

## 4. 仍需闭合的实际启动条件

本评审认可的投资理由已经成立，剩余门槛应是具体且可验收的工程条件：

1. 新source-only版本绑定原A96身份、冻结P0/提示/解析/H50及新d5规则；在新结果前固定task-local seed/pool初始化、顺序、输出与输入/协议hash。它不使用旧v1四位置矩阵或已消费release来冒充兼容。
2. 最小生产路径能可靠保存S5、正常source终局与独立source seal；独立auditor可重算物理费用和E/F/S，并拒绝teacher/branch调用、漏源、unknown归零、source预算绕过或错误停止分类。exact-SHA软件审查需覆盖这些边界，但本轮没有测试。
3. 真正可信的执行身份与严格GPU所有权核验成立；冻结8B/P0的装载和source所需资源有新、有限且可追溯的工程证据。无需为source-only验证不执行的teacher路径。已有旧失败/非零设备费用和已消费授权保留。

协调方新报告当前forwarded SSH agent路径不存在、没有可信宿主视图/能力。本轮没有检验该基础设施，因此只把它作为协调方报告，不声称独立测成。修复已有认证入口是合理解阻方向；未知PID白名单、猜测宿主PID或放宽身份检查不构成修复。

这些工程步骤可在用户已经授权的持续推进范围内由协调方安排；本报告不增加重复用户确认要求，也不将未知C24重新列为工程启动门槛。工程条件未齐时仍不能宣称已开始实验。

## 5. C01/C02 附录的独立结论

审查文件：`/home/lizening/research-notes/agent-logs/2026-10-26T095405Z__CODEX__si-p3-v2-C01-C02-clarification__ed7dbe04/C01_C02_CLARIFICATION_ADDENDUM.md`，SHA256=`e350b1de383d7b2dac228f052916ca70ff70b9473438cffd8f14bb5d074a72e5`。

- **C01关闭**（第19–23行）：学生不得接收诊断；teacher Stage2允许同一S5上Stage1的diagnosis/subgoal与stage_one_valid。Stage1 invalid仍保留固定Stage2诊断调用，但不执行teacher动作、YT=NA。它修正了之前负向验收条目的冲突，没有改变冻结teacher。这是完整v2的文字澄清，绝不让本次source-only获得任何teacher调用额度。
- **C02关闭**（第27–40行）：9/6/4/2/3是C臂C24配额和B臂同family新例总量，B仍从整个B_pool一次匹配抽取；至少8neutral意味着B中C类及与所选C24交集均至多16。不要求B含全C、不增加逐family neutral条件、不改为neutral-only。
- **叙述hash更正已核实**（第15行）：当前 `NEXT_STAGE_DESIGN_TASKS.md` 文件SHA确为`12e312be741343e9998f331bad5a9a3b5ddb09df4444a0e47fd0cf869214fdd5`。本轮只验证该文件字节hash，没有重审其全部任务内容，也未重新核对附录提到的旧INPUT_BINDINGS JSON。

没有发现附录仍需阻断的内容。仅接受以上澄清，不以附录自动采纳完整v2。附录第44行的旧NO_GO/投入未闭合状态应保留为其交付时状态，并由本次新source-only投入决定显式更新当前适用范围。

## 6. 交接

给协调方的结论：**可继续最小source-only实现和实际执行条件准备；无需事前证明C24；当前没有launch clearance。** 完整teacher/训练/评价维持未放行。报告、决策和证据hash仅写本轮唯一目录，原件不改，共享INDEX/根清单与统一发布仍由Sol Designer负责。
