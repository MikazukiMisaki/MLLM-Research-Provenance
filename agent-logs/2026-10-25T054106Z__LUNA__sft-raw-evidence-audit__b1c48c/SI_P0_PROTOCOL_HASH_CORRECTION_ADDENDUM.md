# SI-P0 protocol-hash correction addendum

Status: read-only correction, additive to the frozen SI-P0 record. This note supersedes only the prior draft/addendum interpretation that treated raw JSON file hashes as mismatching protocol-declared manifest hashes. The original audit, draft, command receipts, and earlier addendum are preserved byte-for-byte.

## Verified raw and canonical hashes

The project helper `src/sft/protocol.py:40-45` defines canonical JSON as `json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))`, UTF-8 encoded before SHA-256. `scripts/build_sft_protocol_assets.py:49-54` computes the split and exclusion protocol bindings with this `sha256_value` helper. The current split/exclusion files are pretty-printed JSON, so their raw-byte hashes are expected to differ from canonical object hashes.

| Object | Raw file SHA-256 | Canonical SHA-256 (project helper) | Protocol declaration | Result |
|---|---|---|---|---|
| `sft_task_splits.json` | `5347163365e77f46517756156c22e803a7e5a6a54009f7151eab92fb51e6ff56` | `e6695359f2e6b53b74c54e9d9712b1f8bc8534487d85b659151c71eb1441e25d` | `e6695359f2e6b53b74c54e9d9712b1f8bc8534487d85b659151c71eb1441e25d` | match |
| `sft_task_exclusions.json` | `fdbe3b1c2d8162fa7c95ff25b57ace1eaf01c1224d42f9f1f447bf7a859541c5` | `8e0d04d315a16d4fd28ef04bf9bf92212ebc98bbba8a10dfe0e3acb2b9fbf798` | `8e0d04d315a16d4fd28ef04bf9bf92212ebc98bbba8a10dfe0e3acb2b9fbf798` | match |

The independent stdlib check also computed both `ensure_ascii=True` and `ensure_ascii=False`; both produce the same respective canonical hashes for these current objects. The protocol file raw SHA-256 is `dd06d08773e9842b2302263429c7a1752e968dcb30d2dd89f185c01ef9605155`.

## Corrected interpretation and boundary

The earlier “split/exclusion binding conflict” finding is withdrawn. The raw-SHA comparison was the wrong hash domain: the protocol stores canonical-object hashes, and the current objects match those declarations exactly. There is no demonstrated split/exclusion canonical-binding defect in the saved records.

This current-file verification does not by itself prove which bytes a historical training process loaded. Keep historical runtime/model/tokenizer/launch-receipt gaps as separate provenance questions; do not infer or manufacture runtime evidence from this hash match. No prior text or receipt was rewritten.

## Evidence and scope

- Machine result: `protocol_canonical_binding_check.json`, SHA-256 recorded in `PROTOCOL_CORRECTION_HASHES.sha256`.
- Reproduction: `verify_protocol_canonical_bindings.py`; actual return code 0, recorded in `protocol_binding_check_receipt.json`.
- Source helper and asset-builder hashes are in the machine result.
- Read-only stdlib JSON parsing and hashing only. No project imports, analyzer, validator, model/tokenizer/environment, training, replay, or tests; no original files, shared indexes, or scientific configuration were edited.

