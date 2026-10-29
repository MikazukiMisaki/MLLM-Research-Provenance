# ALFWorld missing game source audit — metadata only

Scope: identify the provenance and meaning of missing game files without loading task contents, running ALFWorld, executing model/CUDA, downloading task archives, or generating games. Counts are by on-disk `split/<parent>/trial_*` directories, not by unique scenes or parent tasks. `AUDIT.py` is the read-only metadata recount; `AUDIT.json` captures raw results and upstream release-asset metadata. No task identities or trajectories are printed.

## Observations

| Split | Trial directories | `traj_data.json` | `initial_state.pddl` | `game.tw-pddl` | Game absent |
|---|---:|---:|---:|---:|---:|
| train | 6,374 | 6,374 | 6,374 | 3,553 | 2,821 |
| valid_seen | 251 | 251 | 251 | 140 | 111 |
| valid_train | 200 | 200 | 200 | 200 | 0 |
| valid_unseen | 255 | 255 | 255 | 134 | 121 |
| Total | 7,080 | 7,080 | 7,080 | 4,027 | 3,053 |

All 3,053 missing-game directories have both remaining named inputs. This is a file-presence observation only: it neither establishes that any absent game is constructible or executable nor that a generated game is faithful. It does not imply 3,053 new independent tasks. Official upstream documentation describes 3,553 training, 140 seen and 134 unseen games, exactly the local split counts (it does not provide the above full cross-split identity comparison). The project's [issue #129](https://github.com/alfworld/alfworld/issues/129) contains an independent 7,080-PDDL/4,027-game download log; a project collaborator states that not every ALFRED game can be played in text. This is evidence that the installed pattern is consistent with the official subset and is not enough to classify the 3,053 absent games as corruption. It is not proof of the specific reason for every absence, nor a full byte/member verification.

Installed `alfworld` distribution reports 0.4.2, `textworld` 1.7.0. The installed downloader and official tag 0.4.2 downloader differ only in the first (interpreter) line. It points to official release 0.2.2 JSON/PDDL zips and 0.4.0 `json_2.1.2_tw-pddl.zip`, despite extraction under `json_2.1.1`. Downloader skips existing files unless forced; therefore current files cannot be attributed to a single download based on script identity. Official metadata also lists earlier 0.2.2 text-game archives; the larger compressed size does not prove more games, equivalent gameplay, or suitability. GitHub release-asset API reports `digest: null` for all listed archives, so no trusted official SHA-256 was established. No archive or archive member was downloaded, and the found file counts cannot substitute for asset/member hashes.

Bounded filename search under `/home/lizening` to depth 5, plus `/home/lizening/.cache`, `/home/lizening/alfworld_data` and `/tmp` to depth 5 found no exact named release archives. It does not establish absence elsewhere. `pip show` reports MIT software licensing; upstream [issue #132](https://github.com/alfworld/alfworld/issues/132) asks for explicit terms covering archive data and has no maintainer clarification visible in the checked issue. This is an unresolved attribution/terms question, not a legal conclusion or a prohibition on academic use.

## Provenance-conservative follow-up, not a new protocol or authorization

1. Obtain evidence of the installed dataset's actual prior acquisition/version, local historical install logs, and archive location; snapshot read-only file manifests and compare all installed member bytes to a trusted official archive if the latter can be accessed in a separate staging location with its terms understood. Record actual archive SHA and authenticated release metadata; never replace current data. Exact metadata count alone is insufficient.
2. Compare identities and hashes of any official additional game members across the old and current releases, then evaluate title/split/parent/scene, all historical task exposure and other duplication at a prespecified level without inspecting outcomes. A game missing from one archive may still be missing in all official releases.
3. Upstream [generation documentation](https://github.com/alfworld/alfworld/blob/master/alfworld/data/README.md) and [generator source](https://github.com/alfworld/alfworld/blob/master/scripts/alfworld-generate) describe creation and expert solvability checks. A newly generated file is a new artifact, not automatically byte-identical to an old frozen file or the same experimental treatment; version, domain, grammar, seed, generation behavior, and solvability must be recorded. No automatic reclassification as held-out or recovered original is justified. Any generation/expert execution would need a separately reviewed scope; none occurred here.
4. After authoritative file/member evidence, independently redo historical-exposure exclusion and quantify distinct parents/layouts rather than simply counting trials. Unknown training pre-exposure and incomplete historical records remain limitations. Only then evaluate statistical sufficiency and budget; do not select or remove examples according to observed outcomes.
