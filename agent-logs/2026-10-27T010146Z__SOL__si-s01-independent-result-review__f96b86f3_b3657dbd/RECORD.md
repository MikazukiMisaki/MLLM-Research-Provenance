# SI-S01 独立结果验收与停止记录

正式 source-only 采集完整、真实并通过独立执行验收；当前冻结数据配方的结论为 **COMPLETE_SOURCE96_STRUCTURAL_NO_GO**。停止教师采集、训练、评价及补样；没有新的执行授权。

- Agent/task：Sol Designer（独立审查与协调），同一次 A96 source-only run 的运行后审计及原始证据发布。
- 审查目录开始 UTC：2026-10-27T01:01:46Z；审查完成 UTC：2026-10-27T01:10:41.461712Z。运行时间为日本时间 2026-10-27 09:26:37–10:00:22（UTC 00:26:37–01:00:22）。
- 科学仓库：MikazukiMisaki/Alfworld-Self-Improvement-Project；branch `codex/si-s01-shared-gpu-adapter`；开始与结束 SHA 均为 `f1e0d56a1be2a65876bbec5b8950fb76cda3eace`，工作树保持干净。
- 唯一 run：`f96b86f3391940eaa9d75040c444a8e4`；真实 supervisor/outer returncode 均为 0，cleanup=true、deadline=false，原 PID 882767/882823 已退出。没有重跑或自动重试。
- 真实完整数据：96/96 normal sources，96 trajectory rows，16,455 条连续哈希链事件，source seal 完成，0 failed/open units。
- 独立复算：固定解释器 `python -I -B independent_source_result_audit.py`，使用真实 production audit、独立资源核验、cached CPU tokenizer、生产编码/解析函数。重新核对 1,959 次生成的输入及输出，不构造模型权重、不初始化 CUDA、不构造/reset/step ALFWorld、不调用 collector/科学 CLI。真实 exit=0；复算报告与原报告逐字段相等，9 份原始输出前后字节 SHA256 不变。
- 软件测试未重跑。既有独立 exact-SHA 软件验收为 1,162 passed，已知 3 failures + 77 errors 与 baseline 的 node/phase/type 集合相同，无新增。此次独立原始结果核验不是 synthetic 测试结果。
- 成本：本轮新增 1,959 generations、1,164,593 input tokens、9,795 output tokens、2,055 environment operations = 96 resets + 1,959 steps；另有各 96 constructs/closes、1 model load。最终 supervisor 成本为 2,024.9118513343856 秒 / 0.5624755142595516 device-hours；不与 report 中阶段下界 0.5456197222185114h 叠加。
- 既有科学基数 5,142 generations / 7,949 operations 保留。本轮后已知科学累计为 7,101 / 10,004。另计已经完成的工程验证 1 generation / 7 operations，合并已知科学及该工程为 7,102 / 10,011；以前失败的 model-load/probe 预留及其他工程成本没有清零。
- 持有数据与隔离：仅固定 96 TRAIN、冻结 task/order/seed42/pool42/S5/H50/P0；没有 held-out、teacher、recovery、训练或评价；YT 保持 null。共享 GPU 资源契约不声称 NVML/宿主 PID 映射、独占、整体进程显存上限或任意 8192-token fit。

E 是可用 S5 checkpoint 数，F/S 是其中按原 source Y0 划分的失败候选／成功对照数。它们是资格子集，不能把 S72 写为全96任务成功数。E89 达到72且所有家族 E 下限通过；F17 未达24，另外四项家族检查未通过：

| 家族 | 可用 F | F 最低要求 | 可用 S | S 最低要求 |
|---|---:|---:|---:|---:|
| 简单放置 | 0 | 9 | 28 | 9 |
| 清洗后放置 | 2 | 6 | 24 | 6 |
| 冷却后放置 | 6 | 4 | 10 | 4 |
| 加热后放置 | 1 | 2 | 8 | 2 |
| 双物体放置 | 8 | 3 | 2 | 3 |

这是预注册的数据供给停止条件，未检验 self-improvement、teacher 或训练效果。共同质量筛选及真实目标长度匹配仍未测量；不能把 F17 直接称为 B_pool 数据量。按家族对原 source F/S 一一配对的 Σmin(F,S)=11 只适用于额外的纸上假设，**不是正式 B_pool/C 容量或新的验收门槛**，因为 B_pool 的构成包含 C 且另有长度匹配条件。

Sol Research 对报告、冻结协议及正式审查记录做了只读科学复核；其正式追加说明 SHA256 为 `b6cdc2ecb72d98748ee73f4a45e78881f059576b8a82619dbfd3d2cd60644793`，原临时解释保留。Astra Main 亦对已验收数据条件作出一致的停止解释；未将该讨论当作新实验批准。

原始输出9文件共474,608,517 bytes。Luna 确定性 gzip/tar 归档17,608,129 bytes，SHA256 `474a9264bc483b2c641842478f5dcd8287e8d01a60a764c8dd84d892a922ef0a`，含41个原始输出/监管/授权/预检成员。Root 逐成员独立流式解压、核对原件长度及 SHA256，覆盖全部9输出并扫描解压后的内容，0目标凭据模式，排除模型/adapter/cache/输入 dataset。所有原始文件保留；17.6MB 文件经过人工目的和内容审查后选为原始实验证据发布，非自动导入任意大文件。

Unexpected events：Luna 启动前辅助检查器存在占位符及符号链接等假设错误，均在 production CLI 前中止；另一次监控误用了缺少随机后缀的路径，随后更正，没有停止/重启进程。Root 启动前缀检查器一次错误地等同两种绑定 envelope，按实际生产 schema 更正；只读失败检查没有修改运行。原始诊断及更正保留，科学代码及约定未修订。

仅改动本任务 provenance 文件；不改科学代码、冻结输入、旧账本或其他 agent 文件。发布由 Root 在独立 /tmp Git object store 协调，仅 stage 明确审查的 compact 文件、该单个安全归档和自身 INDEX/inventory 变更，非 force push；随后用独立远端 Git objects 核对字节。最终 commit 由独立 post-push receipt 报告，不能把本记录自身 commit SHA 写进自身。

下一步仅允许结果复盘和后续协议设计。保留本次 NO_GO；不事后降低配额、替换任务、扩池或将当前结果改为主结果 PASS。任何新采集／teacher／训练／评价均没有在本记录中获准。

实际使用追加清单见 OBSERVED_TRAIN_USAGE_APPENDIX.json：96 个身份与原注册 union 2612 及其他冻结 partition 的交集为0；按既有 task-level 前缀规则额外核对。未来全部 seed/prefix/alias 继承 ever-used TRAIN 状态。该结论仅覆盖已有登记，不证明未登记历史从未查看或 scene/template 无相似性；旧 register/metadata 未修改。
