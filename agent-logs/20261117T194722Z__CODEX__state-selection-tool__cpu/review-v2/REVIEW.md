# Independent review: state-selection prototype v2

**PASS for the scoped fictional duplicate-reference repair; scientific use remains HOLD.** Original same-reference cross-parent alias is rejected, as are terminal hard links and complete decision-reference tuples made of hard links. A shared label alone remains valid. Distinct copied files and fabricated IDs still pass: this is an explicit provenance limitation, not evidence of 16 authentic parents.

## Exact evidence

Candidate `/home/lizening/research-notes/agent-logs/20261118__CODEX__si-state-selection-cpu-v2__private/`; `FILE_HASHES.sha256` SHA256 `697528040927db1d2675c94adc90a6c2059e3cff422cbeb1176917d85e7a6cc1`; all six entries verified. `select_pairs.py` SHA256 `50f85244d80664e2c1d83eb311a0ce66891522ca2bcd4ae29c9a24c4c44ea462`; `test_selector.py` `fe024c59f5ca536e50c0d232812e62a3ff545ec504b327e367524ad5a325dcca`; `README.md` `718e316584ebb6e440650702a829928ecd37b4a9979a3463cb8a2738860a7993`. Independent pinned-Python run of twelve fictional CPU tests passed, exit 0; `tests.log` SHA256 `20c3f425f11c7e2541edaecaefd7ab7a062ad111adef12af45b7afe543b8dc0c`.

Reviewer-authored fictional replay `replay_aliases.py` SHA256 `550ec067688a32ba56fe35f24fb4738fba4ba73f934ef8011a76858efae99e39`; raw `replay_aliases.log` SHA256 `8d0767144a04f1579a838e754684bc9b3fe7372b743bd1783a10497fad8646ef`. Results: v1's exact whole-episode alias rejected on episode ID; a terminal hardlink rejected on device/inode reuse; all four decision refs hardlinked under new filenames rejected on tuple identity; sharing one label ref accepted; copying original bytes to new inodes and supplying fresh caller-claimed episode/decision IDs accepted, classified as unverified claims.

## What is fixed and what is not

`select_pairs.py:80–103` requires unique declared cohort-wide episode and decision IDs, tracks terminal device/inode across parents, and rejects a repeated four-component decision-reference device/inode tuple across parents. V2 explicitly scopes IDs globally; actual source record identity must be mapped into that scope before use. Matching content alone does not establish duplicate record identity: distinct real episodes may have identical labels and/or text. Conversely, copying bytes to new files or changing caller claims defeats these structural alias checks; successful filtering does not authenticate source, action history, actual input, origin, terminal success or parent lineage.

The suite also retains manifest/hash binding, declared cross train/evaluation lineage overlap rejection, claimed first-episode/no-backfill behavior and strict paired IDs/masks. First episode, lineage and input authenticity are not independently verified by this prototype. The schema is provisional and status remains `SELECTED_UNVERIFIED_CLAIMS`, `source_identity=UNKNOWN`, `execution_identity=UNKNOWN`, `lineage_authenticity=UNKNOWN`, `scientific_use=HOLD`. The terminal JSON is a claimed boolean, not independently bound native proof; returned JSONLs are references, not actual trainer-ready data. Same-UID races, complete durable output, real trainer transformation, evaluation source and real budget remain unverified.

No real task, model, environment, GPU or preflight was accessed or run. No candidate or prior evidence changed. This limited review grants no scientific execution authorization.
