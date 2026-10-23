# Independent result — sole authorized R19 G3 successor

**Observed: G3 completed with authentic child exit 0; G4 was not run and is blocked.** This is an execution and evidence-integrity decision, not a K-specific scientific result or a full G4 acceptance.

The only invocation under clearance `1702806e11d0f4efa9933de7dcc7c353f5220b43b135ab4768bb6cfd81612232` was run `260422ac02bd42a8b2929d7ef240526b` at clean scientific source `2da980f631badc25086d12db60d128ff507d3ae6`. Supervisor status is completed, returncode source is subprocess.returncode, and the clearance is consumed. There was no retry, G2 rerun, training, held-out execution, scientific edit, G4 statistics or report invocation.

## What was genuinely completed and checked

The genuine event ledger, branch records and frozen source schedule were checked with production validators, independently of Luna's summary. All 127 TRAIN source episodes completed; 39 initial attempts produced 36 eligible states (failure 6, success-control 15, random-control 15), 39 formal branch rows and 183 completed K-arm records. All 385 new registry units are completed. All 12,741 physical operation completion events are bound: 4,219 to sources and 9,424 to branches. Source digests, action/parser/event identities and branch integrity passed. The exact first-source snapshot comparison passed **before its first environment action** with expected/observed SHA256 `d85d870bfddbad4eb62116d3d5de54a4b7fd4f250634af1c1ed89958e4c400b8`.

The failure candidate queue contained 7 candidates and yielded 6 eligible, below frozen failure quota 30; the other strata reached 15 each. Total enrollment is 36 rather than the planned maximum 60. No backfill, quota transfer, resampling, schedule expansion or additional run was used. This is a sample limitation to retain in any later authorized analysis, not permission to manufacture a full cohort.

All frozen phase/global caps were respected. Original failed predecessor evidence/registry/manifest and authentic G2 evidence remained unchanged; the old failed source is not relabeled as a completed or task-failed episode.

## Final physical costs and explicit monitor correction

G3 added **4,965 model generations**, **7,273 non-reset environment operations +334 resets =7,607 environment operations**, with zero incomplete external operations. Historical 177 generations /342 operations remains fully charged. Cumulative: **5,142 generations; 7,603 non-reset operations +346 resets =7,949 operations**, zero incomplete external operations. Logical per-K costs are not substituted for this physical expenditure.

My incremental monitor had displayed 8,118 environment operations because it counted 169 recovery transition wrappers in addition to their already-recorded physical API operations. Each wrapper was independently linked to its actual operation event. Production physical-ledger validation and runtime phase counters agree on 7,949. Earlier monitor observations/state and raw scientific ledger remain preserved; `monitor_display_cost_correction.json` documents the correction. It removes duplicate display counting, not actual expenditure.

## Two confirmed G4 acceptance blockers — unrepaired

1. Runtime producer `scripts/run_r19_experiment.py:937` emits the frozen nested `r19_inference_runtime_manifest_v2`. G4 consumer `scripts/analyze_r19_recovery_duration.py:1517` requires flat v1 fields and rejects this genuine manifest. The tracked rejection predicate was evaluated read-only on actual raw v2; no runtime normalization or report was used. Frozen nested local-only/offline/model bindings independently match; this is a consumer contract gap, not observed runtime drift.
2. `validate_live_exit_receipt`, `scripts/analyze_r19_recovery_duration.py:2014`, requires a `run_started` ledger envelope the actual producer did not emit. Authentic receipt/status/context/argv/log/hash checks reached this final check successfully, then production validation rejected the absent envelope. **This does not change authentic runner returncode 0.** No fake event was appended and no raw manifest/ledger was edited.

The initial `final_g3_integrity_audit.json` review-required status and failed exit-consumer check remain unmodified. This final addendum makes the distinction explicit: genuine successful G3 completion and source/branch/physical-budget checks passed; formal G4 consumer acceptance has not passed. Prior synthetic source-to-report coverage did not test the actual runtime metadata/start-envelope contract and cannot establish a live G4 PASS. Historical review records remain immutable; these concrete coverage gaps are now recorded.

## Complete raw upload independently verified

Luna published a lossless complete-output/supervisor archive at provenance commit `f384514036c8267ef4f7f49d89d249a5dc6009ea`. Archive `agent-logs/2026-10-23T024938Z__LUNA__r19-g3-raw-upload__2da980f/r19_g3_complete_evidence.tar.gz` is 18,545,447 bytes; SHA256 `c7b09370e7b7625d60ad257a4a4cfe023cceb5a47f48d1f660b2ae36fd5c808f`. I read the actual remote Git archive bytes, decompressed all 15 regular-file members without executing them, and checked every member's size/SHA256 against original local files and the inventory. All 10 files in the original scientific output tree are included, alongside the authentic supervisor context/status/exit/log and launcher output. Original source hashes before/after agree. Dataset inputs, weights, adapters, cache and credentials are excluded. The earlier compact record's local-only raw omission was true at that earlier checkpoint and is superseded by the later upload, without historical edits.

Raw ledger SHA256 `05e1d443ff304eaa25d08b92a4e19d204a6c93a4f46bbe50aefef3271f211762`; source trajectories SHA256 `c6f37a7da28e326c70818524c79c17bbd85a286754c111f17db07cbe151a4f1c`; authentic runner exit SHA256 `015fe2296f5dce979d6e9db2a17dc03d217958620dd13a29a73b256d56cb144b`.

**HOLD after evidence delivery.** No G4, retry or new scientific process is authorized. Future offline consumer repair/independent exact-SHA review/G4 authorization must be separate; genuine G3 data remain immutable and should not be rerun to repair an analyzer contract.
