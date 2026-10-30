# Self-improvement of a language-model agent: research update

**Question.** Can a language-model agent improve task completion by learning from its own successful experience, and how does this compare with continuing training on expert demonstrations?

**Study.** Starting from the same expert-supervised Qwen3-8B policy (P0), we compared P0 with two continued policies: one trained on expert data and one trained on the agent's successful trajectories. The continuation datasets were matched by task-family parent counts and supervised-token dose, but used different tasks and states. Self-success data consist of selected actions from previously collected successful P0 trajectories, not evidence of improvement without expert or environmental supervision. All three checkpoints were evaluated on the same 82 ALFWorld TRAIN tasks; each continuation used one training seed.

| Policy | Tasks completed |
|---|---:|
| P0 (unchanged) | 65 / 82 (79.3%) |
| Expert-data continuation | 68 / 82 (82.9%) |
| Self-success continuation | 67 / 82 (81.7%) |

**What we can conclude.** On these tasks, self-success minus P0 was +2.44 percentage points and self-success minus expert continuation was −1.22 points. Both predeclared paired comparisons had Holm-adjusted p = 1.00; the result is inconclusive. It does not establish an improvement, equivalence, absence of harm, or an isolated effect of data source. The fixed TRAIN schedule, one seed per continuation, and incomplete knowledge of historical task/scene exposure limit generalization.

**A descriptive observation.** None of the three policies completed the eight evaluated two-object tasks. Each continuation dataset contained two parent tasks in this category. Low coverage is a possible explanation, but the evidence is retrospective and does not identify a cause; task difficulty, trajectory quality and differences in states are alternatives.

**Separate recovery study.** On 36 selected development prefixes, the recorded original-policy continuation and the best fixed recovery duration each succeeded on 30; a hindsight choice among five measured durations succeeded on 32. This 5.56-point hindsight gap over the best fixed duration is not the performance of a deployable controller. The two cases responsible for the gap were already successful under the original continuation. The best fixed duration was also selected on this development sample; this separate study did not evaluate the SI-U1 continuation-trained policies or establish a self-improvement effect.

**Position and next decision.** Training on an agent's successful trajectories is established prior work, including in ALFWorld; our contribution is a transparent comparison of the specified pipelines, failure analysis and evidence about their limitations, not invention of the general method. A new evaluation should not be designed until independent tasks, a testable hypothesis, defensible precision and a complete budget are supported and independently reviewed. The present task inventory and exposure history do not yet meet that standard. In parallel, the existing results can support a carefully scoped thesis with an inconclusive finding.

**Questions for discussion.** Would you consider this bounded empirical comparison, its inconclusive findings, and the documented failure cases suitable as the thesis's main contribution? If further evidence is essential, which claim and thesis requirement should we prioritize before committing to new data or computation?

*Working brief for discussion; no new experiment is proposed or authorized by this document. Detailed evidence: SI-U1 formal review and R19 independent G4 review, cited in the accompanying thesis working draft.*
