# Excluded local supervisor files

These original supervisor files remain preserved in the local task directory. They are not uploaded verbatim because the JSON receipts embed machine-specific absolute command paths. The sanitized receipt summary is uploaded as `supervisor_receipt_summary.json`; the original receipt hashes are also recorded there.

| Local task-relative path | Size | SHA-256 | Reason |
|---|---:|---|---|
| `supervisor/runner_exit.json` | 1714 bytes | `96e8a0e3507c3d32880bfa1c281dc29238fc306aa5b84198499da2fc5c37831d` | Contains absolute local paths in `command_argv`; preserved locally and summarized without argv. |
| `supervisor/supervisor_status.json` | 1567 bytes | `3a9098e47a5e16e4381f77e5256a5878c4f639b21a5eec6d136934ad1afb19c2` | Contains machine-specific absolute paths; preserved locally and summarized without those paths. |
| `supervisor/runner.log` | 6584 bytes | `0ca35166eac10c1a359b5f9e4b2610be884ebd0bc32f534674b1e8753a2feb3d` | Byte-identical duplicate of uploaded task-root `runner.log`; original remains locally preserved. |

No excluded file was deleted or modified. `FILE_HASHES.sha256` inventories every uploaded evidence file except the inventory file itself.
