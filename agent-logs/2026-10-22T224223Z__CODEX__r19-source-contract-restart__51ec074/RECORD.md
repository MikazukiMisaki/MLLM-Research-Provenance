# R19-B1 source contract repair and controlled restart

- Agent/task: Codex; integrate the adopted R19 source producer/consumer contract repair, validate it in the full repository, obtain exact-SHA independent review, then follow only the package's bounded restart procedure.
- Start UTC: 2026-10-22T22:24:00Z (continuation checkpoint); record opened 2026-10-22T22:42:23Z.
- Current status: READY_FOR_EXACT_SHA_REVIEW; restart gates pending. No new G3 preflight or live G3 has been started in this task.
- Scientific repository: `MikazukiMisaki/Alfworld-Self-Improvement-Project`.
- Starting source: `bf31f3da430ffc35bd17fc380e1752adce6d1467`, branch `codex/r19-recovery-duration-v1`.
- Current source: `da7d348ffd3677d619dd31357e1e1e3cca28c9ec`, branch `codex/r19-source-contract-repair`; clean after commit.
- Remote source branch: pushed to `origin/codex/r19-source-contract-repair`; `git ls-remote` matched the current local commit exactly. Commit `51ec074cec6c2c2a7b1ecd64e0da33bc446a7e54` was superseded by this follow-up that binds the predecessor's actual supervisor command, working directory, receipt hashes, run identity, and clean Python-environment evidence.

## Scope and changes

- Verified and followed the attached `R19_Source_Contract_Repair_Package.zip` (`SHA256 20f9414a2d80a48060247368afcb9b9f07bc0573f591fd28d4f19213c8c23813`) and its `START_PROMPT.txt` (`SHA256 4cd8802385f2dc08bf51aaca7367a43d84e3433d2f55b1908b3c631e3e391b44`). The user explicitly adopted the one bounded restart described there.
- Corrected `_collect_one_source` to consume the existing mapping returned by `actor_generation`, without changing parser, prompt, decoding, action-selection, failure-status or horizon semantics.
- Corrected `actor_generation` to retain `source_generation` for the task actor while retaining the established SFT suffix event operation.
- Added restart-only dynamic phase ceilings so the previous completed source generation and reset are debited: source generations/resets each have 8,999 remaining; other phase ceilings and global ceilings remain unchanged. The amended exact fingerprint overlay covers precisely the four affected production methods: the two producer/consumer methods and the two cap-reservation methods. No G2/G2 smoke rerun.
- Added a pre-action comparison of the preserved first-source state, valid actions, prompt/rendered prompt, raw output, token IDs/counts/settings, parser status, action ID/action, and action map. A mismatch writes its comparison receipt, then stops before an action; no automatic retry is allowed.
- Added G4 validation for the comparison sidecar, its source-event binding, and its position before the first action. Added versioned source repair/restart records and an append-only known-failed disposition. Original failed events, registry, manifest, supervisor receipts and prior review remain unchanged.
- Frozen protocol, source schedule and exclusions remain unchanged at SHA256 `3d7d1865c807d12276a8109b06c55da4e9182df0ca05a0b5463f8128dd03e122`, `0be460359fe43193e73f8cb55a8fb19fdba02ea70e3d0809ec5978fad21c8948`, and `70447bba1b2a944d52ab9b4041b2d6ff3d865f4f0abd55d655214c8060ff5367`.

## Evidence and verification completed

- Predecessor failure audit independently records exit 1, four authentic ledger events, one completed generation (267 input + 5 generated tokens), one reset, zero steps, zero incomplete operations, and zero source completions. Cumulative cost remains 177 generations / 342 environment operations, including G2 and the failed predecessor.
- Production restart-record loader was run without mocks against the actual predecessor ledger, unit registry, failure-audit JSON and supervisor receipts. It passed the exact evidence, unit-disposition, four-method fingerprint and remaining-cap checks; recomputed predecessor snapshot SHA256 was `d85d870bfddbad4eb62116d3d5de54a4b7fd4f250634af1c1ed89958e4c400b8`.
- `py_compile` passed for the modified production modules and test modules.
- Full targeted R19 suite passed clean after commit: `pytest -q tests/test_r19_source_contract.py tests/test_r19_entrypoint_repair.py tests/test_r19_g3_authorization.py tests/test_r19_recovery_duration.py`; 93 collected, 93 passed, exit 0. The 16 source-contract integration cases use synthetic generator/environment boundaries but real `actor_generation`, collector, parser, durable journal, unit registry, production source validator and synthetic report renderer. Restart mismatch rejection and remaining-cap enforcement are tested.
- An earlier run of the CLI test while the implementation was uncommitted failed closed because the worktree was dirty; after commit, the same suite passed. The extra supervisor-binding commit itself was followed by a clean rerun: 93 passed. No scientific side effects occurred.
- A first pytest attempt with the default Miniconda interpreter exited 1 because that interpreter has no pytest module; no package was installed or changed. The fixed experiment interpreter was used instead.
- After `da7d348`, the production restart loader was run in a clean new process against the authentic predecessor artifacts and passed all predecessor, supervisor argv/cwd/environment, fingerprint, disposition, and 177/342 cap checks.
- Scientific execution in this task so far: 0 model loads/generations, 0 ALFWorld constructions/resets/steps, 0 fresh-task consumption, 0 held-out use, 0 training.

## Pending gates and next step

- Exact-SHA independent review for `da7d348ffd3677d619dd31357e1e1e3cca28c9ec` has been requested through `codex queue` (messages `01a165ca-c1b1-7872-b0c6-b032d433cf2d` and `01a165cb-6830-73a1-8d56-cfad1d9b690f`); no decision has been received at this checkpoint. Do not construct a passing local gate or start a supervisor preflight until the reviewer returns an authentic PASS for this exact commit and confirms the G2 carry-forward, unchanged treatment semantics, known-failed disposition, four-method overlay, one restart, first-source comparator and cumulative caps.
- After review PASS: create a new ignored `configs/local/` gate bound to the exact commit, frozen authorizations/hashes, review artifact, G2 execution SHA `92aae1d9b230cc212c6ec4effc99aa468941e69d`, predecessor and local evidence paths. Run the authentic positive supervisor/CLI preflight only. If it passes, follow exactly one bounded G3 restart, starting from 177 generations / 342 operations, compare before the first action and stop on mismatch/failure. If G3 finishes, run report-only G4 on its real provenance bundle. Never rerun G2 or automatically retry G3.
- Final completion work: update this record, hash inventory and provenance index; scan for secrets; commit only this task's provenance-safe files; push to provenance `main`; verify the remote SHA. Preserve unrelated existing untracked provenance paths.

## Commit and artifact references

- Scientific commit: `da7d348ffd3677d619dd31357e1e1e3cca28c9ec` (supersedes `51ec074cec6c2c2a7b1ecd64e0da33bc446a7e54` for review).
- Remote scientific branch `origin/codex/r19-source-contract-repair` verified to point to `da7d348ffd3677d619dd31357e1e1e3cca28c9ec`.
- Predecessor failure audit: `/home/lizening/research-notes/agent-logs/2026-10-22T191409Z__ASTRA__r19-g3-failure-audit__3d1ccea7/failure_audit.json`, SHA256 `8eb1248c1d863674119813ba1f90ba3ca6834bb1906cb2aa67acc6a4e087fe34`.
- Exact test command and checkpoints are summarized in `commands.log`; per-task hash inventory will be finalized after all authorized gates complete.
