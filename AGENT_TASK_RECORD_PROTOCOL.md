# AGENT TASK RECORD PROTOCOL v2

Every Astra/Gemini task must create a unique immutable task directory under `agent-logs/<UTC>__<AGENT>__<task-name>__<unique>/`, outside all scientific Git worktrees. Never overwrite an earlier directory. A record may be developed during its task; finalize it at task completion and preserve the finalized historical record thereafter.

Each task MUST end with `RECORD.md`, regardless of PASS, FAIL, STOP, or ERROR. Finalize the record even after failure or a stop condition. Records do not authorize additional execution.

## Required record fields

- Agent and task.
- Start UTC, finish UTC, and status.
- Scientific repository, branch, starting SHA, and ending SHA (UNKNOWN or not applicable when not observed).
- Exact commands or command summary, worktrees used, target commits, and files changed.
- Tests executed with exact results; distinguish checks not performed from checks that passed.
- Scientific model calls, ALFWorld calls, held-out usage, and execution boundaries.
- Commits, merges, pushes, resulting refs, and artifact hashes.
- Unexpected events, final decision, and next authorized step.

Save useful command output in `commands.log`, test output in separate logs, and runtime/result summaries when applicable. Distinguish OBSERVED, INFERRED, and NOT PROVEN. Never synthesize a missing exit code or substitute a monitoring-shell status for the runner's real status.

## Role policy

ASTRA may write scientific code when authorized, write/fix tests, and owns implementation, engineering fixes, and final technical/scientific acceptance.

GEMINI is execution-only by default. It may run authorized commands/tests, monitor, collect logs/hashes, create provenance records, and push provenance repository records. It MUST NOT edit scientific source code, MUST NOT edit scientific tests, MUST NOT repair unexpected scientific failures, and MUST STOP and return evidence to Astra on unexpected failures.

These roles do not expand a task's scientific authorization. A provenance upload is not permission to resume, replay, infer, train, or change scientific state.

## Automatic provenance synchronization

At the end of every task:

1. Finish RECORD.md, including failure or STOP outcomes.
2. Hash key files; refresh FILE_HASHES.sha256 for intended committed content, excluding itself, .git, and ignored files.
3. Update INDEX.md with the task's status and relative record link.
4. Scan the task directory for secrets; review matches and redact actual credentials before staging.
5. Commit only provenance-safe files in this repository.
6. Push to MLLM-Research-Provenance/main without force operations.
7. Record the provenance Git commit SHA inside RECORD.md if practical. A record cannot contain its own final commit SHA; cite an earlier checkpoint SHA and resolve the containing commit through Git history. If needed, preserve an ignored local post-push-receipt.json with final verification, and report the exact final SHA to the user.
8. Never modify the scientific repository merely to record provenance.

If remote access fails, preserve and finalize the local record, report the exact error, and do not alter SSH keys or credentials. Do not claim synchronization succeeded until local HEAD equals the verified remote main.

## Size and content policy

Only provenance, audit, log, and summary artifacts belong here. Never import weights, adapters, datasets, caches, keys, tokens, passwords, cookies, authentication files, secret .env files, or arbitrary home-directory contents.

Files up to 1 MB are normally suitable; inspect usefulness at 1–10 MB. Do not automatically commit files above 10 MB; above 50 MB keep local unless explicitly authorized. For omitted raw files, preserve local path, byte size, SHA256 and omission reason, plus a concise remote summary. Ignored transient PID/lock/cache files may remain local; preserve relevant evidence in ordinary logs.

## Historical integrity and redaction

Do not rename task directories or rewrite historical records for style. Add corrections in notes/HISTORICAL_CORRECTIONS.md and link the contradicting evidence. Necessary credential redaction is an explicit exception to byte preservation: document files and redaction categories, keep original and sanitized hashes, and never publish the removed credential. Do not silently rewrite old hash inventories; FILE_HASHES.sha256 represents current sanitized content.
