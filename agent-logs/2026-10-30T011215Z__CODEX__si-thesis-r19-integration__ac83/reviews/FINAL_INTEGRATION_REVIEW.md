# Final exact-SHA review: integrated SI-U1 and R19 thesis working draft

**Decision: PASS_FOR_WORKING_DRAFT.** This review binds `/home/lizening/research-notes/agent-logs/2026-10-30T011215Z__CODEX__si-thesis-r19-integration__ac83/THESIS_WORKING_DRAFT_SI_U1_R19.md`, SHA-256 `ca948da71a0b8a207c0e7f04d0072f659dc18da8cc67c53f8d262dd55777c0bd`. It is not a thesis-submission approval, full reproducibility claim, or authorization for any scientific experiment.

## Exact amendment and evidence

Removing only the single added sentence, including its preceding space, from the candidate file recovers SHA-256 `7e38e82b164088984b3386df3bbe58562fa980e6645f096c8f779904bbf4fd7a`, the exact previously reviewed integrated draft. The added sentence occurs once, immediately after the post-intervention eligibility qualification at line 98:

> Enrollment was frozen after these initial recovery attempts and before the common recovery paths were extended or their alternative SFT suffixes were evaluated.

This exactly matches the independently proposed wording in `ENROLLMENT_TIMING_CLARIFICATION.md`, SHA-256 `e277fda79cc71b0994bae6d24f24b1da0fb9d4befea2f8f0657f7cdfd904b7b7`. I independently read the frozen implementation `2da980f631badc25086d12db60d128ff507d3ae6:src/recovery/r19_duration.py`: `enrollment_frozen` is emitted after initial attempts and before `execute_frozen_r19_enrollment` extends eligible common paths and invokes handoffs. I located the authentic original enrollment event at ledger sequence 9698, ID `f14635272a407ddf96a0a83e172d3a033ad5ecfb45a7a1941aa41b744f5fd9f4`: it records 39 attempts, eligible strata failure=6, success_control=15, random_control=15, and `additional_stage_two_generations_before_freeze=0`. This is a bounded source-and-event check; it is not a new complete ledger audit or reproduction of execution.

The added sentence does not assert freezing before all intervention or before source outcomes: primary eligibility still depends on the initial recovery stage, and original source outcomes contribute to the enriched selection. The wording limits the freeze to before path extensions and alternative suffix evaluation. It addresses the methods-completeness note in the previous integration review without removing the selection caveat.

## Carried-forward exact-SHA reviews

The independently reviewed R19 V2 source `60a679691403be15c308d68f496b6b1a8c7a628ad37cfe7f9a79e808b942d277` is accepted for a working thesis with stated limits by `R19_V2_ACCEPTANCE.md`, SHA-256 `180d42ca9ab3b0aee23fde4bd37c74c1360564d87754ed1da26254c29c666707`. The earlier integration review `INDEPENDENT_INTEGRATION_REVIEW.md`, SHA `6ab94465166efbe2968c51e48c5f6dcf8ae71e8498abbd7947e447bfd2247f3a`, documents section replacement, controls, denominator and cost distinctions, hindsight oracle limitations, the 9-reference scan, privacy boundaries, and source hashes. Its pending-R19-review qualification is resolved by the independent acceptance above; all other scientific and confidentiality limitations remain.

The linked figure remains available at its relative SVG path. The integrated copies retain the separately reviewed hashes: SVG `e60ecbf7a84768226db99ecdc7e957e109aa45e3d8f2c4c3831e63727395dfd2`, PDF `7f64ecb093a057700ce113498d836ab66982b3cca3cd99f5c17461f5983c458a`, and PNG `912abdd0c0904976e34be33431a0c6d5fc8fb009d9a7c7d677e2f69c7c3c20bd`. Preserve `figures/` with the Markdown whenever moving or publishing the draft.

Nine citations remain paired with bibliography entries. The work remains an evidence-bounded, nonrandomized exploratory fixed-TRAIN comparison and separate post-intervention-conditioned recovery study, not a demonstrated generalizable improvement or deployable oracle. Private material, task identities, trajectories and incomplete remote full-content verification must not be treated as public or fully reproducible data. Formatting, institution-specific references, permissions and supervisor feedback remain open before submission.

No original draft, source, figure, ledger, or scientific code was modified during this review. No model, GPU, ALFWorld, G3/G4 process, or new scientific evaluation was run.
