# R19 Luna execution readiness — task record

- Agent/task: Codex/Luna, Experiment Operator & Provenance Owner; read-only execution-readiness inspection and handoff report.
- Start UTC: 2026-10-22T23:05:30Z. Finish UTC: 2026-10-22T23:10:14Z.
- Status: `NOT_READY_FOR_EXECUTION`; exact-SHA implementation review failed; no launch gate or preflight.
- Scientific repository: `/home/lizening/wt-r19-recovery-duration-v1`; starting/ending SHA `da7d348ffd3677d619dd31357e1e1e3cca28c9ec`; branch `codex/r19-source-contract-repair`; worktree clean and remote branch SHA matched.
- Scope: read-only inspection only. No scientific repository files, code, tests, model, prompts, data, frozen configs, local gates, registries, manifests or raw evidence were changed.
- Main deliverable: `R19_LUNA_EXECUTION_READINESS.md` in this task directory.

## Observations

- No R19 supervisor/runner process was present; recorded historical PIDs 759377 and 759380 were absent. Available R19 output inventory contains the known two G2 runs and one G3 failed run only.
- Failed run `3d1ccea7e97f4727abf8e216ac6ec498` has authentic subprocess exit 1. Its event journal SHA is `fde95fcd72f1c4ac6409fab7f2112654e145f6184fefec690cae58ad345f1cd7`, with exactly four events: one reset start/completion and one generation start/completion. Delta: 1 generation (267 input + 5 generated tokens), 1 reset, 0 action steps, 0 completed source episodes, 0 incomplete external operations. Cumulative cost remains 177 generations / 342 environment operations including resets.
- Preserved unit registry status remains `in_progress`, and execution manifest status remains `RUNNING`; authentic supervisor receipts show failed/exit 1 and no active process. Preserve both raw statuses.
- Existing append-only known-failed event SHA `58783ba60b076ee190dccb0875aac65891d7e1c811e00fbe6303ca65896369d9` is recorded in the readiness report and exact file hash; the independent review independently accepts the known-failed disposition. Its `review_status=PENDING_EXACT_SHA_REVIEW` field is stale. Luna did not alter it; a new appended adjudication/review receipt or reviewed amendment is needed to reconcile without rewriting history.
- Frozen R19-B1 input hashes, 127 unique TRAIN identities, exact index-zero failed identity, source/recovery quotas, K=1..5, horizon 50, phase/global ceilings, G2 run/SHA, current runtime package metadata and local runtime paths are recorded in the readiness report.
- Independent review artifact `independent_review.json`, SHA `8fcd731bcbfd01b2e89228e79f70834e15c57a5f3502e1a68f559355ab2e3c40`, targets exact SHA `da7d348ffd3677d619dd31357e1e1e3cca28c9ec`: `IMPLEMENTATION_REVIEW=FAIL`; `G2_CARRY_FORWARD=PASS` only for authentic prior evidence/unchanged smoke semantics; positive preflight eligibility NO; launch clearance NOT ISSUED. It identifies three defects: restart comparator repeats at source index 1, standalone clean-process G4 comparator import failure, and persisted trajectory digest mismatch.
- A separate untracked Sol evidence directory appeared during this task. Its preliminary synthetic probes independently reproduce those same lifecycle/import/hash defects and report zero real model/ALFWorld calls. It has no final review record at inspection and was preserved unstaged.
- A prior positive preflight did exit 0 with `PREFLIGHT_ONLY_PASS`, but it was bound to implementation SHA `bf31f3da430ffc35bd17fc380e1752adce6d1467` and gate SHA `63d6634f14fe9f768b3cc8c4120d7b85ba09bd54ca2b8e1f2c103a705137e1ee`; it is not reusable for the current/replacement code.
- At inspection, provenance local `main` and `origin/main` both matched `d54ebb7eec421f6e5c70565f895adfdbe6498ee2`. Existing failure and exact-review artifacts are tracked there. Four unrelated untracked provenance folders were preserved and not staged.

## Commands, tests, and effects

- Read-only command summaries are in `commands.log`.
- Tests executed by Luna: none. The independent reviewer reports 93 targeted tests passed on da7d348, but that did not resolve the reproduced lifecycle/G4/hash blockers.
- Model calls/generations in this task: 0. ALFWorld constructions/resets/steps: 0. G2 reruns: 0. G3 preflights/live launches: 0. G4 analyses: 0. Held-out/training: 0.
- No new output directory, process, operation, or exit code was synthesized.

## Decision and next authorized step

No execution readiness is granted. Wait for New Agent's corrected implementation, Sol's independent exact-SHA PASS, an append-only/reviewed reconciliation of the stale unit-resolution review marker, and explicit new execution authorization/formal handoff. Only then construct a new ignored gate and conduct fresh positive preflight. Do not reuse old gates or the bf31 preflight; do not run G2 again. No current preflight, launch, or G4 was authorized or performed by this task.

Provenance synchronization for this report: create a SHA inventory, scan for secrets, update `INDEX.md`, stage only this task's safe report/record/log files, push to `MLLM-Research-Provenance/main` without force, then verify local and remote SHAs. Existing unrelated untracked paths must remain untouched.
