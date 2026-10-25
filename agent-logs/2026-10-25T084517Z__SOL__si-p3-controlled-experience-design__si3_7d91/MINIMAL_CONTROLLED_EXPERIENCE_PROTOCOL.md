# SI-P3 受控新经验最小协议与投入决定

**DESIGN_REVIEWED_WITH_LIMITS / NOT_EXECUTABLE。** 协调方独立决定：值得保留“提高小语言Agent成功率”的研究主线，**只把一次固定96-task采集可行性研究列为有条件投入候选；不打包批准480采集、训练或600评估**。本轮只有设计、元数据与纸上数学，科学新增0。既有R19/G3/G4、模型与旧失败现场保持不变；没有launch/preflight/科学执行授权。

这96不是效能试验；其最严格可得结论是“固定新经验配方能/不能在预算内形成可追溯、可比较的训练输入”。不能把yield、mask正确、训练loss降低或已产生24个目标说成学生成功率改善。

## 1. 论文主线、问题与可支持贡献

专家SFT已建立可用agent；恢复实验证明局部收益/伤害并给出收益边界；下一步检验能否把同基座controller的一次纠错经验转移到学生，使学生在部署时无需recovery仍提高成功率。

A=冻结原SFT-P0；B=同初始化+共同背景S+同池success-only第一动作；C=同初始化+同S+同池中“原actor失败且teacher恢复成功”的第一动作。两项共同主比较C>A和C>B。C在B内等价于baseline-failure filtering；新意最多是这个受控采纳配方及明确实证，不包装为新价值估计器、adaptive stopping、在线自主循环或从零无专家自举。相关工作/主张边界另见RELATED_WORK_AND_CLAIM_BOUNDARY.md。

## 2. 任务隔离与有限总体

独立metadata复算known-use union2612；候选TRAIN1141中light仅2，其他五家族1139。light两例不运行；74valid_unseen不使用；无新held-out宣称。所有canonical task/trial及其prefix/seed/alias只归一个分区，排除expert训练/验证、旧dev/架构/恢复/R19等已登记使用。对未登记历史浏览及scene/template重用仍有局限。

最终采纳的非执行metadata分区见ADOPTED_METADATA_RESERVATIONS.json：

| 家族 | 首轮采集 | 接口工程预留 | 最终评估预留 | 不运行余量 |
|---|---:|---:|---:|---:|
| pick-place |35|18|221|145|
| clean |26|13|158|104|
| cool |16|8|102|68|
| heat |9|4|56|37|
| pick-two |10|5|63|41|
| 合计 |**96**|**48**|**600**|**395**|

另有2light不运行。600与48沿用Luna五家族identity hash/Hamilton提案，原480采集metadata中只保留96；剩384转回不运行余量，不设计“缺正例就接着采”的通道。395也不得作结果驱动的替补。没有打开未使用task正文/结果，没有生成seed/call-order/launch配置。固定hash是可重复选择规则，不保证随机代表性。

48仅是接口工程身份预留，优先synthetic；当前真实dev科学预算0，不能用于选teacher/prompt/d/recipe/checkpoint或评估效果。最终600为五家族、TRAIN内任务隔离评估，不是布局外验证。独立读取task名字发现final600的103个numeric-folder-suffix代理全部在known-use也出现，不能称未见scene；详见scene proxy JSON。旧development-only seeds1005/1009/1010/1022/1027不用于本新正式评估。

## 3. 共同生成池

固定原Qwen3-8B snapshot/tokenizer b968826...、原P0 adapter6e403d85...、公共goal/current obs/H4/完整有序map、greedy、thinking=false、H50、40/16/16生成帽。source/suffix adapter-on，teacher adapter-off。每task一条完整source、一个事先确定的d；d取5/10/15/20，采用独立复算的五家族×d矩阵（见independent_sol_addendum_review.json），全96位置每个d各24、总d1200，且每家族各d计数差≤1。构造为按表中family顺序先各分floor(N_family/4)，余数以四个d的共同循环指针顺延分配；再在各family固定identity hash顺序里按四个d的计数切块分配。它替代初始协调方草稿的全局位置cycle，以避免call-order变化造成family/cutoff偏斜。d按已完成动作计，模型见第d+1动作前公开状态；完整映射在任何新source结果前冻结，当前没有生成每task的d/seed/call-order可执行manifest。不得根据source终局或teacher成功挑另一个prefix。

