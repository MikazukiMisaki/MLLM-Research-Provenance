# R19 recovery-control duration opportunity report

This report is reconstructed from the supplied evidence only. The sample is enriched TRAIN-development data and does not estimate general ALFWorld accuracy.

## Integrity and denominators

- Primary eligible prefixes: 0
- Initial attempted prefixes: 1
- Physical model generations: 4
- Physical environment operations (including replay): 0
- Physical tokens, input/generated/total: 80/12/92
- Held-out/task-use scope: not certified for synthetic evidence.

## Success and paired comparisons

| Policy | Successes | N | Rate | Mean full-branch tokens | Mean recovery-only tokens |
|---|---:|---:|---:|---:|---:|
| CONTINUE | 0 | 0 | NA | NA | NA |
| K1 | 0 | 0 | NA | NA | NA |
| K2 | 0 | 0 | NA | NA | NA |
| K3 | 0 | 0 | NA | NA | NA |
| K4 | 0 | 0 | NA | NA | NA |
| K5 | 0 | 0 | NA | NA | NA |

- **K2_vs_K1:** N=0, both-success=0, both-failure=0, wins/losses/ties=0/0/0, mean difference=None, exact p=1.0, Holm p=1.0, conservative model-based 95% interval=None.

- **K3_vs_K1:** N=0, both-success=0, both-failure=0, wins/losses/ties=0/0/0, mean difference=None, exact p=1.0, Holm p=1.0, conservative model-based 95% interval=None.

- **K4_vs_K1:** N=0, both-success=0, both-failure=0, wins/losses/ties=0/0/0, mean difference=None, exact p=1.0, Holm p=1.0, conservative model-based 95% interval=None.

- **K5_vs_K1:** N=0, both-success=0, both-failure=0, wins/losses/ties=0/0/0, mean difference=None, exact p=1.0, Holm p=1.0, conservative model-based 95% interval=None.

## Duration opportunity

- S_fixed: None
- S_oracle: None
- H_success: None
- Outcome patterns K1..K5: `{}`
- States helped / harmed by extra recovery versus K1: 0 / 0
- Development-selected fixed K: None; success-tied candidates=[]; final cost-tied candidates=[].
- The hindsight envelope is opportunity analysis over tested common paths, not a deployable controller or population ceiling.

## Adjacent handoff contrasts

| Contrast | N | Wins | Losses | Ties | Mean difference |
|---|---:|---:|---:|---:|---:|
| K2_minus_K1 | 0 | 0 | 0 | 0 | None |
| K3_minus_K2 | 0 | 0 | 0 | 0 | None |
| K4_minus_K3 | 0 | 0 | 0 | 0 | None |
| K5_minus_K4 | 0 | 0 | 0 | 0 | None |

## Cost dimensions and net-success cost

Mean logical costs are shown separately; replay/restoration belongs only to physical research expenditure.

| Policy | N | Full input | Full generated | Full calls | Full actions | Recovery input | Recovery generated | Recovery calls | Recovery actions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CONTINUE | 0 | None | None | None | None | None | None | None | None |
| K1 | 0 | None | None | None | None | None | None | None | None |
| K2 | 0 | None | None | None | None | None | None | None | None |
| K3 | 0 | None | None | None | None | None | None | None | None |
| K4 | 0 | None | None | None | None | None | None | None | None |
| K5 | 0 | None | None | None | None | None | None | None | None |
- K2_vs_K1: net additional successes=0; tokens per additional net success=None.
- K3_vs_K1: net additional successes=0; tokens per additional net success=None.
- K4_vs_K1: net additional successes=0; tokens per additional net success=None.
- K5_vs_K1: net additional successes=0; tokens per additional net success=None.

## Sampling composition

- Attempted-prefix K1 versus CONTINUE: `{"both_failure": 1, "both_success": 0, "comparator_successes": 0, "harm_rate": null, "losses": 0, "mean_paired_difference": 0.0, "n": 1, "reference_successes": 0, "rescue_rate": 0.0, "ties": 1, "wins": 0}`
- Primary family denominators: `{"look_at_obj_in_light": {"K1_successes": 0, "K2_successes": 0, "K3_successes": 0, "K4_successes": 0, "K5_successes": 0, "n": 0}, "pick_and_place_simple": {"K1_successes": 0, "K2_successes": 0, "K3_successes": 0, "K4_successes": 0, "K5_successes": 0, "n": 0}, "pick_clean_then_place_in_recep": {"K1_successes": 0, "K2_successes": 0, "K3_successes": 0, "K4_successes": 0, "K5_successes": 0, "n": 0}, "pick_cool_then_place_in_recep": {"K1_successes": 0, "K2_successes": 0, "K3_successes": 0, "K4_successes": 0, "K5_successes": 0, "n": 0}, "pick_heat_then_place_in_recep": {"K1_successes": 0, "K2_successes": 0, "K3_successes": 0, "K4_successes": 0, "K5_successes": 0, "n": 0}, "pick_two_obj_and_place": {"K1_successes": 0, "K2_successes": 0, "K3_successes": 0, "K4_successes": 0, "K5_successes": 0, "n": 0}}`
- Primary stratum denominators: `{"failure": {"K1_successes": 0, "K2_successes": 0, "K3_successes": 0, "K4_successes": 0, "K5_successes": 0, "n": 0}, "random_control": {"K1_successes": 0, "K2_successes": 0, "K3_successes": 0, "K4_successes": 0, "K5_successes": 0, "n": 0}, "success_control": {"K1_successes": 0, "K2_successes": 0, "K3_successes": 0, "K4_successes": 0, "K5_successes": 0, "n": 0}}`
- The analysis requires a separate frozen enrollment ledger for source, attempt, eligibility, and exclusion counts; these are not inferred from the outcome table.

## Passive public-state stopping diagnostic

- Primary prefixes / diagnostic records: 0 / 0
- Supported / unsupported predicates: 0 / 0
- Exact measured-suffix mappings / coverage-only cases: 0 / 0
- Satisfied-trigger handoffs / successes / rate: 0 / 0 / None
- Mean detector computation: None ns; new model/environment calls: 0 / 0.
- The diagnostic is mapped to already-measured suffixes only; unsupported or non-exact mapping is not imputed.

## Integrity-qualified interpretation: INCONCLUSIVE

## Provenance

- Protocol SHA-256: `3d7d1865c807d12276a8109b06c55da4e9182df0ca05a0b5463f8128dd03e122`
- Events SHA-256: `9eb2d62dc01b5a2d45f25cb8c1cc6c8f6e613163e17d9d2ab832446f646a6639`
- Branches SHA-256: `5370ae8bdf8e256766525756607b4fc40ffc66c4fa4c1dc1fad7eca77d43412d`
- Latency reconstructed from shared generations is not an independently measured deployment latency.

Interpret the report as exploratory TRAIN-development evidence. Do not use it to train a selector, extend the budget, or claim held-out performance.
