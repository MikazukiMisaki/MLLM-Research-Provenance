# SI-P2 cost and limit ledger — not executable

This file records already-audited costs and missing quantities; it is not a
budget request, schedule, or authorization.

| Quantity | Bound evidence / value | Interpretation |
|---|---:|---|
| R19 cumulative model generations | 5,142 | Includes the earlier 177-generation predecessor; do not add it again. |
| R19 cumulative environment operations | 7,949 | Includes resets (7,603 non-reset + 346 resets); predecessor 342 is already included. |
| R19 incomplete external operations | 0 | Preserved prior production-validator result. |
| Historical SFT optimizer steps | 2,354 | Separate from R19 physical costs. |
| Historical SFT wall time | 27,406.28269892931 seconds | Wall time is not GPU-device time. |
| Historical input_tokens_seen | 23,860,000 | Retain source metric name; padding semantics unknown; completion targets not merged. |
| Historical GPU-device seconds | UNKNOWN | Not proved by wall time. |
| Historical prospective SFT target tokens | UNKNOWN | Inference generation tokens are not a training-token count. |
| Independent historical data-acquisition cost | UNKNOWN | Must not be encoded as zero. |
| Clean, independently sourced eligible examples | UNKNOWN / NOT ESTABLISHED | The 171 candidates are all in the known-use union. |

The already frozen *hypothetical* minimal three-arm evaluation formula is
`150E` generations and `153E` reset-inclusive environment operations for
horizon 50 with A/B_pool/C_student and no extra controller probe/replay.
`E` was not selected. This formula is not a future budget, launch command,
authorization, or permission to run anything; any additional operations
require a separately frozen and authorized budget. No costs were incurred by
this SI-P2 read-only audit beyond local CPU/file reading; no new model or
environment operation was made.
