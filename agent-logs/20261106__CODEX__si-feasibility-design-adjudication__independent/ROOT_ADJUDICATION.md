# Independent adjudication: next self-improvement feasibility design

Status: **DRAFT, NOT READY FOR SCIENTIFIC EXECUTION**. A real one-generation, one-environment-step P0 engineering probe completed; its `look` action did not complete the task. It provides no success-rate or training-effect estimate.

## Blocking correction to the proposed training objective

The proposal `SCIENTIFIC_FEASIBILITY_PROPOSAL.md`, SHA256 `c5f82b8382e90422ab4495d5d413e428f3dc7ee3296e4bff7a124f64d1ad5dc2`, section 3, says to divide by the batch weight sum and proposes an eight-example forward batch. Neither is the already specified training contract. The scientific contract in `TRAINING_SEMANTICS_SPEC_V1.md` uses one example per forward and one update over the complete accumulation window. Given `M` distinct examples and `K` designated examples, require `0 < K < M`; set `alpha = M/(M+3K)` and weights `4*alpha` or `alpha`. For an update window `U`, the objective is `sum_i w_i sum_t CE_it / sum_i n_i`, with the denominator the **unweighted** count of active shifted supervised tokens across the whole window. C1 uses weights of one. Do not divide by a window's weight sum or re-normalize per batch. A different objective may be proposed and reviewed separately, but must not be presented as this frozen contract.

If retaining a maximum update window of eight examples, perform one forward/backward per example, accumulate against that window's full token denominator and step once, including the final partial window. With one epoch and 16–128 examples, at most 16 updates per arm and 32 across two arms remain possible. The count of at most 524,288 padded positions across both arms assumes each of at most 256 example exposures has at most 2,048 padded positions; padding and all tokenization/forward calls need actual receipts. No training integration, model fit or dataset readiness is implied by arithmetic.

## Scope and resource interpretation

The 40 acquisition plus 20 feasibility-group targets are a proposed operational screen, not evidence of statistical independence. Independent creation/custody, semantic distinctness, group lineage, feasible tasks and unknown historical/model exposure remain unproved. A shared-account role separation cannot establish independent custody. Do not inspect protected historic data to manufacture it.

The proposed 5,200 generations and 8,540 reset-plus-step operations are conditional planned count ceilings, not a complete approved budget. They exclude at least model/tokenizer loads, training forward/backward/optimizer costs, tokenization and storage, CPU/native translations, cleanup and uncertain or incomplete external operations. No meaningful scientific execution should start before separately reviewed source, authentic dataset, complete resource bounds, isolation and stop rules are in place. Twenty paired units are descriptive feasibility evidence and cannot establish a precise population effect.

The draft remains available unchanged for provenance; this adjudication does not approve it or authorize another model/environment run. The original single-action clearance was consumed. No further live work occurred for this review.
