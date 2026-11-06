# Independent review: hard-disabled one-action candidate

**Decision: prior two isolated semantic counterexamples are rejected; additional offline record-consistency gaps remain. Fake tests reproduced; no real execution clearance.** This review covers only the exact source/fixture bytes described in the candidate `REVIEW_HANDOFF.md`. The candidate itself hard-disables the real worker, real ports and real supervisor. A later enabled composition would be new code requiring a new review.

## Scope and reproduced evidence

All 14 handoff-pinned source/test/fixture SHA256 values matched both before and after the independent test. Main exact hashes: `candidate_supervisor.py` `926c51937c3d6517b5ce260117963921158b63d48928efd47466f9adb0e9d2f0`; `candidate_worker.py` `e1d0511df3e7a27ac408e4a0b860f4e759ba2abcddcfbe6e171e93da577c3268`; `semantic_audit.py` `7b2661f8aed1887576c5405757c064a3a4983a8e8ab97af15721798fc0fea264`; `capture.py` `93f343e57e640996f2832721d1d819f6c714500effe2e2308184a9f281f7336b`. The pinned interpreter independently reran the **15 fake-only tests**, exit 0; raw output and shell-observed exit are retained as `fake_test.*`. No true model, CUDA, adapter, environment or scientific call occurred, and the original candidate directory/fixture was not changed.

The reviewer separately reproduced the previous two synthetic, valid-chain mutations and an incorrect forwarded command. A guard-only input-token alteration was rejected with `tokenizer_guard_ids_mismatch`; an invalid recorded parser status for the otherwise grounded action was rejected with `parser_status_mismatch`; a modified forwarded command was rejected with `selected_step_action_mismatch`. The relevant fake fixture and current output use production prompt/parser functions but fake tokenizer/model/environment edges. The reproduced rejections are meaningful improvements for these particular mismatches, not proof that same-process telemetry is independently truthful.

All counterexamples below were applied **only in memory** to the already-synthetic fixture; the reviewer recomputed the guard binding and core chain as necessary. `counterexamples_v2.stdout` records the actual accepted/rejected results, and `counterexamples_v2.exit` is 0. A trustworthy anchor retained before mutation would detect changed core bytes; the existing observer is explicitly local and not trusted independent storage. These examples are not evidence that any original record was altered or any real event happened.

The earlier `counterexamples.stdout` is retained; v2 added a direct check against the frozen fake tokenizer and the action-map-hash case. The current script corresponds to the v2 output.

## Finding 1: public and full action lists can contradict

Severity: **offline record validation gap for a successor**, not proof of a defect in the untouched fake fixture. In `semantic_audit.py:76`, validation checks equal full-command/grounding counts and uniqueness of the *selected* command, but does not check that `public_actions == sorted(set(full_commands))`, which is a precondition independently imposed by the production core.

Synthetic reproduction: append an additional full command and corresponding grounding to `initial_state`, leave the public action list, selected `open` command and rest of the record unchanged, and reseal the core. `verify_joint` returns acceptance even though the public/full lists contradict. Before carrying the validator into a real successor, validate action list types, full/grounding lengths and the same public action derivation as the core, with both selected and unselected discrepancy cases.

## Finding 2: recorded prompt and action-map hashes can be wrong

Severity: **offline evidence-integrity gap**. `semantic_audit.py:46` reconstructs the actual public prompt and compares prompt text; line 51 verifies the rendered prompt hash; line 67 reconstructs the action map. It does not verify the separate stored `policy_returned.prompt_sha256` or `action_map_sha256` against those values. Independent synthetic tests changed each recorded hash to 64 zeros, resealed the core and left content unchanged; each contradictory record was accepted. A successor should recompute and check both recorded hashes or remove redundant fields through a separately reviewed schema change.

## Finding 3: malformed terminal state can be accepted

Severity: **offline record validation gap**. The original core refuses a post-step `won` or `done` that is not an exact boolean and also requires a valid post-step feedback/facts representation. `semantic_audit.py:72` checks selected ID, forwarded command and grounding, but does not check the recorded post-step terminal and feedback/fact field types. In the synthetic reproduction, changing `step_returned.won` from `false` to the string `not_a_boolean` and resealing the core was accepted. Validate the required terminal/post-state schema against the core's contract before interpreting a step as validly returned; this does not claim task success or failure.

## Trust boundary: coordinated tokenizer and guard records

The new capture comparison catches a guard-only input ID change, but `semantic_audit.py:53` compares two records from the same producer and does not independently tokenize the recorded rendered prompt. A synthetic change to both capture IDs and guard IDs from `[1,1,1]` to `[2,1,1]`, followed by resealing, is accepted even though the bound fake tokenizer returns `[1,1,1]` for the original recorded prompt. This is the **explicitly disclosed same-trust-domain limitation**, not evidence of actual tampering, and cannot be resolved merely by comparing another same-process hash. A real design must either retain that limitation in its claims or introduce independently bound tokenization/instrumentation and separately retained anchors.

## Remaining real-run gaps

The source includes a static `cuda:0` loading sketch, not a real executable release; its placement behavior would differ from an earlier automatic device-map treatment and has not been justified as a replacement. The proposed 24,576 MiB floor and 1 MiB display margin are unvalidated assumptions. Real 8B/PEFT loading and peak CPU/GPU memory, CUDA tensor capture, allocator/offload hooks, continuous shared-device monitoring, parent-death and escaped-process handling, complete native/import access closure, actual own-task ALFWorld step and trusted external anchoring remain untested together. The original five-shard file scan's exit 1 and scope deviation must remain in provenance; five matching local cache-reference hashes do not create an independently authenticated upstream model identity.

The fake run's `ONE_STEP_RETURNED` is not evidence of agent effectiveness. Missing/failed/torn records and physical cleanup uncertainty must remain unknown, not zero cost. No historical protected task, trajectory, schedule or source log was opened in this review.
