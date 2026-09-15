# Integrated R16 / R18 Findings

**Accepted development evidence; no reliable terminal-benefit claim.** The strongest contribution is a controlled audit separating public semantic validity, information addition, identical-fact rendering, emitted recovery changes, executed actions, trajectory behavior and terminal rescue/harm. [Full scientific acceptance](R18_C2_SCIENTIFIC_ACCEPTANCE.md).

## Controlled progression

All terminal comparisons use the same 60 frozen R15 development prefixes. The marginal successes are CONTINUE 29/60, OSR 31/60, FACT-TEXT 32/60 and CARD-v2 30/60. These are paired conditions, not independent samples, independent replications or general deployment-success estimates.

| Milestone | Scientific role | Main observation | Defensible interpretation |
|---|---|---|---|
| R16 OSR | Frozen bounded one-step recovery control vs CONTINUE | 4 W / 54 T / 2 L; net +2; two-sided p = 0.6875; directional p = 0.34375. Rescues 4/31, harms 2/29. | Some interventions rescued and some harmed; reliable average benefit was not established. |
| R18-A | Outcome-blind public-evidence audit of frozen v1 progress facts | 660 fields: 326 exact, 259 justified unknown, 27 unjustified unknown and 48 not applicable. Coverage gaps affected 19 prefixes in eight groups; no coded partial/incorrect fields. | Separate missing public evidence from extraction failure. This audit did not establish treatment efficacy or attribute prior outcomes causally to parser quality. |
| R18-B | Correct documented gaps; freeze canonical v2 facts and matched treatments before inference | 353 exact, 259 justified unknown, 48 not applicable; zero unresolved semantic coverage failures. Sixty CARD-v2/FACT-TEXT pairs share identical semantic facts. | Establish public semantic support and a controlled information/rendering comparison, without inventing unknown targets or locations. This milestone is not an efficacy result. |
| R18-C1 | FACT-TEXT vs OSR: validated added-progress-information effect under the frozen one-step recovery operator | 3 W / 55 T / 2 L; net +1; mean +0.016667; two-sided p = 1.0; directional p = 0.5. | Validated information changed emitted behavior; reliable terminal improvement was not demonstrated. |
| R18-C2 primary | CARD-v2 vs FACT-TEXT: identical-fact rendering-package effect | 0 W / 58 T / 2 L; net −2; mean −0.033333; two-sided p = 0.5; directional p = 1.0. | No evidence of CARD-v2 benefit. Two observed discordances favored FACT-TEXT, without establishing superiority, significant harm, zero effect or equivalence. |
| R18-C2 secondary | CARD-v2 vs OSR: combined secondary contrast | 1 W / 57 T / 2 L; net −1; mean −0.016667; two-sided p = 1.0; directional p = 0.875. | No reliable combined benefit. This is not the representation effect. |

The primary rendering package includes syntax, labels, layout, tokenization, length and compliance. It does not isolate pure abstract representation. Historical generated report/schema labels are preserved unchanged; use these explicit contrast definitions when presenting the results.

