# Two interrupted DEV incidents: combined event-ledger costs

Scope: only the isolated goal-wording incident and the fixed-product per-arm-v2 incident documented in provenance commits `62f346b03e3b23ad96ae59ca54f509dd029036b0` and `4f51184444a86bffecd856e0689a9d7bbf8cfd0a`, with subsequent corrections `b6478626ecfe21925190852a7807819613c38417` and `b72eed01ca5369f11894f8101d476161216a9b0d`. This is not the project lifetime budget, the original G3/R19 cost, or a budget for another run. The owner returns explicitly are child-claim receipts, not independent hardware metering.

| Event | Goal-wording returned | Fixed-product returned | Combined returned | Unreturned reservations |
|---|---:|---:|---:|---:|
| Task materialization | 1 | 6 | 7 | 0 |
| Environment construction | 2 | 6 | 8 | 0 |
| Environment initialization | 2 | 6 | 8 | 0 |
| Reset | 2 | 6 | 8 | 0 |
| Model loading | 1 | 6 | 7 | 0 |
| Model generation | 50 | 199 | 249 | 0 |
| Environment step | 50 | 198 | 248 | 1 |

Returned-generation receipts contain 13,175 + 61,223 = **74,398 input token IDs**, and 250 + 995 = **1,245 output token IDs**, including generated EOS. Reset plus returned step is 256 environment operations, with one additional reserved step unclosed. The final reserve lacks corresponding worker `step_started`; the inspected code checks for stop before sending ACK, but raw owner accounting remains unclosed. Do not mark it a successful action or refund it. The goal-wording attempt's second environment cleanup remains unknown even though the supervisor reports no remaining descendants. Total GPU device-hours are not derivable from these two ledgers alone.

The fixed-product source plan originally capped materializations at four; the coordinator configured eight and six returned. That +2 deviation is not cured by pooling this table or by calling the tasks a new study. No run may resume or retry on the basis of this accounting. Neither two incidents produces an accepted complete scientific experiment or a goal-wording pair. The exploratory two complete per-arm pairs both tie on success; missing outcomes remain unknown. All tasks are exposed and related.

Recount method: read existing owner `operation_reserved`/`operation_returned` events in each distinct run, and sum length of each worker `generation_returned` evidence's `output_ids` and `sequence` minus `output_ids`. The two attempts have independent ledgers and their costs are summed only for resource accounting; their outcomes and statistical denominators are not combined. Goal-wording owner SHA256 `7e94e1c2efbcaa62be2ce4b55714f3a1a461a836f9cf77d023e8bc5a68e562be`; per-arm individual worker and owner hashes are in the original `INDEPENDENT_COST_RECOUNT.json`/Astra's review. No model, GPU, environment or new materialization was used for this calculation.
