# R18-C2 Scientific Acceptance

**Scientific acceptance: PASS. Primary rendering-benefit hypothesis: unsupported.** Astra accepts the completed run as interpretable null/negative development evidence. Acceptance concerns protocol integrity and usability of the outcomes; it does not mean the intervention succeeded. No new experiment, replay, model inference, environment execution or held-out use was performed during acceptance.

## Execution integrity

The execution implementation SHA remains `aa9fa3c34520941e7e3be00294b111e8254fd65b` on `codex/progress-aware-recovery`. The separate results archival commit is `4f5c2e18e0dfdf48e9471fcba0a3ee715be3ca3b`. The latter contains only the three exact generated outputs and is verified on the authoritative remote branch. It must never replace the execution SHA in experimental provenance.

Astra independently checked the completed manifest, authentic wrapper-captured exit 0 and sealed runner log; all 60 individual branch files against the branch journal, summary, CSV and ledger; each frozen prefix and historical comparator; and exactly one start and completion event per prefix. Replay was exact on 60/60 with zero model calls. Accepted branches and ledger rows were 60; events were 120. C2 completed reruns, incomplete retries, interruptions, comparator reruns, training and held-out usage were all zero. The completed manifest, 23 frozen input hashes, frozen adapter directory hash and all requested Luna result-key fields matched. All 120 recovery prompts contained the assigned frozen card; its chat-serialized prompt hashes matched. No treatment block entered the 1,285 recorded SFT continuation prompts.

The audit passed 674 integrity assertions and 866 analysis assertions. Those are consistency checks over existing records, not additional scientific observations. The paired tests, rescue/harm counts, emitted-text comparisons, actual action categories, loop counts/cross-tabs and cost summaries were recomputed from recorded branches. The sample contains 60 distinct task IDs and schedule indices. The primary analysis retains all 60 prefixes, including withheld interventions.

| Exact generated output | Final SHA256 |
|---|---|
| Report | `f33868ce0fa0849b85a929ad405deb39a9fd7b93a79c8fe2072aeef3074fc9ee` |
| Summary JSON | `5d434346eb8b1a8f2016fa31c640a43e582d4499b24c7b482768c82b944140a7` |
| Pairs CSV | `cf4b7f2eb5ae80e1950d9d0fc2e290f0cbc5a4351f38d754f0052f5363c3d7a7` |

These hashes match Luna's completed execution inventory and the completed runtime manifest, including the actual archived Git blobs. The report's embedded summary digest refers to the summary **before** the artifacts metadata was added; the separately named `summary_sha256_before_hash_field` was verified in memory. It is not the final summary-file digest above. No artifact was regenerated or edited.

Git's existing text normalization initially changed CSV CRLF endings in an unpublished archival blob. The generated file stayed unchanged. Astra replaced the staged blob with the unfiltered original bytes and amended only that unpublished commit; final blob hashes, ordinary clean-worktree status and remote revision were verified. Repository attributes/configuration were not changed. Original CSV line endings are preserved.

Evidence: [independent integrity results](../agent-logs/2026-09-15T014845Z__ASTRA__r18c2-scientific-acceptance__159bf149/integrity-results.json), [analysis verification](../agent-logs/2026-09-15T014845Z__ASTRA__r18c2-scientific-acceptance__159bf149/analysis-verification.json), [archival receipt](../agent-logs/2026-09-15T014845Z__ASTRA__r18c2-scientific-acceptance__159bf149/scientific-archival.json), and [Luna execution record](../agent-logs/2026-09-14T120417Z__ASTRA__r18c2-durable-resume__zgJ2NUTG/RECORD.md) at execution-provenance commit `983f5d52d9cebd1bab8c313472956e31b87497b5`. Historical task records remain unchanged.

## Primary result

**CARD-v2 vs FACT-TEXT is the identical-fact rendering-package effect.** Both receive the same validated canonical public-progress facts. Syntax, labels, layout, tokenization, length and compliance behavior may differ, so this does not isolate a pure abstract representation effect.

