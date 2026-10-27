# SI-S01 isolation and bounded-budget evidence

Status: `READ_ONLY_EVIDENCE_COMPLETE_DESIGN_SUPPORT_ONLY_NOT_AUTHORIZATION`  
Created: 2026-10-27 02:45 UTC  
Scope: existing identity metadata, accepted A96 source output summaries, and prior execution receipts only.

## Result

The accepted A96 run used 96 canonical TRAIN task/trial identities. The append-only observed-use receipt marks all 96 `ever-used TRAIN`; it is not a model-training or held-out label. Re-parsing the frozen 2,612-identity exact known-use union found zero exact task/trial intersections with these 96. The 96 also exactly equal the previously reserved acquisition-feasibility partition, and have zero overlap with the earlier 171-row/169-unique same-pool cohort.

The P3 metadata partitions contain 600 final-evaluation TRAIN identities, 48 engineering-development TRAIN identities, the now-consumed 96 acquisition identities, and 395 unallocated nonlight reserves; two light-task candidates remain excluded and unrun. The 1,139 partition rows plus the two light identities exactly equal the 1,141 supported TRAIN-candidate identities. The partitions are pairwise disjoint, and each is disjoint at exact task/trial level from the 2,612 registered union and the 0/74 valid-seen/valid-unseen candidate metadata. Thus 600 task-disjoint TRAIN evaluation identities remain reserved in metadata, but none has been run. They are not “held out.”

The exact registration results do not prove that all historical views were registered. The preserved P1 register explicitly leaves historical viewing absence unproven and some R4/R16–R18 prefix-to-task mappings partially unresolved. Its valid-unseen difference of 74 is only a known-use difference, not a clean/held-out certificate; this audit did not open those task payloads. Exact task/trial disjointness also does not rule out shared scenes/layouts/objects or near-duplicate prompts. Seeds, prefixes, and aliases inherit the consumed identity status under the saved canonical rule.

Observed A96 outcomes are 79 successes and 17 failures among 96 TRAIN development sources. All 17 failures ended after 50 actions with `done=true`, reward 0, and `truncated=false`. Seven other cases are not failures: they are simple-placement successes terminal after exactly five actions (`done=true`, reward 1), so they have no usable post-S5 intervention state. The usable S5 pool is 17 failures plus 72 successes (89 total). The production structural counts remain E=89/F=17/S=72 and `COMPLETE_SOURCE96_STRUCTURAL_NO_GO`; the preregistered F minimum was not met. Do not infer recoverability or a learning effect.

## Physical cost ledger

| Scope | Generations | Reset-inclusive environment operations | Other observed cost |
|---|---:|---:|---|
| Historical science before A96 | 5,142 | 7,949 | Existing accepted total |
| SI-S01 A96 source increment | 1,959 | 2,055 | 1,164,593 input tokens; 9,795 output tokens; 96 resets + 1,959 steps; 0.5624755 allocated device-hours |
| Cumulative science only | 7,101 | 10,004 | Exactly the two scientific rows above |
| SI-S01 engineering adapter (separate) | 1 | 7 | 267 input / 5 output tokens; 1 reset + 6 saved steps; 0.0209157 allocated device-hours |
| SI-E2 failed engineering diagnostic (separate) | 0 | 0 | 0 tokens; failed/open model-load unit before weights; 0.0066242 allocated device-hours |
| SI-E2 identity-only probe (separate) | 0 | 0 | 1-byte CUDA tensor; 512 bytes allocated / 2 MiB reserved; no model/environment; ownership still unproven |

Engineering rows are not added to the 7,101/10,004 scientific totals. The source run used nonexclusive shared-container allocation accounting; NVML-to-local-PID mapping remains `UNPROVEN_NOT_ASSERTED`. These records establish neither exclusive GPU access nor free-memory or inference-fit estimates.

## Comparison boundary and candidate ceilings

The source run contains a historical P0 trajectory and S5 public snapshot references for the 96 sources. Without fresh CONTINUE calls, those records are a descriptive reference only. Replaying saved P0 commands is a physical action replay, not a new policy decision. A fresh same-task CONTINUE arm adds up to 45 generations/actions per branch after reset and five-action prefix replay; even exact equality of the public observation and ordered action map cannot prove identical hidden simulator/RNG state.

The companion [BUDGET_CANDIDATES.json](BUDGET_CANDIDATES.json) gives per-arm maxima. Under candidate caps of Stage1=40, Stage2=16, P0=16 output tokens and 8,192 input tokens per generation:

- 17 failure interventions alone: at most 782 generations, 12,920 output tokens, 6,406,144 input tokens, 17 resets, 850 physical steps, and 867 reset-inclusive operations.
- Add a fresh CONTINUE arm on those same 17 failures: at most 1,547 generations, 25,160 output tokens, 12,673,024 input tokens, 34 resets, and 1,734 operations.
- Add 17 S5-usable positive P0 controls: at most 2,312 generations, 37,400 output tokens, 18,939,904 input tokens, 51 resets, and 2,601 operations.

The additive [LATE_ANCHOR_ARITHMETIC_ADDENDUM.md](LATE_ANCHOR_ARITHMETIC_ADDENDUM.md) calculates a separate conditional five-case late-anchor option from coordinator-supplied replay depths. Its identities and semantic eligibility are not independently verified here; it does not replace or change any fixed-S5 17-failure calculation above.

The last scenario exceeds a 16M input-token candidate cap. The suggested 1.0/2.0 allocated-device-hour ceilings are hard-stop candidates, not runtime predictions or capacity claims. All candidate ceilings require prospective adoption and new authorization; old unused budgets are not transferable.

Before any future run, freeze arm definitions and identities, context/token limits, model-load count, one-shot resource accounting, and stop rules. Enforce exact pre-action S5 state comparison; stop without replacement on identity mismatch, replay divergence, invalid action mapping, incomplete operation, unproven GPU ownership, or any cap. No teacher/training/held-out/G4, top-up, retry, or effect-based arm selection is authorized here.

## Evidence files

- [SI_S01_ISOLATION_AND_COST_AUDIT.json](SI_S01_ISOLATION_AND_COST_AUDIT.json) contains the machine-readable joins, outcomes, cost math, comparison limits, and input path/size/SHA-256 bindings.
- [BUDGET_CANDIDATES.json](BUDGET_CANDIDATES.json) contains formula-derived design-only cost scenarios and fail-stop candidates.
- [LATE_ANCHOR_ARITHMETIC_ADDENDUM.md](LATE_ANCHOR_ARITHMETIC_ADDENDUM.md) contains only the requested conditional arithmetic extension.
- `FILE_HASHES.sha256` records the final hashes of these task-owned deliverables; no shared index or repository publication was touched.
