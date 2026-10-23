# RECORD — R19 exact-SHA Phase1 zero-science preflight

## Task and status

- Agent/operator: Codex Luna, Experiment Operator & Provenance Owner.
- Task: stage the independently reviewed R19 source-contract candidate and execute exactly one Sol-released production `preflight_only` supervisor invocation.
- Start UTC: `2026-10-23T00:05:54.619257Z` (release issue time; this is the earliest persisted task marker).
- Finish UTC: `2026-10-23T00:16:02Z` (final record/hash inventory complete; provenance commit/push immediately follows).
- Status: **PREFLIGHT_ONLY_PASS**. Live launch clearance is **NOT_GRANTED**; fresh user scientific authorization is **NOT_GRANTED**. No live launch, G2 rerun, or G4 was performed or released.
- Authoritative one-preflight release: `/home/lizening/research-notes/agent-logs/2026-10-23T000029Z__SOL__r19-phase1-preflight-release__2da980f_669620/phase1_release.json`, SHA256 `d634514f0d177ff7b6b2712dd160fa0d1c86ba193e3e377260c5bc872e27ae46`.

## Scientific repository and staging

- Repository: `/home/lizening/wt-r19-recovery-duration-v1`.
- Starting state: branch `codex/r19-source-contract-repair`, HEAD `da7d348ffd3677d619dd31357e1e1e3cca28c9ec`, remote ref matched; one expected untracked `R19_IMPLEMENTATION_ONBOARDING.md`.
- Ending state: detached HEAD `2da980f631badc25086d12db60d128ff507d3ae6`; remote `codex/r19-source-contract-review-fixes` matched this SHA; tracked and untracked (non-ignored) worktree clean. No reset, clean, source edit, test edit, or ignore-rule edit was performed.
- The onboarding report was verified at SHA256 `27be0ca4c3e5abffa4fa492aaf47bf087328f41718fcc5f774c43fdf5b1c4e7e`, mode `0644`, then moved to `preserved/R19_IMPLEMENTATION_ONBOARDING.execution-original.md`. Both it and the previously preserved copy still hash identically. The original location is absent; the report is recoverable byte-for-byte from the preserved copy.
- The reviewed gate was copied without modification to the ignored local path `configs/local/r19_b1_g3_gate_2da980f_phase1.json`, SHA256 `c285692615eaaf1c7cb7139b0417528022db6ee03c510de13f881d126f14415e`. Earlier local gates were not edited or used.

## Release, review, authorization, and frozen-input bindings

- Independent exact-SHA review: `85a694f24da347dcb0e6f09f4fe0d33afefb46abf1d5b0063361870c3fe7820b`; unchanged and reverified.
- Known-failed source-unit adjudication: `3abea8efc2bd9d88677d71031aef0a21e905e6dd7b3ed75d06f1486d4c6718e0`; unchanged and reverified. Original source episode remains incomplete; original failure registry/manifest were not rewritten.
- Release gate file SHA256 `c285692615eaaf1c7cb7139b0417528022db6ee03c510de13f881d126f14415e`; resulting local gate matches exactly.
- Canonical supervisor argv SHA256 `7c1519ccb6f34683ee1ac09d4757d8a00bc225576b6a4f8370736790a2b9235b`; canonical child argv SHA256 `eea6b0032ca714ec011b3d48f9c6a1a1bec3879560910ae77ce3da1c924aaa68`; the exact arrays were loaded from the immutable release JSON files and passed to `execve` without shell argument reconstruction.
- Environment set/unset file SHA256 `59fbf34e59cb02fbe1a06dc11cff6b966cde3ed2a90805a6da6368d630b5c03b`; canonical object SHA256 `f6814cb23d94fcacb28f73f0ce786192e48c425469d942941450f2c940a02028`. Supervisor-recorded effective allowlist canonical SHA256 `84a59e93bd64b751ec5e1baad246314776562158bdb46019a864d5dba52697c0`. `PYTHONPATH`, `PYTHONHOME`, `VIRTUAL_ENV`, and stale `R19_*` identity/context fields were removed before launch; supervisor injected a fresh run identity.
- The source contract amendment is the reviewed exact-SHA value `1b94a0ed37284d37a21d07985a5ba18de25ea4e11f9ffa553ca624c9739aee1e`. The historical runtime environment-manifest raw digest used was the corrected `81ea3b3aea86a850c70d88846f1ce12dfb276cca34aacb9f598ea13e733bf902` (not the earlier typo).
- Before preflight, independently rehashed: all 12 pinned model snapshot files, all 11 adapter files, all 254 underlying files (game + trajectory) for 127 scheduled TRAIN identities, and frozen protocol/baseline/amendment/authorization/schedule/exclusion/config inputs. Hashes matched the Sol read-only input verification record, SHA256 `5f5f10b3fc199b5f7e760d33fc03067f0b36a84f4042a531cd5d3a460c2d04e6`; runtime preload matched `64ebf4667da70dc4acd0a49b645bb6b6d4c3e1fe5d3e8e6351a8bf66f148ab9a`.
- Post-run protected G2 evidence and failed G3 output/registry/supervisor receipt hashes matched their frozen values (listed in `FILE_HASHES.sha256` where applicable). G2 was not rerun.

