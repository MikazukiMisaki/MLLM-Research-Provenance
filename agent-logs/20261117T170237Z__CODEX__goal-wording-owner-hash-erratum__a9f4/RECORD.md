# Goal-wording owner-journal SHA-256 erratum

Agent: Codex. Status: PASS, evidence correction only. Start: prior to 2026-11-17 17:02:37 UTC (exact time not captured). Record prepared: 2026-11-17 17:03:43 UTC.

The preserved [published failure transcription](../20261117T164500Z__CODEX__goal-wording-dev-failure__one-shot/RECORD.md) and its original `RUN_FAILURE.md` contain a one-character error in the **owner journal digest**, not in the journal bytes:

- Printed incorrectly: `7e94e1c2efbcaa62be2ce4b55714f3a1a461a836f9cf77e023e8bc5a68e562be`
- Correct SHA-256: `7e94e1c2efbcaa62be2ce4b55714f3a1a461a836f9cf77d023e8bc5a68e562be`

The digest differs at character 47. The owner journal is `agent-logs/20261118__PARALLEL__goal-wording-experiment__private/fixed-p0-goal-wording-01/eval-two-pair-a/owner/supervisor_events.jsonl` inside the published evidence archive. The local owner journal and that exact member extracted as a byte stream from the local archive both produced the correct digest. The archive is 137,451 bytes and SHA-256 `797128afad1a1a3e93dc12419d6eaeeefc463dba2cc766425190e17b1f515390`. The same archive SHA-256 was computed from its Git object at provenance commit `62f346b03e3b23ad96ae59ca54f509dd029036b0`; `git ls-remote` identified that commit as remote `main` at verification time. The user independently reports downloading the published archive and obtaining the same digest. This task did not independently redownload the archive from GitHub.

The initiating task's existing failure report and the user's independent update state that its authentic process-session wait returned exit 1. This erratum did not itself observe or re-create that wait. No `runner_exit.json` was found in the archive listing; a persisted runner-exit receipt is not claimed.

The one-shot remains consumed and incomplete; there is no paired treatment result. This correction does not authorize retry, relaunch, continuation, replacement output, model calls, environment calls, training, or held-out use. Existing published `RECORD.md`, source `RUN_FAILURE.md`, raw event logs, evidence archive, and original per-task hash inventory are preserved byte-for-byte.

Provenance base: `62f346b03e3b23ad96ae59ca54f509dd029036b0`. Work was performed in a separate provenance worktree on branch `codex/provenance-goal-wording-hash-erratum`; the scientific repository at `e537f441010077123a307e9d50ea40cf8dad8547` was not modified. Checks: SHA-256 of local archive and owner journal; SHA-256 of the owner member streamed from the archive; SHA-256 of the committed archive Git object; remote-main SHA lookup; one-character comparison of the two printed digests. Zero model, environment, scientific evaluation, training or held-out calls. Provenance commits and remote refs are resolved from Git history; this file cannot contain its own final commit hash.
