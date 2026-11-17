# Illustrative precision for a future paired confirmation

This is a prospective design calculation, not an analysis of existing results, not a task release and not a power claim for the current 12-task DEV screen. No evaluation data were used. `power.py` uses the exact conditional, two-sided McNemar test (not mid-p), averaged over the binomial number of discordant pairs. It assumes independent, identically distributed parent-task pairs and fixed true discordance and effect. It uses per-comparison alpha 0.025 as a conservative planning threshold for two predeclared comparisons controlled by Holm, rather than modelling the joint test correlations.

Examples, conditional on these assumptions:

| Independent parent pairs | Assumed discordant-pair fraction | Assumed absolute success-rate improvement | Power |
|---:|---:|---:|---:|
| 200 | 20% | 10 percentage points | 81.0% |
| 400 | 30% | 10 percentage points | 91.6% |
| 400 | 20% | 5 percentage points | 46.0% |
| 800 | 20% | 5 percentage points | 80.7% |

These hypothetical inputs are not estimates of performance or discordance. Actual parent dependence, heterogeneity, task reuse, invalid/UNKNOWN outcomes, multiple checkpoints and selection can reduce validity or precision. A confirmation protocol must justify the effect of interest and discordance, lock a source-traceable independent parent roster, randomization, outcomes and complete budget before its results; no amount of repeated seeds turns one parent into independent parents. The 12-parent development comparison can inform feasibility, but is too small to establish stable generalization.

`result.json` retains all combinations and exact floating-point outputs. Computational verification is pending independent review.
