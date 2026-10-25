# SI-E2 Luna read-only resource/readiness record

**Status:** `PREPARATION_ONLY / NOT_READY_FOR_PROBE_RELEASE`  
**Writable scope:** this Luna-owned task directory only. No shared INDEX, provenance commit/push, model/environment execution, supervisor/preflight, training, or scientific experiment was performed.

## Captured UTC window and source identities

- Evidence capture began at `2026-10-25T12:44:41.977024Z` (first host-inspection subprocess); final report/hash verification completed at `2026-10-25T13:04:13Z`. Each subprocess has its own actual argv, start/end UTC, monotonic duration, return code, and stdout/stderr byte hashes in its receipt. The module-origin probe returned 0 and used the pinned interpreter with `-I` and `find_spec`; it did not import torch/transformers/peft/ALFWorld/TextWorld or construct a model/environment.
- Historical import checkout: `/home/lizening/Alfworld-Self-Improvement-Project`, HEAD `4f5c2e18e0dfdf48e9471fcba0a3ee715be3ca3b`, branch `codex/progress-aware-recovery`.
- Engineering base observed read-only: `/home/lizening/wt-si-p3-engineering-contracts`, HEAD `a995d4c3c5f7d31a2cf1fd0afc4bfa4bd72ee3a3`, branch `codex/si-p3-engineering-contracts`, clean. Sol's runtime-adaptation candidate CLI and exact code SHA were not frozen at this handoff; no future invocation command has been invented.
- Starting assignment: `LUNA_TASK.md` SHA256 `b69dea3250a60b4480cdf45b1d7a9b9ccfedfd8c8dfd44ee03cf76e5ac221b41`; `ENGINEERING_SCOPE.md` SHA256 `7d4f554095e96f55bf97a286dbcbdc3851f9a34b8036c5ac72d048b15564f85d`; read-isolation ruling SHA256 `2eeadc19a1faaf49c71a6dfbd00f4e27665df5554f6a272770bb4aed9b9b61b1`.

## Work completed

1. Captured current visible GPU, process table, CPU/RAM, disk, scheduler-binary presence, Git/worktree state, package versions/origins, and path absence using read-only subprocesses. Exact receipts and raw outputs are listed in `COMMAND_RECEIPT_INDEX.json` and `FILE_HASHES.sha256`.
2. Hashed cached base snapshot files and P0 final-adapter files individually; read safetensors headers only for static parameter-count/payload arithmetic. No weights/cache were copied or published.
3. Bound all original G3 output/supervisor hashes to the independent final G3 evidence. The cumulative science cost remains 5,142 generations / 7,949 reset-inclusive environment operations; earlier 177/342 is already included. This task's actual science increment is zero.
4. Selected only the first existing source-trajectory JSONL record at schedule index 0. It has six saved actions and historical terminal status. The compact V3 candidate stores identity, line/file hashes, event refs, and action-map digests/counts, not command text. Proposed replay uses two fresh one-game instances, one reset each with seed 30000, and six saved steps per instance; pool_seed remains pending frozen Sol CLI. No environment was constructed, reset, or stepped.
5. Added `input_bindings.json`, including original config, selected game/traj_data, domain and grammar hashes; interpreter-resolved module origins; historical G3 input/output identity; source replay candidate; and non-executable future bindings.
6. Added `PROBE_PROPOSAL_PREPARATION_ONLY.json`. Exact argv/environment, candidate code SHA, independent review, pool_seed, and release remain null/pending. It is not a gate or launcher. Candidate paths were absent at the captured check and require fresh recheck if separately released.
7. Added `GPU_PROCESS_VISIBILITY_CLARIFICATION.md`: PID 5364 ownership/mapping is unresolved, not proven to be in another native/root namespace. The empty compute-process query is point-in-time evidence only, not GPU exclusivity. A future authorized worker must prove its own CUDA-context/NVML PID mapping before 8B allocation and stop if unresolved.
8. ALFWorld isolation blocker retained: the installed constructor scans task bodies under `dataset.data_path` before old helper filtering. A later reviewed factory must restrict discovery to the single authenticated historical task path before constructor entry; original config bytes must remain unchanged. No constructor was called.

## Resource and readiness result

The visible A40 snapshot had 45,390 MiB free, while static base+adapter parameter payload is approximately 16.73 GB. This makes a small inference probe plausible as a *conditional candidate only*; it does not establish peak memory, latency, device-hour, runtime compatibility, or training fit. The graphics PID 5364 is not visible via this process view and remains unresolved. `/home` had only 5,220,106,240 bytes available (95% used); avoid copying large cache/weights. Scheduler reservation evidence is unavailable. Accordingly the task is `NOT_READY_FOR_PROBE_RELEASE`.

If a later independent release issues the scope's ceilings, the proposal remains limited to one GPU UUID, at most 1,800 seconds / 0.5 allocated GPU-hour; four model calls with per-phase caps 16/40/16/16, no more than 88 output tokens total, 8,192 input tokens per call / 32,768 total; fixed synthetic public prompt/state; no model-produced command execution in ALFWorld; and two fresh replay instances with two resets / twelve steps. GPU hours must use allocated-device count × monotonic allocated seconds / 3,600, not wall time. No such release exists now.

## Actual call/cost accounting

| Activity | Actual in this task |
|---|---:|
| Model loads / CUDA model allocations | 0 |
| Generations | 0 |
| Training / optimizer steps | 0 |
| ALFWorld constructions | 0 |
| Environment resets / steps | 0 / 0 |
| G2/G3/G4/preflight/supervisor/policy replay | 0 |
| Historical cumulative science (unchanged) | 5,142 generations / 7,949 operations incl. resets |

## Frozen handoff files

- `READ_ONLY_READINESS.md`
- `input_bindings.json`
- `PROBE_PROPOSAL_PREPARATION_ONLY.json`
- `COMMAND_RECEIPT_INDEX.json`
- `MODULE_ORIGINS.json` and `module_origins_receipt.json` (new metadata-only capture)
- `GPU_PROCESS_VISIBILITY_CLARIFICATION.md`
- Existing raw/receipt evidence, including original candidate V1/V2/V3 attempts; none overwritten.
- `LOCAL_ONLY_FILES.md` and `FILE_HASHES.sha256`

No files were staged, committed, pushed, or added to a shared index. Wait for Sol's frozen candidate, exact-SHA independent review, a concrete immutable proposal, and a separate root release before any probe action.
