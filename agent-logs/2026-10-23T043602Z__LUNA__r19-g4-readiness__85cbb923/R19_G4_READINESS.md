# R19 G4 readiness — proposal only

Status: **READY_FOR_PROPOSAL_REVIEW / PREPARATION_ONLY / FORMAL_G4_NOT_AUTHORIZED**
Prepared: 2026-10-23 04:36 UTC by Luna
Scientific task: R19-B1 G4 offline analysis preparation; no analysis executed.

## Authorization boundary

The exact-SHA analyzer review is `IMPLEMENTATION_REVIEW=PASS` for analyzer source `85cbb92395e5e2420c2adeb1fa0634653e742910`. This is not formal G4 authorization or launch clearance. This task performed only static review, Git/process inspection, file hashing, and absence checks. No analyzer entrypoint, validator, test, report/statistic function, model, ALFWorld environment, supervisor, preflight, G2, G3, or retry was invoked. No report output was created. A fresh direct human authorization and separate formal release remain required after proposal review.

## Scientific identities and input custody

- Executed G3 source: `2da980f631badc25086d12db60d128ff507d3ae6`; run `260422ac02bd42a8b2929d7ef240526b`; authentic child exit `0`, status `completed`.
- Reviewed analyzer source: `85cbb92395e5e2420c2adeb1fa0634653e742910`; analyzer raw SHA-256 is recorded in `input_hashes.json`. Analyzer SHA is distinct from the G3 execution SHA.
- Original execution root/CWD remains `/home/lizening/wt-r19-recovery-duration-v1`; original supervisor receipt directory remains `/home/lizening/research-notes/agent-logs/2026-10-23T002200Z__LUNA__r19-g3-live-successor__2da980f/supervisor_live`. The analyzer's C02 consumer resolves its sibling `launch_context.json` from this original receipt directory.
- Reviewed analyzer checkout `/home/lizening/wt-r19-g4-consumer-contract-repair` is clean at exact 85cbb…; its `codex/r19-g4-consumer-contract-repair` local and live remote refs match. The original execution checkout is clean, detached at exact 2da… . No checkout was switched or altered.
- All 15 original G3 output files named by the independent review's pre-hash inventory and all four supervisor files (`launch_context.json`, `runner.log`, `runner_exit.json`, `supervisor_status.json`) matched their pinned original SHA-256 values. The complete original evidence archive remains referenced in place at SHA-256 `c7b09370e7b7625d60ad257a4a4cfe023cceb5a47f48d1f660b2ae36fd5c808f`; it was not duplicated or changed.
- Frozen machine protocol, protocol document, source schedule, exclusions, and G3 gate matched their review-bound hashes. No data traversal or model/cache access was performed.

## Future-only analyzer invocation

The exact argument vector is in `proposed_analyzer_argv.json`; the explicit environment set/unset plan and CWD are in `proposed_environment.json`. Both are proposals only and are not to be executed under this release. Future invocation uses the pinned Python and reviewed analyzer absolute paths, the original protocol and G3 evidence paths, original supervisor receipts/context, original schedule/exclusions/manifests, and `--evidence-class live`. It deliberately omits `--allow-synthetic`. Future output is uniquely planned at:

`/home/lizening/research-notes/agent-logs/2026-10-23T043602Z__LUNA__r19-g4-readiness__85cbb923/future_g4_report`

That path was absent at preparation and remains absent. No report directory or report files were created. The original execution CWD and all original input identities are preserved; the analyzer SHA is pinned separately from the executed G3 SHA.

Canonical future argv SHA-256: `69abc553c35baf28423c0e1eb51a39547e95005f058ba3a87d32e01f32c15c89`. Canonical environment-plan SHA-256: `fb67e1cd8ab5d78ba8f236322de3970f916fcde5ac1bd3654ada01215ffa0aa4`. Raw JSON hashes are recorded in `input_hashes.json`.

## Budget, sample, and stop conditions

- Existing cumulative physical cost remains **5,142 model generations / 7,949 environment operations**, with **0 incomplete external operations**; historical 177 generations / 342 operations remain included.
- This preparation added zero model generations and zero environment operations. Formal G4 is proposed as offline evidence analysis only and releases no generation/reset/action budget.
- Actual G3 cohort is 127 source episodes, 39 attempts, 36 eligible (failure 6, success-control 15, random-control 15), with 183 K-arm records. The failure queue was exhausted. No quota transfer, backfill, re-enrollment, or sample expansion is proposed.
- No K outcomes, paired statistics, best fixed K, cost-saving estimates, or scientific conclusions were computed in this task.
- If any bound input, hash, source identity, receipt, original path, or output-absence condition drifts before a future separately authorized G4, stop and report the mismatch. Preserve originals; do not repair evidence, synthesize a `run_started` event, normalize manifests, rerun G3/G2, retry, or start a model/environment process.
- Formal G4 must use the full authentic original G3 provenance bundle. Any subsequent authorization is limited to its own explicit scope; this proposal does not itself authorize execution.

## Review evidence

Sol's immutable review JSON SHA-256 is `8817b955846624936d591a104a0bcbedde1b66c9c1e1573b6eb60de7db965579`; the task specification SHA-256 is `64b9f8068a132a2ee6938f9c4288b6e70f768501560a2ba0227496f0f2326037`. Review reports five real-data production integrity validators PASS, without actual-data analyzer main/statistics/report execution. Its 246 focused tests passed; the full suite's 703 passes, 3 failures, and 77 errors exactly match the 2da baseline's 617 passes, 3 failures, and 77 errors across the same 80 failure/error IDs. These are review facts, not tests run by Luna in this preparation.

## Prepared artifacts

- `proposed_analyzer_argv.json` — exact future-only argv array.
- `proposed_environment.json` — future-only pinned CWD and environment set/unset plan.
- `input_hashes.json` — raw source, review, original evidence, protocol, schedule, and archive bindings.
- `commands.log` — read-only checks actually performed and checks explicitly not performed.
- `RECORD.md` — immutable task record and completion boundary.
- `FILE_HASHES.sha256` — finalized inventory for this task's publishable files, excluding itself.

No scientific output or report is included. After independent proposal review, await separate direct human G4 authorization and a distinct formal release; do not execute automatically on review PASS.
