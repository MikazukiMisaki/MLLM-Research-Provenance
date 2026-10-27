# 框架默认环境修订：聚焦裁定

**条件接受新的工程协议修订；既有任务授权足够，无需新人工批准。本记录不是第三次运行的放行。** 旧family=2方案已耗尽，旧clearance不可复用；先前“第二次失败即停止”的要求已执行，不能将本修订描述为旧许可内续跑。

**技术与科学依据。** 提案及引用原件哈希匹配。第二次真实rc1，10条事件保留model_load/probe各一次失败预留；CUDA已初始化、UUID已观察。exact f1的顺序为init→UUID→configure→one-byte→Qwen加载；失败在完整环境比较，故尚未到显式one-byte、权重、生成及环境调用。allocator限额和显存门槛也尚未验证；报告的resource_rejected=false不能当PASS，因为validated_resource_samples=0。

固定PyTorch源码317–319行在缺键时写入CUDA_MODULE_LOADING=LAZY，旧auth确实缺该键。预先声明同值可消除此项必然冲突；保持完整环境guard，不采用豁免或过滤键。CPU导入诊断仅覆盖其无CUDA初始化的进程，不能证明失败现场只有这一差异，也不保证修订后成功。此变更纠正工程环境声明，无新的科学输出选择或模型/任务/解码调整。

**授权判断。** 本会话此前直接核对的真实用户指令包括“持续进行这个任务，直到开始实验”和“继续做真实运行适配和GPU资源核验……你负责统筹和独立审查”（原始ID及摘录已绑定）。这些具体任务授权覆盖原科学范围内的窄工程适配；family/预留限制来自Root方案，所核对人类消息未设本family不可修订的一次性上限。本次独立接受新增工程预留，不把前次仅限pre-worker的裁定自动外推，也不以FullAccess当预算豁免。旧R19及科学限制不变。

| 项目 | 修订后family上限／状态 |
|---|---|
| live CLI | 已用2，最多3，仅剩1 |
| model_load、context_probe预留尝试 | 各已失败1次，合计各最多2；绝不退款或清零 |
| 实际CUDA初始化 | 已观察1次，再次执行可能增至2次 |
| 实际权重加载／显式one-byte／生成 | 各最多1次，前两次均未到达 |
| 环境调用 | 构造/reset/close各1、saved steps6、reset-inclusive7 |
| token及科学范围 | 8192输入/16输出；无A96、teacher、训练或评价放行 |

**计费成立：** 22＋ceil(67.34844062384218)=90秒已扣；新supervisor≤510秒，合计≤600。第二次真实0.018707900173289493设备小时原样保留，stage区间不重复相加；全部CLI时长另列，不声称完整CLI生命周期总计≤600。其他历史工程及smoke费用不抹去。

**放行前条件：** Root另立明确修订并绑定本结论、两次失败、计数及90秒扣费；新auth/run/output/命令/环境/有效期，实际env只增加LAZY且其余绑定不变。每份新authorization仍maximum_launches=1、model_load/probe各≤1、seconds≤510，不能把family的2填入单次cap。保留两个旧claim/撤销标记。完成新零科学预检和独立exact放行后，才可由执行者启动一次。任何再次失败按原guard停止，保留真实开销和未完成单元；本裁定不授权进一步延长或自动修订，成功也不自动放行source。

本轮仅静态阅读、元数据及哈希核对；未运行测试、导入项目/PyTorch、执行CUDA/model/env/SSH/预检或改源码。
