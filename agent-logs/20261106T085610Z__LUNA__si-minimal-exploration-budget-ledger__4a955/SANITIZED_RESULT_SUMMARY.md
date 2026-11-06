# Sanitized result and candidate summary — SI minimal exploration

**Current decision: no concrete executable training/evaluation candidate is
established.** The reviewed design is useful as a prospective comparison, but
its eligible input surface, `N`, loader scope, and full resource budget remain
unknown. No task, trajectory, manifest, or protected input was opened for this
summary.

## Candidate in the reviewed design (not executable)

Proposal V3 describes a fixed, paired development comparison of P0, uniform
continuation C1, and targeted-weight continuation C4, with one fixed training
product per C1/C4 arm and `H=50`. It calls for the same starting checkpoint,
examples, order, dose, optimizer and seed policy, with only the preregistered
loss weighting differing between C1 and C4. It requires complete outcome
denominators and failure states, and does not claim statistical confirmation or
generalization.

The historical P0 65/82 and self-experience 67/82 are already-exposed TRAIN
results, not an independent development asset or a new evaluation instance.
The prior one-step run is explicitly `live_engineering_only` with
`scientific_result=false`; its run ID is not a reusable asset identity, and its
one-run clearance is consumed. No independently addressable, non-protected
development training input or evaluation instance—with version, source,
documented prior use, and loader-visible scope—can be named from the reviewed
sanitized records. Its existence and applicability are **UNKNOWN**, not
“absent.”

## Actual one-step engineering evidence

- Run: `35a71802c2dd4f4c95171af2d87a47a2`; source revision:
  `4a9556375e4c299c26dc5abd07f7325b9587a132`.
- Evidence class: `live_engineering_only`; report flag:
  `scientific_result=false`.
- Authentic outer and inner return codes: `0`; cleanup was recorded as
  established.
- Actual counters: 1 generation; 267 input tokens; 5 output tokens; 1 reset;
  1 step. No training or held-out use.
- Outer elapsed: 104.1789 seconds. The inner receipt reports
  0.028890565521756395 device-hours. The outer record labels actual allocation
  `UNKNOWN_FROM_OUTER`; PID-to-device ownership was not established.
- Peak allocator-reported memory: 17,125,454,336 bytes allocated and
  17,146,314,752 bytes reserved. This is inference-path evidence, not a
  training-memory estimate.
- The saved 24-row journal passed independent canonical event-hash, sequence,
  and previous-link checks.

Source for those actuals: sanitized engineering summary SHA-256
`34a6c74eef1595f044550b9d63c423b7c8369c405ab0c9f73d7e099da04280b8`;
engineering-report SHA-256
`e9853c364672c76975f02f136f55e4aa89abd9c95d91a569d313a48771840297`;
inner-exit SHA-256
`9b1ee400e9f6fe65258744b1fc5eed377c74bd89f8c5d3b87da506df09104963`;
outer-exit SHA-256
`6764310541fe91eabbc86ec819bfb1202432f785212c8cd272ae1ccf98efcea7`;
resource-log SHA-256
`fab0f3377704850b67274e6fee1b2dda2bcf26d3439663ac94c0151ffa7f715e`.

## Proposed thresholds—not forecasts or authorization

The design proposes monitored thresholds of 1.5 device-hours for each of two
training arms and 1.0 device-hour for each of three evaluation arms, totaling
6.0 device-hours sequentially on one GPU. An optional single full P0 episode has
a separate 0.5-hour threshold. These are proposal stop thresholds, not proven
hardware limits. New self-experience acquisition is a separate, presently
unspecified budget and is excluded. The only run-specific caps from the
consumed engineering authorization are not reusable for this design.

For `H=50`, the proposal's arithmetic is `3N` episodes, `150N` generations and
`153N` environment operations including resets. If the eventual runtime really
uses caps of 8,192 input and 16 output tokens per generation, the conditional
maxima are `1,228,800N` input and `2,400N` output tokens. `N=16` is an arithmetic
example only, not evidence of 16 eligible instances.

## Remaining blockers and next evidence

Before turning the comparison into a bounded candidate, obtain a narrowly
scoped metadata summary for one individually addressable development asset:
opaque identity and version/content hash; source and production stage; known
prior use and permitted role; exact loader-visible scope; eligible count and
family/parent grouping; and a complete, auditable exclusion/overlap summary for
protected and already-used scopes. No task text is needed. If this metadata does
not establish the specific candidate's scope, keep it `UNKNOWN` rather than
searching raw inputs.

Then fill the cost ledger with actual episode/parent counts, tokenization and
training-step settings, and explicit CPU/RAM/storage/device ceilings. Independently
review the exact production loss/masks, runtime, accounting, and stop controls.
Separate acquisition, training, and evaluation costs; preserve the full
cleanup tail; and do not use the one-step duration or memory as a forecast.

No experiment, model, environment, training, preflight, or supervisor was
started while preparing these files.
