# 位置已知／未知时的自生成诊断与动作

按[事前协议](DIAGNOSIS_LOCATION_OBSERVABILITY_PROTOCOL_V1.md)，在四组研究者构造的双物体情境中，各向同一个模型提供一次位置已知和一次位置未提供的题面，并分别生成诊断、子目标及动作。一次运行完成 **8 次第一阶段、8 次第二阶段**，工具退出 0；八条第一阶段格式均有效，八次动作编号均映射成功。每对提示的其余文字及动作映射由执行者核对一致。下表为模型实际输出的完整诊断、子目标和映射动作；不含环境执行。

| 组别 | 位置条件 | 诊断 | 子目标 | 所选动作 |
| --- | --- | --- | --- | --- |
| 1 | 已知 | Missing mug 2; cabinet is closed preventing access. | Open cabinet to retrieve mug 2. | open cabinet |
| 1 | 未提供 | Missing mug 2; cabinet closed preventing access. | Open cabinet to locate and retrieve mug 2. | open cabinet |
| 2 | 已知 | Basket has one book, drawer is closed, inventory is empty. | Open drawer to access book 2. | open drawer |
| 2 | 未提供 | Book 2 location unknown, basket has only book 1. | Open drawer to locate and take book 2. | open drawer |
| 3 | 已知 | Missing spoon 2; cupboard is closed and not accessible. | Open cupboard to retrieve spoon 2. | open cupboard |
| 3 | 未提供 | Missing spoon 2; cannot complete task without it. | Open cupboard to locate and retrieve spoon 2. | open cupboard |
| 4 | 已知 | Missing towel 2; closet is closed and inventory is empty. | Open closet to access towel 2. | open closet |
| 4 | 未提供 | Missing towel 2 and inventory is empty. | Open closet to locate and retrieve towel 2. | open closet |

## 诊断和动作的限定判断

八条诊断均没有以明确句式直接断言「第二件在某处」，所以没有可按预定位置规则判为支持、矛盾或无依据的明确位置断言。未知条件中 1 条直接说位置未知，另 2 条未说位置；第 1 组未知诊断说柜子关闭导致无法取得，若“取得”的对象指第二件，这一因果关系在题面中没有依据；若仅指柜内访问，则未必如此，故记为 **1/4 存在需解释的隐含位置／因果歧义**，不计作明确错误。已知第 3 组“不可访问”也可能指柜内不可访问或柜体本身不可接近，不能据关闭状态断言后一种解释。`Missing` 可指尚未完成或尚未找到，单凭这个词不判断物体实际位置。

研究者将八个子目标均解读为先打开相应容器，然后寻找或获取物体；八次动作均为对应的 `open`，与这一步一致。它们没有实际执行、寻找或拿到物体，不能称为完成整个多步子目标。四个已知／未知有效配对的首动作均相同；未知条件下选择搜索该容器仅是一项行动选择，不足以证明模型认定物体必在其中。

这是单一执行者对四组虚构文字的非盲语义判断，题面还明确告知未知条件位置未提供。固定顺序、不同句式和自然生成的子目标使其不能分离“信息可得性”的纯效应；不能由零个明确断言推断模型在真实状态中没有幻觉，也不估计总体错误率。其他诊断主张未逐项得到独立认证，真实环境的局部进展及终局仍未知。

## 核对及资源

执行者检查 8 对保存结果的 token 后缀与原始输出一致且以已记录 EOS 结束、动作编号映射与记录一致；核对 4 对第一阶段提示除位置句外逐字一致。语义判断和该核对均非第三方或异机复现，日志本身和解码依赖可信主机。实际 token 计数包括终止符，真实模型与配置依赖既有可信主机假设，未重算权重摘要。

本批新增 3,600 输入 tokens、268 输出 tokens；最长一次约 1.358 秒，进程自报至完成事件约 19.194 秒，用户／系统 CPU 16.253／5.316 秒、最大 RSS 4,659,736 KiB；离散整卡显存最高样本 16,198 MiB，不证明硬峰值或独占。系统 I/O、实际 GPU 峰值和人工成本未知。Git 忽略目录中的事件日志 SHA-256 `2feff33d3f00a258d1c5fae02baa69a973d063d5d743b8f77632b3ac6efaf9a4`；脚本和提示摘要见协议。不访问真实轨迹、方向 2 受限输入或受保护任务。
