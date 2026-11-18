# Independent read-only review: restarted weighted arm A interruption

Run `fb192e9157014ce9b5e153c412feb857`, source `8900f5c7750a25d6b2ca6ffbe63b2130ff0b69a8`. Read-only inspection of actual logs, source bindings, two supervisor receipts, process identities and resource samples. No real model, GPU, ALFWorld or runner was invoked by this review; no raw files modified and no retry.

## Result and failure

Outer `SI_WEIGHTED_OUTER_EXIT_V1`: `status=FAILED_OR_UNKNOWN`, `outer_signal=15`, real direct child return code 1, `direct_child_reaped=true`, `monitor_error=RuntimeError`, `cleanup=UNKNOWN`, `unknown_effects=UNKNOWN`, retry=false. Inner `SI_CONTINUATION_SUPERVISOR_EXIT_V1`: `status=INCONCLUSIVE`, `supervisor_error={type: InterruptedError, message: termination signal 15}`, worker `authentic_returncode=-15`, deadline not triggered, retry_authorized=false. These show signals and exits; they do not identify the sender or establish why signals occurred, or prove outer signal caused inner signal. The inner has no training_result and no checkpoint. No training effect or performance conclusion can be inferred.

Training event ledger has 795 events. Model-load started and completed once; 175 microbatch started vs 174 completed; 14 optimizer steps started and completed. The final, unclosed microbatch is step 14, position 6, recorded 445 input / 5 supervised tokens; its physical outcome is UNKNOWN. Summing recorded reservations gives started 97,417 input / 875 supervised tokens and completed 96,972 / 870. These are recorded token counts, not inference generations or independent measurements of GPU work.

## Identity, time and cleanup

The outer records 152.24259970337152 seconds and rounds allocation upward to 153. Inner reports 146.51585297379643 seconds, within its cap. Outer monotonic start/end: 6812881.998847011 / 6813034.241549201; inner start and reported end: 6812883.796829702 / 6813030.312682676. Last of 206 resource observations occurred at 6813029.521584295 before both receipt endpoints. Outer device samples are device-wide, not exclusive process attribution. Allocation intervals are not independently measured per-process GPU utilization and must be added to earlier costs without treating the first failed A's unknown tail as zero.

Inner records `cleanup_established=true`, `members_after_cleanup=[]`, `subreaper_restored=true` in its visible process namespace. It references a matching launch-context SHA, runtime-import SHA and resource SHA, and its binding equals the launch-context binding; worker-start context SHA also matches. The outer samples SHA matches the raw samples. Context binds the authorized plan `c06276072c35ba697f1c7acb62e1b4a6f6f49888211335c2ef4ad543fb01cb8d` and exact source. Input validation started and completed in the event ledger; this review did not redo all byte-level input checks or assert full dataset provenance.

Inner supervisor PID 1718696/start tick 681288207; worker PID 1718765/start tick 681288380. Both PID numbers were absent from current `/proc` during this later read. This supports the inner's local cleanup observation but does not prove absence of escaped/invisible descendants or host-wide/GPU cleanup; outer correctly remains UNKNOWN. No process was signaled by this review.

## Raw artifact SHA256

- outer_exit.json `a5345ffa1fc83162420c560b5afe1087aacd6089ec3f85ca15e0388c49a260bc`
- samples.jsonl `ec823dd61227da3961e5f6743179b7aed72881f36c5e16ccf123cbb3a21da42e`
- supervisor/supervisor_exit.json `acf3cb3378d65f2859119963c8cd69b3f5b02e2969c24d2380f57ad631e083ce`
- supervisor/training/training_events.jsonl `9e1e7b9b50ae7b85e96a0e30b79ebf24712d93ece7c31ef39653817e092a4038`
- supervisor/resource.jsonl `460d8706554f43d3dab3e75311baee37224375a9baa3d0a41b98947b4a3f8b28`
- supervisor/worker_start.json `d30752f547043eed3a2f3c7741aab69c1c47fcc21aba4b0c662f9b77be535830`
- supervisor/launch_context.json `d7a69c28e88ffbcac3580182367f4d60c0c5174fa9e1d7cd2df13d97400f9613`
- supervisor/runtime_import_receipt.json `40aa708fc524e1992a6152ae1ce95b5d61bd48d61495ff1c69902615c75723de`
- supervisor/worker.stderr `9c8e76302f8abd969316b5ee41cf476d01602e9ece1576dff2ecb6bf081fb120`
