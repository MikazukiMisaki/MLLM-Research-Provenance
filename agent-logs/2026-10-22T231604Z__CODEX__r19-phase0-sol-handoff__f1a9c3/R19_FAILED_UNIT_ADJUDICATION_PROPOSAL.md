# Failed source unit adjudication proposal

> **PROPOSAL ONLY — NOT_ADJUDICATED_BY_LUNA / NOT_APPROVED.** Sol owns the independent final adjudication. Do not modify the original event journal, resolution event, registry, execution manifest, or supervisor receipts.

## Proposed bounded disposition

- Run: `3d1ccea7e97f4727abf8e216ac6ec498`, implementation `bf31f3da430ffc35bd17fc380e1752adce6d1467`, authentic child exit 1 from `subprocess.returncode`.
- Unit: `source_episode`, unit ID `7d9da2ea723b4e93b76804e8c552a7f06aaf23e53559c5e54ddd19310e6d7689`, schedule index 0, task `pick_and_place_simple-Pencil-None-GarbageCan-316/trial_T20190907_165839_449092`, seed 30000.
- Proposed disposition string: `KNOWN_FAILED_SOURCE_CONTRACT_AFTER_GENERATION_BEFORE_ACTION`.
- Physical outcome: determinate known software failure after one completed reset and one completed actor generation (267 input + 5 generated tokens); zero environment action steps; zero completed source episodes; zero incomplete external operations.
- Enclosing unit outcome: `INCOMPLETE_PRESERVED_IN_ORIGINAL_REGISTRY`. No task success/failure label is supported because no task action occurred. The physical operation outcomes are known, while the source episode itself did not finish.
- Preserve the raw unit registry's `in_progress` status, execution manifest's `RUNNING` status, and the exact original files/hashes. Do not call `UnitRegistry.begin/complete`, mutate the old directory, resume it, or use it as a writable output.

## Evidence binding Sol's immutable receipt must include

The independent receipt should bind all of the following, then state its decision and reviewer identity without rewriting any source evidence:

1. Failed run ID, failed implementation SHA, unit ID, schedule index, canonical TRAIN identity, seed and original output directory.
2. Raw execution journal SHA `fde95fcd72f1c4ac6409fab7f2112654e145f6184fefec690cae58ad345f1cd7`; manifest `f5d3efa6c17abea3d944d7dea01099210d846eb8ed107057ec24502bbb51d2df`; registry `870923242ae585c66cbcffa554528ab3d92cf98fc4d87dee2c4d408f5f6ba800`; empty branch ledger `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
3. Authentic supervisor runner log `ee7c6010edf0e46bcba2969cdddf236e7c6d23830d2bd92e88593d7a21a7bbcd`, runner exit `a802079398fd415765b8f6b8685fec998325625da733011ff7a9ce11459a9386`, status `e2a70bf670376b648e52357376fa88f3a7a3cac92b41a5c628bd4ad251353913`, launch context `6b8933ed06db1b2e74f1b921ca13e6f73842b18e7a0c8217381a809ed4ea180e`, and independent failure audit `8eb1248c1d863674119813ba1f90ba3ca6834bb1906cb2aa67acc6a4e087fe34`.
4. Sol raw-ledger validator result/audit SHA `b666f5d2d69171a0305c6657f952d70f5ab304295c13b171fc77690a9cb05dab`, with the aggregate physical total 177 generations / 330 non-reset operations + 12 resets = 342 operations and zero incomplete operations.
5. Existing append-only resolution JSONL hash `58783ba60b076ee190dccb0875aac65891d7e1c811e00fbe6303ca65896369d9`; explicitly note it still contains `review_status=PENDING_EXACT_SHA_REVIEW`. Preserve its bytes. The new external receipt may supersede that pending marker, but must not claim the old line was edited or already reviewed.

The subsequent replacement campaign, if separately authorized later, must keep this failed source unit's history linked and must repeat schedule index 0 under the newly reviewed code, charging one new reset/generation and comparing before the first task action. That is not part of this adjudication, and this proposal does not authorize a replay, preflight, or live launch.
