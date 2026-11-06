# Shared A40 follow-up snapshot

A second read-only device query on 2026-11-06 around 14:06 UTC reported 46,068 MiB total, 36,100 MiB used, 100% utilization and 78°C; 9,968 MiB remained by subtraction. A compute process was present and was not touched. This is a separate point-in-time device-wide observation, not a reservation or a continuous utilization history. It supersedes no earlier snapshot.

The available memory remains below the roughly 15,259 MiB nominal BF16 storage for eight billion parameters, before other runtime costs. This comparison does not measure actual Qwen/adapter fit and does not evaluate CPU offload or quantization. No model, CUDA context, tokenizer or environment was initialized by the query. Shared device use was already authorized; waiting here addresses observed resource contention and unvalidated fit, not lack of permission.
