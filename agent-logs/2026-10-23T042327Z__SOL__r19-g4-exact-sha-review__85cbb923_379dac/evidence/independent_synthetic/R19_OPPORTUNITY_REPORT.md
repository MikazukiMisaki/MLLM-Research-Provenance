# R19 recovery-control duration opportunity report

This report is reconstructed from the supplied evidence only. The sample is enriched TRAIN-development data and does not estimate general ALFWorld accuracy.

## Integrity and denominators

- Primary eligible prefixes: 2
- Initial attempted prefixes: 2
- Physical model generations: 352
- Physical environment operations (including replay): 656
- Physical tokens, input/generated/total: 35200/382/35582
- Held-out/task-use scope: not certified for synthetic evidence.

## Success and paired comparisons

| Policy | Successes | N | Rate | Mean full-branch tokens | Mean recovery-only tokens |
|---|---:|---:|---:|---:|---:|
| CONTINUE | 2 | 2 | 1.0 | 2727.0 | NA |
| K1 | 2 | 2 | 1.0 | 2843.0 | 217.0 |
| K2 | 2 | 2 | 1.0 | 2843.0 | 318.0 |
| K3 | 2 | 2 | 1.0 | 2843.0 | 419.0 |
| K4 | 2 | 2 | 1.0 | 2843.0 | 520.0 |
| K5 | 2 | 2 | 1.0 | 2843.0 | 621.0 |

- **K2_vs_K1:** N=2, both-success=2, both-failure=0, wins/losses/ties=0/0/2, mean difference=0.0, exact p=1.0, Holm p=1.0, conservative model-based 95% interval=[-0.8881966011250104, 0.8881966011250104].

- **K3_vs_K1:** N=2, both-success=2, both-failure=0, wins/losses/ties=0/0/2, mean difference=0.0, exact p=1.0, Holm p=1.0, conservative model-based 95% interval=[-0.8881966011250104, 0.8881966011250104].

- **K4_vs_K1:** N=2, both-success=2, both-failure=0, wins/losses/ties=0/0/2, mean difference=0.0, exact p=1.0, Holm p=1.0, conservative model-based 95% interval=[-0.8881966011250104, 0.8881966011250104].

- **K5_vs_K1:** N=2, both-success=2, both-failure=0, wins/losses/ties=0/0/2, mean difference=0.0, exact p=1.0, Holm p=1.0, conservative model-based 95% interval=[-0.8881966011250104, 0.8881966011250104].

## Duration opportunity

- S_fixed: 1.0
- S_oracle: 1.0
- H_success: 0.0
- Outcome patterns K1..K5: `{"11111": 2}`
- States helped / harmed by extra recovery versus K1: 0 / 0
- Development-selected fixed K: 1; success-tied candidates=[1, 2, 3, 4, 5]; final cost-tied candidates=[1, 2, 3, 4, 5].
- The hindsight envelope is opportunity analysis over tested common paths, not a deployable controller or population ceiling.

## Adjacent handoff contrasts

| Contrast | N | Wins | Losses | Ties | Mean difference |
|---|---:|---:|---:|---:|---:|
| K2_minus_K1 | 2 | 0 | 0 | 2 | 0.0 |
| K3_minus_K2 | 2 | 0 | 0 | 2 | 0.0 |
| K4_minus_K3 | 2 | 0 | 0 | 2 | 0.0 |
| K5_minus_K4 | 2 | 0 | 0 | 2 | 0.0 |

## Cost dimensions and net-success cost

Mean logical costs are shown separately; replay/restoration belongs only to physical research expenditure.

