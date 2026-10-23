# R19-G4-C01-C02 — test-only fingerprint contract ruling

Decision: APPROVED_TEST_ONLY_CONTRACT_ADAPTATION. This supplements the existing user-authorized two-consumer repair; it does not expand production scope or grant independent acceptance, Luna preparation or formal G4 permission.

## Independent cause verification

The coordinator read the actual draft traceback and hashed source spans independently, without importing candidate production code or executing a validator/model/environment. All40 frozen authorization-plus-amendment method fingerprints equal `git show 2da980f631badc25086d12db60d128ff507d3ae6:<source>` spans. Only the currently authorized C02 method differs from that historical list: `scripts/analyze_r19_recovery_duration.py::validate_live_exit_receipt`, historical SHA256 `87b95e896e62c77183e78c517edc23f5ecfd88d9dade2135f0804e3cedf9929b`. Frozen authorization/amendment bytes are unchanged. The independent proof and draft log snapshot are saved alongside.

## Exact test-only scope

Adapt `tests/test_r19_g3_authorization.py::test_source_contract_amendment_fingerprints_exactly_current_methods` and narrowly necessary test-only AST/Git-source helpers, or split its assertions into explicitly named historical/live-code checks while preserving regression accounting. No new production changes are authorized by this ruling.

Required checks:

1. Authenticate unchanged historical authorization/amendment records against their exact2da Git objects and existing frozen hashes. Resolve every one of the40 expected historical function-source hashes from that exact Git object using the same source-span hashing semantics; assert exact equality, complete key set and9 amendment entries. Do not just assert a prefix, an arbitrary current HEAD, a local mutable copy or a self-generated expected manifest. Missing exact Git object is a test failure with a clear cause, never a skip or silent fallback.
2. Preserve current-checkout fingerprint equality for **all39 unchanged entries**, including every runtime producer, parser/scheduler/recovery/SFT/statistics/report function and unchanged evidence validators already covered by the list. Exclude exactly the authorized `validate_live_exit_receipt` key from this CURRENT-versus-HISTORICAL equality; do not exclude all analyzer methods/files or relax any other fingerprint. Current G3 execution-gate code stays byte-unchanged and continues using its historical contract; it must not be taught to authorize a new G3.
3. Separately constrain the current production analyzer delta from2da. Existing top-level methods that may differ are exactly `validate_live_execution_provenance` (C01 call-site) and `validate_live_exit_receipt` (C02), with only helpers `_validate_local_inference_runtime`, `_supervisor_option`, `_read_supervisor_object`, `_validate_supervisor_launch_context` added for these contracts. Check no other existing function/class or module constants/control-flow/import behavior is silently changed; an AST structural comparison can ignore only those explicitly authorized definition slots. If a further helper or module change is genuinely required, disclose it for review instead of using an unbounded allowlist. This structural allowance is not a semantic PASS: actual new method/helper hashes and complete diff still require independent exact-SHA review.
4. Do not edit any historical fingerprint JSON, amendments, authorization/disposition, gate or original G3/review/evidence byte to match the new analyzer. Do not refresh production fingerprint constants, auto-compute expected candidate values from the same candidate input, delete coverage, skip/xfail the regression, or treat the new failure ID as accepted. The no-new-failure/error-ID criterion remains.

## Testing-boundary clarification

Retain original genuine G3 SHA2da and separately report candidate analyzer SHA. The developer's report that allfive actual production integrity validators returned with originals unchanged is a handoff claim, not independent acceptance; save all raw returns/module origins/pre-post hashes for later reproduction by Sol. No actual-data analysis/report/main/statistics is permitted.

A nonempty explicit-synthetic production CLI report test **plus** separately marked synthetic wire-format fixtures directly exercising the fixed consumer contracts is acceptable in combination with the genuine complete actual-data validator-only integration. Be explicit about the coverage: synthetic CLI runs its synthetic branch and does not itself prove the live CLI provenance branch; the genuine validators prove actual consumer acceptance; the formal live CLI/report end-to-end remains unexecuted pending user authorization. No fake live run/report or statistics on actual data to fill that gap. Do not claim a synthetic CLI test reached live-only validators when it did not.

The required existing negative regression fixtures may launch isolated temporary subprocesses that reject invalid supervisor/preflight arguments/authorization before any model/ALFWorld construction or generation/reset/step. These are bounded software rejection tests, not new official preflight/scientific invocations. Do not run the real gate/runner against execution checkout or original output/record paths. Save true test receipts and zero scientific counters when applicable. The dirty-worktree gate failure must be rerun on a clean committed candidate and genuinely resolve; do not bypass the clean-worktree guard.

## Handoff and authorization

Complete authorized tests; retain draft failures/this ruling as history. Return clean exactSHA/local+remote equality, full delta, method hashes, focused/full raw test results and failure/error-ID comparison. Current production scope remains only C01/C02. Independent review=PENDING_FROZEN_SHA; Luna preparation=NOT_RELEASED; formalG4=NOT_AUTHORIZED; no G3/G2 retry or model/ALFWorld run. Additional concrete blocker means report and stop scope expansion, not repair by inference.
