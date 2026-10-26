# 旧 source 固定 cutoff 可达性：只读设计风险核验

本检查仅描述已消耗的 G3 source 原件，不是 G4 重跑、新实验、项目 validator/analyzer 或新96采集预测。只用 Python 标准库读取 JSONL；未导入项目模块，未调用 tokenizer、模型、CUDA、环境、测试或 SSH。只新增本方法和同目录 `historical_reachability_audit.json`，未修改冻结协议、旧原件或任何 schedule。

## 输入与边界

输入为 `/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z/source_trajectories.jsonl`，127条、19,726,633字节。原件审查首次读取、最终计算前和最终读取的 SHA256 均为 `c6f37a7da28e326c70818524c79c17bbd85a286754c111f17db07cbe151a4f1c`。只输出 schema、动作数、终止位置、家族和布尔一致性统计；不输出 prompt、observation、task正文、任务路径或命令内容。不读取或使用 teacher/恢复结果、reward 或成功标记来选择 cutoff。

原件没有顶层 `states` 数组，而是 `initial_observation` 加逐动作 `steps`。每个 step 包含动作前 `observation`、`valid_actions` 和 `metadata.action_selection.id_to_command`，以及动作后 `result_observation`、`done`、transition引用等。

127条均满足：index从0连续；首个动作前observation等于initial_observation；相邻step的动作后/动作前observation相等；仅最后step的done为真；trajectory和transition均未truncated；generation/transition引用列表与逐step引用相同；全部2046个step记录为合法selected动作。该文件中的完整动作记录支持将L=len(steps)解释为“日志记录的已完成动作数”，但本检查未重新核验外部物理事件或真实环境。

cutoff d定义为已完成d个动作、准备选择第d+1个动作。零基索引应读取 `steps[d]` 的动作前状态，并与 `steps[d-1].result_observation` 对齐。因为所有轨迹都仅在最后动作done，必须 **L>d**；L=d时最后动作已经terminal，不能用L≥d计为可执行状态。还检查该动作前observation/命令map非空、map值的顺序与valid_actions一致、原记录动作对应map中的合法ID、此前未done。所有满足L>d的候选都通过这些本地schema一致性检查。

本地日志足以支持“记录中存在非终止、含合法动作map的下一动作前状态”。它不证明重新reset/replay后的状态等价、完整公共H4/map/prompt投影绑定、真实运行版本、训练2048 fit或完整Q资格。这些项保持 **NOT_PROVEN**；历史可达性只是完整Q的必要条件上界。

## 描述性结果

| 家族 | 旧source数 | d=5 | d=10 | d=15 | d=20 | 四d等权可达比例 |
|---|---:|---:|---:|---:|---:|---:|
| pick-place |30|21|7|4|2|28.3333%|
| clean |30|30|19|12|7|56.6667%|
| cool |30|30|23|13|10|63.3333%|
| heat |30|30|26|12|3|59.1667%|
| pick-two |0|NOT_PROVEN|NOT_PROVEN|NOT_PROVEN|NOT_PROVEN|NOT_PROVEN|
| 五家族口径、light排除 |120|111|75|41|22|51.8750%（仅四个有观测家族的旧mix）|
| light，单列且不纳入目标口径 |7|6|3|2|1|42.8571%|
| 全部旧source |127|117|78|43|23|51.3780%|

五家族口径必须明确其中pick-two没有旧source，不能把0/0写为0%失败或据此声称已估计完整新五家族分布。原旧队列已被选择、家族构成与新96不同，未知选择过程及跨队列可交换性限制仍然存在。

等权计算为 `sum_d count(L>d and local_state_evidence)/(4*N)`。全部127条为261/508；排除light后的120条为249/480。若仅在这个固定旧队列上给每条独立、等概率分配四个d，其期望可达source数分别为65.25/127和62.25/120。这些是历史等权平均，并非某个确定分配的最大可达数；不保证实际balanced固定分配会等于该均值。未生成旧或新task的d分配。

若误用L≥d，非light会得到272/480=56.6667%，多计23个已经terminal的source-cutoff组合；全部source会得到287/508，多计26个。终止边界不能忽略。

## 与Q≥72/96的联系及投入意见

冻结配方要求96个计划slot至少72个Q有效，即75%。Q需要先有可恢复的非终止动作前状态，还需通过replay、完整来源、合法teacher动作、终局和训练序列等额外条件；这些额外条件不会增加可达数。

历史非light等权可达平均51.875%本身明显低于75%，且较晚的d15/d20只有41/120和22/120可达。因此，**采集前值得由协调方与Astra复审fixed-cutoff设计与Q门槛是否协调；不能再以工程PASS作为数据可行性的理由。**

这不是新96的Q预测、成功率预测、失败概率或硬上界，不证明新96无法达到72。没有将旧率外推为新96期望人数，没有给出把旧选择队列当iid新样本的置信区间，也没有用teacher/恢复效果挑d。完整新五家族可达性因pick-two缺失尤其未获证明。

本核验不改变冻结协议、不推荐具体替代d、不生成新schedule。若保持原设计，应明确接受可能因结构性不可达而NO_GO的投入风险；是否在新数据前另立版本化设计属于后续独立决定，不能借本报告自动调整。禁止根据新结果补task、改anchor、延长N、追加384，或将未达门槛重新解释成通过。
