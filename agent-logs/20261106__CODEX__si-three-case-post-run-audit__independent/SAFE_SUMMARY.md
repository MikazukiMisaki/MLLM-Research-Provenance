# Three-case symbolic engineering check

**Outcome: 3 of 3 predefined engineering cases completed their fixed action sequences and reached the specified goal.** This check used three self-authored symbolic variants, with actions fixed in advance. It is a software and evidence-contract check; it does not evaluate a language agent or establish a performance improvement.

| Case | Source and destination | Distractors | Recorded action steps | Result |
|---|---|---:|---:|---|
| 1 | Initially closed | 0 | 5 | Goal reached |
| 2 | Initially open | 2 | 3 | Goal reached |
| 3 | Initially closed | 2 | 5 | Goal reached |

The independently recounted event records show **3 constructions, 3 loads, 3 resets and 13 action steps**, with no recorded incomplete external operation. The worker completion records report **zero model calls**. Each case's supervisor recorded exit code 0 and successful contract validation; the campaign event record ends in `returned`. A separate tool observation reported campaign exit code 0, but there is no separately persisted outer-launcher exit receipt, so the campaign event and tool observation are distinct evidence.

The audit checked the full per-case event order, fixed action and state contracts, recorded input-hash agreement, and the current hashes of the authored problem, worker, supervisor and contract inputs. The raw evidence and selected input hashes matched their recorded bindings. The three case supervisor elapsed times were approximately 1.63, 1.53 and 1.63 seconds. The largest observed sampled resident-memory peak was approximately 100.8 MiB; sampling can miss peaks and is not a hard resource bound. No unrecorded operation can be ruled out by a ledger alone.

These variants share one authored template. They are **not held-out tasks or an independently validated test population**; their relationship to earlier data is unknown. The task-instruction quality and production adapter compatibility remain unverified. Consequently, these results do not establish training effectiveness, agent success-rate gains, generalization, or statistical significance. The raw output files remain local.

For byte-level reference, the campaign event record SHA-256 is `46f94173d7d1b361599074507f84e5d0d06292d66a43998c0528e1bf9bc3fb24`. The three per-case event-ledger SHA-256 values, in table order, are:

- `ff8b20c911b1c4ebc34557bdfa7c1c268891db6c97f732686930361783d21c11`
- `86f9e212c6c63279c38f4829897f79e1cdd3a063c98ef9372508a644bc09c357`
- `9837c528e244839a4214e1e4fe407124059f8d70316aded2432e327bea3ab3ff`
