# SI-P3 Task Isolation and Finite-Budget Design

**Status: design-only; no science, launch, training, or evaluation authorization.** This is an identity/hash/family metadata proposal, not an executable schedule. No task body, unused result, model, environment, tokenizer, project validator, or pytest was used.

## Recommendation

Retain the proposed fixed partition sizes as a reviewable upper-bound plan: 480 acquisition TRAIN identities, 60 development TRAIN identities, 600 final-evaluation TRAIN identities, and one unallocated TRAIN identity. Partition once, before any CONTINUE or recovery outcome is observed, using canonical task/trial identities and an outcome-blind SHA-256 order within each of the six task families. The exact assignment and per-family cross-counts are in `partition_proposal.json`.

This allocation is arithmetically feasible: 1,141 supported TRAIN metadata candidates are split into 480 + 60 + 600 + 1. It is not evidence that all candidates are pristine: the 2,612 registered known-use identities are excluded, but registry completeness and unregistered historical viewing cannot be proven from these metadata. The 74 `valid_unseen` candidates are unused and are not called held-out.

One important coverage limit is explicit: `look_at_obj_in_light` has only two supported TRAIN candidates, so it cannot appear in all three task-disjoint partitions. The deterministic allocation gives one to final evaluation, none to development, one to acquisition. Do not transfer quotas or replace identities after outcomes. If the protocol requires every family in every partition, this reference design is infeasible without a separately justified change to scope/targets; do not silently relax that requirement.

The 600-task evaluation is a planning reference, not a power guarantee or a claim of a universal minimum. No acquisition tranche is authorized here. If a later execution is separately authorized, the initial 96-task feasibility tranche must be reviewed independently; the remaining 384 must not begin automatically.

## Identity and partition rule

1. Freeze the supported TRAIN identity/hash input and the complete known-use union before collecting outcomes. Exclude any identity in that union. Require the supplied SHA-256 to equal SHA-256 of the canonical UTF-8 identity string.
2. The split unit is the canonical task/trial. Every seed, prefix, alias, derivative, or replay mapped to that task/trial inherits the same partition; never split at episode-prefix level.
3. For each candidate identity, define `rank = SHA256(UTF8("SI-P3-task-partition-v1\n" + family + "\n" + canonical_identity + "\n"))`.
4. Within family, sort ascending by `rank`. Assign family quotas by largest remainder (remainder descending, family-name lexical tie-break): allocate final evaluation 600 from the full candidate family counts; allocate development 60 from the remaining counts; allocate acquisition 480 from what remains; leave one reserve. This ordering and all identity rows are frozen in the proposal. It is deterministic and outcome-blind, but is not a scientific schedule or launch manifest.
5. Verify all four identity sets are disjoint, their union is exactly the 1,141 TRAIN candidates, no identity intersects known-use, and the 74 `valid_unseen` identities appear nowhere. Any failed check means stop and redesign before data/outcomes are observed.

| Candidate family | TRAIN candidates | Acquisition 480 | Development 60 | Evaluation 600 | Reserve |
|---|---:|---:|---:|---:|---:|
| look_at_obj_in_light | 2 | 1 | 0 | 1 | 0 |
| pick_and_place_simple | 419 | 176 | 22 | 220 | 1 |
| pick_clean_then_place_in_recep | 301 | 127 | 16 | 158 | 0 |
| pick_cool_then_place_in_recep | 194 | 82 | 10 | 102 | 0 |
| pick_heat_then_place_in_recep | 106 | 44 | 6 | 56 | 0 |
| pick_two_obj_and_place | 119 | 50 | 6 | 63 | 0 |
| **Total** | **1,141** | **480** | **60** | **600** | **1** |

This is a proportional largest-remainder allocation with sequential rounding. It deliberately does not impose an impossible six-family-per-partition constraint. The full per-identity proposal contains hashes and family labels only.

## Controlled experience design boundary

The common comparison is frozen P0 actor A versus student recipes B and C on the same exact acquisition source pool. B is success-only and must include qualifying C examples; C is the B subset filtered to source-baseline CONTINUE failures, not a distinct algorithm. Freeze one anchor and the whole task schedule before outcomes. Keep all failures, non-rescues, invalid generations, and empty-positive outcomes in the accounting. There is no success quota, top-up, outcome-dependent anchor choice, or task replacement.

Use only the already specified single K=1 teacher recovery: original Qwen3-8B/P0 actor and teacher, common H=50, greedy decoding, unchanged prompt/map/operator, Stage1 cap 40 and Stage2 cap 16, actor cap 16. Train only the first recovery action label; an adapter-on suffix is terminal evidence and never a target or input to the student. Source CONTINUE is generated once and reused as the baseline if its existing deterministic/replay binding is valid. One exact prefix replay is a physical reset plus the already observed prefix actions, with no extra comparison model call. These are protocol-bound design statements, not authorization to run them.

