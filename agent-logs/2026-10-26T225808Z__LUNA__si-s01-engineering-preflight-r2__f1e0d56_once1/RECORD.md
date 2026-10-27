# SI-S01 engineering preflight — corrected distinct release

Status: `STATIC_ENGINEERING_INPUTS_BOUND_NOT_RUNTIME_READY`. This was one new preflight-only release, distinct from the consumed timestamp-format attempt. It is not a live engineering launch or scientific experiment authorization.

Before starting, the release directory's `FILE_HASHES.sha256` passed; release SHA was `dcd0ae2ec1ca8cf6d86979f14818a05410814dcbf34f948f97f52546deff3f20`. Exact argv and environment canonical hashes matched the release, the stdlib-only startup receipt confirmed the isolated process environment including `LC_CTYPE=C.UTF-8`, both auth timestamps ended in literal `Z`, the corrected proposal/review/auth hashes matched, source remained clean at `f1e0d56a1be2a65876bbec5b8950fb76cda3eace`, and the new output and launch-claim paths were absent.

The exact production CLI child ran once, with `shell=False`, approved `preflight_argv`, explicit environment and cwd. PID 878555 returned 0 in 41.355473799 seconds. Authentic stdout is preserved in `preflight.stdout.bin` (525 bytes; SHA-256 `6c05bf959f7d38d62c6d3dd943276493e59100d34d309f9f2045aa1e32d9bd48`); stderr is empty (SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).

The preflight receipt binds the selected nine historical event references and reports `science_authorized=false`, `models=0`, `CUDA_initializations=0`, environment constructions/generations/resets/steps/units all 0, and `output_exists=false`. Whole historical trajectory and event journal hashes remain prior-certificate references and were not rehashed. The static status explicitly says `NOT_RUNTIME_READY`; actual model loading, GPU ownership/fit, CUDA initialization, and ALFWorld construction have not been demonstrated.

Post-checks confirmed unchanged release/commands/authorization/proposal/review, resource policy, pinned interpreter, historical game and trajectory-data hashes; source remains clean; the child has exited; output and launch claim remain absent. One ancillary stdlib-only post-check attempt failed because it assumed a top-level `sha256` key on the release JSON; it failed before hashing anything and was corrected. It did not rerun the preflight.

The one preflight allowance in this release is consumed. No retry, live command, worker, model, CUDA tensor, environment, R19/A96 science, training, or evaluation was invoked. Wait for independent Root verification and a separate live clearance.
