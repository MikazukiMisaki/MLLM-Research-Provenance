# Independent exact-SHA R19 source-contract and restart-gate review

Target: `51ec074cec6c2c2a7b1ecd64e0da33bc446a7e54`; base: `bf31f3da430ffc35bd17fc380e1752adce6d1467`.

IMPLEMENTATION_REVIEW: FAIL
G2_CARRY_FORWARD: PASS (evidence and unchanged smoke semantics only; restart remains blocked)
source_treatment_semantics_changed: false
scientific_execution_behavior_changed: true
first_source_episode_integration: PASS, single synthetic episode only
first_source_restart_comparison: FAIL for multi-episode lifecycle; index-zero pre-action comparison passes in synthetic isolation
known-failed disposition: PASS_KNOWN_FAILED_NO_ACTION_NO_UNCERTAINTY
Launch clearance: not issued. Positive production preflight: not run.

## R19-SRC-01: BLOCKING — One-time restart comparison runs again on source episode 2

Location: `scripts/run_r19_experiment.py:1905`.

The guard tests restart_expected and step_index==0, without schedule_index==0 or consumed guard. After a successful first source episode, the second episode completes a synthetic reset and generation then raises FileExistsError because source_restart_comparison.json already exists. No second-episode action occurs. The real 127-episode campaign cannot complete.

Minimal fix: Restrict comparison creation to the first scheduled source decision exactly once, preserving duplicate-index-zero rejection and mismatch-stop behavior. Add an integration regression with two consecutive episodes in the same runtime.

## R19-SRC-02: MAJOR — G4 comparator cannot resolve production runner in a clean standalone analyzer process

Location: `scripts/analyze_r19_recovery_duration.py:490`.

A fresh pinned-Python process with PYTHONPATH/PYTHONHOME/VIRTUAL_ENV removed loads the actual analyzer via runpy, then invokes its comparator on the passing nonempty synthetic source fixture. It fails at from scripts import run_r19_experiment with ImportError. The in-process tests preload scripts and mask this dependency.

Minimal fix: Resolve the production dependency from the analyzer file's repository root with origin verification, or share the pure snapshot helper under src. Verify the successful comparator/report path in a clean fresh process.

## R19-SRC-03: MAJOR — Persisted first-source trajectory does not reproduce its declared canonical hash

Location: `scripts/run_r19_experiment.py:2032`.

The code calculates trajectory_sha at line 2017 and serializes the source event before adding metadata.source_restart_comparison_sha256 at line 2033. Both canonical hashing helpers retain that field. Independent recomputation on the returned row and source_trajectories.jsonl differs from metadata.source_trajectory_sha256. The durable event trajectory and persisted trajectory file therefore disagree in their hash domain.

Minimal fix: Use a consistent documented hash domain: include the sidecar reference before hashing/serialization, or keep it outside the trajectory hash domain consistently. Assert canonical digest equality across returned row, persisted source JSONL and durable source-event trajectory.

## Checks that passed

The complete eight-file delta was inspected. The package/start-prompt hashes match. Protocol/schedule/exclusions are byte-identical to the base; exactly four of the 40 pinned methods differ and all four amendment overlays match. Model, tokenizer, adapter, prompts, parser, K grid, quotas and horizon are unchanged. The source-contract bugfix and pre-action gate change execution behavior, so no blanket no-behavior-change claim is made.

Authentic restart-record loader passed without mocks against the preserved predecessor and independent audit. Four authentic predecessor files were copied into ignored detached runtime to preserve exact PROJECT_ROOT behavior; originals were never modified. Append-only disposition leaves the original unit incomplete and original evidence intact. The one-restart output gate accepts only that predecessor and rejects a second successor sentinel. Source model and source environment-operation budgets including resets are 8,999 each; all other phase ceilings unchanged; cumulative maxima remain 26,756 generations and 41,201 operations within original global limits 26,988 / 41,260.

Targeted suite: 93 passed in 11.89s. Full suite: 3 failed, 550 passed, 77 errors in 27.77s. Historical failure/error IDs exactly match the previously independently tested base; they are not reasons for this FAIL.

The implementation worktree advanced to da7d348 during review. All reported decisive tests and probes were rerun in the retained detached 51ec074 checkout; no approval covers da7d348 or later commits.

## Three record hashes

- `r19_b1_g3_source_contract_repair_amendment_v1.json`: `62ff158f5739859266664b1db2e323dca6ea0ad3b8e84134ecbe5fd06c847372`
- `r19_b1_g3_source_contract_restart_authorization_v1.json`: `de634ba310e47d3d49838b8a73d9c6d87f7db87deed042311e3718061a7eb428`
- `r19_b1_g3_source_unit_resolution_events_v1.jsonl`: `58783ba60b076ee190dccb0875aac65891d7e1c811e00fbe6303ca65896369d9`
