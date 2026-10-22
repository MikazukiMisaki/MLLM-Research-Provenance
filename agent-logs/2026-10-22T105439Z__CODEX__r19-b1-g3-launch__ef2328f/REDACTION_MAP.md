# Raw-to-sanitized evidence map

| Local raw source | Original SHA-256 | Uploaded sanitized substitute | Treatment |
|---|---|---|---|
| `review_raw/independent-review.txt` | `bcc32fd8d01b71882bf1377efad950834977c01f34c9980185034292dd367525` | `review_sanitized.md` | Preserves exact reviewed SHA, PASS conclusion, scope, reviewer caveat, and identified discrepancy; machine absolute paths omitted. |
| `supervisor_raw/runner.log` | `45eda8a835a07f841657da7ce00d0f5bddda182c1dc4f8cd50cfc7291f6e59cd` | `supervisor_receipt_summary.json` | Preserves observed import error, failure location, and pre-live-runner boundary; machine paths removed. |
| `supervisor_raw/runner_exit.json` | `7e1fc0771c78fa4022717c6b9926147f5565f6cdbe5e04cdec7f165cc732e6c4` | `supervisor_receipt_summary.json` | Preserves authentic run ID, implementation/protocol SHA, real exit code/source, and zero research calls. |
| `supervisor_raw/supervisor_status.json` | `e71147fe2f0f9097cbae38357c4b2186159fd0341d3211a9e7c9988f3c58474c` | `supervisor_receipt_summary.json` | Preserves failed status, incomplete-artifact state, and absent event/branch hashes. |
| Ignored local G3 gate JSON | `41ccaae32b1adebf22743f5c5f23df074820e7698d7b77ec97f1777c3c733e59` | `g3_gate_manifest_sanitized.json` | Preserves frozen hashes, review/G2 carry-forward identity, authorized limits, and offline gate result; all absolute runtime/input paths excluded. |

No scientific action or observation evidence was redacted. No authentic G3 scientific evidence was generated.
