# SI-E2 proposal publication boundary

Status: proposal-only; root review pending. This inventory is for a later, separately coordinated publication and does not authorize staging or upload.

## Safe-to-publish proposal/evidence candidates

These files contain compact bindings, hashes, receipts, and engineering design only. They still require root-owner review before publication:

- `SI_E2_PROPOSAL.json` — exact proposal; no prompt body, task row, token IDs, model weights, adapter bytes, or cache payload.
- `ENGINEERING_ENV_PROPOSAL.json`, `ENGINEERING_ARGV_PROPOSAL.json` — proposed environment/argv; authorization hash is pending and argv is explicitly non-runnable.
- `FIRST_SOURCE_REPLAY_BINDINGS.json` — identity and hashes only; action text omitted.
- `FUTURE_READ_ONLY_MONITOR_PLAN.md` — proposed bounded monitoring/stopping design.
- `PROMPT_DIGEST.json` — digest and length metadata only, no prompt text.
- `PROPOSAL_HASHES.json`, `PROPOSAL_INPUT_HASHES.json` — file hashes and bindings, not underlying data.
- `RECORD.md`, `PUBLICATION_ALLOWLIST.md`, `LOCAL_ONLY_FILES.md`, `COMMAND_RECEIPT_INDEX.json`, `FILE_HASHES.sha256` — task provenance and inventory.
- `prompt_digest_receipt.json`, `proposal_input_hashes_receipt.json`, `safe_environment_receipt.json`, `final_proposal_state_receipt.json`, `proposal_finalization_receipt.json` — command metadata, return codes and output hashes; review path disclosure before publication.
- `raw/*.bin` — captured command stdout/stderr. Prompt capture emits digest/key/length only; input capture emits path/hash/size records. Publish only after content-level confirmation that no prompt, task row, credential, or token array is present.

## Local-only

The local-only inventory is authoritative for this delivery. In particular, helper scripts and `SAFE_ENVIRONMENT_VALUES.json` can disclose machine-specific paths/environment values. Do not publish any model/cache/data payload; none is copied into this task directory.

No publication, commit, or push was performed in this task.
