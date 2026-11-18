# Read-only review of interrupted A engineering restart

This review did not signal processes, modify evidence, run a model, use a GPU, construct an environment or retry. Run fb192e9157014ce9b5e153c412feb857 is a separately recorded new A initialized from C-quarter, not a successful continuation of the earlier failed run. B and evaluation were not run.

## Observed execution and cost

The outer start was 2026-11-18 00:47:08.788865 UTC and end was 00:49:41.031501 UTC. Its 152.24259970337152s allocation interval rounds up to 153 seconds under the declared allocated-wall convention. Outer status FAILED_OR_UNKNOWN, outer_signal 15, return code 1, direct child reaped, cleanup UNKNOWN, unknown_effects UNKNOWN and no event-ledger hash in the outer receipt. The old inner supervisor receipt reports 146.51585297379643s, status INCONCLUSIVE, supervisor error InterruptedError 'termination signal 15', worker return -15, cleanup_established true, no remaining members in its observed process view, and no training-result hash. This inner receipt reports cleanup within its visibility; it does not turn the outer UNKNOWN into verified host-wide/GPU cleanup. Recorded inner PID 1718696 and worker PID 1718765 were absent from the current procfs during this review; absence is limited to that visibility.

Raw training ledger: 175 microbatch starts, 174 returns, 14 optimizer-step starts and 14 returns. The last microbatch was started, not returned; there is no final training result or adapter checkpoint in the original tree. The starts reserve 97417 input/sequence tokens and 875 supervised tokens; completed events record 96972 input and 870 supervised tokens. These are logged reservations/returns, not an independent measurement of all physical computation. There were 206 paired resource checks, all recorded PASS; maximum recorded allocated peak 19477299200 bytes and reserved peak 22605201408 bytes refer to the CUDA allocator, not total device use. The last completed outer sample showed GPU device-wide free 23494 MiB and disk free 24931262464 bytes. The records do not show a GPU or disk guard failure as the cause of interruption; the signal sender and motivation are not established by the new run's receipts.

## Relationship to earlier failure

Earlier run 8582b3aa9cd649278cdf2cc493e99e55 had 348 microbatch starts/347 returns and 28 optimizer starts/28 returns. It had supervisor return -15, no inner supervisor exit receipt and an unknown tail; worker resource activity was observed at least 9.8135s after the outer receipt ended. A separate operator stop record reports sending SIGTERM to the earlier inner and worker groups; that report is an attributed account for the earlier run, not independent evidence of who signaled the new restart. The new outer additionally records signal 15 and the new inner separately reports termination signal 15; neither records sender credentials. Do not infer a common sender or intent.

Both attempts bound the same plan, source training ledger, newly encoded rows and C-quarter initial adapter. Frozen source diff aa82a060→8900f5c changes only the weighted launcher, adds signal-supervisor module and its tests; six worker/training/resource source hashes in both launch contexts match. Both started actual training and stopped before a checkpoint with an outstanding microbatch and a recorded SIGTERM somewhere in the hierarchy. This is a common observable interruption pattern, not evidence that the loss or model caused SIGTERM and not evidence of model efficacy. No gate, result or receipt was rewritten to success.

Across the two incomplete A attempts, logged microbatch starts sum to 523, returns 521; optimizer starts/returns each sum to 42. Both have one started/unreturned microbatch. The exact physical costs of unreturned operations remain UNKNOWN. The earlier source has separately documented 2318s rounded allocation (other R19/SI histories excluded). Adding first A's >=264s observation through its last worker resource event and restart A's 153s rounded outer interval gives **at least 2735 allocated seconds** under this convention. The previously proposed extra 60s and 1800s reserves are budget allowances, not observed expenditures or upper bounds; earlier tail beyond last activity, earlier unknown allocations, and host-wide cleanup remain UNKNOWN. The 16200s was a proposed budget ceiling, not proof of actual allocation or independent approval. Do not resume either failed A, start B, or infer a result from them.

## Evidence hashes at review time

- Restart outer_exit.json: a5345ffa1fc83162420c560b5afe1087aacd6089ec3f85ca15e0388c49a260bc
- Restart samples.jsonl: ec823dd61227da3961e5f6743179b7aed72881f36c5e16ccf123cbb3a21da42e
- Restart inner supervisor_exit.json: acf3cb3378d65f2859119963c8cd69b3f5b02e2969c24d2380f57ad631e083ce
- Restart training_events.jsonl: 9e1e7b9b50ae7b85e96a0e30b79ebf24712d93ece7c31ef39653817e092a4038
- Restart resource.jsonl: 460d8706554f43d3dab3e75311baee37224375a9baa3d0a41b98947b4a3f8b28
- Restart worker_start.json: d30752f547043eed3a2f3c7741aab69c1c47fcc21aba4b0c662f9b77be535830
- Restart worker.stderr: 9c8e76302f8abd969316b5ee41cf476d01602e9ece1576dff2ecb6bf081fb120
- Earlier independent failure review: 929d371e33750504aa7b8ce808ad6f0f87181244f46bd834ad4fbde8b4bce504
