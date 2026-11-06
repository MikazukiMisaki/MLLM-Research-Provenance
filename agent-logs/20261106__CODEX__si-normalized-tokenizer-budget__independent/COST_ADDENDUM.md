# CPU tokenization accounting after the own-task witness

This addendum accounts only for three explicitly identified new CPU checks, separate from the earlier SI-E2 tokenizer activity whose token lengths were not recorded. The earlier SI-E2 failed/open model-load unit and its allocated device interval remain as recorded in the prior cost addendum; this note does not erase or reconcile other project campaigns.

1. The first partial-history check loaded the local tokenizer once and tokenized four prompts for 816 input tokens.
2. The real-tokenizer/fake-model integration loaded the tokenizer once, tokenized one 177-token prompt and encoded a fabricated action ID as four tokens. The fake model returned those encoded IDs; they were not model-generated tokens.
3. The normalized-goal correction loaded the tokenizer once and tokenized four prompts for 816 input tokens. Its prompts differ from the first check even though their token counts happen to match.

Together these three CPU checks record three tokenizer loads and ten tokenizer encode/call invocations, processing 1,813 token IDs in the named calls. Chat-template rendering is additional CPU work and is not counted as a tokenizer encode call here. They record **zero model-weight loads, zero actual model generations and zero environment calls**. Their reported process CPU seconds sum to approximately 12.32 seconds; their individual peak RSS figures cannot be added to infer concurrent peak memory. These are process-reported measurements, not complete device-hours or full native/descendant resource accounting. Each check observed CUDA uninitialized.

The earlier own-task environment witnesses remain four resets plus 16 steps in total, with four constructions and loads, before considering separately scoped prior P0 or R19 work. These tokenizer checks add no environment operation. No scientific effect or complete experiment budget follows from this arithmetic.
