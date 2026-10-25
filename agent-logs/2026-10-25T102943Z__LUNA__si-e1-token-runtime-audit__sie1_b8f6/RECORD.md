# SI-E1 Luna read-only audit record

**Status:** `READ_ONLY_AUDIT_COMPLETE__RUNTIME_NOT_READY`  
**Scope:** tokenizer/background-S/CPU collator and runtime feasibility evidence only.  
**Writable boundary:** this Luna-owned task directory only.

## UTC window and source identity

- Captured audit subprocess window: start `2026-10-25T10:36:28.229107Z` (worker attempt 001) and finish `2026-10-25T10:41:39.675290Z` (finalizer completion). Each individual attempt's start/end UTC and actual child return code are preserved in its receipt. Attempt 001 returned 1 before tokenizer loading; attempts 002 and 003 returned 0. The finalizer returned 0. No timestamps or exit codes were reconstructed from memory.
- The actual scientific checkout used for imports was `/home/lizening/Alfworld-Self-Improvement-Project`, HEAD `4f5c2e18e0dfdf48e9471fcba0a3ee715be3ca3b`, branch `codex/progress-aware-recovery`. It was not HEAD `85cbb92395e5e2420c2adeb1fa0634653e742910`; that commit was checked as an existing Git object only.
- Actual imported module origins are retained in `input_bindings.json` → `python_path_policy.module_origins`. Independent root evidence `/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__SOL__si-e1-engineering-review__sie1_b8f6/independent_luna_helper_equivalence.json` (SHA256 `9061c15404c0753e7c997f09cd8677fd0450f120effb8b3c9f982da5ae4a9eb9`) confirms byte identity to exact 85 for exactly eight helper source files. This is file-scoped equality only, not whole-checkout identity, collector equivalence, or runtime readiness; details are recorded in `BINDINGS_SOURCE_SCOPE_ADDENDUM.json`.

## Results

1. Verified exact source/provenance state and all bound input paths/hashes; see `input_bindings.json`. Twenty-four inputs were present and all pre/post comparisons matched. Dataset SHA matched the contract value.
2. Produced `S_BACKGROUND_MANIFEST.json`: 120 unique fixed-hash S identities from known-use expert-train identities, family quotas 44/32/20/11/13, zero overlap with adopted 96/48/600/reserve identities. The compact rows contain no full prompt, training example, or token-ID list.
3. Loaded only the two local tokenizers, offline: exact cached base revision and actual P0 final-adapter tokenizer. Fixed S120 output lengths, prompt prefix, `enable_thinking=False` template, terminal EOS, 2,048 no-truncation, token-ID digests, and CPU collator masks are documented in `TOKENIZER_MASK_AUDIT.json` and `.md`. Tokenizers agree on the fixed rows, but tokenizer configuration file bytes differ; differences are explicitly preserved.
4. A first Luna-local worker attempt exited 1 before tokenizer loading due to a local helper-name/import failure. Its real return code, stderr/stdout bytes and hashes are retained as attempt 001. Two subsequent read-only worker attempts exited 0; their unmodified capture receipts/raw output are retained. This is engineering audit history, not a scientific failure and not a source-code/data change.
5. The tokenizer-only audit does not establish actual model runtime, generation behavior, GPU memory/device-hours, environment compatibility, training feasibility, or future paired B/C exposure. The allowed pure SFT production helpers were used, but no standalone project-level validator was run. No readiness gate or execution authorization was produced.
6. The P3 output-token cap wording correction is recorded in `TOKENIZER_MASK_AUDIT.md`: `4,800×16 + 96×40 + 96×16 + 3,504×16 = 138,240`. The budget is unchanged.

## Activity accounting

Across captured attempts: tokenizer loads 4; selected-row encodings 240 per tokenizer; P0 template renders 240 per tokenizer; tokenizer function calls 489 base / 480 adapter; CPU toy/collator invocations 4. Actual model loads 0, generation calls 0, training runs 0, ALFWorld constructions/resets/steps 0, source collection 0. Future B/C exposure is `NOT_OBSERVED`. The source/task budget figures are planned P3 arithmetic only and do not add or repeat historical R19 costs.

## Frozen files

- `S_BACKGROUND_MANIFEST.json`
- `TOKENIZER_MASK_AUDIT.json` and `TOKENIZER_MASK_AUDIT.md`
- `READ_ONLY_READINESS.md`
- `input_bindings.json`
- `audit_worker.py`, `run_capture.py`, `finalize_audit.py`, `capture_finalize.py` (Luna-owned audit helpers; not project scientific code)
- `audit_worker_001/002/003.receipt.json`, `dependency_probe.receipt.json`, `finalize_audit.receipt.json`
- `raw/` actual captured subprocess stdout/stderr
- `RECORD.md`, `FILE_HASHES.sha256`

No files were added to a shared INDEX, committed, or pushed.
