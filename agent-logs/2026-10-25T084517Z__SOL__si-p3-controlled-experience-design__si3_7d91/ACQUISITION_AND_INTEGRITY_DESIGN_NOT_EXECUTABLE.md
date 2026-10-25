# SI-P3 数据生成与完整性设计：非执行附件

本附件不新增可执行schedule/gate或代码实现。最终数值和采纳由MINIMAL_CONTROLLED_EXPERIENCE_PROTOCOL.md及独立review负责；作者初稿不能自行提供科学执行许可。

## 单任务物理流程与不可混淆的标签

1. 先固定task分区、source order、每task唯一anchor规则、环境种子及模型/adapter/tokenizer/runtime/输入版本。原P0独立生成一条最多H50的source，保存每个动作前公共状态、原action map/ID/命令、原prompt/token/raw/parse、动作后状态、done/won/reward/truncated和真实receipt。source终局R_A仅作为学习采纳的离线反馈，不回流到teacher或学生prompt，也不用于挑另一个anchor。
2. 若在固定anchor前已终止/无有效状态，保留NO_ELIGIBLE_STATE；不替换task、不选另一个前缀。预期的malformed/invalid/truncated模型输出按原fail-closed科学路径处理，不能伪装为基础设施异常来重试。Horizon exhausted不是成功。
3. 对每个合格anchor最多一次reset与exact已记录prefix动作replay，0次baseline再生成。逐步比较task/seed/counter、公开goal/observation、完整有序动作map、H4及actor公共prompt；状态或map不同即技术STOP，不得静默重索引、忽略该task后补task，或新采样至匹配。要记录重放来源动作ID、真实command/transition及各操作物理ID。
4. 在同一个恢复环境上最多一次Stage1(40 tokens)+一次Stage2(16 tokens)，只执行第一合法恢复动作K1，接冻结adapter-on P0 suffix，原总horizon仍50。Stage1不合法仍按原协议作一次Stage2诊断性生成但不执行该动作；不repair、不重试、不扩K、不更换teacher。Stage1 complete=true但cap=true本身不是截断；以原输出完整性/parser合同判定。suffix只证明该单步干预后的终局R_T，不自动成为teacher训练标签。
5. 共同质量Q在B/C采纳前对所有尝试适用：完整已执行首teacher动作/合法完整bare ID、公共map唯一映射、原件/生产者身份/完整源与replay/终局收据可核对。已完成但无效输出仍保留在完整池，Q_FAIL不能通过改写target修复。物理生成复用、alias、完全相同public-input/target、task重复均需显式标识，每canonical task最多一个teacher目标。
6. B_pool={Q且R_T=1}；C={Q且R_T=1且R_A=0}。同时报告full N、source reachability、尝试、Q_PASS、B/C/neutral/harm/失败，不只保存positive。C属于B，B抽样不能剔除C。B−C仅作审计。原source CONTINUE是共享的真实baseline证据，不能反复当作新采样成本或重新标注。

## 持久化、预算与停止

事件物理操作ID先reserve/start持久化，再真实调用，后complete及真实返回/成本。trajectory/单位完成需有可验证终局与hash引用后才写完成标记。model input/output token、generation、reset、step、wrapper归类与调用阶段须分账；linked wrappers不重复记外部物理调用。每个完成或技术中断均保留原始journal/manifest/registry/supervisor，追加裁定不得改原status。旧R19失败unit、旧consumed clearance和原G3/G4完全独立。

模型/环境异常、receipt缺失、external operation incomplete、输入/SHA漂移、replay不符、预算将超上限或协议外调用：立即停止整次有界run，保留真实退出和已花成本；不把基础设施错误算任务失败，也不自动retry/换task。预算应在每项外部调用前同时检查分项与累计限额，不能在收尾才发现超支。源轨迹正常完成而teacher无有效target不是基础设施失败；它按预定计数损失候选，不替补。

本设计没有另一次replay-gate pass、actor复生成或G2重跑的隐藏额度。若未来实现需要额外安全/一致性操作，必须事先单列版本/预算并独立审查，不能称它已包含在101N/102N里。原R19 source剩余8999/8999是旧授权的restart debit，不是SI-P3的可用额度；新协议没有继承任何科学预算或clearance。

## 软件到运行的条件

未来生产实现须有完整非空synthetic contract路径：真实actor包装/collector/parser/journal/trajectory/registry/共同质量与dataset接合，只有model/env边界可synthetic；至少覆盖invalid Stage1/Stage2、cap完整输出、source早终止、map/replay差异、append-only异常、预算预留/linked-wrapper去重及B仍可采C。新增实现exact-SHA由协调方独立复审；实际正向预检只能在其另行授权后执行，未运行不能写PASS。

实施前还需冻结实际runtime、模型/tokenizer身份、prompt长度及不截断/上下文fit门槛、input-token/直接计时资源cap、所有允许调用的smoke/dev/采集分账、training实际mask/token匹配与no-retry执行边界。当前这些运行附件尚未存在，不应将科学结构审查通过写成READY_TO_RUN。


## 未执行分支的结果字段

若没有已执行的合法第一teacher动作，保存attempt的原parser/complete/eligibility失败原因与已花成本，恢复后的环境终局R_T标为NOT_OBSERVED/NA，不凭空制造一个done/won的0或1。没有合格teacher动作自然不入B/C，但它留在原N及attempt/invalid分母中。不要把这类无target记录重新标成任务失败或将source成功复制成恢复成功来扩大目标池。只有真实执行后的有效终局才支持恢复成功标签；expected actor/parser fail-closed episode与基础设施incomplete操作分别编码。
