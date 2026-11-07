# C-low budget addendum: exact token totals

This addendum supplements, without changing, resource-envelope revision 2
SHA256 `e84bc6697e6580ff4d861fabdd556ee6b9d8d7533f944b6380f906709b6f92d6`.
The revision-2 independent review gives a **conditional arithmetic PASS**, not
preflight or execution approval.

The historical C run observed **695,872 input tokens and 6,240 supervised
tokens**. The reviewed historical `9bbaa12c2d8177a60ec5a74ed2f970ef29a57bce`
gate derives exact expected totals from the arm's frozen protocol; when those
totals are passed to `train_from_p0`, its pre-encoded token totals must equal
them exactly. It separately rejects totals exceeding the frozen **700,000 /
6,240** input/supervised upper bounds, and checks the prescribed per-example
supervised count when supplied. These checks occur after tokenizer loading and
encoding but **before base model loading**. A mismatch is a stop even when the
counts are below the upper bounds; tokenizer load/encoding and prior gate/hash
work may already have incurred real cost.

For the contemplated C-low path, the proposed expected C totals are
**695,872 / 6,240** only if the actual independently authenticated derived
protocol, dataset, tokenizer and complete gate confirm that same binding.
Historical observations alone do not establish the new live binding. The
future exact-entry review must verify these values and that `expected_totals`
and per-example constraints are actually passed to the trainer; it must not
remove or loosen those checks to make a run fit. Any disagreement, missing
binding, tokenization drift or inability to account for preceding work means
STOP/UNKNOWN, with no retry or model-load success claimed.

The actual destination filesystem and enforceable output quota, complete
read/mmap/native I/O accounting, external process/device monitoring, final
cleanup and physical tails remain unverified. The proposal remains **NOT
READY**. No real gate, preflight, model, environment or scientific work was
performed for this addendum.
