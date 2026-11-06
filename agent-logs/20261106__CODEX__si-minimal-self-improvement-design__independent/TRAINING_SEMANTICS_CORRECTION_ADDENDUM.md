# Correction to the self-improvement feasibility proposal: C1/C4 training

This addendum **supersedes the training-objective, forward-batch and accumulation statements in section 3** of `SCIENTIFIC_FEASIBILITY_PROPOSAL.md` and the corresponding training-budget interpretation in section 4. The original is preserved unmodified at SHA256 `c5f82b8382e90422ab4495d5d413e428f3dc7ee3296e4bff7a124f64d1ad5dc2`. The controlling previously reviewed contract is `TRAINING_SEMANTICS_SPEC_V1.md`, SHA256 `2969f9c1812babbd8488d8c10246cc99cbe295d36ec4e266daacb763c2d977fa`. My prior per-batch weight-sum denominator and eight-example forward with no accumulation were incorrect for this contract; do not implement or review them as an equivalent formulation.

Freeze the common dataset D with `M` distinct example records, `16 ≤ M ≤ 128`, and `K` distinct target repair records with `0<K<M`. The feasibility screen requiring repair rows from at least four distinct acquisition groups is separate: K counts **records**, not groups. Compute exactly once over the entire distinct dataset:

```
alpha = M / (M + 3 K)
C1: w_i = 1
C4: w_i = 4 alpha for target-repair rows, alpha otherwise
```

One forward pass contains **one example**. Accumulate exactly eight successive examples per optimizer update, except the final window which contains the remaining 1–7 examples. For the full realized update window U, let `n_i` be the number of active shifted labels for occurrence i and `A_U = Σ_{i∈U} n_i`; reject zero active labels and invalid masks. If `c_it` is native cross-entropy on each active token:

```
C1 update loss = Σ_{i∈U} Σ_{active t} c_it / A_U
C4 update loss = Σ_{i∈U} Σ_{active t} w_i c_it / A_U
native_i       = Σ_{active t} c_it / n_i
backward_i     = (w_i n_i / A_U) × native_i
```

The denominator is **unweighted active-token count for the whole update window**. Do not use `Σw_i`, `Σw_i n_i`, per-window alpha, per-example weight normalization, or a second division by eight. Use the native mean-loss path and exact shift/mask/EOS requirements in the controlling specification. Perform one zero-grad before the complete window, one backward per example, one gradient clip after all window backwards, and one optimizer step; the partial final window uses its actual `A_U`. Both arms must match source data, realized order/windows, initialization, optimizer, LR schedule, clipping, tokenization, trainable parameters and runtime; only the prescribed global weighting differs. An informative *synthetic* mixed example can demonstrate non-identical weighted gradients, but equal gradients for a particular real batch are not by themselves proof of an implementation defect.

For the proposed **one epoch** and one full pass per arm, the number of one-example forward/backward occurrences is M per arm and optimizer updates are `ceil(M/8)` per arm, including one partial final window when needed. Therefore the existing bound of **at most 32 total optimizer updates** is correct: `2 × ceil(128/8)=32`. With separately enforced post-tokenization sequence length ≤2,048 and no unaccounted extra forward passes, the existing ceiling of **524,288 padded token positions across both arms** remains valid: `2 × 128 × 2,048`; actual padded, nonpadding and active-supervised counts must be separately recorded, with supervised tokens included within—not added to—sequence totals. The bound is not 524,288 generated tokens or measured usage. Evaluate finite/nonfinite loss, masks and actual training counts before accepting a checkpoint.

The earlier **5,200 generations / 8,540 reset-plus-step operations** table is a planned nominal cap under the explicitly stated fixed successful-stage/attempt rules and no extra calls; it is not a complete cost envelope for failed or incomplete physical operations, retries, extra diagnostics, cleanup, unseen descendants, native translations or their unknown tails. Real CPU/GPU time, model/adapter load behavior, training memory fit, storage/network and the resource/timeout tail remain UNKNOWN. Before launch, set and enforce separate numeric failure and physical-resource limits, account for all previously started/open liabilities and independently verify the implementation; stop if any required value or effect is unknown beyond its admitted bound. This correction does not authorize training or any experiment.
