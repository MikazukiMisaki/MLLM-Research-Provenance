# Local evidence exclusions and redaction map

The following raw supervisor files are retained locally under `supervisor_raw/` and are intentionally excluded from GitHub because the JSON receipts contain machine-local absolute argv paths and process identifiers. Their SHA-256 digests are recorded in `supervisor_receipt_sanitized.json`; the sanitized receipt preserves the authentic run ID, status, exit code/source, implementation/protocol identity, exact command hash, event/branch hashes, runner-log hash, completion/interruption flags, and artifact-completeness flag. The raw command is thereby bound without publishing its local path strings.

| Local file (relative to this task directory) | Bytes | SHA-256 | Published substitute / omission reason |
|---|---:|---|---|
| `supervisor_raw/runner_exit.json` | 1,632 | `fd9f44777e2ef27bf920aa86c1e65f74fb65f2511b45f742bee544a7eba93d5f` | `supervisor_receipt_sanitized.json`; raw receipt includes machine-local argv paths and process identifiers |
| `supervisor_raw/supervisor_status.json` | 1,485 | `87d47f8ea8a2cf664a8c943a7bd7d44a7c5391d899814258e8a565e9fd5719f5` | `supervisor_receipt_sanitized.json`; raw status repeats local argv paths and process identifiers |
| `supervisor_raw/runner.log` | 26,981 | `986c8c7c43f977a9ad3bf030cb7d8a9b679fd18f65b8577bf191e64306ab12b3` | Redundant runner stdout retained locally; status, exit, event and branch hashes are authenticated by the sanitized receipt and offline verifier |

The task-owned successor evidence copied under `g2_evidence/` was checked for machine-home paths, temporary paths, bearer credentials, API-key patterns, and token assignments before upload; no matches were found. The runtime identity note mentions the `HF_HUB_CACHE` variable name as a configuration fact, but does not disclose its local value or a cache path. Local adapter/model/data/config/cache paths are represented by frozen identity and content hashes, not published paths.
