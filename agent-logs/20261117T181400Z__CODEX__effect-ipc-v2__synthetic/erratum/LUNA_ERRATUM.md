# Erratum: withdraw Luna's ACK short-write finding

This append-only correction withdraws the ACK short-write finding in these immutable prior notes:

- `2026-11-17_180103_UTC__LUNA__ipc_bridge_preliminary_review.md` (SHA256 `0a7547cef5da46c56eaceddb8c8437b359f8d40b3f6f5fabf0984e8d77530410`).
- `2026-11-17_180526_UTC__LUNA__bridge_review_followup.md` (SHA256 `1903c0a40298f0a943bd8c62477a9e1cdef844c9ed88fbc9181f90d920815e2c`).

I re-read the current exact saved `bridge.py` and recomputed its digest. SHA256 is `8f24510def275bc78938d85fa2a3edb7018d98c3ad68c890d2d47c9f81637a7a`; lines 112–114 use `sock.sendall(...)` for the ACK, followed by the unknown/finished handling. The candidate `FILE_HASHES.sha256` also verifies all listed bytes. Therefore the prior statement that the pinned file used one unchecked `stream.write(...)` was incorrect and is withdrawn. The source of that mistaken observation is unknown; no source-change inference is made. A deterministic short-write test is optional additional regression coverage, not a presently demonstrated defect.

This erratum changes no code or experiment status. Remaining candidate limitations—parent-owned per-arm maximum quotas, trusted physical-effect provenance, pair/worker integration, global scientific budget enforcement and runtime/resource supervision—remain as previously bounded. HOLD/no-retry remains unchanged.
