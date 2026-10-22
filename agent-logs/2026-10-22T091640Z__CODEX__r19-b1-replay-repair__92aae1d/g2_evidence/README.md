# Successor G2 raw evidence

These are byte-for-byte copies of the immutable successor output directory `artifacts/runtime/r19_b1_g2_recovery_after_089429e4_20261022T092806Z_92aae1d/`. They preserve the actual live run, model outputs, public transitions, branch traces, event sequence, unit receipts, runtime/environment identity, smoke verdict, and offline verification. They are not reconstructed or regenerated. Their SHA-256 values are in the parent `FILE_HASHES.sha256`; event and branch hashes are also bound by the execution manifest, supervisor receipt, and offline verification.

The two 1–10 MB files were reviewed for upload value: `execution_events.jsonl` (5,864,069 bytes) is the authentic ordered operation/generation ledger; `branches.jsonl` (4,629,330 bytes) contains the exact branch outputs and repeated K3 traces. Both are required to independently reconcile the PASS, are below the repository's 10 MB per-file threshold, contain no machine-home/temp paths or credential patterns, and are published byte-for-byte.

The supervisor's raw local-path-bearing receipt/status/log are kept outside this folder and excluded according to the parent `EXCLUDED_FILES.md` redaction map.
