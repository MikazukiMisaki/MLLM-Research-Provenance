# Independent audit: five-action public synthetic environment check

**Decision: documented engineering run PASS, with provenance and observation limits.** The retained ledger and supervisor receipt support completion of one exposed-development PddlEnv run: one construction, one load, one reset and five recorded fixed action calls, ending with the synthetic goal satisfied. This is not a model or agent evaluation, a measure of self-improvement, held-out evidence, a statistical success rate, or proof of general task solvability. No environment, model, GPU operation, inference or replay was run during this audit.

## Independent ledger checks

`audit_run.py` independently parses and verifies the 24 contiguous sequence numbers and exact event order: unit start; construction, load, reset STARTED/RETURNED; initial observation; five complete STARTED/RETURNED/OBSERVED triplets; unit_complete. The frozen `probe_id` matches the receipt. For each step the script verifies command and index, pre-observation continuity with the previous post-state, command in logged admissible commands, exact predicted versus actual action identity, complete typed parameter mapping, and expected post-fact. The first four report done=false, won=false, score 0. The fifth reports done=true, won=true, score 1 and the fact `inreceptacle(item,destination)`; the final unit record agrees.

| Step | Documented action | Grounded action ID | Check |
|---|---|---:|---|
| 1 | open source | 12 | source opened |
| 2 | take item from source | 14 | agent holds item |
| 3 | go to destination | 6 | agent at destination |
| 4 | open destination | 11 | destination opened |
| 5 | move item to destination | 15 | item in destination |

Full pre/post action names and typed mappings are retained in the original ledger and independently reproduced in `AUDIT_RAW.json`. All mappings and IDs match per step. The ledger does not include the full raw `_valid_commands` / `_valid_actions` arrays; uniqueness of the raw match is an assertion executed by the inspected worker, not something independently reconstructible from the ledger alone. Facts and action identities are journaled by that same worker; no independent semantic replay or external attestation was performed.

## Receipt, costs and bindings

The retained supervisor receipt states PIDFD_BOUND, GO sent, direct child reaped, return code 0, no stop reason and no retry. It records wall 1.3218228417 s, user CPU 1.469614 s, system CPU 0.092106 s and max RSS 67,972 KiB. The distinct earlier load/reset probe was additional cost: one construction/load/reset, zero explicitly requested steps, 1.2220247081 s wall and max RSS 68,044 KiB. The earlier zero-step count was a constant report, not an independent counter. The two max RSS values are peaks, not additive total memory; unobserved work and physical tails are UNKNOWN.

The current package inventory has 14/14 matching entries and current execution-input inventory has 16/16 matching entries. Input-manifest SHA256 is `ab2202e7c1466e747751ccaebaed9cc6c3e19c77a232c0c9df960a553997c285`, and proposed command SHA256 is `3e9d26558fc68e3b372dcf94bd3c25d8c374ebfab5b7d59b1bf599943c8007ff`. These are rechecks of current bytes and do not independently prove which exact outer command was executed or that there were no transient changes at launch. The original 14-file package inventory predates the four new run output files, so this audit hashes the current files rather than asserting a preexisting immutable seal.

- Event ledger SHA256: `c52643006f5b5a3a3cc2dd8564c7761e2177552b3997cdf49ab1537b2ad96392`.
- Supervisor receipt SHA256: `2171dfc3c664401b0054a3416c9d69fe89e0e47b68ef9f63e3e7cafb32984486`.
- stdout and stderr are both empty (SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).

All four run-file hashes were unchanged between the beginning and end of this audit. The JSON receipt is a local unsigned supervisor record; it is not cryptographic process attestation. The exclusive run directory and no-retry receipt document this retained run, but cannot alone establish that no other copy or separate unlogged execution ever happened. The launcher reports no explicit model calls, and the execution was designed for zero requested model/GPU work, but this audit did not independently trace all native or system calls.

## Limits and preservation

Direct child exit was recorded; the receipt explicitly leaves unobserved descendants and GPU cleanup UNKNOWN. Per-process resource limits do not prove aggregate resource bounds. Directory fsync and complete crash-durable preservation are not established. The environment code and worker can generate additional internal PDDL/native operations; the five count refers to documented explicit `env.step` calls, not all lower-level activity.

`AUDIT_RAW.json`, `audit_run.py` and the read-only audit subprocess receipt preserve the independent checks. Original run files were not changed. The exposed development task was already seen by the project; this result cannot be used as an independent test-set observation or as evidence that a policy learned. Any further live/model evaluation requires its own reviewed plan, budget and task-isolation evidence.
