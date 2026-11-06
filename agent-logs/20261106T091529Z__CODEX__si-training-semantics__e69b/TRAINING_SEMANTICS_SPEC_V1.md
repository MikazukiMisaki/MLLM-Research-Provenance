# C1 C4 production training semantics

**Scientific contract for implementation and independent review.** Scope: one example per forward, one device, fixed C1/C4 products. This specifies a candidate objective; actual inputs and production acceptance remain unestablished. It does not release execution or the separately interrupted engineering work.

1. **Data and provenance.** Bind one permitted, separately addressable dataset D, its version, exact ordered records, encoding, and trustworthy target-family labels. Let M>0 be its distinct example-record count and K its target count, 0<=K<=M. Existing credible provenance must establish development use, acquisition/selection history, label meaning, allowed content and loader reach; hashes bind bytes but do not establish these facts. Do not inspect protected originals or mixed containers to create this evidence. Freeze actual epochs, exposure order, update windows and final-window handling. Never substitute historical 312/8 counts, four epochs, 16-item updates or 78 updates. Permitted exposed development tasks can support exploration; independent task evidence is required for corresponding new-task generalization claims.

2. **Chosen treatment.** Normalize once over D's distinct records, before repeated exposures, using:

       alpha = M / (M + 3K)
       C1: w_i = 1
       C4: w_i = 4 alpha for target records; alpha otherwise

   Only the dataset sample mean of C4 weights is fixed at one; exposure, token and individual-update means need not be one. Do not substitute token normalization, a weighted denominator, or per-update renormalization. C4/C1 compares the complete weighted recipe, including changes in gradient scale, clipping and optimizer dynamics. If K=0 or K=M, C4 collapses to C1: no weighting contrast exists. Real M/K and labels are required; 26/7 and 13/14 are not defaults.

3. **Loss and accumulation.** Position t predicts labels[t+1]; ignore the last logit. Prompt/padding labels must be -100; attention masking alone is insufficient. Freeze completion/EOS treatment and reject invalid vocabulary labels or any example with zero active shifted labels. Let n_i be that active count, c_it the native token cross-entropy, and U the complete ordered occurrences in one optimizer update:

       A_U = sum(i in U) n_i
       native_i = sum(active t) c_it / n_i
       backward_i = w_i * n_i / A_U * native_i
       L_U = sum(i in U, active t) w_i * c_it / A_U

   Preserve the native mean-loss path: num_items_in_batch=None, shift_labels=None, ignore_index=-100, logits_to_keep=0, with verified loss identity, wrappers, masks and numerical semantics. A nondefault external denominator would invalidate this scaling. C1 must retain the native reference, not silently replace it with a different CE implementation. One zero-grad, all backwards, one clipping operation and one optimizer step belong to each U. No second division by accumulation count; no microbatch clipping, dropping failed rows or recomputing A_U around omissions. Multi-example forwards or distributed reductions require a separately reviewed extension.

4. **Matched controls.** Both arms start afresh from the same authenticated P0/adapter and optimizer initialization. Match encoded data, realized order/windows, exposure dose, trainable parameters, optimizer, LR schedule, clipping, dtype and runtime. Bind the RNG construction and realized schedule, not merely equal seed numbers. Only the declared weighting differs. Keep separate arm/output identities; use the prespecified final product, with no best-checkpoint selection. Preserve the frozen baseline and historical trainer.

5. **Errors and accounting.** Missing authority, labels, bindings or an informative contrast means NOT_READY before use. During execution, mismatches, nonfinite values, loss-contract violations or resource/evidence failures yield INCOMPLETE and stop; no silent skips, fallback normalization, retry or resume. A possibly mutated optimizer or partially saved adapter is not rolled back or accepted. Preserve restricted evidence and charge started/failed work. Record unobserved cleanup tails as UNKNOWN, with a supported conservative bound if available, never zero or a claimed exact charge. Bind actual input, padding and supervised-token counts, updates, acquisition costs if needed, resource limits and load-through-cleanup windows; this objective supplies no budget allowance.

6. **Independent acceptance evidence.** Use permitted invented fixtures to compare C1 with the native reference's losses, pre-clip gradients, optimizer states and updates at declared tolerances; independently check C4's formula with unequal lengths, homogeneous/mixed windows and a partial final window. Reject changed labels/order, empty supervision and external loss denominators. Verify actual runtime dispatch and accounting separately before production acceptance; arithmetic or source consistency alone is insufficient. Release only allowed aggregate receipts, never protected prompts or trajectories.

Basis: PROPOSAL_V3, the native-loss audits, integration review and normalization note; exact document bindings are in SOURCES.sha256. Historical-dose examples in those sources do not override this contract.
