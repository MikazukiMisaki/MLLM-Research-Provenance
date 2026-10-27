# Read-only command receipts (SI-M1 preparation)

All entries below are from local subprocess/tool results during preparation. No receipt represents a model/runtime call.

## Source and design state

- Worktree query: `git status --short; git rev-parse HEAD; git branch --show-current` in `/home/lizening/wt-si-five-case-probe`. Observed exit 0; stdout: `?? configs/experiments/si_m1_single_step_v1.json`, `?? src/self_improvement/si_m1/`, `f1e0d56a1be2a65876bbec5b8950fb76cda3eace`, `codex/si-five-case-probe`.
- Resource contract query: `sha256sum configs/experiments/si_s01_shared_resource_v1.json` in `/home/lizening/wt-si-s01-shared-gpu-adapter`. Observed SHA256 `d908573f0c6d9518aec0a9b6b0a48c24648a26c3c708652b185a7cfe7b7e2489`.
- Design decision and Root cross-review were read from their existing files. Astra decision is `GO_DESIGN_ONLY_NOT_EXECUTABLE`; Root cross-review says `future_execution_ready=false`, `engineering_budget_frozen=false`. Their immutable paths and hashes are in CURRENT_BINDINGS.json.

## Static input hashing

- `sha256sum /home/lizening/.cache/huggingface/hub/models--Qwen--Qwen3-8B/snapshots/b968826d9c46dd6066d109eabc6255188de91218/* /home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/model-artifacts/sft-policy-bootstrap/full/final_adapter/*`. Subprocess exit 0; 23 lines returned (12 base snapshot files and 11 adapter files). Exact observed SHA256/path pairs are transcribed into MODEL_ADAPTER_SHA256SUMS. No model/adapter was loaded.
- `sha256sum -c MODEL_ADAPTER_SHA256SUMS` completed with exit 0; all 23 entries returned OK.
- `sha256sum` over the ten fixed case game.tw-pddl/traj_data.json files. Subprocess exit 0; exact observed SHA256/path pairs are in CASE_ASSET_SHA256SUMS. No task body was printed or parsed in this command.
- `sha256sum -c CASE_ASSET_SHA256SUMS` completed with exit 0; all ten entries returned OK.
- `sha256sum` over the original source_events.jsonl and source_trajectories.jsonl. Subprocess exit 0; observed 04ce4c0f32f40a3dbff6f42fec3c54107534ec45dd005795bd52014442513105 and 5e74691cee1cddae2c58191a524970fb0bd8a6f5517f40b4daa17c77d5fa3848, respectively. Their sizes and paths are in CURRENT_BINDINGS.json.
- Rehashing does not constitute environment replay or event-semantic validation. The prior independent Sol/Astra evidence is the source for the selected event-chain checks.

## GPU/process and storage snapshot

- Final `nvidia-smi --query-gpu=uuid,name,memory.total,memory.used,memory.free,utilization.gpu,temperature.gpu --format=csv,noheader` at 2026-10-27T03:32:50Z returned `GPU-b08bc603-ebdb-787d-b5b6-ec796ea3022a, NVIDIA A40, 46068 MiB, 40805 MiB, 4599 MiB, 100 %, 77`.
- Final `nvidia-smi --query-compute-apps=pid,used_memory,name --format=csv,noheader` returned six PIDs: 4001127 (6792 MiB), 4001123 (6784 MiB), 4001122 (6796 MiB), 4001126 (6796 MiB), 4001124 (6792 MiB), 4001125 (6794 MiB), all names `[Not Found]`.
- `ps -p 4001127,4001123,4001122,4001126,4001124,4001125 -o pid,user,comm,etime,args` returned only its header. This does not establish ownership; no process was signalled.
- Final `df -PT /home /tmp` returned `/home` ext4 with 401220 1K blocks available, capacity 100%, and `/tmp` overlay with 177974916 1K blocks available.
- `stat -c '%n mode=%a owner=%u:%g type=%F' /tmp` returned `/tmp mode=1777 owner=0:0 type=directory`; `test -w /tmp` and `test -w /home/lizening/research-notes/agent-logs` both succeeded. `findmnt -T /tmp` returned target `/`, source overlay, read-write. `id -u` returned 2000; `umask` returned 0022.
- The earlier candidate output path `/home/lizening/wt-si-s01-shared-gpu-adapter/artifacts/runtime/si_s01_minrec5_single_step_20261027T032024Z_once1` was absent when checked. It is not selected as a final path and no output directory was created.
- Final source-tree check at 2026-10-27T03:32:50Z still showed only the two untracked candidate paths above at base HEAD f1e0d56a1be2a65876bbec5b8950fb76cda3eace. The candidate output path remained absent.

## Negative invocation receipt

No command in this record invoked a model, tokenizer, CUDA API, ALFWorld, experiment runner, supervisor, preflight, project test, project validator, training, or replay. Counts for this preparation are all zero as recorded in CURRENT_BINDINGS.json. There is no raw experiment stdout/stderr, no child PID, no scientific exit code, and no experimental result because no experiment was attempted.
