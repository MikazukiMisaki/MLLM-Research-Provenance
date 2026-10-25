# SI-P3 独立审查与投入决定

**可以继续self-improvement研究主线；当前只支持一次固定96任务采集可行性研究的有条件投入候选。完整学习/600评估投入NO_GO_NOW；本轮设计审查不是执行许可。** 新增模型/环境/tokenizer/训练/项目validator/pytest/preflight/G2/G3/G4均0，R19历史5142/7949保持。

最终规则见MINIMAL_CONTROLLED_EXPERIENCE_PROTOCOL.md；精确字节及证据见phase3_independent_review.json。这是协调方独立收敛结论，不以作者自己的设计/测试结论替代，也没有将未执行的预检、实际token匹配或学习效能写为PASS。

## 最重要的独立发现与决定

1. **容量约束实际改变总体。** known-use2612以外支持TRAIN1141，但light仅2。初稿六家族均衡配额不可行。收敛五非light、96采集/48接口身份预留/600最终身份预留/395不运行；另2light不运行，74官方unseen不使用。全部1139行与原Luna各身份/rank/hash/Hamilton配额由协调方独立重算；600与48身份保持，384归还余量。任务隔离不是场景隔离；final600的103numeric-suffix代理与旧known-use重叠，不作heldout/新布局结论。
2. **完整池、事前anchor与共享物理账。** 每task一个预先d，均衡5/10/15/20总各24，不看未来标签；source只一次，CONTINUE复用，reset+exact replay后一次teacher首动作+原地P0suffix。不能直接拿旧多K运行器执行后宣称满足新账。Q对称，B包含C，未执行teacher没有YT终局标签。独立七个Hamilton规模/五×四cut矩阵与预算公式匹配。
3. **方法主张有限。** C在success-only B中恰等价baseline失败筛选。未来两项C>A/C>B可支持固定共同池/剂量下的采纳配方，不识别独特价值算法。真实动作有效不等于它的学习信用/泛化。既有oracle5.56pp不是预期新学生效果或功效先验。
4. **小剂量的可构造性不同于数据充分。** 96后一次检查Q≥72、C≥24、neutral≥24及家族/覆盖/实际token/contrast门槛；B一次匹配抽样仍允许C入选，协调方另要求实际B中≥8neutral且不与C相同，失败不重抽。C24+S120、2epoch/18updates，每新task最多2曝光。24个首动作只得到48次展示，是高风险小剂量，不是已证明的有效剂量；mask/exposure PASS也不能预测transfer。通过这些guard只能返回下一次有清楚成本的投入判断，绝不自动训练/评估/加384。
5. **预算有硬帽也有未闭合处。** 单次96计划8496生成/9792含reset操作/138240输出tokens；累计输入16M、每call输入8192、GPU占用4device-hours为尚待工程验证的投资帽，非实测完成预算。现存config maxcontext40960仅证明理论帽未越界。smoke/dev/训练不隐藏在采集里，当前预算0；旧8999 debit/消费过clearance不转移。
6. **600不保证5pp验收。** 两项W−L≥30/L≤30已使p≤.00206；真正约束是价值和伤害。假设真5pp、true harm2.5%的单pair完整数值验收概率约52.3%，两项联合不独立，且不含数据/软件门槛。为24标签自动支付90k次生成的最终评估不合理；先解决有界数据/工程可行性，保留最终任务不用于调参。

## 独立工作与证据范围

协调方独立读取注册身份及候选metadata，重做partition/order/家族容量/scene代理/原生产trainer与prompt接口的静态检查；另写纯stdlib数学与元数据核对，不导入项目模型/parser/analyzer/validator/tokenizer。真实subprocess receipts均保留。回查G3四份原始大文件SHA与冻结值相同，科学三worktree/远端85与2da refs无漂移。正式pytest/模型/环境检查不在本轮范围，未运行。

Sol Research提交共同池/剂量/负向及一次96建议，初稿六family前提被容量否定后追加五family版本，旧字节保留。Luna提交identity-only分区/预算，独立重算接受其实际metadata数学；三个input path转录漏agent-logs、一个人工stdout转录错误及其erratum开头的错误否认均明确保留并由协调方给出正确绑定。实际原build tool receipt经read_thread独立回收为exit0，和完整proposal一致。这些记录异常不被隐去，也不被扩大为科学数据失真；详见LUNA_DELIVERY_REVIEW.md。

另有独立方法critic审查协调方协议，支持DESIGN_REVIEWED_WITH_LIMITS/NOT_EXECUTABLE，并要求明确累计prompt-token ratio和共用paired slot顺序；均在冻结前补齐。模型/tokenizer/训练未运行，所以EXPOSURE_CONTROL仍SPECIFIED_NOT_VERIFIED，新IMPLEMENTATION_REVIEW为NOT_APPLICABLE。

## 明确停止与下一步

不改变现有冻结baseline、teacher/prompt/greedy/H50/K1或训练超参来凑结果；无自动retry、换task、扩K、controller学习/记忆/DPO/RL/多轮或新环境。技术漂移、缺receipt、错误命令、replay不符、预算将超限或外部操作不完整即整runSTOP，原证据/退出/已花成本保留，不把incomplete改taskfailure。预期科学invalid/早终止保留原分母而不补样。

下一步只应按最终协议补齐新增single-K1 collector、P0 continuation/final18、实际tokenizer/EOS/loss-mask与资源计账等工程合同，并完成独立exact-SHA审查。当前没有派发实施/启动，也没有建立gate/clearance。未来任何明确放行必须基于其具体冻结实现与剩余科学范围；full access不把设计变成已启动科学运行。
