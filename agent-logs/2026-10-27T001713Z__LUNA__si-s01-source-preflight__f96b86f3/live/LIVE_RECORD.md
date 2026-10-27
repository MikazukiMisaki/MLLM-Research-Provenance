# SI-S01 A96 source-only live run record

Status: `LIVE_RUN_COMPLETE_RAW_EVIDENCE_ARCHIVED_LOCALLY_PENDING_ROOT_AUDIT_AND_PUBLICATION`  
Run ID: `f96b86f3391940eaa9d75040c444a8e4`  
Record finalized: 2026-10-27T01:05:00Z

## Execution

The single authorized production invocation completed with authentic supervisor
return code 0 and cleanup established. It ran from
`/home/lizening/wt-si-s01-shared-gpu-adapter`, clean at
`f1e0d56a1be2a65876bbec5b8950fb76cda3eace` on
`codex/si-s01-shared-gpu-adapter`. The exact argument and environment digests
are recorded in [LIVE_CHILD_START.json](LIVE_CHILD_START.json) and
[LIVE_SUBPROCESS_RECEIPT.json](LIVE_SUBPROCESS_RECEIPT.json). The supervisor
started at 2026-10-27T00:26:37.318091Z and exited at
2026-10-27T01:00:22.356308Z. Supervisor PID 882767 and worker PID 882823 were
both absent after completion. There was no automatic retry.

The authentic production report says
`COMPLETE_SOURCE96_STRUCTURAL_NO_GO`: 96/96 normal sources and trajectory rows,
the source phase sealed, 16,455 contiguous event-ledger entries (sequence
0–16,454), one run-closed event, and zero failed or open units. It explicitly
records `all_YT: null`, `TEACHER_NOT_AUTHORIZED_SOURCE_ONLY`, and
`NOT_LEARNING_OR_TEACHER_ACCEPTANCE`. This is not a learning, teacher, or final
scientific acceptance pass.

Production physical counters for this run are 1,959 generations, 1,164,593
input tokens, 9,795 generated tokens, and 2,055 environment operations:
1 model load, 96 environment constructions, 96 resets, 1,959 steps, and 96
closes. Authentic supervisor allocation is 0.5624755142595516 device-hours.
The report's 0.5456197222185114 stage figure is a lower bound, not an additional
cost to sum with supervisor allocation. The production report's historical
unchanged field (5,142 generations / 7,949 environment operations) is retained
as a separate historical value, not merged with this run's delta.

Shared-container accounting was nonexclusive; NVML-to-local-PID mapping remains
`UNPROVEN_NOT_ASSERTED`. No exclusive-GPU or device-wide attribution claim is
made.

## Raw evidence and archive

The nine original output files total 474,608,517 bytes. Their exact sizes and
SHA-256 values are recorded in [LIVE_RESULT.json](LIVE_RESULT.json) and match
the supervisor's output-at-exit receipt. The complete 41-member evidence bundle
is at:

`/tmp/si_s01_source_uid-2000_run-f96b86f3391940eaa9d75040c444a8e4_oxwwsyg4/publication/luna_source_bundle_f96b86f3/si_s01_source_f96b86f3_evidence.tar.gz`

Archive SHA-256:
`474a9264bc483b2c641842478f5dcd8287e8d01a60a764c8dd84d892a922ef0a`;
size 17,608,129 bytes. The independent round-trip check recorded here in
[RAW_ARCHIVE_VERIFICATION.json](RAW_ARCHIVE_VERIFICATION.json) confirms all 41
members match their originals and all original files' pre/post hashes are
equal. The bundle excludes input dataset payload, model weights, adapters, and
cache. Archive and records remain local-only; Root is responsible for its own
independent review and publication. No shared index, staging, commit, or push was
performed.

## Scope boundary

The single-use source-only live allowance is consumed. No teacher, training,
evaluation, G4, retry, or additional experiment is authorized by this record.
Prelaunch wrapper aborts and monitor-path mistakes remain preserved in their
original incident records; none launched another production run or changed the
scientific output. See [LIVE_MONITOR_INCIDENTS.md](LIVE_MONITOR_INCIDENTS.md).

Machine-readable summary: [LIVE_RESULT.json](LIVE_RESULT.json). The top-level
preflight record and its `FILE_HASHES.sha256` are unchanged; this live record is
an additive subdirectory record.
