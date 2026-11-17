# Fixed-product v2: stopped active run and EOS/budget evidence

Status: STOPPED FOR REVIEW; no launch, retry, continuation, new model call, tokenizer invocation or environment call from this Parallel task. This is a new non-overwriting coordination record; the live-output directory and other original evidence are not edited.

## Active process and stop

After the user directed no launch and review before execution, read-only process inspection showed an already-running supervisor PID 1675004, PPID 720131, using the fixed-product per-arm `batch-config-v2.json` (SHA-256 `258cde04c4965fc82c46c4b336f09389bcbdb0ede86c78bb19045dc03b4cbde4`) and worker PID 1676069. The live worker was on case C, candidate arm. To prevent additional execution before review, this task sent SIGTERM to supervisor PID 1675004 after verifying its command line, UID, and stable start tick 678526421. A subsequent process check found neither observed PID, and the GPU compute-app query was empty. This task did not receive the initiating session's direct wait result and does not assert its exit code.

The original output is `agent-logs/20261118__CODEX__fixed_product_per_arm__private/live-output` under the local research notes. Its six owner journals show 6 materializations, 6 environment constructions, 6 initializations, 6 resets, 6 model loads, and 199 generations reserved and returned. Environment steps were 199 reserved, 198 returned: the last reserved step is UNKNOWN, not a completed action or a model failure. Worker journals have 61,223 input tokens in prepared records and 995 output tokens in the 199 returned generations. These are log-based counts, not independent complete physical-cost measurements. Five owner logs report completed arms; the sixth records `stop or deadline before budget ACK` and `no_remaining_children=true`. Output is incomplete and no effect/generalization claim should be made without separate evidence review. Do not restart or use a replacement output to bypass this stop.

## EOS contract discrepancy: evidence before any fix

The original Luna plan declares `tokenizer_eos_id=151643`, `pad_token_id=151643`, allowed generation EOS `[151645,151643]`, and `max_materializations=4`. The v2 candidate retains allowed generation EOS and pad but permits 8 materializations; this is a real budget discrepancy and the observed log already records 6 materializations. An eight-materialization allowance cannot be treated as a mere implementation detail or retroactively authorized by this note.

The user's report correctly identifies that exact candidate `episode.py` rejects actual tokenizer EOS equal to pad, and the reused historical `_generation` also excludes output padding and requires final EOS not pad. If the plan's declared tokenizer EOS really equals the actual runtime tokenizer EOS, that production path fails. However, the fixed base's static metadata contradicts that declared tokenizer EOS:

- `tokenizer_config.json` SHA-256 `d5d09f07b48c3086c508b30d1c9114bd1189145b74e982a265350c923acd8101`: `eos_token` is `<|im_end|>`; `pad_token` is `<|endoftext|>`.
- `tokenizer.json` SHA-256 `aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4`: added-token IDs map those strings to 151645 and 151643 respectively.
- `generation_config.json` SHA-256 `2325da0f15bb848e018c5ae071b7943332e9f871d6b60e2ed22ca97d4cb993d2`: allowed EOS `[151645,151643]`, pad 151643.
- The six existing worker journals contain 199 returned sequences, all ending 151645; 199 parser events record `eos_last=true`. The first generation's observed effective model generation config had EOS `[151645,151643]` and pad 151643.

Consequently, the claim that this exact observed execution necessarily stopped before the first generation is contradicted by its saved production logs. Static token-file interpretation and the observed logs do not alone prove every tokenizer implementation/loading detail, nor do they establish that rejecting 151643 is scientifically appropriate. Do not silently change the pinned contract, patch the candidate, relabel the 199 outputs, or infer an intervention effect. Review the actual import/loading evidence and determine an explicit EOS policy; preserve the documented plan discrepancy.

The exact candidate runtime `episode.py` SHA-256 is `06922aed662e84c1366624600c361f64ca7fba1ee93daccf83ff8de7a174a21b`; worker SHA-256 is `1f2dadcf27530438e20ed96ab04f0fb7e6a7492662650008a7fefc098140e4fb`. Original plan SHA-256 `3df73994bc2aba5912959ab7c0970241cba071466f85a8ef440c4b57c5ca03ec`; candidate v2 remains frozen and unmodified by this review.

## Forward engineering option, not authorization

If a later independently approved design must respect the original cap of four materializations with separate arm processes, consider materializing each case once in a supervisor-owned private location, binding its hashes, and using separate verified read-only views for each arm. The shared artifact's ownership, lifetime, input verification, per-case/global budget and cleanup still need implementation and review. Do not alter the 4-materialization cap or start another batch merely on this suggestion.

Cross-thread messaging was unavailable when this record was prepared; this file is the shared handoff, not proof that any recipient read it.
