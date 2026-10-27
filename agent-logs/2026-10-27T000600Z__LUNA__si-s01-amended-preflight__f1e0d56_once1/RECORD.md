# SI-S01 amended preflight-only record

The single preflight invocation authorized by the framework-default amendment
completed with authentic return code 0 at 2026-10-27 00:07:20 UTC. Its exact
status was `STATIC_ENGINEERING_INPUTS_BOUND_NOT_RUNTIME_READY`. All reported
science/runtime counters were zero; the proposed run output and launch claim
remain absent. This does not authorize or establish a live experiment.

The only environment change from the prior release was the explicitly reviewed
`CUDA_MODULE_LOADING=LAZY`; the remaining environment map was preserved. The
child ran the released preflight argv with inheritance disabled, `shell=false`,
and the pinned interpreter. Source `f1e0d56a1be2a65876bbec5b8950fb76cda3eace`
remained clean and matched the remote branch. Both historical revocation claims
remain byte-identical to their pinned hashes.

Interpret the verbatim receipt carefully: `whole_file_hashes` refers to prior
certificates for historical trajectory/event whole-file hashes, not to current
frozen model/P0 input files; `historical_input_ids=UNRECORDED` is an accepted
historical limitation, not a new blocker. Neither value is reconstructed or
used to broaden the release.

This preflight release is consumed. No retry, second preflight, live command,
model load, CUDA initialization, or environment call is authorized here. Raw
stdout, stderr, subprocess receipt, and the pre-start consumption marker are
preserved in this directory. Await independent root verification and a separate
exact live clearance.
