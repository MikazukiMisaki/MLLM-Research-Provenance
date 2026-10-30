# Independent resource-accounting review

**Decision: ACCEPT_SELECTED_RECORDED_LEAF_SUBTOTAL_WITH_LIMITS.** The reviewed `/home/lizening/research-notes/agent-logs/2026-10-30T060600Z__SOL__si-resource-raw-recount__8be2/THESIS_RESOURCE_EVIDENCE.md` has SHA-256 `d682a8e4fb56c447501a3fea3e774d64c574b04068a96ebbafbcda74e3598e0f`. Its `RAW_LEDGER_RECOUNT.json` and all three package inventory entries verify. This is accounting of seven specified journals, not the entire thesis or project, evidence of GPU exclusivity, an exhaustive physical-cost audit, or a future budget.

## Independent original-journal recount

`independent_recount.py` in this folder separately reads the seven original event journals identified by the accepted report, verifies their original SHA-256 before and after, and emits aggregates only. It independently reproduces the following completed-call counts:

| Journal | Completed generations | Completed reset-inclusive operations | Resets | Nonreset operations |
|---|---:|---:|---:|---:|
| R19 G2 replay predecessor | 0 | 19 | 1 | 18 |
| R19 G2 successful smoke | 176 | 322 | 10 | 312 |
| R19 G3 failed predecessor | 1 | 1 | 1 | 0 |
| R19 G3 completed successor | 4,965 | 7,607 | 334 | 7,273 |
| SI-S01 source96 | 1,959 | 2,055 | 96 | 1,959 |
| SI-M1 probe | 10 | 64 | 5 | 59 |
| SI-U1 paired evaluation | 5,001 | 5,247 | 246 | 5,001 |
| **Seven selected journals** | **12,112** | **15,315** | **693** | **14,622** |

The R19 subset is 5,142 / 7,949, and the SI three-journal subset 6,970 / 7,366. The former is already included in the seven-journal subtotal; do not add the R19 campaign aggregate to it again. The 15,315 measure is reset plus recorded nonreset operations, excluding lifecycle operations. Nonreset operations are categorized by their recorded type, not all assumed to be action steps.

For each of the four R19 journals, recorded generation and environment-operation start/completion counts agree, and the multisets of their full recorded identities agree per operation class. The four R19 root run IDs are distinct. This is stronger than an aggregate-only recount, but a multiset match does not establish a unique one-to-one call for every repeated identity, a full hash-chain verification, or absence of unrecorded activity. The four actual R19 journal files have distinct SHA-256s.

For each SI journal, every `unit_completed` has a unique `started_event` link to a recorded `unit_started` of the same unit and identity, and no started unit is unmatched; the recorded journal has one `run_closed`. Counts of linked starts/completions are source96 4,207/4,207, M1 85/85, SI-U1 10,746/10,746. The SI event schemas do not carry a root `run_id`, so this review does not infer separate process identities from absent root fields. Across all seven journals, no event ID occurs in two journals. Distinct event IDs are useful de-duplication evidence but cannot rule out different IDs for an unrecorded duplicated external call; original supervisor and process provenance remains separately required.

## Wrapper and lifecycle accounting

The completed G3 journal contains 169 `environment_step_completed` wrapper events in addition to 169 `recovery_environment_operation` completions. All 169 wrappers individually reference the corresponding physical operation's event ID, with matching prefix, command, recovery action index and transition; they represent the linked same events for counting and must not be added a second time.

The completed G2 journal similarly contains 12 wrappers, each linked by event ID to one of 12 physical recovery-operation records, with prefix, command and transition matching. **Eight of twelve linked records disagree in `recovery_action_index`.** This does not add external calls or change the verified 322-operation G2 total; it does mean one must not assert all historical G2 bookkeeping fields match. Earlier exact-SHA review `/home/lizening/research-notes/agent-logs/2026-10-22T234140Z__SOL__r19-exact-sha-independent-review__2da980f_198732/REVIEW.md` separately discusses correction of shared-callback recovery-index bookkeeping and carries forward genuine G2 evidence without re-running it. This recount does not establish the cause of every one of the eight discrepancies, nor rerun G2.

The SI source96, M1 and SI-U1 journals record 96+5+246 = **347 completed constructions** and the same **347 completed closes**. These 694 lifecycle calls are separate from—not embedded in or newly added to—the 15,315 reset-inclusive subtotal. They are lower-scope known lifecycle records, not a complete project lifecycle count.

## Training, timing and previously adjudicated engineering

Read-only access to the original P0 `training_result.json` confirms SHA `e6a47124200cacba4d1f3eaf97fdf79657d7df04f072a4d5446c2bec677c399e`, 2,354 optimizer steps, 23,860,000 recorded input tokens, and wall time 27,406.28269892931 seconds. Wall time is not the same as an established exclusive GPU interval. The accepted report's B, C, SI-U1 evaluation and engineering allocation values agree with the independently reviewed prior partial ledger (`PARTIAL_ACTUAL_LEDGER_V2.json` SHA `3c9060003bbf4b96e49afa596cabedbd53a5a6448edc611227d2ac2395937470`); I did not independently reread all underlying supervisor clock records during this task. The three reported B+C+evaluation intervals sum to 6,063.3355512162669 device-seconds, and should not be added to the same individual intervals. Four engineering intervals sum to 455.85605997219683 seconds. Neither interval shows exclusive access to a shared device.

The separately adjudicated failed-reset/successful-check pair is 2 physical resets + 1 step and 1 generation, outside the seven selected journals. The failed reset physically returned but failed logical completion; its reservation, return and failure are multiple observations of one call, not three calls. This limited review relies on the earlier independent archived-event adjudication in `/home/lizening/research-notes/agent-logs/2026-10-30T010000Z__CODEX__si-project-ledger-correction-independent/RECORD.md`; it did not re-extract or independently replay that private archive.

The older 1-generation/7-operation pre-source engineering aggregate remains nonadditive until its leaf identity and overlap are resolved. Input-token training counts, inference generation counts, logical per-policy token costs, reset-inclusive physical operations, model load/close, environment construction/close, device-allocation intervals and P0 wall time are different metrics. The R19 K2 vs CONTINUE logical-token average is not a physical spend or latency measurement and shared/aliased branches are not independent physical calls.

## Limits and evidence custody

The accepted source96 original journal currently resolves under `/tmp`; its observed input SHA matches, but durable raw-evidence custody requires separate verification before that temporary copy disappears. This audit has not verified whether a permanent or remote complete copy exists. Seven input file identities, before/after hashes, event counts and all linked aggregate checks are recorded in `INDEPENDENT_RECOUNT.json`; the wrapper ID checks are in the script. No raw task text or identifiers are included in this report. The checked records do not establish complete historical project costs, absence of unknown interrupted work, environmental process ownership, full journal chain validity or remote artifact availability.

No model, GPU, ALFWorld, runtime, formal G4/evaluation, or historical journal writer was invoked. The original report and journals were not modified.