CARD-v2 succeeded on 30/60; FACT-TEXT on 32/60. The paired result was **0 wins / 58 ties / 2 losses**, net −2, mean difference −0.033333 (−3.33 percentage points). There were only two discordant pairs. The exact two-sided paired p-value was 0.5; the directional CARD-v2 > FACT-TEXT p-value was 1.0. Both were independently recomputed as binomial tests over discordant pairs.

There is no evidence of CARD-v2 benefit under this protocol. The observed paired direction favored FACT-TEXT in both discordant cases. These data do not establish FACT-TEXT superiority, significant harm, equivalence, absence of an effect, or that rendering never matters. The small discordant count leaves substantial uncertainty; failure to reject is not an equivalence test.

The generated report/schema retain historical labels such as “primary representation effect.” This acceptance note supplies the narrower interpretation without rewriting the archived output. [Exact generated report](https://github.com/MikazukiMisaki/Alfworld-Self-Improvement-Project/blob/4f5c2e18e0dfdf48e9471fcba0a3ee715be3ca3b/reports/PROGRESS_AWARE_RECOVERY_CARD_V2_R18_C2.md).

## Secondary result

**CARD-v2 vs OSR is a combined secondary contrast** involving validated information addition and its structured rendering. It is not the representation effect.

The paired result was **1 win / 57 ties / 2 losses**, net −1, mean difference −0.016667 (−1.67 percentage points), three discordant pairs, exact two-sided p = 1.0 and directional CARD-v2 > OSR p = 0.875. This offers no evidence of a reliable combined benefit. It does not support an inferential ranking of the methods.

## Rescue / harm

| Condition | Successes / 60 | Rescues among 31 CONTINUE failures | Harms among 29 CONTINUE successes |
|---|---:|---:|---:|
| CONTINUE | 29 | — | — |
| OSR | 31 | 4 | 2 |
| FACT-TEXT | 32 | 5 | 2 |
| CARD-v2 | 30 | 3 | 2 |

CARD-v2 rescued 3/31 (9.68%) and harmed 2/29 (6.90%). It had two fewer rescues than FACT-TEXT and one fewer than OSR, with equal aggregate harm counts. Equal counts alone must not be described as proof of equal risk or identical affected cases. The two primary losses, R15-F24 and R15-F27, are missed FACT-TEXT rescues among CONTINUE failures, rather than extra harms to CONTINUE successes. The secondary win, R15-S14, restored a CONTINUE success that OSR lost; it is not an additional rescue among CONTINUE failures.

## Mechanism

The evidence supports a descriptive failure to consistently convert changed recovery behavior into terminal gains. It does not isolate a single causal mediator.

| Link in the proposed chain | What is observed | What remains unproven |
|---|---|---|
| Public evidence → validated facts | R18-B validated 60 fact objects: 353 exact fields, 259 justified unknowns, 48 not applicable; no coded partial/incorrect/unjustified-unknown/ambiguous fields. The two treatments preserve identical facts. | Public semantic validity is not hidden-state completeness or a solution plan. |
| Validated facts → emitted diagnosis/subgoal | C1 vs OSR changed parsed diagnosis text in 54/60 and subgoal text in 51/60; C2 vs FACT-TEXT changed 37/60 and 38/60. | These are parsed-text inequalities, not semantic quality judgments or access to latent reasoning. |
| Emitted text → executed recovery action | C1: 34 same executed actions, 23 different, 3 previously withheld now executed. C2 vs FACT-TEXT: 38 same, 18 different, 4 previously executed now withheld. | The diagnosis/subgoal was not independently randomized; no causal mediation or action optimality is established. |
| Executed action → local trajectory | C2 vs FACT-TEXT reduced recorded loop counts in 11 pairs and increased them in 3. | Reduced repetition may reflect a different or shorter failed trajectory; it does not identify the required solution sequence. |
| Local trajectory → terminal success | The 18 changed-action primary pairs yielded 0 wins / 17 ties / 1 loss; the 11 loop reductions yielded 0 wins / 10 ties / 1 loss. | The precise contribution of missing information, action choice, compliance, limited horizon and later SFT follow-through is unresolved. |

C1's 23 different-action pairs gave 2 wins / 19 ties / 2 losses. Its three execution-asymmetry pairs gave 1 win / 2 ties. C2 vs OSR changed diagnosis/subgoal text in 51/60 and 46/60. Its action categories were 35 same, 19 different, 1 both withheld, 3 prior-executed/current-withheld and 2 prior-withheld/current-executed. The 19 different-action secondary pairs gave 0 wins / 17 ties / 2 losses. Behavior change is demonstrable; useful behavior change is a separate outcome.

Compliance is part of the measured package. C2 had four invalid Stage-1 outputs and four withheld recovery actions, compared with none in FACT-TEXT. Two were overlong subgoals and two were truncated Stage-1 outputs. R15-F24's primary loss involved withholding after an overlong subgoal; R15-F27's involved a different valid executed action. The four withheld primary pairs yielded 0 wins / 3 ties / 1 loss. This is descriptive accounting, not proof that fixing the invalid output would rescue that task. Removing these pairs would change the frozen estimand and bias interpretation.

**Semantic correctness is not sufficient to guarantee actionable recovery information; changed emitted text or action is not sufficient to guarantee useful recovery.** A “Progress-to-Action Actionability Gap” is defensible as a descriptive concept: semantically valid public progress information can alter diagnosis, subgoal and action without identifying or inducing the sequence needed for terminal recovery. It is not a newly validated construct or an isolated causal bottleneck. The fixed operator permits one recovery action and then returns to the unchanged SFT policy, so follow-through remains a plausible part of the gap.

## Pick-two

Among the 18 failure-stratum pick-two prefixes, CONTINUE succeeded on 0, and OSR, FACT-TEXT and CARD-v2 each on 1. CARD-v2's recorded fact-coverage counts were count-aware 18/18, instance-aware 17/18 and location-aware 3/18.

These labels need operational definitions: count-aware means `required_count == 2`; instance-aware means nonempty `known_targets`; the frozen “location-aware” proxy means nonempty `known_unfinished_targets`. They describe available fact fields, not demonstrated model understanding. In particular, this proxy is not an independent direct test that the location of the missing target is known.

The pattern is consistent with an actionability bottleneck: knowing that another object is needed, or knowing a completed object's identity, often does not specify where or how to obtain the missing target. It does not prove that location knowledge is causal or sufficient, or that adding locations would solve pick-two. Unknown instances/locations must not be invented to make the treatment appear complete. No outcome-blind actionability coding was performed in this acceptance task.

## Loop analysis

CARD-v2 vs FACT-TEXT: **11 reduced / 46 unchanged / 3 increased**. Among reductions: **0 primary wins / 10 ties / 1 loss**. Reduced repetition is therefore insufficient evidence of improved terminal recovery in these records. Loops are not shown to be irrelevant.

C1 vs OSR had 5 reduced / 43 unchanged / 12 increased. The loop metric combines adjacent repeats, repeated two-cycles and revisited navigation destinations; these indicators overlap and depend on trajectory exposure. They are descriptive behavior measures, not a validated progress or reasoning score. No post-hoc loop subgroup significance test is used.

## Cost

CARD-v2 local recovery tokens averaged 1,364.5667 (median 1,263). Against FACT-TEXT, mean local token delta was **+7.5667**, median +8; mean treatment-input overhead was +7.2833. Mean local latency delta was approximately **−0.001455 seconds**, with median +0.001588 seconds.

The explanation “CARD-v2 failed simply because it was much longer than FACT-TEXT” is not supported by this small average local token difference. That observation does not isolate tokenization from other rendering features, or rule out output-cap and compliance effects. Historical-arm latency measurements are not a randomized timing experiment and should not be presented as evidence of a speed advantage. Full-branch tokens still differed: mean +584.3167 vs FACT-TEXT, with substantial trajectory variation; local prompt cost is not total episode cost.

Against OSR, CARD-v2 added **164.5833 local tokens** on average and 164.25 treatment-input tokens. C1 added 157.0167 local tokens vs OSR. Added public progress content therefore has a meaningful context cost relative to OSR, without demonstrated reliable terminal gain here.

## Integrated R16 / C1 / C2 interpretation

The marginal progression is CONTINUE 29/60 → OSR 31/60 → FACT-TEXT 32/60 → CARD-v2 30/60. These are matched outcomes on the same frozen prefixes, not four independent samples or three independent replications.

| Stage and paired contrast | Estimand | W / T / L | Net / mean difference | Exact two-sided / directional p | Supported conclusion |
|---|---|---|---|---|---|
| R16: OSR vs CONTINUE | Bounded one-step recovery effect | 4 / 54 / 2 | +2 / +0.033333 | 0.6875 / 0.34375 | Some observed rescues and harms; reliable average benefit is not established. |
| R18-C1: FACT-TEXT vs OSR | Validated added-progress-information effect under the frozen one-step recovery operator | 3 / 55 / 2 | +1 / +0.016667 | 1.0 / 0.5 | Added facts altered emitted text and actions; terminal benefit remains unsupported. |
| R18-C2 primary: CARD-v2 vs FACT-TEXT | Identical-fact rendering-package effect | 0 / 58 / 2 | −2 / −0.033333 | 0.5 / 1.0 | No evidence of structured-rendering benefit; two observed discordances favor FACT-TEXT. |
| R18-C2 secondary: CARD-v2 vs OSR | Combined secondary contrast | 1 / 57 / 2 | −1 / −0.016667 | 1.0 / 0.875 | No reliable combined benefit demonstrated. |

R18-A supplied the public-evidence semantic audit; R18-B corrected only the documented extraction gaps and froze matched renderings before C1/C2 inference. This progression separates semantic validation, information addition and rendering-package changes. None of the three adjacent paired contrasts supports a general improvement claim. Shared comparators, development selection and sequential execution limit generalization. R16's frozen record includes three incomplete retries and zero completed reruns; those historical retries are not C2 retries and are not silently recast as zero.

Sources: [R16 frozen report](https://github.com/MikazukiMisaki/Alfworld-Self-Improvement-Project/blob/aa9fa3c34520941e7e3be00294b111e8254fd65b/reports/PROGRESS_AWARE_RECOVERY_OSR_R16.md), [C1 frozen report](https://github.com/MikazukiMisaki/Alfworld-Self-Improvement-Project/blob/aa9fa3c34520941e7e3be00294b111e8254fd65b/reports/PROGRESS_AWARE_RECOVERY_FACT_TEXT_R18_C1.md), and [integrated findings](R18_INTEGRATED_FINDINGS.md).

## Supported claims

Confidence below describes the stated scoped claim, not the probability that a null hypothesis is true.

| Claim | Evidence | Confidence | Limitation | Thesis-safe wording |
|---|---|---|---|---|
| Validated public progress facts change emitted recovery behavior. | C1: 54 diagnoses, 51 subgoals and 23 executed commands differ; 3 execution asymmetries. | High descriptively within this protocol. | Text inequality is not semantic improvement; fixed development sample. | Adding validated public facts changed emitted recovery text and executed actions on these prefixes. |
| Validated public progress facts reliably improve terminal recovery. | C1: 3 W / 55 T / 2 L; p = 1.0. | Unsupported as an efficacy claim. | Few discordances; no equivalence or absence claim. | Reliable terminal improvement from the added facts was not established. |
| Structured rendering of identical facts improves terminal recovery. | C2 primary: 0 W / 58 T / 2 L; p = 0.5. | Unsupported as an efficacy claim. | One package and operator; low information from two discordances. | These data do not support CARD-v2's rendering-benefit hypothesis. |
| Different actions imply better reasoning. | C1 changed-action W/T/L 2/19/2; C2 primary 0/17/1. | High that action difference alone is insufficient evidence. | No independent reasoning-quality measurement. | Changed executable behavior must be evaluated separately from its usefulness. |
| Reduced loops imply improved recovery. | Eleven primary loop reductions: 0 W / 10 T / 1 L. | High descriptively for insufficiency of this proxy. | Exposure-dependent metric; other benefits may exist. | Reduced repetition did not by itself establish terminal recovery improvement. |
| Pick-two failures are consistent with missing actionable search/location information. | Fact-coverage proxies 18/17/3; terminal success 1/18. | Suggestive, low-to-moderate. | “Location-aware” is a proxy; no blinded coding or intervention isolates location. | The pattern is consistent with limited actionable knowledge about obtaining the missing object. |
| Evidence supports an information-to-action/follow-through conversion bottleneck. | Frequent emitted/action changes with weak or negative paired terminal differences across C1/C2. | Moderate as a descriptive organizing account; low for an exact causal locus. | Information, compliance, action selection and continuation are not independently manipulated. | The audit reveals a descriptive conversion gap, while leaving its causal components unresolved. |

## Unsupported claims

The evidence does not prove zero effect, equivalence, FACT-TEXT superiority, significant CARD-v2 harm or universal irrelevance of rendering. It does not establish that changed diagnoses are more accurate, changed actions reflect better reasoning, reduced loops indicate successful recovery, or known locations would be sufficient. It does not justify a learned selector or a claim of self-improvement, held-out generalization, broad model-family generality or research firstness. Two nonsignificant development contrasts cannot establish that every useful progress-information intervention will fail.

## Thesis contribution

**Recommended central wording:** In a controlled audit of 60 frozen ALFWorld development prefixes, validated public-progress facts and their rendering changed emitted recovery text and executed actions, but the paired results did not establish a reliable terminal-success benefit under one fixed bounded Qwen3-8B recovery operator.

The defensible contribution is the controlled audit and decomposition: public semantic validity, added information, identical-fact rendering, emitted diagnosis/subgoal changes, executable action changes, local trajectory behavior and terminal rescue/harm. It explains why semantic correctness and visible behavioral responsiveness are insufficient validation targets on their own. It is a scoped empirical contribution, not a claim that the original proposed recovery selector has been demonstrated.

Broad novelty risk is **HIGH**: the broad idea that extra information or changed reasoning need not improve performance is too general for a priority claim. The narrow reproducible audit contribution is potentially meaningful/moderate. This is a positioning judgment, not a literature-verified novelty finding; no firstness claim is made.

## Limitations

One environment; one primary actor/model family (unadapted Qwen3-8B recovery and frozen adapted Qwen3-8B continuation); 60 selected development prefixes; an enriched recovery distribution (30 failure, 15 success-control, 15 random-control prefixes); one fixed bounded recovery operator and one CARD rendering; and no held-out confirmation yet. Marginal success percentages are not estimates of general ALFWorld deployment success.

The prefixes are development evidence even though execution completed formally. Consumed development seeds, including 1005, 1009, 1010, 1022 and 1027, must never be relabeled as held-out evidence. Small discordant counts, reused historical comparators and timing differences limit statistical precision and cross-condition latency interpretation. Pick-two remains weak. Text equality, fact coverage, lexical fact relevance and loop counts are imperfect descriptive proxies. Terminal success is one important outcome and does not capture every possible local benefit. No exact causal bottleneck or mediation path has been identified.

## Stop rule

**Stop CARD formatting tinkering.** Do not pursue CARD-v3/v4, further syntax/layout sweeps, prompt micro-optimization, selector training, DPO, ORPO, RL, memory or multi-environment expansion on the strength of this result. No new implementation or experiment is authorized. Preserve the frozen operator and turn the accepted evidence into the thesis/presentation. A future proposal would need an independently justified scientific question, not a search for a favorable C2 result.

## Optional next experiment

**One optional study: an outcome-blind Actionability Audit of existing frozen prefixes/branches. It is not necessary for the scoped master's-thesis audit claim and was not executed.**

Scientific question: what actionable content is available before recovery, and does the chosen recovery action use it? Existing C1/C2 measure fact validity, text/action differences and outcomes, but do not independently code whether facts specify a feasible next search/navigation operation or a route to the missing object.

Minimal design: preregister a short codebook on all 60 existing prefixes, with the pick-two subset declared in advance. Prepare randomized neutral-ID packets containing only public pre-intervention evidence and frozen facts. Independent reviewers unaware of outcomes and treatment labels code what remains, which instance remains, any actually evidenced location, and available search/navigation operations. Freeze this first-stage coding and adjudication before reviewing the recorded recovery command in a second outcome-masked action-use stage. Lock those labels before joining terminal outcomes; report missing/ambiguous evidence and reviewer agreement. Since the results are already known to the implementation owner, blinding requires genuinely outcome-naive reviewers and masked packets; it cannot be asserted from anonymization alone. The audit remains retrospective.

No new Qwen inference, model calls, environment calls or replay is needed; only existing public records are used. A positive pattern would sharpen the descriptive actionability-gap account. A null pattern would weaken the missing-actionable-information explanation and leave compliance/action selection/follow-through unresolved. Neither result would isolate causality. No alternative new mechanism experiment is recommended here.

## Held-out confirmation decision

**Thesis requirement:** additional confirmation is not scientifically necessary for a thesis explicitly scoped to this development audit. It would be necessary to support a stronger claim of generalizable recovery benefit or generalizable lack of benefit. Existing development results must remain labeled accordingly.

**Publication strengthening:** a fresh same-model Qwen confirmation is worthwhile if the intended paper makes claims beyond these selected prefixes. Decide its value and budget before considering a second model. Freeze the operator, facts procedure, rendering, primary estimand and analysis; use genuinely fresh disjoint tasks/prefixes and matched CONTINUE/OSR/FACT-TEXT/CARD-v2 conditions. Predeclare sampling and precision requirements appropriate to sparse paired discordances. Repeating the known 60 is a repeatability check, not held-out confirmation; collecting until a favorable p-value appears is not acceptable.

A second model is optional and lower priority than that decision. Neither confirmation nor any second-model work is authorized or executed by this task.

## Presentation summary

**A. One slide — R18-C2: accepted run, unsupported rendering benefit**

- Same validated facts; FACT-TEXT 32/60 vs CARD-v2 30/60.
- Primary paired comparison: 0 W / 58 T / 2 L; −3.33 percentage points; exact two-sided p = 0.5.
- Diagnosis/subgoal text changed 37/38 times; 18 different executed actions yielded 0 wins.
- Local token delta only +7.6 on average. No evidence of benefit; no equivalence or significant-harm claim.
- Development evidence only. Protocol acceptance PASS; efficacy hypothesis unsupported.

**B. One slide — R16 → C1 → C2: changes do not guarantee recovery**

- Matched progression: CONTINUE 29 → OSR 31 → FACT-TEXT 32 → CARD-v2 30 successes, each out of the same 60 prefixes.
- Adjacent paired W/T/L: 4/54/2 → 3/55/2 → 0/58/2; exact two-sided p: 0.6875 → 1.0 → 0.5.
- Separate bounded recovery, validated information addition and identical-fact rendering-package effects.
- More changed text/actions and fewer loops did not establish reliable terminal gain; the causal location of the descriptive conversion gap is unresolved.

**C. Contribution:** A controlled development audit separates valid public progress information and rendering-induced behavior changes from terminal rescue and harm.

**D. Limitation:** Sixty selected prefixes, one environment/model family/operator and no held-out confirmation support a scoped audit, not general efficacy or equivalence claims.

**E. Next step / stop rule:** Stop CARD formatting changes, present the accepted findings, and seek separate authorization only if the optional masked audit or fresh confirmation serves a defined claim.

## Final scientific verdict

**PASS for scientific acceptance and exact result archival. Primary and secondary benefit hypotheses are not supported.** No contamination or completed-run integrity mismatch was found in the inspected frozen evidence. All generated bytes and historical records are preserved. The final interpretation is narrower than the generated report's shorthand labels. Next authorized step: **NONE. STOP.**
