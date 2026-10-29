# Official ALFWorld game archive metadata audit

Status: **read-only metadata and hash evidence, not task approval or a runnable dataset**. Three official release assets were downloaded directly over HTTPS into an isolated `/tmp/si-official-archive-audit-20261029/` directory. No archive was extracted into the dataset and no model or environment was started. The checker reads game bytes only to calculate digests and verify ZIP CRC; it does not print or copy member contents, task identities, or task results. Task identity sets remain transient in memory. SHA-256 fingerprints identify the bytes actually downloaded; GitHub's asset API exposes `digest: null`, so these hashes are not independent official checksum verification. HTTPS and the release asset URL establish the observed source, not the training history of any task.

## Source and exact assets

The official release API metadata, asset URLs, sizes, IDs and timestamps are recorded in `OFFICIAL_RELEASE_METADATA.json`; source pages: https://github.com/alfworld/alfworld/releases/tag/0.2.2 and https://github.com/alfworld/alfworld/releases/tag/0.4.0. Important: release-tag age is not asset immutability. The 0.2.2 current asset reports a 2024 upload, and its alternative `.old.zip` reports earlier creation and a 2024 update.

| Asset | Bytes | Downloaded archive SHA-256 | Game members |
|---|---:|---|---:|
| 0.2.2 `json_2.1.1_tw-pddl.zip` | 45,059,629 | `d376c4bbb097c068528a2a9805e358e4cd14bc75c4d68a24e5141aebd234ef67` | 5,234 |
| 0.2.2 `json_2.1.1_tw-pddl.zip.old.zip` | 45,060,177 | `2259f0ce8ad460ff9ee11f5edbbd4830b8685618b80e3400031797395871647d` | 5,234 |
| 0.4.0 `json_2.1.2_tw-pddl.zip` | 36,493,542 | `eea90499df27b9cb3147d1d1927264146d38194b575e25f70a82875545742dcb` | 4,027 |

Despite the 0.4.0 asset's `2.1.2` filename, its member paths begin `json_2.1.1/`. Every file has the expected split/parent/trial/game path schema; no duplicate member paths were found. The two 0.2.2 assets have the same 5,234 paths and 5,233 matching member hashes; one shared path differs. The older package is therefore not interchangeable even with its same-release sibling.

The 0.4.0 package exactly equals the full set of local `json_2.1.1/*/*/*/game.tw-pddl` paths: 4,027 on each side, no members local-only or archive-only, and every corresponding game hash matches. The 0.2.2 standard asset contains all 4,027 paths, but every shared game hash differs from the installed 0.4.0 game. Its remaining 1,207 game paths lack local game files while their matching trajectory metadata files exist: 1,099 TRAIN trials across 521 parent directories, 47 valid_seen trials across 45 parent directories, and 61 valid_unseen trials across 25 parent directories. These parent totals are per split and have not been deduplicated across splits or against history. Four of the 61 valid_unseen trials have a two-object family prefix, which is not a claim about distinct parents or usability.

## Compatibility, selection and science limits

The official [0.4.0 release](https://github.com/alfworld/alfworld/releases/tag/0.4.0) cites [PR #94](https://github.com/alfworld/alfworld/pull/94), which describes changed action terminology and feedback and an accompanying script to update old games. This directly motivates a version-compatibility concern; this audit did not run that script, inspect candidate game semantics, compare execution behavior, or establish equivalence. In particular, differing hashes do not by themselves identify a semantic difference for every member, nor do absent 0.4.0 members prove that historical ones are solvable. Historical data exposure, file-byte aliases, parent and scene isolation, conditions of removal, license compatibility for redistribution, and complete task registry remain unresolved. These archives cannot be silently mixed into the frozen runtime, treated as new certified held-out tasks, or counted as a new experimental sample on this evidence.

`audit_archives.py` performs the reproducible aggregate comparison; `ARCHIVE_METADATA_AUDIT.json` contains counts, hashes, and size ranges but no task identifiers. The extra reverse local-set count was independently checked read-only: local 4,027, 0.4.0 4,027, intersection 4,027, local-only 0, archive-only 0. Source and output are local evidence awaiting independent review and coordinator publication.
