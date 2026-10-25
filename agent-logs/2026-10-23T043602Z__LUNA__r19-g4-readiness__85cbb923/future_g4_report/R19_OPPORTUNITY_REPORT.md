# R19 recovery-control duration opportunity report

This report is reconstructed from the supplied evidence only. The sample is enriched TRAIN-development data and does not estimate general ALFWorld accuracy.

## Integrity and denominators

- Primary eligible prefixes: 36
- Initial attempted prefixes: 39
- Physical model generations: 4965
- Physical environment operations (including replay): 7273
- Physical tokens, input/generated/total: 3098660/25817/3124477
- Held-out tasks / training runs / external paid calls: 0 / 0 / 0

## Success and paired comparisons

| Policy | Successes | N | Rate | Mean full-branch tokens | Mean recovery-only tokens |
|---|---:|---:|---:|---:|---:|
| CONTINUE | 30 | 36 | 0.8333333333333334 | 7470.222222222223 | NA |
| K1 | 29 | 36 | 0.8055555555555556 | 9778.888888888889 | 1194.8055555555557 |
| K2 | 30 | 36 | 0.8333333333333334 | 9854.25 | 1869.7777777777778 |
| K3 | 28 | 36 | 0.7777777777777778 | 11749.666666666666 | 2505.972222222222 |
| K4 | 25 | 36 | 0.6944444444444444 | 13514.0 | 3133.0555555555557 |
| K5 | 24 | 36 | 0.6666666666666666 | 13482.361111111111 | 3759.5833333333335 |

- **K2_vs_K1:** N=36, both-success=28, both-failure=5, wins/losses/ties=2/1/33, mean difference=0.027777777777777776, exact p=1.0, Holm p=1.0, conservative model-based 95% interval=[-0.15986620528108386, 0.20690759147384352].

- **K3_vs_K1:** N=36, both-success=27, both-failure=6, wins/losses/ties=1/2/33, mean difference=-0.027777777777777776, exact p=1.0, Holm p=1.0, conservative model-based 95% interval=[-0.20690759147384352, 0.15986620528108386].

- **K4_vs_K1:** N=36, both-success=23, both-failure=5, wins/losses/ties=2/6/28, mean difference=-0.1111111111111111, exact p=0.2890625, Holm p=0.8671875, conservative model-based 95% interval=[-0.3466446091857465, 0.15270177339381052].

- **K5_vs_K1:** N=36, both-success=23, both-failure=6, wins/losses/ties=1/6/29, mean difference=-0.1388888888888889, exact p=0.125, Holm p=0.5, conservative model-based 95% interval=[-0.3509918926491024, 0.11000767066440675].

## Duration opportunity

- S_fixed: 0.8333333333333334
- S_oracle: 0.8888888888888888
- H_success: 0.05555555555555547
- Outcome patterns K1..K5: `{"00000": 4, "00001": 1, "01010": 1, "01110": 1, "10000": 1, "11000": 1, "11100": 3, "11101": 1, "11110": 1, "11111": 22}`
- States helped / harmed by extra recovery versus K1: 3 / 7
- Development-selected fixed K: 2; success-tied candidates=[2]; final cost-tied candidates=[2].
- The hindsight envelope is opportunity analysis over tested common paths, not a deployable controller or population ceiling.

## Adjacent handoff contrasts

| Contrast | N | Wins | Losses | Ties | Mean difference |
|---|---:|---:|---:|---:|---:|
| K2_minus_K1 | 36 | 2 | 1 | 33 | 0.027777777777777776 |
| K3_minus_K2 | 36 | 0 | 2 | 34 | -0.05555555555555555 |
| K4_minus_K3 | 36 | 1 | 4 | 31 | -0.08333333333333333 |
| K5_minus_K4 | 36 | 2 | 3 | 31 | -0.027777777777777776 |

## Cost dimensions and net-success cost

Mean logical costs are shown separately; replay/restoration belongs only to physical research expenditure.

