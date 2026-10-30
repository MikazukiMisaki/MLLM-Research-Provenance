# Independent custody review: SI source96 original event journal

**Decision: ACCEPT_LOCAL_ARCHIVE_AND_GIT_OBJECT; REMOTE_METADATA_MATCH_ONLY.** This review applies to `2026-10-30T063500Z__SOL__si-source96-custody-audit__8be2/CUSTODY_REVIEW.md`, SHA-256 `fa4bb65ad2f1fe302ed0b93a41117a3823861cdf129e35dcfee992656c01cac8`. The checked record is no longer supported solely by its temporary journal copy; independent off-host restore and long-term durability are not established.

## Independently verified local evidence

An independent streaming script read the `/tmp` journal, the stored `.tar.gz`, the unique regular tar member `run/raw/source_events.jsonl`, and the Git object without writing a copy or displaying task content. The journal and uncompressed member are both 474,180,490 bytes and have SHA-256 `04ce4c0f32f40a3dbff6f42fec3c54107534ec45dd005795bd52014442513105`. The 17,608,129-byte archive has SHA-256 `474a9264bc483b2c641842478f5dcd8287e8d01a60a764c8dd84d892a922ef0a` before and after the comparison.

I independently calculated the Git blob ID from the archive's bytes plus Git's object header: `50dfc19f76b763357bcb7db7dc0d3f8a1a9e386c`. Commit `adac6a5c5721ede3ebf896240d7d70af73a24c67` maps the expected archive path to that object; a complete local `git cat-file blob` stream produces the archive's SHA-256 and length. The original source journal and archive hashes also match after the checks. `INDEPENDENT_LOCAL_CUSTODY.json` records only aggregate identifiers, sizes and hashes; no raw evidence is duplicated into this review directory.

The archive and Git object are both on the same checked local filesystem. The tar member's SHA identity is strong evidence of preserved bytes in that archive; it does not prove the archive will remain indefinitely available, or that source runs were scientifically correct. This review covers the named journal member, not an independent examination of every other archive member.

## Remote information and historical receipt

A fresh read-only GitHub connector metadata request for the archive path on `MikazukiMisaki/MLLM-Research-Provenance` `main` returned blob ID `50dfc19f76b763357bcb7db7dc0d3f8a1a9e386c`, equal to the local Git blob; a separate repository metadata query reported `visibility=private`. The requested response used base64 encoding with `content` length 0. Thus the present check **did not** receive the 17.6 MB remote body, stream or hash the remote object, restore it, or prove an independent remote copy's resilience. The live observation is captured in `INDEPENDENT_REMOTE_METADATA.json`; another channel could have different capabilities, but no such fresh retrieval was made in this task.

The existing Oct 27 publication receipt for commit `adac6a5c...` reports a full remote object match for the archive and the same archive SHA; I checked the exact receipt entry. That is historical supporting evidence recorded by that publication workflow, not a fresh remote restore or an independently reproduced proof of the full remote content now.

## Consequence and limits

The earlier resource audit's narrow uncertainty—whether a durable local archive existed beyond the `/tmp` copy—is resolved by the byte-matching archive and local Git object. The broader retention question is not resolved: these are not demonstrated independent disaster-recovery copies, and remote full-byte verification remains pending. The original journal contains private task/model data, and the linked provenance repository is private; no original raw file was copied, uploaded or sent. The remote query was metadata-only.

No model, CUDA, ALFWorld, scientific analyzer, task generation, inference, or experiment ran. Neither the original custody report, the original source journal, the archive, the Git repository index nor any scientific files were changed.
