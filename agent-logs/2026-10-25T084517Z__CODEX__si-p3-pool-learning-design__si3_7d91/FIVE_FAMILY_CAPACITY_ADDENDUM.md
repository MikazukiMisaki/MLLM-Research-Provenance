# SI-P3 五家族容量修订与投入建议 Addendum

本补充保留先前24项交付及FILE_HASHES原字节。独立metadata已使初稿“六家族均衡96/60/600、每family至少126候选”的条件明确不成立：light只有2，而非足以支撑其独立采集/开发/评估配额。初稿的六家族quota与六家族普遍性说明由本文显式取代；没有新科学调用，也不把旧条件失败当实验失败。

**判断：支持五个非light家族作为唯一主总体、light2不运行、TRAIN task-disjoint评估及固定容量比例/Hamilton。480+48+600是算术可行的metadata预留包；我仍不建议据此一次承诺480采集投入。唯一推荐仍是仅将固定96例作为下一次单独审查/授权候选，384明确DEFERRED_NO_GO，不作为采够rescue的后续。** 当前全部采集、训练、评估许可均NOT_GRANTED。

## 1. 证据与总体的明确更换

只读取协调方independent_capacity_metadata.json、family_capacity_scope_feedback.json、independent_scene_proxy_overlap.json，SHA见新增source bindings；未重跑其脚本，未读未消费game/traj_data/outcomes，也未读取Luna未完成文件。独立metadata的TRAIN总1141，其中light2、pickplace419、clean301、cool194、heat106、picktwo119，非light合计1139；known-use union2612排除保持。metadata差集仍不是“从未看过”的证书。

这不是把light缺额随手转给其他家族：研究总体改为五个非light TRAIN家族，全部quota从新固定总体容量重新计算并逐列公开；不再声称六家族均衡。2个light留存不运行，不进入B/C/dev/E，也不从74官方unseen补light。若将来学生在light退化，本设计没有评估凭据，不能声称保持全六家族能力。

## 2. 可核查的整数容量方案

固定weights为原非light容量N_f/1139；对每个总额n先取floor(n*N_f/1139)，剩余按整数余数降序分配，完全平手按canonical family字符串升序。不同分区都用这组原weights，不在切掉eval之后偷偷重算分母。以下是纸上配额，不是已创建的task schedule：

| family | 可用metadata | E600 | 接口D48 | A480预留上界 | 96一期 | 384差额 | 全480包余量 |
|---|---:|---:|---:|---:|---:|---:|---:|
| pick_and_place_simple | 419 | 221 | 18 | 176 | 35 | 141 | 4 |
| pick_clean_then_place_in_recep | 301 | 158 | 13 | 127 | 26 | 101 | 3 |
| pick_cool_then_place_in_recep | 194 | 102 | 8 | 82 | 16 | 66 | 2 |
| pick_heat_then_place_in_recep | 106 | 56 | 4 | 45 | 9 | 36 | 1 |
| pick_two_obj_and_place | 119 | 63 | 5 | 50 | 10 | 40 | 1 |

总额1128≤1139，五family列和均不超容量，余11非light（4/3/2/1/1），加light2为13永久未分配项。在metadata候选canonical ID唯一的前提下，每family统一hash排序后不放回切E、D、A的固定长度块，可构造task-disjoint解；这不是本线程已复核最终ID表或取得使用许可。若协调方已有metadata候选包，建议保留其相同E/D/A480身份块，先从A480各family按固定hash选上表96子块，不另换eval或dev。

**Hamilton不满足这里需要的分阶段可加性。** H(96)+H(384)为(176,128,81,45,50)，H(480)为(176,127,82,45,50)。如果总体480 quota已冻结，后384必须为H(480)−H(96)=(141,101,66,36,40)，不能再独立Hamilton384造成clean/cool的1例转移。所有子块/余量在新source结果前固定，不用一期yield换family、d、seed或task。

若只考虑我推荐的96采集，保留相同E600/D48元数据块后，还有395非light不属于这次96采集（即384 deferred+11余量），加light2共397。13是完整480 metadata-envelope之外的余量；397是只采96时未纳入本次采集的余量，两个分母不同。当前所有这些task均未由本线程运行。

若后续身份/可用文件数不能满足某列，先标NOT_READY/停止，不能跨family挪额、用light替代、读取未获准heldout或看结果补11个reserve。预先固定容量只是可构造性的条件，不是所有task独立新场景/无暴露的证明。

## 3. 96个动作前anchor与对称质量

一期family数量35/26/16/9/10。依旧每task一个完整source、一个动作前anchor、不用未来标签。d仍为5/10/15/20，总体各24；在每family先每d分floor(n_f/4)，余数按固定family次序循环分给不同d，可使每family各d差≤1、总体均值12.5。只有数字矩阵写入新增数学文件，没有task IDs或可执行schedule。若source达不到预定d、终局/空map/invalid，保留slot去向、不补prefix。

40/16/16帽、H50、H4、有序map、模型/adapter pin、一次teacher首动作、原source CONTINUE复用/完整replay绑定、合法首动作terminal允许空suffix、complete=true/cap=true保留、invalid和技术缺失不填0均沿原设计。B_pool仍为全共同Q内恢复成功，C仍为其CONTINUE=0子集；B不能排除C或改成neutral-only。

