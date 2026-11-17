# Independent sensitivity: predeclared 16 versus finite 128 candidate parents

Under an **illustrative independent, identically distributed Bernoulli model**, requiring all 16 preselected parents to qualify is highly restrictive unless the unknown per-parent qualification probability is very high. A separately predeclared 128-parent screening roster can greatly improve feasibility at moderate qualification rates, but is still unlikely to yield 16 pairs at q=0.05. This is a design calculation, **not an estimate of the project's actual q, number of available parents or source eligibility**.

Here q is the joint probability that a preselected parent's one preordered first episode is completed and successful *and* satisfies every loop, same-action, exact loss-bearing token/mask, provenance/context and pairing rule. Do not substitute the frequency of loops alone for q. Assume the 128 parent qualification indicators are independent Bernoulli(q), with fixed q across parents and a fixed pre-result ordering. Then:

- Current protocol: `P(all 16 qualify) = q^16`.
- Prospective alternative: declare 128 candidate parents and one first episode per parent in advance; inspect in fixed order and take the first 16 qualifying parents without changing episodes or expanding the pool. Feasibility is `P[Binomial(128,q) ≥ 16] = 1 − Σ(k=0..15) C(128,k) q^k (1−q)^(128−k)`.

| Assumed q | 16 of 16 qualify | At least 16 of 128 qualify | Expected number screened with stop at 16 or 128 |
|---:|---:|---:|---:|
| 0.05 | 1.526 × 10⁻²¹ | 0.0687% | 127.99 |
| 0.10 | 1.000 × 10⁻¹⁶ | 20.88% | 124.60 |
| 0.20 | 6.554 × 10⁻¹² | 99.04% | 79.91 |
| 0.50 | 0.001526% | approximately 100% | 32.00 |
| 0.80 | 2.815% | approximately 100% | 20.00 |
| 0.90 | 18.53% | approximately 100% | 17.78 |

“Approximately 100%” does not mean certainty: the exact modeled failure probabilities at q=.50/.80/.90 are approximately `4.465e-20`, `4.993e-62`, and `2.762e-95`. Expected numbers are computed as `Σ(n=0..127) P[Binomial(n,q)<16]`, counting screening until the 16th eligible parent or all 128 are exhausted. The pure standard-library script `sensitivity.py` SHA256 `4499b5347f8f02792690b09042d7c620c3c733dbf6a3ea079586b35aa82a8197` and raw `results.csv` SHA256 `4c87e039c487f3ff7ffe4537124bd18dbb8e2694123d37ba98d699076377eed3` reproduce the full precision.

## Interpretation and proposed action

Treat the exact-16/all-pass design as a stringent feasibility pilot, not as evidence of rarity if it fails. If a genuine, permitted and independently identifiable 128-parent source roster actually exists, consider a **new prospective protocol amendment** fixing its membership, order, one preselected episode per parent, qualification rules and first-16 stopping rule *before observing these candidates or evaluation outcomes*. This changes v5's no-parent-replacement rule and cannot be called the already-frozen v5 rule or applied retroactively to a known result. No reroll of episodes, adaptive expansion, post-hoc threshold change, or test-result-guided selection. If fewer than 16 qualify after 128, stop and report all rejection counts and the original denominator.

A larger screened roster selects qualifying successful trajectories and their parent types; estimates remain conditional on this selected source and state-selection rules. It does not remove success-selection bias, show that a target action caused recovery, establish self-data superiority over other sources, or make these 16 training parents representative. Preserve a separately fixed evaluation roster, parent/variant lineage separation and honest exposure labels. Record every candidate's eligibility outcome and reason, the exact ordered roster and frozen selection/source-code manifest, with UNKNOWN kept distinct from a confirmed failure. Material scanning has additional CPU, I/O, time, storage, provenance and reviewer costs even if it causes zero *new model generations*; preallocate and monitor those costs and maintain existing physical cost history. Do not read evaluation outcomes to alter eligibility or stop criteria.

The iid assumption is strong: similar parents or shared success/trace-generation conditions can induce dependence and heterogeneous q. The binomial table can therefore be badly miscalibrated; e.g. if all parents share one common qualification indicator, both roster rules succeed with probability q, not these iid values. With a finite already-fixed roster, qualification count is fixed but unknown, and any sampling model must reflect how that roster was selected. The hypothetical q values are not empirical prevalence, and no source, model, environment or task data was inspected here. The alternative is a planning recommendation only, not permission to scan material, train, evaluate or claim success.
