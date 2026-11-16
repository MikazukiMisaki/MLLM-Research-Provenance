# Append-only metadata checksum correction

This note supersedes only the metadata digest entries in initial publication commit bdd42ee01e153838c17b3c5f423e4c83d26ccff0. That commit's package and report payloads remain unchanged and are retained in history.

A defect in the in-memory SHA-256 helper used while preparing several metadata digests omitted round constant efbe4786. The affected metadata digest values below were therefore not valid SHA-256 digests. The original file contents were not corrupt: their Git blob IDs match the objects created from the prepared bytes. A verified SHA-256 implementation was checked against the standard empty-string and hello test vectors and applied to the exact remote UTF-8 contents. All 21 allowlisted package/report payload files independently match their source SHA-256 values and returned Git blob IDs.

| Metadata path | Initially recorded digest | SHA-256 of original remote bytes |
|---|---|---|
| agent-logs/20261116T120407Z__LUNA__parallel-research-github-sync__r9m2/RECORD.md | d8494ba60b7ab568da0edc6f138f9e30e260d7dfb81148dab92cac5132e565d2 | 2d734955f816950d4493f14a8903a2f47716cd7bcc9cfd2b9d0e6cea83162a4d |
| agent-logs/20261116T120407Z__LUNA__parallel-research-github-sync__r9m2/commands.log | 4ff0516807c400cbe5a1377daa999a6b5f44d97de0339eae2d40eeb2570db0f5 | 0e56828b894ddd625f97b3af1ff5bb140af1c317fc5f63fd42e6dad8f127ed83 |
| agent-logs/20261116T120407Z__LUNA__parallel-research-github-sync__r9m2/PUBLICATION_MANIFEST.json (initial version) | 8d5f5acb91cf4624d4d4f70123c549d8aa74e0bfc08592db82592735d7bab7a7 | 0b0fe96aebb7214f086440b46ade1c567a52b2386fd46451d01a7f37409d134f |
| agent-logs/20261116T120407Z__LUNA__parallel-research-github-sync__r9m2/FILE_HASHES.sha256 (initial version) | f876322610f0605838a6863d5594c0a4b3ccf118541a28080ca0f57664df95ad | 2977d1cc324ce6bd7df9e9747931e022c07e75c864d33de8522eaf0fbb8efa44 |

The initial INDEX.md digest was correct; its content is now updated only to link this note, so the new digest is recorded in the corrected root inventory. The corrected PUBLICATION_MANIFEST.json and both corrected FILE_HASHES.sha256 inventories are written in this follow-up commit. The corrected manifest records the valid RECORD.md and commands.log hashes and links to this note.

The package payload bytes, source manifests, boundary report, scientific contents, and experiment records were not modified or regenerated. No model, tokenizer, training, ALFWorld, or environment operation occurred during this correction.
