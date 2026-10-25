# SI-P0 identity-availability metadata addendum

Status: bounded, read-only directory-name and consumed-registration inventory. No experiment, schedule, or new held-out authorization is created. This is an additive record; prior SI-P0 files remain unchanged.

## Directory inventory and known-set difference

Only immediate directory names under the installed `json_2.1.1/{train,valid_seen,valid_unseen}` tree were read. Canonical episode identity is the normalized relative `task_directory/trial_directory` string. No `traj_data.json`, `game.tw-pddl`, trajectory, outcome, or unconsumed task payload was opened by the final audit script.

| Split | Task directories | Task/trial directory identities | Matched known used/exclusion identities | Known-unlisted candidates |
|---|---:|---:|---:|---:|
| train | 2,435 | 6,374 | 2,412 | 3,962 |
| valid_seen | 242 | 251 | 140 | 111 |
| valid_unseen | 85 | 255 | 60 | 195 |

The candidate IDs and per-ID SHA-256 values are in `AVAILABLE_IDENTITY_CANDIDATES.json`. The split directory identity inventories have zero cross-split task/trial overlaps. Candidate identity sets also have zero cross-split overlap.

These counts are **known-set differences only**. The global historical consumption/visibility register is not proven complete. Therefore none of the 3,962 / 111 / 195 candidates is certified clean, unseen, or held out; the figures do not establish statistical power or authorize future sampling. Exact task-level exclusions, where present without a trial suffix, were conservatively applied to all trial identities beneath that task.

## Previously consumed / excluded identity metadata

- The accepted SFT index binds 1,074 expert-training, 126 offline-validation, and 60 online-development task/trial identities (input SHA `9c374fafdcc7d7db77e878d23e852a0ec55eedcc3886cb0cebe7491d67e564e5`).
- The held-out exclusion register contains 1,406 identities across its categories (SHA `badff9aec90bc21828b8b5ae92eb254c66f50aacc1dfc16bbcbe15e6f038b419`). Its exact intersection with installed `valid_seen` is 140; all remain used/excluded, not newly available.
- The frozen G1 `valid_unseen` schedule contains 60 consumed identities (SHA `7ce71ad01bd03ad8a018104f3edacc4310e9a1b5fc6e015d808152f316e4e13e`). Those 60 remain used; the remaining 195 directory identities are only candidate differences, not clean held-out.
- Recovery exclusion registrations include the R6/R7 source-pool/Sprint-2C, R8, R9, R10, R11/R11a, R12, and prior-recovery categories. The machine result records exact category counts, intersections, and source-file hashes.
- R4's consumed run manifest records 24 completed prefix IDs, but this metadata-only pass did not resolve those prefix IDs to extra task/trial IDs.
- R14's completed run manifest records 180 task/trial schedule positions (manifest SHA `2216eaaec2a268e4f54bc0322098d5d4d080517691dc41a83bddac4715737043`). R15/R16/R17 manifests record 60 prefix IDs each; these prefix IDs are not counted as extra episodes, and their exact task mapping was not reconstructed from outcome-bearing files. R18 C1/C2 manifests record 60 prefixes and zero held-out consumption but expose no canonical task/trial list in those manifests; exact round-specific identity mapping remains incomplete.
- R19's completed `unit_registry.json` (SHA `c3898492c1fe542d60ea7c9f9363f48e352058f2b7ee86c812b54ef4e18f0cc8`) registers 127 unique `source_episode` canonical task/trial IDs. Its 36 `recovery_path_extension` units and 39 prefix-replay/recovery units are lower-level units, not additional source episodes; they are not added to the 127 source identities.

The R1 SFT recovery, persistent-recovery, and progress-aware source schedules are marked `frozen_unexecuted`; they were not treated as evidence that their selected identities were consumed. All input paths, sizes, and raw SHA-256 hashes used by this inventory are listed in `AVAILABLE_IDENTITY_AUDIT.json`.

## Scope caveat

During preparation, a broad text search briefly printed two rows from already-consumed R16/R17 pair-result CSVs, including outcome columns. No unconsumed task result or payload was opened, and those values were not used in this inventory. The final audit script reads only task/trial directory names and the allowlisted identity, schedule, exclusion, and consumed-registration JSON metadata. This deviation is preserved in the machine record rather than hidden.

No schedule/argv was generated; no outcome, model, environment, project analyzer/validator, pytest, replay, or training operation was run. The entire activity was read-only except new Luna-owned addendum outputs in this directory.

