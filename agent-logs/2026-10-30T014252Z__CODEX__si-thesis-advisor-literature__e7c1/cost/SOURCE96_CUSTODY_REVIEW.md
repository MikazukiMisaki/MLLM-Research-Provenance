# SI source96 original journal — read-only custody audit

**Decision: a byte-equivalent persistent local archive is verified; current remote Git object identity matches, but a fresh remote full-content SHA-256 check was unavailable.** This corrects the impression that the only known source96 journal is the `/tmp` copy; it does not claim independent backup redundancy or guaranteed long-term retention.

## Persistent local copy

The running source log under `/tmp` is 474,180,490 bytes with SHA-256 `04ce4c0f32f40a3dbff6f42fec3c54107534ec45dd005795bd52014442513105`. The local research-notes archive `/home/lizening/research-notes/agent-logs/2026-10-27T010146Z__SOL__si-s01-independent-result-review__f96b86f3_b3657dbd/si_s01_source_f96b86f3_evidence.tar.gz` is 17,608,129 bytes, SHA-256 `474a9264bc483b2c641842478f5dcd8287e8d01a60a764c8dd84d892a922ef0a`. I streamed, without extracting to disk, exactly one regular tar member `run/raw/source_events.jsonl` through SHA-256: its 474,180,490 bytes have the **same** `04ce4c…` SHA-256 as the current `/tmp` journal. Both source and archive hashes were rechecked after this comparison. The complete member is recoverable from this local archive even if the temporary journal is removed, subject to the filesystem and archive remaining available.

The local Git object at provenance commit `adac6a5c5721ede3ebf896240d7d70af73a24c67` for that archive has blob ID `50dfc19f76b763357bcb7db7dc0d3f8a1a9e386c`. A full `git cat-file blob` byte stream was independently SHA-256 hashed and matched the 17,608,129-byte local archive `474a9264…`. The working file and Git object are on the same local filesystem; they are not two independent disaster-recovery copies. `LOCAL_CUSTODY.json` and `check_local_custody.py` contain these aggregate observations and bindings only.

## Remote metadata and its limit

A live read-only GitHub connector request for the same path on remote `main` returned the same blob ID `50dfc19f76b763357bcb7db7dc0d3f8a1a9e386c`. The repository metadata currently reports visibility `private`. The connector response for this 17.6 MB object returned an empty content field, so this task **did not** retrieve the remote archive body, compute its remote SHA-256, or independently stream-decompress the remote member. Matching the remote Git object ID is useful content-addressed metadata, not a fresh independent full-byte retrieval. `REMOTE_METADATA.json` records the limited observed connector result.

An earlier publication receipt `/home/lizening/research-notes/agent-logs/2026-10-27T010146Z__SOL__si-s01-independent-result-review__f96b86f3_b3657dbd/post-push-receipt.json` reports a full remote object match at publication commit `adac6a5c…`. That is historical supporting evidence, not a substitute for a fresh full-content recheck here. The archive contains private task/model interaction data and must remain within the project's authorized private-access boundary.

## Remaining retention gap and safe handling

There is no longer a demonstrated **local-only-in-/tmp** gap for this journal. What remains unverified is a fresh remote full-byte restore and the resilience of any independent off-host copy. Preserve the existing local archive and its Git object through ordinary cleanup, retain the recorded hashes and private access control, and use an authorized private channel capable of retrieving the full remote blob to verify its SHA-256 and streamed member hash when such access is available. A separately managed private backup on independent storage would reduce single-filesystem risk; any such copy should be byte-verified and handled as sensitive research evidence. Do not publish or upload the original raw task content as part of this audit, overwrite existing evidence, or treat a metadata-only Git object match as a completed restore test.

No new copy or upload, scientific worktree change, model, CUDA, ALFWorld, analysis runner or experiment was performed. The report and machine receipts contain only paths, hashes, sizes and verification states, not task data.
