# SI-E1 工程任务共同合同与范围

用户说“按你说的继续”，此轮实施前一阶段明确的工程步骤，不是新科学实验。权威设计：/home/lizening/research-notes/agent-logs/2026-10-25T084517Z__SOL__si-p3-controlled-experience-design__si3_7d91/MINIMAL_CONTROLLED_EXPERIENCE_PROTOCOL.md（SHA256 2d5ddfddc4c18072fa1b431d9c1e8e0688e1dd180511e49cdfb8112fb90d7d6e）及phase3_independent_review.json（2c29a244...）。上一轮任务结案由本新任务替代，但所有旧文件冻结。

允许新增隔离worktree的科学工程实现、真实软件pytest/synthetic integration、只读现有模型/adapter/tokenizer文件hash、**本地已缓存精确tokenizer文本编码/mask审计**。禁止加载/构造Qwen3-8B或实际P0神经模型对象、真实model.generate/实际LoRA优化/训练、ALFWorld构造/reset/step/replay、采集96/新task正文或结果、正式preflight/supervisor/G2/G3/G4。测试可用明确synthetic模型/env边界与CPU tiny toy+PEFT/梯度来验证软件（标为软件toy，不声称真实训练或实际P0 warm-start通过）；不触GPU或下载。允许隔离fixture负向CLI/supervisor测试，不称真实预检PASS。

科学base85cbb923，原R19/G4/prompt/baseline/trainer/config/旧失败及消耗过clearance保持字节；优先纯新增模块/新协议/新测试，不改历史文件使测试变绿。旧SFT协议recovery-target禁止仅由新的SI-P3独立工程协议说明**未来条件性例外**，不篡改旧冻结或给当前执行许可。目标scope为最小可独立审查的单步collector+evidence/cost+public目标/共同池+paired-exposure+warm-start/final18合同包；不是通用self-improve平台。不开learned selector/额外K/多轮/memory/DPO/RL/新模型或环境。

最终五family：source96=35/26/16/9/10；D48预留科学调用0，E600封存，395非light+2light不运行；74official unseen不用。新pool每task唯一预定d5/10/15/20，family×cut matrix见前协议绑定独立addendum JSON；原source CONTINUE只引用，exact prefix replay后一次stage1/2(40/16)，一个teacher动作且在同一个环境立即P0suffix(16)、H50。source50+teacher2+suffix49−d，上界8496gen/9792含reset/138240out，input总16M、单call8192、GPUallocation4devicehours只是未来投资帽、当前不花。额外baseline/replay/gate/shadow/科学smoke不许藏入，剩余额度非自由调用授权。失败/漂移/replay/receipt/预算异常stop、不retry/换task；单位原件append-only。

Q对全池对称，source早停/无target仍留slot，未执行teacher YT=NA，complete=true/cap=true不能误判截断；bare-ID/真实map/命令/transition一致。B所有Q且YT1，C在B内Y0=0；B抽样不排除C。C24配额9/6/4/2/3，neutral最低同；Q≥72，family22/17/10/6/7；选B24后至少8neutral且与C非相同，不重抽；各≥20public projections。真实新pool尚未产生，软件tests不能替代该门槛验收。

S120背景配额44/32/20/11/13：仅原expert_train已用task；不读新task正文。为闭合尚未指定的outcome-blind背景规则，本轮在任何新pool结果前固定：每family按SHA256 UTF8("SI-P3-S-v1\n"+family+"\n"+canonical_task+"\n")排序取配额（canonical tie）；每个已选task从旧dataset_split=train、格式/map/public完整且2048整序fit的既有动作row中，按SHA256 UTF8("SI-P3-S-row-v1\n"+task+"\n"+str(step_index)+"\n"+prompt_sha256+"\n"+completion+"\n")取最小（step_index tie）。不得按loss或新效果挑row；已选task无合格row则NOT_READY，不用另一task替换。S-task身份不换；若source/hash/机械质量不闭合报告不要修旧数据。旧dataset路径由使用者CLI传入，SHA固定c547e8f0c5988b29288f2a097169c7859741b7d4f53f222af31f5e2889d516cf。

B/C 24new+同S120=144、epochs2、effective16(micro2×accum8)=18update，各新task曝光≤2。同P0adapter warm-start/freshoptimizer/LoRA-only/final18，seed42，无best-validation/epoch/seed/checkpoint搜索。family×**实际loss-bearing ID+EOS长度**内B/C固定hash一次采样配paired slots，再共用每epoch同置换/批边界，确保逐microbatch/累积update真实监督token相同。prompt/padding不得进loss，EOS在PAD==EOS时仍合法监督，CausalLM shift实数须核对。两臂累计nonpad prompt量的新例与全臂两种ratio都≤1.05，非单样本max/min，不许truncate map/target、改loss mask或重抽B来过。

工程不能导出可误运行的科学gate/launch argv/真实运行manifest，不建configs/local通过gate。新增tracked协议/config只描述ENGINEERING_ONLY、execution=false；若提供CLI仅offline audit/synthetic，不提供本阶段可直接launch的live/train入口。生产runtime-port可实现供未来有独立授权的driver使用；真实模型/环境默认关闭且入口不可绕过explicit gate。需要额外科学scope先报告具体阻断，继续独立部分，不自动扩修旧基线。

每位仅写自己任务dir；Sol另有独立科学worktree。所有命令由subprocess真实capture stdout/stderr/returncode，不用人工转录作raw；遇本地脚本错误原log保留。不得执行旧硬编码ROOT脚本；新OWN=Path(__file__).resolve().parent并精确断言新dir；输入路径由Path实际构造并exists/hash后序列化，不手写易漏agent-logs路径。冻结交付SHA/manifest及RECORD，即便FAIL；不写共享INDEX/root inventory，不stage/push provenance。协调方统一审查/发布。R19实际5142/7949仍是历史，当前真实科学新增0；tokenizer-only与toy软件活动单独据实报计数，不冒充0活动。
