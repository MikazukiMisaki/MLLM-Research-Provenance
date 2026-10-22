# Task record

- Agent/task: Codex — R19-B1 G3 entrypoint repair, real preflight-path verification, and conditional G3/G4 handoff.
- Start UTC: 2026-10-22 11:50:54 (earliest recorded repair commit; task preparation may have started earlier). Finish UTC: pending remote provenance verification; the final record commit will replace this field with the observed finish time.
- Status: **READY_FOR_REVIEW**. Safe implementation and tests are complete. Independent exact-SHA approval and a successful production CLI preflight were not obtained; therefore no G3 successor launch and no G4 analysis were performed.
- Scientific repository: `MikazukiMisaki/Alfworld-Self-Improvement-Project`.
- Branch: `codex/r19-recovery-duration-v1`. Starting SHA: `ef2328f06256054a6b71c6dc4bdc74dab3a1d3d9`. Ending SHA: `bf31f3da430ffc35bd17fc380e1752adce6d1467`.
- Changes: `42f972297c1acad70215f802d34b7effd89a244c` adds the repository-root import bootstrap, exact production-module origin checks, supervised preflight-only routing/receipts, and G4 provenance binding. `dedb958f8fca9ad03bb98e3af898b4c9e05834f6` makes the declared review scope include G4 provenance routing. `bf31f3da430ffc35bd17fc380e1752adce6d1467` makes the bad-authorization CLI integration test explicitly preflight-only and records the failed-launch linkage. No frozen scientific function, machine protocol, baseline, schedule, quota, exclusion, or horizon was intentionally changed; all 40 authorization-pinned scientific function fingerprints match exactly.

## Root cause and repair

The preserved formal runner attempt on `ef2328f06256054a6b71c6dc4bdc74dab3a1d3d9` exited with subprocess code 1 at `scripts/run_r19_recovery_duration.py::_pilot_gate_check`: `ModuleNotFoundError: No module named 'scripts.run_r19_experiment'`. When the file is invoked by absolute script path, Python puts the `scripts/` directory—not its repository parent—at `sys.path[0]`; the old bootstrap exposed `src/` but not the repository root. Supervisor `cwd` alone did not repair that import path. The prior raw receipt and its SHA-256 values remain in the earlier G3 launch record; this task did not overwrite or reinterpret them.

The repair derives and prepends the repository root from the executing file, imports the production runner from that exact checkout, and verifies module origin. The supervisor captures argv, cwd, interpreter identity, evidence class, prior-failure linkage, and an allowlisted/redacted import-relevant environment. A production preflight-only branch reuses gate, authorization, runtime-identity, and immutable-input checks, then returns before output-directory, registry, model, environment, or scientific-unit construction.

## Review and CLI gate status

- An available reviewer attempt returned **BLOCKED**, explicitly not independent approval; it said its audit could not be represented as independent review. The final SHA `bf31f3da430ffc35bd17fc380e1752adce6d1467` has no independent exact-SHA PASS artifact. Do not treat the review attempt as approval.
- A fresh-process test verifies the production runner and analyzer resolve to this checkout with `PYTHONPATH`, `PYTHONHOME`, and `VIRTUAL_ENV` removed.
- A real subprocess test launches the same supervisor and pilot CLI in `preflight_only` mode, links it to failed run `a0de515d7e104101bf8157175ea3d995`, reaches `_pilot_gate_check`, imports/loads the production authorization code, then correctly rejects a deliberately wrong repair-authorization hash. It exits 2 and creates neither preflight receipt nor scientific output. This is a negative authorization test, **not** a successful real preflight.
- The successful early-return path is covered at function level with model/runtime construction forbidden and zero-side-effect assertions. The production CLI's positive preflight cannot be truthfully certified until the exact-SHA independent-review gate is available; no approval or local gate was fabricated.
- Synthetic production scheduler coverage exercises frozen enrollment and K=1..5 paths. The analyzer CLI is verified in a fresh process to import and reach event-ledger validation, where an empty ledger is rejected without creating report output; the G4 provenance validator has a positive synthetic fixture. A complete successful synthetic CLI report-write fixture was not produced, so that specific end-to-end report-write path remains unverified.

## Tests and checks

See `tests.log` for commands and exact observed outcomes. The three R19 test files contain 75 tests and passed at the final SHA. Python compilation, `git diff --check`, and all 40 frozen scientific fingerprints passed. The full repository suite did **not** pass: the three named failures and historical-data errors are recorded in `tests.log`; they concern absent prior R12/R18 validation artifacts and a frozen R18 adapter hash mismatch, not R19 tests. No R19 test failure remained.

## Scientific boundary and expenditure

- The prior genuine G2 evidence remains bound to execution SHA `92aae1d9b230cc212c6ec4effc99aa468941e69d`; it was not rerun or relabeled.
- One prior failed G3 launch remains recorded with subprocess exit code 1. This task made no formal/live launch attempt. The new supervisor/CLI integration test is explicitly `preflight_only` and rejects invalid authorization with exit code 2; it creates no scientific output.
- New model generations: 0. New environment operations/resets: 0. New TRAIN attempts/source episodes: 0. New scientific units: 0. Training/DPO/ORPO/held-out/new-model/selector/BO/prompt-tuning/sample expansion: none.
- Cumulative physical expenditure remains 176 generations and 341 environment operations from G2. G3 is **NOT_STARTED**; G4 is **NOT_REACHED**. No results, paired statistics, best-K selection, hindsight headroom, cost-saving result, or passive-stopping result are claimed.
- Historical R18 model equivalence remains unresolved and was not revisited.

## Pushes, hashes, and next step

- Scientific branch was pushed normally. `git ls-remote` verified `refs/heads/codex/r19-recovery-duration-v1` at `bf31f3da430ffc35bd17fc380e1752adce6d1467`.
- Provenance repository started at `c257dc82921a939a3bbe63d57d7815135db1c708`. This record, sanitized review status, test outcomes, exclusion/redaction notes, and refreshed file hashes are committed and pushed to `MLLM-Research-Provenance/main`; the final remote SHA is reported in the handoff after verification.
- Raw prior failed-launch receipts are not duplicated; their local location and hashes are in the linked earlier G3 record. No raw successful or failed scientific data was generated here. Temporary synthetic gate/test fixtures and ignored machine-local gate files are excluded.
- **NEXT: obtain a genuine independent exact-SHA review of `bf31f3da430ffc35bd17fc380e1752adce6d1467`, then run the required successful same-supervisor production preflight. Only if all launch conditions pass may the single authorized G3 successor launch proceed. If reviewer remains unavailable, retain READY_FOR_REVIEW and STOP.**
