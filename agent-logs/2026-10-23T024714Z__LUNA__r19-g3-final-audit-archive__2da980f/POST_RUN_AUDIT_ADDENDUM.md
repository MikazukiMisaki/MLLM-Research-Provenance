# R19-B1 G3 post-run audit addendum

This addendum supplements the Luna execution record at `agent-logs/2026-10-23T002200Z__LUNA__r19-g3-live-successor__2da980f/`. It does not replace or rewrite the earlier record, raw evidence, scientific output, or Sol's immutable audit files.

## Run and physical-cost correction

The sole authorized run `260422ac02bd42a8b2929d7ef240526b` completed naturally with authentic child exit code 0 and supervisor status `completed`. Sol's independent final audit confirms 127 completed source episodes, 39 attempts, 36 eligible states (6 failure / 15 success-control / 15 random-control), 39 branch rows, 183 arms, all frozen caps respected, all protected old bytes unchanged, and source SHA `2da980f631badc25086d12db60d128ff507d3ae6` unchanged.

The authoritative production physical recount is 4,965 generations and 7,607 environment operations (7,273 non-reset operations + 334 resets), with zero incomplete operations. Including the prior 177 generations / 342 environment operations, cumulative cost is 5,142 generations and 7,949 environment operations (7,603 non-reset + 346 resets). Sol verified that 169 `environment_step_completed` wrapper events each link to an already counted `environment_operation_completed` transition. The earlier live-monitor display of 8,118 cumulative environment operations double-counted those wrappers and is superseded by the validated 7,949 total; raw science files were not altered.

## G4 consumer blockers; no G4 execution

Two future G4 production-consumer contract gaps are confirmed by Sol's read-only audit:

1. `validate_live_execution_provenance` expects flat v1 runtime fields, but the genuine unchanged runtime manifest is frozen v2 with nested local-only inference fields. The v2 runtime matches the frozen preload and is not G3 drift.
2. `validate_live_exit_receipt` rejects the authentic event ledger because it has no `run_started` envelope; the actual producer writes run context on the first real operation. This validator failure does not invalidate the authentic successful runner exit.

These are classified `BLOCKED_BY_CONFIRMED_SCHEMA_AND_EMITTER_ENVELOPE_CONTRACTS` for future G4 acceptance. No G4 main/report/statistics command was run. Neither the runtime manifest nor event ledger was flattened, edited, or augmented, and no final manifest fields were fabricated. The successful child exit remains authentic; it is not labeled as a runner failure.

Sol-owned immutable audit sources (not copied or staged as Luna-owned files):

- `agent-logs/2026-10-23T005510Z__SOL__r19-authorized-g3-monitor__2da980f_eea6b8/final_g3_integrity_audit.json` — SHA-256 `242225209e397674c19b6f88463f7881d2fe151c8570636ccdaa5a28a031ad62`.
- `.../monitor_display_cost_correction.json` — SHA-256 `d41383c3519df79292d9d5fa2607cb0f2b946e6f463a7fa93931e22e6c885f24`.
- `.../g4_runtime_schema_contract_finding.json` — SHA-256 `c8ebd8ec1229a231fa8a88b019abbd5d660bd1c8790896580f639283f0c497ba`.

## Raw evidence archive

The two raw payload files omitted from the initial publication are now preserved byte-for-byte in deterministic gzip streams under `raw/`. Their uncompressed SHA-256 values were verified by streaming decompression against the original local files. Sizes, source paths, original hashes, archive hashes, and exact decompression verification are in `raw_payload_manifest.json`. The earlier publication already includes the authentic runner/supervisor receipts and logs, execution manifest, branches, registry, runtime and gate manifests, and restart comparison. No model weights, adapter, cache, or dataset files are included.

This is a provenance-only addition. No experiment, model, environment, preflight, G2, G3, or G4 invocation occurred during this archival task.
