# SI-E2 UUID 静态诊断补充（只读封存）

本目录独立于原 dfc 交付。此处仅静态读取源码/收据和运行 stdlib 文件解析；未导入 torch，未调用 CUDA/NVML/模型/环境，未运行测试，未更改生产代码。新实现授权另立工程目录处理，不改变本补充的只读性质。

## CONFIRMED

1. 原唯一工程 probe 的 journal 只有 opened / model-load started / model-load failed / driver_failed 四个事件；错误为 `actual CUDA device UUID differs or is unobservable`，`resource_evidence=null`。原始失败现场没有 UUID 实际值、type 或 repr；不能事后给该次调用补造原始观测。
2. 冻结 `runtime_backend.py:114–119` 先 `torch.cuda.init()`，再比较 `str(getattr(get_device_properties(0), "uuid", "")) == permit.gpu_uuid`，然后才到一字节张量及 own-context 证明。第 137 行重复相同比较。该异常表明比较返回 false，不能仅据错误字符串断言设备确实不同，也不能称原 probe 从未进入 CUDA 初始化。8B loader 位于其后，尚未到达。
3. 已安装包由原收据及文本路径绑定到 torch 2.6.0+cu124 / Python 3.10。`torch/cuda/__init__.py:511–527` 的 `get_device_properties()` 会 `_lazy_init()` 后转发编译绑定；`init():275–286` 也调用 `_lazy_init()`。静态审计不能通过调用这些方法来声称零 CUDA。
4. `_C/__init__.pyi:10784–10795` 把 `uuid` 标作 `str`，但它是静态 stub，不是实际属性类型的证明。安装目录提供的这些文本不能证明编译 `_CUuuid.__str__` 的全部跨版本语义；本审计没有加载绑定来补证。
5. `cuda/__init__.py:781–810` 的私有 NVML UUID 函数会实际装载 NVML/查询设备；`:813–840` 私有 UUID→ordinal helper 使用 `startswith()` 支持部分 UUID。两者均未调用；部分匹配不能作为严格身份比较器。
6. 后续、独立获准的 Luna identity diagnostic（不是原 probe）保存了实际值：type 为 `torch._C._CUuuid`，str 为 `b08bc603-ebdb-787d-b5b6-ec796ea3022a`；NVML/预期为 `GPU-b08bc603-ebdb-787d-b5b6-ec796ea3022a`。36 字符完整 payload 相同，直接字符串比较 false。此结论来自实际新收据，不是只凭静态 stub 猜测前缀。
7. 同一独立 diagnostic 的后续一字节分配记录 local PID 837631，而 NVML compute row 为 PID 3082604、name `[Not Found]`。`own_compute_row_observed=false`。没有已认证的映射，不能把该行认可为本进程；UUID wire 兼容并不解决进程身份。原 `inspect_gpu` 必须继续拒绝。
8. 原 full probe child exit=1，supervisor 分配成本 0.006624203831630034 device-hours；generation/reset/step 均 0，model-load failed/open 保留。独立 identity diagnostic 另有一字节及非零耗时成本，不能冒充本代理的新调用或并入原 probe 成功。科学累计仍为 5142 generations / 7949 reset-inclusive ops。

## SUSPECTED / NOT VERIFIED

原 full probe 缺少 raw UUID，因此其那一次实际属性值仍 NOT_RECORDED。后来的同源/同 torch 证据支持 wire-format mismatch 机制，但不是追溯采样。未来严格格式比较修复后能否继续到 own-context、8B/P0、环境仍 NOT_VERIFIED；当前 PID mismatch 独立 BLOCKING。不能从本审计推导 inference/training memory fit、资源稳定性或 acquisition/training/evaluation readiness。

## 最小后续提案（本目录未实现、未测试）

* 增加只处理完整 canonical 8-4-4-4-12 UUID 的 pure comparator：观察值允许 bare canonical 与既有完整 GPU-prefixed 表示，预期必须是完整 `GPU-` 格式；只比较全部 128 位。拒绝 missing/empty/空白/截断/非 hex/多 UUID/MIG/其他设备，不使用 strip、prefix match、名称、ordinal、显存或任意替代身份。
* 在首次断言前把原值的 present/type_module/type_name/str/repr、预期字符串与观测阶段写入现有 journal，并由 append 的 flush/fsync 保证失败后仍可读；同一个 comparator 用在 post-load 断言。属性缺失或转换/查询异常也应有 fail-closed 的可区分证据。
* 仅新增 production-function 软件测试：真实 wire 文本正例；不同/畸形/缺失值；首次断言失败仍持久化原值且尚未分配 tensor/加载 8B；post-load 使用同一比较；捕获 host PID mismatch 持续拒绝，raw NVML 原文保留。不得 mock parser/journal/validator 成 pass。
* UUID 修复、独立 exact-SHA 审查以及另一个已审查执行上下文和全新授权是彼此独立条件。旧 probe 已消费，不重试；本方案不扩大 driver、训练、处理流程、prompt、费用或 PID/UID 权限。

## 可核查证据

`SOURCE_BINDINGS.json` 绑定 13 份原件（完整路径/bytes/SHA）；`STATIC_SOURCE_EXCERPTS.json` 保存以上代码行段。新 identity 两份 SHA 分别为 `41712d0516832fc48ddaadccee66a9e93ad48d4c0fa744ec5b5eb5c171824335`、`b30bec7d674a273d08b55bf90da12d8be4ec6ddf493686cccb4322369778e982`。原失败 journal SHA 为 `cbe32c033032c3ee42b0d412795e3cb675b784dacf7372fe9b1591473e48edef`。`receipts/static_capture.receipt.json` 为实际 stdlib 捕获 exit 0；初始路径发现错误在 discovery_failures.json 如实保留。
