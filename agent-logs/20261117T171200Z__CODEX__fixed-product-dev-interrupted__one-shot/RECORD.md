# Fixed-product four-pair DEV run — interrupted

The supervised batch began once and exited 1. There was no automatic retry. The planned four-pair evaluation did not complete; the partial findings below are descriptive DEV observations, not an estimate of independent generalization.

| Planned case | P0 | Candidate | Status |
|---|---|---|---|
| eval-two-pair-a | failed (50 steps) | failed (50 steps) | complete pair |
| eval-two-pair-b | success (9 steps) | success (11 steps) | complete pair |
| eval-two-pair-c | failed (50 steps) | UNKNOWN; interrupted after 28 recorded steps | incomplete pair |
| eval-two-pair-d | not run | not run | not run |

The two completed pairs both agree across arms: one failure and one success each. They do not demonstrate a candidate advantage. Four tasks were pre-used and related. The observed public initial state matched between arms in the two complete pairs; public equality is not proof of identical hidden state.

Supervisor stderr reports `RuntimeError: stop or deadline before budget ACK`. The available error does not distinguish stop signal from deadline. The last owner record reserves a 29th step in case c candidate, but has no returned receipt; conservatively its effect is UNKNOWN. The worker recorded 28 started and returned steps. No completed outcome or cleanup receipts exist for this candidate arm; supervisor final descendant cleanup says no remaining children. Do not silently interpret the incomplete outcome as failure or success, and do not resume this batch.

The owner journals record six model loads, resets, environment constructions/initializations, and task materializations returned; 199 generations returned, 198 environment steps returned and one step reservation without return. Generation receipts contain 61,223 input token IDs and 995 output token IDs, including EOS when present. See INDEPENDENT_COST_RECOUNT.json for per-arm counts, raw file hashes and the uncertainty. These counts are additional to the separate earlier goal-wording attempt; they are not combined with other historical budgets.

Configuration SHA256 258cde04c4965fc82c46c4b336f09389bcbdb0ede86c78bb19045dc03b4cbde4; manifest SHA256 0fac7820b919392f0be5f5ca50f27847147312dbc07457d3d68b7861cbb35cc6. Runtime source HEAD 9dd630af4218ac44332edc7e4fb9affe0f90097b; source/config/task bindings and CPU-only tests received limited independent review before launch. Original owner/worker journals, per-arm configurations and stderr remain unchanged under live-output; launch stderr/stdout and immutable preparation files are beside this report. This record states the observed subprocess return value and does not invent a supervisor receipt.
