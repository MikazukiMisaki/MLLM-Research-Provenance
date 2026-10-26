# Sol Research：最小SI-S01 source-only实现任务

这是新的实现/软件测试授权，科学执行仍未放行。先读同目录ADOPTED_SOURCE_ONLY_PROTOCOL.md，以及原v2三文、C01/C02澄清附录e350b1de...；后者已由root复核正确限定teacher/学生边界和B/C配额。user新要求持续到实验启动，现缩小为单臂source96必要条件可行性研究。不要开发完整teacher/training管线。

## 工作树与修改范围

以exact `844cc4b78df1f83e29391ffd5ab861a2d0c0a3fd`为基，在自有隔离worktree开发，建议branch codex/si-p3-source-only-v2。不得改权威worktree或评审worktree；代码前确认并读取AGENTS要求的PROJECT/PAPER_PROPOSAL/EXPERIMENT_PLAN/IMPLEMENTATION_PHASES/SPRINT_1_5资料。保留所有旧代码行为、旧journal/协议/权重/失败原件。机器路径和实参在ignored configs/local，不能写入科学commit。

可新增v2 namespace/contract/driver/source auditor/report/CLI及必要tests；尽量复用冻结公共projection/parser/typed generation/runtime backend和TextWorld规范化，不放宽旧synthetic gate、旧Caps/MAXIMA/授权。若必须改旧共享方法，先给具体触发证据和最小差异，由root明确裁定；不自行扩修。真实host/PID ownership guard保持严格，本任务不解决认证/内核/容器权限，不伪造map或忽略未知NVML PID。

## 必须交付的最小生产路径

- 绑定原A96身份/metadata hash、家族及固定seed42/pool_seed42/d5/order的纯metadata计划；拒绝D48/E600替代和未来结果字段。不得实际生成真实生产launch配置或打开新task正文来调规则。
- source-only typed producer→原P0 parser→collector→raw events/trajectory/registry→独立source auditor→JSON/Markdown report。模型/环境真实接线必须是可执行的明确接口，不能把synthetic collector+单独4调用diagnostic宣称接好；但任何真实调用只能后续授权进行。
- S5及时保存、正常Y0/technicalNA、source seal96、E/F/S必要上界，source-only零teacher硬门禁，所有YT=NA。报告只作source供给可行性，不作恢复成功率/学生效能。
- 各预算先reserve/start落盘，调用后complete或failed/open；实际source各物理调用只计一次。模型装载/环境construct/close独立记录，counted envops仅reset+step，分阶段无clock/debit归零。全局超限前拒绝，无retry/topup。
- live gate必须绑定新source SHA、review、原输入/runtime和独立root授权、唯一argv/env/output；输出已存在拒绝。清洁解释器production CLI preflight-only必须0模型对象/生成/CUDA初始化/环境construct/reset/step/单位/fresh source且science output不存在；与software fixture明确区分。正式maxlive1，无自动retry。只实现这些gate，不创建真实gate或执行production preflight。
- 新脚本应清楚区分software_only fixture与live，拒绝synthetic冒充真实。不得调用旧G4统计或改旧结果。

## 必要测试/验收

真实production函数非空正向fixture，只有raw模型生成/环境I/O边界synthetic；包含全96去向及五家族的完整source-only source seal/report。分别证明结构NO_GO、NOT_FUTILE、normal terminal/empty map/parser fail、技术或预算INCOMPLETE，不能mock auditor/registry/parser令其通过。

负向至少：第5动作terminal/truncated/empty；S5有效第6次parser失败仍E内；snapshot晚于未来生成或缺map拒绝；source不足96不作结构判定；E/F/S总量够但family不足；任何teacher/replay/suffix/train调用被硬拒；foreign task/seed/order/map/action-ID/引用/跨run/hash/origin不符；异常后已完成Y0不丢；partial外部操作不归零；budget边界先拒绝、time持续累计；samePID/UUID不足以绕过owner；旧consumed auth、旧output、错SHA拒绝；真生产preflight synthetic fixture计数0且无source output。

独立新source auditor不能依赖collector汇总计数或report自证；须逐raw receipt/trajectory引用重构。真实输入计划只由后续Luna在复审通过后准备，本轮测试只用明确synthetic identities/manifests。

clean pinned interpreter跑focused及完整repo suite、py_compile/diff；已知基线953passed/3failed/77errors的80历史ID/type可保留，要求无NEW失败/错误，新增相关全部通过。若clean gate因dirty阻断，封存提交后重跑并保存真实subprocess收据，不能假PASS。

推送非force科学branch exactSHA并核对live ref；提交完整delta/方法hash/原始测试日志/receipts/输入beforeafter/清洁origin与scope flags。开发者不拥有独立验收/launch权；所有真实模型/tokenizer/CUDA/ALFWorld/SSH/preflight/live/采集/训练/eval均不运行（pytest软件fixture子进程不等于生产预检）。

## Provenance协调

自己新唯一目录保存RECORD及紧凑发布清单；不用共享INDEX/rolling inventory，不stage其他agent文件，不自行provenance push。root统一发布。若独立生产链发现新具体接口问题，给路径/触发/真实synthetic证据请求最小scope裁定，不停在泛泛风险列表。完成后冻结代码交root exact-SHA独立审查。
