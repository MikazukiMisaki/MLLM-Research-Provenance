# Exact power of a single paired binary comparison

This calculation uses no experiment data. Assume independent identically
distributed parent tasks, discordance probability `q = 0.30`, and true
candidate-minus-baseline probability difference `delta`. Let `W` be candidate
only successes, `L` baseline only successes, and `K = W + L`. Then
`K ~ Binomial(N, q)` and `W | K=k ~ Binomial(k, (q+delta)/(2q))`.

For each `k,w`, include its probability exactly when both
`(2w-k)/N >= 0.10` and the two-sided exact McNemar p value is at most
`0.025`. Since the first condition requires `w > k/2`, the exact p value is
`2 P(Binomial(k, 0.5) >= w)`. The implementation uses integer sums and
rational arithmetic rather than a normal approximation. A separate floating
point conditional-binomial sum reproduced the table to 12 decimal places.

| True difference | N=82 | N=200 | N=400 |
|---|---:|---:|---:|
| 0.10 | 0.217334008588 | 0.524869812028 | 0.518264973641 |
| 0.15 | 0.541393888430 | 0.920984560704 | 0.974410043202 |

At true difference exactly 0.10, the observed-effect threshold lies at the
true value; increasing N cannot make its pass probability approach one. The
small non-monotonicity follows discrete count and significance cutoffs.
These are prospective powers for **one** preselected contrast, not the joint
power of two comparisons or three arms. They are not valid for dependent
variants or as a claim of independent, unexposed DEV tasks.

Reproduce with `python exact_power.py`. The script's SHA256 is
`de86c38e0cc9b7befc8e33afdfb84f11fcaca55c35540a89f26d7ed96d322e0a`.
