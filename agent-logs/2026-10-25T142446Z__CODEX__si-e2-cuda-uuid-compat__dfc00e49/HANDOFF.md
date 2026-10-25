# SI-E2 CUDA UUID compatibility — frozen implementation handoff

Candidate `844cc4b78df1f83e29391ffd5ab861a2d0c0a3fd`; direct parent `dfc00e49d1ef4d48453d2331507429f8a0c7bbc5`.
Own worktree `/home/lizening/wt-si-e2-cuda-uuid-compat`; branch/remote ref `refs/heads/codex/si-e2-cuda-uuid-compat`.
Status: FROZEN_FOR_INDEPENDENT_EXACT_SHA_REVIEW. Developer software evidence only. Actual execution remains BLOCKED; no runtime readiness or retry permission follows.

## Scope and actual evidence

The unique task SHA256 is `a4a7eca995bab03e8fca768be0b1724d72e91c96ad07ec0407a58c788fe8f94d`. All six required instruction/project documents were read before code changes. The original dfc worktree, handoff, authorization and failed evidence were preserved. The separate read-only static addendum is frozen at `/home/lizening/research-notes/agent-logs/2026-10-25T141130Z__CODEX__si-e2-uuid-static-addendum__dfc00e49` (`STATIC_DIAGNOSIS.md` SHA256 `9714de79099866eade57d8bc1578f2b00675c4d99f8662bbdb3be046cb084544`).

CONFIRMED: later independently authorized identity receipts show torch._C._CUuuid str `b08bc603-ebdb-787d-b5b6-ec796ea3022a`, while NVML/authorization use `GPU-b08bc603-ebdb-787d-b5b6-ec796ea3022a`. Full payloads match, direct strings do not. The original full probe did not record its own raw UUID/type, so that missing observation remains missing. No original record is retroactively repaired.

CONFIRMED: independent identity receipt also shows local PID 837631 vs NVML PID 3082604, `[Not Found]`, and own_compute_row_observed=false. Their mapping remains NOT_PROVEN. This is a separate runtime blocker even after format compatibility is repaired.

## Exact source delta

Two files only: runtime_backend.py modified and tests/test_si_e2_cuda_uuid_compat.py added; 344 insertions / 4 deletions. Of 542 preexisting tracked files, 541 blobs remain identical; runtime_backend.py is the sole changed old blob.

* `cuda_uuid_matches`: pure strict full 8-4-4-4-12 hex matching. Expected must be an exact GPU-prefixed canonical UUID; observation may be complete bare canonical or complete GPU-prefixed canonical. Hex case alone is immaterial to the same full 128-bit identity. No trimming, partial IDs, UUID-to-ordinal conversion, name/memory substitutes, MIG/URN/braces/multiple values or malformed input acceptance.
* `verify_cuda_uuid`: records present/type_module/type_name/str/repr, expected UUID, ordinal and phase in an existing `resource` event. Real EngineeringLedger.append flush/fsync happens before comparison. Missing property remains explicit; property/str/repr exceptions are recorded and propagated. UUID text is recorded unnormalized.
* `LocalInference.load`: exactly two old comparison calls replaced by the same helper, at the original pre-one-byte and post-load positions. The point `cuda_uuid_before_context` means before the explicit one-byte context probe, after existing cuda.init(); it does not claim zero initialization before the record.

`EXACT_SOURCE_SCOPE_AND_METHOD_HASHES.json` gives old/new AST hashes and proves the exact two-call overlay. No other existing method changed. inspect_gpu/validate_gpu_rows, allowed PID and UID logic, raw NVML errors, package/source checks, ledger, costs, prompts, parser, scheduler, treatment, partitions and scientific fingerprints remain byte-identical.

The one-byte own-context check still precedes the 8B/P0 loader. We did not add a host-PID alias, accept an unknown PID, introduce fallback, change execution permissions, or add acquisition/training/evaluation drivers. The consumed authorization cannot authenticate this new source SHA.

## Software evidence and actual exits

