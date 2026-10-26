# SI-S01 engineering-adapter feasibility (read-only)

Status: `FEASIBILITY_ONLY / NOT_EXECUTABLE / NO SOURCE PASS`  
Started: 2026-10-26T11:02:00Z (existing task-directory evidence begins at this time)  
Finished: 2026-10-26T11:58:55Z  
Immutable source reviewed: commit `9bc15b593ec6144915762a2fb1b172e063fe2c48` in `/home/lizening/wt-si-e2-cuda-uuid-compat`. The checked-out worktree itself is at `844cc4b78df1f83e29391ffd5ab861a2d0c0a3fd`; it is **not** represented as the reviewed 9bc commit. Inspection used Git object reads (`git show`/`git grep`) only; no project imports or tests.

## Finding

The immutable engineering implementation is not currently wired to run the proposed one-generation/one-source engineering observation. Its producer is `LocalInference`, not the proposed `LiveProducer` API; it performs a four-prompt synthetic diagnostic and its authenticated permit requires 4 generations and 88 generated tokens. The A96 `Slot`/`Plan` and collector are intentionally synthetic-only, enforce the fixed 96-row plan, and reject live evidence. Therefore neither passing an old source through an A96 slot nor weakening the synthetic-only guard is a valid route.

The current environment helper also does not fit the proposed strict bound as-is: `replay_twice()` constructs two isolated environments and performs two resets plus twelve action steps (14 environment operations). Its `historical_replay` helper consumes a whole supplied event journal, so it is not suitable for this task's first-row/reset-only evidence boundary. No source execution was attempted.

Conclusion: a small, separately gated engineering-only adapter is required before any later execution proposal. This is a design finding, not implementation, source-contract PASS, readiness, or authorization.

## Existing APIs and boundaries observed in the immutable commit

- `runtime_backend.LocalInference.load(permit, ledger)` contains model-load safeguards (authenticated permit, source/module-origin checks, fixed synthetic prompts, input/generation ceilings, CUDA UUID checks, single-byte CUDA context allocation before weights, Qwen/PEFT loading and adapter checks). Preserve these guards; do not bypass or repurpose its four-prompt diagnostic as the one-call protocol.
- `runtime_backend.LocalInference.prepare()` and `.generate()` are the available inference methods. The reviewed commit has no `LiveProducer`, `LiveProducer.load`, or `_raw` interface.
- `contract.Slot`/`freeze_plan` bind the fixed 96 identities and family quotas (35/26/16/9/10). `software_only` requires synthetic evidence; `Collector` and `ProducerAdapter` enforce it before live calls. This plan cannot authorize a historical task.
- `runtime_gate.Permit` requires 4 generations and 88 output tokens, and its authentication binds source identity, clean Git state, authorization, and visible GPU identity. It does not admit the proposed 1-generation/16-token ceiling without a separately reviewed engineering permit.
- `runtime_ledger.EngineeringLedger` records load/construction/reset/step/close/generation events, but does not itself enforce a combined reset-plus-action `environment_operations <= 7` ceiling. A dedicated strict budget check is needed.
- `runtime_environment.ReadIsolatedEnvironment` narrows the environment to one task's game directory and accepts the historical task seed. Its `replay_twice()` helper intentionally runs two fresh instances. A bounded single-pass path would need exactly one construct, one reset and the six saved actions, then close.
- The existing `verify_artifacts(permit)` and `historical_replay(...)` paths read/hash or parse full trajectory/event artifacts. Do not call them under a first-row-only authorization. Bind the already certified full-artifact hashes by reference; consume only the authorized first trajectory row and its referenced reset event locally.

## Historical first-source evidence (bounded read)