| Policy | N | Full input | Full generated | Full calls | Full actions | Recovery input | Recovery generated | Recovery calls | Recovery actions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CONTINUE | 2 | 2700.0 | 27.0 | 27.0 | 27.0 | None | None | None | None |
| K1 | 2 | 2800.0 | 43.0 | 28.0 | 27.0 | 200.0 | 17.0 | 2.0 | 1.0 |
| K2 | 2 | 2800.0 | 43.0 | 28.0 | 27.0 | 300.0 | 18.0 | 3.0 | 2.0 |
| K3 | 2 | 2800.0 | 43.0 | 28.0 | 27.0 | 400.0 | 19.0 | 4.0 | 3.0 |
| K4 | 2 | 2800.0 | 43.0 | 28.0 | 27.0 | 500.0 | 20.0 | 5.0 | 4.0 |
| K5 | 2 | 2800.0 | 43.0 | 28.0 | 27.0 | 600.0 | 21.0 | 6.0 | 5.0 |
- K2_vs_K1: net additional successes=0; tokens per additional net success=None.
- K3_vs_K1: net additional successes=0; tokens per additional net success=None.
- K4_vs_K1: net additional successes=0; tokens per additional net success=None.
- K5_vs_K1: net additional successes=0; tokens per additional net success=None.

## Sampling composition

- Attempted-prefix K1 versus CONTINUE: `{"both_failure": 0, "both_success": 2, "comparator_successes": 2, "harm_rate": 0.0, "losses": 0, "mean_paired_difference": 0.0, "n": 2, "reference_successes": 2, "rescue_rate": null, "ties": 2, "wins": 0}`
- Primary family denominators: `{"look_at_obj_in_light": {"K1_successes": 0, "K2_successes": 0, "K3_successes": 0, "K4_successes": 0, "K5_successes": 0, "n": 0}, "pick_and_place_simple": {"K1_successes": 2, "K2_successes": 2, "K3_successes": 2, "K4_successes": 2, "K5_successes": 2, "n": 2}, "pick_clean_then_place_in_recep": {"K1_successes": 0, "K2_successes": 0, "K3_successes": 0, "K4_successes": 0, "K5_successes": 0, "n": 0}, "pick_cool_then_place_in_recep": {"K1_successes": 0, "K2_successes": 0, "K3_successes": 0, "K4_successes": 0, "K5_successes": 0, "n": 0}, "pick_heat_then_place_in_recep": {"K1_successes": 0, "K2_successes": 0, "K3_successes": 0, "K4_successes": 0, "K5_successes": 0, "n": 0}, "pick_two_obj_and_place": {"K1_successes": 0, "K2_successes": 0, "K3_successes": 0, "K4_successes": 0, "K5_successes": 0, "n": 0}}`
- Primary stratum denominators: `{"failure": {"K1_successes": 0, "K2_successes": 0, "K3_successes": 0, "K4_successes": 0, "K5_successes": 0, "n": 0}, "random_control": {"K1_successes": 0, "K2_successes": 0, "K3_successes": 0, "K4_successes": 0, "K5_successes": 0, "n": 0}, "success_control": {"K1_successes": 2, "K2_successes": 2, "K3_successes": 2, "K4_successes": 2, "K5_successes": 2, "n": 2}}`
- The analysis requires a separate frozen enrollment ledger for source, attempt, eligibility, and exclusion counts; these are not inferred from the outcome table.

## Passive public-state stopping diagnostic

- Primary prefixes / diagnostic records: 2 / 2
- Supported / unsupported predicates: 2 / 0
- Exact measured-suffix mappings / coverage-only cases: 2 / 0
- Satisfied-trigger handoffs / successes / rate: 0 / 0 / None
- Mean detector computation: 4979021.5 ns; new model/environment calls: 0 / 0.
- The diagnostic is mapped to already-measured suffixes only; unsupported or non-exact mapping is not imputed.

## Integrity-qualified interpretation: NO OBSERVED SUCCESS HEADROOM

## Provenance

- Protocol SHA-256: `3d7d1865c807d12276a8109b06c55da4e9182df0ca05a0b5463f8128dd03e122`
- Events SHA-256: `f1d6f7f70dec65ef9f0db0e6ba06cb8d6e77ef28caa5a8391bdc0372e41ba880`
- Branches SHA-256: `012a126b391fb422d531995ea8fd68d591d408d1eb55e3e0e852bc1d52c86785`
- Latency reconstructed from shared generations is not an independently measured deployment latency.

Interpret the report as exploratory TRAIN-development evidence. Do not use it to train a selector, extend the budget, or claim held-out performance.
