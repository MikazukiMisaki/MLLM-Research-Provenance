# Synthetic counterexample: unrecognized guard record

After the ten fake-record tests passed, a separate pure-function probe supplied an unrecognized guard status with a nonzero worker exit. The candidate correctly returned `INVALID_RECORDS_STOP`, but also returned `generation_budget_charge=0` and `generation_unknown=false`. Those latter fields could be misread as proof of zero work even though the record was uninterpretable. No real tokenizer, model, GPU or environment was invoked.

The original candidate and its receipt are retained; it must not be used as a physical cost oracle. A later revision should treat unrecognized or malformed operation evidence as unknown, charge at least the remaining authorized maximum when feasible, and explicitly state that actual excess work cannot be bounded from corrupt records. It must never convert invalid evidence into a zero-cost claim.
