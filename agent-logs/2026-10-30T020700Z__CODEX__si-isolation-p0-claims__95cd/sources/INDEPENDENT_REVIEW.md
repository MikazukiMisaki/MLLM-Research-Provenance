# ALFWorld 来源元数据报告：独立抽查

结论：`ACCEPT_BOUNDED_SOURCE_METADATA_CLAIMS; NO_INDEPENDENCE_CERTIFICATION`。被审报告 `/home/lizening/research-notes/agent-logs/2026-10-30T022100Z__CODEX__alfworld-source-metadata__c048/ALFWORLD_SOURCE_METADATA_REVIEW.md` exact SHA-256 已核对为 `e81703545eeae1422350bb99f9078b39a7f465b373b12d8fc3fdc8bb65198aa5`。本次没有发现所抽查核心陈述的阻塞错误，不将抽查等同完整原文/历史复算。

## 独立核查结果

1. **ALFWorld 官方 README 的 split 数是文档描述，不是本项目可用样本数。** 直接读取指定 commit 的官方 data README，确有 3,553 training、140 seen validation、134 unseen validation。报告准确写成上游文档计数，没有把它与本项目历史清单合并或称为未曝光任务。这份 README 的数字也不能代替各 release archive 的逐版本成员计数。[固定官方 README](https://github.com/alfworld/alfworld/blob/aaba6870f86c5be6a08a491f32a50b906227bc3e/alfworld/data/README.md)

2. **ALFRED 原始 split 定义准确，映射限制必要。** 直接查阅 ALFRED 论文 Table 2 的说明：seen validation/test 的 scene 是 train scenes 的子集；unseen validation/test 的 scenes 与 train、彼此分开。它描述原始 ALFRED 构造，不提供本项目使用史，也不证明其测试集已有可兼容的 ALFWorld TextWorld 对应资产。报告保留这两层未知，正确；不能把视觉测试 fold 当现成文本任务来源。[ALFRED 原论文 Table 2](https://arxiv.org/html/1912.01734v2)

3. **AgentBench 只核实目录元数据。** 浏览器工具无法读取该 API，随后以标准库直接只读请求同一官方目录 API，返回 200：`dev.json` 为 2,644 bytes，`standard.json` 为 6,391 bytes，均 type=file，与原 receipt 一致。独立收据另存 AGENTBENCH_DIRECTORY_RECEIPT.json，含 API 返回的 Git blob IDs、响应字节 SHA 和真实查询时间。没有请求两个文件的正文或 download_url，没有读取任务 ID、记录数、任务内容或结果。官方 v0.2 文档也把 Householding 标为 ALFWorld。因此可证的是“该目录当时列出两个文件”，不能证任何独立新任务、上游映射、任务数量或兼容性。[官方目录元数据 API](https://api.github.com/repos/THUDM/AgentBench/contents/data/alfworld?ref=v0.2)，[官方说明](https://github.com/THUDM/AgentBench/blob/v0.2/docs/Introduction_en.md)

4. **0.4.2 下载脚本的混合版本引用正确。** 静态读取脚本可见 JSON/PDDL 链接指向 0.2.2，TextWorld game archive 链接指向 0.4.0；已存在下载文件且未 force 时直接返回，解压阶段也会跳过既有文件。报告据此拒绝由 Python 包版本或 release 名称推断清洁安装和资产版本，合理。本次只读代码，没有执行下载器、下载 archive 或解压候选文件。[0.4.2 官方 downloader](https://github.com/alfworld/alfworld/blob/0.4.2/scripts/alfworld-download)

## 未重新核验的部分

本次没有刷新各 release asset 的时间戳或 issue 状态，没有重读模型训练语料报告或全部许可文件，也没有再次复算 G1/旧 archive/0.4.2 的历史计数。它们在被审报告中是指明来源与观察时间的既有发现；本验收不赋予其新的实时状态或独立全文核验。未检索或执行新生成器路径。论文提供的上游 split 定义并不消除未定位的文本映射、历史运行或模型前训练接触问题。

原报告将“未知条款”与“禁止”区分，不用软件许可替代逐资产结论；本次不作新的法律判断。AgentBench Git blob 身份来自目录元数据，本次没有独立对文件正文重算 Git blob 或 SHA，不能写为全文验证。

## 允许用途与门槛

可将报告作为来源调查与未解决映射的证据入口；不能称任何列表、上游 unseen/test 名称或不同包装器已经提供项目隔离样本。现有 G1 使用史依然约束相关已用子集，保守保护规则不变。本审阅不建议挑选某些来源、任务、分组、seed 或门槛，也没有形成新评估方案。四项前提全部先有证据并经独立复核的要求保持不变。

原报告及 METADATA_RECEIPT.json 未修改。独立审阅仅使用公共文档、源代码和目录级元数据；无候选文件正文、模型、环境或科学过程访问。
