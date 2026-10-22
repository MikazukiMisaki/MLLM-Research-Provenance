# R19 independent audit and recovery decision

Reviewer / technical lead: Sol. This is an independent audit, not an execution authorization.

## Exact observed state

- Frozen scientific branch `codex/r19-recovery-duration-v1`: local and remote `bf31f3da430ffc35bd17fc380e1752adce6d1467`.
- Existing repair branch `codex/r19-source-contract-repair`: local clean HEAD and remote `da7d348ffd3677d619dd31357e1e1e3cca28c9ec`. It contains `51ec074` plus predecessor-context hardening; no later repair was visible at audit start. Do not redo or overwrite those changes.
- Reviewer root `/home/lizening/wt-codex-r18c2`, branch `agent/codex-r18c2`, HEAD `e537f441010077123a307e9d50ea40cf8dad8547`, clean. No development in `/home/lizening/Alfworld-Self-Improvement-Project`.
- Provenance local/remote main at audit start: `d54ebb7eec421f6e5c70565f895adfdbe6498ee2`; the older `4c3bcaae...` checkpoint is superseded by actual review commits, not a pending PASS.
- No R19 runner/supervisor entrypoint process or GPU compute process found. Only the known failed G3 output directory was present. These are point-in-time observations, not continuing monitoring.
- Current implementation decision: FAIL. G2 carry-forward: PASS for authentic old evidence and unchanged smoke semantics only. Real positive preflight eligibility: NO. No launch clearance.

## Authentic failure and cost independently recounted

Run `3d1ccea7e97f4727abf8e216ac6ec498` truly exited 1 (`subprocess.returncode`); supervisor says failed, not interrupted. Its four-event ledger contains one reset start/completion and one generation start/completion (267 input +5 output tokens). Zero action steps, completed source episodes, recovery attempts, eligible prefixes or branches. No incomplete external operation.

Production `validate_event_ledger` was rerun on the raw failed G2 predecessor, successful G2, and failed G3 ledgers, checking their pinned hashes. Totals: **177 completed generations; 330 non-reset operations +12 resets =342 environment operations; zero incomplete external operations**. The earlier import-only G3 failure contributed no science cost. See `evidence/state_and_cost_audit.json` for all raw paths, hashes and per-run results.

The sole source unit remains `in_progress`; manifest remains `RUNNING`. These retained local statuses do not override authentic supervisor exit. The unit is a known software-interrupted, incomplete source episode, not a successful episode or an observed task failure. Do not call `UnitRegistry.begin` on the old file: its fail-closed behavior would mutate the old in-progress entry to indeterminate. Never use the old output as a writable continuation.

Pinned identities:

- Failure audit SHA256: `8eb1248c1d863674119813ba1f90ba3ca6834bb1906cb2aa67acc6a4e087fe34`.
- Event ledger SHA256: `fde95fcd72f1c4ac6409fab7f2112654e145f6184fefec690cae58ad345f1cd7`.
- Registry SHA256: `870923242ae585c66cbcffa554528ab3d92cf98fc4d87dee2c4d408f5f6ba800`.
- Manifest SHA256: `f5d3efa6c17abea3d944d7dea01099210d846eb8ed107057ec24502bbb51d2df`.
- Authentic supervisor directory: `/home/lizening/research-notes/agent-logs/2026-10-22T190221Z__CODEX__r19-g3-cli-preflight__bf31f3da/live_supervisor/`.

## Confirmed defects and candidate fixes

### A — BLOCKING in bf31f3da; repaired in da7d348

`actor_generation` returns `(generation mapping, selection mapping, event_id)`. At baseline `scripts/run_r19_experiment.py:1456`, `_collect_one_source` read `parsed.selection_status` / `.action` / `.action_id` as object attributes. The authentic first live source generation produced the traceback. Candidate collector consumes mapping keys, reuses contemporaneous selection metadata, and passes real-producer single-episode synthetic integration. Retain this fix; do not alter parser or action semantics.

