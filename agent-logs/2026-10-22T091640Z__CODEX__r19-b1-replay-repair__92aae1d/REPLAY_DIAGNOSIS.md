# R19-B1 G2 replay repair diagnosis

## Finding

The R8-F16 public trace in the failed run matches the retained R9/R8 public
reference. The failure was in the production validator's representation of
the last-four-transition context, not an ALFWorld transition, hash, task,
seed, action-order, or horizon mismatch.

The earliest mismatch is
`$.recent_context_k4[0].action` at public transition index 14. The frozen and
recorded value is `look`; the pre-fix validator reconstructed it as the string
`action`. Its paired result field was likewise reconstructed as
`resulting_observation`. `contexts` was already a list of dictionaries, but
the list comprehension unpacked each dictionary as a pair, which iterates its
keys. The direct K4 equality check therefore failed first and short-circuited
the later K4-hash and complete-prefix-hash checks.

## Field-level comparison

| Check | Expected / observed | Result |
|---|---|---|
| Task, TRAIN split, seed | Same task ID, `train`, seed `20055` | PASS |
| Game / trajectory-data bytes | `a7e89a…ffc1822` / `71a136…76b2c6`; local bytes match the frozen R19-B1 inputs | PASS |
| R7 identity and prefix | Source trajectory hash `3d1fd2…3b1a7`; decision index 18; 18 commands; remaining horizon 32 | PASS |
| Reset | Expected and observed task, seed, observation, and ordered action list match | PASS |
| Transitions 0–17 | Each action, action ID/map, pre-state, history, result observation, resulting ordered actions, reward, done, and truncation match the historical R9 signature and raw ledger | PASS, 18/18 |
| Endpoint | Observation hash `7bc36d…1200fa`; 43-command ordered map hash `67c139…284ed` | PASS |
| Public K4 trace | Expected and raw-ledger K4 hash `7daa7e…6dfa8` | PASS |
| Pre-fix validator K4 representation | Four entries each became `{action: "action", resulting_observation: "resulting_observation"}`; reconstructed hash `2e8ed5…f4d37f` | FAIL — first divergent check |
| Complete public prefix | Frozen, historical R9, and raw-ledger recomputation all equal `15e600…0dee0` | PASS |

The complete field-level expected/observed values, 18 operation-event pairs,
hashes, and status flags are in [`replay_diff.json`](replay_diff.json).
The retained full public reference is the R8 manifest plus the complete R9
replay signature; the ALFWorld task `traj_data.json` is input metadata, not a
step trajectory. No missing observation was filled from an expectation.

## Physical operations and the enclosing unit

The original raw ledger has 38 events: 19 operation starts and 19 completions
(one reset and 18 steps), with no incomplete pair. The runner's reset and step
calls in this smoke path go through the journaled `record_reset` and
`record_step` wrappers. There are zero generation-start/completion events,
zero branch rows, and the supervisor records subprocess exit 2 without
interruption. Thus the physical operation results are known; the enclosing
`prefix_replay_and_initial_recovery_attempt` unit did not complete and remains
`in_progress` in its untouched original registry.

[`UNIT_ADJUDICATION_PROPOSAL.json`](UNIT_ADJUDICATION_PROPOSAL.json) is only a
snapshot of the proposed disposition. Exact-successor review returned PASS;
the reviewer-approved `KNOWN_FAILED_REPLAY_VALIDATION / NO_BRANCH_EXECUTED`
resolution is now appended in [`unit_resolution_events.jsonl`](unit_resolution_events.jsonl).
The original event ledger, registry, execution manifest, runner log, and
supervisor receipts remain unchanged.

## Repair and regression evidence

Commit `92aae1d9b230cc212c6ec4effc99aa468941e69d` fixes K4 reconstruction by
preserving the already-formed dictionaries. It also binds the supplied seed to
the frozen R8 seed, records structured failure evidence before a public-prefix
comparison raises, and leaves the frozen replay comparisons fail-closed.
No frozen hash, baseline, protocol, task, quota, exclusion, prompt, model, or
environment definition changed.

The exact production method passed on the authentic saved reset and all 18
saved transitions with only the environment boundary mocked. Tampering with
the current observation, ordered action mapping, older history, K4 window,
reset task identity, seed, or horizon was rejected. See
[`production_validator_regression.json`](production_validator_regression.json).
The R19 focused suite passed: 47 tests; compilation and `git diff --check`
also passed. These are offline validator checks, not a live replay or G2 pass.

The current R19-B1 preload runtime, all 12 pinned base/tokenizer files, all 11
adapter files, and the R8-F16 game/trajectory-data files were revalidated
without loading weights or initializing ALFWorld. The default conda cache
fingerprint differed; the read-only check explicitly bound the local cache to
the already frozen runtime fingerprint and exact model bytes. Full details are
in [`identity_revalidation.json`](identity_revalidation.json), and the old
ledger was revalidated by the production event-ledger validator in
[`event_ledger_validation.json`](event_ledger_validation.json).

## Scope and expenditure

The prior G2 remains `G2_FAIL_BEFORE_BRANCH_ARM_EXECUTION`, authentic exit 2.
It consumed 19 physical environment operations, zero model generations, and
zero branch executions. This offline diagnosis used zero physical operations.
The original campaign cap therefore has at most 381 environment operations
remaining. The frozen successor-smoke plan is capped at 374 operations, 228
model calls, and six production arms, so it fits within the remaining original
400 / 408 / 8 ceilings if all retry prerequisites pass. No successor G2 has
started. G3 and fresh TRAIN tasks remain unauthorized.

The successor commit is pushed to the original branch and its remote ref
matches. Exact-SHA independent review passed and the append-only unit
resolution is recorded. A single successor G2 attempt has not started; it is
eligible only under the already approved section-6 conditions, with the
previous run and cumulative costs bound into its gate manifest. No second
retry or G3 is authorized.
