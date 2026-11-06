# SI-E2 bounded engineering run — public-safe result

## Decision

The single authorized, bounded engineering run completed successfully as an
engineering smoke. It is explicitly **not a scientific result** and does not
establish readiness for a full training or evaluation campaign. The run's sole
live-launch allowance is consumed; this record authorizes no further execution.

## Bound execution

- Run ID: `35a71802c2dd4f4c95171af2d87a47a2`
- Scientific source revision: `4a9556375e4c299c26dc5abd07f7325b9587a132`
- Independent implementation review: `1c31d33436841ccf894fd4780de95f5066b17f55bad744521be8152b1179e14e`
- One-run clearance SHA-256: `d1be535203aac731b45c1eec642472674d2dab32ba1429c0189ec25880c42709`
- Authorization SHA-256: `142ae35cec69db70328f73e349eb3f4a29b2d314c46de5c6d654fbda3bd0dd57`
- Canonical runtime-environment SHA-256: `560e3c0d379e092292c60590097645fb70725230d74d140bfc2ed45962491c43`
- Evidence class: `live_engineering_only`; scientific result flag: `false`.
- Outer supervisor and worker return codes: both `0`; both authentic exit receipts
  record cleanup established, no cleanup errors, no surviving descendants, and
  completion within the authorized time cap.

The production path completed one model-load lifecycle, one environment
construction, one reset, one generation, one selected-action step, and orderly
environment/model close. Observed work was 1 generation, 267 input tokens, 5
output tokens, and 2 environment operations (1 reset + 1 step). No training,
held-out use, or additional task was performed.

## Resource evidence

- The outer supervisor recorded 104.1789 seconds elapsed. Its conservative
  one-device elapsed estimate is 104.1789 device-seconds (about 0.02894
  device-hours); `actual_device_allocation` remains `UNKNOWN_FROM_OUTER`.
- The inner receipt reports `allocated_device_hours=0.028890565521756395`.
  These are receipt-defined timing values, not an independently measured GPU
  power or utilization integral.
- Resource records identify the expected GPU UUID at each measured checkpoint;
  PID-to-device ownership remains `UNPROVEN_NOT_ASSERTED`.
- Peak allocator-reported memory was 17,125,454,336 bytes allocated and
  17,146,314,752 bytes reserved. No allocator OOM or retry was recorded.
- A post-run point snapshot at 2026-11-06 06:23:45 UTC showed 46,068 MiB total,
  45,390 MiB free, 14 MiB used, and 0% utilization. This is one observation,
  not a durable capacity guarantee.

## Integrity checks

- The 24-row event ledger was independently rehashed using the production
  journal's canonical JSON encoding; sequence numbers, previous-event links,
  and every event digest matched. Ledger SHA-256:
  `8713431ff9335560ab604d6618f6743a24b093690b40913c5159bc94afe8fdc9`.
- The result report says `COMPLETED`, `step_executed=true`, and
  `scientific_result=false`; report SHA-256:
  `e9853c364672c76975f02f136f55e4aa89abd9c95d91a569d313a48771840297`.
- Inner supervisor-exit SHA-256:
  `9b1ee400e9f6fe65258744b1fc5eed377c74bd89f8c5d3b87da506df09104963`.
- Outer supervisor-exit SHA-256:
  `6764310541fe91eabbc86ec819bfb1202432f785212c8cd272ae1ccf98efcea7`.
- Launch-context SHA-256:
  `4e04814ca53cacdcd8a3e09cb60b4c5f926e72decafecfa417957220f37cda22`.
- Pre/post runtime-import receipts are byte-identical, each SHA-256
  `061059d6acb8a2a689b5a66f2874ef2452b152065cf85743a5234ce3c9fa4980`.
- The source checkout was clean at the exact reviewed revision after exit; no
  scientific source or configuration was changed.

## Scope limits and publication

This run validates one bounded production engineering path only. It does not
prove scientific effectiveness, cohort-scale reliability, sustained memory or
throughput, training readiness, or GPU process ownership. It does not grant
permission to train, evaluate a cohort, or repeat this run.

Raw event, context, runtime, and supervisor files are intentionally retained
locally: they include machine-specific paths and/or prompt, state, action, or
runtime details. This document and `PUBLIC_ARTIFACT_HASHES.txt` contain only a
sanitized summary and file hashes, not raw payloads. The local-only inventory
records omitted raw paths, sizes, hashes, and reasons.

Provenance publication was attempted through the configured Git remote, but
`git ls-remote origin refs/heads/main` returned `ERROR: Repository not found`.
No credentials were changed, no files were committed or pushed, and the shared
index was left untouched. This local summary is therefore **not yet published**.
