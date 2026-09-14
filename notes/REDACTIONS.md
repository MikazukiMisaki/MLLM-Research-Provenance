# Provenance import redactions

Before the first Git commit, actual local IDE session/CSRF token values were replaced by `[REDACTED_SESSION_TOKEN]`. Opaque signed model metadata was conservatively replaced by `[REDACTED_OPAQUE_SIGNATURE]`; its authentication significance was not assumed. No removed value is reproduced here.

26 occurrences were sanitized across seven evidence files: 20 session-token occurrences and six opaque-signature occurrences. Historical RECORD.md files and their factual claims were not rewritten. Documentation mentions of authorization, token paths, cookie/API-key names, and example patterns are not credential values.

The [redaction manifest](../agent-logs/2026-09-14T061140Z__ASTRA__provenance-repo-initialization__wo8b4ovs/redaction-manifest.json) identifies each affected path, category/count, original SHA256, and sanitized SHA256. No unredacted backup was created in this repository. Originals outside research-notes were not scanned or changed.

Old artifact-inventory/hash files are retained as historical evidence and can refer to pre-redaction bytes or ignored local files. Their apparent mismatch is explained here; use FILE_HASHES.sha256 for current committed sanitized content.
