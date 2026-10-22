# R19-B1 G2 successor result

## Outcome

The single authorized successor smoke completed with authentic subprocess exit code `0`, execution status `G2_PASS`, and offline verification `PASS_OFFLINE_VERIFICATION`. It used only the frozen R8-F16 and R8-S04 cases. No G3, fresh TRAIN collection, held-out evaluation, training, DPO/ORPO, prompt change, quota/exclusion change, or model replacement occurred. Historical R18 model equivalence remains `NOT_ESTABLISHED`.

R8-F16's production model-free replay passed before the first model generation. All four scheduled case/repeat replays passed. The frozen 50-action horizon, adapter isolation, replay checks, K1 comparison, K3 repeat integrity, common-path/handoff checks, and raw event reconciliation passed.

## Replay diagnosis and repair

The failed predecessor (`f4fb81842e949930433def5817723bab74159f14`, run `089429e4a2554bc386580d87014b4951`) had the earliest mismatch at transition 14, JSON path `$.recent_context_k4[0].action`: expected `look`, observed `action`. All 18 saved public transitions, reset state, task/seed, ordered action mapping, current observation, history, and horizon matched the frozen source; the mismatch was in controller-side assembly of the recent-context representation, not in the environment trace or frozen hash.

Root cause: `contexts` held dictionaries, but the implementation unpacked each dictionary as `(action, result)`, which iterated its keys and emitted key names as values. The minimal fix copies the final four dictionaries directly. Production-path regression used the authentic saved R8-F16 results and passed; observation, action-map order, prior history, recent-window indexing, task, seed, and horizon tampering continued to reject. The validator durably records detailed mismatches before raising.

The original failed evidence remains unchanged. Its 19 physical operations (one reset and 18 steps) are complete and certain; its enclosing replay/attempt unit remains a failed validation, not a successful completion. The reviewer-approved resolution was appended separately as `KNOWN_FAILED_REPLAY_VALIDATION / NO_BRANCH_EXECUTED`; the original `in_progress` registry bytes were not edited.

## Frozen smoke checks

| Check | R8-F16 | R8-S04 |
|---|---|---|
| Model-free public-prefix replay | PASS | PASS |
| K1 reference vs production | PASS; raw generations and parser/action mapping match | PASS; raw generations and parser/action mapping match |
| Historical OSR diagnostic | K1 outcome `0` matches historical failure; recovery command matches | K1 outcome `1` matches historical success; recovery command matches |
| Production K3 repeat | Two distinct arms; rebuilt trace signatures match; evidence sets disjoint | Two distinct arms; rebuilt trace signatures match; evidence sets disjoint |
| Original horizon and SFT handoff coverage | PASS | PASS |

K1 is diagnostic/reference comparison, while the G2 acceptance decision is based on the frozen smoke checks; historical OSR agreement is not used as a pass predicate. K3 success was `1` on both R8-F16 repeats and `0` on both R8-S04 repeats; these bounded smoke outcomes are not a fresh-task or held-out estimate.

## Cost reconciliation

All environment operations include resets. The predecessor used 19 operations, 0 generations, and 0 branch executions. The successor used 312 environment actions plus 10 resets (322 operations), 176 physical model generations, and 6 branch executions. Thus cumulative use is 341/400 environment operations, 176/408 generations, and 6/8 branches. Remaining ceilings are 59 operations, 232 generations, and 2 branch executions; the one authorized retry has been consumed. There were no unplanned retries and no branch reruns outside the frozen repeat schedule. The run stopped after G2; remaining capacity does not authorize further work.

## Evidence and review

- Exact source review: PASS on successor `92aae1d9b230cc212c6ec4effc99aa468941e69d`; reviewer Popper.
- Independent successor gate/campaign reconciliation: PASS; no discrepancies; gate SHA-256 `2e7beb89c0ade2adf3886e551b733b37f4edb55ceac68bfa2d076babd05de612`.
- Successor run ID: `33b5563d86d6491a821db224dd38ec3c`.
- Raw event ledger SHA-256: `1456c43f7d3f0a849fe4bb8015164815fd70f4e2813d343449c1a34c2eaebe0c`.
- Branch results SHA-256: `c91f9ff8ab5869bfcdcddd850e038b84c84ad317a7098928a4a09129652e96d3`.
- Offline verification: exit code `0`; event ledger, branches, runtime/baseline hashes, all 14 scientific unit receipts, smoke predicates, and supervisor receipt reconciled.

The complete unmodified successor event ledger, branch rows, execution/runtime/environment manifests, smoke report, unit registry, and offline verification are included under `g2_evidence/`. Raw supervisor files containing machine-local command paths and process identifiers are retained locally and excluded from upload; `supervisor_receipt_sanitized.json` and `EXCLUDED_FILES.md` provide the hash-linked redaction record. `FILE_HASHES.sha256` inventories uploaded evidence files.

No work is authorized beyond this G2 result.
