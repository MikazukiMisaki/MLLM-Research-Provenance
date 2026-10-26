# Astra：最小工程适配与旧公开路径证据的独立静态意见

**范围可接受，不需要扩大实际调用或追索不存在的历史内部RNG。** 公开路径吻合本身不是P0运行证明；若再有任务要求的真实冻结P0装载、同一受保护生产核心的一次真实推理、当前输入/张量/解析/动作绑定和完整身份/费用收据，就足以支持**这个输入上的真实source actor/P0推理，以及这条保存命令路径的公开可观察兼容性**。

这不是六步自主actor闭环或A96全流程证据，也不是launch clearance。本轮只读两份范围文档及已封存d7软件审查JSON，未运行任何测试、validator、模型、tokenizer、CUDA、NVML、ALFWorld、SSH或preflight；未读旧raw轨迹或新任务正文，未改代码/当前任务文件，未联系其他应用线程。

## 1. 一个需要明确的验收连接：不增加调用

实现任务第17–19行分别规定保存首提示推理、解析/动作比较和reset后六步公开路径比较；Revision2第7行规定prepared-versus-sent一致性。应在实现及验收记录中**明确把首次输入/首次命令连成同一条证据链**，而非两个互不相连的PASS：

1. 本次reset的公开task/goal/observation/完整有序map，与被认证的历史reset/首动作前状态相符；H4使用该历史首次请求实际对应的空/已记录历史语义，不从未来source结局取得信息。
2. 从该当前公开状态经冻结的P0 projection/prompt规则所得首提示，与历史保存首提示匹配。该提示经本次冻结tokenizer/chat template准备出的内容，与真正交给共用生产核心的rendered input/tensors/attention mask相符；不能只比较打印出来的字符串而发送另一份输入。
3. 本次真实输出通过冻结P0 parser，再经**同一个当前完整ordered map**得到合法Action-ID及command；与被认证的历史首次parsed选择和第一条保存命令相符。之后实际执行的仍是既定保存命令白名单，不把比较机制改成新的actor控制流。

这只是对任务已要求的prompt、prepared/sent、parser、map、command和receipt比较作连接约束，不要求第二次generation、额外reset/step、读取更多task或新架构。可用既有production函数和本次允许的原件/内存数据完成；此处并未执行它们。

**若上述连接缺失**，可以如实报告“对保存文本的一次P0推理兼容”和“保存命令的环境路径兼容”两项组件结果，但不能称当前环境公开状态→P0请求→合法首动作之间的值/引用一致性已经验证。即使连接齐全，也不能称生成输出实际驱动了六步环境闭环：本方案明确由六条保存命令驱动环境。

这是本复审唯一需要显式收紧的验收表述；没有证据支持扩大开发或实际调用数量，也不认定尚未提交的实现已有此缺陷。

## 2. 可以接受什么，不能据此推出什么

| 未来实际观察及约束 | 可支持的有限结论 | 不能推出 |
|---|---|---|
| 两wrapper真正调用同一guarded core；当前冻结8B/P0、adapter-on、dtype/SDPA、tokenizer/chat/张量/mask/greedy/cap/身份收据闭合；一次首提示生成成功 | 同一source推理核心在该实际输入上可装载并完成推理；该次输出及解析/首命令兼容 | 其余五个状态或S5上的新actor推理、所有长度/任务、H50闭环或完整A96运行均正确 |
| 新工程pool42、nominal seed30000，一次reset及六条保存命令的全部已保存公开states/maps/commands/transitions相符 | 在本次配置下，这条固定命令路径公开可观察兼容 | 历史pool/RNG/counter被重建、隐藏状态相同、其他动作分支或seed42的未来source必然等价 |
| 当前prepared内容与实际发送张量相等；所有已保存历史prompt/token/output/parser字段按约定匹配 | 当前推理输入绑定成立，已保存的历史字段吻合 | 未保存的历史输入token IDs/attention mask/内部张量被恢复或已经精确比较 |
| 一次真实load/inference及有界环境路径的费用、资源、清理与supervisor终态闭合 | 这一具体有限工作负载的资源与运行事实 | 8192最大输入必然放得下、A96全部4800调用可在4device-hours/16M内完成，或学习效果 |

单次旧首提示可能短于以后A96输入；本方案不提供最坏输入内存/时延保证。保留逐调用上限、真实预算与失败STOP即可如实限定这一风险，不应因此擅自添加最大长度压力实验。一次工程成功可以解除“从未观察到真实P0装载/单输入推理/该公开环境路径”这几个具体缺口，其余生产编排仍依赖独立软件验收及之后真实科学运行证据。

## 3. 缺失的历史内部RNG不是这次兼容检查的必需输入