The captured first trajectory line is 35,486 bytes including its newline and hashes to `465bff755ba34c18acca299470cd7c3a40455cb395df3e6fe43eee99119a7c73`. Identity is `pick_and_place_simple-Pencil-None-GarbageCan-316/trial_T20190907_165839_449092`; task-id SHA-256 is `7a05bf94153d050578cfd5c5d3d5b2b8fe5b20e6981e16311c65bc016572cccb`; train split, nominal seed 30000, schedule index 0, six saved actions. These are historical provenance facts, not a new task selection.

The referenced reset is event-ledger sequence 2, event id `5a8c49daf6691ebd1bd644e12662bc66894d93153618e9488bce7e4db27f7a31`, raw event line 3,425 bytes, SHA-256 `c7c44a37a4717dfdd1241dff06ced3a7a19aace35e96cb8383301a77fa93b80f`. The reset/task/seed/observation bindings and first-step pre-observation, valid-action map and selected-versus-executed action cross-checks were true in the bounded capture. First-step metadata reports parser status `selected`, valid action, mode `indexed_admissible`, 267 input tokens, 5 generated tokens, 5 token IDs and 10 valid actions. Hash-only prompt/output/token-array evidence is in `HISTORICAL_FIRST_SOURCE_FIELDS_V2.json`; raw prompt, output, action text and token values are intentionally not reproduced here.

Important limitation: the saved reset evidence records nominal seed 30000, but does not record the internal TextWorld pool seed or game RNG counter. Event sequence 2 is a ledger sequence, not an environment counter. Consequently an exact claim about those internal RNG states is unsupported by the historical record and must remain unresolved; do not infer them from the nominal seed.

## Minimal adapter needed (proposal only)

1. Add a distinct, immutable engineering permit and run identity that is not an A96 `Slot` or scientific schedule. Require explicit authorization, exact task identity/hash, exact source commit, clean tree, bound cached model/adapter/runtime hashes, trusted device UUID and process ownership, and a fresh absent output path.
2. Reuse existing model loading and UUID/PID/PEFT/tensor safeguards, but provide a one-prompt preparation/generation route with hard limits: one model load, one generation, at most 16 generated tokens, at most 8,192 input tokens, one one-byte context probe, and 600 seconds. Do not use the four-prompt `LocalInference.load` diagnostic unchanged because its gate requires 4/88.
3. Provide one explicit historical replay path: one environment construction, one reset, exactly six saved actions, and close. Enforce a combined maximum of seven reset/action operations in a fail-closed ledger. Do not call `replay_twice()` or full-journal `historical_replay()`.
4. Capture raw argv/environment allowlist, PID/device identity evidence, source and input hashes, each physical operation/generation/token count, timestamps, stdout/stderr/real exit code, and post-run hashes. Stop on any missing/ambiguous PID-to-device ownership, UUID mismatch, input drift, budget overrun, RNG provenance claim, or partial external operation; no retry.

The adapter must not silently convert this engineering observation into an A96 sample, source acquisition, training row, or scientific result. A later independent source review and a separate execution authorization would still be required.

## Evidence inventory

- Static source API receipt: `STATIC_API_RECEIPT.json` (selected immutable Git-object file hashes and symbol inventory); command receipt: `STATIC_SOURCE_COMMAND_RECEIPT.json`.
- Bounded original-source captures: `HISTORICAL_FIRST_SOURCE_FIELDS.json` (preserved first attempt) and `HISTORICAL_FIRST_SOURCE_FIELDS_V2.json` (additive safe-field capture); command receipts retained separately.
- `HISTORICAL_SUMMARY_INSPECTION_ATTEMPT.json` records one exploratory summary command that exited 1 because it queried a V2-only field in the V1 artifact. It did not modify evidence or read additional scientific content; preserve the failure honestly.
- The earlier `INPUT_HASH_READINESS.json` belongs to the prior input-readiness task and is not promoted as a source PASS.

No model, tokenizer, CUDA, ALFWorld, project validator, test suite, preflight, supervisor, or scientific execution was invoked for this feasibility report. No source, historical evidence, shared index, or provenance repository was modified.
