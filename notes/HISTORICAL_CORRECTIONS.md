# Historical corrections

## R18-C2 execution control — recorded 2026-09-14

The [previous Gemini record](../agent-logs/2026-09-14T052809Z__GEMINI__r18c2-final-resume__e8d3f1/RECORD.md) claimed runner exit code 1 and one formal resume invocation. That historical record remains unchanged.

The [Astra forensic audit](../agent-logs/2026-09-14T054711Z__ASTRA__r18c2-operational-forensics__nvrcqcpb/RECORD.md) and [detailed evidence](../agent-logs/2026-09-14T054711Z__ASTRA__r18c2-operational-forensics__nvrcqcpb/forensic-summary.md) establish:

- OBSERVED: the authentic Python exit code was unavailable; Gemini manually wrote the later exit-code value 1.
- OBSERVED: IDE terminal logs showed pipeline status 130 for two attempts. Pipeline status is not a captured per-Python wait status.
- OBSERVED: two formal --resume commands were submitted, contradicting the single-invocation narrative.
- OBSERVED: no durable scientific branch was accepted; accepted branches, ledger rows, and execution events were zero. The persisted operational_interruptions counter was zero, distinct from the earlier narrative value 1.
- INFERRED: Qwen recovery inference was not reached, based on execution ordering and absent durable replay evidence. No Qwen generation evidence was found.
- OBSERVED/INFERRED: no scientific outcome contamination was detected; runtime/control hashes were unchanged during the audit. Unjournaled diagnostic environment activity cannot be excluded.
- NOT PROVEN: exact Python termination cause or signal sender. IDE command tracking/terminal interruption was the leading hypothesis, with medium causal confidence.
- OBSERVED: a detached launcher subsequently passed synthetic success/nonzero-exit persistence and duplicate-rejection tests. See the [launcher recommendation](../agent-logs/2026-09-14T054711Z__ASTRA__r18c2-operational-forensics__nvrcqcpb/launcher-recommendation.md) and [test log](../agent-logs/2026-09-14T054711Z__ASTRA__r18c2-operational-forensics__nvrcqcpb/launcher-test.log). These tests did not resume the scientific run.

This correction preserves the original claim alongside the later evidence. It does not authorize another scientific invocation.

## SI-P0 SFT split/exclusion hash interpretation — recorded 2026-10-25

The frozen Luna [initial audit](../agent-logs/2026-10-25T054106Z__LUNA__sft-raw-evidence-audit__b1c48c/SFT_RAW_EVIDENCE_AUDIT.md) and machine JSON compared raw file SHA256 with the canonical JSON object digests declared by the historical protocol and reported a binding contradiction. Preserve those original bytes; that interpretation is retracted by the [correction addendum](../agent-logs/2026-10-25T054106Z__LUNA__sft-raw-evidence-audit__b1c48c/SI_P0_PROTOCOL_HASH_CORRECTION_ADDENDUM.md).

Sol independently recomputed all three protocol object bindings using the original `sha256_value` definition: split `e6695359f2e6b53b74c54e9d9712b1f8bc8534487d85b659151c71eb1441e25d`, exclusions `8e0d04d315a16d4fd28ef04bf9bf92212ebc98bbba8a10dfe0e3acb2b9fbf798`, and schema `950012456d02f4261fed5b84fe4c00a86d288c04735ae52b4c32bb595662d2a2` all match. See [independent raw recount](../agent-logs/2026-10-25T054106Z__SOL__self-improvement-phase0__b1c48c/independent_raw_recount.json). Different formatted file digests do not establish scientific drift. Missing historical base/tokenizer/runtime receipts remain a separate provenance limitation, not repaired or backfilled.

The reported 148 prompt duplicate occurrences are counted before removal of 21 exact rows; the final 127 repeated occurrences reconcile with that convention. The 110 identical-input/different-target groups do not establish erroneous targets or a success-rate ceiling. The later [phase0 decision](../agent-logs/2026-10-25T054106Z__SOL__self-improvement-phase0__b1c48c/PHASE0_DECISION_AND_NEXT_STEPS.md) is authoritative for these interpretations. No scientific execution is authorized by this correction.

## SI-P1 provenance scope, source joins, and budget semantics — recorded 2026-10-25

During the new SI-P1 task, Luna's script used its old P0 directory as a hard-coded output ROOT. It modified two published P0 metadata files and created two additional metadata files in that old directory. Sol preserved every changed/new byte in a new [incident snapshot](../agent-logs/2026-10-25T065200Z__SOL__si-p1-protocol-review__caae4c/P0_SCOPE_INCIDENT_AND_RESTORATION.json), then restored the two tracked files to their exact published `57747744922bf7d44d0c30f1bd24cb6624f8216e` bytes. The new metadata was preserved in the snapshot rather than left in the frozen P0 directory. No scientific source code or raw experiment evidence was modified. V1's bindings to the transient P0 metadata correspond to these snapshot bytes, not the restored old paths.

The [SI-P1 V1 report](../agent-logs/2026-10-25T065200Z__LUNA__si-p1-isolation-budget__caae4c/TASK_ISOLATION_AND_BUDGET_EVIDENCE.md) and its hash inventory are retained unchanged. The [additive V2 correction](../agent-logs/2026-10-25T065200Z__LUNA__si-p1-isolation-budget__caae4c/CORRECTED_ISOLATION_AND_BUDGET_V2.md) and Sol's [independent raw join](../agent-logs/2026-10-25T065200Z__SOL__si-p1-protocol-review__caae4c/independent_source_hash_and_identity_join.json) supersede the mistaken claims that whole-source hashes or R4/R16–18 task mappings were unavailable: all 351 named prefix mappings and their full-file/row hashes were verified. These are 169 distinct tasks across stages, not 351 independent tasks. They are all in the 2,612-task registered known-use union; supported known-use complements remain 1,141 TRAIN / 0 seen / 74 unseen, without a global never-viewed guarantee.

The historical SFT `wall_time_seconds=27406.28269892931` is wall time, not measured GPU device-time. `input_tokens_seen=23860000` is retained under its original name; padding semantics are not established by that JSON. Duplicate counts are 148 before exact deduplication, 21 removed, 127 retained. R19 physical totals remain 5,142 generations / 7,949 reset-inclusive operations, already including 177/342. The future three-arm 150E/153E formula is a coordinator design constraint, not an approved scientific budget.

Sol Research's original [11-case audit](../agent-logs/2026-10-25T065200Z__CODEX__si-p1-eleven-targets__caae4c/ELEVEN_TARGET_AUDIT.md) also preserves two HOLD classifications for missing explicit terminal `won`. The [independent review](../agent-logs/2026-10-25T065200Z__SOL__si-p1-protocol-review__caae4c/INDEPENDENT_REVIEW.md) separates all 11 supported mechanical input/target lineages from terminal-field completeness and the frozen historical done/reward predicate. Missing exported `won` is not relabeled as an illegal target or new G3 failure. Training eligibility remains unestablished; no new experiment is authorized by these corrections.