历史只保存nominal seed30000、该路径及相应公开记录，内部pool/RNG/counter没有保存。本次pool42是**新工程设置**。只要明确记录 `HISTORICAL_INTERNAL_RNG_NOT_RECONSTRUCTED`，可以合法比较其公开结果；没有必要要求恢复无法从原件取得的内部状态。

这里的逻辑是“本次运行观察到相同公开路径”，不是“输入seed相同所以内部状态一定相同”。即使公开字段全吻合，内部RNG状态、未走分支和其他任务的等价性仍未获证。若公开字段不符，按固定合同立即STOP，不换seed、不第二次reset、不修改白名单去求匹配；不把不匹配自动解释成模型错误或科学学习失败。

同理，历史input token IDs缺失只能记UNRECORDED。本次重建/发送一致性是新的当前运行证据，不是历史张量原件。历史terminal之后的map若是合同要求且原件缺失，不能凭terminal补成空map；这与允许历史内部RNG未记录是不同的证据字段政策，任务已作区分。

## 4. 任务与Revision2的其余边界可接受

- **作用域不混用。** 实现任务第11–13行保留真实A96 Permit/Plan及source ledger；工程使用独立typed EngineeringPermit、purpose、持久预留、输出和一次授权。共享的是受保护加载/生成机制，不是将旧task伪装为A96或把engineering加入科学Plan modes。内部环境RNG未保存不能成为放宽GPU PID/UID身份的理由；两类证据相互独立。
- **共用核心必须由新代码证实。** 原d7软件PASS只覆盖d7，不能自动覆盖后续抽取。任务已要求两wrapper真正调用同一core、保留source guard/ledger/treatment、AST/method-span及production differential软件证据，并对新exact SHA独立验收。实现前描述“共用”不能替代这些证据。
- **旧记录读取有界。** 第19行绑定first raw line及reset/六transition/source-complete/首generation原件和receipt joins；当前selected slices与既有全文件认证区分，不扫描其他source来找替代，不读A96或held-out正文。未来manifest/原件不足时应在既定边界内停止，不能猜测补写。
- **费用与失败原件边界充分。** 一次model/tokenizer load、一次显式one-byte probe、一次≤16输出/8192输入的生成、一次环境构造、一次reset+六step=七次环境操作、一次close、600累计allocated seconds。构造/close另记，不重复算reset/step；未知/failed保守预留不变零，返回raw先于后置检查失败保留。所有成本属于新工程，不能冲减或重写科学5142/7949及未来A96预算。
- **supervisor与许可保持独立。** 第21行及Revision2第9–11行将最终真实supervisor区间作为费用权威，保留真实child rc/unknown、deadline、cleanup/survivors和原始日志；exit0不是完整PASS。host/GPU可信所有权、新exact代码、proposal/input/argv/env/output绑定和新root授权未齐，不得进入实际工程。本文未检查任何当前socket/host/NVML状态。

该受限工程只回答一个component-level runtime兼容问题，不改变已采纳科学A96身份/order/42/42/d5/H50、质量门槛或科学预算。允许nominal30000与新工程pool42只属于这次独立工程Permit，不能渗入A96科学计划。

## 5. 最终意见与记录依据

**建议继续现有最小适配实现和独立验收；明确首次reset→P0输入→首次解析命令的证据连接，报告范围限于一次真实推理与保存命令路径的可观察兼容性。无需增加真实调用，不追索未保存内部RNG，不放宽任何执行身份核验。** 实际成功仍须上述新代码与真实原件证明；本轮没有新运行证据、没有独立launch clearance。

已封存root review记录d7为PASS_SOURCE_ONLY_SOFTWARE，1116 collected /1036 passed /3 failed /77 errors，新增83通过、既有问题keys和prior passes无回退。本次仅阅读并核对该JSON的SHA，没有重跑测试或重审全部代码；不能称全套测试全绿。实际工程仍未启动。

| 本次输入 | SHA256 |
|---|---|
| ENGINEERING_ADAPTER_IMPLEMENTATION_TASK.md |525d271b38a8ecd2248c653291679a1c8fd37ceaec05b4dbf3b575932a7e103b|
| ENGINEERING_VERIFICATION_PROPOSAL_REVISION_2.md |fe974f732ca03d96718c679facaf1201aa78a364c2f3251690c461f28acf189f|
| d7 INDEPENDENT_REVIEW.json |0e878105b523afef4af18d130f6a60dacccd127c27e6f580723cf625ce2e385d|

输入绝对路径和字节数见initial-state.json。本轮仅写自己的唯一目录；原任务、源码、旧证据、共享INDEX/根清单不变，不发送其他应用线程消息，由root统一收取和发布。
