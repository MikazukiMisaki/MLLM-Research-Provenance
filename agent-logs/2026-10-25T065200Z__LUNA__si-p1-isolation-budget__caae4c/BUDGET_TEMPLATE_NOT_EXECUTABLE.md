# Future Budget Ledger Template — NOT EXECUTABLE / NOT AN AUTHORIZATION

Do not fill unknowns with zero. Record physical calls once across the shared campaign and logical per-policy costs separately.

| Cost category | Shared physical ledger | Logical per-policy ledger | Evidence / status |
|---|---:|---:|---|
| Source acquisition | UNKNOWN until measured | Attribute source rows to each arm | distinguish reuse from new reset/generation/action |
| Stage 1 | UNKNOWN | per method and task | record calls, tokens, latency |
| Stage 2 | UNKNOWN | per method and task | record calls, tokens, latency |
| CONTINUE | UNKNOWN | per method and task | record calls, tokens, latency |
| Recovery | UNKNOWN | per method and task | include diagnosis and action calls separately |
| Suffix | UNKNOWN | per method and task | include generation and action calls |
| Reset | UNKNOWN | per arm/episode | every reset is physical environment cost |
| Prefix replay | UNKNOWN | logical replay per arm | shared physical replay counted once only if actually reused |
| Failed / incomplete | UNKNOWN | attribute to originating unit | never erase uncertain operations |
| Validation | UNKNOWN | per artifact/arm | no free validators or smoke calls |
| Training | UNKNOWN | per run/arm | steps, examples/tokens, GPU seconds, peak resources |
| Offline validation | UNKNOWN | per candidate | report dataset/query cost; no environment assumed free |
| Evaluation | UNKNOWN | per policy | include environment and model calls |

For E task episodes, 3 arms, 50-action horizon: action generation bound `150E + C`; environment bound `153E + R_extra`, only under one generation/action step, one reset/episode, no extra controller/replay/probe/validation calls. Report C and R_extra, or leave unknown. This template selects no E and grants no budget.
