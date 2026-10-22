# R19-B1 physical budget ledger — Phase0 draft

> **NOT_APPROVED / NOT_EXECUTABLE.** Read-only reconciliation and planning only. The values below do not authorize any operation.

## Cumulative physical start

Sol's pinned production-validator recount covers the failed G2 replay predecessor, successful G2 smoke, and failed G3 successor:

| Category | Cumulative used at Phase0 | Evidence interpretation |
|---|---:|---|
| Completed physical model generations | 177 | G2 successful 176 + failed G3 1; failed G2 predecessor 0 |
| Non-reset environment operations | 330 | 18 failed-G2 predecessor + 312 successful G2 + 0 failed G3 |
| Resets | 12 | 1 failed-G2 predecessor + 10 successful G2 + 1 failed G3 |
| Environment operations including resets | 342 | `330 + 12` |
| Incomplete external operations | 0 | No pending start/completion pair in the three pinned ledgers |

The failed G3 source call consumed one generation and one reset; it did not complete a source episode. A later authorized index-zero replay/comparison must charge its own reset and generation again. Do not relabel either physical call as free replay or as recovered prior work. Logical per-policy costs are distinct from physical expenditure and cannot be used to substitute for this ledger.

## Frozen campaign ceilings and remaining headroom

| Phase / cap | Original generation cap | Already charged to phase | Remaining generation cap | Original environment-operation cap (resets included) | Already charged to phase | Remaining environment cap |
|---|---:|---:|---:|---:|---:|---:|
| Source collection | 9,000 | 1 | 8,999 | 9,000 | 1 | 8,999 |
| Replay gate | 0 | 0 | 0 | 5,400 | 0 | 5,400 |
| Initial recovery attempts | 240 | 0 | 240 | 5,520 | 0 | 5,520 |
| Common path extension | 240 | 0 | 240 | 2,940 | 0 | 2,940 |
| Logical recovery branches | 17,100 | 0 | 17,100 | 18,000 | 0 | 18,000 |
| **Phase total remaining** | — | — | **26,579** | — | — | **40,859** |

Global ceilings remain 26,988 physical generations and 41,260 environment operations. With 177 / 342 already charged and all remaining phase caps hypothetically exhausted, projected totals are **26,756 generations / 41,201 environment operations**. This stays 232 generations and 59 operations below the global ceilings. It does not authorize using all headroom; stop at the earliest phase or global cap. No quota or budget transfer is permitted.

Frozen design remains 127 TRAIN identities; max 120 initial attempts; max 60 eligible (failure 30, success control 15, random control 15); no quota transfer; K=1..5; horizon 50. G2's 176 generations / 341 environment operations are part of the cumulative 177 / 342, not reset by a new output directory.

## Reconciliation sources

- Sol raw-validator audit: `../2026-10-22T230825Z__SOL__r19-independent-audit-task-handoff__599954/evidence/state_and_cost_audit.json`, SHA256 `b666f5d2d69171a0305c6657f952d70f5ab304295c13b171fc77690a9cb05dab`.
- G2 source journals: failed replay predecessor `b2d9045514bc3251ee3e954e4787569566cf7ba995821adbdb5af6b1dfdf065c`; successful G2 `1456c43f7d3f0a849fe4bb8015164815fd70f4e2813d343449c1a34c2eaebe0c`.
- G3 failed successor event journal: `fde95fcd72f1c4ac6409fab7f2112654e145f6184fefec690cae58ad345f1cd7`.

These are physical counters only. Do not derive K-arm logical cost by multiplying physical generations, and do not report policy savings or recovery outcomes without authentic completed G3 evidence.
