> Publication copy: original SHA-256 `36b4b7a04bab4b1e02b5b7bcbbf51d23f64d6ecd53f1bdf10db9a89628c32ef5`. Location clarification: raw test artifacts remain local and are not published here.

# Exact-SHA independent review: combined owner and prompt binding

Candidate `5ade46b09faae340d7b9f7dd6dbf7c4ebe73f430`; compared complete delta from `73e7ade3b4e782b32c81551db386f279ae5573d4`, reviewed reachable production episode/gate path, verified clean isolated worktree and `git diff --check`. **Decision: FAIL for release/readiness; fake-only engineering evidence is useful.** Real entry stays disabled; no model, CUDA, ALFWorld, protected task or science unit was run.

## Blocking defect: final receipt ACK failure is treated as clean disconnect

`operation_owner.py:276–278` writes/validates `unit_observed` before sending the ACK. If that final `sendall` raises `BrokenPipeError`, `supervise_one` catches the exception as `ConnectionError` at lines 320–331. Its `complete` check relies only on `receipt_checked`, phase and active operation, all already changed by the successful ledger write; there is no record that the ACK was successfully sent. Thus it follows the clean-disconnect bounded-wait branch even when the worker did not receive an ACK.

`test_lost_final_ack.py` demonstrates this with an actual separate synthetic child and socketpair: child sends a structurally accepted final receipt, closes its end before receiving an ACK, then executes a fake file effect and exits 0. An independently instrumented wrapper observed actual `BrokenPipeError` from ACK send. Nevertheless the supervisor waited, reported `stop_reason=None` and return code 0, and the fake post-disconnect effect was observed. The final campaign remains `UNKNOWN_OR_INCOMPLETE`; this is not evidence that a real model or environment ran. Distinguish and persist ACK-send failure from post-ACK EOF and stop/mark UNKNOWN on the former; an ACK send alone still cannot prove receipt by the child, eliminate child actions during a grace period, or prove process-tree cleanup.

## Receipt and prompt binding evidence

Four independent acceptance assertions adapted only for the `bind_generation` API passed: the valid synthetic receipt is accepted, and per-generation input redistribution, per-generation output redistribution and final `won/lost` conflict are rejected. The existing code now records and compares per-generation input/output pairs rather than only their sums.

Two additional synthetic counterexamples remain accepted as `STRUCTURAL_MATCH`: (a) a `generation_returned.input_tokens` value inconsistent with its matching start and the owner ledger; (b) a `step_returned` moved before the corresponding generation started. The verifier selects event types separately, checks aggregate/per-type ordering, and does not validate the complete interleaving or all duplicated fields. These are deliberately forged fake files, not evidence of real corruption. Treat `STRUCTURAL_MATCH` as a subset of structure checks; require complete ordered event/accounting reconciliation and independently verified semantics before relying on real results.

The proxy now installs a check directly inside the existing `GenerationGate`, after its `generation_started` callback and before the original generate wrapper. Existing synthetic tests exercise a modified tensor in that callback and stop before the fake model; the owner binds prompt, rendered text, tensor digest and input length to the generation start. This fixes the previously demonstrated callback mutation path. It does not prove immutable CUDA buffers, trusted tokenizer semantics, secure same-process isolation, or absence of concurrent/native mutations after the final check. All arms would need identical reviewed behavior, and guarded results cannot be silently combined with historical unguarded runs.

## Other limits and retained evidence

Existing cross-process fake tests check early EOF, dropped generation ACK, mutation, observed overrun, normal and delayed exit and deadline stop. The supervisor remains one unit only; its process-tree cleanup and physical tail are UNKNOWN. Input trees, transitive source/package/interpreter bytes, complete cross-run budget, independent task custody, source-to-prompt isolation, device/energy/I/O costs and external outcome validation remain unresolved.

The focused synthetic suite with independent adapted acceptance and counterexamples ran 39 tests, real subprocess exit 0; the separately retained lost-final-ACK test ran one test, exit 0. Their successful status means the counterexamples were reproducibly observed, **not** that the implementation passed release review. Raw stdout/stderr and actual subprocess receipts are in the local review directory and are not uploaded in this publication. No scientific work was performed.
