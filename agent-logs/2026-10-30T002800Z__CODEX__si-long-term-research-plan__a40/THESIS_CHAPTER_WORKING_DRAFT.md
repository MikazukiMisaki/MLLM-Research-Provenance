# Draft thesis text: self-improvement and bounded recovery

*Working draft for supervisor review. Integrate with the institution's thesis template and insert independently checked bibliography entries before submission. The study names below are internal identifiers, not claims of novel algorithms.*

## Experimental setting and research questions

This study investigates whether supervised continuation training on an agent's own successful experience improves task success relative to a fixed starting policy and a continuation trained on expert experience. We use Qwen3-8B [4] in ALFWorld [3], a text-based interactive task environment. The common starting policy, P0, is an expert-supervised checkpoint. The primary outcome is binary task completion under the frozen evaluation configuration, with at most 50 environment actions per episode. A separate exploratory study examines the consequences of varying the duration of a bounded recovery intervention. The studies address related but distinct questions; their outcome denominators and treatments are not interchangeable.

## Position in prior research

Prior work has already investigated improving language agents with their own generated trajectories. Re-ReST trains agents on self-generated trajectories and uses an additional reflector to improve low-quality samples, including experiments in ALFWorld [1]. Sarukkai et al. construct a database of successful self-generated trajectories primarily for in-context use, and also examine fine-tuning on this database [2]. The present work therefore does not claim to introduce self-generated agent experience or successful-trajectory training.

Our empirical question is narrower: starting from the same expert-supervised checkpoint and a fixed action interface, how do a self-success continuation and an expert-data continuation compare on a fixed paired task schedule? The continuation data were matched on supervised-token dose and family-level parent counts, but their tasks, states and input-token totals differ. Consequently, the comparison does not isolate experience source as a single causal factor. Its contribution is a documented experimental comparison and failure analysis, subject to the limitations stated below; a methodological novelty claim requires a broader related-work review.

## Supervised continuation comparison

Three policies were evaluated. A is the unchanged P0 checkpoint. B is a continuation from P0 trained on expert demonstrations. C is a separate continuation from the same P0 trained on actions from P0's own successful trajectories. Neither continuation starts from the other's checkpoint. Each continuation uses 78 distinct training parent tasks and 312 unique samples, presented for four epochs (1,248 microbatches and 78 optimizer updates); both have 6,240 supervised tokens over training. The expert and self-generated sets differ in source tasks and states. The input-token totals were 661,620 for B and 695,872 for C, so matched supervised-token dose does not imply equal input computation or identify data source as the sole causal difference.

The fixed evaluation schedule contains 82 tasks from 82 distinct parent directories in the ALFWorld TRAIN partition. Each policy was evaluated once per task, in the same task order and with the corresponding environment seed, producing 246 completed episodes. Identity checks covered recorded task names, parent directories, and available source-file bytes; these checks do not establish a complete history of prior exposure, unseen layouts, or semantic independence. The schedule is an exploratory fixed development sample, not a certified held-out test set. Each of B and C has one training seed and one final checkpoint. Thus the experiment does not estimate variability across training seeds.

The two frozen primary comparisons were C minus A and C minus B on matched tasks. We report the paired win/loss counts, two-sided exact McNemar tests with Holm correction across these two comparisons, and conservative simultaneous 95% intervals constructed from four 98.75% Clopper–Pearson marginal intervals. Population interpretations of both the tests and intervals require appropriate sampling, exchangeability, or model assumptions, which were not established for this fixed task schedule. The predetermined positive decision required complete results without missing outcomes, both Holm-adjusted comparisons to be significant at a family-wise level of 0.05, and both observed differences to be at least +10 percentage points, with no family warning. A family warning meant an observed C−A difference of at most −10 percentage points in any task family; a primary warning meant an observed C−A or C−B difference of at most −10 percentage points. These family comparisons were descriptive, not tests of subgroup safety. This rule was not changed after results were observed.

## Results of the self-improvement pilot

| Policy | Task successes | Success rate |
|---|---:|---:|
| A: fixed P0 | 65/82 | 79.27% |
| B: expert continuation | 68/82 | 82.93% |
| C: self-success continuation | 67/82 | 81.71% |

For C versus A, there were 3 paired wins, 1 paired loss, and 78 ties, for a difference of +2.44 percentage points. The unadjusted exact p value was 0.625, the Holm-adjusted p value was 1.00, and the conservative simultaneous 95% interval was [−7.98, +12.42] percentage points. For C versus B, there were 3 wins, 4 losses, and 75 ties, for a difference of −1.22 percentage points; the unadjusted and Holm-adjusted p values were both 1.00, and the corresponding interval was [−13.78, +11.54] percentage points. The predeclared decision was inconclusive. The data do not establish an advantage of self-success continuation over either comparator, and the intervals do not support claims of equivalence or of harm smaller than five percentage points.

The formal evaluation completed all 246 episodes with no unresolved episode records. It consumed 5,001 model generations and 5,247 environment operations including resets. Training B and C together with evaluation used 6,063.34 allocated device-seconds; separate engineering probes used another 455.86 device-seconds. These are measured research costs, not latency estimates for a deployed policy.

## Descriptive failure analysis

