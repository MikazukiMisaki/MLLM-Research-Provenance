# SI-S01 feasibility correction addendum

Status: corrective, read-only addendum. The prior `ENGINEERING_ADAPTER_FEASIBILITY.md` and its JSON/hash receipts are preserved byte-for-byte; this addendum supersedes only their incorrect source/API conclusions. No code, tests, runtime, model, tokenizer, CUDA, ALFWorld, SSH, preflight, or supervisor was invoked.

## Exact source inspected

Static Git-object inspection was performed at:

- `9bc15b593ec6144915762a2fb1b172e063fe2c48`
- `d7a82acb510157ab7ba5439d790816c5c948439f`

The three implementation files central to the correction are byte-identical across both revisions. The adjacent collector is also identical; the evidence ledger changed between revisions, so its hashes are recorded separately rather than represented as equal:

| Correct path | 9bc SHA-256 | d7 SHA-256 |
|---|---|---|
| `src/self_improvement/si_s01/runtime.py` | `e33f96daf677480c81f71fb4c9d04e9e30050e9084cb285cff5e5600629da3e6` | `e33f96daf677480c81f71fb4c9d04e9e30050e9084cb285cff5e5600629da3e6` |
| `src/self_improvement/si_s01/contract.py` | `43350414e313273eb9747e879c70e24c90a044562e509a4bfff20fd26104d507` | `43350414e313273eb9747e879c70e24c90a044562e509a4bfff20fd26104d507` |
| `src/self_improvement/si_s01/gate.py` | `cde29b94d87070a117825cc1ec80aec23f098ee14550690b5e820d3fe15ea6a8` | `cde29b94d87070a117825cc1ec80aec23f098ee14550690b5e820d3fe15ea6a8` |
| `src/self_improvement/si_s01/collector.py` | `02c6a0fe8a213885bf46801847d517f1ee564f97de7c026762af8a92f401ca6a` | `02c6a0fe8a213885bf46801847d517f1ee564f97de7c026762af8a92f401ca6a` |
| `src/self_improvement/si_s01/evidence.py` | `d85882513e41d62e99a5fd51b3acb39311a52dfb20ce17523926eb9555e9239a` | `4048468a1666d23547f0d48cfcd42d20edd526893498a0d91e7434ad3cb5a1f0` |

The earlier `STATIC_API_RECEIPT.json` instead indexed `src/self_improvement/si_p3/{contract,collector,runtime_backend,runtime_environment,runtime_gate,runtime_ledger}.py`. In particular, its `runtime_backend.py` finding (“no `LiveProducer`/`_raw`”) was true only for that helper module and was incorrectly generalized to SI-S01 as a whole. The actual SI-S01 API is in `src/self_improvement/si_s01/runtime.py`.

## Corrected implementation findings

- `si_s01.runtime` defines `LiveProducer.load`, `LiveProducer._raw`, `LiveEnvironment`, and `run_worker`. `LiveProducer.load` requires `permit.plan.evidence_class == 'live_source_only'`, binds actual package origins, checks the one visible CUDA UUID, creates the one-byte context before weights, loads the frozen Qwen/P0 adapter, and checks device/dtype/adapter state. `_raw` requires a pre-reserved active ledger unit whose identity matches the source slot/generation and produces at most 16 tokens. These are static source findings only, not executed or independently runtime-validated here.
- `si_s01.contract` supports both `synthetic_software_fixture` and `live_source_only`; it is not synthetic-only. However, its current `Plan` is specifically the fixed A96 plan: 96 unique slots, fixed per-family `SOURCE_QUOTAS` and hash order. For `live_source_only`, `bind_plan` requires the exact frozen `METADATA_SHA256` reservation metadata.
- `si_s01.gate.Permit` is an actual SI-S01 permit. Its current authentication is deliberately scoped to `purpose == 'SOURCE_ONLY_A96'`, binds the A96 protocol/task SHA and exact metadata, and requires `status == 'PREFLIGHT_ONLY'`, `maximum_launches == 1`, and a separate fresh independent launch clearance before a live invocation. It is not a general engineering single-task permit.
- `si_s01.evidence.Ledger` reserves physical units by calling `call(slot, kind, index, ...)`; it rejects a slot not present in `plan.slots`, and `_raw` checks that the active unit identity is the source generation for that exact slot/index. Thus the LiveProducer cannot be safely invoked by inventing an A96 `Plan`, fabricating a `Permit`, or bypassing reservation.
- `si_s01.collector.Collector` is the real source-only collection path, not an inference that A96 is synthetic-only. Its current live plan runs the planned source schedule, and its collector loop can continue across source steps up to the protocol horizon. `run_worker` enters that collector and then writes the source audit report.
- `LiveEnvironment` delegates environment construction/reset/step to `si_p3.runtime_environment.ReadIsolatedEnvironment`, while the SI-S01 collector enforces the returned pool seed and records reset/action operations. This use of a P3 helper does not negate the SI-S01 live wrapper.

Accordingly, retract these prior claims as stated at project scope: “no LiveProducer API,” “A96 collector is synthetic-only,” and “existing authenticated producer gate requires the four-prompt/4-generation/88-token P3 diagnostic.” Those describe the old P3 helper APIs, not the SI-S01 live source implementation. The unrelated P3 `replay_twice()` behavior must not be presented as the SI-S01 `LiveEnvironment` execution path.

## Minimum legitimate engineering-scope adaptation (design only)

The real blocker is scope/authorization typing, not absence of a live producer. To reuse SI-S01 live components for a separate one-task engineering observation without impersonating A96, a future reviewed implementation would need a distinct, explicit engineering scope interface:

1. A separate immutable engineering plan/permit schema with its own purpose and authorization domain, bound to exactly one explicitly approved historical source identity, exact source/proposal/runtime/input hashes, output identity, device/PID ownership evidence, and strict ceilings. It must not call the object an A96 `Plan`, claim the A96 metadata hash, or satisfy the `SOURCE_ONLY_A96` gate by fabricated fields.
2. A typed source-unit reservation contract understood by the live producer: the selected identity and generation index must be durably reserved in a ledger before `_raw` can run; completion/failure must preserve the same unit identity and raw physical accounting. Either make `LiveProducer` consume a narrow scope/permit protocol that is valid for both A96 and this separately authorized engineering mode, or add a separate engineering producer adapter that delegates to shared guarded loading/generation primitives. Do not mock `Permit` or manually populate `Ledger.units`.
3. A matching one-unit orchestrator with the explicitly bounded source/replay behavior and fail-closed stop rules. Preserve existing CUDA UUID, process ownership, frozen-model/adapter, tensor and event-evidence checks; do not weaken A96 checks or widen its authorization to accommodate the engineering task.

This is the minimum interface boundary inferred from static call contracts, not a code-change instruction or launch proposal. Exact ceilings, route trust, historical input validation, independent review, and fresh authorization remain separate prerequisites. No source PASS or runtime readiness follows from this correction.

## Historical first-source evidence remains a separate issue

The bounded first-row/reset capture and its hashes in the preserved V2 artifact are not changed by this implementation correction. That historical reset record binds the recorded nominal seed and transition but does not contain the internal TextWorld pool seed or game RNG counter. Therefore, exact internal RNG-state replay remains unsupported by that historical evidence. This limitation is independent of the SI-S01 API/path correction and must not be used to claim either a code defect or successful runtime replay.

## Evidence and scope

The path and symbols above were checked using `git show`/`git grep` against Git objects only. No repository worktree or original report was changed. No imports/tests/project validators, model/tokenizer/CUDA/environment/SSH, preflight, supervisor, or scientific call occurred. No launch release exists in this addendum.
