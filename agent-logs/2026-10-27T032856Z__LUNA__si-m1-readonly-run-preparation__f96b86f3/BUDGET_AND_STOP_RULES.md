# SI-M1 proposed physical budget and fail-stop ledger

This is a design-linked preparation ledger only. It is not a gate, command, authorization, runtime pass, or observed expenditure.

## Maximum physical work

| Unit | Fixed prefix replay | Reset | Teacher calls | Teacher action | Maximum reset-inclusive operations |
|---|---:|---:|---:|---:|---:|
| C088 | 11 | 1 | 2 | 1 | 13 |
| C091 | 8 | 1 | 2 | 1 | 10 |
| C093 | 16 | 1 | 2 | 1 | 18 |
| C094 | 12 | 1 | 2 | 1 | 14 |
| C095 | 8 | 1 | 2 | 1 | 10 |
| Total ceiling | 55 | 5 | 10 | 5 | 65 |

Each case uses one unique game instance and one reset with seed 42 and pool seed 42; replay its exact saved prefix action-by-action once, then run Stage 1 and Stage 2 once, execute at most one valid selected action, and end the case. Do not call replay_twice. The old A96 source continuation is reused without a new generation. No P0 suffix, CONTINUE, replacement case, additional seed, retry, second reset, or follow-up horizon is allowed.

| Resource | Proposed hard ceiling | Accounting rule |
|---|---:|---|
| Teacher generations | 10 | Count every started, completed, and incomplete generation separately; both stages per case. |
| Input tokens | 81,920 conservative | 10 calls x 8,192 max each; record actual per-call input tokens if the released runner reports them. |
| Output tokens | 280 | Five Stage 1 outputs x 40 plus five Stage 2 outputs x 16. |
| Environment constructors | 5 | One new game instance per case. |
| Resets | 5 | One per case, seed 42. |
| Replay steps | 55 | Exact fixed depths 11+8+16+12+8. |
| Teacher-selected action steps | 5 | At most one per case. |
| Reset-inclusive environment operations | 65 | Resets + completed/incomplete replay steps + executed/incomplete teacher actions, unique physical operation IDs only. |
| Allocated device time | 0.5 device-hour = 1,800 monotonic seconds | Clock starts before any wait/model load and includes wait, load, generation, audit, and cleanup. Not a wall-time prediction. |

The reviewed shared-resource contract caps the native allocator at 24 GiB, requires at least 28 GiB global free before weight loading, and at least 2 GiB at later checkpoints. It is non-exclusive shared GPU; do not interrupt or claim ownership of NVML PIDs. Its contract status is software-only and gives no launch authority. The final 4,599 MiB free snapshot fails the 28 GiB pre-weight condition.

## Physical ledger schema for a future released run

Maintain immutable raw operation rows keyed by unique physical operation ID. Record case ID, phase, operation type, request/start/completion timestamps, seed, exact action/replay index, authentic return code, raw done/reward/truncated, state/observation/map hashes, and whether the external operation is complete, failed, or uncertain. Do not count wrapper events as additional environment operations when they point to an existing physical operation ID. Keep constructor/close counts separate from reset/step counts. Record each model call separately with stage, request/start/finish, input/output token counts, completion/exception/exit, and resource accounting. Preserve raw receipts; never reconstruct absent output or success values.

Before the proposed experiment, existing accepted scientific cumulative cost is 7,101 generations and 10,004 reset-inclusive environment operations: 5,142/7,949 prior cumulative plus A96 source 1,959/2,055. The conditional full-ceiling projection is 7,111/10,069 only if no intervening science occurred. Recount authoritative ledgers immediately before any launch and after any real exit. Engineering-only run cost is separate (prior recorded adapter engineering run: 1 generation, 7 environment operations, 0.020915668825360223 allocated device-hours); do not mix this into scientific totals. The failed SI-E2 resource probe likewise remains a separate engineering expenditure.

## Typed outcome and fail-stop rules

- Check exact candidate/source/config/data/model/adapter/environment hashes and the first anchor snapshot before allowing the first operation. Any mismatch stops before the affected scientific action; no substitute or rerun.
- If the resource gate fails before load, do not load. If a later global-free checkpoint fails, stop promptly and perform bounded cleanup within the same 1,800-second budget. Do not wait while holding a GPU allocation.
- Every reset/step/generation counts once when its physical call is issued; if it is uncertain whether an external operation occurred, preserve it as incomplete/uncertain and stop. Never retry it.
- An invalid or missing action is not silently repaired. A technical or integrity failure gives Z=NA with the reason. No automatic second generation, action, reset, replay, or new run identity.
- Z_immediate=1 only when the action was actually executed and authentic raw terminal evidence has done=true and reward>0. Z_immediate=0 only after a completed action with no positive immediate terminal success; distinguish terminal-zero from nonterminal. A nonterminal endpoint has Y_T=NA_NOT_MEASURED, not “H50 failed.”
- Any nonzero exit, timeout, interruption, hash mismatch, ambiguous operation, budget breach, or cleanup uncertainty preserves original logs/registry/event records and stops. No relaunch, repair during run, G4, training, or effect-based case replacement.

No part of this document authorizes execution. Exact implementation SHA, fresh gate/context, independent exact-SHA review, zero-science preflight, and separate one-run clearance remain future requirements.
