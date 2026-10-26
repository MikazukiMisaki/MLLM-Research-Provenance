# SI-S01 source-only input hash readiness — preparation only

- Status: `INPUT_HASHES_CAPTURED_SOURCE_SHA_PENDING_NOT_READY_FOR_LAUNCH`.
- Start/finish UTC: approximately `2026-10-26T10:59:45Z` (own directory creation minute; first command timestamp not separately captured) / `2026-10-26T11:02:58Z`.
- Adopted protocol: `ADOPTED_SOURCE_ONLY_PROTOCOL.md`, SHA256 `daa1d787f9ef13f5927dcf696a2be4c6328dc159b3eb39b5f0f5f520582ebb72`.
- A96 metadata reservation: SHA256 `6ce8a32a2345b59ecdef9c28c3a341e9c0801b8105f79895f9b2cb9545a4937e`.
- Source code SHA: `PENDING_FROZEN_EXACT_SHA`; independent software review and launch clearance have not been issued.

## Captured evidence

- `INPUT_HASH_READINESS.json` SHA256 `faeba6e7b31a4b33c0cdfd612f3a625584eb52ff4e00e41fc9e6c04caeb6979b`, 136,019 bytes. It binds the fixed 96 task identities, family counts 35/26/16/9/10, task-order digest, 192 source asset byte hashes, original YAML/data root, logic files, package source bytes, current candidate module bytes, and certified model/adapter file current stats.
- Independent rank-wire reproduction matched the requested ordered-task newline SHA256 `40893826093d24bb111803a3532a260c2061c6c9b1c28b8d95c87000b3daa6c2`; serialization is 96 UTF-8 task IDs in fixed family/rank order, each followed by newline. The input-hash bindings follow that order but are not a production schedule: no slot seeds, operations, argv, gate, or run identity were emitted.
- All 192 fixed-A96 `game.tw-pddl` / `traj_data.json` files existed and were streamed twice for SHA256/size only. Their contents were not parsed, printed, or copied. Hashes were stable between the two passes. No D48/E600 task body was read.
- Original runtime interpreter: `/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python`, current file hash and size recorded; direct `-I --version` returned `Python 3.10.20`, exit 0. Current package module source hashes matched the prior bound proposal. No project imports were made.
- Original YAML is `/home/lizening/wt-r19-recovery-duration-v1/configs/local/r19_b1_g2_alfworld.yaml`, SHA256 `e90f93eb4604a473b6eb4a259a19ef1ca3c296bba1771ba70a1c9b0edbc99700`; selected paths resolve to training data under `/home/lizening/alfworld_data/json_2.1.1/train` and logic files under `/home/lizening/alfworld_data/logic`. The recorded `ALFWORLD_DATA` root is `/home/lizening/alfworld_data`.
- Logic file hashes: `alfred.pddl` `f1473041ed01da514de1f87adfd7ef0804862361f83ccf63c75e43633b0eb280`; `alfred.twl2` `c5b22f0f73309a7fd7c8e5b71de42ad4803b60766ab4a51cc2feb34162be036b`.
- The certified P0/base snapshot manifest contains 12 files and final adapter manifest 11 files. Current stat found all present with sizes matching the certified manifest. No model/adapter file content was rehashed or loaded; certification is by the prior E1 input-binding artifact, whose path/hash is in the readiness JSON.
- Current source module bytes are recorded only as observations: candidate `si_p3/contract.py` and original `src/env/alfworld.py`; this does not freeze or validate a source revision. The readiness JSON explicitly leaves `source_SHA` pending.
- SSH-agent socket was checked by `lstat` only and remains missing at `/home/lizening/.codex/app-server-control/forwarded-ssh-agent.sock`. No SSH attempt was made.
- Actual outer-command stdout/return code and pinned interpreter `--version` subprocess receipt are preserved in `CAPTURE_COMMAND_RECEIPT.json` and `INPUT_HASH_READINESS.json`.

## Boundaries

No task body beyond the fixed A96 game/trajectory files was opened; no content was interpreted. No tokenizer/model/weights, CUDA/NVML, ALFWorld/TextWorld construction or action, validator/test, preflight/supervisor, scientific unit, or launch command was run. The one pinned interpreter command was `-I --version`. No output directory, run identity, schedule, gate, authorization, or runnable argv was created. No shared index/inventory, source tree, prior evidence, or provenance Git state was changed; no stage/commit/push occurred.

This is input-byte readiness evidence only—not a frozen implementation, software PASS, runtime-readiness PASS, preflight, or launch clearance. A future task must bind it to the reviewed exact source SHA and separately clear every required gate.
