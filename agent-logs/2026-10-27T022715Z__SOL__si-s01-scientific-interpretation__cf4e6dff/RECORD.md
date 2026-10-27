# SI-S01 正式 source-only 结果科学复盘

Agent: Sol Designer / independent reviewer and coordinator. Status: DESIGN_ONLY_REVIEW_COMPLETE; current STRUCTURAL_NO_GO preserved.

本任务记录目录创建 UTC：2026-10-27T02:27:15.668258+00:00；完成 UTC：2026-10-27T02:27:15.696589+00:00。科学仓库 Alfworld-Self-Improvement-Project，执行 branch codex/si-s01-shared-gpu-adapter，开始/结束均 f1e0d56a1be2a65876bbec5b8950fb76cda3eace；审查 worktree wt-codex-r18c2 保持 agent/codex-r18c2，HEAD e537f441010077123a307e9d50ea40cf8dad8547。本任务仅新增本 provenance 目录及自身 INDEX/inventory 行。

判断：继续围绕提升小语言 Agent 成功率研究，但停止按当前五类均衡 C24/B24 配方直接进入教师采集与训练。正式执行完整通过，冻结数据供给门槛未通过。当前瓶颈是失败经验与可学监督的构造，而非已解决的 GPU 接入。

OBSERVED：全部96 TRAIN source 中79成功、17失败，描述性比例82.29%。简单放置35/35、清洗24/26、冷却10/16、加热8/9、双物体2/10。14/17失败集中于冷却与双物体；不能外推为未见任务性能。7个不可用S5都是正好第5步完成的成功任务。合格S5子集E89，F17/S72，S72不能写成全部任务成功数。

冻结门槛共5项未通过：F总17<24；简单F0<9，清洗F2<6，加热F1<2，双物体S2<3。不是补足7条就能满足。24是事先制定的投资门槛，不是普适学习理论界限。F17仍需教师恢复成功、共同质量筛选、去重和真实监督长度匹配，因此不能当作17条可训练目标；B_pool包含C，不得改成纯neutral pool或套用纸上11配对数当正式容量。

Root 对 Sol Research 的行为审计进行独立字节/计数交叉核验：17个失败均正常执行50步、done=true/reward0；1959个动作均在旧生产验收和逐字段复核中可解析并绑定当前动作表。Root独立重复片段重算实际exit0，12/17失败、4/79成功存在周期1..10的重复动作/可见状态片段，第5步时均未确认完整重复片段。该指标事后定义、轨迹长度不同，也不等于潜在环境状态或子目标毫无变化，不能当作因果失败原因或部署selector。

INFERRED：本批存在明显家族异质性，原先按任务量近似分配失败例额的配方与实际错误供给不匹配。固定S5监督是否指向错误决策尚未证明；后续失败不能反向自动证明第5步动作错误。值得优先核验失败能否形成具有任务迁移价值的修正监督，尚无依据直接训练或盲目扩池。

下一阶段只设计：Sol Research逐案核验全部固定17例的可见子目标进度、重复片段与S5时点关系、潜在监督是否可辨识，保留不确定；Luna维持冻结使用登记、隔离与预算证据。Root收敛一个预注册的小规模机制验证协议，保留真实共同生成池/成功中性对照定义、共同Q和任务去重。不以循环指标新增selector或改动当前S5/任务/种子来挽救本次NO_GO。教师、可恢复性、目标长度、真正B/C差异尚未实测；若未来有独立新协议才可验证。真正self-improvement仍需训练后actor-only C优于原P0和同池成功监督B，且在未使用评价任务上成立；工程运行成功或teacher轨迹本身不能替代该证据。

新实验、模型/CUDA/ALFWorld、tokenizer、teacher、训练、评价、heldout均0；没有重跑软件测试或项目validator。本任务检查是封存输出的stdlib只读统计，不声称新production验收。原始证据不修改。Sol行为审计新副本发现字面量\n文件结尾，已要求严格JSON修正与重算清单；不影响原始run结果或Root独立重算。本记录不依赖该未冻结副本作为验收权威。

命令摘要及实际Git只读检查见commands.log，紧凑事实见INTERPRETATION_FACTS.json。仅允许下一步离线分析与协议设计。本记录不授予任何新增科学执行。Provenance非force发布和远端字节核验由Root协调；最终Git SHA在独立post-push receipt中报告，避免自身引用循环。
