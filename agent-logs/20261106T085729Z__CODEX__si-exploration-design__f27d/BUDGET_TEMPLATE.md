# SI exploration budget and evidence template

Status: planning only. No inputs, launch budget, process or exact experimental schedule is approved by this template. Source: Luna's 2026-11-06 read-only preparation and the scientific design draft. Unknown values remain UNKNOWN; no totals are invented.

## Fixed identities, scope and exposure

- Experiment/review/source identifiers and hashes: UNKNOWN. Phase and run identities: UNKNOWN.
- Model, tokenizer, adapter, environment and software versions/hashes: UNKNOWN.
- Training input and evaluation input separately: opaque asset reference, version, permitted use, source history, bounded loader scope and relevant separation evidence: UNKNOWN. Do not expose task or trajectory contents in this template.
- Evaluation unit, eligible parents G, actual episodes per arm T, fixed schedule commitment, horizon, randomization and sampling/decoding: UNKNOWN. Parent counts and episode counts are not interchangeable.
- Weight semantics, normalization, batch size, gradient accumulation, epochs, supervised masks and optimizer configuration: UNKNOWN.

## Each phase: acquisition; C1 training; C4 training; P0, C1, C4 evaluation; cleanup

For each phase separately record a prospective reservation and monitored stop threshold; actual known costs; unresolved liability and reason; phase state; unique run and operation identities; start, completion, failure and external supervision receipts; and hashes of authorized artifacts. Include all training, sampling, source filtering, model loading, failures and partial attempts. Prior sunk costs and new incremental costs must remain separate and be reported together where meaningful. No automatic retry.

- Physical model calls: started, completed, failed/open, exact available input and output tokens, and EOS counting convention.
- Training: rows, epochs, sample presentations, microbatches, padded and non-padded input tokens, non-ignored supervised tokens, optimizer updates, failed work.
- Environment: reset, step, replay and other physical calls, keyed by underlying operation ID. Avoid double counting wrapper events only when their linkage is proven.
- Resources: each device UUID and credible process identity, monotonic allocation start/end, device count, device-time and evidence quality; GPU allocator allocated/reserved peaks separately from device-wide NVML samples; elapsed time, CPU/RAM/storage and monitoring caps. A device-wide snapshot does not establish process ownership or a hard physical resource limit.
- UNKNOWN process/GPU identity, tail, missing receipt or missing cleanup confirmation is not zero cost. Preserve the full outstanding reservation, record known costs and unresolved tail separately, and halt further work. Count actual overrun rather than clipping it to a planned threshold.

## Conditional arithmetic, not availability evidence

For three newly evaluated arms with T episodes per arm, H=50, one generation and one action per step and one reset per episode: 3T episodes, at most 150T generations and 153T reset/step operations. If the actual frozen runtime limit is 8192 input and 16 output tokens per generation, token maxima are 1,228,800T input and 2,400T output. Source acquisition, data preparation, training, retries, other environment calls and unresolved tails are additional and currently UNKNOWN.

An optional planning threshold of 1.5 device-hours per training arm and 1 hour per evaluation arm totals six device-hours for sequential use of one device; this is a proposed stop condition, not a runtime prediction, full budget or physical hard ceiling. An optional full P0 episode has a separate proposed 0.5-hour threshold and, under H50 assumptions, up to 50 generations and 51 reset/step operations. Neither is an authorization or proof that any eligible episode exists.

A historical single-action engineering result is not a basis for estimating full-episode duration, training memory or usable task count. Determine actual input, resource and total budget values before the relevant run.