| Policy | N | Full input | Full generated | Full calls | Full actions | Recovery input | Recovery generated | Recovery calls | Recovery actions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CONTINUE | 36 | 7412.305555555556 | 57.916666666666664 | 11.583333333333334 | 11.583333333333334 | None | None | None | None |
| K1 | 36 | 9676.805555555555 | 102.08333333333333 | 15.416666666666666 | 14.416666666666666 | 1159.8055555555557 | 35.0 | 2.0 | 1.0 |
| K2 | 36 | 9750.5 | 103.75 | 15.75 | 14.75 | 1829.7777777777778 | 40.0 | 3.0 | 2.0 |
| K3 | 36 | 11630.361111111111 | 119.30555555555556 | 18.86111111111111 | 17.86111111111111 | 2461.3888888888887 | 44.583333333333336 | 3.9166666666666665 | 2.9166666666666665 |
| K4 | 36 | 13378.444444444445 | 135.55555555555554 | 22.11111111111111 | 21.11111111111111 | 3084.027777777778 | 49.02777777777778 | 4.805555555555555 | 3.8055555555555554 |
| K5 | 36 | 13349.583333333334 | 132.77777777777777 | 21.555555555555557 | 20.555555555555557 | 3706.1111111111113 | 53.47222222222222 | 5.694444444444445 | 4.694444444444445 |
- K2_vs_K1: net additional successes=1; tokens per additional net success=2713.0.
- K3_vs_K1: net additional successes=-1; tokens per additional net success=None.
- K4_vs_K1: net additional successes=-4; tokens per additional net success=None.
- K5_vs_K1: net additional successes=-5; tokens per additional net success=None.

## Sampling composition

- Attempted-prefix K1 versus CONTINUE: `{"both_failure": 6, "both_success": 30, "comparator_successes": 31, "harm_rate": 0.0625, "losses": 2, "mean_paired_difference": -0.02564102564102564, "n": 39, "reference_successes": 32, "rescue_rate": 0.14285714285714285, "ties": 36, "wins": 1}`
- Primary family denominators: `{"look_at_obj_in_light": {"K1_successes": 4, "K2_successes": 3, "K3_successes": 3, "K4_successes": 1, "K5_successes": 2, "n": 4}, "pick_and_place_simple": {"K1_successes": 5, "K2_successes": 6, "K3_successes": 5, "K4_successes": 5, "K5_successes": 4, "n": 6}, "pick_clean_then_place_in_recep": {"K1_successes": 4, "K2_successes": 5, "K3_successes": 5, "K4_successes": 5, "K5_successes": 3, "n": 6}, "pick_cool_then_place_in_recep": {"K1_successes": 7, "K2_successes": 7, "K3_successes": 6, "K4_successes": 6, "K5_successes": 7, "n": 10}, "pick_heat_then_place_in_recep": {"K1_successes": 9, "K2_successes": 9, "K3_successes": 9, "K4_successes": 8, "K5_successes": 8, "n": 10}, "pick_two_obj_and_place": {"K1_successes": 0, "K2_successes": 0, "K3_successes": 0, "K4_successes": 0, "K5_successes": 0, "n": 0}}`
- Primary stratum denominators: `{"failure": {"K1_successes": 1, "K2_successes": 2, "K3_successes": 2, "K4_successes": 1, "K5_successes": 0, "n": 6}, "random_control": {"K1_successes": 14, "K2_successes": 13, "K3_successes": 12, "K4_successes": 12, "K5_successes": 13, "n": 15}, "success_control": {"K1_successes": 14, "K2_successes": 15, "K3_successes": 14, "K4_successes": 12, "K5_successes": 11, "n": 15}}`
- The analysis requires a separate frozen enrollment ledger for source, attempt, eligibility, and exclusion counts; these are not inferred from the outcome table.

## Passive public-state stopping diagnostic

- Primary prefixes / diagnostic records: 36 / 36
- Supported / unsupported predicates: 7 / 29
- Exact measured-suffix mappings / coverage-only cases: 7 / 29
- Satisfied-trigger handoffs / successes / rate: 7 / 7 / 1.0
- Mean detector computation: 75310.5 ns; new model/environment calls: 0 / 0.
- The diagnostic is mapped to already-measured suffixes only; unsupported or non-exact mapping is not imputed.

## Integrity-qualified interpretation: ADAPTIVE STOPPING OPPORTUNITY

## Provenance

- Protocol SHA-256: `3d7d1865c807d12276a8109b06c55da4e9182df0ca05a0b5463f8128dd03e122`
- Events SHA-256: `05e1d443ff304eaa25d08b92a4e19d204a6c93a4f46bbe50aefef3271f211762`
- Branches SHA-256: `eff9b5e74d3d5daa928cb662dcc59fc3f434f66796b673679d40b374f3c8636f`
- Latency reconstructed from shared generations is not an independently measured deployment latency.

Interpret the report as exploratory TRAIN-development evidence. Do not use it to train a selector, extend the budget, or claim held-out performance.
