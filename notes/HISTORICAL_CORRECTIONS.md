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
