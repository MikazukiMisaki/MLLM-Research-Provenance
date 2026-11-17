# Hypothetical three-arm paired joint power

This is a hypothetical planning illustration, not an experiment, protocol amendment or claim about available independent tasks. For every independently drawn parent task, simulate fixed-product binary success C, A and B, with P(C=1)=0.5. Conditional on C=1, each comparison has disagreement probability 0.45 (C wins); conditional on C=0 each has disagreement probability 0.15 (C loses). Consequently C−A and C−B both have true net difference +0.15 and discordance 0.30. We examine two explicit coupling constructions: their disagreement indicators are independent given C, or identical given C. These are examples, not bounds over all joint distributions.

For each pair, the observed net improvement must be at least 0.10. Each two-sided p value is an exact conditional McNemar p, and *both* must be rejected by Holm at familywise alpha 0.05: min(pA,pB)≤0.025 and max(pA,pB)≤0.05. Estimated joint probability comes from 20,000 Monte Carlo samples per scenario using Python's fixed-seed pseudo-random generator. Standard errors below quantify Monte Carlo variation only, not uncertainty about the assumed outcome probabilities.

| IID parent tasks | Disagreements independent given C | Disagreements identical given C |
|---:|---:|---:|
| 82 | 44.55% (MC SE 0.35 pp) | 54.46% (0.35 pp) |
| 200 | 85.54% (0.25 pp) | 92.15% (0.19 pp) |

For identical indicators the comparisons are identical and the joint rule reduces to one comparison p≤0.025 and the effect threshold. Its independently computed exact powers are 54.1394% at N=82 and 92.0985% at N=200; simulated differences are consistent with sampling error. An independent reviewer using a separate program and random seeds obtained 44.55%/85.52% for the independent construction and 54.25%/92.05% for identical indicators, respectively. Its script SHA256 is `01b55cdc357817bbdc3c2c9c6c1ad00b97f8cfa09aa974af8d0e94634476b62b`. The two marginal comparisons in both constructions have exactly the same assumed true differences and discordance; the variation is due to joint dependence and Monte Carlo error. Neither scenario supports extrapolation to the related, previously exposed DEV tasks or shows that such independent eligible tasks exist.

These are fixed-product probabilities, not joint power for multiple training seeds, non-IID tasks, missing/failed runs or unknown physical outcomes. They should inform Astra's choice of prospective estimand, meaningful threshold, plausible joint scenarios and full budget; they do not change completed SI-U1 criteria, authorize a run, or resolve the current hold. Source `joint_power.py` and `result.json` preserve code, seeds, raw counts and MC standard errors. No model, GPU, environment, tokenizer or actual task data were used.
