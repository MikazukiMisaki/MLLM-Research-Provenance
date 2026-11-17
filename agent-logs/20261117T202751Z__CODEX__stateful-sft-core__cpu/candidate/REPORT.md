# Injected CPU stateful SFT core, research candidate / HOLD

`stateful_core.run_cpu_research_core` is an isolated CPU-only candidate that accepts an already initialized model and 16 ordered token/mask rows. It constructs one AdamW optimizer, keeps the same model/parameter/optimizer identities through four epochs, processes microbatch1 with accumulation4, and records 64 microbatches / 16 optimizer steps. It uses causal shift and sum of completion losses divided by the active completion-token count across each four-row group. It validates full token arrays, exact completion-only masks, EOS/pad, vocab and 4096 total-token software limit without truncation, rejects missing/nonfinite loss, gradient, parameter or optimizer states, and calls a supplied checkpoint callback exactly once only after step16 with `FINAL_ONLY_NO_BEST`. Model is supplied by the caller: no product is loaded or authenticated by this function. Callback completion is only a caller claim; this is not a real checkpoint implementation.

This is **not a security sandbox or executable production release**. Generic Python callers can pass arbitrary objects or alter code. `run_real_training` always raises, regardless of caller declarations. The CPU-only requirement and single final callback narrow this research example, but do not themselves authorize or protect a production process. No actual sample, Qwen/PEFT, adapter, environment or GPU was loaded.

## Exact relationship to native_update

| Concern | Native `run_one_update` | This candidate |
|---|---|---|
| Model / source | Caller supplies reviewed fresh P0 producer; function checks architecture/names/EOS; owner must bind identity | Caller injects CPU model; no P0, LoRA, tokenizer or provenance validation |
| Rows / schedule | Four `Row(prompt, generated)` values, one step per call | 16 explicit token/mask rows, four fixed-order epochs, 16 steps |
| Optimizer | Constructs AdamW each call; repeated calls reset state | Constructs one AdamW for entire injected run; fixed lr3e-5, betas .9/.999, eps1e-8, no decay, non-fused |
| Loss | Shifted logits/labels, float logits, sum ignored-prompt CE divided by total generated tokens in four rows | Same shift, float conversion, sum/active-token normalization for each four-row group |
| Bounds / EOS | prompt+generated <=4096, <=16 generated, vocab and loaded tokenizer/model EOS/pad checks | Same software length bounds and structurally injected vocab/EOS/pad values; no runtime tokenizer/model identity verification |
| Checkpoint | Saves LoRA adapter once after one update; separately owned readback/reload and effects | One untrusted injected callback after all 16 steps; no file, LoRA adapter, checkpoint hash, readback, reload or durable owner |
| Budgets / state | effects delegated to owner; configured source/handoff and seed | No effect owner, no CPU/GPU/wall/I/O/model budget, no identity or immutable source handoff; explicit research HOLD |

Both paths can observe a failure after an optimizer step; this candidate propagates it, never automatically retries, and must not be treated as rollback. A failure after completed model operations can leave mutated model/optimizer state. The caller must handle that state as unknown/failed. The 4096 limit is a software constraint only; actual model context and memory remain unverified. Exact comparison diff and reference source hash are `native-to-core.diff` and `reference-hashes.json`.

## Actual CPU checks

The pinned Python / PyTorch CPU test directly calls this candidate with a tiny fictional injected model and 16 fake rows. One positive checks the same model and optimizer through the recorded 16-step sequence, exact row order and one final callback; a negative rejects malformed mask and nonfinite model loss before callback and checks the real entry is held. Command is captured in the task handoff; aggregate process exit 0 (`test-output.log`, `test-output.exit`). A separate fictional run saves all 16 history records to `synthetic-trace.json` with exit 0 (`trace-run.log`, `trace-run.exit`). This tests the current core's orchestration only; it does not prove real-model numerical behavior or complete safety.
