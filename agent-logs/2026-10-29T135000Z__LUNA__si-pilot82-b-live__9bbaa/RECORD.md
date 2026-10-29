# SI-U1 B arm: completed training, independent review pending

Status: **OBSERVED_COMPLETED_AWAIT_INDEPENDENT_REVIEW**. The one cleared B training run `064d0c7f39f14414acf24f399188f85f` on source `9bbaa12c2d8177a60ec5a74ed2f970ef29a57bce` completed and the actual supervisor worker and launcher returned 0. There was no timeout or supervisor error, and process cleanup was established. The run was not retried and did not start C or evaluation.

The real result reports 78 optimizer steps, 1,248 completed microbatches, 661,620 input tokens and 6,240 supervised tokens. A separate local reconciliation matched all 1,248 sample IDs to the frozen order, all 78 learning rates to the frozen protocol, finite losses, the supervisor result hash, and every resource record. No allocator OOM or allocation retry was observed. This is evidence of the completed training procedure; it is not a success-rate result.

The B final adapter tree SHA256 is `9d8ce785c635db80ddd17999a981f0cee478ccf92d0aeb12eb7812978e441a36`. Its files remain at the original output path and are not included in the log archive. The original base and P0 model tree hashes remained unchanged. C must start from the original P0, not B's adapter.

The actual supervisor allocation was 883.2235775915906 seconds, or 0.2453398826643307 device-hours, within the 5,400-second B cap. Earlier engineering expenditure is separately accounted and not added to overlapping timers. Device-wide readings returned to the 14 MiB baseline after exit; they do not establish process ownership.

`B_RUN_AUDIT.json` SHA256 `35129a247c9eae7992af7867e4fe40f3500649e3dff940fe3cd0a04b49421391` contains the local reconciliation and adapter file hashes. `B_RAW_EVIDENCE_PRIVATE.tar.gz` SHA256 `98d4c09f24cf9278dfaa66fd9f7f01da36458792a7c983f85eee4b2531d8d4bd` contains 27 raw log and authority members; each was byte-verified against original files and original pre/post hashes matched. It excludes adapter weights and contains private training metadata; keep it private.

Astra's separate independent B audit is required before any C preflight or execution. This record alone is not that audit. No shared index or prior evidence was modified.