A retrospective inspection covered all nine distinct tasks on which either primary paired comparison disagreed and all eight two-object tasks, a total of 17 tasks and 51 trajectories. This subset was selected using observed outcomes and is not a new randomized comparison. All 37 unsuccessful trajectories recorded done=true and reward zero on their 50th action. This record alone does not establish the mechanism of termination. The recorded 2,206 generated actions in the subset could be reconstructed under the frozen action mapping and matched the executed requests. No parser-to-request action mismatch was observed in these 2,206 recorded actions; this does not exclude unrecorded pipeline faults, establish that actions were appropriate, or show that other tasks were error-free.

None of A, B, or C completed any of the eight evaluated two-object tasks. Each continuation's training set contained only two distinct parent tasks and eight unique examples in that category. This limited coverage motivates a prospective hypothesis about training coverage, but the present data do not show that it caused the failures. Repeated command patterns appeared in some failing trajectories; because failed episodes were generally longer than successful ones and repetition may be legitimate, these observations do not establish a causal loop mechanism. On the 11 discordant paired comparisons, recorded model inputs, observation, and action-map hashes agreed immediately before the first different executed command; this does not establish equality of unrecorded environment state or that the divergence caused the ultimate outcome.

## Exploratory recovery-duration study

In a distinct enriched TRAIN-development sample, 36 eligible prefixes were retained from 39 attempted prefixes. The no-recovery CONTINUE condition uses the source policy's recorded continuation, whereas the K1–K5 conditions examine the measured common recovery path with handoff after up to one through five recovery actions. CONTINUE and K2 each succeeded on 30/36 prefixes, with each succeeding where the other failed in two cases. On the recorded logical full-branch cost measure, K2 averaged about 31.9% more tokens than CONTINUE. These are logical costs of reconstructed branches, not total physical research expenditure or a deployment-latency measurement.

The best fixed K among K1–K5 succeeded on 30/36, while a hindsight choice among the five observed K outcomes succeeded on 32/36, a difference of 2/36 or 5.56 percentage points. Both the best fixed K and this envelope are selected and evaluated on the same sample. The two cases contributing to the difference from K2 were already solved by CONTINUE, so they are not two additional rescues over CONTINUE. The envelope uses future outcomes and is an empirical opportunity measure over the tested paths, not a deployable stopping policy or a population upper bound. The sample was enriched for controls, included only six failure-stratum prefixes and no eligible two-object prefix, and was not a held-out evaluation. Its statistics cannot be combined directly with the 82-task continuation experiment.

## Discussion and limitations

The principal contribution of the pilot is a controlled, paired comparison of two continuation-data sources from a common checkpoint, with measured exposure, costs, case-level diagnostics, and an explicit inconclusive outcome. It does not demonstrate autonomous improvement or isolate data source from task and state distribution. Nor does the recovery study demonstrate a useful adaptive controller. The results can inform hypotheses about data coverage, trajectory quality, and intervention costs, but they do not justify selecting a mechanism on these same outcomes and then treating it as independently validated.

The evaluation schedule is a fixed subset of TRAIN; historical exposure and layout separation remain incompletely known. There is one trained seed per continuation, and subgroup counts are small. The original frozen extraction tool failed after evaluation because its tokenizer symlink interface did not match the environment. It had already read result-file bytes for hashing but did not complete result parsing or statistics. An independently reviewed technical amendment corrected this offline extractor; the original analysis plan, thresholds, data, and failure receipts were retained. No claim is made that no person or process had previously seen the results. For remote provenance, eleven large raw archive fragments have matching reported remote Git blob identities, but the original connector outputs were not separately retained and the fragments have not undergone independent full-content redownload verification.

The next study should be designed only after a trustworthy independent task source and documented exposure history are established. Before execution, the estimand, task and seed dependence, primary contrasts, minimum worthwhile effect or interval precision, multiplicity, missing outcomes, and full compute budget should be specified and independently reviewed. A retrospective two-object coverage hypothesis requires a prospective task selection and evaluation design. If the necessary task isolation or precision cannot be established, the present controlled comparison and its limitations remain a valid descriptive thesis result rather than a basis for a confirmatory efficacy claim.

## Working references

[1] Zi-Yi Dou, Cheng-Fu Yang, Xueqing Wu, Kai-Wei Chang and Nanyun Peng. “Re-ReST: Reflection-Reinforced Self-Training for Language Agents.” *Proceedings of EMNLP 2024*. https://aclanthology.org/2024.emnlp-main.861/

[2] Vishnu Sarukkai, Zhiqiang Xie and Kayvon Fatahalian. “Self-Generated In-Context Examples Improve LLM Agents for Sequential Decision-Making Tasks.” arXiv:2505.00234v3, 2025. https://arxiv.org/abs/2505.00234

[3] Mohit Shridhar et al. “ALFWorld: Aligning Text and Embodied Environments for Interactive Learning.” ICLR 2021; arXiv:2010.03768v2. https://arxiv.org/abs/2010.03768

[4] An Yang et al. “Qwen3 Technical Report.” arXiv:2505.09388, 2025. https://arxiv.org/abs/2505.09388

References are preliminary; verify bibliographic details and formatting against the institution's requirements and complete the related-work review before submission.