### B — MAJOR in bf31f3da; repaired in da7d348

Baseline actor at `scripts/run_r19_experiment.py:1350` overwrote source operation with `task_actor_generation`; actual failed ledger confirms the emitted value, whereas `validate_live_source_schedule` expects `source_generation`. Candidate `actor_generation` (lines1778–1787) preserves source_generation only for task_actor; SFT suffix retains its historical task_actor_generation event convention. Retain both conventions; never rewrite old events.

### R19-SRC-01 — BLOCKING, still present in da7d348

Location: `scripts/run_r19_experiment.py:1905` (exception at1934). Trigger: a valid first restarted episode completes and writes source_restart_comparison.json; the next schedule-index-one episode reaches decision0. The guard checks only restart_expected and step_index==0, so it reruns the first-only comparison and finds the existing receipt. Independent rerun again consumed one synthetic reset/generation for episode2, then FileExistsError, zero actions. A normal127-source campaign cannot complete. Restrict comparison to first scheduled episode exactly once; preserve mismatches stopping before action and duplicate-index-zero rejection. Required regression: two distinct consecutive episodes on the same runtime with restart enabled.

### R19-SRC-02 — MAJOR, still present in da7d348

Location: `scripts/analyze_r19_recovery_duration.py:490`. Trigger: clean pinned process, cwd outside checkout, PYTHONPATH/PYTHONHOME/VIRTUAL_ENV absent, actual analyzer loaded as standalone module and comparator invoked with a passing nonempty fixture. `from scripts import run_r19_experiment` raises ImportError; only src is bootstrapped. In-process tests pre-import runner and hide it. Fix repository-root import/origin handling or share the pure helper without a circular dependency. Required regression: successful comparator plus report CLI in a fresh clean process. No full genuine G4 was run by this audit.

### R19-SRC-03 — MAJOR, still present in da7d348

Location: `scripts/run_r19_experiment.py:2017–2033`. trajectory_sha is computed and source_episode_completed serialized before comparison metadata is appended to the returned/persisted row. The canonical hashing helpers retain that field. Fresh rerun again shows persisted declared digest differs from production canonical recomputation. Use one documented hash domain and assert digest equality across event trajectory, returned row, source JSONL and registry receipt. This is a persistence-integrity defect; do not inaccurately claim the current event-only validator necessarily rejects every such row.

## Full path review and limits

| Path | Independent evidence / conclusion |
|---|---|
| Source actor → parser → collector | Production actor_generation, parse_p2_selection, collector, journal, registry and source validator pass nonempty synthetic single-episode path. Dict consumer and operation fixes verified; later-episode and hash defects above remain. |
| Parser / selection metadata | Emitter retains parser result and ordered map; analyzer `_validate_generation_parser` reparses raw output for task_actor/sft and separately for stage1/stage2. Stage1/2 attribute access is on actual parser objects, unlike former source mismatch. No additional concrete dictionary/object defect identified in these inspected sites. |
| Persistence | Journal append is fsynced; source event precedes trajectory append; registry completion follows successful collection. An interruption may leave incomplete units and must remain fail-closed. Hash mismatch above is confirmed. Do not promise arbitrary crash resume or mutate old artifacts to reconcile them. |
| Replay / checkpoints / SFT suffix | Inspected `_replay_source_prefix`, `_replay_path_checkpoint`, `run_sft_suffix`, initial candidate and frozen enrollment orchestration. Public before/after states and cursor hashes are compared; suffix is isolated per prefix/K and consumes mapping keys. No newly reproduced defect here; require cross-path synthetic regression, not speculative refactoring. |
| Physical versus logical cost | Physical starts/completions validated separately from logical branch reconstruction. `_check_cost_reconstruction` reconstructs per-arm generation/action costs; replay/reset expenditure remains physical, and shared generation is not multiplied physically by K. Current raw177/342 independently confirmed. |
| Exceptions and retry | Durable journal detects unfinished operations; registry rejects uncertain reuse. Existing output gate allows only one successor to the exact preserved predecessor. Failure remains stop/no automatic retry; old clearance is consumed. |
| G4 positive path | Existing source report test calls renderer on fabricated branch-result fixtures; this is not a complete production source→recovery→branch validation→CLI proof. Fresh clean comparator currently fails. Developer must supply a nonempty production synthetic pipeline and fresh CLI success; synthetic report never counts as genuine G4. |

