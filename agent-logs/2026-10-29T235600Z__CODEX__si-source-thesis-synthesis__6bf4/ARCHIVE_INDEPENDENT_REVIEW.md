# Independent audit of official archive inventory and historical joins

## Scope

Independent read-only implementation re-opened the three already downloaded ZIPs in `/tmp/si-official-archive-audit-20261029`, streamed all game members solely into SHA256 computation/ZIP CRC checking, checked the existing game files by path and hash, and independently rejoined protected task/parent identities and existing byte hashes. No member contents, private task IDs or outcomes were emitted; no model, CUDA, ALFWorld, extraction, generation or selection took place. Archive and input file hashes were compared before/after. `recheck.py`, `RESULT.json`, `history_recheck.py`, `HISTORY_RESULT.json`, and `COMPARE.json` are the exact audit code/output and aggregate comparison; a first draft of `recheck.py` had a Python syntax error and no byte operations before correction.

## Archive identity comparison

- Existing 0.4.0 archive SHA256 `eea90499df27b9cb3147d1d1927264146d38194b575e25f70a82875545742dcb`: 4,027 game members, zero duplicate/unexpected member files. Current local inventory is also 4,027, identical member paths, and each of 4,027 member digests matches its local counterpart.
- 0.2.2 archive SHA256 `d376c4bbb097c068528a2a9805e358e4cd14bc75c4d68a24e5141aebd234ef67`: 5,234 members, including all 4,027 current paths with **different** per-member SHA256, plus 1,207 paths not in 0.4.0: 1,099 TRAIN, 47 valid_seen and 61 valid_unseen. All 1,207 lack local games but have a local trajectory metadata file. Local parent totals by split are 521, 45 and 25 respectively; they cannot be added as distinct parents without a union check.
- 0.2.2-old SHA256 `2259f0ce8ad460ff9ee11f5edbbd4830b8685618b80e3400031797395871647d`: same 5,234 paths as 0.2.2, 5,233 byte-identical members and 1 differing member.
- Observed hashes are fingerprints of files already downloaded from the official release URL; the release API provides no authoritative asset digest. This confirms reproducibility of the file bytes checked, not a signed/official checksum or proof of past local installation events.

## Independently reproduced history/exclusion join

The inputs include checked historical registry, full balanced expert rows, initial and extension SFT candidate manifests, G1 schedule, authentic SI-U1 82-task schedule and byte bindings, B/C training parent manifests, two engineering probe identities, and, separately, the full prior proposed reservation. Exclusion is conservative by exact ID and parent, and against the available frozen game/trajectory hashes. All game and trajectory files for excluded parent folders, and matching older-archive game members for protected parents, were additionally compared. The cross-version change means a different game hash does **not** prove a different task or layout; task/parent and trajectory checks remain essential and still do not prove unrecorded history or semantic/layout separation.

| Policy | Old-only rows | Old-only distinct parents | Existing parents | Parent overlap | Union distinct parents |
|---|---:|---:|---:|---:|---:|
| Checked history plus all initial/extension SFT manifest parents | 960 | 353 | 35 | 9 | 379 |
| Plus protection for all earlier proposed/reserved parents | 950 | 345 | 6 | 1 | 350 |

For valid_unseen alone, both policies give 54 old-only rows over 19 parents; one of the 19 overlaps the 6 existing parents, producing 24 distinct parents in the union. Old-only and local candidate game-byte or trajectory-byte overlap was zero under these two exact-byte comparisons, not proof of semantic novelty. All 950/960 accepted archive hashes and matched trajectory hashes were distinct within the respective sets. `COMPARE.json` confirms every comparison field and split/family count matches the other audit (`ALL_AGGREGATE_FIELDS_MATCH`).

The 350 protected-policy union is an identity-level **upper bound under these checks**, not a runnable, statistically independent, held-out, or approved evaluation pool. The earlier reservation remains protected; the 379 sensitivity union does not silently remove that protection. Historical planned SFT task entries were excluded even where an individual replay receipt is unavailable. The current engineering and frozen evaluation use 0.4 games; it is not known whether a 0.2 extra game works with that runtime or has scientifically equivalent action/observation behavior. [Official ALFWorld PR 94](https://github.com/alfworld/alfworld/pull/94) explicitly describes a command terminology/feedback change and an old-game patch script, further motivating a compatibility review. This review did not run the patch or any environment. License/redistribution terms for task archives and complete historical exposure remain unresolved. Any future archived-game use needs independently reviewed, separate version/compatibility treatment, identity and layout/history audit, statistical plan and budget; no new evaluation is implied here.
