# R19-G4-C01-C02 engineering freeze

Developer handoff only; independent exact-SHA review is pending. This record grants no Luna preparation, formal G4, preflight, launch, retry or scientific execution permission.

## Authority and identity

- Deduplication identity: `2026-10-23T035119Z__SOL__r19-g4-minimal-contract-repair-assignment__9c5a99`.
- Task: `/home/lizening/research-notes/agent-logs/2026-10-23T035119Z__SOL__r19-g4-minimal-contract-repair-assignment__9c5a99/SOL_RESEARCH_TASK.md`, verified SHA256 `d9e3b00a3b83f3a3ac250a5772b3cb41b7c4070f05515e2860218c761f7e02f4`; sibling user authorization and observed byte bindings were read.
- Additional **test-only** ruling: `/home/lizening/research-notes/agent-logs/2026-10-23T041035Z__SOL__r19-g4-fingerprint-test-scope__b0f8de/SCOPE_RULING.md`, verified SHA256 `de6a5b81f44c4c3adbecd5e765fded1d0667a8ecb838768c49088ce7ffb6e821`. Its independently reproduced cause and hash inventory remain in Sol's directory, untouched.
- Own worktree: `/home/lizening/wt-r19-g4-consumer-contract-repair`.
- Exact candidate: `85cbb92395e5e2420c2adeb1fa0634653e742910`; direct parent and executed-G3 identity: `2da980f631badc25086d12db60d128ff507d3ae6`.
- Local branch and live remote: `codex/r19-g4-consumer-contract-repair`; clean before/after final checks. Non-force push and live `ls-remote` equality are recorded in `evidence/source_push.*` and `evidence/remote_equality.json`; the separate GitHub connector also resolved this branch to the exact candidate. Old `codex/r19-source-contract-review-fixes` still resolves to exact2da.

## CONFIRMED: final delta

Only four files changed: the analyzer and three tests. `evidence/source_delta.patch` contains the complete incremental patch; its SHA256 is `a20d1dda6d65aa3be49ed3291946747deae952c239d369782dc2f9c9290db554`. `evidence/source_freeze.json` gives every changed file's old/new raw hash and all six changed/added production function hashes.

1. `_validate_local_inference_runtime` explicitly distinguishes flat v1 from nested v2, requires exact local-only booleans/transport, and rejects malformed, unknown and mixed representations. `validate_live_execution_provenance` calls it while retaining the original manifest as its hash input. All existing baseline, authorization, source, runtime, environment, gate, ledger and cost bindings remain.
2. `validate_live_exit_receipt` preserves integer-zero child exit, completed/live/not-interrupted status and receipt/status/log/events/branches authentication. It rejects empty/malformed/ambiguous identities and contexts and checks its event view against the persisted receipt-bound ledger. Legacy start envelopes must be first, unique and internally consistent. A journal without `run_started` requires the persisted sibling `launch_context.json`, authenticated by both receipt and final status. The helper cross-binds run/source/class/cwd/command/interpreter/superseded run, supervisor invocation, protocol/output paths, original runtime/environment context hashes, offline flags, config/data and recorded cache identity. `_supervisor_option` rejects absent/duplicate options; `_read_supervisor_object` rejects missing/nonobject input. No start event or original file is manufactured.
3. Receipt regression fixture now has its harmless child persist the legacy start bytes actually hashed by the supervisor. Provenance fixtures test explicit v1/v2 plus valid-shape/raw-hash and baseline-identity tampering. New contract fixtures exercise 85 software cases, including malformed shapes, receipt/launch/context/identity/environment/raw-byte rejection and self-consistent resealed commands with wrong protocol/output/mode.
4. Sol's test-only ruling resolves the historical fingerprint-test conflict without changing any frozen fingerprint or execution gate. The test authenticates exact2da Git objects and all 40 historical source spans, keeps current equality for exactly 39 unchanged entries, and constrains the analyzer AST delta to the two authorized existing methods plus four named helpers. Other definitions, imports, constants, classes and module control flow remain structurally identical. The missing exact Git object is an assertion failure, not a skip/fallback.

The production source, supervisor, collector, scheduler, parser, recovery/SFT/replay, scientific report/statistics calculations, protocol, budget, quotas, treatments, authorizations, amendments and fingerprint artifacts are unchanged. The source implementation fingerprint gate intentionally remains historical; this analyzer repair cannot authorize another G3.

## CONFIRMED: tests and original-data engineering validation

Pinned interpreter: `/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python`. Subprocess receipts record argv, timestamps, actual `subprocess.returncode`, environment presence and, for repository checks, clean exact HEAD before/after. `PYTHONPATH`, `PYTHONHOME` and `VIRTUAL_ENV` are absent. Pytest receives `-o pythonpath=src` as test import configuration; clean external processes bootstrap production modules from the candidate explicitly or use the real script entrypoint.

