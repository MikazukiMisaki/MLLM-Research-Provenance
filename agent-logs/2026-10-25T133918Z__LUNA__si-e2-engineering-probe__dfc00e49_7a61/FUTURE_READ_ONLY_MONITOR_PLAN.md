# Future SI-E2 engineering-probe monitor plan (not executed)

This is a read-only monitoring plan for a separately authorized future probe. It does not start a supervisor, CUDA context, model, or environment. Current engineering release remains `NOT_GRANTED`.

## Before any worker allocation

1. Root rechecks the exact reviewed source SHA and clean state, proposal raw hash, authorization raw bytes/hash, exact GPU UUID, output and record-path absence, all proposal input hashes, and the current point-in-time process snapshot.
2. A separately authorized worker creates/checks its one-byte CUDA context, verifies actual CUDA UUID, and binds its own visible NVML PID to `/proc` PID/start-tick/UID/cgroup evidence before any 8B weights are loaded. If ownership is unknown, PID mapping is inconsistent, or a foreign compute PID exists, stop before allocation. The known graphics PID 5364 may remain a declared shared baseline only; do not kill it and do not claim exclusivity.
3. Record supervisor and worker PID, start ticks, UID, process group/session, argv, cwd, exact environment-set names, monotonic start, and output identity. Do not record token credentials or unrelated environment.

## During a released probe (monitoring only)

- Poll the bound GPU by UUID at one-second intervals using read-only NVML/nvidia-smi fields: memory used/free, utilization, temperature, power, and compute-process UUID/PID/name/used memory. Record each raw line with monotonic and UTC timestamp. The maximum sampled memory is a sampled peak, not a guaranteed hardware high-water peak.
- On each poll, verify that all visible compute PIDs belong to the authorized worker/supervisor identity set and that UUID remains the bound A40. A newly visible foreign compute PID, device mismatch, owner ambiguity, output drift, or cap breach triggers stop of **our own** supervised process only; never signal/kill another process or the shared graphics baseline.
- Track supervisor/worker process liveness by PID plus start-tick/UID (not PID alone), descendants, process group/session, authentic exit status, and child/parent relation. Keep raw supervisor receipts, worker report, and incomplete reservations as emitted. Do not fabricate a completed result or retry.
- Track monotonic wall duration from launch through cleanup; allocated-device hours are `allocated_device_count × monotonic allocated seconds / 3600`. Keep wall time and device-hours separate.
- Track ledger reservations/completions for each of the four generations, per-call and cumulative input/output tokens, environment constructions/closes, resets, and physical steps. Maxima remain 4 generations, 88 output tokens, 8,192 input tokens/call, 32,768 total input tokens, 2 resets and 100 steps; proposed replay is only 2 fresh instances / 2 resets / 12 steps.

## After a released probe

Capture a final GPU/process snapshot, process/child exit proof, raw supervisor/worker evidence, input pre/post hashes, output-tree inventory, and separately counted engineering costs. Any unknown child, missing receipt, open reservation, PID mismatch, or uncertain environment action is a stop/incomplete result. No automatic retry, resume, scientific validator, G2/G3/G4, training, or acquisition is implied by this monitor plan.
