# 独立设计复核：source-first v2与C候选稀缺

**结论：当前NO_GO优先。v2仅为待审、不可执行设计；工程通过不自动放行96采集，更不放行训练或600评估。v1冻结原件不变。**

本复核仅用标准库描述已消耗旧source，静态读取已执行2da提交的代码；没有导入项目模块、执行validator/analyzer、测试、模型、环境、CUDA或SSH，没有读取teacher/恢复结果或新task正文。后续核验未改先前历史reachability审查；本交接仅新增本文件。root的独立source-outcome统计与本复核一致。

## 静态成功语义及精确旧数据

旧source JSONL没有顶层success字段。已执行提交 `2da980f631badc25086d12db60d128ff507d3ae6` 中：

- `src/trajectory/trajectory.py::Trajectory.succeeded` 定义为steps非空、末step.done真且末step.reward>0。
- `scripts/run_r19_experiment.py::_build_source_candidates` 使用同一done/reward>0谓词判定source成功；不是用轨迹长度推断失败。
- source生成路径将真实transition.reward/done写入step；`src/env/alfworld.py::step`将底层rewards/dones直接转为float/bool。

静态读取的完整文件SHA256：trajectory.py=`31bbd35c7960ddcf87c6d1c38376d10aaf95e741f9dedecbe4f8e23a97fdb958`；alfworld.py=`086a4a6fc7aac6250230ceeb5f1fa2f198ef4d529bc5af6c476181cd1c7f959d`；run_r19_experiment.py=`06bb8e11c3cc9e9484b8d5731c86690b97a4c445a0e5aa16b72b912c6c14dd5c`。这些是Git对象静态读取，不是重新执行。

| 旧source口径 | N | source成功 | source失败 | d5可达失败：C的最宽上界 | d5可达成功：neutral的最宽上界 |
|---|---:|---:|---:|---:|---:|
| 全部 |127|120|7|7|110|
| 非light |120|114|6|6|105|
| pick-place |30|30|0|0|21|
| clean |30|28|2|2|28|
| cool |30|28|2|2|28|
| heat |30|28|2|2|28|
| pick-two |0|NOT_PROVEN|NOT_PROVEN|NOT_PROVEN|NOT_PROVEN|
| light，单列排除 |7|6|1|1|5|

失败source行号为4/7/10/24/28/62/125，其中第10行是light；全部末step.done=true、末reward=0，合法已执行动作数50。其余120条末reward=1且done=true。原件前后SHA256均为 `c6f37a7da28e326c70818524c79c17bbd85a286754c111f17db07cbe151a4f1c`。

**早cutoff主要解决可达性，不解决原actor失败候选稀缺。** 这6个非light失败source在d5/10/15/20均可达。因此即使旧队列上的teacher全部成功，C也至多6，而不是24；旧pick-place没有失败source。不能从d5的111/120可达率推导学习数据已接近充足。

以上只描述已被选择的开发队列，不能外推新96失败数、C yield或通过概率；pick-two尤其无历史证据。它足以要求重新审视投入理由，不能当作新96必败证明。

## v2 source-first方案的条件性正确性

全96 source封存后，以保守的source-only集合E判定是否有可能达到Q72及家族22/17/10/6/7，E且Y0=0是否可能达到C24及9/6/4/2/3，E且Y0=1是否可能达到neutral24同家族配额，逻辑上是有效的必要条件检查。只有在上界已不足时取消整个teacher阶段；通过后必须对全部预设可达任务各运行一次teacher，包括Y0=1。这不是按失败状态只挑teacher任务的选择器。

E必须覆盖所有仍可能满足Q的状态。旧队列的L>d规则依赖仅末动作terminal；未来若正常parser/selection-stop留下非terminal动作前状态，不能机械地因缺少已执行step6而排除。应依实际完成的5个动作、done、已记录map和来源合同定义；技术missing单独STOP，不能填Y0=0或擅自缩小E。

source-futility取消时YT保持NA并标记TEACHER_NOT_RUN_SOURCE_FUTILITY；仅有source数据，不是完整配对集，不能估计恢复成功/伤害率或宣称C为零。该资源guard必须先验冻结，不能看到新结果后改阈值、补task、延长N或追加384。

## 预算与仍需闭合的工程合同

纸上上界正确：4800 source +192 teacher +4224 suffix=9216 generations；输出tokens为149760。环境操作4800 source +480 replay +96 teacher +4224 suffix +192 reset=9792。16M输入和4device-hours仍是硬停止帽，不是完成预测；source-futility最多省去teacher/replay/suffix阶段，并不退还已花source成本。

source-first改变执行顺序，未来必须证明teacher阶段重放绑定原task/game、seed、reset-order/counter和环境版本，而不是使用当时全局reset计数。不能为凑counter加入未计费reset或重新生成CONTINUE。只有精确绑定源prefix后才能复用原Y0作为局部反事实对照。

若后续仍考虑v2，应先由Astra/root判断是否愿意为“很可能先暴露数据不足”的source-feasibility问题投入，而不是以d5高可达率为学习配方背书。当前不建议把工程就绪与96采集、C24形成或成功率提升打包成承诺；统一封存后不再扩展本核验范围。
