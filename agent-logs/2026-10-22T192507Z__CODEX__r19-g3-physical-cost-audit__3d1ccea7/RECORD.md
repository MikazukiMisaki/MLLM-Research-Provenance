# R19-B1 G3 physical-cost reconciliation

## Status

`PASS_READ_ONLY_COST_RECONCILIATION_NO_NEW_EXECUTION`

Agent: CODEX. Start UTC: `2026-10-22T19:25:07Z`. Finish UTC (record finalization): `2026-10-22T19:26:12Z`. This is a read-only audit follow-up; it does not authorize relaunch, repair, unit adjudication, or G4.

## Scientific identity and boundaries

- Scientific repository: `/home/lizening/wt-r19-recovery-duration-v1`, branch `codex/r19-recovery-duration-v1`.
- Scientific source SHA: local and origin `bf31f3da430ffc35bd17fc380e1752adce6d1467`; worktree clean.
- No scientific source, registry, manifest, event ledger, or runtime output was changed. No model/environment execution occurred in this audit.
- The consumed live successor remains run `3d1ccea7e97f4727abf8e216ac6ec498`, authentic runner exit `1` from `subprocess.returncode`. G3 unit registry remains `in_progress`, execution manifest `RUNNING`; these are incomplete persisted unit/run states, not evidence the process is still running.

## Independent event-ledger recount

Read-only JSONL parsing counted event kinds and operation identities from the original event ledgers and cross-checked the manifests and supervisor receipt. Event starts were paired against completions by trial, operation, schedule index, and payload operation.

| Evidence unit | Model generations completed | Non-reset physical environment operations | Resets | Operations including resets | Incomplete external operations |
|---|---:|---:|---:|---:|---:|
| G2 failed replay predecessor | 0 | 18 replay action steps | 1 | 19 | 0 |
| G2 successful smoke | 176 | 312 | 10 | 322 | 0 |
| Earlier G3 import failure `a0de515d7e104101bf8157175ea3d995` | 0 | 0 | 0 | 0 | 0 |
| G3 failed successor `3d1ccea7e97f4727abf8e216ac6ec498` | 1 | 0 action steps | 1 | 1 | 0 |
| **Cumulative observed total** | **177** | **330** | **12** | **342** | **0** |

G3 itself has exactly four ledger events: environment reset started/completed and generation started/completed. The completed generation consumed 267 input and 5 generated tokens. No `environment_step_started`/`environment_step_completed` or action-operation event occurred in G3. Its one source episode is unfinished (`in_progress`); this is distinct from incomplete external operations, which are zero. The process failure is established by the durable supervisor receipt and traceback, not inferred from the still-`RUNNING` execution manifest.

The G2 total reconciles directly from the two preserved G2 ledgers: the failed predecessor has 38 events (19 operation starts and 19 completions: 18 `smoke_replay_environment_step` plus one reset, zero generation); the successful G2 ledger has 1,063 events (176 generation starts/completions, 322 environment-operation starts/completions, including 312 non-reset operations and 10 resets). The earlier G3 entrypoint failure has no scientific output directory or manifest and its receipt records zero model generations, environment operations, or resets.

## Evidence hashes

- Failed G2 predecessor events: `b2d9045514bc3251ee3e954e4787569566cf7ba995821adbdb5af6b1dfdf065c`.
- Failed G2 predecessor manifest: `83ef899e4b241052b1fa03470f1c942f8b9ba8489afdd5d8ce24ac83e760977e`.
- Successful G2 events: `1456c43f7d3f0a849fe4bb8015164815fd70f4e2813d343449c1a34c2eaebe0c`.
- Successful G2 manifest: `7d8758bcc1fa5e40bb0f1b8f3e13707062104f6a2038673dd3cff93171de4c39`.
- G3 failed-successor events: `fde95fcd72f1c4ac6409fab7f2112654e145f6184fefec690cae58ad345f1cd7`.
- G3 execution manifest: `f5d3efa6c17abea3d944d7dea01099210d846eb8ed107057ec24502bbb51d2df`.
- G3 registry: `870923242ae585c66cbcffa554528ab3d92cf98fc4d87dee2c4d408f5f6ba800`.
- G3 runner-exit receipt: `a802079398fd415765b8f6b8685fec998325625da733011ff7a9ce11459a9386`.
- G3 supervisor status: `e2a70bf670376b648e52357376fa88f3a7a3cac92b41a5c628bd4ad251353913`.
- Prior G3 import-failure summary: `5a1558378b2168c1da7d358b070bfdf299841c532a5f10124e8405b63544c819`.

Machine-readable counts and complete evidence paths are in `cost_reconciliation.json`; read-only commands are summarized in `commands.log`.

## Provenance

The original raw failure evidence and task record were already pushed to the provenance repository. At audit start, local and remote `main` both resolved to `3fcca25b2dec2594204872a85715dff4162fd627`; those remote SHA-256 checks had matched for the failure bundle, task record, and independent audit. This reconciliation is uploaded as a new immutable provenance task directory; its final containing commit is resolved through Git history and reported separately because a commit cannot contain its own SHA.

## Decision

The one-live-successor clearance was consumed and the run failed. No retry, new output directory, source/registry/manifest edit, or G4 efficacy analysis was performed. Return this cost reconciliation to the reviewer; any scientific continuation requires a new scoped instruction and independently valid evidence/authorization.
