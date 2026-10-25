# SI-P0 独立验收标准
本文件是协调方审查标准，不是开发者自评、实验预检或科学执行许可。科学source2da/analyzer85不变，新模型/环境/训练调用上限0。

## 证据
1. 从真实逐episode字段重数，成功使用环境won，不用自然语言自评。配对按canonical trial/split、seed、reset、schedule、horizon、输入接口核对；记录匹配不弥补历史launch/runtime receipt缺失。
2. 专家SFT、普通自身成功、同前缀rescue、neutral/harm/incomplete、oracle-over-K分开。G3不完整原source不当负样本。R19两oracle额外病例CONTINUE原本成功，不能当新增救回。
3. 任务/episode/prefix/branch/action多个统计层级不得互换。跨R16–R18同prefix与同K alias去重；跨base/SFT不同actor不合并成独立训练队列。已有小样本不虚构power。
4. 哈希必须先核对定义：原始文件bytes与canonical JSON不同，旧protocol生成器sha256_value须使用原定义。审计工具的CONTRADICTED也要独立复核。当前文件匹配不证明历史加载。
5. 精确相同输入存在不同合法专家目标，只能报告观测歧义/多解候选；不直接称错误、解释pick-two失败或要求改冻结输入/数据。

## 学习与创新
6. 干预价值不等于学习价值：同一任务的救回只说明当次动作结果；要证明可学习收益，须只用动作前公开输入训练，并在独立未用于选择/调参的任务上比较新权重。
7. A冻结强SFT基座；B普通成功自训练；C纠错增量候选。C>A与C>B是整体方案必要比较，不能单独隔离筛选机制。若主张筛选机制，B必须改为同一candidate pool的success-only采纳，或增加同池恢复成功不做增益筛选的D；不能一边混淆数据来源一边声称机制成立。
8. 等资源包括数据生成、配对验证、discarded/incomplete成本与训练；相同训练tokens不等于相同总成本。不能靠复制少数救回样本制造N或match预算后声称覆盖足够。公共输入、actor和checkpoint规则相同，禁止终局/未来结果进推理输入。
9. 最近文献已有reflection→verified-success→selftraining、paired rescue/harm、数据学习效用选择。区别须落到可证伪的具体比较；不宣称首次。候选“增量有利的干预样本是否更可学习”是研究问题，不是已成立方法。
10. 没有干净独立任务空间、可靠来源或足够独立纠错覆盖，则NOT_READY；不为了阳性扩大采集或反复调prompt。保留可成立的专家SFT/恢复边界实证主线，不强行包装成自主self-improvement。

## 本阶段结束条件
Luna与Sol返回冻结证据、真实subprocess收据和hash，协调方独立抽查并做主张矩阵、协议审查与后续路线裁定。所有缺口精确标明，不能以二者自评PASS代替。后续实现/训练/新评估只有具体协议与资源/数据边界闭合后另立阶段，旧one-shot许可不复用。
