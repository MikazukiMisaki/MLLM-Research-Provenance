# SI-E2 real-runtime adaptation and GPU resource review

- Agent: Sol Designer / root technical lead and independent reviewer; thread `01a0994c-a209-7600-8a3e-5ff3096ed346`.
- Start UTC: 2026-10-25T12:41:18Z. Finish UTC: recorded in `task_finalization.json`.
- Status: **SOFTWARE_REVIEW_PASS_ENGINEERING_ONLY / REAL_RUNTIME_BLOCKED / UUID_COMPATIBILITY_FIX_ASSIGNED**. This is a final checkpoint record, not a runtime or science clearance.
- Scientific review root `/home/lizening/wt-codex-r18c2`, branch `agent/codex-r18c2`, clean start/end `e537f441010077123a307e9d50ea40cf8dad8547`.
- Frozen base `a995d4c3c5f7d31a2cf1fd0afc4bfa4bd72ee3a3`; reviewed candidate `dfc00e49d1ef4d48453d2331507429f8a0c7bbc5`, branch `codex/si-p3-runtime-adaptation`, clean and live remote verified. No root scientific source changes. No development in the authoritative worktree.
- Provenance starting main `aa925dd0ba4a44121e1a9eeaddb36a13eec974a4`; containing publication commit resolves via Git history. Final remote verification is preserved in ignored `post-push-receipt.json`.

## Work, independent evidence and actual execution

Read AGENTS, all five required project documents, prior exact-SHA SI-E1 review and task-record protocol. Dispatched implementation to actual Sol Research thread `01a165de-c75e-7120-abc9-fa74cde1f17f` and resource/execution work to Luna thread `01a09fcb-ab5f-7b83-9acf-91026145b764`. Native app messaging/status became unreliable; actual CLI queue receipts are retained. Queueing is not represented as execution; subsequent agent-owned raw artifacts establish actions.

Reviewed all 15 added files and 527 unchanged old blobs; source semantics/scientific execution unchanged. Root used a separate clean detached checkout `/tmp/si-e2-independent-review-dfc00e49`. Comparable independent full suite: **883 passed / 3 failed / 77 errors**, real exit1; exact same 80 historical IDs/types as pristine a995, all83 new tests pass, no skips. Compile/diff checks pass. An initial collection-only harness error (10 errors, exit2) is retained and explained in `INDEPENDENT_HARNESS_CORRECTION.md`; inherited Python settings were removed, then the same explicit checkout/src software binding as the baseline was applied. Real runtime CLI remains isolated `-I` with no Python environment inheritance.

Independent frozen-generation differential: 12 combinations of four phases and three token termination cases, cached real tokenizer and tiny CPU PEFT, synthetic generation edge; all raw fields/full input IDs/masks match except timing/additional state proof. Software tests include actual tiny CPU model/optimizer APIs and are not claimed zero model API activity. No actual 8B/P0 scientific training or evaluation occurred.

Root found a PEFT restoration defect in an intermediate draft using a CPU toy; final dfc explicitly restores original gradient flags and tests success/exception state. Root independently rehashed 12 base files, 11 P0 files, five old G3 critical files; all28 match before/after the full probe. Pinned module/version/file bindings pass without CUDA context during software review.

Luna concrete proposal original bytes remain frozen; Revision2 corrected data root and auxiliary first-line hash. Root actual model-free production authenticate/artifact/replay/package/tokenizer/GPU checks pass, true exit0, no model/world calls. This is not a formal scientific preflight.

Root and a separate critic reviewed coordinator launcher and monitoring; one partial-marker JSON race was fixed before release. `FINAL_ENGINEERING_DISPATCH.json` binds the wrapper, exact CLI/environment/source/reviews/proposal and one-only authorization. Luna invoked it once. Genuine full engineering child exit1; wrapper exit1, not monitor-killed, no deadline and no residual process. `torch.cuda.init()` ran, then UUID guard failed before one-byte proof, 8B load, generation or environment calls. Failed/open model-load evidence preserved. Root independently replays the four-event hashchain and cost ledger. Supervisor 23.847seconds/0.006624device-hours; no completed gen/reset/step. The 38 monitor samples show global14–17MiB and no compute row; not a model-fit measurement.

A separate root-reviewed, fresh-identity **pure CUDA identity** release allowed <=60seconds, one explicit byte, no model/world. It exited1 in2.571seconds, within cap, no residual process. Its preallocation checkpoint proves raw Torch `_CUuuid` is a bare full UUID while NVML has `GPU-`; full 128-bit identity agrees. The same diagnostic independently exposes localPID837631 versus NVML3082604 with no trusted map. Ownership remains UNPROVEN; no fallback or waiver. Raw observations and conservative nonzero time are independently reviewed in `independent_cuda_identity_review.json`.

## Boundaries, costs and next action

Historical scientific cumulative remains5142generations/7949reset-inclusive operations. New engineering generations, ALFWorld construct/reset/step, acquisition, student training/evaluation, held-out task bodies and G2/G3/G4 reruns: **0**. Two CUDA initializations and one one-byte tensor are real engineering expenditure, separately recorded. Original raw G3/failed unit and scientific inputs untouched. No automatic retry or weight/cache copy.

All tested software contracts pass, but actual 8B/P0/ALFWorld readiness, inference/training memory/throughput and96 acquisition feasibility remain **NOT PROVEN**. Root assigned only strict UUID compatibility/evidence persistence software repair via `SOL_UUID_COMPATIBILITY_TASK.md`; unknown host PID must remain blocking. New exact-SHA review and proven execution context are independent prerequisites; no full-probe, acquisition, training or evaluation release is granted.

## Publication

Root alone coordinates six completed task directories (this review; frozen implementation; Luna readiness; Luna proposal/full failure; Sol read-only UUID addendum; Luna identity diagnostic). Explicit safe file manifests, local omission size/hashes, credential scan and rolling inventory accompany publication. Preserve all prior finalized bytes. No broad staging, weights/adapter/cache/dataset/software fixture payloads or credentials. Publication is a provenance action and confers no launch authority. See `FINAL_OUTCOME.md` for the decision and linked machine receipts for exact hashes.
