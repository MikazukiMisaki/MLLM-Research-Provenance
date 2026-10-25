# SI-E2 bounded engineering invocation — runtime record

**Status:** `TECHNICAL_STOP_NO_RETRY`; the single root-released engineering invocation was consumed. This was not a scientific experiment and does not grant science authorization. No retry, repair, or second invocation is authorized here.

## Dispatch and identity

- Root dispatch `FINAL_ENGINEERING_DISPATCH.json` SHA256: `404370d8bea17fff1b5e39f9dfc1f7b1b9ad7bc92d73eec5ce93d29868f66c7c`.
- Wrapper SHA256: `06ef35837f5e0d52a111cdb4c9ea797c1dc46cf0eebcc98a31fdc8e1f68ae879`.
- Approved invocation SHA256: `f336b78a6aa3b24759ae492db9868576488e67c90c00cd93cd00eb7351f25b17`.
- Authorization SHA256: `f7334f8b3a5d8707f5226998e362d207ee429e7a296a772e9f0a216320c0882e`.
- Proposal Revision 2 SHA256: `1820e78ab1765fdf96109e319298f0c9eefa2f8ac26eaaa5f4e52cc78f0ea586`; source bindings Revision 2 SHA256: `b2fdaa6db55572d0eca4d92dd865497a2caac7f0f82b437e8f79fa58d3c75944`.
- Pre-dispatch check: `PRE_DISPATCH_CHECK_PASS` at `2026-10-25T14:07:22.524663Z`; 6 dispatch-bound files and all 71 entries across the preserved proposal/revision inventories verified. Source checkout `dfc00e49d1ef4d48453d2331507429f8a0c7bbc5`, branch `codex/si-p3-runtime-adaptation`, clean. Output path was absent. Authorization window was valid; no previous launcher artifact existed. Bound A40 UUID was visible and the compute-app table was empty.
- The exact dispatch argv was invoked once through the prescribed wrapper. Wrapper supervisor PID `836358` (PPID `836355`, PGID/SID `836358`, UID `2000`, start tick `478730594`); worker PID `836517` (PPID `836358`, PGID/SID `836517`, UID `2000`, start tick `478732272`). Both were confirmed gone after completion. No retry.
- Start UTC: `2026-10-25T14:07:32.731178Z`. Wrapper receipt file mtime / completion evidence: `2026-10-25T14:08:14.208095333Z`.

## Authentic outcome and root cause

Worker and supervisor authentic return code: `1`. Wrapper return code: `1`; monitor stop reason and wrapper exception are both null, so this was the worker's technical stop, not a monitor kill. The worker report is `TECHNICAL_STOP_NO_RETRY` with `ContractError: actual CUDA device UUID differs or is unobservable`.

The production path imported the pinned packages, verified historical artifacts, loaded the cached tokenizer once, and CPU-tokenized the four predeclared synthetic prompt strings. It then imported torch, called `torch.cuda.init()`, and failed the actual CUDA UUID check. Source order places the one-byte owned-context probe and Qwen policy/model-weight loading after that UUID check; they were not reached. No base model weights or adapter were loaded, no model generation occurred, and no generated action/world command was produced or executed. The token counts for the four CPU tokenizations were not emitted before the failure; the ledger records 0 input/output tokens and no follow-up tokenizer call was made.

The environment replay path was not reached: environment constructors `0`, resets `0`, action steps `0`. Engineering events are the four authentic transitions `engineering_opened → external_started(model_load) → external_failed → driver_failed`; the `model-load` unit is failed/open, with no completed external unit. No acquisition, training, evaluation, or science action occurred.

## Actual resource/cost accounting

- Wrapper elapsed: `41.48076330590993 s`; supervisor allocated interval: `23.847133793868124 s` = `0.006624203831630034 device-hours` on one allocated device. Within authorized ceilings.
- Wrapper sampled peak total GPU memory-used: `17 MiB` over 38 samples. Before/after resource readings were `14 MiB`; the wrapper's compute-app table was empty in every recorded sample. Treat 17 MiB as a sampled device-wide peak, not attributable worker allocation; own GPU PID/context was not proven.
- Ledger: generations `0`, generated tokens `0`, recorded input tokens `0`, resets `0`, steps `0`, environment constructs/closes `0`; one model-load call started, failed, and remains open in the failure ledger. Historical science remains `5,142 generations / 7,949 environment operations`; no cumulative scientific-cost increment.
- `resource_after.json` reports the bound A40 visible, 14 MiB used, with an empty compute-process table. This does not establish successful worker GPU ownership.

## Integrity and retained evidence

The captured post-run read-only audit returned `POSTRUN_INPUTS_UNCHANGED_AND_FAILURE_EVIDENCE_VERIFIED`: all 16 original source/config/game/domain/grammar/interpreter/package files matched their pre-dispatch hashes; all 12 frozen snapshot files matched the production gate hashes; P0 adapter directory hash matched `6e403d85b150a74dfcc176f1f180ce4baf6fdacd922d2f96b3ceef0a21100f11`. The six dispatch-bound review/authorization/proposal files matched; source checkout remained at exact SHA and clean.

Original runtime evidence remains in `engineering_run/`: `engineering_events.jsonl`, `engineering_report.json`, `launch_context.json`, `resource_after.json`, `supervisor_exit.json`, `worker_gate.json`, `worker_start.json`, and authentic empty `worker.stdout` / `worker.stderr`. Wrapper evidence remains at the task root: `launcher_invocation.json`, `launcher_start.json`, `launcher_receipt.json`, `gpu_monitor.jsonl`, `launcher.stdout`, and `launcher.stderr` (both child streams are zero bytes). Hashes are in `ENGINEERING_RUNTIME_INVENTORY.sha256`.

The wrapper's structured terminal result was returned by the execution tool and is durably represented by `launcher_receipt.json`; the child's stdout/stderr streams were separately persisted by the wrapper and are empty. No reconstructed transcript is labeled as raw output. No model weights, adapter payload, cache contents, or copied task data were added to this evidence directory.

Do not rerun this dispatch or attempt a second invocation. Any next step requires a separate root review/release; this record itself grants none. No Git publication/shared INDEX change was made.
