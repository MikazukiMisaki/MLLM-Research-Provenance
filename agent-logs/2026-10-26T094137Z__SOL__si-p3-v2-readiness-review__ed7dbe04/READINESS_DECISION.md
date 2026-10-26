# SI-P3 v2 当前启动条件独立审查

**EXPERIMENT_READINESS=NO_GO。当前不能启动正式source采集、teacher采集、训练或评价。** Sol Research已完成的是v2候选设计交付；没有新的实现SHA、真实GPU工程成功结果或采集release。

## 本次实际核对

评审工作树保持clean，agent/codex-r18c2 / e537f441010077123a307e9d50ea40cf8dad8547。工程工作树clean，codex/si-e2-cuda-uuid-compat / 844cc4b78df1f83e29391ffd5ab861a2d0c0a3fd；本轮活跃远端ref与本地一致。Provenance审查开始local/origin/live main均45631b5bb8a45885f74c54c03a3f6907823f7309。无新科学代码或实验结果。

通过真实app线程读取了Sol Research、Luna及Astra最新公开交接；根协调方直接核对新包，而非采用开发者自己的PASS。Sol包路径为 ../2026-10-26T091852Z__CODEX__si-p3-v2-source-first-design__cec2ce5a/；18个选中文件的字节数和SHA256及本地18行hash清单全部匹配，另2个辅助清单保留原字节。三份主文已读；现collector/contract关键静态门禁再次核对。内部设计critic和执行critic分别独立审查了文档与本地执行状态；执行critic未查远端，远端由root独立查验。

## 已完成的设计进展

候选的全d5、先source后branch、S5在第6次生成和source终局前冻结、正常parser-stop边界、E/F/S必要上界、unknown不当0、YT未测为NA、保留全部96分母、B_pool包含C但B24可以不包含所有C24等逻辑基本自洽。它仍是未采纳、不可执行的草案，不能称完整协议PASS或实验就绪。

预算独立核对：完整9,216 generations /9,792含reset环境操作 /149,760输出tokens；source-only最多4,800 /4,896 /76,800。16M累计输入token和4device-hours是硬停止帽，不是完成预测；本轮没有实际资源测量。历史科学累计仍5142/7949，新科学调用0。

文档在采纳或实施前必须澄清以下两点，不修改已封存作者原件。总体文档状态为CHANGES_REQUIRED_BEFORE_ADOPTION；这不是新发现的生产运行失败：

1. 配额表的“各臂选中C数”应理解为C臂的C配额及B臂匹配的family总数。B24至少8neutral，因此不能要求B24含全部C24。
2. 实现缺口文档负向测试第14项把诊断进入teacher输入也列入禁止，和冻结两阶段teacher冲突。不得泄漏的是未来终局及私有诊断进入学生公共输入；冻结teacher的Stage1→Stage2合法诊断/子目标传递必须保留，不能误删以“修复泄漏”。root与内部critic已独立指出，Astra的新静态审查也确认这一处冲突。需用明确的新版本/附录限定正确边界，不能按该矛盾文字开始实现。

## 尚未满足的实际启动条件

1. **投入理由与候选版本未采纳。** 必须有足以承担source96本身成本的理由；d5提高可达性并不产生更多Y0失败。新96至少需24个可达失败，且各家族满足9/6/4/2/3，随后还须teacher成功/Q/去重。旧6/120既不能证明新96够，也不能预测必败。不能降低门槛、增加N或换任务以绕开这个判断。
2. **真实两阶段采集驱动与审计未实现。** 当前Collector仍synthetic-only、逐slot source→teacher；版本/caps/auditor也沿用v1。source-first、独立source seal、事件/预算顺序与真实seed/pool/reset-counter复放均未完成新exact-SHA验收。现SI-E2四调用工程CLI不能承担96采集。
3. **可信执行身份与真实8B/P0资源证据缺失。** UUID软件兼容已接受，但宿主NVML PID到容器PID映射仍未证明；没有新的可信执行入口。真实权重装载、显存/耗时及旧已用轨迹经新桥接的运行证据仍未获证明。旧探针的已消耗边界保持不变，不重试。
4. **Luna的登记身份交集证据已在本轮补齐。** 本次初查09:41UTC时其091005目录为空，只有旧状态确认；续办后收到5份交付及清单。root逐一核验15个输入hash并独立做元数据集合连接：R19旧127∩A96=0、旧127∩expert_train=0、旧127∩S120=0、A96∩S120=0、A96∩已登记known-use2612=0；S120的120个身份全部在expert_train。P2的169个独立身份及R19-K1的39个身份也不与A96/S120相交。这支持登记task/trial互斥，不证明scene/语义隔离或未登记历史浏览不存在，更不证明C产率或运行就绪。旧R19与expert_train零交集也意味着不能把旧成功率高简单解释为这些精确task已用于专家训练。

## 已继续的工作与边界

Astra的最终独立审查现已收到并核验3个宣告hash及7行清单；结论为DOCUMENT_REVISION_REQUIRED，指出相同teacher边界冲突，其余逻辑无实质问题。Luna的最终登记身份交集和预算证据现已收到并独立核验，但可信执行能力没有新增。root已把最小文档澄清附录实际派给Sol Research，要求保留原件、不改代码/测试。附录之后再决定候选版本和投入，不自动进入实验。

另有一项叙述性hash需澄清：Sol主文/RECORD引用旧任务hash511431...，当前提交的任务文件实际为12e312...。root核对其before/after输入绑定发现二者正确保存了当前12e312...，故不是实际输入校验伪造；需在新附录如实说明旧叙述摘要不认证当前字节。当前task的授权范围仍仅文档/静态证据，不存在因此新增的运行权限。

本轮仅文件、Git、app和标准库hash/算术审查；无模型/tokenizer/CUDA/NVML/环境/SSH/测试/preflight/launch/采集/训练/评价。原G2/G3/G4及所有失败原件不变。本记录不设launch clearance，不发科学执行指令。
