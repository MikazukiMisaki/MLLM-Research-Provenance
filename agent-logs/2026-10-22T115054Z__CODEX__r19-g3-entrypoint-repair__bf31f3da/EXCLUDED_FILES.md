# Excluded files and evidence

- Prior failed G3 `runner.log`, `runner_exit.json`, and `supervisor_status.json`: not duplicated. They remain preserved in the prior local task record at `agent-logs/2026-10-22T105439Z__CODEX__r19-b1-g3-launch__ef2328f/supervisor_raw/`; their SHA-256 values are recorded in that task's `RECORD.md` and the frozen repair-authorization document. They are historical failure evidence, not newly generated output.
- Prior reviewer raw material: not duplicated; the earlier task's raw review folder is left untouched. The current review attempt did not produce an authenticated exact-SHA PASS artifact; `review_sanitized.md` is explicitly only a status summary.
- Current synthetic gate fixtures, launch-context test receipts, and analyzer inputs: ephemeral pytest temporary files; not scientific observations and not retained as G3 evidence.
- Machine-local `configs/local/r19_b1_g3_gate.json`: not uploaded or modified; it remains stale relative to the repair commits and cannot authorize launch.
- No model weights, adapters, datasets, environment outputs, credentials, tokens, keys, cookies, or `.env` files were copied into this task directory.
