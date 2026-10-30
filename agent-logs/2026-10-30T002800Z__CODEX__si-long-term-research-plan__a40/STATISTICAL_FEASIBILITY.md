# Conditional feasibility: four parent labels and the old single-seed rule

Decision: IMPOSSIBLE_UNDER_THIS_RULE_AND_CONDITIONAL_METADATA_BOUND; NOT_A_GENERAL_POWER_CLAIM. A recent independent archive reconstruction found 350 candidate parent labels after the documented parent/byte and old-proposal protections. A further hypothetical rule rejecting every numeric scene label appearing among four enumerated previously used or materialized-source categories leaves at most four parent names; zero of the 24 valid_unseen parent names survive this category-specific rule. This is a label-only metadata upper bound for the inspected dataset and policies, not four proven independent, runnable or unexposed tasks. A stricter screen that additionally treats all historical candidate/reservation lists as protected is a different policy and can leave fewer; the source audit reports that all 350 overlap the full recorded-history suffix set.

For the original single-seed paired design, the two planned comparisons are C−A and C−B, each a two-sided exact McNemar test, with Holm correction over the two p-values at familywise alpha 0.05. This audit enumerates every possible observed (A, B, C) triple of binary outcomes for each of N=1,2,3,4 parents, computes the exact paired discordance tests, and applies the two-comparison Holm procedure. Thus 8^N complete outcome tables are checked, including all correlations from a shared C outcome:

| N | Tables enumerated | Minimum possible raw two-sided p | Tables with at least one Holm-significant comparison | Tables with both significant |
|---:|---:|---:|---:|---:|
| 1 | 8 | 1.000 | 0 | 0 |
| 2 | 64 | 0.500 | 0 | 0 |
| 3 | 512 | 0.250 | 0 | 0 |
| 4 | 4,096 | 0.125 | 0 | 0 |

For N=4 the minimum occurs when all four paired observations are discordant in the same direction: `2 × (1/2)^4 = 0.125`. The first Holm threshold is 0.025; hence no comparison, let alone both, can reject for any data. A zero-task set supplies no test. Since the smallest p for N<4 is even larger, the conclusion holds for N≤4 under this precise rule. An additional ≥10 percentage-point observed-effect threshold cannot make an already impossible significance result possible. This is a statement of the rule's limited resolution, not an estimate that the true treatment effect is zero.

It does not establish that all possible designs, different endpoints or tests, three-training-seed estimators, or separate research questions are impossible. A multi-seed design requires an explicit estimand, task/seed dependence and separately validated inference; one cannot count correlated task×seed observations as independent to circumvent this limitation. Revisit the sampling frame or scientific question before a prospective design, not the old decision threshold after observing results.

For resource planning only, a different illustrative scheme with A once and B/C each three seeds, four parents and horizon 50 would produce at most 28 trajectories, 1,400 generations, 1,428 reset-inclusive environment operations and, if all start, 28 resets; under old per-call maxima of 8,192 input/16 output tokens, upper limits are 11,468,800 input and 22,400 output tokens. This is not the statistical design just enumerated, a cost prediction, a claim four tasks are eligible, or authorization: training, model/environment initialization and cleanup, engineering, and failed/incomplete operations are additional. No model, CUDA, ALFWorld or experiment was run.

Reproduction: `python enumerate.py` in this directory. The input SHA256 and full per-N output are recorded in `ENUMERATION.json`; `FILE_HASHES.sha256` covers the script, result and this interpretation.
