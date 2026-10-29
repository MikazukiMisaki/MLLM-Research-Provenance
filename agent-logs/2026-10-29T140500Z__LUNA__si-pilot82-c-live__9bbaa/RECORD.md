# SI-U1 pilot82 C training: original execution record

Status: OBSERVED_COMPLETED_AWAIT_INDEPENDENT_REVIEW. Scientific source 9bbaa12c2d8177a60ec5a74ed2f970ef29a57bce; run d83bc760a92f468abe7d3e300450eb5e. The separately cleared C arm started from the original frozen P0, after independent acceptance of B. No evaluation or retry was performed.

The genuine supervisor returned 0, within its 5,400 second cap, with cleanup established. The event ledger records 78 optimizer updates and 1,248 microbatches with the frozen sample order; 695,872 input tokens and 6,240 supervised tokens. Recorded losses were finite; all resource rows passed and report zero allocator OOMs/retries. Final C adapter tree SHA256 40202cade31425b823ae4b153f2c975487d64b48461b47b922aebda226dd4c57; its weights remain in the original local output and are not included in the evidence archive. Frozen base and original P0 tree hashes remained unchanged.

Supervisor device allocation was 916.8313971711323 seconds; B plus C scientific allocation 1800.0549747627229 seconds. Earlier engineering allocation 455.8560599721968 seconds is accounted separately. These elapsed allocation intervals are not evidence of exclusively owned GPU use. The completed training execution does not establish any outcome on held-out tasks.

C_RUN_AUDIT.json contains actual process receipts, ledger/resource checks and the 27-member raw archive inventory. The archive is private, contains task/sample metadata, and excludes adapter weights and dataset text; every member was rehashed against its unchanged original. Independent scientific acceptance remains pending.
