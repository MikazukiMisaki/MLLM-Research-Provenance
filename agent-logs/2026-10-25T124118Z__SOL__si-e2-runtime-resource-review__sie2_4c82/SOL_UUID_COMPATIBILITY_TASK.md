# SI-E2 UUID compatibility follow-up — implementation only

Root scope ruling: user authorizes real runtime adaptation and GPU resource verification. The dfc full engineering probe failed and its authorization is consumed; do not rerun it. A separate reviewed pure identity diagnostic now saved the exact installed Torch representation. This task authorizes code/software tests only, no CUDA context, 8B/model/world calls or scientific execution.

Create an isolated new worktree and codex/si-e2-cuda-uuid-compat branch from frozen dfc00e49d1ef4d48453d2331507429f8a0c7bbc5. Preserve dfc branch/worktree and finalized handoff bytes. Read required project instructions. Own a new unique provenance directory; do not edit shared INDEX/inventory or stage/push provenance.

Actual input evidence: /home/lizening/research-notes/agent-logs/2026-10-25T141400Z__LUNA__si-e2-cuda-identity__dfc00e49_2e79/identity_run/pre_allocation_identity.json and identity_observation.json. Torch 2.6.0 returns torch._C._CUuuid whose str is b08bc603-ebdb-787d-b5b6-ec796ea3022a; authentic NVML identifier is GPU-b08bc603-ebdb-787d-b5b6-ec796ea3022a. Direct string comparison in runtime_backend.py115/137 rejects identical UUID bytes. Root separately confirms this representation mismatch.

The later tiny allocation ALSO shows NVML compute PID3082604 versus local PID837631. Their identity mapping is NOT PROVEN. This is an independent unresolved execution-context blocker, not permission to accept foreign/unknown PIDs.

Allowed minimal source changes:

1. Add strict UUID compatibility comparison for observed canonical 36-character CUDA UUID versus NVML GPU-prefixed canonical UUID. Compare full UUID identity; reject missing/empty/malformed/other UUID/MIG/ambiguous values. Do not compare name, ordinal, prefix substring, or free memory as a substitute.
2. Before the first identity comparison, append/fsync actual observed value, type, repr and expected value into the engineering journal so a future stop preserves the concrete identity evidence. Preserve actual package/source bindings and existing no-model-before-own-context order.
3. Use the same strict comparison at the later post-load assertion.
4. Add relevant production-function tests for observed installed wire, differing/malformed/unobservable values, raw pre-assertion evidence durability, and continued refusal of the captured unmapped host PID. No new runtime driver, scheduler, treatment, prompt, parser or training changes.

No changes to inspect_gpu allowed-pid/UID semantics, foreign-process stops, NVML raw receipts, physics counters, existing scientific data, frozen science, task partitions or consumed authorization. No runtime API fallback that waives ownership. Do not claim runtime readiness from this repair.

Run new/focused software tests and comparable full suite in a clean committed candidate, clear inherited Python settings and CUDA visibility, use deliberate source binding for pytest as existing independent baseline. No new failure/error IDs relative to883/3/77. Preserve raw real subprocess exit evidence. Freeze and push a new exact SHA without force; return delta, method hashes, test results and publication manifest. Root independently reviews exact SHA; no actual probe/retry until a different reviewed execution context and fresh root engineering authorization exist.
