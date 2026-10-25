# SI-E1 tokenizer and supervision-mask audit

Status: `AUDIT_ONLY_NOT_RUNTIME_OR_TRAINING_READINESS`.

## Scope and exact inputs

This was a local-only CPU audit using pinned Python 3.10.20, offline Hugging Face settings, hidden CUDA devices, and `local_files_only=True`. No 8B model/adapter weights were loaded; only the tokenizer files from the exact cached base snapshot and the actual P0 `final_adapter` were loaded. No generation, training, ALFWorld construction/reset/step, formal preflight/supervisor, project validator, or pytest was run.

The base tokenizer revision was `b968826d9c46dd6066d109eabc6255188de91218`; the adapter tree is the recorded P0 final adapter. All 24 bound files/trees in `input_bindings.json` were present and before/after-identical. Dataset SHA256 was `c547e8f0c5988b29288f2a097169c7859741b7d4f53f222af31f5e2889d516cf`. Exact package versions and origins, source/provenance Git state, and all input hashes are recorded in that binding file.

## S120 tokenization and template

The two tokenizer loads each resolved to `Qwen2TokenizerFast`, vocabulary size 151,669, EOS `<|im_end|>`, PAD `<|endoftext|>`, with PAD and EOS distinct. The effective rendered chat template was 4,168 bytes with SHA256 `a55ee1b1660128b7098723e0abcd92caa0788061051c62d51cbe87d9cf1974d8`. For each of the 120 selected compact-manifest rows, the `enable_thinking=False` public P0 rendering matched the stored prompt; the full encoding began with the separately encoded prompt; all sequences fit the frozen 2,048-token limit without truncation; and target EOS remained present.

| Measure, one S120 pass | Base snapshot | P0 final-adapter tokenizer |
|---|---:|---:|
| Rows | 120 | 120 |
| Full non-pad input tokens (prompt + target) | 64,922 | 64,922 |
| Prompt input tokens | 64,322 | 64,322 |
| Supervised target tokens including EOS | 600 | 600 |
| Causal-shift loss-bearing target tokens | 600 | 600 |
| Full-sequence length min–max | 277–876 | 277–876 |
| Prompt length min–max | 272–871 | 272–871 |
| Any >2,048 / truncation | No / none | No / none |

Across all 120 rows there were zero length or token-ID-sequence digest differences between the two tokenizers. This is an observed equivalence on this fixed S120 only, not proof of universal equivalence. Tokenizer files are not byte-identical: tokenizer JSON, vocab, and merges match; tokenizer config differs (base `d5d09f…`, adapter `443bfa…`); adapter additionally has `added_tokens.json`, `special_tokens_map.json`, and `chat_template.jinja`. Those differences are preserved in `TOKENIZER_MASK_AUDIT.json` and must not be normalized away.

The manifest stores per-row lengths, prompt/target/map hashes, bare action ID, selection/quality provenance, and token-ID sequence digests—not prompts, full training rows, or token-ID arrays. S120 is a frozen identity/metadata accounting set, not a claim that training occurred.

## Labels and CPU collator

The installed production `tokenize_prompt_completion` helper and installed TRL collator were exercised on CPU. Both ordinary configured padding and a software-only forced `PAD == EOS` case passed: padded attention entries were zero; prompt and padding labels were `-100`; a real terminal EOS remained supervised; and causal-shift target counts were `[5, 5]` in the two-row toy batch. The batch had lengths 506 and 398, padded shape `[2, 506]`, and 108 padded slots. The forced PAD==EOS case is specifically a software robustness check; the audited real tokenizer has PAD != EOS.

Production-helper negative software cases rejected a malformed bare action ID and a synthetic 25,002-token overlength input (including the would-truncate case) with truncation prohibited. These are software checks, not new-task data or scientific observations.

## Token accounting and exposure limits

Do not combine these quantities:

- **Generation tokens:** none were generated in this audit. A source dataset target is not evidence of generated tokens.
- **Training supervision:** the fixed S120 metadata projects to 600 supervised target tokens per arm for one pass, or 1,200 per arm for two epochs, including EOS; this is conditional arithmetic, not training exposure.
- **Non-pad input:** one S120 pass is 64,922 tokens. Two epochs project to 129,844 per arm if exactly these 120 rows are used.
- **Padded slots:** no future training padding was observed. At the frozen 2,048 maximum, 120 rows × 2 epochs × 2,048 is 491,520 slots per arm. The broader protocol ceiling of 144 examples × 2 epochs × 2,048 is 589,824 per arm; neither is measured runtime consumption.
- **Future B/C pool exposure:** `NOT_OBSERVED`; paired-exposure ratio is not evaluable and has not passed.

The production source budget remains the P3 design arithmetic: 8,496 generations (4,800 source + 96 Stage-1 teacher actions + 96 Stage-2 teacher actions + 3,504 suffix), 9,792 environment operations including 192 resets (4,800 source actions + 1,200 exact-prefix replay actions + 96 teacher actions + 3,504 suffix actions), and 138,240 output tokens. The output calculation is `4,800×16 + 96×40 + 96×16 + 3,504×16 = 138,240`: Stage 1 uses the 40-token cap, while source, Stage 2, and suffix use 16-token caps. This is a correction to the cap description only; the frozen total is unchanged. Source continuation is reused; this adds no source generation. There is no extra replay-comparison model call. Do not charge the 1,200 replay actions as free, and do not add another replay.

The proposed 16,000,000 cumulative inference-input-token cap must be metered from actual per-call non-padding input token counts and durably accumulated before each call; no such future campaign usage was observed here. The proposed 4 device-hour cap must use the sum, across allocated GPU UUIDs, of allocated-device count × monotonic elapsed seconds / 3,600, with allocation boundaries and monotonic timestamps recorded. Wall-clock time alone is not GPU-device time. This audit used no GPU, so it provides no measured device-hour estimate. Software smoke/development and training resource budgets remain separate and unauthorized; they must not be hidden inside campaign totals.

## Captured activity

There were two successful worker passes: aggregate four tokenizer loads, 240 selected-row encodings per tokenizer, 240 P0 template renders per tokenizer, and four CPU toy/collator invocations. One earlier worker attempt exited 1 before tokenizer loading because of a Luna-local helper import/name error; its actual stdout/stderr and exit receipt are preserved, and it contributed zero tokenization/collator calls. The successful passes were retained without changing scientific code/data. Aggregates are reconstructed from their captured stdout and code paths in the finalizer receipt.

The authoritative machine detail is `TOKENIZER_MASK_AUDIT.json`; process-level receipts and raw stdout/stderr are in the sibling `*.receipt.json` files and `raw/` directory.
