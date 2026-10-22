# Excluded and local-only evidence

The following files are retained locally and intentionally excluded from GitHub because they contain machine-specific absolute paths or runtime configuration. Their sanitized, hash-linked summaries are uploaded in this task directory.

| Local-only artifact | Bytes | SHA-256 | Exclusion reason | Uploaded substitute |
|---|---:|---|---|---|
| `review_raw/independent-review.txt` | 3321 | `bcc32fd8d01b71882bf1377efad950834977c01f34c9980185034292dd367525` | Raw reviewer response embeds machine-specific absolute paths. | `review_sanitized.md` |
| `supervisor_raw/runner.log` | 602 | `45eda8a835a07f841657da7ce00d0f5bddda182c1dc4f8cd50cfc7291f6e59cd` | Raw runner log includes local paths. | `supervisor_receipt_summary.json` |
| `supervisor_raw/runner_exit.json` | 1648 | `7e1fc0771c78fa4022717c6b9926147f5565f6cdbe5e04cdec7f165cc732e6c4` | Raw receipt contains machine-local execution details. | `supervisor_receipt_summary.json` |
| `supervisor_raw/supervisor_status.json` | 1500 | `e71147fe2f0f9097cbae38357c4b2186159fd0341d3211a9e7c9988f3c58474c` | Raw receipt contains machine-local execution details. | `supervisor_receipt_summary.json` |
| `configs/local/r19_b1_g3_gate.json` | 4903 | `41ccaae32b1adebf22743f5c5f23df074820e7698d7b77ec97f1777c3c733e59` | Ignored machine-specific gate includes local runtime/input paths. | `g3_gate_manifest_sanitized.json` |

No G3 execution manifest, event ledger, branch ledger, or result directory exists; these are not omitted artifacts. The earlier G2 evidence remains in its prior task directory and is not regenerated or duplicated here. Unrelated untracked supervisor directories from earlier tasks were neither staged nor modified.