## Actual supervisor and preflight result

- Record directory: `preflight_supervisor/`.
- Run ID: `a9ca70cb082b4f2387d242664031b0bc`; supervisor PID `776941`; child PID `776946`.
- Evidence class: `preflight_only`; supersedes failed run `3d1ccea7e97f4727abf8e216ac6ec498`.
- Authentic child return code: **0**, `exit_code_source=subprocess.returncode`; supervisor status `completed`; receipt status `PREFLIGHT_ONLY_PASS`.
- `runner_exit.json` SHA256 `7323984be1fbac09a88586feeda2e98a4ab13be1c72110ec5fb2e22bce46af6c`.
- `supervisor_status.json` SHA256 `9ae5417d129178a64cc21c5ba50f38f1a3df037ba1231e866964c8ba391308de`.
- `launch_context.json` SHA256 `aa6bf1f1dc18ec7d0c52c1b9afa069973ca9304fdf917eab2241f0b75f21546a`.
- `runner.log` SHA256 `9652604e8e033ea62fac1436f5bd9f4d1a6528ab2a8e8326b431b3a8db81f392`.
- `pilot_preflight_receipt.json` SHA256 `aed33e7f813a7ce2992b7860fbef59cabe814e31543c3e8eb1dcac5b95390574`.
- Receipt bound source SHA `2da980f631badc25086d12db60d128ff507d3ae6`, gate SHA above, review and authorization hashes, protocol SHA `3d7d1865c807d12276a8109b06c55da4e9182df0ca05a0b5463f8128dd03e122`, model revision `b968826d9c46dd6066d109eabc6255188de91218`, adapter SHA `6e403d85b150a74dfcc176f1f180ce4baf6fdacd922d2f96b3ceef0a21100f11`, source schedule/exclusion hashes, and 127 scheduled TRAIN tasks.
- Production module origins were both inside the exact reviewed checkout: `scripts.run_r19_experiment` and `scripts.analyze_r19_recovery_duration` resolved under `/home/lizening/wt-r19-recovery-duration-v1/scripts/`.
- All recorded side-effect counters were zero: model objects loaded `0`, generations `0`, ALFWorld instances `0`, resets `0`, steps `0`, fresh TRAIN attempts `0`, scientific units `0`.
- Output sentinel `/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_preflight_2da980f_20261022T235413Z` remains absent. No execution event/branch output was created. Supervisor `artifacts_complete=false` is expected for this zero-science preflight.
- After completion, no R19 runner/ALFWorld process was observed; GPU reported 0% utilization and 14 MiB used of 46,068 MiB.

## Physical cost and boundaries

- Recounted from authentic completed event ledgers: **177 generations**, **342 environment operations** = **330 non-reset + 12 resets**. The preflight added zero to both totals.
- Original G3 failed predecessor had one completed generation, one reset, zero environment steps, and zero incomplete external operations; its unit remains incomplete/known-failed under the separate adjudication.
- Held-out tasks `0`; model loads/generation `0`; ALFWorld construction/reset/step `0`; fresh source units `0`; G2 reruns `0`; live launches `0`; G4 runs `0`.
- No scientific tests were run in this task. The real production supervisor + CLI preflight was the only execution check.

## Provenance and next dependency

- Provenance repository at task start: local/remote `main` SHA `d51b434cb4c146daa97b3fdbeac27a18e1e6cbfc`.
- Own task files: this record, command log, file-hash inventory, preserved onboarding bytes, and authentic supervisor evidence. The scientific worktree contains only the new ignored local reviewed gate and is left at the clean reviewed detached SHA, as required on success.
- No independent live launch clearance exists and no fresh user scientific authorization exists. Next step is independent review of this actual preflight evidence. Wait for separate clearance and fresh explicit user authorization before any scientific execution; no automatic live transition.
- The final publication commit is reported to Sol and in the operator handoff; its exact SHA is resolvable from Git history for this record because a commit cannot contain its own final SHA.

## Final publication checkpoint

- Provenance baseline before this publication: local/remote `main` matched `d51b434cb4c146daa97b3fdbeac27a18e1e6cbfc`.
- This record and its own task artifacts, `FILE_HASHES.sha256`, and one `INDEX.md` row are the only intended staged paths. The final publication commit is deliberately not embedded in itself; resolve its exact SHA from the commit containing this `RECORD.md`, and verify local `main` equals remote `origin/main` after push.
- No inventory/index changes or files from other agents are staged.
