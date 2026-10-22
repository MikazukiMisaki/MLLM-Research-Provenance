# R19 source-contract implementation handoff

Status: READY_FOR_INDEPENDENT_EXACT_SHA_REVIEW_SOFTWARE_ONLY. No independent implementation PASS, G2 carry-forward acceptance, positive preflight release, launch clearance, or new scientific execution authorization is claimed.

## Frozen candidate

- Scientific repository: MikazukiMisaki/Alfworld-Self-Improvement-Project.
- Own worktree: `/home/lizening/wt-r19-source-contract-review-fixes`.
- Branch / verified remote ref: `codex/r19-source-contract-review-fixes` / `refs/heads/codex/r19-source-contract-review-fixes`.
- Exact local and verified GitHub remote SHA: `2da980f631badc25086d12db60d128ff507d3ae6`.
- Parent candidate: `da7d348ffd3677d619dd31357e1e1e3cca28c9ec`; frozen research branch remains `bf31f3da430ffc35bd17fc380e1752adce6d1467`.
- One implementation commit, pushed without force. Clean worktree after final checks. Freeze this exact SHA; any subsequent change requires another review.

## Authority and scope

Original assignment verified at SHA256 `01b53d97bf45b85bf2f207ce762278dc2586badf2ca08b2caad3e71f864c018d`. Onboarding completed before implementation; repository AGENTS and required research documents read. Existing mapping/source-operation repairs retained.

Additional findings were first reproduced and returned to Sol before repair. Sol independently reproduced and explicitly approved implementation scope only:

- SRC-04/05: scope ruling SHA256 `de8b780d1c310d6055da59c1b7c3a73f551c69033f96233a1348c9346e491767`, provenance directory `2026-10-22T232008Z__SOL__r19-additional-contract-scope__677223`.
- SRC-06: scope ruling SHA256 `2bb6fac00f8dd75a558289e4193bcf6242f505a65647347d23cf82274fadd9ee`, provenance directory `2026-10-22T232351Z__SOL__r19-alias-validator-scope__535726`.

## Resulting behavior

1. SRC-01: index-zero decision-zero restart comparison occurs once; later source episodes execute normally. Duplicate index zero rejects before reset/generation; mismatches stop before action.
2. SRC-02: standalone analyzer bootstraps the repository root, retaining exact helper-origin verification. Clean fresh subprocess comparator and nonempty synthetic report CLI succeed outside the checkout without PYTHONPATH/PYTHONHOME/VIRTUAL_ENV.
3. SRC-03: immutable comparison receipt digest is placed in trajectory metadata before canonical hashing and event serialization. Event, returned row, JSONL round trip and registry receipt reproduce the same canonical digest. Own digest/event-reference exclusions remain unchanged; no cyclic sidecar hash.
4. SRC-04: source replay explicitly derives the exact current Action-ID from the ordered admissible map and passes it to record_step. Both initial and branch source replay retain ID/command/map binding; record_step does not globally infer missing IDs.
5. SRC-05: extension callback carries the number of already executed recovery actions. Physical indices match scheduler indices 1..5; initial=1 and extension=4 for a full path. Analyzer verifies the cross-layer recovery index invariant.
6. SRC-06: aliases resolve by actual authenticated arm event order and the measured source endpoint, preserving fixed shuffle 2,5,4,1,3. Checkpoints, cursor digest, horizon, terminal/termination fields, shared suffix references and own-row/event bindings are checked. Each K's canonical recovery generations and cost are independently reconstructed. K1 can correctly alias K2 while charging 2 recovery calls versus 3 after invalid attempt2. No scheduler, endpoint, logical-cost function or treatment was changed.

Incremental delta has seven files: two scripts, source-contract amendment, restart authorization's amendment-hash reference only, and three test files. Full bf31→final delta has nine files and includes the pre-existing repair. `evidence/incremental_to_final.diff` and `evidence/frozen_base_to_final.diff` preserve both exact diffs.

Nine frozen methods differ from bf31: seven runtime methods (actor_generation, _collect_one_source, _reserve_model_call, _reserve_environment_operation, _replay_source_prefix, recovery_step_callback, common_path_step_factory), and two analyzer methods (validate_branch_evidence, _validate_recovery_operation_link). Six of these change in this incremental commit; actor_generation and both reservation methods retain da7 bodies. The amendment records all nine old/new fingerprints; loader enforces this exact scoped set. New pure analyzer arm-order helper and bootstrap are file-diff changes outside those old method spans. Exact hashes are in `evidence/implementation_manifest.json`.

Scope flags: `source_treatment_semantics_changed=false`; `scientific_execution_behavior_changed=true`. Amendment says pending exact-SHA review and no new live authorization. Original G3 authorization, consumed clearance, unit-resolution JSONL bytes, protocol, schedule, exclusions, model/adapter/prompt/parser/decoding, K/horizon, quotas and caps are unchanged.

## Verification on frozen commit

Pinned interpreter: `/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python`.

| Check | Authentic result | Raw log / process receipt |
|---|---|---|
| Final five-file focused R19 suite | 160 passed, exit 0 | `evidence/final_focused.log`, `final_focused.receipt.json` |
| Full repository suite | 617 passed, 3 failed, 77 errors, exit 1 | `evidence/final_full_suite.log`, `final_full_suite.receipt.json` |
| Exact failure/error ID comparison | identical to both archived bf31 and da7 results; no added or removed IDs | `evidence/regression_comparison.json` |
| py_compile of changed Python files | exit 0 | `evidence/py_compile.log`, `py_compile.receipt.json` |
| git diff --check bf31→frozen final | exit 0 | `evidence/final_diff_check.log`, `final_diff_check.receipt.json` |
| Old genuine G2 raw evidence replay-free validation/re-evaluation | old G2_PASS reproduced; 176 generations, 322 operations including resets; all five pinned hashes match | `evidence/g2_compatibility.log`, `g2_compatibility.receipt.json` |
| Shared G2 callback scientific-behavior comparison | old/new model prompts/raw token evidence, commands, public transitions, checkpoints, stop reason and total costs identical at original prefix offsets 8 and18; bookkeeping indices corrected | `evidence/shared_callback_comparison.log`, `shared_callback_comparison.json` |

