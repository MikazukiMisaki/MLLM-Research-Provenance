# Independent scientific design review: preserve the self-improvement question

Status: design recommendation, not an executable protocol or an experimental result. No task instances, model or environment were accessed for this review.

The proposed C4 minus C1 comparison estimates a difference between the two training treatments, conditional on their frozen checkpoints. It does not alone show that either treatment improves agent success versus its initial P0. To align with the stated research question, propose evaluating fixed P0, C1 and C4 on the same independently drawn tasks and predeclare two comparisons: C4 minus P0 as the primary improvement contrast, and C4 minus C1 as the training-treatment contrast. C1 minus P0 can be descriptive unless explicitly included in the multiplicity plan. The names C1 and C4 do not themselves establish that their training data, weighting or checkpoints have been implemented or are comparable: verify a common training pool and record weighting, sample presentations, effective token/optimization dose, seeds and all checkpoints before evaluation.

## Restricted estimand and data boundaries

For fixed policies, frozen generator, validity rules and a declared mixture of the two permitted evaluation families, estimate the paired success differences over independent draws from that constructed distribution. Freeze task generation and all acceptance rules before observing model outcomes. Task validation must be treatment independent, bounded and fully recorded, with no hidden substitution after seeing results. Keep generated training and evaluation supports disjoint under the separately reviewed lineage/family rule, with separate custody of evaluation randomness; never probe protected prior task assets to infer overlap. Historical and pretraining exposure remain unknown. Two evaluation families do not provide replication across unseen families, and one checkpoint per treatment does not characterize training-seed variability.

Independently sampled draws with replacement are the unit for the illustrative IID calculation, even if duplicate task representations are possible; duplicates must be counted and disclosed, never recast as new families. The generator and execution must actually support the stated sampling and independence assumptions. The prior generic source audit found that a shared Python global RNG can be consumed by task solving and later grammar selection; merely saving one seed is not sufficient to show independence or reproducibility. A practical prospective implementation should assign per-draw independent random streams and bind their algorithm, initial state, ordering, generator bytes and validity outcomes; verify actual implementation instead of assuming such isolation exists. Process/runtime correlation or failure-dependent filtering invalidates the simple calculation unless modeled or controlled.

## Precision and feasibility

For either paired contrast D in [-1,1], two-sided Hoeffding with Bonferroni correction across two prespecified contrasts yields simultaneous 95% half-width sqrt(2 ln(80)/n). At n=877, this is approximately 10 percentage points. This is a sufficient distribution-free interval bound under the specified IID conditions, not a universal required sample size, a demonstration of 80% power, or a guarantee that an effect at the 10-point boundary will pass a success threshold. Separately specify the minimum practical effect and which confidence-bound decision would justify continuation. Claims beyond the conditional generator distribution need independent task families and/or training realizations and a separate analysis plan.

A small n=20 three-arm paired stage is only an engineering and data-yield feasibility exercise; its conservative two-contrast half-width is approximately 66 percentage points. Freeze the execution completeness, identity, unknown-operation and data-yield criteria before this stage. Do not use its selected outcomes for a confirmatory claim; outcome-dependent design selection or sample-size increases require a new independent confirmatory set or a valid prespecified sequential method.

## Conditional physical envelopes

Assume one episode per task per arm, horizon 50, at most one generation and one action step per turn and one reset per episode. Counts include resets and steps, but do not include task generation/verification, translations, model loads, training, cleanup, engineering, failed/open operations or other unknowns.

| Stage | Three-arm evaluation generations | Three-arm evaluation reset+step ops | With illustrative acquisition generations | With illustrative acquisition reset+step ops |
| --- | ---: | ---: | ---: | ---: |
| n=20 | 3,000 | 3,060 | 5,000 | 5,590 |
| n=877 | 131,550 | 134,181 | 133,550 | 136,711 |

The added acquisition envelope of 2,000 generations and 2,530 reset+step operations is a prior hypothetical arithmetic input, not an implemented or complete cap. Actual input/output token ceilings, optimizer work, allocated device-hours, available capacity, storage, independent verification, failed starts and unknown tails must be separately specified and enforced. Three-arm evaluation costs more than the earlier two-arm table. An engineering single-action probe cannot estimate full-episode or training cost.

Sources reviewed: `20261106__CODEX__si-static-grammar-derivation__independent/STATISTICAL_PRECISION_OPTIONS.md`, `COST_ADDENDUM.md` and `PUBLIC_DATA_NOTE.md`; `2026-11-06__CODEX__si-u1-decision-synthesis/SAME_DOMAIN_PARAMETRIC_COST_V2.md`; `2026-11-06__CODEX__independent-population-path__review/GENERIC_GENERATOR_RNG_ADDENDUM.md`; `2026-10-29T231000Z__CODEX__si-u1-scientific-review__c2356/SI_U1_SCIENTIFIC_REVIEW_AND_THESIS_NEXT_STEPS.md`.