source早结束/不可达d/空map保留NO_ELIGIBLE_STATE，不替换。source正常完整终局为Y0；从同task/seed/counter精确replay到原prefix后一次Stage1+Stage2，最多执行一个合法teacher动作K1，立即在同环境交回原P0，剩余50−d−1。完整对照Y0直接引用已完成source suffix，不再跑baseline、不做多K路径/分支/reset。未执行teacher动作时YT=NA，保留原invalid状态与费用，不制造恢复成功/失败。

共同Q与去重在结果采纳之前：完整可追溯且精确版本的源/公开投影/map/replay、原输出完整性/parser、合法bare ID与实际命令/transition、真实分支终局、2048完整训练序列fit；physical event复用→task一个anchor→exact公开输入/command去重。cap=true但complete=true不误排除；超长不截map/label，不只剔C。所有96计划slot、未到达/无效/失败/neutral/harm保持在完整池与分母。

B_pool={Q且YT=1}；C={Q且YT=1且Y0=0}。B保留C的采样资格，不能偷换neutral-only控制。全部有效配对包括harm与双方失败均留原件。source、replay reset/action、teacher、suffix各物理调用记一次；logical policy costs另列。具体合同/负向检查另见ACQUISITION_AND_INTEGRITY...及PAIRED_LABEL...。

## 4. 可行性与可比较训练剂量门槛

**只在完整96封存后审查一次；不据中期yield改变N。** 以下是资源决策guard而非最低可学习N定理。未达即当前配方NO_GO并封存，不能加384/改anchor/扩K/过采样直至通过。

| 检查 | 固定门槛 |
|---|---|
| 原source单元/slot去向完整 |96/96按原正常停止契约记录；技术missing不能填0 |
| 机械Q有效paired目标 |总≥72；各家族分别≥22/17/10/6/7（顺序同上；ceil(0.625*N_family)）|
| C独立task |至少24；家族最低9/6/4/2/3 |
| neutral独立task |至少24；家族最低9/6/4/2/3；因此B≥48 |
| 泄漏/错命令/身份/replay/receipt问题 |0，出现则整run STOP |
| 实际选中C24/B24公开projection |各≥20种；exact input-command无重复 |
| 实际训练set对比 |固定B单次抽样中至少8/24 neutral，且B/C训练multiset不相同；不通过不能重抽/排除C |
| token/mask/初始化/成本 |未来独立工程核验闭合；本轮未运行 |

C的9/6/4/2/3为final metadata家族容量比例对24的Hamilton分配，在新结果前冻结；不是依据效果选择family。按固定SI-P3-C-v1 hash各取配额；B从所有B_pool按“family×selected-C实际supervised completion长度（含EOS）”对应配额，以独立SI-P3-B-v1 hash只抽一次。它是length-and-family-matched success-only control，不代表使用所有B的训练效果。至少8 neutral是协调方比作者初稿更严格的contrast投资guard：它只决定是否继续，绝不能用来换B样本获得更好对照。

这些条件通过只意味着**这个小剂量训练配方可构造**。24个teacher首动作、每个最多2次曝光、共48次新例展示，不保证语义充分或迁移；不足以自动正当化90,000-generation评估。必须把“配方可构造”与“完整效能试验是否值得花钱”分别作决定。

## 5. 条件性学习剂量：不启动

保留原作者最小剂量：两臂分别为S120+B24和相同S120+C24，共144个task例；S从已用expert_train五个非light家族按44/32/20/11/13配额（合计120）取不同task、每task一既有合法公共动作pair，以预设hash/质量在新池结果前固定；配额在新结果前按原1139容量Hamilton计算，不按收益转配。不使用expert validation或新eval，旧expert_train每家族179 task的metadata容量足够，但实际row与token审核未执行。S不是新经验；它共同用于约束漂移，其本身效果没有第四臂分离。

每臂2epochs/effective batch16(micro2×accum8)=18updates，seed/data_seed42，fresh optimizer；同原lr1e-4/AdamW fused/cosine/warmup.03/clip1/bf16/LoRA r32 alpha64 dropout.05 all-linear/packingfalse/completion-only，唯一final update18 checkpoint。**从同一P0 adapter字节继续训练，仅更新预定LoRA；不是从base新建一个LoRA。** 同S顺序与权重、同新task曝光2次上限，逐microbatch/optimizer update真实loss-bearing token数完全一致（匹配完整ID+EOS，不计prompt/pad）。未来工程必须证明这套量，不能以字符数/原generated_tokens代替。

完整序列2048 fit，不截公共map/标签。prompt资源对称guard明确比较**两臂累计非padding prompt-token总量**：对两epoch的新经验曝光分别求P_B_new/P_C_new，对含S的全部曝光分别求P_B_all/P_C_all，两项max(P_B,P_C)/min(P_B,P_C)均≤1.05；不是每个数据集内最长/最短样本之比。分母非正即STOP。不符则停止该固定draw，不重抽或调整loss遮掩。589824 padded token slots/臂只是144×2×2048上界，不是已测监督token或耗时。