The full-suite historical failures/errors reference missing archived R7/R9/R18 artifacts. They were not repaired or reclassified. The result is not an all-green full suite; exact IDs and source log hashes are retained. No new formal-R19 dependency on those absent historical files was demonstrated by this work.

Core integration executes real actor_generation, collector, parser, DurableEventJournal, UnitRegistry, source selection, initial enrollment, extension, K handoffs, physical replay, SFT suffix, materialized branches, event/source/branch validators, analysis and renderer. Only generation and environment interaction edges are synthetic. No collector/parser/validator was mocked to force success. Authentication/unit fixtures remain explicitly synthetic; formal live 127-task/provenance requirements were not relaxed.

Focused tests retain valid, malformed/empty/out-of-range/non-admissible source output, source horizons, two different consecutive tasks in one runtime, immutable one-time comparator, 17 snapshot-field mismatch cases, pre-action receipt checks, hash round trips/tampering, source-persistence interruptions, unreceipted generation/environment operation blocks, phase caps, replay mismatch, distinct endpoints, terminal/invalid SFT suffixes, later invalid/terminal recovery with aliases, and alias future/self/cycle/missing/wrong-source/run/prefix/task/checkpoint/state/horizon/shared-suffix/outcome/termination/cost/recovery-ref/order tampering. A first test draft incorrectly treated multi-line output as malformed; it was corrected to preserve the existing final-line parser semantics rather than modifying the parser. Initial failure logs remain retained.

## Raw nonempty software evidence paths

Under this directory's `evidence/focused_artifacts/`:

- `test_restart_two_consecutive_s0/`: two-source lifecycle, completed units, one comparison receipt.
- `test_clean_fresh_comparator_no0/`: standalone comparator input and nonempty source evidence.
- `test_production_pipeline_nonem0/`, `...1/`, `...2/`: horizon, terminal and invalid SFT continuation, respectively; each contains real production `synthetic-output/` events/trajectories/registry/branches, `analyzer_cli_result.json`, and `report/summary.json`, `R19_OPPORTUNITY_REPORT.md`, `report_hashes.json`.
- `test_stopped_common_paths_auth0/`, `...1/`: invalid-later and terminal-later recovery aliases; `alias_cli_result.json` and nonempty synthetic report outputs.

These are synthetic software fixtures, never real G3/G4 results, task-failure evidence or held-out evidence. Pre-fix reproductions are retained separately in `pipeline_replay_failure/`, `alias_reproduction/`, `pipeline_tests_v2.log`, `alias_probe.log` and `additional_contract_findings.json`.

## Preservation, G2 and limitations

Original failed G3 ledger/manifest/registry/empty branches match pinned hashes before/after this task; original supervisor hashes also rechecked. Do not use UnitRegistry.begin on the original registry. No editing, rerunning, adjudicating or completing old scientific units occurred. Original first source remains incomplete, not a task failure. Cumulative actual expenditure stays177 generations/342 environment operations; source headroom8999/8999 and all other/global caps unchanged.

G2 executed SHA stays92aae1d9b230cc212c6ec4effc99aa468941e69d. Callback changes correct bookkeeping IDs while preserving the synthetic scientific traces and total smoke accounting; new strict scheduler/physical link checking applies to formal branch validation. Carry-forward routing authenticates old G2 via its raw ledger, original smoke evaluator and stored offline evidence, without applying a new live-source schema to old smoke. The full offline G2 verifier deliberately requires the original exact clean executed commit and was not relabeled as having run on this candidate. Final new-SHA G2 carry-forward is PENDING_SOL_REVIEW; no G2 rerun is authorized.

Authentic predecessor loader in this isolated checkout fails closed because original output and supervisor cwd bind the designated execution checkout. Exact observed error: `source-contract restart predecessor identity is missing or unsafe`. Original receipts were not copied/rewritten and PROJECT_ROOT was not mocked to manufacture a PASS. Actual predecessor bytes, G2 evidence, snapshot/cost audit and the new fingerprint overlay were separately read/checked. Sol must review the genuine predecessor binding in the intended execution context; this task claims no new authentic-loader/preflight PASS for the isolated candidate.

Zero real model loads/generations, ALFWorld constructions/resets/steps, held-out tasks, training, G2 rerun, real preflight, G3 launch, live G4 or external model calls. No launch instructions sent to Luna. New worktree only; shared execution/reviewer/scientific-main worktrees and Sol/Luna records untouched in this task. Prior onboarding file in the execution worktree remains untouched.

## Publication and return

Scientific branch pushed and remote verified; no PR, merge or force push. This developer-owned provenance directory is local pending Sol's coordinated publication. Shared provenance INDEX.md/FILE_HASHES.sha256 and Sol/Luna task directories were never edited or staged by this developer. Raw large fixture trees remain local for review; publish only compact own record/log/manifest files according to the attached publication inventory, then let Sol coordinate shared inventory/index changes. Do not claim a provenance main commit for this task until actually published and verified.

Return channel: Sol thread `01a0994c-a209-7600-8a3e-5ff3096ed346`. Stop at frozen SHA awaiting independent review. No preflight, launch, retry or additional science follows from developer test results.
