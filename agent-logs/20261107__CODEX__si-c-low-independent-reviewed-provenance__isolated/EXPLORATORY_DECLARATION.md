# C-low exploratory continuation: declaration before preflight

Status: **PROPOSED; NOT A PREFLIGHT OR LAUNCH CLEARANCE.** This declares one
possible model-training attempt, not a scientific result. Its purpose is to
check whether continuing the existing self-imitation development training from
the frozen P0 adapter at learning rate 5e-5 yields a valid candidate for a
later, separately reviewed comparison. It does not establish that changing
the rate improves agent success. Only the C arm would be newly trained.

The reviewed comparison is with the already existing 1e-4 C continuation and
P0, as descriptive anchors. Relative to the prior C training specification,
the new specification changes the learning rate and derived learning-rate
schedule; the protocol identifier also changes. The same development rows,
order, seed, 312 distinct examples, four passes, 1,248 presentations, batch
configuration, 78 optimizer updates, local base model and initial P0 adapter
are retained. The exact protocol and manifests require fresh independent
software and pair reviews. The derived B manifest is a binding for
the existing pair gate and is not a newly trained B model.

The prior development training data are reused; they are not an independent
evaluation set. No protected evaluation tasks are to be opened or used. A
useful improvement claim requires a separately designed common evaluation,
actual task isolation and adequate uncertainty; the present plan does not
solve those questions. Four proposed new self-authored development cases, if
later admitted, have only descriptive power. No model evaluation is authorized
by this declaration.

## Operational bounds and accounting

The one exact preflight is model-free and must report zero tokenizer, model,
CUDA, training and environment effects. Actual local files and the complete
runtime metadata are checked by the original source gate. Before training,
independently verify the new preflight, fresh source, current inputs and device
admission. A new, exact one-run clearance is required; no historical clearance
or failed run is reused. One live C-low attempt only; stop on failure, resource
violation or uncertain process cleanup, and do not automatically retry/resume.

The inner frozen protocol still binds 5,400 seconds and its existing GPU
limits. The proposed separately supervised outer live ceiling is 1,800 seconds
from launching the CLI, including its preliminary gate. This shorter ceiling
may interrupt a valid training run and therefore changes the operational
execution boundary; it does not change the scientific training recipe or
guarantee a completed model. Proposed preflight ceiling is 600 seconds.
Hard enforcement and cleanup are contingent on independently reviewing and
successfully running the outer supervisor; unobserved tails are UNKNOWN.

The training config permits at most 1,248 presentations, 78 optimizer updates,
700,000 input and 6,240 supervised tokens. The production path additionally
requires the exact expected C token totals, 695,872 and 6,240. No generation
or environment operation is intended in this training stage. Unexpected calls,
incomplete external effects and all actual costs must be recorded, never
treated as zero without evidence.

This is a shared A40, not an exclusive reservation. Before live admission,
sample the bound device for at least a minute, requiring the previously proposed
free-memory/utilization thresholds; keep device-wide telemetry separate from
the worker's own allocator statistics. The old gate enforces its own allocator
cap. Apply monitored storage stops and confirm free space, preserving partial
outputs. Sampling cannot rule out spikes or concurrent writes. Never terminate
another user's process or attribute whole-device use to this experiment.

Prior revision 2 proposed stage-3 96 GiB of accounted logical reads and a
4 GiB output reservation, but made complete native/mmap instrumentation and a
hard quota prerequisites. Those complete facilities have not been established.
For this exploratory attempt, replace that infeasible prerequisite with
source-based planned accounting, a free-space admission floor and sampled
stop thresholds, provided the independent review accepts the actual monitor.
These are practical controls, not hard physical-I/O or filesystem quota
guarantees: physical disk reads, unobserved native reads, sampling overshoot,
concurrent writes and crash tails remain UNKNOWN. The estimate of about
76.3 GiB for four base-tree hashes plus one shard-equivalent model load is a
conditional lower sizing reference, not total I/O; package trees and other
reads are extra. A separate preflight performs another base-tree hash.
This change supersedes only the earlier complete-meter/quota prerequisite; it
does not enlarge the one-run training, token or outer-time limits.

## Evidence

Preserve real preflight, process, resource, token, training and exit receipts,
including failures or partial output. Keep training examples, identities and
machine-specific manifests private; upload separately reviewed non-sensitive
receipts and integrity hashes. Missing provenance or model output is a stop,
not evidence of success. Actual global historical cost remains incompletely
known; do not label a selected subset as total project expenditure.
