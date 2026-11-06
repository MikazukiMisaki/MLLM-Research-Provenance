# Exploratory investment rule: illustrative null sensitivity

For N paired binary outcomes the draft investment rule requires D=W-L >= ceil(N/50) and L <= floor(N/50). This was chosen after viewing earlier results and is not a confirmatory significance test. To understand how weak or strong it is under one invented null scenario, suppose episodes are independent, each arm has equal success probability, and the two discordant outcomes each have probability 0.05 (total discordance q=0.10). Sum the multinomial probabilities for all W,L satisfying the rule.

| N | Required net wins | Maximum losses | Probability of meeting rule under this assumed null |
|---:|---:|---:|---:|
| 16 | 1 | 0 | 25.48% |
| 50 | 1 | 1 | 22.10% |
| 51 | 2 | 1 | 15.22% |
| 82 | 2 | 1 | 6.58% |

These are arithmetic examples, not measured error rates or measured task discordance. Parent clustering, model variation, data-dependent panel selection, tuning or selection across arms would change the calculation; no familywise probability is asserted. The discontinuity from N=50 to 51 follows from integer rounding. A small development panel passing this resource-allocation threshold is not strong evidence that the true effect is positive. Fix the population, unit and threshold before new outcomes, report all arms, and seek genuinely independent evaluation before any corresponding generalization claim.

Formula independently calculated using standard-library exact integer binomial coefficients and floating-point probability products: sum over l=0..floor(N/50), w>=l+ceil(N/50), w+l<=N of N!/(w!l!(N-w-l)!)*0.05^(w+l)*0.90^(N-w-l). No model, environment, data, real task, or GPU was accessed.
