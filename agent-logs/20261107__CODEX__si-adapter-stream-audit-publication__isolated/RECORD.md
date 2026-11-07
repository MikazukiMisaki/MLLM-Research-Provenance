# Independent audit of the adapter stream record

Status: `LEDGER_AND_TREE_SERIALIZATION_CONSISTENT`; C-low outer supervision remains `UNKNOWN`. This is a private, sanitized provenance record. It does not contain model bytes, task or training data, local paths, or storage identifiers.

The independent auditor examined retained code, manifest, progress ledger, result, direct supervisor receipt, coordinator observation and historical identity records. The audit did not read model products again or call a model, GPU or environment. All 19 consulted evidence files had equal before/after SHA256s; the private audit result preserves their complete inventory.

There are 1,033 progress entries: 1 pre-scan, 1,029 read completions and 3 tree matches. The 17 files' sequential chunks, size limits and cumulative counters agree with the retained result and cap. Logical bytes: P0 365,138,109; C-low 349,250,053; C-high 349,250,053; total 1,063,638,215. This is application-level logical input data, not measured physical disk traffic.

The tree digest for each arm was independently recomputed from retained ordered file name, size and digest rows; each matches the retained manifest and an earlier identity record:

- P0: `6b13612c33d96ae9bbda041c08d33e0e1888406c4782670e90c8ebd27467b5a5`.
- C-low: `1cc6c153138e58ca1bda44c0682757d68649c11190258854e7ee2454df816669`.
- C-high: `40202cade31425b823ae4b153f2c975487d64b48461b47b922aebda226dd4c57`.

The child supervisor recorded GO, direct child return 0, no stop reason, elapsed 5.836685906 seconds, and direct-child user/system CPU of 2.486318/0.68244 seconds. Owner stdout recorded receipt persistence. A coordinator note reports observed outer process exit 0, but a separate outer wait receipt is unavailable. The older C-low training supervisor is a different matter and remains UNKNOWN.

The per-file digests were produced by the one reader and were not independently reproduced from raw bytes. The legacy digest cannot be recalculated from the retained per-file digests. Streaming hashes do not establish an atomic snapshot, stability before/after the read, behavioral model compatibility, or scientific success. Physical I/O, kernel I/O tail, and descendant status remain UNKNOWN. Same-UID output-directory rename races and other check-to-use limitations remain possible, with no claim of actual occurrence.

Source SHA256s: independent private review `87010fc9f38e1011447e6b9b05ba00a71551d924486b48d33cf5fa8b4412f2a4`; independent audit script `dc4baf40979140b70220dd6dbfd3e750c3d54965d897148907fc5e4c15e504bf`; independent audit result `5e54e5e7202949aa6eab6f50dfaff963082ec588ddefab56fe87d9d060ae67aa`; original progress ledger `e39fcbda213b072329a0ce20dc78f49b0ef8e781139b80300011e47e367f9a61`; original result `db5712dc124d648244555a62169ac5d150fcae1012b0438e41c2c22e0345c803`; original supervisor receipt `c4fdb10aa0c37f407949e92125360e595a41d67a756dcbf4ac6f1f8f12974c4a`; verifier `1fc87aabec55504b45704b4ada99c3256b3d05eb2c2d86efbf930869a04aa4c2`; owner `380ae9f319b9a5aa02eaa02ac6bdda9454b4e23871186bcc4400f4342c1e6edc`; gate `d1fdc1fd6216b26179f154dbe7127c6d95fded4c97709e24b3ea5d7dd999a98f`; manifest `9148c5ba661f5ef3c3e85b92d8dde3c1042a3da9ebed1b96b7ffff8c19297fa0`.
