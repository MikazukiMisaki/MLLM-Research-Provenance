# SI-U1 approved extraction: technical stop

The independently accepted completed evaluation was submitted to the single approved offline extractor execution using pinned Python and the frozen specification and approval. The actual extractor child PID was 951017 and its observed return code was 1. It stopped at `si_u1_extract.py:154` in `binding(f)` with `Rejected: bound byte mismatch` while checking a tokenizer file, before the complete production auditor and statistics. No analysis output was produced, and no retry was made. The traceback does not alone identify which binding predicate failed.

The original evaluation tree was independently hashed before and after; the two inventories are identical. Frozen specification references, authorization, approval, independent operational review, and extractor file were also rehashed after the attempt and matched. The invocation used the offline environment with `CUDA_VISIBLE_DEVICES` empty; it did not invoke model, CUDA, or environment. Original evaluation and input files were not modified.

`PROCESS_RECEIPT.json`, `stdout`, and `stderr` record the actual child command, return code, and output. `original_before.json` and `original_after.json` contain the matching full original-tree snapshots. `LAUNCH_STOP.md` separately documents the preceding outer shell exit 127: that failed before the wrapper or extractor started and is not a production extraction attempt. Root explicitly disposed of that launcher error before authorizing the actual single execution documented here.

Current status: `EXTRACTION_TECHNICAL_STOP`; scientific conclusions and independent statistical recomputation remain blocked pending review and resolution. No data from results is reported here.
