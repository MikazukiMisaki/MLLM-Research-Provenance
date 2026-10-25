# SI-E2 read-only resource and replay readiness

**Disposition:** `PREPARATION_ONLY / NOT_READY_FOR_PROBE_RELEASE`  
**Science authorization:** `NOT_GRANTED`  
**Evidence boundary:** metadata, hashes, static safetensors headers, and existing completed G3 evidence only. No model load/generation, CUDA context, environment construction/reset/step, supervisor, preflight, training, or scientific invocation occurred in this task.

## Frozen source and historical accounting

- SI-E2 engineering base: `a995d4c3c5f7d31a2cf1fd0afc4bfa4bd72ee3a3`, branch `codex/si-p3-engineering-contracts`, clean at the captured inspection. Separate candidate runtime-adaptation worktree/output path was absent then. Sol's implementation SHA and independent exact-SHA review are not yet frozen; therefore no executable CLI or exact argv/env can be bound.
- Existing G3 evidence is run `260422ac02bd42a8b2929d7ef240526b`, executed from scientific SHA `2da980f631badc25086d12db60d128ff507d3ae6`, exit 0. Read-only hashes match the independently finalized G3 audit for all 10 output and 4 supervisor files. Historical cumulative science remains **5,142 generations / 7,949 environment operations (resets included)**. This SI-E2 preparation added **0 generations, 0 resets, 0 environment steps, 0 training runs**. Do not add the earlier 177/342 separately; they are already included.
- Original scientific checkout `/home/lizening/Alfworld-Self-Improvement-Project` was HEAD `4f5c2e18e0dfdf48e9471fcba0a3ee715be3ca3b`, branch `codex/progress-aware-recovery`; do not call it `a995` or the later candidate SHA.

## GPU, memory, and host capacity

At the captured point, the visible device was NVIDIA A40 UUID `GPU-b08bc603-ebdb-787d-b5b6-ec796ea3022a`, driver 550.163.01 / CUDA 12.4, 46,068 MiB total, 45,390 MiB free, compute mode Default, MIG N/A, utilization 0%. The compute-process query was empty. `nvidia-smi -q` also showed a 4 MiB graphics row with PID 5364, but its owner and mapping were not visible to this task's `ps`/`/proc` view. The process view has Docker cgroup metadata and a local `NSpid`; this does **not** prove PID 5364 is from another native/root namespace or execution context. Treat its ownership as unresolved. This is a known graphics baseline and a point-in-time absence of a visible foreign compute process, **not** an exclusivity claim. Do not kill or reclassify the graphics process.

Future GPU use is not ready. Although static parameter bytes are below the observed free-memory number, no CUDA context, real model load, allocator peak, generation latency, or device-hour has been measured. A future separately authorized worker must prove its own CUDA-context/NVML PID mapping against the bound GPU before 8B allocation; if that proof is missing or inconsistent, stop before allocation. No such worker/release exists now. One GPU-hour accounting must be allocated-device count × monotonic allocated seconds / 3,600, not wall time.

Host CPU/RAM snapshot: 64 logical CPUs (Xeon Silver 4314); RAM 134,853,836,800 bytes, available 130,623,057,920 bytes. `/home` was 95% full with 5,220,106,240 bytes available. Do not copy model weights/cache or create a large cache. Scheduler executables were not found, so no scheduler reservation/ownership evidence is available.

Static header-only facts (no tensor payload read or model load): base snapshot has 8,190,735,360 BF16 parameters / 16,381,470,720 calculated tensor payload bytes; P0 adapter has 87,293,952 F32 parameters / 349,175,808 calculated payload bytes. These are storage lower bounds, not runtime peak or training-fit measurements; do not cast the adapter or infer training feasibility.

## Runtime and input bindings

Pinned interpreter is Python 3.10.20 at `/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python`. Distribution versions and module-resolution origins are bound in `ENVIRONMENT_PACKAGES.json`, `MODULE_ORIGINS.json`, and their actual subprocess receipts. Key versions: torch 2.6.0+cu124, transformers 4.56.2, peft 0.17.1, ALFWorld 0.4.2, TextWorld 1.7.0, PyYAML 6.0.2. The module-origin probe used `importlib.util.find_spec` under the pinned interpreter and `-I`; it did not import these runtime packages. No runtime compatibility is thereby established.

