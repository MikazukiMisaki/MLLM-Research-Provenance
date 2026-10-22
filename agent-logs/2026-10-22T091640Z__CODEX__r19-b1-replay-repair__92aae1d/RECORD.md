# Task record

- Agent/task: Codex — R19-B1 G2 replay recovery and one conditionally authorized successor smoke.
- Start: 2026-10-22 09:16:40 UTC. Scientific work completed: 2026-10-22 09:38 UTC; provenance synchronization follows.
- Status: G2_PASS; offline verification PASS; sanitized provenance synchronization pending.
- Scientific repository: `MikazukiMisaki/Alfworld-Self-Improvement-Project`.
- Scientific branch: `codex/r19-recovery-duration-v1`; initial failure SHA `f4fb81842e949930433def5817723bab74159f14`; ending/reviewed/executed SHA `92aae1d9b230cc212c6ec4effc99aa468941e69d`; local and remote branch matched at inspection.
- Scientific changes in the successor commit: `scripts/run_r19_experiment.py` and `tests/test_r19_recovery_duration.py`; no scientific code/test changes after exact-SHA review.
- Frozen baseline/protocol: R19-B1 unchanged; historical model equivalence remains `NOT_ESTABLISHED`.
- Predecessor run: `089429e4a2554bc386580d87014b4951`, exit 2, 19 completed operations, 0 model generations, 0 branches. Its event ledger, manifests, supervisor evidence, and original `in_progress` registry were preserved.
- Append-only resolution: `b78e7bf3cfd100e2bd6866908e95ee7b7b43d201ac7c3d0edc96dc6bfc8a47eb`, `KNOWN_FAILED_REPLAY_VALIDATION / NO_BRANCH_EXECUTED`; original registry SHA remained unchanged.
- Successor run: `33b5563d86d6491a821db224dd38ec3c`; authentic exit code 0; `G2_PASS`; offline verification `PASS_OFFLINE_VERIFICATION`.
- Cases: R8-F16 and R8-S04 only; four scheduled case/repeat replays passed. R8-F16 replay passed before any generation. K1 reference/production comparison passed on both cases; K3 repeated-arm evidence and original horizon/handoff checks passed.
- Tests: focused R19 suite 47 passed; compilation and diff checks passed. Saved-data production validator regression passed with negative mutation cases. Gate preflight and completed-run offline verification passed.
- Physical costs: predecessor 19 operations / 0 generations / 0 branches; successor 312 environment actions + 10 resets = 322 operations / 176 generations / 6 branches; cumulative 341/400 operations, 176/408 generations, 6/8 branches. Held-out/fresh tasks/training/external paid calls: 0.
- Execution boundary: exactly one planned successor retry; no unplanned retry or branch rerun; no G3, fresh TRAIN, held-out evaluation, training, DPO/ORPO, model replacement, prompt change, quota/exclusion change, or additional case.
- Provenance repository checkpoint before this task's upload: `2d12f3f505984b84285d20cad57b3125244c6ac0`. The final containing Git commit is resolved by the pushed history and reported to the user; a record cannot include its own final commit SHA.

Exact command summaries and the raw-to-sanitized supervisor mapping are in `commands.log` and `EXCLUDED_FILES.md`. Review and result artifacts: `G2_SUCCESSOR_REPORT.md`, `REPLAY_DIAGNOSIS.md`, `replay_diff.json`, `production_validator_regression.json`, `unit_resolution_events.jsonl`, `review-92aae1d.md`, `successor_gate_review.md`, and `g2_evidence/`.