The two registered comparisons remain C>A and C>B. Later analysis, if separately authorized, must report exact paired McNemar tests with Holm adjustment at the stated .025/.05 levels, full paired wins/losses/net/gross harm, and 10% Newcombe marginal intervals. The stated observed decision guard is net lift at least 5 percentage points and gross harm no more than 5%; no result may be selected after inspection. A single training seed cannot support a cross-seed claim, and R19 oracle results do not estimate power. The historical B95/C10 and strict 29/1 pool is motivation/case history, not a new training or evaluation pool.

## Cost model and ledgers

See `budget_design.json` for machine-readable arithmetic. At a source failure/decision index `d` in 0..49, one acquired task has worst-case physical totals:

- Source CONTINUE: up to 50 generations, 50 actions, one reset; reused as baseline rather than repeated per arm.
- Prefix replay: one reset and exactly `d` actions; zero model calls.
- Teacher: exactly two calls, Stage1 + Stage2, with at most 40 + 16 output tokens. Stage2 supplies the one recovery action.
- P0 suffix: at most `49-d` actor generations/actions, 16 output tokens each.
- Total: `101-d` generations (maximum 101), 100 non-reset actions, two resets (102 reset-inclusive environment operations), and at most `1640-16d` output tokens (maximum 1,640).

Therefore the cap-based totals are: N=96 feasibility, at most 9,696 generations / 9,600 actions / 192 resets / 9,792 environment operations / 157,440 output tokens; N=480 total reference, at most 48,480 / 48,000 / 960 / 48,960 / 787,200. The incremental 384 after 96 would be 38,784 / 38,400 / 768 / 39,168 / 629,760, but is not authorized and is not automatic.

For E=600, three arms A/B/C each capped at H=50 imply at most 90,000 generations, 90,000 actions, 1,800 resets, 91,800 reset-inclusive operations, and 1,440,000 actor output tokens at 16 per call. No teacher calls are included in evaluation. Keep this evaluation ledger separate from acquisition. Combined N96+E600 and N480+E600 arithmetic appears in `budget_design.json` only as a planning illustration, not one fungible authorization.

Physical shared-pool accounting charges every real source generation, replay reset/action, teacher call, suffix generation, action, and output token once. Logical per-policy accounting reports each arm's exposure and outcome separately but does not multiply the shared source trajectory by the number of arms. Do not double-count wrapper events that merely reference an existing physical event. R19's historical 5,142 generations / 7,949 reset-inclusive environment operations remain separate; its predecessor 177/342 is already included and is not added again. SI-P3 adds zero scientific calls in this task.

Software smoke, development execution, training, and infrastructure/GPU spend are separate budget lines, not zero-cost inclusions. None is authorized or included in the totals above. Before any later freeze, record exact serialized prompts and token-count distributions, pinned tokenizer/model/adapter identities, max context and truncation policy, stage/actor prompt lengths, target masking, training steps/epochs/batch/accumulation/sequence/padding settings, total token accounting, and an explicit GPU-hour/device-second ceiling. Historical `input_tokens_seen` has unresolved padding semantics and cannot establish a reliable training-cost bound. No runtime estimate is asserted here.

## Evidence and fail-closed controls

**Before any future data collection:** freeze and hash the identity registry, candidate metadata, partition proposal, family quotas, protocol/config/model/adapter/runtime, prompt, schedule and exclusion mapping; have an independent reviewer reproduce identity-hash and disjointness checks; bind a unique run and empty output destination only after separate authorization. Keep the decision thresholds and analysis plan outcome-blind.

**During any separately authorized work:** append-only raw events with stable task/arm/operation IDs, exact argv/cwd/allowlisted environment, wall-clock and process receipts, input/output hashes, generation token counts, reset/action counts, task-level completion state, and physical-versus-logical links. Charge resets, replay, failures, invalid outputs, and retries (if a future protocol explicitly permits retries) to the same cumulative ledger. This design itself permits no retry.

**After any future run:** preserve original logs/receipts and hashes; verify all pre/post input bindings, assignment disjointness, schedule/exclusion identity, event-to-artifact links, task and arm denominators, caps, and independent analysis inputs before reading efficacy summaries. Publish no efficacy claim if any required integrity gate is unresolved.

**Stop without repair/retry/reassignment** on any hash drift, identity collision, alias mapping uncertainty, missing/duplicate operation, ambiguous physical operation, unplanned call, quota/cap exceedance, task/result leakage, output corruption, process interruption, or inability to bind an event to its task and arm. Preserve the incomplete unit and its raw evidence. Do not change thresholds, family quotas, task anchors, or exclusions after viewing outcomes. Any failed family-capacity or disjointness condition returns to design review; never fill from valid_unseen or an outcome-selected replacement.

## Non-authorization statement

This deliverable creates no runnable schedule, gate, argv, or output directory. It authorizes no smoke, dev run, acquisition, replay, training, evaluation, model/environment/tokenizer call, validator, or pytest. Any future execution requires a separate task and explicit authorization with a newly reviewed frozen plan.
