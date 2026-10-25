# SI-E1静态风险裁定：仅新增合同/负向测试，不修历史组件

独立critic与协调方读取冻结85代码，发现以下**旧helper能力限制**，尚无candidate缺陷结论。请在新增合同层处理，不扩修原R19：

1. old _reserve_model_call只计generation次数，_generate_exact在backend._load之后才tokenize；新预算必须在实际generation前对已知input tokens/8192/16M及count reserve，超限不发调用，已用reset照记。别把旧count-only当新input caps已实现。
2. old DurableEventJournal load已有operation key缺kind，append无online state机；registry.complete可收任意receipt。新层要拒绝cross-kind complete、completed physicalID重用、错run/task/seed、无start完成；durable事件/trajectoryhash/registry完成顺序和中断不可自动再跑。可wrapper或新增strictledger，不改旧frozenhelper。
3. generation token_ids长度/count/hash/阶段帽必须互相一致。**不要悄悄改变原P0 actor执行语义**：原actor parse_p2_selection并不以output_complete决定是否执行；若原raw本身合法但EOS未到，保留原P0parser决策/标志，不能把新teacher完整性规则套到source/actor来改Y0。teacher Stage1/Stage2完整性按其真实production parser，complete=true/cap=true保留；外部调用完成receipt与EOS-complete是两个概念。若这和你的Q解释冲突，明确报告，先不扩改source policy。
4. old run_sft_suffix会新reset/replay环境，不能用于新singleK1原地handoff。集成fixture给环境不可伪造instance_id/reset counter，teacher后P0必须同实例，teacher终态不用suffix。invalid/no executedteacher=YT NA，不用旧success默认0代替。
5. oldtrain_lora freshbase+freshLoRA+bestval不是newwarmstart。旧maskhelper算出的labels在旧trainer中被丢弃让TRL再tokenize；新审核看真实collated shifted labels/分母/梯度，不只看中间helper。installed TRL0.23 collator本身按position pad -100，没有已证EOS==PAD bug，别修想象bug。
6. paired144slots×2epochs应共144个microbatch（每批2）、18updates（accum8），而非每epoch18updates；保持逐slot target/EOS长度、sharedshuffle与new/all累计prompt ratios。B排序允许C，selected7neutral拒绝、8边界允许，无redraw。

这些是原授权工程的具体负向合同，不是新scope/实验。保持无8B/env/真实训练，原R19无需维修。测试tiny PEFT/软件toy与tokenizer-only活动据实单列；不声称actualP0加载PASS。
