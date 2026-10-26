# SI-S01启动前最小工程验证方案（待exact-SHA审查，不执行）

科学source-only设计不需要验证未运行的teacher或训练路径。本方案用于证明新source actor/环境桥与真实P0输入、旧已消耗状态及设备资源兼容，独立于科学A96账本。当前没有launch clearance，旧任何探针授权不复用。

前提：可信宿主执行入口或完整可信host/container PID见证已成立；新source-only实现冻结、独立exact-SHA review通过；旧snapshot/P0/tokenizer及runtime/data/config哈希无漂移；工程输入/输出/argv/env/唯一run identity已具体准备并独立审查。缺一项不运行。

候选最小一次工程范围：cached tokenizer加载与冻结P0模型加载各一次；新source P0 producer在已消耗真实G3首source的原第一动作公开prompt上最多1次generation（cap16/input≤8192），保存实际IDs/mask、raw tokens/parser、真实PEFT before/during/after证明并与原公开map/选择证据核对；使用原first-source task/seed/pool绑定，最多1次reset+重放原6个已执行动作，逐state/map/ID/command比对，不生成新prefix、不搜索seed、不新增task。只读旧证据，输出新目录，不把工程调用归类为旧source科学unit重试。

总帽建议：1generation /7含reset环境操作 /16输出tokens /8192输入tokens /1模型加载 /1env构造 /600seconds allocated time；CUDA身份若需上下文，只允许一次显式1-byte probe并完整计入新工程记录。一次supervised invocation，异常或snapshot/parser/身份不符即停、不retry。所有实际工程CUDA及generation/environment成本单列非零，不能混进5142/7949或A96未来额度。构造/close另记，不当reset/step；现场证据不改。

这只检查固定旧输入和局部真实资源，不预测A96 prompt均fit、source96可在16M/4h内完成，也不证明新失败来源/学习效能。若旧first-source lineage或真实P0输入比较不能严格闭合，先返审，不换更易通过的旧样本。

本文件是root工程范围候选，尚未形成最终可执行配置/argv。实现可先提供strict gated验证接口；实际调用必须等新review和独立clearance，不因用户持续目标或本文存在而执行。
