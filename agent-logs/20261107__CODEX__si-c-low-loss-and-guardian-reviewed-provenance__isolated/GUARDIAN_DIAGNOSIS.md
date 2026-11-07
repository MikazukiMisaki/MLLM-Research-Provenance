# Guardian observation error: independent read-only diagnosis

## Scope and identity

Read only the explicitly designated original guardian `events.jsonl` and `exit.json`, and the actual enabled guardian source. No scientific input, task data, model, GPU, environment, or training process was accessed. Source SHA256: `77cb06dc267234d69d9f0a1d8a2b7d3e9e62447180c8c0e3ac64c2fedb86850b`. Raw event SHA256: `7da17ec933c334ab1c0e3f1844ce386b0a5ac27ccb5bbfb5faabefe62c8e38ed`. Exit SHA256: `9a3bb921c0c3cdc60ec2b1abac2b1a9bff864f2b19259b3fd7de33ebe5d8a310`.

## Established observations

The original journal has 240 records, with a valid sequence/hash chain: one guardian start, one spawn request, four observed-process records, 233 device samples and one finish. The finish payload equals the exit receipt. Direct child return code is 0; deadline was not triggered; `error` and `stop_reason` are null. The guardian recorded `observation_errors=true`, zero signal entries, zero observed processes alive after cleanup, and `unseen_descendants=UNKNOWN`. Final status is `STOP_FAILED_OR_UNKNOWN`. These records corroborate only the outer monitor's own observations; no inference of training quality or unobserved process absence is possible. They contain no event giving the site, exception type or moment at which the observation flag first became true.

## Candidate paths and limiting evidence

Code sets this same boolean for several distinct mechanisms: a discovered PID or parent becomes unavailable or changes identity, ownership/parent/start-time mismatch, pidfd opening failure, `/proc` child-list discovery failure, monitor/cleanup exceptions, pidfd poll or close failure, wait/reap failure, fd-close failure, or inability to restore the subreaper/signal state. GPU telemetry failure paths also set the flag, but the recorded null stop_reason and error and normal completion do not match the ordinary GPU gap/lost branch, which explicitly assigns a non-null stop reason. This rules out only the recorded normal manifestation of those branches, not every possible external disturbance. No signal entries and no recorded survivors do not prove no process escaped discovery.

The code writes process-observed events only after identity checks succeed; it does not record failures at the point that the flag is set. Thus the original records cannot discriminate the listed causes or identify when the first failure happened. In particular, a short-lived process is a hypothesis, not an established cause.

## Controlled synthetic reproduction

`synthetic_repro.py` imports the hash-verified exact guardian and calls only its built-in fake CLI against temporary directories, with no CUDA or model. It interposes only the child-discovery helper. In one scenario, a completed and reaped local toy PID is artificially returned in a child listing to simulate disappearance between discovery and identity lookup. In another, the helper is made to raise a synthetic PermissionError. Each case yields return code 0 from the toy direct child, null error/stop, no deadline, zero signals, no observed survivor, observation_errors=true and STOP_FAILED_OR_UNKNOWN. These reproductions show the coarse signature is not diagnostic; the artificial listings do not establish what occurred in the real run. Output: `synthetic_repro.log`.

## Minimal follow-up

For future guardian revisions only, keep the existing fail-closed status and all identity/signal safety checks. Record a bounded reason enum, monotonic timestamp and stage for every assignment of observation_unknown; distinguish at least child-discovery read failure, identity disappeared/mismatch, pidfd open/poll/signal failure, cleanup/wait/reap, and restoration. Record safe aggregate counters; avoid leaking private process identifiers. Preserve UNKNOWN if reason-recording itself fails. Add separate synthetic tests that inject each failure, assert nonzero/unknown status, reason/ordering, no unrelated process signaling, incomplete-record handling, and a clean-success control. Review/freeze the new exact source before future use. Do not edit the original journal, change the historical flag, automatically retry, or infer a successful outer monitor from internal training completion.
