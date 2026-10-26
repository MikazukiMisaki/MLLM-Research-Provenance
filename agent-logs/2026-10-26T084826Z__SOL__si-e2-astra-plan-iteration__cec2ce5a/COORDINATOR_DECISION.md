# SI-E2/SI-P3 与 Astra Main 讨论后的协调决定

**DESIGN_ITERATION_COMPLETE / COLLECTION_NO_GO_NOW / NO_NEW_RUNTIME_RELEASE。** 用户要求核对进展并与 Astra Main 讨论迭代；已通过真实应用线程发送简报、预算和逐轮证据，并收到 Astra 的审查意见。当前决定是继续设计与工程准备，暂不投入新96采集。冻结 v1 保留；固定早期位置 v2 只是待审候选，不能因工程通过就自动采集。

## 当前进展和独立核验

- 评审根目录、分支及干净状态符合约束：`agent/codex-r18c2`，HEAD `e537f441010077123a307e9d50ea40cf8dad8547`。
- 工程候选 `844cc4b78df1f83e29391ffd5ab861a2d0c0a3fd` 本地干净，活跃远端 ref 本轮再次核对完全相同。已有独立软件结果 953 passed / 3 failed / 77 errors，原80个历史失败/错误身份不变，新增70项通过；本轮没有重跑测试。这接受 UUID 格式兼容及证据持久化，不接受真实 GPU 运行。
- 当前缺少可信的宿主/NVML PID 与容器 PID 映射，实际8B/P0权重装载、显存/时延、旧轨迹经新桥接复放未获证明。实际96采集驱动也未实现；不能把 synthetic collector 与独立工程桥接拼称真实采集已经可用。
- 科学原始结果没有新增，累计仍为 5,142 generations / 7,949 含 reset 环境操作。旧5.56pp是开发前缀上的事后 oracle headroom，不是学生已取得的提升。当前尚未证明新经验蒸馏改善学生成功率。
- 本轮源代码修改、模型/tokenizer/CUDA/ALFWorld/SSH/测试/preflight/采集/训练/评估调用均为0。只读取既有原件、静态代码、Git/app元数据并作标准库描述性复算；未打开未使用任务正文。

## 本轮发现的两个设计风险

1. 旧120条非light轨迹在d=5/10/15/20处的非终止可达数为111/75/41/22；四位置等权描述平均249/480=51.875%。原配方却要求96中至少72条完整Q配对，即75%。这提示晚位置会消耗有效样本，但旧队列只有四家族，pick-two缺失；它不是新96产率预测、硬上界、功效或iid估计。旧日志只有末步done，L=d已经终止，不能误作下一动作前状态。
2. 按生产代码“末步done为True且reward>0”的source成功语义，旧127条为120成功/7失败；非light120条为114成功/6失败。四家族失败数pick-place/clean/cool/heat为0/2/2/2，6条在d5均可达。此处只读source，没有读取teacher结果。即使d5减少不可达，也不会增加基线失败数量，故不能解决C至少24且家族9/6/4/2/3的构造风险。旧队列被选择、与新隔离队列不同，这同样不是新96失败率预测。

root与内部独立critic分别复算得到相同数字；Astra阅读并审查这些统计及解释边界，没有冒称自己重新计数原文件。原source文件前后SHA256均为 `c6f37a7da28e326c70818524c79c17bbd85a286754c111f17db07cbe151a4f1c`。

## 收敛的下一候选及尚未解决之处

可另立v2草案：同96身份、家族35/26/16/9/10、任务隔离、同模型/提示/解码、H50和单K1原地交回，仅统一固定d5，并改为source-first。全部96 source正常完整封存后、任何teacher前，以保存的d步后公开snapshot/terminal/truncated/map和停止原因构造完整Q的保守可达上界E；证据unknown为完整性STOP，不能压成0。不能把旧L>d计数方法直接搬到可能parser-stop的未来运行。

若E无法达到Q72及各家族22/17/10/6/7，或E中Y0失败无法达到C24及9/6/4/2/3，或E中Y0成功无法达到neutral24及同家族配额，才记 `COMPLETE_SOURCE96_STRUCTURAL_NO_GO` 并省去全部teacher。YT=NA，标记TEACHER_NOT_RUN_SOURCE_FUTILITY，不称已完成paired采集、不填0。技术missing或预算未完成另记STOP。通过这些必要上界也不代表Q/产率或学习有效；随后所有预定可达任务含成功对照都须按原规则各一次teacher，不能只采失败者。

这要求独立冻结source-first seed/counter/reset/replay、原始证据、顺序、预算和审计合同，并审核实际驱动；不是现有软件PASS的自然延伸。不得补任务、改变d、追加384、降低门槛、重抽B或自动重试。B仍从包含C的共同成功池一次抽样，并保留至少8neutral、同token/曝光和质量要求。

v2完整上界经root和Astra分别复算：4,800 source +192 teacher +4,224 suffix =9,216 generations；含reset环境操作9,792；输出token149,760。比v1多720 generations/11,520输出token，环境上界相同。16M累计输入token及4 device-hours如保留，仅是更紧的投资硬帽，不是能完成的预测。source-only阶段本身最多4,800 generations，也是一项独立投入，不能称免费筛查。

**主要风险仍未解决：失败样本与C24是否足够，24个动作目标是否有学习价值。** 目前既不建议直接采v1，也不把v2排成默认运行队列。下一步只形成有版本的协议和实施影响分析，区分配方可构造与效能是否值得投入；训练及600任务评价继续NO_GO。论文问题收窄为固定早期单次干预经验的动作蒸馏；不声称adaptive stopping、错误触发恢复或跨阶段收益。

## 分工和依赖

具体设计任务见NEXT_STAGE_DESIGN_TASKS.md：Sol Research负责v2草案与静态实现差距；Luna负责旧/新队列可比性与预算、可信执行能力所需证据；协调方与Astra独立审查。两者本轮仅文档/旧证据，不修改代码、不调用设备或实验。不建立可执行gate或新clearance。

唯一顺序是：设计风险与版本审查 → 必要实现及exact-SHA独立验收 → 可信执行入口与有界工程测量 → 独立采集投入决定 → 实际数据/学习投入决定。不得借以前已消耗的探针或G3授权跨阶段执行。
