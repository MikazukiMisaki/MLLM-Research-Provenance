# Independent read-only audit: weighted training arm A failure

Run `8582b3aa9cd649278cdf2cc493e99e55`, source `aa82a06076bcf87b18f7a87bf08b5eed3feeb256`. Scope: read-only source and original event, supervisor, process and resource evidence. No evidence changed, no model/world called, no rerun. No complete training result or adapter was found in the original run tree. Raw event classifications below describe durable records, not a guarantee of all physical computation.

`outer_exit.json` reports `actual_returncode=-15` (the outer supervisor's directly monitored child was terminated by SIGTERM), `direct_child_reaped=true`, `monitor_error=ValueError`, `cleanup=UNKNOWN`, `unknown_effects=UNKNOWN`, `retry=false`; inner `supervisor_exit.json` is absent. On the exact frozen driver control flow, its `wait_owned_supervisor` returns a nonzero child and `verify_inner_receipts` rejects that nonzero via `ValueError` before reading the absent inner receipt. Thus `ValueError` is compatible with—and under the displayed control flow follows from—the nonzero child status; it does not identify the signal sender, purpose, or origin. The evidence cannot determine why SIGTERM was delivered. No OOM or model exception is demonstrated by worker stderr; that is not proof that every possible technical issue is absent.

The raw ledger has 1,571 events: one model_load started/completed; 348 microbatch started and 347 completed; 28 optimizer steps started and completed; no checkpoint or completed training result. Last entry is microbatch started at optimizer step 28 position 11, with 404 input and 5 supervised tokens; its outcome is UNKNOWN. Summed recorded input/supervised token reservations over started microbatches are 194,105 / 1,740, with 193,701 / 1,735 on completed microbatches. These are recorded inputs/reservations, not inference generations or separately measured GPU work. The earlier 28 complete optimizer events do not make a complete 33-step product.

The outer observed allocation interval is 253.6970064966008 seconds (rounded upward in its receipt to 254). The resource ledger's last recorded monotonic time is 6811650.128676761, whereas outer ended monotonic is 6811640.315160314: 9.813516447 seconds later. From outer start 6811386.618088698 to that last observed resource entry is 263.510588063 seconds. Therefore 254 seconds alone cannot upper-bound the surviving worker tail; the 264-second ceiling of this *observed span* is a conservative count for that span only, not an upper bound on unobserved tail. GPU utilization/memory samples are device-wide and cannot establish per-process physical cost. Cleanup and final total allocation duration remain UNKNOWN pending stronger evidence.

`worker_start.json` binds worker PID 1716919, UID 2000, start tick 681138842, PGID/SID 1716919, separate from observed supervisor PID 1716852, start tick 681138668. A later read-only `/proc` check found both recorded PID numbers absent from the current namespace at the observation time; this does not establish when they exited, excludes neither unobserved descendants nor host/GPU activity, and does not retroactively establish clean shutdown. No process was signaled or changed by this review.

Frozen code: `launcher.py` SHA256 `74fc4866472fb960a83926768bb300ed6830fd2fc055dd5accc19a0a8964bbcd` lines 129–146; `bridge.py` SHA256 `87fb1ac2a8cea6b1afa879ccc6fb0f87d7bccb081796e1535100545eddacb99f` lines 52–84; inner `supervisor.py` SHA256 `a644cf4b21a49f520971116ea7e35d6628d42472c6910a431de7cb5847ab1cba` lines 61–83 and 104–120. The final parent status is failed/unknown, not an authorization to retry or use partial weights.

Read-only original input hashes:
- outer_exit.json `486f49064d3ed765b5cdcc28e11c1f645681bc25faf19215a9ca6dc32dbde1f7`
- samples.jsonl `8db42e03c1b6c4ebddec199631362687f906c927f7a577c8713ee4585e62f986`
- supervisor/training/training_events.jsonl `aca30e7b04645290f4a271995cbc844bce3adab9be5de6ddfb4943d9ed5f440a`
- supervisor/resource.jsonl `6b462dc67c57987860e1d7dd16a06afbe0ca7a2be3f81dbc085709a4684b46eb`
- supervisor/worker_start.json `9f79c69a9d6622b67399f234dd1a3c36c6c651b23a5bbe424750a4ff73eed7b1`
- supervisor/launch_context.json `e3bede658e1f339f54756fdf2f80289c1b04df3dcc8c3226d3c6e8c76b62a216`
- supervisor/worker.stderr `c21a49d2edd833546f62b5685edd1b3e20bdf4b1556c058bc4e4b19507cf61ad`
