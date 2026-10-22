# R19 command and environment draft

> **NOT_APPROVED / NOT_EXECUTABLE.** The commands below are planning templates containing unresolved placeholders. They have not been run. Phase0 does not authorize preflight or live execution. Do not paste them into a shell.

## Future model-free preflight template

Use only after a separate written Sol Phase1 release, the exact replacement implementation is reviewed PASS, the adjudication is accepted, and a new ignored gate is validly prepared. Bind fresh unique record and absent output paths in the new reviewed gate. This is a plan, not a launch command.

```text
/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python \
  /home/lizening/wt-r19-recovery-duration-v1/scripts/launch_r19_supervised.py \
  --record-dir <FRESH_PREFLIGHT_RECORD_DIR> \
  --evidence-class preflight_only \
  --supersedes-run-id 3d1ccea7e97f4727abf8e216ac6ec498 \
  -- \
  /home/lizening/miniconda3/envs/alfworld-self-improve/bin/python \
  /home/lizening/wt-r19-recovery-duration-v1/scripts/run_r19_recovery_duration.py pilot \
  --protocol /home/lizening/wt-r19-recovery-duration-v1/configs/experiments/r19_recovery_duration_v1.json \
  --manifest /home/lizening/wt-r19-recovery-duration-v1/configs/local/<NEW_REVIEW_BOUND_GATE>.json \
  --output /home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/<FRESH_ABSENT_PREFLIGHT_OUTPUT> \
  --adapter /home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/model-artifacts/sft-policy-bootstrap/full/final_adapter \
  --data-root /home/lizening/alfworld_data \
  --config /home/lizening/wt-r19-recovery-duration-v1/configs/local/r19_b1_g2_alfworld.yaml \
  --preflight-only \
  --preflight-receipt <FRESH_PREFLIGHT_RECORD_DIR>/pilot_preflight_receipt.json
```

Required observed result later: supervisor and runner both genuinely exit 0; receipt is `PREFLIGHT_ONLY_PASS`; exact source/gate/review/runtime/input bindings match; module origins resolve to the reviewed checkout; the scientific output path remains absent; model loads/generations, ALFWorld construction/reset/step, and scientific units all remain 0. A command being queued or submitted is not evidence of start/completion.

## Future single live successor template

This is even more conditional: use only after the authentic preflight, a new independent exact-context launch clearance, and fresh explicit user authorization. Generate new unique supervisor record and scientific output paths; never reuse `a0de...`, `3d1c...`, the consumed clearance, or any existing output. Supervisor `supersedes-run-id` must bind the failed live run `3d1ccea7e97f4727abf8e216ac6ec498`; create a new supervisor run identity. `evidence-class` is `live`. The child is the same reviewed production pilot with preflight-only flags removed.

```text
/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python \
  /home/lizening/wt-r19-recovery-duration-v1/scripts/launch_r19_supervised.py \
  --record-dir <FRESH_LIVE_SUPERVISOR_RECORD_DIR> \
  --evidence-class live \
  --supersedes-run-id 3d1ccea7e97f4727abf8e216ac6ec498 \
  -- \
  /home/lizening/miniconda3/envs/alfworld-self-improve/bin/python \
  /home/lizening/wt-r19-recovery-duration-v1/scripts/run_r19_recovery_duration.py pilot \
  --protocol /home/lizening/wt-r19-recovery-duration-v1/configs/experiments/r19_recovery_duration_v1.json \
  --manifest /home/lizening/wt-r19-recovery-duration-v1/configs/local/<NEW_REVIEW_BOUND_GATE>.json \
  --output /home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/<FRESH_ABSENT_LIVE_OUTPUT> \
  --adapter /home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/model-artifacts/sft-policy-bootstrap/full/final_adapter \
  --data-root /home/lizening/alfworld_data \
  --config /home/lizening/wt-r19-recovery-duration-v1/configs/local/r19_b1_g2_alfworld.yaml
```

No run ID is manually invented; the durable supervisor creates it. Keep all original bounds: 127 TRAIN identities and index 0 first; at most 120 initial attempts and 60 eligible states; 30/15/15 with no quota transfer; K=1..5; total horizon 50; one successor maximum; no automatic retry. Stop on mismatch, nonzero exit, incomplete/unknown external operation, or any budget cap.

## Environment allowlist to bind in a later reviewed context

The historic `live_supervisor/launch_context.json` in the 2026-10-22 19:02 record lists the following allowed keys. Its `PYTHONHOME`, `PYTHONPATH`, and `VIRTUAL_ENV` presence flags were false. The future command must explicitly ensure those three are absent and record the actual effective allowlist in its own immutable launch context; do not rely on an interactive shell to hide them.

| Key | Phase0 observation / later policy |
|---|---|
| `PYTHONPATH`, `PYTHONHOME`, `VIRTUAL_ENV` | absent; explicitly unset before the supervised launch |
| `CONDA_PREFIX` | `/home/lizening/miniconda3` in historical launch context; pin/verify against the approved runtime |
| `PATH` | captured by the historical context; preserve only the supervisor-reviewed value and record/hash it in the new context; do not append interactive-shell paths |
| `ALFWORLD_DATA` | `/home/lizening/alfworld_data` |
| `ALFWORLD_CONFIG_PATH` | `/home/lizening/wt-r19-recovery-duration-v1/configs/local/r19_b1_g2_alfworld.yaml` (current file SHA `e90f93eb4604a473b6eb4a259a19ef1ca3c296bba1771ba70a1c9b0edbc99700`) |
| `HF_HOME` | not present in the captured effective-environment map; keep absent unless a reviewed context explicitly binds it |
| `HF_HUB_CACHE` | `/home/lizening/.cache/huggingface/hub` |
| `HF_HUB_OFFLINE`, `TRANSFORMERS_OFFLINE` | both `1` |
| `CUDA_VISIBLE_DEVICES`, `CUDA_HOME` | not present in the captured effective-environment map; do not add/change without reviewed runtime binding |

No credentials, access tokens, or unrelated environment variables are allowed in the published record. Capture actual argv, cwd, interpreter, allowlist, and omitted-key presence in the supervisor receipt; this draft does not stand in for that evidence.