The exact cached Qwen3-8B snapshot (`b968826d9c46dd6066d109eabc6255188de91218`) and actual P0 final adapter were hashed file-by-file (12 and 11 files). Their hashes/bytes and all original G3 output/supervisor bindings are in `input_bindings.json` and the captured runtime-hash receipt. No weights/cache were copied or published. Bound environment inputs include the original active R19 ALFWorld YAML, base A40 YAML, task `game.tw-pddl`, `traj_data.json`, Alfred domain, and grammar; see the same binding file and `REPLAY_INPUT_HASHES.json` for exact byte counts/SHA256s.

Important isolation blocker: installed ALFWorld `AlfredTWEnv.__init__` scans and opens task bodies under `dataset.data_path` before the old exact-task helper narrows `game_files`. Reusing the old helper against the global TRAIN root would violate the closed 96/48/600 pool boundary. Sol's new exact-task factory must restrict effective discovery to the authenticated historical task directory **before** construction, or use a no-scan subclass. Keep the original YAML bytes/hash unchanged and record the effective discovery-path restriction separately. No ALFWorld constructor was called here.

## One deterministic historical replay candidate

Selection is the first JSONL record in the authentic G3 `source_trajectories.jsonl` (schedule index 0); no outcome-based search or substitution. Task identity: `pick_and_place_simple-Pencil-None-GarbageCan-316/trial_T20190907_165839_449092`, split TRAIN, seed 30000, source line 35,486 bytes, SHA256 `465bff755ba34c18acca299470cd7c3a40455cb395df3e6fe43eee9919a7c73`, trajectory id `aea7c51203026ec5ec1fdb57`, six saved actions, within the 50-step source cap. Registry unit is completed; the existing record says `environment_terminal`; original before-action snapshot comparison PASS. Existing game, trajectory-data, config, domain, and grammar hashes are bound in `input_bindings.json`.

Conditional design only: two **fresh, separate** one-game instances, each reset once with seed 30000 and replay the same six saved actions; same frozen `pool_seed` in both once Sol's CLI freezes it. Maximum proposed use is 2 resets / 12 physical steps (well within the 2-reset / 100-step ceiling). Compare all ordered public fields, action maps, and transitions. Do not execute model-generated actions. Terminal-map behavior on a future replay remains `NOT_OBSERVED`; never synthesize an empty map. No instance has been constructed and no replay has happened.

## Conditional engineering probe placeholder — not executable

The only candidate ceilings are those in the reviewed scope: at most 1 probe, 1 bound A40 UUID, 1,800 seconds and 0.5 allocated GPU-hour; at most 4 actual generation calls (source 16, Stage 1 40, Stage 2 16, suffix 16), 88 output tokens total, 8,192 input tokens/call and 32,768 total; fixed synthetic public state/prompt only; no generated action executed in ALFWorld; at most 2 resets / 100 environment steps. Source continuation is reused; no extra comparison-model call, no optimizer step, training, adapter save, acquisition, evaluation, G2/G3/G4, or retry.

Exact child argv, environment, supervisor, code SHA, review SHA, authorization, `pool_seed`, output identity, and record identity remain pending. The candidate JSON is explicitly non-runnable and records those null/pending fields. Candidate output `/home/lizening/wt-si-p3-runtime-adaptation/artifacts/runtime/si_e2_luna_probe_a995d4c_20261025T124118Z` and record leaf `engineering_probe_supervisor` were absent at the captured check; never reuse a path without a fresh authorized check. No gate, launcher, UUID, or runnable command is created here.

## Readiness conclusion

The visible free-memory snapshot makes a one-GPU engineering probe **plausible only as a conditional candidate**, based on static lower bounds. It does not establish runtime fit. Unresolved graphics PID ownership, no CUDA-context proof, low `/home` space, unmeasured load/latency/peaks, the unresolved exact-task discovery fix, and absent frozen Sol CLI/review all block release. This report is not a probe PASS, model readiness, training readiness, exclusive reservation, or execution authorization. Wait for frozen implementation, independent exact-SHA review, a concrete immutable proposal, and a separate root release.