## 4. 学习组成与resource guards同步修订

为避免仅更换eval总体却暗留六家族学习quota，条件性B/C新例24与背景S120的总量、两epoch、effective batch16及18 updates保持；各family组成改用同一预先容量weights的Hamilton：

| family | C24配额（B24同family配额） | neutral最低 | S120背景配额 | Q最低ceil(5*A96_f/8) |
|---|---:|---:|---:|---:|
| pick_and_place_simple | 9 | 9 | 44 | 22 |
| pick_clean_then_place_in_recep | 6 | 6 | 32 | 17 |
| pick_cool_then_place_in_recep | 4 | 4 | 20 | 10 |
| pick_heat_then_place_in_recep | 2 | 2 | 11 | 6 |
| pick_two_obj_and_place | 3 | 3 | 13 | 7 |

C配额为9/6/4/2/3、S为44/32/20/11/13；不是每family4/20，也不是将light的例子按观察收益分给某家族。S只来自已消费的原expert_train，不能从新eval/dev补背景；上述S family容量及实际token仍需独立工程核验。这个配额数值不证明学习充分。

原总Q≥72/96保留，每family guard按原10/16的比例写为ceil(5n/8)，C≥24及neutral≥24且分别达到上表quota，使B≥48。在全96固定完成后一次审查，不作效应中期加样。任何门槛不满足，本96方案NO_GO，不自动用后384填C。它们仍是资源/主张决策guard，不是少于24就不能学习的定理。

B抽样仍只看B eligibility、family及与C相同的真实completion token长度组成，单次固定hash、C完全有资格被抽到；不得按CONTINUE删C。实际B neutral数、重叠和信息不足如实报告，不重抽以改善contrast。公共projection覆盖≥20/24、真实loss-bearing token逐update相等、new-example与全臂非padding prompt-token比≤1.05、每task2次曝光、144例/臂、18updates、最终checkpoint18、同一P0 warm-start及共享S等约束均不变。缺实际tokenizer/初始化/collector审计仍阻断，当前训练NOT_READY。

接口D48是metadata预留，普通阶段0/软件开发使用已消费或synthetic fixtures，不需要运行48个新task。D48不做teacher/policy/recipe/checkpoint效果选择；不得以“接口测试”名义消耗未计账的模型/环境调用。若未来确需真实接口科学调用，须另行授权和记账，不能把其标签拿来调配方后称原方案未改。

## 5. 480投入与600评估的边界

支持480作为可行metadata envelope，不等于支持现在支付全部采集成本。固定96全局d均值12.5使原纸上上界仍为8,496 generations、9,792含reset操作；完整480为42,480/48,960，多出的384最多增加33,984/39,168，尚无可用新yield证据证明值得。新单K1原地handoff collector/pin/receipt、训练初始化/token-mask约束及单独授权依赖保持；不套用旧R19运行器，不改原85/2da。11个nonlight余量也很薄，不能当绕过metadata/integrity风险的补样池。

E600的family数为221/158/102/56/63。主效应是该预定五家族近容量比例（有限舍入）的task-micro成功率差，不是五家族等权宏平均，更不是六家族或整个ALFWorld。family效果只描述，无light结论。仍沿C>A/C>B、exact McNemar+Holm、观测净5pp/gross harm≤5%及边际Newcombe10；总体600时30 net/30 loss计数不变。原假设同质单pair功效表不是这个五family固定quota或共同两比较的功效认证，不能搬成新power PASS。

协调方scene-proxy元数据中，480草案采集与E600有97个数字folder suffix重叠，E600的103个suffix都与known-use共享。suffix只是场景/布局代理、非环境规范认证；所以既不据此宣判实际完全同场景，也不允许声称scene-disjoint/novel templates。97是协调方480草案的数，未计算或声称96子集的具体重叠。可支持的评估名为“task-disjoint TRAIN evaluation”，不叫heldout/新环境泛化。

600三臂评估仍可能最多90,000次generation、91,800含reset操作，非免费；接口D48本建议科学调用0。采集或学习机械可行也不自动释放评估。通过元数据容量检查、通过资源guard、证明学习收益是三个不同结论；当前只有纸上可分配性结论，科学许可仍NOT_GRANTED。

## 6. 与旧交付的关系与冻结

本文是追加修订，不重写旧CONTROLLED_POOL_AND_LEARNING_DESIGN.md、design_parameters.json、FILE_HASHES或commands.log。旧六家族条件与对应配额由本文/新增five_family_design_parameters.json显式覆盖；未提及的安全、反泄漏、质量对称、label代数、无重试、真实曝光/recipe和独立review约束保留。并未认可480科学投入或发布任何新执行权限。

本次仅读取协调方三个metadata摘要及自身冻结文件，stdlib整数纸算；未执行旧脚本、项目validator/analyzer/pytest、tokenizer/模型/环境/训练/G3/G4/preflight/policy replay，未创建实际task schedule/gate/launch argv，不改旧科学树/证据/索引，不commit/push/派agent。新科学调用0，R19累计5142/7949（含177/342）及旧证据不变。新增独立hash清单只绑定本补充；协调方继续独立评审和发布。
