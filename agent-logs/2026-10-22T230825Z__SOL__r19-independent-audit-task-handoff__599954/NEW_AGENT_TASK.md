# R19 implementation assignment — Sol Research / New Agent

Task owner: Sol Research (thread01a165de-c75e-7120-abc9-fa74cde1f17f, host remote-ssh-discovered:sdxsrv03). Role: implement and test only. Independent acceptance belongs to Sol, thread01a0994c-a209-7600-8a3e-5ff3096ed346. This coordinator assignment authorizes the narrow implementation below after onboarding, not a scientific run.

## Start from actual state

Read sibling INDEPENDENT_AUDIT.md first. Independently print root/branch/status/HEAD and compare remote refs. Frozen branch codex/r19-recovery-duration-v1 remains bf31f3da430ffc35bd17fc380e1752adce6d1467. Existing candidate codex/r19-source-contract-repair is da7d348ffd3677d619dd31357e1e1e3cca28c9ec, independently FAIL. Preserve its two existing fixes; inspect the complete base→candidate delta. If another repair exists when you begin, inspect/report rather than overwrite or duplicate it.

Work in your own isolated Git worktree and a new codex/ branch based on da7d348 (suggest codex/r19-source-contract-review-fixes). Never develop in /home/lizening/Alfworld-Self-Improvement-Project, reviewer root, a detached reviewer checkout, or Luna's execution checkout. Do not change other agents' branch/worktree. Read repository AGENTS.md and its required PROJECT.md/PAPER_PROPOSAL.md/EXPERIMENT_PLAN.md/IMPLEMENTATION_PHASES.md/reports/SPRINT_1_5_FINAL.md before code changes, plus R19_PROTOCOL.md and machine protocol.

## Authorized minimal changes

1. Keep the repaired mapping producer/consumer contract throughout source and suffix. Source actor must emit source_generation; SFT suffix retains task_actor_generation. Retain actual parser, selection metadata, ordered admissible mapping and failure statuses.
2. Fix R19-SRC-01 at collector line1905: comparison exactly once on first scheduled episode; subsequent episodes proceed; repeated index0 and mismatches stop without actions/retry. Do not skip index0.
3. Fix R19-SRC-02 at analyzer line490: standalone clean-process comparator resolves exact checkout production helper. Preserve origin checks; no dependency on caller cwd/PYTHONPATH, no importing another checkout, no validator bypass or weakened checks.
4. Fix R19-SRC-03 at collector lines2017–2033: choose a consistent canonical trajectory hash domain and persistence ordering; event/JSONL/returned row/registry receipt must reproduce the same declared digest. Avoid cyclic sidecar hashes. Keep comparison receipt bound and immutable.
5. Update only source-contract amendment/fingerprint/hash references necessitated by the actual fix. Enumerate exact changed frozen methods; update old/new overlay honestly; report execution behavior changed and treatment semantics unchanged. Preserve original G3 authorization, consumed clearance, raw failure evidence and original unit-resolution JSONL bytes. Do not mark a review or launch PASS/APPROVED on Sol's behalf. A developer may document requested/pending review, never fabricate user execution approval.

Initial allowlist: scripts/run_r19_experiment.py, scripts/analyze_r19_recovery_duration.py, tests/test_r19_source_contract.py and narrowly relevant R19 tests; source-contract amendment/restart hash references only as necessary. Shared pure-helper refactoring is allowed only if required for these proved defects and documented in the delta. Do not refactor unrelated replay/recovery systems. For any other issue, supply exact location/reproduction and ask Sol to adjudicate scope before repairing it.

## Required software verification

Use pinned /home/lizening/miniconda3/envs/alfworld-self-improve/bin/python. Real production actor_generation, collector, parser, DurableEventJournal, UnitRegistry, source/branch validators, recovery orchestration and renderer must execute. Only model-generation and environment interaction edges may be synthetic for the core integrated path. Test-local filesystem/supervisor fixtures must be explicitly synthetic; do not represent them as authentic live evidence. Never mock validators, collector, actor_generation, journal or parser to force success.

