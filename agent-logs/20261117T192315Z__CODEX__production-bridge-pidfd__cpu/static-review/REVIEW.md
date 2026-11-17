# Independent review: static pair adapter

**HOLD; declaration drafting only.** No production parent–worker bridge or runnable scientific entrypoint is present. One independently reproduced budget-sufficiency gap exists within the static arithmetic; the module marks outputs NOT_AUTHORIZED and does not execute experiments.

## Evidence and execution scope

Candidate `/home/lizening/research-notes/agent-logs/20261118__CODEX__pair-owned-static-adapter__private/`: 7/7 inventory entries independently checked (`inventory.log`), manifest SHA256 `bd606b7c35ea8a47704b38e5cc0ee366a5ae6498e64d67a5b4de645cc60d6d36`. Key file SHA256 `static_adapter.py` `66a1de9889e4446084630ffd0c55387e3d459ab4290f7f7cf63482f466e09753`; `test_static_adapter.py` `144067df3fff765176ec84057a7b0794f72690768d4d8c1b3f863c5013474cd0`; `REPORT.md` `a032b430e2fe49232b40ad3144cf471e77d8fae05f0679096f19e71bbebcacd5`.

Two independent fictional CPU tests passed, exit 0 (`tests.log`). AST/code review finds no module main, process launch, model, GPU or environment invocation. `launch()` unconditionally raises HOLD (`static_adapter.py:132–133`); the held worker itself has an unconditional first `raise` (`pair-owned-scheduler-v4__private/fixed_product_dev/worker.py:43–45`). The source checker reads and hashes code; the adapter does not physically authenticate any model or task. It is inaccurate to call it zero filesystem access: `check_source_contract` does perform read-only source reads.

`check_source_contract` (`static_adapter.py:12–20,42–52`) hashes seven named v4 candidate files and parses three AST interface shapes; independent test executes this check. The candidate's `draft_arm_config` does not itself call that function: it compares caller-supplied code file digest declarations with the seven expected digest strings (`:116–123`). It does not bind actual runtime imports, all dependencies, process origin or a real product. Source hash match and fictional plan acceptance do not establish a complete source or runtime identity.

Products are caller-supplied record bytes and a caller-supplied digest compared with in-memory declarations (`:53–69`); real base/adapter tree bytes and authority of the digest remain unverified. Historical ledger hash and used amounts are caller claims (`:83–92`); there is no ledger read or actual cost reconciliation. Manifest, input paths and pair binding are also claims; paths are lexical only and can traverse symlinks, and JSON duplicate keys are not rejected. These limits are disclosed in the candidate report.

## Additional reproduced budget weakness

`validate_plan` tests only that nonnegative caller-provided historical + proposed <= caller-provided ceiling (`:83–92`); it does not derive or require proposed additions from the four-pair plan or frozen operation maxima. Independently changing all three fictional `proposed_additional` values to zero still yields `DECLARATIONS_CONSISTENT_NOT_AUTHORIZED`, and `draft_arm_config` also returns a draft, while eight episodes and up to four materializations remain in its declared limits. This is an arithmetic/coverage gap in the declaration checker, not an actual authorization, run or overspend. Reproducer `reproduce_zero_increment.py` SHA256 `f6cf4d2ed17cfc3088c154d76aaa2629ba4b77c7b8af872973622716727d30f4`; output SHA256 `032d2a760f9fbf172334bd08b44397228a222faa019212a5849d2cfc98442844`.

Before relying on this as budget evidence, reconcile authenticated prior use, derive required additional ceilings from the precise proposed operations and stop policy, and require total ceilings and reserved headroom to cover them; alternatively explicitly treat the check as declaration syntax only. Also bind physical token/time/device budget to the real parent owner, not just these declarations.

## Remaining bridge

Actual parent must safely create and identify the held worker/IPC fd, bind real manifest/source/product bytes and paired initial state, fsync global reservations before ACK, use verified per-arm and historical budgets, handle UNKNOWN and clean up known direct children without making host/GPU/descendant claims. The existing `scheduler_synthetic.py` invokes only a fake worker, while `worker.py` is deliberately held. This narrow review did not exercise a real task, worker, model, GPU, environment or preflight and grants no launch authorization.
