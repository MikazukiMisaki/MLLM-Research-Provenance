# SI-E2 engineering execution record (append-only)

**Final outcome:** `TECHNICAL_STOP_NO_RETRY`. The one root-released engineering invocation was consumed and exited 1. This is not a scientific experiment, not an actual Qwen3-8B/P0 load, and not evidence of inference memory fit. No second invocation, GPU/CUDA follow-up, model call, environment replay, or science execution is authorized by this record.

## Exact dispatch and preserved proposal

Root dispatch SHA256 `404370d8bea17fff1b5e39f9dfc1f7b1b9ad7bc92d73eec5ce93d29868f66c7c`; prescribed wrapper SHA256 `06ef35837f5e0d52a111cdb4c9ea797c1dc46cf0eebcc98a31fdc8e1f68ae879`; approved invocation SHA256 `f336b78a6aa3b24759ae492db9868576488e67c90c00cd93cd00eb7351f25b17`; authorization SHA256 `f7334f8b3a5d8707f5226998e362d207ee429e7a296a772e9f0a216320c0882e`.

The wrapper was invoked once with the exact dispatch argv. Proposal Revision 2 SHA256 `1820e78ab1765fdf96109e319298f0c9eefa2f8ac26eaaa5f4e52cc78f0ea586`; corrected first-source binding SHA256 `b2fdaa6db55572d0eca4d92dd865497a2caac7f0f82b437e8f79fa58d3c75944`. The original 47-file proposal inventory, Revision 2 inventory (15 files), and source-binding Revision 2 inventory (9 files) were verified before dispatch and remain preserved. No source files, proposal inputs, or historical evidence were edited.

## Authentic run identity and exit

- Source: clean `dfc00e49d1ef4d48453d2331507429f8a0c7bbc5`, branch `codex/si-p3-runtime-adaptation`.
- Output: `engineering_run/`; no previous output existed before dispatch.
- Start UTC: `2026-10-25T14:07:32.731178Z`; wrapper receipt file mtime: `2026-10-25T14:08:14.208095333Z`.
- Wrapper supervisor PID 836358; child PID 836517. Both exited and were absent on post-run process checks. Wrapper authentic child return code 1; supervisor exit and worker report also record authentic return code 1. No wrapper exception, no monitor-triggered stop, no retry.
- Stop: `ContractError: actual CUDA device UUID differs or is unobservable` during the bounded model-load gate.

## Reached boundary and costs

The worker verified package origins and frozen artifact hashes, loaded the cached tokenizer once, and CPU-tokenized the four fixed synthetic prompts. It called `torch.cuda.init()` and queried CUDA device properties, then failed the approved UUID comparison. Production source order shows that the one-byte owned-context probe and Qwen policy/model-weight load occur after this check; neither was reached. No base-model weights or P0 adapter were loaded, and no model generation or generated world action occurred. Exact token lengths from the pre-CUDA CPU tokenization were not emitted; ledger input/output token counts are both 0. No second tokenizer call was made.

The replay path was not reached: ALFWorld constructors 0, resets 0, physical steps 0. Authentic ledger sequence: `engineering_opened → external_started(model_load) → external_failed → driver_failed`; the model-load unit is failed/open, with 0 completed external units.

- Wrapper elapsed: 41.48076330590993 s.
- Supervisor allocated interval: 23.847133793868124 s = 0.006624203831630034 device-hours (nonzero, within bound).
- Sampled device-wide memory peak: 17 MiB over 38 samples; pre/post readings were 14 MiB. The compute-app table was empty across samples, so the sampled peak is not attributed to the worker and does not prove own GPU PID/context ownership.
- Ledger generations 0; generated tokens 0; recorded input tokens 0; resets 0; steps 0; environment constructs/closes 0. Historical science remains 5,142 generations / 7,949 environment operations, unchanged.

## Post-run integrity

`POSTRUN_ENGINEERING_AUDIT_RECEIPT.json` and its raw stdout report `POSTRUN_INPUTS_UNCHANGED_AND_FAILURE_EVIDENCE_VERIFIED`. All 16 pre-dispatch source/config/game/domain/grammar/interpreter/package inputs match their original hashes; all 12 frozen snapshot-file hashes and P0 adapter directory hash match the pre-load artifact gate; dispatch-bound review/authorization/proposal files and the exact clean source SHA also match. The raw report, four-event ledger, launch context, worker gate/start, resource-after, supervisor exit, wrapper receipt, 38-row raw monitor, and empty worker/launcher stdout/stderr remain untouched under `engineering_run/`, the task root, and `raw/`.

`ENGINEERING_FINAL_AUDIT.json` records final read-only rehash and resource observations. `ENGINEERING_FINAL_PUBLICATION_MANIFEST.json` lists preserved proposal/revision inventories and genuine runtime/launcher/monitor evidence, with local-only or machine-specific items explicitly flagged for root review. `ENGINEERING_FINAL_PUBLICATION_MANIFEST.sha256` provides its detached digest. No files were staged, committed, or pushed; root retains publication ownership.

**Explicit non-claims:** no successful CUDA UUID/PID ownership proof, no Qwen3-8B or P0 adapter load, no generation/inference, no environment replay, no inference memory-fit result, no engineering PASS, and no scientific result.
