# Luna task record — R19 live successor proposal

- Task scope: read-only preparation of one concrete successor proposal only.
- Outcome: `PREPARATION_ONLY`; no readiness or launch claim.
- Source checkout: `/home/lizening/wt-r19-recovery-duration-v1`, exact SHA `2da980f631badc25086d12db60d128ff507d3ae6`, clean detached at inspection. Current local gate SHA matched review-bound `c285692615eaaf1c7cb7139b0417528022db6ee03c510de13f881d126f14415e`.
- Sol's actual preflight verification is PASS for authentic run `a9ca70cb082b4f2387d242664031b0bc`, receipt `PREFLIGHT_ONLY_PASS`; immutable review SHA `ded8456fdf9d0e76e52a0d6979aa9f442c5f6feca587935028e9e629730812f7`. Five raw preflight hashes, original implementation review, adjudication, G2, predecessor evidence, authorizations and frozen input/runtime hashes are enumerated in `bindings.json`.
- Read-only process check found no matching R19/ALFWorld runner process. GPU query reported 0% utilization / 14 MiB. No supervisor, preflight, model, environment, G2, G3, or G4 process was started by this task.
- Proposed output and future supervisor record paths were both absent at check time. They were not created. The proposal directory itself contains only planning/evidence files; no launcher, gate, output directory, or executable record was created.
- Cumulative historical cost: 177 generations / 342 environment operations (330 non-reset plus 12 resets); old source unit remains incomplete/in_progress and is preserved under its accepted append-only disposition.
- Separate exact-proposal review, independent launch clearance and fresh explicit user scientific authorization are all pending. Maximum invocation counts for this task: supervisor 0, preflight 0, live 0, model/ALFWorld/scientific calls 0.

## Canonical hashes

Canonical JSON is UTF-8, compact separators `(',', ':')`, keys sorted, `ensure_ascii=false`; argv arrays use the same serialization without key ordering significance.

- `child_argv.json`: raw SHA256 `af84459ed7a90bb59f90b4965e959d4e80a24d6c3c563f443b4cb8f4433781fe`; canonical argv SHA256 `93aa3a833fbb65241fcab6b7e68d3863fa83985084d9c1b27875c730285f55ef`.
- `supervisor_argv.json`: raw SHA256 `c9f57d2735d95250b8a12d34c68f6ea7e8bd644e9a5c194bad55d42a81b4024b`; canonical argv SHA256 `c2270f4e43d88d53022b38bc4bc0e1890bc49b738387f99485045fd9020e450a`.
- `environment_plan.json`: raw SHA256 `24af21a3db2ae89abc56f81e5fb8e457ed3a801ca9fc21ef40a472b4c02703c9`; canonical whole-plan SHA256 `d0bd5721913a6316affcbd4918befe65f2f9400a9d6e14536b88df5627e62189`; canonical static `{set,unset}` SHA256 `4c1e7ef497ccdcc288e8e79c844705842ad15697c574108b9f146f3d64c148dc`.
- `bindings.json`: raw SHA256 `9f10793c0e73ac70c861c0ef8a8d2babbbe878f5aba167a5b4c61f26d2e05aa2`; canonical SHA256 `ccef7bbf8a303f8ebb221a1e0e40c26d56e5f6877ad44ce6ad41314d4ac14816`.

All file hashes are additionally recorded in `FILE_HASHES.sha256`. This directory is Luna-owned. Do not stage or modify other agents' records. Publication is to be coordinated additively on the current provenance main after Sol receives this proposal.
