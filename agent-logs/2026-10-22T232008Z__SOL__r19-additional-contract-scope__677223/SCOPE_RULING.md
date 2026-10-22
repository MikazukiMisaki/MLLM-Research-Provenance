# R19 additional scope ruling: SRC-04 / SRC-05

Decision by Sol: **APPROVE TWO MINIMAL ADDITIONAL FIXES AND THEIR REQUIRED FINGERPRINT/TEST BINDINGS**. This is an implementation-scope decision, not implementation acceptance, positive preflight release, launch clearance or scientific execution authorization.

## Independent evidence

Baseline HEAD of developer worktree: da7d348ffd3677d619dd31357e1e1e3cca28c9ec, with uncommitted SRC-01/02/03 repairs and integration test. This is a source-content-hash-bound scope reproduction, not an exact-SHA approval of that dirty tree. The exact runner/analyzer/test hashes are in independent_reproduction.json; files did not change during this probe.

Sol read the fixture and independently called actual _run_frozen_pilot using its synthetic generation/environment edges. Actor/collector/parser/journal/registry/recovery scheduler/replay/suffix/materialized branches were production functions; no validator was mocked. One synthetic eligible prefix and five K arms were produced. Authentic scientific cost remains177 generations/342 operations: this probe is software-only and adds zero real model/ALFWorld operations.

### R19-SRC-04 — BLOCKING: source-prefix replay omits Action-ID receipt binding

Developer current scripts/run_r19_experiment.py approximately2087: _replay_source_prefix calls record_step without action_id. Sol's first replay receipt has command look, action_map {A000:look,A001:go to garbagecan1}, action_id=null. validate_event_ledger rejects it at analyze_r19_recovery_duration.py:354 with 'environment command is not bound to its contemporaneous admissible-action map'. Both initial replay and branch checkpoint replay share this producer. Independent preserved fixture contains24 such replay completions; the first is sufficient to trigger rejection.

Authorized change: in _replay_source_prefix derive the replayed command's exact ID from production action_id_mapping of the contemporaneous ordered valid_actions, fail closed if absent/inconsistent, and pass it explicitly to record_step for both start/completion receipts. Preserve command, action order, replay before/after checks, model/parser/prompt and environment behavior. Do not weaken analyzer checks or globally make record_step silently infer missing IDs for arbitrary emitters.

Required tests: nonzero source-prefix replay and branch replay, Action-ID/command/map consistency at every replay transition, successful actual ledger/branch validation; altered ID or map rejected. No edits to original receipts, no replay of the authentic failed run.

### R19-SRC-05 — MAJOR: callback rebases physical recovery index and phase debit

Developer scripts/run_r19_experiment.py recovery_step_callback approximately1660–1710 and common_path_step_factory approximately1712–1718. Factory resumes at checkpoint1 but callback computes index relative to that checkpoint instead of the original recovery prefix. Independently observed physical recovery indices [1,1,2,3,4], scheduler action-record indices [1,2,3,4,5]. Runtime phase counters count2 initial actions and3 extension actions instead of1 initial/4 extension; other replay/logical operations stay separate. Frozen classification at _reserve_environment_operation and _step_budget_category treats recovery_action_index1 as initial; this can falsely exhaust initial budget or undercount extension against the wrong phase.

Authorized change: keep physical event indexing relative to the ORIGINAL common recovery path. A narrow explicit starting offset/baseline parameter through recovery_step_callback and common_path_step_factory is acceptable. Ordinary initial callbacks default to offset0; continuation starts after exactly len(path.actions) already executed. Do not change actual command/action order, K checkpoints, cursor/horizon, generation count, stopping rule, budgets or phase definitions. No moving costs between phases by changing the frozen cap/classifier to accept the bug.

Required tests: actual joined scheduler/physical operation refs show indices1..5; nonzero prefix action count and already-executed recovery offset both covered; one initial physical action and four path-extension actions for a five-action common path, each charged once. Test terminal/invalid extensions and phase cap boundaries. Add an assertion/invariant that scheduler recovery action index agrees with its referenced physical receipt so this mismatch cannot be silently accepted. A narrowly scoped check in analyzer._validate_recovery_operation_link is allowed if needed for that negative regression; preserve documented legacy G2 carry-forward routing and explain its compatibility rather than rewriting historical bytes.

## Exact allowed extension and provenance metadata

Beyond existing SRC-01/02/03 allowlist, production changes are limited to LiveR19Runtime._replay_source_prefix, LiveR19Runtime.recovery_step_callback and LiveR19Runtime.common_path_step_factory, plus the specific analyzer link invariant above if necessary. Add focused tests and continue the already assigned complete production synthetic source→recovery→K branches→validators→clean report CLI path. No unrelated replay/alias/phase concerns or broader refactors are approved by this ruling.

These three runtime methods are in the original frozen40-method manifest. Extend the versioned amendment old/new method overlay and exact whitelist loader/schema honestly to include only methods actually changed. The old loader's hardcoded exactly-four allowlist must be updated as necessary for this explicitly approved extension, retaining exact method-set/hash enforcement. Count and disclose all changed pinned methods (up to seven if all original four plus these three change); do not mask a hash, bypass fingerprints, or claim all scientific execution behavior unchanged. Update dependent versioned hashes/review bindings; never edit original G3 authorization, old failed evidence, old clearance or original unit-resolution JSONL. Documentation may state developer scope is approved; no APPROVED_BY_USER scientific launch or reviewer PASS may be fabricated.

## G2 carry-forward and review boundary

Source replay helper is on formal pilot path, whereas G2 smoke has its own smoke replay helpers. However common_path_step_factory/recovery_step_callback are also used by smoke orchestration. Therefore previous G2_CARRY_FORWARD PASS for the old candidate does not automatically approve the new delta. Return an explicit comparison showing unchanged G2 model/prompt/decoding, actions/checkpoints/outcomes, total physical costs and smoke ceilings; disclose corrected bookkeeping identities and any legacy validator effect. Preserve G2 executedSHA92aae1d9b230cc212c6ec4effc99aa468941e69d and raw bytes; NO G2 rerun. Sol decides carry-forward in the new exact-SHA review. If evidence demonstrates a genuine scientific-semantic incompatibility, stop/report rather than change protocol or claim continuity.

Prior SRC-01/02/03 repairs and the19 passing tests are developer results, not independently accepted here. After these fixes run all relevant positive/negative integration, fresh-process comparator/report, pinned focused/full checks and return new frozen exact SHA/diff/raw logs. Any further failure requires another concrete scope request before repair.

No model/ALFWorld, real preflight, live G3/G4, retry, schedule/K/quota/horizon/cap changes. Cumulative real cost177/342 and source headroom8999/8999 stay fixed. Original failed source is incomplete, not a task outcome. This scope ruling grants no execution authorization.

Shared provenance INDEX/inventory publication remains paused for Luna's previously allocated window. This unique Sol-owned scope record is local evidence until a coordinated publication; do not stage it in the developer/Luna commit or claim it uploaded.