Pinned interpreter `/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python`; deliberate current src:tests PYTHONPATH, inherited Python settings cleared, CUDA_VISIBLE_DEVICES empty, offline settings, no pytest cache/bytecode. All candidate checks started and ended with a clean committed worktree.

| Check | Result | Raw evidence |
|---|---|---|
| Focused UUID + all existing SI-E2 tests | 153 passed, exit 0 | focused.xml; receipts/focused.stdout/.stderr/.receipt.json |
| Comparable full suite | 953 passed / 3 failed / 77 errors, exit 1 | full.xml; receipts/full.stdout/.stderr/.receipt.json |
| Frozen dfc reference | 883 passed / 3 failed / 77 errors | immutable saved dfc frozen_full.xml, bound by SHA; not rerun |
| Full ID comparison | same exact 80 failure/error ID+type pairs; every old status unchanged; all 70 new cases pass, no missing IDs or new skips | REGRESSION_COMPARISON.json |
| Compile two changed/new Python files | exit 0 | receipts/compile.* |
| git diff --check base..candidate | exit 0 | receipts/diff_check.* |
| Captured raw UUID/PID consumer software check | exit 0; old direct match false, strict match true; captured unmapped PID rejected with raw compute text | CAPTURED_WIRE_SOFTWARE_CHECK.json; receipts/captured_wire.* |
| Genuine child abruptly exits without journal close | actual child exit 23, journal still readable; fsync independently observed in focused test | selected_software_fixtures child_receipt.json/stdout/stderr/durable.jsonl |
| Non-force source push / live equality | exit 0; local=tracking=live=exact candidate, clean | LIVE_REMOTE_EQUALITY.json; receipts/nonforce_push.* and live_remote_after.* |

New tests exercise the actual production comparator, identity observer, LocalInference.load, real journal/reconstruction and unchanged inspect_gpu validator. Only CUDA, tokenizer/model construction and NVML subprocess boundaries are fake. Both loader checks, first-assertion-before-tensor/weights, post-load drift, missing/invalid UUID, property/conversion errors, unnormalized durable raw evidence and foreign NVML PID rejection are covered. No validator or journal is replaced with an always-pass implementation.

The captured-wire check reads both hash-pinned real identity JSONs but reconstructs a software object; it does not claim to instantiate the actual compiled _CUuuid or obtain a new live observation. Its memory columns are explicitly fixture columns; the actual compute row is preserved verbatim. The script asserts no torch import and zero real hardware/model/environment calls. The full/focused suites retain their existing tiny CPU PEFT/generation/optimizer software exercises; these are not actual 8B/P0 training or scientific examples.

## Frozen inputs and publication

`INPUT_BINDINGS_BEFORE.json` and `ORIGINAL_INPUTS_AFTER.json` bind/recheck 18 originals, including task, actual identity evidence, failed run, old own manifest and full XML, root review and required project documents. All match. All 102 original own handoff hash entries and the separate static addendum hashes still match. Original dfc/a995/85/2da worktree SHAs are unchanged; own new worktree is clean. No old evidence, shared INDEX/inventory, reviewer worktree or provenance Git was edited/staged/pushed.

`PUBLICATION_MANIFEST.json` selects compact files only; `FILE_HASHES.sha256` also binds that manifest. Local /tmp focused/full fixture trees remain retained; neural fixture weights/token caches are not selected. Root alone publishes provenance. Initial status fields describe creation time and are not an independent acceptance.

## Limits / handoff to root

Independent review of this exact SHA is PENDING. UUID byte equivalence is not process identity, model fit, memory stability or inference readiness. The captured host/local PID mismatch remains independently BLOCKING and was reproduced against unchanged production guards using software input. No actual CUDA/context, 8B/P0 or ALFWorld invocation, original probe retry, acquisition, training or evaluation was performed by this assignment. The historical scientific total remains 5142 generations / 7949 reset-inclusive operations; prior engineering device-hours and all failed/open evidence remain intact.

Only an independently reviewed new execution context with proven ownership plus fresh root engineering authorization could permit another runtime action. This delivery authorizes none.
