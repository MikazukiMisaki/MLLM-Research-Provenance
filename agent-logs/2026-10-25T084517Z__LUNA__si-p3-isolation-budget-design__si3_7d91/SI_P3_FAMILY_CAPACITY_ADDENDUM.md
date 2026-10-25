# SI-P3 family-capacity addendum

**Disposition: accept the five-family proposal for further design review, with scope limits below.** This addendum does not edit or erase the initial 480/60/600/1 draft. That draft is retained unchanged as historical; its six-family/general-purpose interpretation is blocked by the observed `look_at_obj_in_light` capacity of two. The new identity-only partition proposal is separate and supersedes the earlier allocation only for review.

## Recommendation and exact allocation

Define the main target population as the five non-light TRAIN families only. Exclude both `look_at_obj_in_light` candidate identities from all partitions and mark them retained-but-unrun; do not transfer their two slots to another quota as an after-the-fact outcome adjustment. This is a declared population restriction, not a claim about all ALFWorld families. Any result has no `look_at_obj_in_light` generality claim.

The five-family candidate total is 1,139. Use a fixed 480 acquisition / 48 engineering-development / 600 final-evaluation / 11 reserve allocation, all task/trial-disjoint. The 48 identities are reserved only for engineering interface compatibility; they are not a policy-development set, must not be used to compare recipes or select an effect-based recipe, and need not be consumed merely because they are reserved. Prefer synthetic interface fixtures. Any future use of real tasks or physical model/environment operations requires its own explicit release and budget.

Allocate by a sequential Hamilton largest-remainder rule from the remaining five-family capacities: final evaluation 600 first, engineering development 48 second, acquisition 480 third, and the rest reserve. For each stage, calculate each family’s quota as `floor(stage_total * remaining_family_capacity / remaining_total)`, then distribute residual slots by fractional remainder descending and lexical family-name tie-break. Within family, retain the existing outcome-blind canonical identity hash ordering. The exact per-family cross-counts are:

| Family | Capacity | Acquisition 480 | Engineering interface reserve 48 | Final evaluation 600 | Unallocated reserve 11 |
|---|---:|---:|---:|---:|---:|
| pick_and_place_simple | 419 | 176 | 18 | 221 | 4 |
| pick_clean_then_place_in_recep | 301 | 127 | 13 | 158 | 3 |
| pick_cool_then_place_in_recep | 194 | 82 | 8 | 102 | 2 |
| pick_heat_then_place_in_recep | 106 | 45 | 4 | 56 | 1 |
| pick_two_obj_and_place | 119 | 50 | 5 | 63 | 1 |
| **Total** | **1,139** | **480** | **48** | **600** | **11** |

The Hamilton table is an exact partition of the five-family metadata pool: 480+48+600+11=1,139. The two light identities are outside this denominator and remain unrun. No quota is transferred to or from them.

`partition_proposal_family_capacity_addendum.json` contains only canonical identity, identity SHA-256, family, assigned partition, and the deterministic rank hash. It is a non-executable metadata proposal, not a schedule, gate, argv, or authorization. The hash ordering is `SHA256(UTF8("SI-P3-task-partition-v1\n" + family + "\n" + canonical_identity + "\n"))`; task/trial is the split unit and all aliases, seeds, prefixes, or derivatives inherit that one assignment.

## Design implications and limits

- This is TRAIN task-disjoint final evaluation, not held-out evaluation. The 74 `valid_unseen` candidates remain unused and are not rebranded as held-out.
- The registered 2,612 known-use identities remain excluded. Zero overlap is a registry-based exclusion only; it does not prove no unregistered historical exposure or alias.
- The 480-task acquisition cap and its optional 96+384 phases do not change. 96 is still feasibility-only; the additional 384 never starts automatically. The 600 evaluation count is still a planning reference, not a power guarantee or authorization.
- The 48 engineering identities are not required for stage-0/software development and cannot become a policy-tuning dataset. No observed policy success, recovery, or estimated treatment effect may decide which recipe is chosen. If later engineering needs actual model/environment operations, budget those as a distinct authorized activity; do not hide them in the acquisition/evaluation budget. If all 48 were ever run through the full per-task upper-bound protocol, the illustrative ceiling would be 4,848 generations, 4,896 reset-inclusive environment operations, and 78,720 output tokens; this addendum does not authorize that spend.
- The acquisition and evaluation physical caps from `budget_design.json` remain unchanged because their N and E are unchanged. Logical per-policy outcomes must continue referencing the one shared source episode; no duplicate physical source generation.
- R19 remains historical 5,142 generations / 7,949 reset-inclusive environment operations; its earlier 177/342 is already included. No new scientific operation was performed for this addendum.

## Fail-closed handling

Before any future execution, re-verify canonical identity hashes, complete known-use intersection, partition disjointness, family quotas, frozen source inputs, and all task-to-alias mappings. Any identity or alias collision, metadata drift, family capacity mismatch, task leakage, unplanned physical call, or ambiguous operation stops the work without replacement or retry. Preserve the initial draft and this addendum as separate records; independent review must decide whether the five-family estimand and 48-task engineering reservation are acceptable before any executable plan is created.

This remains design-only. It does not authorize schedule generation, model/environment/tokenizer calls, interface smoke on real tasks, policy replay, training, or evaluation.