| Check | Actual exit | Result and raw evidence |
| --- | --- | --- |
| Final all-R19 focused | 0 | 246 passed; `evidence/final_focused.log` and receipt |
| Exact2da full regression, separate own detached baseline | 1 | 617 passed / 3 failed / 77 errors; `evidence/baseline_full.log` and receipt |
| Candidate full regression | 1 | 703 passed / 3 failed / 77 errors; `evidence/final_full.log` and receipt |
| Failure/error comparison | 0 | All 80 exact node IDs equal both the fresh exact2da baseline and archived exact2da log; no additions/removals. Parametrized IDs retain spaces. `evidence/regression_comparison.json` |
| Compile / incremental diff check | 0 / 0 | `evidence/final_compile.*`, `evidence/final_diff_check.*` |
| Original G3 integrity-only baseline | 1 | First three validators returned; exact C01 and C02 exceptions reproduced. `evidence/actual_baseline.*` |
| Original G3 integrity-only frozen candidate | 0 | All five production integrity validators returned; `evidence/actual_final.json`, `.log`, receipt and pre/post hashes |

The historical full-suite failures concern unavailable R12/R18 frozen artifacts and retain their exact IDs; they have not been repaired, recreated, skipped or marked accepted by developer authority. The authorized original G3 integrity path did not encounter those dependencies. Draft failures remain under `evidence/focused_draft.*`: the dirty-worktree gate failure genuinely resolves on the clean candidate; the old fingerprint-test failure resolves only through the approved test-only adaptation. Neither guard nor frozen manifest was bypassed.

`actual_integrity_only.py` loads the candidate analyzer in a fresh process from `/tmp` and invokes only `validate_event_ledger`, `validate_branch_evidence`, `validate_live_source_schedule`, `validate_live_execution_provenance`, and `validate_live_exit_receipt` on genuine originals. It does not call analyzer main, duration analysis or report rendering. Production constants, PROJECT_ROOT, receipt, source SHA and validators are not monkeypatched. The analyzer SHA, imported duration-module origin, executed-G3 SHA and returned statuses are retained. The final process hashes 48 inputs before/after, including original output/supervisor/archive, original launch config/gate/protocol and preserved predecessor output; every hash matches. Initial assignment-bound hashes are also asserted against Sol's inventory. Original completed G3 remains `260422ac02bd42a8b2929d7ef240526b`, source2da, child exit0; this new analyzer SHA does not replace that identity.

The nonempty synthetic integration uses actual parser, collector, durable journal, common path/K suffixes, validators and report code with only model/environment edges synthetic. It produces two source/branch units and 10 K arms. The child records production module origins, input hashes and executed functions; a separate real script CLI process successfully revalidates the synthetic bundle and idempotently renders its explicit-synthetic report. Separate synthetic wire-format unit fixtures exercise runtimev2 and absent-start launch proof. Those wire fixtures emulate required live schema fields solely for software testing and have no real child/scientific provenance. They are never passed off as a live report. See the retained raw tree `raw_final_focused/test_fresh_process_synthetic_s0/` and its compact unchanged copies in `evidence/synthetic/`.

As clarified by Sol, the required existing regression fixtures may start isolated temporary subprocesses that reject invalid supervisor/preflight authorization before model/ALFWorld construction. The harmless legacy-start fixture runs only a Python file-writing/print child. No official supervisor/preflight, original output, model inference, ALFWorld reset/action, G2/G3 retry or new scientific operation was run. Scientific cumulative expenditure remains the supplied 5142 model generations / 7949 environment operations, retaining the original 177 / 342. No old operation is replayed or reclassified.

## NOT VERIFIED / withheld

The live CLI's actual-data statistics/report end-to-end path and formal G4 remain unexecuted and unauthorized. The synthetic CLI uses its synthetic branch; its success is not evidence that the live CLI provenance branch ran. The separate genuine integrity calls supply that engineering consumer evidence only. Independent exact-SHA review remains for Sol; there is no developer review PASS, G4 scientific conclusion, Luna preparation release or launch clearance. No further concrete blocker was reached within the authorized five-validator path. No unsupported suspected defect is promoted to a finding.

Flags: `source_treatment_semantics_changed=false`; `scientific_execution_behavior_changed=false`; `offline_evidence_validation_behavior_changed=true`.

## Evidence custody and publication

This directory contains only developer-owned material. Raw software fixture trees and failed draft checks are retained locally. Compact evidence selected by `publication_manifest.json` can be published separately by the coordinator; this record itself does not claim upload. No shared INDEX/root inventory, Sol/Luna directory, old review/gate/disposition/clearance or original failed/completed evidence was edited or staged. Large original archive/data/weights are referenced by path/hash, never copied into this directory.

Dependency remains: developer freeze → Sol independent exact-SHA review → only on PASS, separate Luna read-only preparation → fresh user authorization → formal G4.
