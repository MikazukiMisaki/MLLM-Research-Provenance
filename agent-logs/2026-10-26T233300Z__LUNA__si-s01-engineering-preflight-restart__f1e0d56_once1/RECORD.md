# SI-S01 controlled restart preflight record

Status: `PREFLIGHT_ONLY_PASS_STATIC_INPUTS_BOUND_NOT_RUNTIME_READY`.

The single preflight-only invocation authorized by the release completed on
2026-10-26. It returned exit code 0 after 41.228 seconds. Its authentic stdout
reported `STATIC_ENGINEERING_INPUTS_BOUND_NOT_RUNTIME_READY`; it did not report
runtime readiness. The same receipt says the whole-file hashes were referenced
from a prior certificate rather than rehashed and historical input IDs were
unrecorded. The environment therefore cannot yet be declared ready to start the
experiment from this evidence.

Observed scientific/runtime counters were all zero: model loads, CUDA
initializations, environment constructions, generations, resets, steps, and
units. The proposed new output directory and launch claim remain absent. The
source checkout stayed clean at `f1e0d56a1be2a65876bbec5b8950fb76cda3eace` on
`codex/si-s01-shared-gpu-adapter`; the previous consumed claim retained its
expected SHA-256.

This release is consumed. No second preflight, live launch, worker, model, or
environment call is authorized by it. Return these receipts for independent
root review and wait for a new exact engineering clearance.

Raw receipts and output are preserved without editing:

- `PREFLIGHT_RELEASE_CONSUMED.json`
- `subprocess_receipt.json`
- `preflight.stdout.bin`
- `preflight.stderr.bin`
- `PREFLIGHT_RESULT.json`
- `POST_PREFLIGHT_CHECKS.json`