- A single nonempty source episode: valid action, real parser, correct source event operation, trajectory append and registry completion.
- At least two different consecutive source episodes in one runtime with restart enabled. Exactly one first-source comparison receipt, zero repeat comparisons on episode2; episode2 actions execute; duplicate index0 rejected before any new reset/generation. Assert counts and receipt immutability.
- Exact first-source state/prompt/rendered prompt/raw output/token IDs/token statistics/parser/action/map matching before first environment action. Perturb each field category; mismatch leaves incomplete source unit, no action, no retry.
- Malformed/empty/out-of-range/non-admissible outputs retain original fail-closed behavior and physically charge generations; no accidental environment action. Multi-step and horizon50 source cases remain covered.
- Assert canonical digest equality using production hashing helpers for returned/persisted/event trajectory and registry receipt; verify sidecar changes are detected in its intended domain.
- Nonempty production source→prefix/replay→initial recovery→eligibility→common path→K-specific checkpoint/SFT suffix→materialized branch→event/branch validation→summary/report path. Produce actual branch rows through production orchestration, not fabricated success/cost tables. Cover replay mismatch, terminal/invalid suffix, logical per-K cost versus physical shared/replay/reset cost. Existing nonempty renderer-only test is not this full integration.
- Fresh subprocess with PYTHONPATH/PYTHONHOME/VIRTUAL_ENV removed, cwd outside checkout: real comparator succeeds on a matching synthetic fixture. Run actual analyzer CLI with explicit synthetic classification/--allow-synthetic on a nonempty production-produced bundle and assert real process exit0 and report/hash artifacts; invoke production source validator and restart comparator as well. Test tampering rejection. Do not weaken formal live127-task/authentic-provenance requirements for a small software fixture; synthetic success is never a real G4 result.
- Preserve actual predecessor hash/context rejection and old suffix event convention. Authentication unit fixtures may remain explicitly synthetic; real predecessor read-only validation is a separate check. If historical absolute-cwd bindings cannot be tested from an isolated checkout, report that constraint rather than editing original receipt bytes.
- Inject software interruption at representative source persistence boundaries and generation/environment started-without-completion cases; verify no completed source is invented, no silent rerun and no automatic retry. All injected failures use test directories, never old registry/ledger.
- Budget tests: restart-only8999 source generations/8999 source environment operations including resets/actions; every other phase/global ceiling unchanged;177/342 prior baseline remains charged. No quota transfer.

Run focused R19 tests, py_compile, git diff --check, then the appropriate full repository suite. Historical bf31 comparison currently has3 failed/77 errors (550 pass at candidate versus532 at base), attributable to known unavailable historical artifacts; compare failure IDs, not just counts. Do not repair them. New relevant failure or proof a missing historical artifact is required by formal R19 path is blocking and must be reported.

## Forbidden changes and scientific execution

No real model load/generation; no ALFWorld construct/reset/step; no G2 rerun, real preflight, G3, G4 live analysis or training. No model/adapter/tokenizer/prompt/decoding/parser semantics/recovery semantics/K/horizon/schedule/quota/exclusion changes. No selector, memory, DPO/ORPO/PPO/GRPO, new environment, budget expansion, retry loop, deletion/reclassification of previous cost, or edits to raw failed run. All machine-specific paths remain ignored configs/local or external provenance, never committed to scientific repository.

## Freeze and return

Commit the narrow fix on your isolated branch and push that branch without force. Return exact full SHA, remote ref verification, base→final diff, changed file/method list and hashes, all raw test logs/exit codes, regression comparison, scope flags, original evidence hash-preservation check and unresolved limitations. Record software-only synthetic class and zero scientific side effects. Once handed off, freeze that exact SHA; any change requires a new review. You may create provenance files in your own directory, but do not edit Sol/Luna records or concurrently stage shared inventories; coordinate publication with Sol.

Acceptance: Sol independently checks complete frozen-base→final delta, reruns required successful integration plus negative tests and authentic predecessor checks, confirms G2 carry-forward, correct disposition/budgets/frozen inputs, and issues an immutable exact-SHA review. Developer test PASS is not acceptance. Stop after handoff; no preflight or launch permission follows from your implementation assignment.

Dependency: implementation → Sol exact-SHA review → Luna preflight → independent launch clearance → explicitly authorized scientific execution → G4. Send your completion report back to Sol with full evidence paths; do not send a launch instruction to Luna.
