# R19-B1 live successor proposal — PREPARATION ONLY

Status: `PREPARATION_ONLY`; **not ready to launch**. This is a concrete, hash-bound proposal for Sol's review, not a gate, clearance, authorization, or runnable launcher. No supervisor, preflight, model, ALFWorld, G2, G3, or G4 invocation occurred in preparing it.

## Proposed invocation identity

- Reviewed source: `/home/lizening/wt-r19-recovery-duration-v1`, detached and clean at `2da980f631badc25086d12db60d128ff507d3ae6` when checked.
- Current byte-exact gate: `configs/local/r19_b1_g3_gate_2da980f_phase1.json`, SHA256 `c285692615eaaf1c7cb7139b0417528022db6ee03c510de13f881d126f14415e`.
- Proposed scientific output (checked absent): `/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z`.
- Proposed supervisor record directory (checked absent): `/home/lizening/research-notes/agent-logs/2026-10-23T002200Z__LUNA__r19-g3-live-successor__2da980f/supervisor_live`.
- The supervisor must generate the fresh run UUID only after future authorization/clearance. `supersedes-run-id` remains `3d1ccea7e97f4727abf8e216ac6ec498`.
- The exact JSON argument arrays are `child_argv.json` and `supervisor_argv.json`; neither was executed. They preserve interpreter, entrypoints, protocol, gate, adapter, data root, ALFWorld config, and all scientific arguments from the consumed preflight. The only intended invocation changes are removal of the paired `--preflight-only` / `--preflight-receipt` child arguments, a fresh absent output and supervisor record path, and `evidence-class=live`.
- Environment values remain pinned to the actual preflight release. `environment_plan.json` records exact set/unset and supervisor-injected fields; no UUID is generated here. Do not inherit Python overrides or stale supervisor identity fields. Proposal/environment files have raw and canonical SHA256 values recorded in `RECORD.md`.

## Evidence and frozen bindings

`bindings.json` binds the actual independently reviewed preflight (`a9ca70cb082b4f2387d242664031b0bc`; authentic exit 0; `PREFLIGHT_ONLY_PASS`), its five raw supervisor artifacts, the untouched exact-SHA implementation review, accepted append-only known-failed adjudication, current gate/protocol, baseline amendment, G2 carry-forward, original failure event ledger/manifest/registry and supervisor receipt, G3 authorization and source-restart amendment/authorization/resolution event, model/adapter/runtime/input aggregates, schedule and exclusions. No protected bytes were changed. The preflight's seven scientific counters were zero and its output sentinel stayed absent. Its one-time release is consumed; no repeat preflight is proposed or authorized.

Historical failed source unit stays `in_progress`/incomplete, with the old evidence and its append-only known-failed disposition intact. It is not counted as success or rewritten as completed. Cumulative campaign cost entering any future successor is **177 model generations and 342 environment operations (330 non-reset + 12 resets)**. Do not subtract, replay for free, or conceal these costs.

## If separately authorized in the future

These are the existing limits, not new authorization: 127 TRAIN identities starting at schedule index 0; at most 120 initial attempts and 60 eligible states; fixed 30/15/15 allocation; `K=1..5`; horizon 50. Source remainder is 8,999 model calls and 8,999 environment operations. Other phase ceilings stay exactly as bound: model calls initial recovery 240, path extension 240, suffix 17,100; environment operations initial attempt 5,520, logical branch 18,000, path extension 2,940, replay gate 5,400. Global ceilings remain 26,988 model calls and 41,260 environment operations. No quota transfer, expanded schedule, automatic retry, or second successor.

For the first source episode, before the first action, compare against the preserved predecessor snapshot: reset state/observation and ordered valid actions; prompt and rendered prompt; raw generation and token accounting; parsed action, mapping and action map; frozen source identity, seed and schedule index. Any mismatch, uncertainty, or missing evidence means stop, preserve costs/raw receipts, and do not retry, tune, substitute output directories, or change code/configuration. Count no source completion until the actual production source validator accepts the complete episode. Genuine G3 provenance is required before report-only G4; synthetic reports are software evidence only. G4 execution is not proposed as released here.

## Pending decisions — deliberately separate

- Independent exact-proposal review: **PENDING**.
- Separate independent live-launch clearance bound to this exact proposal: **PENDING / NOT GRANTED**.
- Fresh explicit user scientific authorization: **PENDING / NOT GRANTED**.

Historical `APPROVED_BY_USER` markers and the preflight PASS do not satisfy either pending item. Do not execute these arrays or infer permission from the fact that the child array lacks preflight flags. A future attempt requires all three decisions above plus a fresh read-only drift/absence/process check; any proposal-byte or source/input drift invalidates this proposal.
