# SI-M1 Read-only Run Preparation

Status: PREPARATION_ONLY / NOT_READY_TO_START. No experiment, model load, CUDA initialization, ALFWorld construction/reset/step, tokenizer, project validator, preflight, or training was run in this preparation.

## Scope and identity

This record concerns the proposed five-case SI-M1 single-step probe, not a rerun of the completed 96-task A96 source campaign. The immutable design and cross-review remain design-only. The A96 source run is historical evidence and its source-only NO_GO interpretation remains unchanged.

Current candidate worktree: /home/lizening/wt-si-five-case-probe, branch codex/si-five-case-probe, base HEAD f1e0d56a1be2a65876bbec5b8950fb76cda3eace. At inspection it had untracked configs/experiments/si_m1_single_step_v1.json and src/self_improvement/si_m1/. No candidate implementation commit/SHA was submitted or bound; these files were not edited, staged, or included in a review claim.

The current reviewed design is /home/lizening/research-notes/agent-logs/2026-10-27T024153Z__ASTRA__minimal-recoverability-design-review__e6fb570f/MINIMAL_RECOVERABILITY_DESIGN.md (SHA256 c1c8e3eca3b812f633c4cb2531533fc5a2785bc3870ae5c7f5095deb5f4abeb2) and DECISION.json (SHA256 cffbbeeace7d16ae2cd2b7ea6304be4fe6e08ae06779b3d582b4f738236bfbbc). Sol's ROOT_DESIGN_CROSSREVIEW.json is SHA256 7053edd96a7e88c62430b1d7836edbda5d188098db6ea3efb652cdc5c34c5e74. It says ASTRA_GO_DESIGN_ONLY_ROOT_CROSSCHECK_CONCURS, future_execution_ready=false, and engineering_budget_frozen=false. No exact-SHA implementation review, new positive preflight, or distinct launch clearance for this five-case probe was observed. The old A96 clearance is source-only and is not reused.

## Read-only evidence captured

- Fresh SHA256 rehash completed successfully for all 12 files in the cached Qwen3-8B snapshot and all 11 files in the frozen P0 adapter. The complete observed hashes are in MODEL_ADAPTER_SHA256SUMS. This verifies file bytes only; neither model nor adapter was loaded.
- The five selected existing task game/traj_data pairs were rehashed; observed values are in CASE_ASSET_SHA256SUMS. No ALFWorld instance was constructed and no task body was expanded by this rehash.
- The original A96 event ledger and source trajectories were rehashed and matched their accepted historical hashes. Existing Sol/Astra review evidence binds the 40 referenced source-event IDs and five anchor chains; this preparation did not reinterpret future outcomes or expose hindsight suggestions to a teacher.
- The shared-resource contract was rehashed: configs/experiments/si_s01_shared_resource_v1.json SHA256 d908573f0c6d9518aec0a9b6b0a48c24648a26c3c708652b185a7cfe7b7e2489. It is SOFTWARE_CONTRACT_ONLY_NO_AUTHORITY and specifies 24 GiB allocator cap, 28 GiB pre-weight global-free minimum, 2 GiB later global-free minimum, native allocator, non-exclusive shared GPU, and no NVML-to-local-PID ownership assertion.
- Final NVML snapshot at 2026-10-27T03:32:50Z showed an A40 with 4,599 MiB free and 100% utilization, below the 28 GiB pre-weight threshold. Six compute PIDs appeared in NVML but were not visible to the local ps query; their ownership is unproven and no process was interrupted.
- Final disk snapshot at 03:32:50Z: /home had 401,220 KiB available (about 392 MiB; 100% capacity). /tmp had 177,974,916 KiB available (about 169.7 GiB), on the writable overlay filesystem. /tmp is mode 1777, root-owned, sticky; a fresh private directory can be created at launch with umask 077 and mktemp -d, then verified mode 0700. No private directory or scientific output directory was created here. Same-filesystem temp output/archive staging is possible only within that future private /tmp directory; current /home space makes large local archival/publication staging unsafe.

Exact sampled values, commands, and output summaries are recorded in READ_ONLY_RECEIPTS.md. Input bindings and hashes are in CURRENT_BINDINGS.json and the two checksum manifests. These are preparation snapshots, not an execution gate.

## Run envelope, if later independently released

The design fixes five post-hoc development anchors C088, C091, C093, C094, and C095 with replay depths 11, 8, 16, 12, and 8. Each case is one fresh game instance, pool seed 42, one reset with seed 42, exact action-by-action replay of its fixed prefix, two teacher generations (Stage 1 then Stage 2), at most one selected action, then end that case. No replay_twice, extra seed, second reset, replacement, retry, fresh source continuation, P0 suffix, or H50 claim. Hindsight moves and future source results are audit-only and never teacher inputs.

Hard maxima: 10 teacher generations; 55 replay actions; 5 resets; at most 5 teacher actions; at most 65 reset-inclusive environment operations; output tokens at most 5 x (40 + 16) = 280; conservative input bound 10 x 8,192 = 81,920. The proposed 0.5 allocated device-hour cap is 1,800 monotonic seconds and includes any wait, model load, calls, audit, and cleanup. These are design maxima, not observed costs or a release. Existing A96 source generation is reused and adds zero generation calls to this probe.

Before any future run, a new exact candidate SHA, exact argv/environment, fresh output and supervisor identities, resource gate, Astra exact-SHA review, genuine zero-science preflight, and a separate launch clearance must bind together. Recheck all input hashes, source/event anchors, candidate code, output absence, disk space, and GPU memory immediately before the authorized run. If the GPU gate fails, do not load the model or wait while holding a GPU allocation. At the deadline or any integrity/operation uncertainty, preserve the actual receipt and stop; never retry or regenerate the scientific unit.

## Accounting and disposition

Historical scientific totals before this proposed probe: 7,101 generations and 10,004 reset-inclusive environment operations (previous 5,142/7,949 plus A96 1,959/2,055). If no intervening scientific activity occurs and all proposed maxima are charged, the ceiling would be 7,111 generations and 10,069 operations. These are conditional projections; authoritative raw-ledger recount is required immediately before and after any future execution. Engineering-only calls/device time are kept separate and are not hidden in scientific totals.

At a future one-step endpoint, record raw done/reward/truncated and the action receipt. Z_immediate is 1 only for an actually executed, integrity-bound action with terminal positive success; it is 0 for a completed action without immediate positive terminal success; it is NA with a reason when no trustworthy action outcome exists. A nonterminal endpoint has Y_T=NA_NOT_MEASURED. No full-horizon failure is inferred.

## Freeze boundary

No tracked source, candidate file, scientific input, old provenance, shared index, gate, or output was modified. No tests, project validators, tokenizer, CUDA runtime, model, environment, supervisor, preflight, or experiment were invoked. No commit or push occurred. This record does not claim runtime readiness or permission to start.
