# Independent exact-SHA R19 source-contract/restart review

Target: da7d348ffd3677d619dd31357e1e1e3cca28c9ec; branch codex/r19-source-contract-repair; base bf31f3da430ffc35bd17fc380e1752adce6d1467.

IMPLEMENTATION_REVIEW: FAIL. G2_CARRY_FORWARD: PASS (unchanged smoke semantics and authentic old evidence only). Positive production preflight eligibility: NO. Launch clearance: NOT ISSUED.

All three findings below were reproduced anew at the target SHA. The earlier 51ec074 review is superseded as a review request; no PASS is issued for either commit.

## R19-SRC-01 — BLOCKING: One-time restart comparison runs again on source episode 2

Location: scripts/run_r19_experiment.py:1905.

Fresh exact-da7d348 probe: after one matching, completed synthetic first source episode, a second source episode (schedule index 1) completes one synthetic reset and one synthetic generation, then raises FileExistsError at line 1934 because source_restart_comparison.json already exists. It executes zero second-episode actions. The guard at line 1905 checks restart_expected and step_index == 0 for every episode; it lacks a once-only schedule-index-zero condition. The 127-source campaign cannot complete.

Suggested correction: Restrict comparison creation to the first scheduled source decision exactly once, preserving duplicate-index-zero rejection and mismatch-stop behavior. Add an integration regression with two consecutive episodes in the same runtime.

## R19-SRC-02 — MAJOR: G4 comparator cannot resolve production runner in a clean standalone analyzer process

Location: scripts/analyze_r19_recovery_duration.py:490.

Fresh pinned-Python process with PYTHONPATH/PYTHONHOME/VIRTUAL_ENV removed, cwd outside the repository, loads the actual analyzer using runpy and calls validate_source_restart_comparison on the passing nonempty synthetic first-source fixture. It fails at line 490 with ImportError: cannot import name run_r19_experiment from scripts (unknown location). In-process tests already import the runner and mask this dependency. This demonstrates the comparator failure; a full genuine G4 CLI was not run.

Suggested correction: Resolve the production dependency from the analyzer file's repository root with origin verification, or share the pure snapshot helper under src. Verify the successful comparator/report path in a clean fresh process.

## R19-SRC-03 — MAJOR: Persisted first-source trajectory does not reproduce its declared canonical hash

Location: scripts/run_r19_experiment.py:2033.

Fresh exact-da7d348 probe: the returned and source_trajectories.jsonl first-source rows declare hash 17a8aea3ed7aaa1be4e99c3cf2c25ec19daaf8fdd9f19730c794b062d04dee74, but production canonical recomputation is 6458ff7785d1c133c57b1227c76777bd8610eb8a3aa536f3fd27f109c5b45532. trajectory_sha is computed at line 2017 and source_episode_completed serialized before metadata.source_restart_comparison_sha256 is added at line 2033. Both canonical helpers retain this new field, so the persisted artifact does not reproduce its declared hash. This is an artifact-integrity defect; it is not a claim that the current event-only source validator always rejects it.

Suggested correction: Use a consistent documented hash domain: include the sidecar reference before hashing/serialization, or keep it outside the trajectory hash domain consistently. Assert canonical digest equality across returned row, persisted source JSONL and durable source-event trajectory.

## Verified scope and passing checks

The complete eight-file delta from bf31f3da was inspected. Only four of the 40 frozen scientific methods changed; all amendment overlays match. The dict producer/consumer repair and source_generation identity work for a single completed source episode. The old suffix operation remains task_actor_generation. Model, adapter, prompts, parser, decoding, 50-step horizon, K grid, quotas, frozen protocol, 127-entry schedule including index zero and exclusions are unchanged. source_treatment_semantics_changed=false; scientific_execution_behavior_changed=true.

Authentic predecessor loader passed without mocks in the clean original da7d348 checkout. The added supervisor checks bind the exact frozen receipt bytes, actual failure exit and run identity, argv, cwd, clean environment declarations and linked hashes. Four altered launch-context copies (cwd, argv, environment presence and run ID) were rejected by pinned hash verification; originals were never edited. This is software/provenance validation, not a new launch or a claim that a signature system exists.

The append-only known-failed disposition preserves the incomplete source unit and raw RUNNING/in_progress evidence. The one-restart gate rejected a second successor in an isolated directory sandbox. Cumulative expenditure remains 177 generations and 342 environment operations. Restart source generation and environment-operation caps (including resets and actions) are 8999 each; all other phase/global ceilings remain unchanged. Worst-case cumulative totals 26756 / 41201 remain below 26988 / 41260.

G2 five frozen evidence hashes match execution SHA 92aae1d9b230cc212c6ec4effc99aa468941e69d. Its smoke path is unaffected; G2 can be carried forward without rerun, but this does not approve the G3 implementation.

Production actor, collector, parser, durable journal, registry and source validator completed a nonempty source fixture with synthetic model/environment edges. A nonempty synthetic renderer test also passes. The report branch outcomes in that test are synthetic fixtures; no real G3/G4 efficacy claim or full genuine G4 validation is made. Passing single-episode coverage misses the second-episode lifecycle defect, clean-process comparator import and persisted trajectory digest issue.

Targeted R19 suite: 93 passed in 10.77s. Full repository suite: 3 failed, 550 passed, 77 errors in 27.71s. Failure/error IDs exactly match the independently tested bf31f3da baseline; there are no new pytest regression IDs. Historical missing artifacts are not the reason for FAIL. py_compile and git diff --check passed.

## Exact record hashes

- r19_b1_g3_source_contract_repair_amendment_v1.json: `62ff158f5739859266664b1db2e323dca6ea0ad3b8e84134ecbe5fd06c847372`
- r19_b1_g3_source_contract_restart_authorization_v1.json: `de634ba310e47d3d49838b8a73d9c6d87f7db87deed042311e3718061a7eb428`
- r19_b1_g3_source_unit_resolution_events_v1.jsonl: `58783ba60b076ee190dccb0875aac65891d7e1c811e00fbe6303ca65896369d9`

## Conditions

- Resolve R19-SRC-01, R19-SRC-02 and R19-SRC-03, then obtain independent review of the replacement exact SHA before real positive preflight.
- No PASS is issued for da7d348 or superseded 51ec074. No launch clearance is issued.
- G2 carry-forward applies only to authentic execution SHA 92aae1d9b230cc212c6ec4effc99aa468941e69d; do not rerun G2.
- Preserve predecessor raw evidence and incomplete unit, including residual RUNNING/in_progress statuses and cumulative physical cost 177 generations / 342 operations.
- One future bounded restart remains contingent on all reviews, real positive preflight and a separate valid launch clearance; prior consumed clearance is never reusable.
