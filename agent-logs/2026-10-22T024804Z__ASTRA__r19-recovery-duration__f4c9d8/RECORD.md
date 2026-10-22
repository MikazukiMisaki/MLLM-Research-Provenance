# R19 recovery-control duration opportunity pilot

- Agent and task: ASTRA; implement and validate the narrowly scoped R19 duration-opportunity protocol.
- Start UTC: 2026-10-22 02:48:04 UTC.
- Finish UTC: 2026-10-22 03:24:53 UTC.
- Status: BLOCKED at G1; no G2/G3/G4 execution.
- Scientific repository: `MikazukiMisaki/Alfworld-Self-Improvement-Project`.
- Starting branch/SHA: `codex/progress-aware-recovery` / `4f5c2e18e0dfdf48e9471fcba0a3ee715be3ca3b`.
- R19 branch/worktree: `codex/r19-recovery-duration-v1` / dedicated isolated worktree (local path omitted from committed provenance).
- Ending SHA: `fac6a92081cab84e23d2f4630a7f2ab6d18f8baf` (G0 candidate; G1 pending).
- Provenance repository: `MikazukiMisaki/MLLM-Research-Provenance`, branch `main`.

## Scope and gates

User-authorized work: G0 inspection, protocol freeze, additive implementation, and synthetic tests, followed by exact-commit independent review and at most six previously consumed development-task live smoke checks. Fresh TRAIN data collection and duration pilot are authorized only after G1/G2 pass and all frozen preflight evidence is verified. No held-out use, training, learned selector, DPO/ORPO, new model/environment, FACT/CARD changes, or automatic budget expansion.

## Evidence

- Initial local and remote accepted scientific branch SHA: `4f5c2e18e0dfdf48e9471fcba0a3ee715be3ca3b`.
- Remote `codex/progress-aware-recovery` was fetched and `ls-remote` matched the accepted SHA.
- New R19 branch was created from the accepted SHA; no pre-existing local or remote R19 branch was found.
- Repository and provenance instructions read; detailed command/test evidence will be appended.
- The model-free preflight inventoried 3,553 complete TRAIN task/trial records across six families; 2,642 identities were excluded; 127 records were frozen in the source schedule with family counts 30/0/30/30/30/7. The 1,833 incomplete directories were not selected.
- Preflight v2/v3 outputs are byte-identical across the four manifests. Canonical schedule, exclusion-manifest, preflight, and protected-manifest file hashes are recorded in `R19_PREFLIGHT.md`.
- Protected historical-file verification passed at the accepted base: 443 expected tracked files, zero changed/missing/newly tracked files.
- Focused synthetic tests: 19 passed; protocol validation, Python compilation, and `git diff --check` passed. Full historical suite using the accepted base with the R19 source overlay completed at 100% with exit code 0.
- Exact binomial examples matched frozen values. SciPy is unavailable in the pinned environment; no dependency was installed. Historical Qwen3-8B revision equivalence remains unproven.
- Scientific model calls: 0. ALFWorld reset/step calls: 0. Held-out use: 0. Training runs: 0. External paid model calls: 0.
- Live smoke and pilot were not run. Candidate explicitly identifies the live-smoke harness and G3 pilot driver as NOT_IMPLEMENTED; no gate is claimed passed beyond static checks.
- Independent exact-commit review: BLOCKED at `fac6a92081cab84e23d2f4630a7f2ab6d18f8baf`; machine protocol SHA-256 `3d7d1865c807d12276a8109b06c55da4e9182df0ca05a0b5463f8128dd03e122`; protocol document SHA-256 `3839d10c07f67c03e0a3c8d9e7b8f210f030c58533c87aab9acadce470ee48a1`. Independent Codex reviewer made no file changes or scientific calls.

## Changed files and commits

Scientific implementation commit: `7014282d26d8484ae8826fb76dc0e1250a5c241d`; documentation/hash correction commit: `fac6a92081cab84e23d2f4630a7f2ab6d18f8baf`. The dedicated branch push was verified: local and remote branch SHA both equal `fac6a92081cab84e23d2f4630a7f2ab6d18f8baf`. The accepted base branch was not changed. Provenance repository checkpoint before this task upload: `91df5bc31da3b2f294c3ed50001d689796ccff35`.

## Final decision

Independent review verdict: BLOCKED. P1 findings: no live-smoke/pilot execution path; analyzer does not bind outcomes and costs to authentic operation events or require authentic exit codes; required SciPy exact-test cross-check unavailable; historical model-revision equivalence unproven. G0 was not fully closed and G1 did not pass. G2/G3/G4 were not run. Stop without consuming fresh tasks; resolve the listed review blockers, any required user-approved model-revision deviation, and dependency evidence before requesting a new exact-SHA review.
