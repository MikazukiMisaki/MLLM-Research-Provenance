# Difference from design

Implemented in isolation: callback-compatible setup/verify interfaces; one shared materialized path triple per pair; two independently spawned synthetic arm processes; durable global reservation owner and independent per-arm ceilings; pre/post pair-input fingerprint; shared initial-public comparison; reservation-on-unknown and no resume.

Not implemented: importing or executing any real production adapter; the production actor, complete budget IPC and event semantics; immutable OS mount; production process-group lifecycle; real GPU ownership; model identity; input/output token ceilings; research wall-clock ceilings; scientific analysis; source-plan EOS reconciliation; exact-SHA scientific review. See README for detailed limits. No claim of real execution readiness.
