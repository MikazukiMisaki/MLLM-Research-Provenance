# SI-E2 independent outcome

**Software review passed; real runtime readiness is blocked. No scientific launch is released.**

Exact candidate `dfc00e49d1ef4d48453d2331507429f8a0c7bbc5` adds 15 files, changes no old tracked blob, and independently reproduces 883 passed / 3 failed / 77 errors. The exact 80 historical failure/error IDs and types are unchanged; all 83 new tests pass. Twelve independent generation/token/state comparisons against the frozen generator also pass. This proves software contracts under the tested boundaries, not real 8B or ALFWorld readiness.

The only released full engineering probe returned authentic exit 1, naturally, with no retry or residual process. It stopped at the first CUDA UUID assertion before model weights, explicit one-byte tensor or environment replay. `torch.cuda.init()` did execute. A failed/open model-load unit is preserved. Zero generations, reset/steps, acquisition, training, evaluation or historical reruns occurred. The supervisor interval was 23.847 seconds / 0.006624 device-hours. The sampled 14–17 MiB device memory does not measure model memory fit.

A separate, freshly authorized pure identity diagnostic returned authentic exit 1 after 2.571 seconds, within its 60-second ceiling, with no residual process. It preserved the raw UUID before a single one-byte tensor allocation. It loaded no model or world. The installed `torch._C._CUuuid` string is the full canonical UUID without `GPU-`; NVML includes `GPU-`. The complete UUID bytes agree. Direct comparison in the candidate is therefore incompatible with this observed pinned runtime. This new observation explains a reproducible mechanism; it does not invent the missing raw value from the earlier failed probe.

The tiny allocation also exposes an independent execution-context blocker: local PID 837631 versus NVML compute PID 3082604, with no authenticated mapping. The latter cannot be whitelisted by temporal correlation, GPU identity, process count or memory size. GPU ownership remains unproven. The one-byte tensor used 512 allocator bytes / 2 MiB reserved; these are not inference/training measurements.

All 28 independently rehashed model/P0/old G3 files match. Science cumulative cost remains 5,142 generations / 7,949 reset-inclusive operations. Engineering allocation has separate nonzero time accounting: original supervisor plus identity launcher intervals total at most 0.007339 device-hours under their conservative clocks.

Root assigned Sol Research a strict UUID wire compatibility and pre-assertion evidence fix in a new isolated branch, with production software tests only. Existing PID/UID/unknown-process stops must not weaken. The immutable task is `SOL_UUID_COMPATIBILITY_TASK.md`. Any new exact SHA requires a new independent review. Real 8B testing additionally requires a separately proven execution context and fresh engineering release; the two consumed releases cannot be reused. New96 acquisition/student training/evaluation remain unimplemented and unauthorized.

Raw run/identity receipts and namespace metadata are intentionally included in the private provenance audit because they substantiate the blocker. No weights, adapter payloads, dataset copies, software token fixture trees or credentials are published.
