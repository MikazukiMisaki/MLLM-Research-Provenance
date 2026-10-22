# R19-SRC-06: alias evidence validation scope ruling

**APPROVED: narrow validator repair and production synthetic regression tests.** Sol independently reproduced this issue. This ruling changes implementation scope only; it is not implementation PASS, preflight release, launch clearance or scientific execution authorization.

## Reproduction and severity

Severity: MAJOR, blocks valid alias-containing G4 evidence paths. Developer branch codex/r19-source-contract-review-fixes remains based on da7d348ffd3677d619dd31357e1e1e3cca28c9ec with uncommitted repairs. Exact source/test content hashes and stability check are retained in independent_reproduction.json; no dirty tree is approved as an exact commit.

Sol independently executed actual _run_frozen_pilot/run_duration_handoffs and validate_branch_evidence, replacing only model generation/environment edges with synthetic ones. First Stage2 action was valid; later Stage2 attempt was invalid. Frozen suffix order:2,5,4,1,3. All endpoints share checkpoint1; K2 is physically measured first, then K5/K4/K1/K3 alias it. Observed aliases {1:2,2:null,3:2,4:2,5:2}. Raw duration_arm_completed sequences show sourceK2 earlier than K1. K1 correctly charges Stage1+one Stage2 generation (2); K2..K5 charge Stage1+two Stage2 generations (3), including the invalid attempt. Shared physical suffix does not make their recovery generation evidence/cost identical.

Current analyzer validate_branch_evidence, approximately lines955–972 in the developer tree, loops in numeric K order, requires alias_sourceK<currentK and an already numerically validated source row, then requires whole logical_cost and whole evidence_refs equality. All three assumptions conflict with production randomized execution order and frozen per-K recovery accounting. Independently observed exact error: EvidenceIntegrityError: K1 alias is not bound to an exact earlier measured arm. This is separate from SRC-04/05; those producer fixes are still separately required.

## Allowed minimal implementation

Production allowlist extension: scripts/analyze_r19_recovery_duration.py::validate_branch_evidence and only immediately necessary pure local validation helpers in that file. Change its alias authentication logic so 'earlier' means actual authenticated event sequence, consistent with the frozen suffix-order event and same prefix/run/context. Resolve referenced arm completion by exact event ID and K, not ascending numeric-K assumption. Keep exact arm set and frozen ordering/seed validation; do not change scheduler ordering to satisfy a broken validator.

Authenticate:

1. Alias source completion really exists, belongs to the correct prefix/task/run/context and sourceK, predates the alias's execution/completion, and resolves to the actual measured suffix for this endpoint (or valid terminal no-suffix endpoint). Reject self-reference, cycle, dangling/cross-prefix source, future source and inconsistent frozen order. Numeric sourceK may be larger or smaller than aliasK.
2. Endpoint/checkpoint/cursor identity and remaining horizon match the shared physical suffix. Use retained checkpoint/replay/state evidence and start/completion sequence, not success equality alone. Preserve source validation, replay before/after checks and operation-to-action map bindings.
3. Shared suffix generation/transition IDs, replay binding, terminal outcome and termination metadata agree with the actual source suffix. Do NOT require complete evidence_refs equality because recovery generation refs can differ by K. Do not allow a different physical suffix to be passed off as an alias.
4. Each K's own arm event and materialized row remain exactly bound, including its own recovery refs, charged attempts, recovery actions, success and logical costs. Independently reconstruct each arm's recovery-only and full cost from its own recovery refs plus the shared suffix refs. Preserve the invalid later generation's cost, Stage1 inclusion and physical-versus-logical separation. Only the erroneous alias-to-source full-cost equality is removed; cost validation itself must not weaken.
5. Terminal/recovery-stopped aliases are handled without inventing a measured suffix, generations, replay or operations. Per-K treatment and accounting remain as frozen production duration_endpoint/logical_policy_cost define them.

Do not change src/recovery/r19_duration.py::run_duration_handoffs, duration_endpoint, logical_policy_cost, shuffle seed/order, K set, checkpoints, recovery/SFT treatment, prompts/decoding, horizons, quotas, schedule or budgets. Do not rerun an aliased suffix physically. Do not rewrite any authentic old events or branch rows. If the actual scheduler itself proves wrong, return a separate reproduction/scope request before editing it.

## Required tests and independent acceptance

- Production pipeline with invalid later Stage2 reproduces order2,5,4,1,3, K1→K2 alias and all five endpoints. Event/branch validation succeeds after all scoped fixes, followed by nonempty fresh-process synthetic report CLI; real producer/scheduler/journal/registry/validators execute.
- Explicit recovery-call counts2 for K1 and3 for K2..5; independently reconstructed differing logical costs retained, physical suffix generated once, invalid generation charged, total physical counters reconcile without multiplying aliases.
- Cover ordinary distinct endpoints, legitimate same-endpoint aliases to numerically larger/smaller K, terminal aliases and invalid/stopped recovery endpoints while preserving frozen shuffle.
- Negative cases: alias future/self/cyclic/missing source, wrong sourceK/event ID, wrong run/prefix/task, inconsistent checkpoint/state/horizon, swapped suffix refs, forged success/terminal flags and per-K cost or recovery-ref tampering. Each must fail closed at the intended production check; no mock validator success.
- Continue SRC-01..05 and all relevant lifecycle/negative integration tests; disclose any remaining producer/validator issue before repair. Update only necessary amendment/provenance/file-hash references and tests. Do not claim a runtime fingerprint changed if only an unpinned analyzer helper changed; enumerate actual old/new changes honestly.
- Final exact commit, full frozen-base delta, raw test logs, remote verification and G2 impact analysis go to Sol independent review. Developer's46 passing tests and repaired-file status are not independently accepted by this scope ruling. No new exact-SHA PASS exists yet.

## Boundaries and publication

Zero real model/ALFWorld/preflight/live/G4-science operations in this independent reproduction. Real cumulative cost177 generations/342 operations remains unchanged; source headroom8999/8999, all other/global caps unchanged. Genuine G2 remains the old92aae1d execution, no rerun; final new-SHA carry-forward is still subject to Sol's review, especially shared callback changes from SRC-05.

This Sol-owned scope directory is LOCAL_ONLY pending Luna's release of the shared INDEX/inventory publication window. No shared files, scientific source, developer evidence or prior finalized record edited. Do not stage this directory in another agent's commit or report it uploaded. Dispatch receipt, if queued, records only QUEUED, not developer acknowledgement or completion.
