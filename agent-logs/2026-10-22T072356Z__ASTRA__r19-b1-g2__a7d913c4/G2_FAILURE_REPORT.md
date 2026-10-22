# R19-B1 G2 smoke — failure report

## Decision

**G2_FAIL before branch-arm execution.** The reviewed runner verified the R19-B1 bundle and loaded the pinned recovery/actor backends, then failed the mandatory deterministic replay of R8-F16 against its frozen public prefix. The runner raised `EvidenceIntegrityError: old-development smoke replay differs from its frozen public prefix` and exited with authentic subprocess exit code `2`.

This is a hard replay-condition failure, not a successful or incomplete G2 pass. No post-result standard change was made. The bounded smoke was not retried, and no replacement task was used.

## Scope and exact target

- Reviewed implementation: `f4fb81842e949930433def5817723bab74159f14` on `codex/r19-recovery-duration-v1`; remote branch SHA was verified equal.
- Baseline: `R19-B1`, Qwen3-8B / `b968826d9c46dd6066d109eabc6255188de91218`.
- Effective machine protocol SHA-256: `3d7d1865c807d12276a8109b06c55da4e9182df0ca05a0b5463f8128dd03e122`.
- Baseline manifest SHA-256: `d503f35ae913b137dfff091263bf29c38aa0ade2eea648dc45d7e6cf80da0973`.
- Amendment SHA-256: `f8a138045cde125f2c5e08a7d077f75e3838cc7f6d0c67703faffe1166099e49`.
- Historical model equivalence: **NOT ESTABLISHED**.
- Independent exact-SHA implementation review: PASS for `f4fb81842e949930433def5817723bab74159f14`; this is not a G2 PASS.

## What ran

The one durable-supervisor command started the exact two-case smoke. Its prelaunch checks confirmed the pinned model and tokenizer snapshot, 11-file SFT-P0 adapter, approved runtime/environment, frozen protocol, task files, and exact review gate. The resulting execution manifest records the two-model isolation checks as passing: both base revisions equal the pin, recovery adapter inactive, actor's `default` adapter active, distinct model objects, no shared KV cache, BF16/SDPA on `cuda:0`.

ALFWorld initialized the TRAIN pool and replayed the already-consumed development prefix R8-F16. The frozen replay-state comparison failed before any recovery generation. R8-S04 was not attempted. No K1 reference, production K1 arm, or K3 arm was executed.

## Authenticated expenditure and coverage

- Raw event ledger: 38 events, comprising 19 environment-operation starts and 19 completions.
- Physical model generations: **0**; generated/input tokens: **0**; external paid calls: **0**.
- Physical environment steps: **18**; resets: **1**; total charged physical operations including reset: **19**.
- Observed task identity: R8-F16 only (already-consumed development case).
- Production branch arms completed: **0** of the planned 6; reference K1: 0; production K1: 0; K3 repeats: 0.
- Logical per-policy cost: not applicable; no branch arm was completed.
- Registry: one `prefix_replay_and_initial_recovery_attempt` remains `in_progress` because the replay raised before its completion receipt. Treat this as **one incomplete/indeterminate unit**; it is preserved as-is and must not be regenerated.
- Fresh TRAIN tasks: 0; held-out tasks: 0; training runs: 0; G3: not authorized and not run.
- Unplanned retries: 0; completed-unit reruns: 0.

The ALFWorld startup message “Training with 3553 games” describes initialization of the TRAIN split pool; no model-training operation occurred. The authenticated event ledger records zero training-run events.

## Verification and durable receipts

The offline event-ledger validator completed with no incomplete environment operations and reported 0 model generations, 18 environment steps, and 1 reset. The full G2 offline verifier correctly refused this incomplete run because `smoke_checks.json` was never produced; process exit code `2`, message: `offline G2 bundle is missing required files: smoke_checks.json`. No `offline_verification.json` PASS artifact exists.

The durable supervisor recorded run ID `089429e4a2554bc386580d87014b4951`, status `failed`, exit code `2` from `subprocess.returncode`, and `interrupted_by_supervisor=false`. Receipt details and artifact hashes are in `supervisor_receipt_summary.json`; the original receipts containing absolute local command paths remain preserved locally and are not uploaded verbatim.

Relevant original artifact SHA-256 values:

- `execution_events.jsonl`: `b2d9045514bc3251ee3e954e4787569566cf7ba995821adbdb5af6b1dfdf065c`
- `branches.jsonl` (empty): `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `execution_manifest.json` (status remains `RUNNING` because the exception preceded finalization): `83ef899e4b241052b1fa03470f1c942f8b9ba8489afdd5d8ce24ac83e760977e`
- `runtime_manifest.json`: `306a9e7c2d1b968e2a56e258fcd07aaf7467739460802a2b94c5e20411264916`
- `runtime_manifest_preload.json`: `6395e65abf266ba5f6a0834023b1da5c3799550b124a75db4d819cf613ee3312`
- `environment_manifest.json`: `81ea3b3aea86a850c70d88846f1ce12dfb276cca34aacb9f598ea13e733bf902`
- `unit_registry.json`: `bada5f681a8d113182a570b6d4b4c33a453ab10c0766e4c5e3fd37a3ae402922`
- durable runner log: `0ca35166eac10c1a359b5f9e4b2610be884ebd0bc32f534674b1e8753a2feb3d`
- original `runner_exit.json`: `96e8a0e3507c3d32880bfa1c281dc29238fc306aa5b84198499da2fc5c37831d`
- original `supervisor_status.json`: `3a9098e47a5e16e4381f77e5256a5878c4f639b21a5eec6d136934ad1afb19c2`

The retained history is not modified. The recovery implementation or smoke inputs were not changed after observing the replay mismatch. This task stops at G2 failure; any diagnosis/fix and any further execution require a separate user decision.
