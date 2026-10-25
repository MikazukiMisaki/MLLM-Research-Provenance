# SI-P3验收、推断边界和停止：前瞻设计

本文件是本轮设计的独立统计收敛；实际新结果为0。本设计没有将R19 oracle2/36或历史C10/162用于估计新学生效应或新池产率。E600为保留task容量与有限可用空间下的方案，不是保证效能或已批准支出。共同协议中的数据/预算/工程门槛还须全部满足。

## 研究总体与观察量

主总体限定于已登记known-use以外、文件存在的五个非light TRAIN家族的candidate mix，最终固定600个task。每task/trial及全部seed/prefix/alias同分区，同三臂A/B/C各一次actor-only、H50、相同环境种子，无recovery/selector/probe。不得称held-out、未见layout、六家族效果或跨训练seed稳健性。

两个共同主比较C−A、C−B_pool，保存所有配对2×2：两者成功、仅C成功W、仅对照成功L、两者失败。每项Δ=(W−L)/600，gross rescue=W/600，gross harm=L/600。raw结果、成本和初始badcase不可覆盖。家庭分母与家族W/L/Δ/harm均描述性完整报告，不挑子集作新primary。

独立task sampling/exchangeability只作为McNemar和规划的工作模型；固定hash不能证明随机代表性。实际panel均值/W/L不依赖该概率模型才可描述。独立metadata发现final600的103个末尾numeric-folder-suffix proxy全部也出现在known-use；这个proxy不是已验证hidden layout cluster。任务去重不消除模板/scene依赖，不把600任务或103suffix称600/103个独立环境。主检验即使通过，推广结论仍限于工作模型和明确总体。

预设一个零额外模型调用的影响检查：按该numeric-folder-suffix proxy逐组leave-one-group-out，分别重算两项观测Δ/gross harm，报告最小/最大、是否有任何Δ≤0/净5pp/伤害5%门槛翻转。它不作新主检验、不能替代cluster-corrected inference；影响大则收窄解释。若今后要提出布局外/总体稳健效果，须另立独立分组评估，而不是把此敏感性冒充证明。

## 固定数值决策

双侧exact conditional McNemar：D=W+L；D0则p1；否则p=min(1,2*sum(comb(D,j),j=0..min(W,L))/2**D)。两项Holm family alpha.05，排序第一≤.025、第二≤.05且方向均正。仍报告预选Newcombe1998 method10 paired score 95%边际区间（近似；非联合95%，非exact coverage），未来分析实现须用原文示例独立核对。不得临时改单侧/mid-p/检验/CI/主比较。

价值条件：两项观测净增益均≥5pp（W−L≥30），两项观测gross harm均≤5%（L≤30）。这些是资源与研究决策阈值，不证明真实效应至少5pp或总体伤害≤5%。协调方枚举16,771个满足价值/伤害的配对表，最大片p=.00206026568(W60/L30)，因此E600时该两数值门槛已蕴含Holm；保留检验核对但不以p-value组件“功效很高”作投入论据。

## 完整门槛的规划

stdlib独立条件枚举：D~Binomial(E,q), W|D~Binomial(D,(q+δ)/(2q))，单比较事件同时要求alpha cutoff、净5pp、伤害≤5%。假设iid三项分布仅用于纸上规划，不是实际效应估计。两项有关联，不相乘两功效。

| E600假设 | 单比较完整数值门槛概率 | 两项相同边际时的充分/必要界 |
|---|---:|---:|
| δ5pp / true harm2.5% (q.10) | 52.2953% | 4.5906%–52.2953% |
| δ5pp / true harm5% (q.15) | 39.2722% | 0%–39.2722% |
| δ5pp / true harm7.5% (q.20) | 0.9217% | 0%–0.9217% |
| δ10pp / true harm0% (q.10) | 99.9997% | 99.9994%–99.9997% |
| δ10pp / true harm5% (q.20) | 54.8349% | 9.6698%–54.8349% |

界是max(0,p025_A+p025_B−1)到min(p05_A,p05_B)，并不声称已知真实joint power，也不含数据/软件完整性门槛。边界5pp点估计条件的通过概率不能视为1；伤害率边界亦同。独立小N三项式穷举交叉核对、与Sol独立tail方法相同场景差异<2e-15，保存在独立math/receipt JSON。充分说明“600即可稳定验证5pp”不成立。

## 停止与结论层级

- 先冻结分区、完整生成池与采纳/训练方案、有限总N和分阶段门槛，不能采到正例quota、换anchor/task/teacher/prompt或反复搜recipe/seed/checkpoint。96 feasibility不测试学生成效；其结果只能按预定数据/成本guard决定是否值得返回后续投入审查，不自动启384或训练。
- 科学上可预期的invalid/早终止按冻结路径保留，失去候选不补。技术完整性、replay/receipt/hash、输入/预算、外部操作状态出错即整run STOP，保存已花成本和原证据，不自动retry，不记为科学taskfailure。
- 训练B/C同P0精确初始化、固定一seed和最终update。两个checkpoint及其输入数据hash冻结后才允许打开final outcomes。single seed最多支持这两个已冻结checkpoint，不能声称跨seed。
- 最终只分析一次；不逐批看C−A/C−B，显著则停，不加E到显著，不挑成功family或删困难task。新配对不完整则不能默删分母来过检验。
- 两项显著、价值/伤害、完整性及成本均达标：支持五家族任务panel上这一次失败感知采纳配方的成功率改善；不证明新颖算法、因果学习信用或布局外稳健性。C>A但不胜B只支持额外成功演示训练；C>B但不胜A不支持提升原agent。结果不精确则INCONCLUSIVE，不能p>.05=证明无效；同样不允许自动续采/调参。
