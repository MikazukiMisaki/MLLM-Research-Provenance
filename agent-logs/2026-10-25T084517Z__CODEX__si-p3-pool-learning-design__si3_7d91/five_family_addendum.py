"""Additive SI-P3 capacity/design arithmetic only; never instantiate task schedules."""
from pathlib import Path
import hashlib,json,math,datetime
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T084517Z__CODEX__si-p3-pool-learning-design__si3_7d91')
COORD=OWN.parent/'2026-10-25T084517Z__SOL__si-p3-controlled-experience-design__si3_7d91'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def new(name,obj):
 p=OWN/name
 with p.open('x',encoding='utf-8') as f:
  if isinstance(obj,str):f.write(obj)
  else:json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')
 return {'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
expected={'independent_capacity_metadata.json':'b245b93819b513561b86bb3e614f607ecdddc7b7e640a13eabc21938952ec93c','family_capacity_scope_feedback.json':'6c2bd1b2d3f59489048dfbe76fa66f6db4d2494783a4e176b564bd41f51db290','independent_scene_proxy_overlap.json':'50fbee9ca68c9ae2f9276fd9b7ff839f5e50143b217c235305fd6a7222045012'}
bindings=[]
for name,h in expected.items():
 p=COORD/name;assert sha(p)==h;bindings.append({'path':str(p),'sha256_before':h})
old_manifest=OWN/'FILE_HASHES.sha256';assert sha(old_manifest)=='b9905b0acee1e8be477c66e903cd67bd319b38592c2e160b139a37a66056fe97'
old=[]
for line in old_manifest.read_text().splitlines():
 h,p=line.split('  ',1);assert Path(p).is_relative_to(OWN);assert sha(Path(p))==h;old.append({'path':p,'sha256':h})
assert len(old)==24
meta=json.loads((COORD/'independent_capacity_metadata.json').read_bytes());allcap=meta['complement']['train']['family_counts'];assert sum(allcap.values())==1141 and allcap['look_at_obj_in_light']==2
order=['pick_and_place_simple','pick_clean_then_place_in_recep','pick_cool_then_place_in_recep','pick_heat_then_place_in_recep','pick_two_obj_and_place']
cap={k:allcap[k] for k in order};assert list(cap.values())==[419,301,194,106,119] and sum(cap.values())==1139

def hamilton(n):
 den=sum(cap.values());base={f:n*cap[f]//den for f in order};extras=n-sum(base.values());rank=sorted(order,key=lambda f:(-(n*cap[f]%den),f))
 for f in rank[:extras]:base[f]+=1
 assert sum(base.values())==n
 return base
quotas={str(n):hamilton(n) for n in [24,48,96,120,384,480,600]}
stage2={f:quotas['480'][f]-quotas['96'][f] for f in order};assert sum(stage2.values())==384 and all(x>=0 for x in stage2.values())
res480={f:cap[f]-quotas['480'][f]-quotas['48'][f]-quotas['600'][f] for f in order}
res96={f:cap[f]-quotas['96'][f]-quotas['48'][f]-quotas['600'][f] for f in order}
assert min(res480.values())>=0 and sum(res480.values())==11 and sum(res96.values())==395
# Count matrix only. No task IDs, game paths, runnable schedules or gates are created.
d=[5,10,15,20];prefix={f:{str(k):quotas['96'][f]//4 for k in d} for f in order};cursor=0
for f in order:
 for j in range(quotas['96'][f]%4):prefix[f][str(d[(cursor+j)%4])]+=1
 cursor=(cursor+quotas['96'][f]%4)%4
assert all(sum(prefix[f][str(k)] for f in order)==24 for k in d)
assert all(max(prefix[f].values())-min(prefix[f].values())<=1 for f in order)
qmin={f:(5*quotas['96'][f]+7)//8 for f in order}
mathobj={'scope':'PAPER_INTEGER_ARITHMETIC_ONLY_NO_TASK_DATA_OR_POLICY_EXECUTION','source_metadata_sha256':expected['independent_capacity_metadata.json'],'fixed_denominator':1139,'excluded_light_candidates':2,'capacity_nonlight':cap,'rounding_rule':'For each n use ORIGINAL capacity weights cap_f/1139; floor and largest integer remainders; ties canonical family string ascending; do not recompute weights after each reservation','hamilton':quotas,'deferred_384_must_be_480_minus_96':stage2,'independent_H384_is_not_same_as_difference':stage2!=quotas['384'],'independent_96_plus_H384':{f:quotas['96'][f]+quotas['384'][f] for f in order},'full_envelope_residual_nonlight':res480,'full_envelope_residual_total_including_light':13,'only96_acquisition_with_same_E600_D48_nonlight_not_acquired_or_reserved_to_current_acquisition':res96,'only96_nonlight_remaining_total':395,'only96_with_light_remaining_total':397,'prefix_count_matrix_not_schedule':prefix,'prefix_d_global_counts':{str(k):sum(prefix[f][str(k)] for f in order) for k in d},'prefix_d_mean':12.5,'quality_min_per_family_ceil_5_over_8_of_stage1':qmin,'foreground24_per_family':quotas['24'],'neutral_min_per_family':quotas['24'],'background120_per_family':quotas['120'],'training_geometry_unchanged':{'foreground24':24,'background120':120,'per_arm_examples':144,'epochs':2,'effective_batch':16,'optimizer_updates':18},'acquisition_cost_ceiling96':{'generations':8496,'reset_inclusive_operations':9792,'generated_tokens':138240},'acquisition_cost_ceiling480':{'generations':42480,'reset_inclusive_operations':48960,'generated_tokens':691200},'incremental_384_cost_ceiling':{'generations':33984,'reset_inclusive_operations':39168},'future600_three_actor_eval_ceiling_no_dev_calls':{'generations':90000,'reset_inclusive_operations':91800},'all_science_calls_this_addendum':0}
arts=[new('five_family_capacity_math.json',mathobj)]
parameters={'schema':'SI_P3_FIVE_FAMILY_DESIGN_ADDENDUM_V1','status':'DESIGN_ONLY_NOT_AUTHORIZED_NOT_A_SCHEDULE_OR_GATE','precedence':'Overrides only v1 population/family quotas/dev reservation and corresponding S/C composition; all unchanged integrity/privacy/one-first-action/cap/EOS/source-pairing/token/recipe rules carry forward. Old files remain immutable.','metadata_scope_accepted_as_design_basis':{'population':'Five nonlight TRAIN families only','capacities':cap,'light2':'Excluded from collection/dev/evaluation; retained unread/unrun','official_heldout_or_scene_novelty':'No such claim'},'coordinator480_48_600_envelope':'Arithmetic-feasible metadata reservation, not endorsement of spending/launch','unique_investment_recommendation':'At most96 as one separately reviewed future feasibility tranche; 384 DEFERRED_NO_GO without new scientific/financial review, never a quota top-up; no automatic train or evaluation','metadata_envelope_quotas':{'E600':quotas['600'],'D48':quotas['48'],'A480':quotas['480'],'unallocated_nonlight11':res480,'unallocated_light2':2},'first96_and_deferred384':{'A96':quotas['96'],'A384_reserved_difference':stage2,'freeze_both_before_outcomes_if_envelope_adopted':True,'do_not_re_Hamilton384':True,'actual_task_ID_manifest_created_here':False},'interface_development48':{'scope':'Identity/interface reservation only, no policy/teacher/recipe/checkpoint tuning','current_fresh_task_model_or_env_calls':0,'ordinary_phase0_software_work':'Use already consumed or synthetic fixtures; no need to open/use48 new tasks','if_later_scientific_calls':'Separate counted authorization, not free preflight or tuning'},'quality_yield_resource_guards_after_fixed96':{'source_slots_complete':96,'Q_pinned_min_total':72,'Q_min_family_ceil_5n_over8':qmin,'C_min_total':24,'C_min_family_H24':quotas['24'],'neutral_min_total':24,'neutral_min_family_H24':quotas['24'],'B_min_total':48,'stop_instead_of_expand_to_fill':True,'no_learning_N_theorem':True},'conditional_learning_composition_not_approved':{'C24_family_quota':quotas['24'],'B24_family_quota':'Same as C24, plus exact actual supervised-token-length composition; sample from ALL B including C, no CONTINUE exclusion or redraw','S120_family_quota':quotas['120'],'S_source':'Existing consumed expert_train only, each task one precommitted quality/hash anchor; capacity/actual tokens still NOT_VERIFIED, no fresh-task substitution','seed':42,'epochs':2,'effective_batch':16,'optimizer_updates_per_arm':18,'examples_per_arm':144,'per_new_task_exposure_cap':2,'checkpoint':'Final18 only, not selected by effect','real_tokenizer_and_initialization_checks':'BLOCKING_NOT_PERFORMED; same constraints as original design','B_contains_C_and_labels':'Unchanged; within successful B, C is exactly CONTINUE failure filter'},'evaluation':{'task_count':600,'family_quota':quotas['600'],'estimand':'Task-disjoint TRAIN evaluation on precommitted five-family capacity-proportional mixture (rounded finite cohort), not equal-family macro mean, not all-six-family/official-heldout/new-scene performance','co_primary':'C>A and C>B, original exact McNemar/Holm and5pp/gross-harm criteria unchanged','N600_power_certified':False,'paper_power_scope':'Original homogeneous single-pair hypothetical table not a power certificate for this stratified/co-primary study'},'scene_proxy_limit':{'coordinator480_draft_acquisition_vs_eval_suffix_overlap':97,'eval_proxy_groups_already_shared_with_known_use':103,'proxy_is_actual_scene_equality_proof':False,'no_claim_actual96_subset_overlap_computed':True},'source_bodies_read':False,'science_calls_added':0,'historical_R19_cost_unchanged':'5142/7949 including177/342','no_commit_push_shared_index':True}
arts.append(new('five_family_design_parameters.json',parameters))
md='''# SI-P3 五家族容量修订与投入建议 Addendum

本补充保留先前24项交付及FILE_HASHES原字节。独立metadata已使初稿“六家族均衡96/60/600、每family至少126候选”的条件明确不成立：light只有2，而非足以支撑其独立采集/开发/评估配额。初稿的六家族quota与六家族普遍性说明由本文显式取代；没有新科学调用，也不把旧条件失败当实验失败。

**判断：支持五个非light家族作为唯一主总体、light2不运行、TRAIN task-disjoint评估及固定容量比例/Hamilton。480+48+600是算术可行的metadata预留包；我仍不建议据此一次承诺480采集投入。唯一推荐仍是仅将固定96例作为下一次单独审查/授权候选，384明确DEFERRED_NO_GO，不作为采够rescue的后续。** 当前全部采集、训练、评估许可均NOT_GRANTED。

## 1. 证据与总体的明确更换

只读取协调方independent_capacity_metadata.json、family_capacity_scope_feedback.json、independent_scene_proxy_overlap.json，SHA见新增source bindings；未重跑其脚本，未读未消费game/traj_data/outcomes，也未读取Luna未完成文件。独立metadata的TRAIN总1141，其中light2、pickplace419、clean301、cool194、heat106、picktwo119，非light合计1139；known-use union2612排除保持。metadata差集仍不是“从未看过”的证书。

这不是把light缺额随手转给其他家族：研究总体改为五个非light TRAIN家族，全部quota从新固定总体容量重新计算并逐列公开；不再声称六家族均衡。2个light留存不运行，不进入B/C/dev/E，也不从74官方unseen补light。若将来学生在light退化，本设计没有评估凭据，不能声称保持全六家族能力。

## 2. 可核查的整数容量方案

固定weights为原非light容量N_f/1139；对每个总额n先取floor(n*N_f/1139)，剩余按整数余数降序分配，完全平手按canonical family字符串升序。不同分区都用这组原weights，不在切掉eval之后偷偷重算分母。以下是纸上配额，不是已创建的task schedule：

| family | 可用metadata | E600 | 接口D48 | A480预留上界 | 96一期 | 384差额 | 全480包余量 |
|---|---:|---:|---:|---:|---:|---:|---:|
'''
for f in order:md+=f"| {f} | {cap[f]} | {quotas['600'][f]} | {quotas['48'][f]} | {quotas['480'][f]} | {quotas['96'][f]} | {stage2[f]} | {res480[f]} |\n"
md+='''
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
'''
for f in order:md+=f"| {f} | {quotas['24'][f]} | {quotas['24'][f]} | {quotas['120'][f]} | {qmin[f]} |\n"
md+='''
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
'''
arts.append(new('FIVE_FAMILY_CAPACITY_ADDENDUM.md',md))
for b in bindings:
 b['sha256_after']=sha(Path(b['path']));b['unchanged']=b['sha256_before']==b['sha256_after'];assert b['unchanged']
for b in old:assert sha(Path(b['path']))==b['sha256']
assert sha(old_manifest)=='b9905b0acee1e8be477c66e903cd67bd319b38592c2e160b139a37a66056fe97'
arts.append(new('five_family_addendum_source_bindings.json',{'input_bindings':bindings,'old_manifest_sha256':sha(old_manifest),'old_24_files_unchanged':old,'scope':'Read coordinator metadata summaries only; no independent task-body/freshness/ID-list audit or another agent unfinished files','coord_proxy_counts_apply_to':'Coordinator480 metadata draft, not a new96 subset result','all_science_calls_added':0}))
arts.append(new('FIVE_FAMILY_ADDENDUM_RECORD.md','''# SI-P3五家族追加记录

只使用本目录新写five_family_addendum.py（OWN由自身__file__断言），读取协调方三个metadata JSON与自身已冻结文件；没有执行其脚本、前轮脚本或任何项目模块。纸上Hamilton使用整数余数与固定canonical tie-break，配额表不包含task IDs，不是可执行schedule/gate。3个metadata摘要的before/afterSHA见新增source bindings；不独立声称已复核未消费task或freshness。

接受五非light总体与固定容量Hamilton为设计基础，480/48/600算术可行但只接受为metadata envelope；唯一推荐仍为96一期的未来单独授权候选，384 DEFERRED_NO_GO。显式修订旧六family配额、D60为D48接口reservation、C/S family组成；总学习例24+120、18更新、原token/recipe及阻断条件不变。没有silent quota transfer或重抽B以排C。旧24交付、FILE_HASHES和commands.log均保持，新增回执/command log/hash单独保存。

真实程序stdout/returncode和程序SHA由five_family_addendum.receipt.json及同名log保存；不是项目测试或独立review PASS。新科学调用0，无模型/环境/训练/tokenizer/旧脚本/项目analyzer/validator/pytest/preflight/G3/G4或policy replay；无旧证据、共享INDEX/科学树改动、commit/push或agent派发。原R19累计5142/7949含177/342不变。协调方独立评审/统一发布，所有后续科学工作须新授权。
'''))
print(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'hamilton96':quotas['96'],'hamilton480':quotas['480'],'deferred384_difference':stage2,'hamilton600':quotas['600'],'residual_full_envelope':res480,'old_files_unchanged':24,'current_scientific_permission':'NOT_GRANTED','science_calls_added':0,'artifacts':arts},ensure_ascii=False,indent=2))
