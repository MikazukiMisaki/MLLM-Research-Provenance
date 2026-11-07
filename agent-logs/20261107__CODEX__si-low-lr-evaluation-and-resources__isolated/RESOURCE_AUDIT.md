# Prior B/C training resource evidence: scoped read-only audit

Scope: the two unique B_run and C_run children of the authorized prior training run parent. Only each training_result.json, supervisor_exit.json and resource.jsonl were parsed for this record; worker_start.json was hashed/read to establish recorded start, without reproducing its argv. No samples, task identifiers or held-out tasks were read. This is historical evidence, not a new training run, a complete project cost ledger, or a guarantee for a future run.

| Recorded quantity | B | C |
|---|---:|---:|
| Worker start receipt present | yes | yes |
| Training result status / real supervisor child exit | COMPLETED / 0 | COMPLETED / 0 |
| Recorded training elapsed seconds | 824.4404626526 | 857.7407546137 |
| Supervisor elapsed seconds | 883.2235775916 | 916.8313971711 |
| Supervisor allocated device hours (elapsed / 3600) | 0.2453398827 | 0.2546753881 |
| Microbatches started / completed | 1248 / 1248 | 1248 / 1248 |
| Optimizer steps | 78 | 78 |
| Input / supervised tokens | 661620 / 6240 | 695872 / 6240 |
| Reported peak process allocator allocated bytes | 20294383104 | 20222059008 |
| Reported peak process allocator reserved bytes | 24643633152 | 25352470528 |
| Minimum sampled device-wide free bytes | 22596091904 | 21887254528 |
| Sampled device total bytes | 47608692736 | 47608692736 |
| Allocator retries / OOM reported max | 0 / 0 | 0 / 0 |
| Resource records / statuses | 1328 / all PASS | 1328 / all PASS |

Both historical runs used learning rate 0.0001, batch size 1 and gradient accumulation 16. These data only suggest an order of magnitude for a similar candidate, not reliable runtime or memory ceilings under a different learning rate, input distribution, shared-GPU contention or runtime. The elapsed-based device hours are supervisor wall time and not evidence of exclusive GPU ownership or process-compute hours. Allocator peaks refer to observed worker allocator statistics and do not include arbitrary other processes, driver overhead, or unobserved peaks. Free device memory is device-wide and cannot be attributed to the worker. Resource receipts expressly state exclusive_gpu=false and NVML process mapping UNPROVEN. Gaps, potential external/child costs and any aggregate project totals beyond these two runs remain UNKNOWN. Exit receipts report cleanup established and no deadline trigger; these are observations by the supervisor, not independent host-wide guarantees. Preflight, data acquisition, rehashing, setup, evaluation, inference, and future usage are not included.

Evidence SHA256s, full immutable source bytes (hashes verified directly):

| Arm | training_result.json | supervisor_exit.json | resource.jsonl | worker_start.json |
|---|---|---|---|---|
| B | e7d304b2a06195ea24555ec95be971b248bf5a9e86a9ee6955396e7f748f1150 | 3310a93cad131b1441136c2f6284b10d01361ea229f12c41d8e0b77ca7363ce0 | 1f982dbacef6995de77b8ec151ea8da112d7307112f954906ebebb7ebb171889 | b87d58d705262852b2a9b416e051bb74c2680c8ca38351ff4bec9f8ea7bf2b2b |
| C | 446b28796de612072ada2503d4af338ff911d8007d83fa7b4ed40539c63bf421 | e61c9ccc9727795617d6227fa51707b291304c8790f2a3430fce4c4e83ffc4bd | 47be8f68ef9072e736834fc90f49af3ee1dccd9b1ebbb83b1aa6cc1aacd68139 | 7f15522d75eb01adaaa2164c2951dd6b65cd48d402141e7a73754afb965d4e00 |

Both supervisor receipt resource hashes and training-result hashes match the independently read files. Full original receipts, paths, and original resource rows remain in the original local run tree; this aggregate does not publish machine-specific paths or task-level records. No model, environment, preflight, training or original-record modification was performed.
