# 启动 worker 前失败：受控重启独立审查

**结论：接受一次新的受控工程重启方案，须落实以下计时口径及新放行条件；本记录不是 launch clearance。无需重复索取人工批准。**

## 失败与科学边界

提案 SHA 与原始清单8项均匹配。CLI真实退出1，stdout空，stderr为父目录缺失造成的 launch_claim.json FileNotFoundError，单调时钟耗时21.601499736秒。原始失败证据不可修改。

在 exact `f1e0d56a1be2a65876bbec5b8950fb76cda3eace` 中，supervisor_core.py:26 写claim，27建输出，43写context，54才Popen。本次已经进入supervise_core，但在26抛错且未进入52的try/finally；结合原始路径检查，可确认没有启动worker，没有执行其模型加载、显式probe、生成或环境单元。不能称CLI没有执行，也不能将未观察到的GPU分配/峰值写为实测0。

父目录当前存在、UID2000、可写可遍历、被Git忽略；旧output/claim仍不存在，实际源worktree保持exact且干净。仅修复该父目录不改变科学处理，也不产生新的结果选择。旧clearance已消耗，永久不可复用。

## 人类授权

已通过原任务只读消息接口核对真实用户消息：“行，你来持续进行这个任务，直到开始实验”；“继续做真实运行适配和 GPU 资源核验……你负责统筹和独立审查”，以及后来继续核验并推进实验的要求。消息ID见 HUMAN_AUTHORITY_EVIDENCE.json。这些任务授权覆盖原预算内的常规启动前恢复；结论不以FullAccess权限设置代替用户意图，也没有虚构新的批准。

所核对的相关用户消息没有针对本工程family的不可再启动限制。family=1是Root原clearance所设，Root可在新记录中明确改为总共2次：已消耗1次、只剩1次。每份实际authorization的maximum_launches仍为1，不能改为2。旧R19 one-successor及其他科学限制不受影响。

## 预算与必要条件

1. 旧CLI按向上取整22秒、一个设备保守扣费；新authorization的seconds≤578可由现有代码直接收紧，无需改源码。模型load/probe/生成各1、构造/close各1、reset1+saved steps6、8192输入/16输出等合计上限保持原值。历史其他工程与smoke费用另行保留，不清零。
2. 精确口径为 **22 + 新supervisor实际区间≤600秒**。CLI在main入口即记起点，鉴权/文件核验耗时包含在578内；解释器/模块启动在此前，最终报告读取/CLI退出在supervisor回执之后。因此不能宣称两次完整CLI端到端总时长≤600。新完整CLI耗时也须原样留证，外侧差额单列，不与重叠supervisor费用重复相加。若未来要求端到端硬限，需另有外层控制；本案按原supervisor计费口径接受。真实超限或清理不明不得裁剪数字后PASS。
3. 新auth/run/output/claim/clearance身份，明确旧失败与family计数、22秒扣费；新cap及argv/env/有效期绑定，重新做零科学预检并独立核验后才可由Root发新exact放行。旧预检只作历史证据。实际输出与claim须仍全新，parent就绪；源/输入/资源合同及科学语义不变。
4. 第二次无论何种失败均停止，不自动重试、补样、追加probe或提高限额；只清理自身进程，保留原始返回、开放单元与真实费用。本方案不放行A96、teacher、训练、评价或任何科学续跑。

本轮仅静态文件/Git及原始人类消息核对；新增项目运行、测试、CUDA/model/env/SSH/预检/源码修改均0。
