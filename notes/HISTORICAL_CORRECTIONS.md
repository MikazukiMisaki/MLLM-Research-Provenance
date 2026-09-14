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
