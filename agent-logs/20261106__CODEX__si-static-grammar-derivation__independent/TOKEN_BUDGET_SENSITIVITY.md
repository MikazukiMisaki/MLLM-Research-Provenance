# Conditional inference-token budget sensitivity

These are arithmetic illustrations, not a frozen experiment budget. The present 4,096-input and 64-output token limits are proposed for a single engineering probe; they are not established future episode or training limits. If a later reviewed study explicitly enforced these same per-generation limits on every acquisition and evaluation call, the earlier illustrative generation ceilings would imply:

| Conditional scope | Generation ceiling | Input-token ceiling | Output-token ceiling |
| --- | ---: | ---: | ---: |
| 20-task three-arm feasibility plus illustrative acquisition | 5,000 | 20,480,000 | 320,000 |
| 877-task three-arm comparison plus illustrative acquisition | 133,550 | 547,020,800 | 8,547,200 |
| 3,506-task three-arm comparison plus illustrative acquisition | 527,900 | 2,162,278,400 | 33,785,600 |

All numbers assume the specified caps actually hold and that every planned generation is counted; a different limit, hidden call, open failure, or data-acquisition strategy changes the budget. They exclude training tokens, optimizer updates, task creation/verification, model/adapter load, failed or unknown operation tails, CPU, GPU time, memory and storage. They are ceilings on token counts under a hypothetical protocol, not estimates of actual use, cost, sample-size power or authorization to spend.

The saved own-task initial feedback required 189 list-mode tokenizer input IDs in one observed CPU check, but that one state is neither a worst-case prompt nor an independent evaluation sample, and identity with the future model tensor is not established. Do not multiply 189 by the number of calls and present it as a measured study cost. Allocate and monitor input, output, training and hidden/unknown categories separately in the eventual plan.