Fresh focused suite in the retained clean exact-da7d348 checkout: see `evidence/focused_tests.log` (93 passed). Three implementation probes rerun in this task and saved under `evidence/`. Previous exact-SHA full-suite run had550 passed/3 failed/77 errors with unchanged baseline failure/error IDs; not rerun here because source is identical and no new changes justify it. Missing historical artifacts are not a reason to broaden this repair; any newly proven R19 execution/provenance dependency on a missing artifact becomes a blocking finding.

Authentic predecessor loader previously independently passed in a clean fresh pinned process against all four supervisor receipts, context/cwd/argv/environment declarations, actual raw ledger/registry, failure audit, fingerprints and disposition. This narrow PASS remains valid; it does not repair the three defects. Original immutable exact review hash `8fcd731bcbfd01b2e89228e79f70834e15c57a5f3502e1a68f559355ab2e3c40`, containing commit `8cb595540ee4d936bd5ab2324172ca995f40cd17`; clean-loader supplement commit `d54ebb7eec421f6e5c70565f895adfdbe6498ee2`.

## Protocol impact and bounded restart recommendation

Intended source treatment remains unchanged; the contract repair and restart gate change execution behavior. Explicitly report `source_treatment_semantics_changed=false` and `scientific_execution_behavior_changed=true`; do not claim all40 method fingerprints are unchanged. Frozen protocol/schedule/exclusions remain byte-identical; genuine G2 execution SHA `92aae1d9b230cc212c6ec4effc99aa468941e69d` is carried without rerun.

One new engineering restart is scientifically defensible only conditionally: preserve old run, independent new run/output, keep all127 tasks including index0, repeat its reset/generation once and compare exact snapshot before first action, charge both old and new cost, no completed branches duplicated, no automatic retry. Existing append-only disposition JSONL hash `58783ba60b076ee190dccb0875aac65891d7e1c811e00fbe6303ca65896369d9` supports known-failed incomplete source status. Its historical pending-review marker need not be rewritten: a separate immutable Sol adjudication/review receipt can bind its bytes and the actual final decision.

Remaining source ceilings:8999 generations and8999 environment operations including resets/actions. Other remaining phase caps unchanged: initial240 calls/5520 ops, path extension240/2940, suffix17100/18000, replay0/5400. Global ceilings26988 calls/41260 ops. Worst-case cumulative177+26579=26756 calls;342+40859=41201 ops. No budget/quota transfer.

**No new live authorization is granted now.** Prior maximum-one-successor clearance is consumed. Before any scientific execution, obtain fresh explicit user authorization tied to replacement exact SHA, fresh output/run identity, bounded one launch and cumulative caps; independently issue exact argv/environment/hash-bound clearance only after authentic preflight. Existing versioned adoption records do not substitute for that launch decision. Minimal later authorization wording: authorize at most one supervised G3 engineering restart at the independently reviewed SHA with127 frozen TRAIN tasks,120 initial attempts,60 eligible states30/15/15,K1..5,horizon50, source headroom8999/8999, cumulative baseline177/342 and global26988/41260; repeat only index0 reset/generation once for exact pre-action comparison; no G2 rerun/no automatic retry; stop and preserve evidence on mismatch/failure; G4 report-only only from authentic completed successor evidence.

Dependency: **New Agent implementation → Sol exact-SHA review → Luna real positive preflight → independent launch clearance → explicitly authorized scientific execution → genuine G4.** Review and clearance are separate; developer tests cannot self-approve either.
