# Illustrative three-arm joint power

This is a synthetic planning calculation, not an analysis of real tasks or an
experiment. For each IID parent task, draw `C ~ Bernoulli(0.5)`. For each
comparison, independently or identically according to the scenario, draw a
discordance indicator with probability 0.45 when `C=1` and 0.15 when `C=0`;
set each comparator to `C` when its indicator is false and to `1-C` otherwise.
Consequently `P(C=1,A=0)=P(C=1,B=0)=0.225`,
`P(C=0,A=1)=P(C=0,B=1)=0.075`, so each comparison has true net difference
0.15 and discordance rate 0.30. In the independent scenario the indicators
are independent **conditional on C**, not necessarily unconditionally
independent. In the identical scenario A and B are identical on each task.

For both contrasts, the observed success difference must be at least 0.10.
Order the two exact two-sided McNemar p values as `p_min <= p_max`; both Holm
comparisons pass exactly when `p_min <= .025` and `p_max <= .05`. Each case
below uses 20,000 replications and Python standard-library seed 20261118.

| Conditional discordance | Independent parent tasks | Joint power | Monte Carlo SE | Approx. 95% MC interval |
|---|---:|---:|---:|---:|
| Independent | 82 | 0.44545 | 0.003514 | 0.43856–0.45234 |
| Identical | 82 | 0.54245 | 0.003523 | 0.53555–0.54935 |
| Independent | 200 | 0.85520 | 0.002488 | 0.85032–0.86008 |
| Identical | 200 | 0.92050 | 0.001913 | 0.91675–0.92425 |

An independently written implementation with seed 20261119 yields 0.44590,
0.54410, 0.85810 and 0.92400 in the table's order. Identical indicators imply
identical p values, so joint success reduces to a single exact test at .025;
an exact integer calculation independently gives 0.5413938884 at N=82 and
0.9209845607 at N=200, consistent with Monte Carlo error. Intervals describe
simulation error conditional on the constructed model, not uncertainty about
real-world task distributions. The two constructions are examples and do not
establish bounds for all possible dependence structures. This is conditional
on fixed model products and does not measure training-seed variation.

`python joint_power.py` reproduces the primary simulation; SHA256
`01b55cdc357817bbdc3c2c9c6c1ad00b97f8cfa09aa974af8d0e94634476b62b`.
`python independent_verify.py` reproduces the separate check; SHA256
`9c9d21b8281483f8a0707e3c1f4ef5e404d5651f85f5bd913123eb1bd4b51a18`.
No task content, real model, GPU, environment or experiment was accessed.
