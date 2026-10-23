# R19-B1 G3 authorized successor — execution summary

Status: `G3_COMPLETED`; `G4_NOT_RUN` (explicitly outside this release).

## Execution identity

- Scientific checkout: `/home/lizening/wt-r19-recovery-duration-v1`, detached clean source `2da980f631badc25086d12db60d128ff507d3ae6`.
- Supervisor run ID: `260422ac02bd42a8b2929d7ef240526b`; supervisor PID `780643`; child PID `780645`.
- Real runner exit: `0` (`subprocess.returncode`); supervisor status `completed`; not interrupted; artifacts complete.
- Successor of failed run `3d1ccea7e97f4727abf8e216ac6ec498`; no retry, second launch, G2 rerun, or G4 invocation.
- Output: `/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z`.
- Supervisor evidence: `supervisor_live/`; selected safe evidence is copied unchanged under `evidence/`.
- Exact child argv hash `93aa3a833fbb65241fcab6b7e68d3863fa83985084d9c1b27875c730285f55ef`; supervisor argv hash `c2270f4e43d88d53022b38bc4bc0e1890bc49b738387f99485045fd9020e450a`.
- Gate SHA256 `c285692615eaaf1c7cb7139b0417528022db6ee03c510de13f881d126f14415e`; G2 execution SHA `92aae1d9b230cc212c6ec4effc99aa468941e69d`; scientific source stayed at the reviewed SHA.
- Authorization, independent clearance, drift check, and exact proposal/review remain immutable records in the Sol clearance/review directories; see `evidence_inventory.json`.

## First-source restart contract

The production comparison is `PASS`. At schedule index 0 / seed 30000, expected and observed restart snapshot SHA256 both equal `d85d870bfddbad4eb62116d3d5de54a4b7fd4f250634af1c1ed89958e4c400b8`. Comparison occurred before the first environment action; no environment action preceded the comparison. The first source episode completed and its registry unit is completed. The predecessor run remains preserved and is linked as the superseded run; its historical failed unit/evidence was not rewritten.

## Bounded pilot execution counts (operational, not G4 outcome analysis)

- Frozen TRAIN source schedule: 127 scheduled and 127 completed; held-out tasks 0; training runs 0; external paid model calls 0.
- Initial attempts: 39 of the 120 cap. Eligible states: 36 of the 60 cap (failure 6, success-control 15, random-control 15). The failure queue exhausted at 7 candidates. No quota transfer, backfill, or expansion occurred.
- Formal recovery branches: 39; validated K arms: 183, spanning K=1..5 under the frozen horizon. The production branch/source validators bind all 12,741 operation events (4,219 source-bound and 9,424 branch-bound); no operation was left unbound.
- G3 physical ledger: 4,965 completed model generations; 7,273 non-reset environment operations plus 334 resets = 7,607 environment operations; 0 incomplete operations. Input tokens 3,098,660; generated tokens 25,817; total 3,124,477.
- By phase, model generations/calls: initial recovery 78; path extension 133; source 2,046; suffix 2,708. Environment actions: initial attempt 36; logical branch 4,701; path extension 133; replay gate 357; source 2,046. Resets are additional and included in the physical operation total.
- Cumulative including the previously audited baseline 177 generations / 342 environment operations: 5,142 generations and 7,949 environment operations (7,603 non-reset operations + 346 resets). These are physical expenditure counts, not per-policy logical costs.
- Phase limits remained intact: source 2,046 generations / 2,173 operations against 8,999/8,999; initial recovery 78 against 240 calls; path extension 133/133 against 240 calls/2,940 operations; suffix 2,708 against 17,100 calls; initial-attempt operations 36/5,520; logical-branch operations 4,869/18,000; replay-gate operations 396/5,400. No automatic retry or quota expansion.

These are execution and integrity counts only. No K-specific success/cost estimates, paired statistics, best-fixed-K selection, hindsight analysis, passive-stopping analysis, or G4 report was run or inferred here.

## Offline checks and preserved payload policy

The pinned production `analyze_r19_recovery_duration` validators were run read-only against the completed authentic live files. Event-ledger validation, branch validation, frozen source-schedule binding, and the first-source restart comparison all returned PASS; exact compact results are in `offline_validation.json`. Runner/supervisor receipts, execution manifest, branches, registry, runtime/gate receipts, source comparison, and runner log are preserved in `evidence/`.

The raw event ledger (187,978,473 bytes) and source trajectories (19,726,633 bytes) remain in the scientific output directory and were not uploaded: the event ledger exceeds the protocol's 50 MB ceiling; trajectories exceed 10 MB and contain task-level observation/action payload. Their exact hashes, sizes, paths, and omission reasons are recorded in `evidence_inventory.json`. No weights, adapters, cache, or dataset payload were uploaded. The 1.48 MB branch record was inspected and copied unchanged as bounded scientific provenance; it contains identifiers, outcome/cost fields and event hashes, not raw observation transcripts.

No scientific source, test, protocol, frozen input, prior G2 evidence, predecessor output, or historical clearance/review record was modified. No scientific code or configuration changes were made.
