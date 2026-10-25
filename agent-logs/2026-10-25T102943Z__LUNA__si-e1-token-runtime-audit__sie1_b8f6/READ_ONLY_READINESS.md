# SI-E1 read-only engineering readiness

Status: `READ_ONLY_AUDIT_COMPLETE__RUNTIME_NOT_READY`.

This document reports feasibility evidence only. It is not a release, gate, schedule, executable command, or authorization to collect, train, evaluate, or run a model/environment.

## Frozen identity and scope checks

- The P3 engineering contract and authoritative prior protocol/review were hash-checked; recorded exact hashes are in `input_bindings.json`.
- The source repository read-only checkout was `4f5c2e18e0dfdf48e9471fcba0a3ee715be3ca3b`, branch `codex/progress-aware-recovery`, clean and tracking its matching remote branch. The required scientific commits `85cbb92395e5e2420c2adeb1fa0634653e742910` and `2da980f631badc25086d12db60d128ff507d3ae6` were verified to exist as commit objects; this audit did not switch/check out a worktree.
- Provenance repository was at `1962a074a67d6a485feaa7c3b3e01cddc465c1f8`, equal to its observed `origin/main`; existing unrelated untracked records were left untouched.
- Cached snapshot revision, actual P0 adapter tree, balanced dataset, SFT inputs, helper source files, P1 known-use registry, and P3 metadata/protocol/review were individually hashed and rehashed. The 24 before/after bindings were identical. Exact values and paths are in `input_bindings.json`.
- S120 was selected by the fixed P3 hash rules from known-use `expert_train` identities and the balanced expert dataset. It contains exactly 120 unique tasks with family quotas: pick-and-place 44, clean 32, cool 20, heat 11, two-object 13. All 120 have compact row-level selection and quality provenance. Intersections with the adopted acquisition-96, engineering-development-48, final-evaluation-600, and unallocated non-light reserve identity sets are all zero. No task was substituted to fit tokenizer limits.

## Readiness matrix

| Area | Evidence | Status / remaining condition |
|---|---|---|
| Input identity | 24 exact paths/trees, pre/post hashes identical; expected dataset hash matched | Read-only identity check passed |
| Package/runtime files | Pinned Python 3.10.20 and package versions/origins recorded; offline tokenizer-only imports worked | Environment inspection only; not a production runtime launch |
| Tokenizer + SFT masking | Exact base snapshot and actual P0 adapter tokenizers; fixed S120 encodings; allowed pure production helpers (`validate_example`, `tokenize_prompt_completion`) and CPU collator checks | Bounded local software/tokenizer audit passed; not model inference/training validation |
| 8B model load / adapter application | No model weights loaded | NOT OBSERVED; must be checked in a separately authorized, reviewed bounded engineering release |
| Actual inference request/input accounting | No generation or model request | NOT OBSERVED; future per-call input counts must be durably metered before invocation against 16M cap |
| GPU allocation/time | CUDA hidden; no GPU used | NOT OBSERVED; device-hours require allocated GPU UUID/count × monotonic elapsed accounting; 4-hour cap not empirically validated |
| ALFWorld/environment compatibility | No environment constructed/reset/stepped | NOT OBSERVED; must be validated only under a distinct authorized software/environment check |
| Training path/optimizer/memory | No training | NOT OBSERVED; batch/gradient accumulation, precision, optimizer state, activation/checkpointing, memory headroom, and exact GPU inventory are unverified |
| New B/C exposure balance | No new pool or paired run | NOT OBSERVED; exposure ratio and paired-slot/mask/batch requirements remain unevaluated |
| Campaign caps | Protocol arithmetic is documented in tokenizer audit | Budget design only; persistent counters and fail-closed stop wiring are not validated here |

## Future bounded-budget accounting (not authorization)

P3 arithmetic is retained without expansion: 8,496 generations, 9,792 environment operations including resets, and 138,240 output tokens. It includes 1,200 paid exact-prefix replay actions and no extra replay-compare model calls. Reuse source continuation; do not regenerate it. The 16M inference-input cap and 4 GPU-device-hour cap are future proposed limits, not consumed or validated in this task. Software smoke/development and training budgets must be separately specified and authorized.

Before any future freeze/release, an independent engineering review must close at least: actual model+adapter load and generation compatibility; genuine runtime module/config and cache provenance; exact allocated GPU UUID/count and supported memory margin; real input-token meter persistence and fail-closed behavior; training microbatch/gradient-accumulation/optimizer/checkpointing settings with measured peak memory; device-hour meter semantics and interruption accounting; CPU/GPU precision/backend determinism expectations; and environment execution compatibility. This report does not set those values or create a gate/argv/schedule.

## Prohibitions respected

No Qwen3-8B/P0 model load, neural generation, training, ALFWorld construction/reset/step, formal preflight/supervisor, policy replay, standalone project-level validator, pytest, G3, or G4 was run. The narrow pure production SFT helpers named above were intentionally exercised as authorized. No source scientific tree, prior evidence, or shared index was modified; no provenance commit/push was made. The only generated outputs are the Luna-owned audit deliverables and captured receipts listed in `RECORD.md`.
