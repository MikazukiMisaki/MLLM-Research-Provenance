# Independent SFT historical-candidate overlap recount

Scope: metadata joins only. Reviewed both previously materialized candidate inventories, engineering probe identity/hash bindings, original/extension/accepted SFT manifests, identifiers from three historical datasets, SFT audit report and relevant generator source. No candidate task bodies or outcomes were opened or selected, no environment, model or CUDA called. `check.py` is independently written; `RESULT.json` contains counts and hash bindings, no private task identities. Each input was hashed before and after and did not change.

## Recount

| Filter | Wider policy: rows / distinct parent union | Protect all prior-proposal parents: rows / distinct parent union |
|---|---:|---:|
| Existing inventories before two engineering probes | 102 / 42 | 17 / 6 |
| Protect both probe parents and exact task/game/trajectory identities | 98 / 40 | 17 / 6 |
| Additionally exclude parent of every initial or extension train/validation manifest task | 85 / **35** | 17 / **6** |

The 98 wider rows intersect 5 unique initial manifest tasks and 5 unique parents; excluding every sibling of those 5 parents removes 13 rows, including duplicates across data splits. Extension manifest intersects zero task IDs and zero parents. Result 85 rows have 29 train parents, 14 valid_train parents and 6 valid_unseen parents; all 14 valid_train parents are among the 29 train parents, so the union is 29+6=35, not 49. The 17 protected rows span 6 valid_unseen parents. This recalculation does not withdraw or override the 1,141-identity prior reservation: the 35-parent policy is merely a wider sensitivity scenario, not the protected policy.

## What the historical evidence proves

The initial manifest contains 1,350 train/validation candidate identities; the five overlapping candidate identities were **planned** in that initial expert-data collection manifest. It is accurate to say a frozen SFT dataset audit labels 1,869 combined initial/extension candidate tasks as replayed, but `scripts/finalize_sft_balanced_dataset.py` constructs that replay count from hardcoded requested totals 1350+519 and infers rejection count by subtracting output identities. The local evidence examined here does **not** include per-task receipts for those five; it therefore does not independently prove each was actually replayed, had a particular rejection reason, or was viewed by any person. As a conservative design rule, their whole parents are excluded regardless.

Original, extension and balanced dataset files respectively contain 17,588 rows/1,140 unique task IDs, 4,339/133, and 20,967/1,200. The 98 post-probe wider inventory contains zero exact task IDs and zero parent identities present in each of these three datasets. This establishes only that these specific historical output files do not contain rows attributed to these exact tasks/parents. It does not establish that no other data source, model pretraining, evaluation, episode or human exposure occurred; absence in the successful dataset cannot establish that the five were actually collected and rejected. The accepted manifest contains 1,200 train/validation IDs, distinct from the collection's initial planned manifest; nominal validation and train rows in the balanced output should not all be described as optimizer-trained without checking the training pipeline.

Counts are conditional on the earlier inventories' metadata-only rules, existing file availability, known physical/identity alias exclusions and parent-as-unit rule. They are upper bounds under this filtering scope, not certified independently unseen layouts or a feasible experiment sample. No probabilistic power, task availability, legal status, or downstream authorization follows from this recount.