逐slot的构造也预先明确：选定24C及24B后，在每个family×实际loss-bearing completion长度cell内，C按固定C hash、B按固定B hash排序，逐一配成等长pair；S的120行形成输入/标签完全相同的S-pair。144个paired slots由一个独立seed42的固定置换过程为每epoch一次生成，两臂使用相同slot置换、microbatch2边界与accum8分组，保存真实schedule hash，禁止两臂各自重新shuffle。由此每slot的target loss长度相等，才可能保证每microbatch/更新的真实监督token相等；未来实际tokenizer/chat template/collator与loss归一化还必须独立验收。当前没有生成这份训练schedule或测量tokens。

原bootstrap协议禁止recovery targets，现有trainer也不满足P0 continuation/final-checkpoint。下一步须另立SI-P3协议例外/新增实现/真实tokenizer与loss-mask检查，并由协调方独立审查exact SHA。保留原SFT协议、冻结权重、R19/G4代码与全部旧原件；本轮不改科学工作树。

## 6. 预算：仅拟议首轮，不混入旧额度

使用上述固定d，保守完整流程上界：source4800+teacher192+suffix3504=**8496 generations**；source动作4800+replay1200+teacher96+suffix3504+192reset=**9792环境操作（含reset）**；generated tokens≤**138240**。通用101N/102N初稿数学也正确但更松；最终8496依赖新单K1原地handoff及预定cutoff平衡，不允许把省下的量花到额外baseline/replay/probe。

协调方采用作者提出的**累计input tokens≤16,000,000、GPU allocation≤4 device-hours**作为尚待工程测量核验的投资硬帽；另拟每次inference输入≤8192tokens，不截prompt，超限前停止。已有cache config仅静态核对max_position_embeddings40960，8192+max40在其内，不证明未来prompt均fit。8192×8496=69,599,232是逐调用帽推出的宽界，**16M是更紧的实际累计帽**，任一将超限即停止并保留真实单位状态，不能自动增加。4device-hours需按实际GPU张数×占用时长直接记账，不将walltime或CUDA kernel latency冒充GPU资源时间；没有实测就不承诺可完成或折算金钱。

任何runtime smoke/dev/复现若另耗模型/环境必须先列单独固定预算，不能混成免费预检；本轮这些预算均0。实际训练forward/backward/token/检查与未来评估成本另审，不包括在8496/9792。完整未来600task三臂单次actor-only评估自身上界90,000 generations/91,800含reset操作，故是重大后续投入，不自动放行。

R19历史实际5142 generations/7949含reset操作继续单列，已含177/342；新科学实际增量0。旧8999 source debit、旧one-successor/clearance不转成新研究预算，不重跑G2/G3/G4。没有用预算公式充当实际运行结果。

## 7. 效能验收、停止与投入建议

见STATISTICAL_ACCEPTANCE_AND_STOPPING_DESIGN.md：独立最终600，A/B/C三臂相同task初态各一次；C−A与C−B双侧exact McNemar+Holm、完整W/L、边际Newcombe10 CI；两项观测net≥5pp且gross harm≤5%。只一训练seed；推断依赖任务exchangeability工作模型，scene代理重叠保持局限。

E600时通过价值/伤害即W−L≥30、L≤30，最大片p=.00206，已蕴含Holm。完整门槛在假设真5pp/低伤害情况下单pair通过约52%，不能说600保证5pp验证，更不能用旧oracle5.56pp当预期增益。预定family描述与leave-one-scene-proxy-group-out影响检查只作解释，不冒充布局外证明。

**投入结论：有条件支持一次固定96的可行性候选；当前完整学习/评估campaign NO_GO。** 先补最小工程合同与资源闭合，独立exact-SHA审核后，才可在另行明确的科学范围内考虑这唯一采集。yield/覆盖/对照/实际token配平未过则止；全过也只是返回一个透明的高风险小剂量学习投入决定，不自动训练/评估，不自动追加采集。24-row学习可能有用也可能无效，不能靠工程PASS预测转移。

若后续学生不能同时超过强A与同池B，或代价/伤害不可接受，就收束该小剂量采纳路线，以既有专家SFT、恢复收益/伤害/成本和明确反例完成实证链；不把管线复杂度、审计或oracle当作self-improvement效果。论文贡献应忠于真实结果，不要求通过调参把它变正。
