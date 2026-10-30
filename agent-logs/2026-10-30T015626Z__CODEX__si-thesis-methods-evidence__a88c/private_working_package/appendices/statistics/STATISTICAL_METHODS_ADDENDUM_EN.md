# SI-U1: paired estimands, exact calculations and interpretation

*Proposed explanatory text for the completed study; pending independent review before integration. This restates the frozen analysis and does not specify a new study, sample, threshold or analysis. Source labels S1–S7 resolve in EVIDENCE_MAP.md.*

## Paired outcomes and descriptive estimands

Let \(Y_{ia}\in\{0,1\}\) denote the recorded task-completion outcome for task \(i\) under checkpoint \(a\in\{A,B,C\}\). The completed fixed schedule contains \(n=82\) paired task records, with one outcome for each checkpoint on each task. For each prespecified comparator \(j\in\{A,B\}\), define

\[
W_j=\sum_{i=1}^{n}\mathbf 1(Y_{iC}=1,Y_{ij}=0),\qquad
L_j=\sum_{i=1}^{n}\mathbf 1(Y_{iC}=0,Y_{ij}=1),\qquad
T_j=n-W_j-L_j.
\]

The reported paired difference is

\[
\widehat\Delta_j=\frac1n\sum_{i=1}^{n}(Y_{iC}-Y_{ij})
=\frac{W_j-L_j}{n}.
\]

It is an equally task-weighted difference on this schedule, not an equally family-weighted average or a success rate conditional on discordance. Multiplication by 100 expresses it in percentage points. Ties include both joint success and joint failure; they contribute zero to the numerator but remain in the denominator. The 246 episodes do not constitute 246 independent observations for either paired contrast. The extractor required all 82 complete task triples with the frozen task identities, families, order and seeds; missing or invalid records were not silently excluded. [S1–S3]

## Exact paired tests and the multiplicity family

For each contrast let \(d_j=W_j+L_j\). The exact conditional McNemar calculation uses the null model \(W_j\mid d_j\sim\operatorname{Binomial}(d_j,1/2)\), corresponding to equal probabilities of the two directions of discordance under an appropriate paired-sampling model. The frozen implementation computes

\[
p_j=\min\left\{1,\;2\sum_{k=0}^{\min(W_j,L_j)}
\binom{d_j}{k}2^{-d_j}\right\},
\]

and sets \(p_j=1\) if \(d_j=0\). This is the doubled smaller-tail, two-sided exact calculation, not a chi-square approximation, continuity correction or mid-p calculation. Conditioning on discordance is part of the test, not a change to the effect denominator. [S2]

The multiplicity family consists of exactly the two original primary contrasts, C−A and C−B. For ordered raw p-values \(p_{(1)}\le p_{(2)}\), the implementation returns

\[
\widetilde p_{(1)}=\min(1,2p_{(1)}),\qquad
\widetilde p_{(2)}=\min\{1,\max(\widetilde p_{(1)},p_{(2)})\},
\]

and maps these Holm-adjusted values back to the original contrasts. The historical family-wise level was 0.05. Sharing the C outcomes makes the contrasts dependent; Holm does not require their independence, but does require valid component p-values. Descriptive task-family summaries, post-result diagnostic comparisons and the separate R19 analysis are not additional members of this two-test family. Their exclusion from this family does not make them confirmatory findings. [S1–S2]

## Four-component confidence-interval construction

Under a justified common task-sampling model, write \(\pi_{Wj}=P(Y_C=1,Y_j=0)\), \(\pi_{Lj}=P(Y_C=0,Y_j=1)\), and \(\Delta_j=\pi_{Wj}-\pi_{Lj}\). The frozen calculation uses two-sided Clopper–Pearson intervals for each of the four marginal proportions \(\pi_{WA},\pi_{LA},\pi_{WB},\pi_{LB}\), each at confidence level \(1-\alpha_c=0.9875\), where \(\alpha_c=0.0125\). Each component uses denominator \(n=82\), not \(d_j\). [S2]

For a component count \(x\), the lower endpoint is zero when \(x=0\); otherwise it solves

\[
P_{p=\ell_x}\{\operatorname{Binomial}(n,p)\ge x\}=\alpha_c/2.
\]

The upper endpoint is one when \(x=n\); otherwise it solves

\[
P_{p=u_x}\{\operatorname{Binomial}(n,p)\le x\}=\alpha_c/2.
\]

The implementation obtains these endpoints by 100 bisection iterations on binomial tails. Thus the coverage construction is exact-binomial, while the saved endpoints are numerical approximations. The interval for each paired difference is

\[
I_j=[\ell_{W_j}-u_{L_j},\;u_{W_j}-\ell_{L_j}].
\]

If the four marginal binomial intervals have their stated coverage, the union bound gives probability at least \(1-4\alpha_c=0.95\) that all four cover simultaneously; this event implies coverage of both difference intervals. Dependence among the four counts does not invalidate this union-bound step. It does not, however, repair invalid marginal binomial assumptions caused by an inappropriate task-sampling model. These are conservative simultaneous intervals for two differences, not a single Clopper–Pearson interval for a difference, and not intervals obtained by inverting the Holm tests. [S1–S2]

## Recorded results and scope of inference

The existing accepted analysis and independent arithmetic review reported the following values; they were not recomputed for this addendum. [S4–S6]

| Contrast | Wins / losses / ties | Difference (pp) | Raw exact p | Holm p | Nominal simultaneous 95% interval (pp) |
|---|---:|---:|---:|---:|---:|
| C−A | 3 / 1 / 78 | +2.44 | 0.625 | 1.00 | [−7.98, +12.42] |
| C−B | 3 / 4 / 75 | −1.22 | 1.00 | 1.00 | [−13.78, +11.54] |

For the fixed evaluated tasks and checkpoints, \(\widehat\Delta_j\) is a descriptive finite-schedule quantity. Interpreting the intervals as uncertainty about a wider population requires an identified target distribution and a suitable repeated-sampling or stochastic model—for example, independent task draws from a common joint distribution of paired binary outcomes. Directory uniqueness or exchangeability alone does not establish the binomial model, and the study did not establish a representative unseen-task or unseen-scene sample. Related tasks or shared scene layouts may create dependence across task records that these calculations do not adjust for. Pairing accounts for the within-task comparison; it does not remove cross-task dependence, certify historical nonexposure or imply randomized treatment assignment. [S1, S7]

A and the two continuation checkpoints were fixed for this comparison. Each continuation has one training seed and one final checkpoint. These intervals do not estimate variability across independently retrained policies, alternate training datasets or repeated environment realizations, nor do they identify data source separately from the accompanying task/state distribution and training pipeline. The historical positive-signal and warning rules remain unchanged; the accepted decision was INCONCLUSIVE. Neither p-values of 1.00 nor the absence of an observed warning establishes equivalence, absence of harm or a true effect below or above a practical threshold. The retrospective two-object observations and R19 findings do not alter that decision. [S1–S2, S4–S7]