Sources: [R16](https://github.com/MikazukiMisaki/Alfworld-Self-Improvement-Project/blob/aa9fa3c34520941e7e3be00294b111e8254fd65b/reports/PROGRESS_AWARE_RECOVERY_OSR_R16.md), [R18-A](https://github.com/MikazukiMisaki/Alfworld-Self-Improvement-Project/blob/aa9fa3c34520941e7e3be00294b111e8254fd65b/reports/PROGRESS_AWARE_RECOVERY_SEMANTIC_AUDIT_R18_A.md), [R18-B](https://github.com/MikazukiMisaki/Alfworld-Self-Improvement-Project/blob/aa9fa3c34520941e7e3be00294b111e8254fd65b/reports/PROGRESS_AWARE_RECOVERY_R18_B_V2_TREATMENT_FREEZE.md), [C1](https://github.com/MikazukiMisaki/Alfworld-Self-Improvement-Project/blob/aa9fa3c34520941e7e3be00294b111e8254fd65b/reports/PROGRESS_AWARE_RECOVERY_FACT_TEXT_R18_C1.md), [exact C2 results](https://github.com/MikazukiMisaki/Alfworld-Self-Improvement-Project/blob/4f5c2e18e0dfdf48e9471fcba0a3ee715be3ca3b/reports/PROGRESS_AWARE_RECOVERY_CARD_V2_R18_C2.md).

## What changed, and what did not reliably improve

C1 changed parsed diagnosis/subgoal text in 54/60 and 51/60, with 23 different executed recovery actions. Those different-action pairs yielded 2 wins, 19 ties and 2 losses. C2 vs FACT-TEXT changed diagnosis/subgoal text in 37/60 and 38/60; 18 different executed actions yielded 0 wins, 17 ties and 1 loss. Text inequalities are not measures of improved understanding, and changed actions do not establish better reasoning.

CARD-v2 had four withheld recovery actions after invalid Stage-1 output, compared with none for FACT-TEXT. One primary loss was a withheld-action pair; the other involved a different valid action. Compliance is therefore part of the package, while the counterfactual outcome of repairing a particular output remains unknown. Keep all 60 prefixes in the primary result.

CARD-v2 reduced loop counts relative to FACT-TEXT in 11/60 pairs, but these gave 0 wins, 10 ties and 1 loss. Reduced repetition is not sufficient evidence of improved terminal recovery; loops are not thereby irrelevant. Local cost inflation versus FACT-TEXT was small (+7.6 tokens on average, approximately zero mean local latency difference), so a large extra-prompt-cost explanation is unsupported. Against OSR, CARD-v2 added approximately 164.6 local tokens, reflecting a meaningful cost for the progress-content package.

The 18 pick-two failure prefixes yielded one success each under OSR, FACT-TEXT and CARD-v2. Count/instance/location-aware counts of 18/17/3 describe input fact coverage. The frozen location proxy is nonempty `known_unfinished_targets`, not an independent measurement of model location knowledge. These observations are consistent with limited actionable knowledge about obtaining a missing object, but do not prove a location bottleneck or that adding locations is sufficient.

## Strongest thesis claim

In a controlled audit of 60 frozen ALFWorld development prefixes, validated public-progress facts and their rendering changed emitted recovery text and executed actions, but the paired results did not establish a reliable terminal-success benefit under one fixed bounded Qwen3-8B recovery operator.

The evidence supports a descriptive progress-to-action/follow-through conversion gap. It does not identify whether missing information, compliance, action selection, restricted intervention budget or subsequent continuation is the dominant causal component. Semantic validity and behavioral responsiveness are separate from useful recovery. Broad novelty risk is high; the narrow reproducible audit is potentially meaningful/moderate. No literature priority or firstness claim is made.

## Scope and decisions

One environment, one primary model family, a 60-prefix enriched development sample, one operator, one CARD package and no fresh held-out confirmation limit generalization. The adjacent contrasts share comparators and have only 6, 5 and 2 discordant pairs. R16's historical record includes three incomplete retries with zero completed reruns; C1 and C2 report no retries. Do not relabel consumed development prefixes/seeds as held-out evidence. The audit is not evidence that a selector works, and terminal success is not the only possible outcome of interest.

**Stop CARD formatting tinkering.** No CARD-v3/v4, layout sweeps, prompt micro-optimization, selector training, DPO/ORPO/RL, memory or environment expansion follows from this result. No further experiment is necessary for the narrowly scoped master's-thesis contribution. At most one optional outcome-blind Actionability Audit could code existing public evidence and recorded actions, using outcome-naive reviewers, preregistered rules and locked labels before joining outcomes; no model/environment calls are needed. It was not performed.

Fresh same-model paired confirmation is worthwhile for publication claims beyond the development sample, but is not required for the scoped audit claim. Decide and preregister its purpose before considering a second model. Reusing the 60 known prefixes is not held-out confirmation. No confirmation run or other experiment was authorized by the acceptance task.

## Finalization provenance

- Execution implementation SHA: `aa9fa3c34520941e7e3be00294b111e8254fd65b`.
- Execution-only agent: GPT-5.6 Luna; execution provenance commit: `983f5d52d9cebd1bab8c313472956e31b87497b5`.
- Astra acceptance: PASS for scientific usability; benefit hypotheses unsupported.
- Results archival commit: `4f5c2e18e0dfdf48e9471fcba0a3ee715be3ca3b`, containing the three generated files with exact final execution hashes, including original CSV line endings.
- [Acceptance task record](../agent-logs/2026-09-15T014845Z__ASTRA__r18c2-scientific-acceptance__159bf149/RECORD.md).

No new scientific execution. Next authorized step: **NONE. STOP.**
